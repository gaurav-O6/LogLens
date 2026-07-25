from datetime import datetime
from pathlib import Path
import traceback


from app.database.db import db
from app.models.job import Job

from app.services.processing_service import ProcessingService
from app.services.r2_service import r2_service


def normalize_file_reference(
    file_reference: str
) -> str:

    return (
        str(file_reference)
        .replace("\\", "/")
        .lstrip("/")
    )


def download_uploaded_file(
    filename: str
) -> Path:

    filename = normalize_file_reference(
        filename
    )

    temp_dir = Path(
        "/tmp/loglens"
    )

    temp_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    local_path = (
        temp_dir /
        filename
    )

    local_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        "[WORKER] Downloading from R2:",
        filename,
        flush=True
    )

    r2_service.download_file(
        filename,
        local_path
    )

    print(
        "[WORKER] Download complete:",
        local_path,
        flush=True
    )

    return local_path


def resolve_log_file(
    file_reference: str
):

    possible_path = Path(
        file_reference
    )

    if possible_path.exists():

        print(
            "[WORKER] Using local demo file:",
            possible_path,
            flush=True
        )

        return possible_path, False

    local_file = download_uploaded_file(
        file_reference
    )

    return local_file, True


def process_log_job(
    job_id: int,
    file_reference: str
):

    from app import create_app

    app = create_app()

    with app.app_context():

        local_file = None
        cleanup_temp_file = False
        r2_object = False

        try:

            print(
                f"[WORKER] Starting job {job_id}",
                flush=True
            )

            # -------------------------------------------------
            # LOAD JOB
            # -------------------------------------------------

            job = Job.query.get(
                job_id
            )

            if not job:

                raise RuntimeError(
                    f"Database job {job_id} does not exist."
                )

            # -------------------------------------------------
            # MARK PROCESSING
            # -------------------------------------------------

            job.status = "processing"
            job.progress = 10
            job.started_at = datetime.utcnow()
            job.error_message = None

            db.session.commit()

            print(
                f"[WORKER] Job {job_id} marked processing",
                flush=True
            )

            # -------------------------------------------------
            # RESOLVE FILE
            # -------------------------------------------------

            local_file, cleanup_temp_file = resolve_log_file(
                file_reference
            )

            r2_object = cleanup_temp_file

            print(
                "[WORKER] Processing:",
                local_file,
                flush=True
            )

            if local_file.exists():

                size_mb = (
                    local_file.stat().st_size /
                    (1024 * 1024)
                )

                print(
                    "[WORKER] File size:",
                    round(size_mb, 2),
                    "MB",
                    flush=True
                )

            else:

                raise FileNotFoundError(
                    f"Log file does not exist: {local_file}"
                )

            # -------------------------------------------------
            # PROCESS LOG
            # -------------------------------------------------

            print(
                "[WORKER] Entering ProcessingService",
                flush=True
            )

            processor = ProcessingService()

            result = processor.process_file(
                local_file,
                job_id
            )

            print(
                "[WORKER] ProcessingService returned",
                flush=True
            )

            # -------------------------------------------------
            # MARK COMPLETED
            # -------------------------------------------------

            job = Job.query.get(
                job_id
            )

            if not job:

                raise RuntimeError(
                    f"Database job {job_id} disappeared during processing."
                )

            job.status = "completed"
            job.progress = 100
            job.completed_at = datetime.utcnow()
            job.error_message = None

            db.session.commit()

            print(
                f"[WORKER] Completed job {job_id}",
                flush=True
            )

            # -------------------------------------------------
            # DELETE R2 OBJECT
            # -------------------------------------------------

            if r2_object:

                try:

                    normalized_reference = (
                        normalize_file_reference(
                            file_reference
                        )
                    )

                    r2_service.delete_file(
                        normalized_reference
                    )

                    print(
                        "[WORKER] Deleted processed R2 object:",
                        normalized_reference,
                        flush=True
                    )

                except Exception as cleanup_error:

                    print(
                        "[WORKER] R2 deletion failed:",
                        cleanup_error,
                        flush=True
                    )

            return result

        except Exception as error:

            print(
                f"[WORKER] FAILED job {job_id}",
                flush=True
            )

            traceback.print_exc()

            db.session.rollback()

            try:

                job = Job.query.get(
                    job_id
                )

                if job:

                    job.status = "failed"
                    job.progress = 0
                    job.error_message = str(error)

                    db.session.commit()

            except Exception as db_error:

                print(
                    "[WORKER] Failed to record job error:",
                    db_error,
                    flush=True
                )

                db.session.rollback()

            raise

        finally:

            if (
                cleanup_temp_file
                and local_file
                and local_file.exists()
            ):

                try:

                    local_file.unlink()

                    print(
                        "[WORKER] Removed temporary file:",
                        local_file,
                        flush=True
                    )

                except Exception as cleanup_error:

                    print(
                        "[WORKER] Temp cleanup failed:",
                        cleanup_error,
                        flush=True
                    )

            db.session.remove()