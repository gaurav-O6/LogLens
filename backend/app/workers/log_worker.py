from datetime import datetime
from pathlib import Path

from app.database.db import db
from app.models.job import Job
from app.services.processing_service import ProcessingService



def process_log_job(
    job_id: int,
    file_path: str,
):
    """
    Background worker task.

    Processes uploaded logs asynchronously.
    """

    from app import create_app


    app = create_app()



    with app.app_context():


        job = Job.query.get(job_id)



        if not job:

            return



        try:


            job.status = "processing"

            job.progress = 10

            job.started_at = datetime.utcnow()


            db.session.commit()



            processor = ProcessingService()



            result = processor.process_file(

                Path(file_path)

            )



            job.status = "completed"

            job.progress = 100

            job.completed_at = datetime.utcnow()


            db.session.commit()



            return result




        except Exception as error:


            job.status = "failed"

            job.progress = 0

            job.error_message = str(error)


            db.session.commit()



            raise error