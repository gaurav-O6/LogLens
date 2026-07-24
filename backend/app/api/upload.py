from pathlib import Path

from flask import (
    Blueprint,
    jsonify,
    request,
    current_app,
)

from app.database.db import db
from app.models.job import Job
from app.services.upload_service import save_uploaded_log
from app.queue.redis_queue import queue


upload_bp = Blueprint(
    "upload",
    __name__,
    url_prefix="/api/v1/logs",
)


def enqueue_processing(
    job_id,
    file_reference
):
    """
    Add processing task to Redis queue.

    file_reference:

    Uploaded logs:
        filename stored in R2

    Demo logs:
        local file path
    """

    try:

        rq_job = queue.enqueue(
            "app.workers.log_worker.process_log_job",
            job_id,
            file_reference,
            job_timeout=3600,
        )


        return rq_job


    except Exception as error:

        raise RuntimeError(
            f"Redis queue unavailable: {error}"
        )




@upload_bp.route(
    "/upload",
    methods=["POST"]
)
def upload_log():
    """
    Upload log file.

    Flow:

    Client
        |
        v
    Temporary disk
        |
        v
    Cloudflare R2
        |
        v
    Redis worker
    """


    print(
        "[UPLOAD REQUEST RECEIVED]",
        flush=True
    )



    if "file" not in request.files:


        return jsonify(
            {
                "error": "No file provided."
            }
        ), 400




    file = request.files["file"]



    if file.filename == "":


        return jsonify(
            {
                "error": "No file selected."
            }
        ), 400




    try:



        filename = save_uploaded_log(
            file
        )



        job = Job(

            filename=filename,

            status="queued",

            progress=0,

        )



        db.session.add(
            job
        )


        db.session.commit()




        enqueue_processing(

            job.id,

            filename,

        )




        print(
            "[UPLOAD QUEUED]",
            filename,
            job.id,
            flush=True
        )




        return jsonify(

            {

                "message":
                    "Log processing started.",


                "job_id":
                    job.id,


                "status":
                    job.status,


                "filename":
                    filename,

            }

        ), 202




    except Exception as error:



        db.session.rollback()



        print(
            "[UPLOAD FAILED]",
            error,
            flush=True
        )



        return jsonify(

            {

                "error":
                    "Upload failed.",


                "details":
                    str(error),

            }

        ), 500






@upload_bp.route(
    "/demo",
    methods=["GET"]
)
def demo_log():

    """
    Process built-in demo attack log.

    Demo file stays inside repository.
    It is NOT uploaded to R2.
    """


    try:


        demo_file = (

            Path(current_app.root_path)

            .parent

            / "sample_logs"

            / "attack_test.log"

        )



        if not demo_file.exists():


            return jsonify(

                {

                    "error":
                        "Demo log file not found.",


                    "searched_path":
                        str(demo_file),

                }

            ), 404





        job = Job(

            filename="attack_test.log",

            status="queued",

            progress=0,

        )



        db.session.add(
            job
        )


        db.session.commit()




        enqueue_processing(

            job.id,

            str(demo_file),

        )




        return jsonify(

            {

                "message":
                    "Demo processing started.",


                "job_id":
                    job.id,


                "status":
                    job.status,


                "filename":
                    "attack_test.log",

            }

        ), 202




    except Exception as error:


        db.session.rollback()



        return jsonify(

            {

                "error":
                    "Demo processing failed.",


                "details":
                    str(error),

            }

        ), 500