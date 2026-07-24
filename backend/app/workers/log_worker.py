from datetime import datetime
from pathlib import Path
import traceback


from app.database.db import db
from app.models.job import Job

from app.services.processing_service import ProcessingService
from app.services.r2_service import r2_service




def download_uploaded_file(
    filename: str
) -> Path:
    """
    Download uploaded log from R2
    into worker temporary storage.
    """


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
    """
    Decide whether file is:

    1. Demo local file
    2. Uploaded R2 object
    """


    possible_path = Path(
        file_reference
    )



    #
    # Demo local file
    #
    if possible_path.exists():

        print(
            "[WORKER] Using local demo file:",
            possible_path,
            flush=True
        )


        return possible_path, False




    #
    # Uploaded file from R2
    #
    local_file = download_uploaded_file(
        file_reference
    )


    return local_file, True









def process_log_job(
    job_id: int,
    file_reference: str
):
    """
    Background RQ worker.

    Handles:

    - Uploaded logs from R2
    - Demo logs from repository
    """


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



            job = Job.query.get(
                job_id
            )



            if not job:

                print(
                    "[WORKER] Job not found:",
                    job_id,
                    flush=True
                )

                return




            job.status = "processing"

            job.progress = 10

            job.started_at = datetime.utcnow()



            db.session.commit()





            local_file, cleanup_temp_file = resolve_log_file(
                file_reference
            )




            if cleanup_temp_file:

                r2_object = True





            print(
                "[WORKER] Processing:",
                local_file,
                flush=True
            )



            #
            # File diagnostics
            #
            if local_file.exists():

                size_mb = (
                    local_file.stat().st_size
                    /
                    (1024 * 1024)
                )


                print(
                    "[WORKER] File size:",
                    round(size_mb, 2),
                    "MB",
                    flush=True
                )




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





            job = Job.query.get(
                job_id
            )


            if job:


                job.status = "completed"

                job.progress = 100

                job.completed_at = datetime.utcnow()



                db.session.commit()





            #
            # Delete processed upload from R2
            #
            if r2_object:


                try:


                    r2_service.delete_file(
                        file_reference
                    )



                    print(
                        "[WORKER] Deleted processed R2 object:",
                        file_reference,
                        flush=True
                    )



                except Exception as cleanup_error:


                    print(
                        "[WORKER] R2 deletion failed:",
                        cleanup_error,
                        flush=True
                    )






            print(
                f"[WORKER] Completed job {job_id}",
                flush=True
            )



            return result








        except Exception as error:



            print(
                "[WORKER] FAILED",
                flush=True
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
            # Remove worker temp file
            #
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