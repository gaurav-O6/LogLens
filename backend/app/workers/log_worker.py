from datetime import datetime
from pathlib import Path
import traceback

import requests

from app.database.db import db
from app.models.job import Job
from app.services.processing_service import ProcessingService



BACKEND_URL = (
    "https://loglens-backend-3bzc.onrender.com"
)



def download_uploaded_file(filename):
    """
    Download uploaded log from Render backend.
    """

    url = (
        f"{BACKEND_URL}/api/v1/logs/file/{filename}"
    )


    print(
        "[WORKER] Downloading:",
        url,
        flush=True
    )


    response = requests.get(
        url,
        timeout=300
    )


    response.raise_for_status()



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



    with open(
        local_path,
        "wb"
    ) as file:

        file.write(
            response.content
        )



    print(
        "[WORKER] Download complete:",
        local_path,
        flush=True
    )



    return local_path






def process_log_job(job_id: int, file_path: str):
    """
    Background RQ worker task.
    """


    from app import create_app


    app = create_app()



    with app.app_context():


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
                    "[WORKER] Job not found",
                    flush=True
                )

                return





            job.status = "processing"

            job.progress = 10

            job.started_at = datetime.utcnow()



            db.session.commit()





            filename = Path(
                file_path
            ).name




            local_file = download_uploaded_file(
                filename
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


            db.session.remove()