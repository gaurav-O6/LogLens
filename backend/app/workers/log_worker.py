from datetime import datetime
from pathlib import Path
import traceback

from app.database.db import db
from app.models.job import Job

from app.services.processing_service import ProcessingService
from app.services.r2_service import r2_service



def download_uploaded_file(filename: str) -> Path:
    """
    Download uploaded log from Cloudflare R2
    to temporary worker storage.
    """

    temp_dir = Path(
        "/tmp/loglens"
    )

    temp_dir.mkdir(
        parents=True,
        exist_ok=True,
    )


    local_path = (
        temp_dir /
        filename
    )


    print(
        "[WORKER] Downloading from R2:",
        filename,
        flush=True,
    )


    r2_service.download_file(
        filename,
        local_path,
    )


    print(
        "[WORKER] Download complete:",
        local_path,
        flush=True,
    )


    return local_path





def resolve_log_file(file_reference: str) -> tuple[Path, bool]:
    """
    Resolve the actual log file.

    Returns:

    Path:
        File location

    bool:
        Whether file should be deleted after processing


    Uploaded logs:
        filename -> download from R2


    Demo logs:
        local path -> use directly
    """


    possible_path = Path(
        file_reference
    )


    #
    # Demo file
    #
    if possible_path.exists():

        print(
            "[WORKER] Using local file:",
            possible_path,
            flush=True,
        )


        return possible_path, False



    #
    # Uploaded file
    #
    local_file = download_uploaded_file(
        file_reference
    )


    return local_file, True





def process_log_job(
    job_id: int,
    file_reference: str,
):
    """
    Background RQ worker task.

    Handles:

    - R2 uploaded logs
    - local demo logs
    """


    from app import create_app


    app = create_app()


    with app.app_context():


        local_file = None

        cleanup_required = False


        try:


            print(
                f"[WORKER] Starting job {job_id}",
                flush=True,
            )



            job = Job.query.get(
                job_id
            )



            if not job:


                print(
                    "[WORKER] Job not found",
                    flush=True,
                )


                return



            job.status = "processing"

            job.progress = 10

            job.started_at = datetime.utcnow()



            db.session.commit()



            local_file, cleanup_required = resolve_log_file(
                file_reference
            )



            print(
                "[WORKER] Processing:",
                local_file,
                flush=True,
            )



            processor = ProcessingService()


            result = processor.process_file(
                local_file
            )



            job = Job.query.get(
                job_id
            )



            job.status = "completed"

            job.progress = 100

            job.completed_at = datetime.utcnow()



            db.session.commit()

            print(
                f"[WORKER] Completed job {job_id}",
                flush=True,
            )


            return result



        except Exception as error:


            print(
                "[WORKER] FAILED",
                flush=True,
            )


            traceback.print_exc()



            db.session.rollback()



            job = Job.query.get(
                job_id
            )



            if job:


                job.status = "failed"

                job.progress = 0

                job.error_message = str(error)



                db.session.commit()



            raise error



        finally:



            #
            # Remove temporary R2 download
            #
            if (
                cleanup_required
                and local_file
                and local_file.exists()
            ):


                try:


                    local_file.unlink()



                    print(
                        "[WORKER] Temporary file removed:",
                        local_file,
                        flush=True,
                    )



                except Exception as cleanup_error:


                    print(
                        "[WORKER] Cleanup failed:",
                        cleanup_error,
                        flush=True,
                    )



            db.session.remove()