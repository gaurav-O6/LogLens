from datetime import datetime
from pathlib import Path
import traceback

from app.database.db import db
from app.models.job import Job
from app.services.processing_service import ProcessingService


def process_log_job(job_id: int, file_path: str):
    """
    Background RQ worker task.
    """

    from app import create_app

    app = create_app()

    with app.app_context():

        job = None

        try:

            print(
                f"[WORKER] Starting job {job_id}"
            )

            job = Job.query.get(job_id)

            if not job:
                print(
                    f"[WORKER] Job {job_id} not found"
                )
                return


            job.status = "processing"
            job.progress = 10
            job.started_at = datetime.utcnow()

            db.session.commit()


            print(
                f"[WORKER] Processing file {file_path}"
            )


            processor = ProcessingService()


            result = processor.process_file(
                Path(file_path)
            )


            job = Job.query.get(job_id)

            job.status = "completed"
            job.progress = 100
            job.completed_at = datetime.utcnow()

            db.session.commit()


            print(
                f"[WORKER] Completed job {job_id}"
            )


            return result


        except Exception as error:


            print(
                "[WORKER] FAILED"
            )

            traceback.print_exc()


            db.session.rollback()


            job = Job.query.get(job_id)

            if job:

                job.status = "failed"
                job.progress = 0
                job.error_message = str(error)

                db.session.commit()


            raise error


        finally:

            db.session.remove()