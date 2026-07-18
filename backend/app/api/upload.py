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


@upload_bp.route("/upload", methods=["POST"])
def upload_log():
    """
    Upload log file and create async processing job.

    Flow:

    Upload File
        ↓
    Save File
        ↓
    Create Job
        ↓
    Queue Worker
        ↓
    Return Job ID
    """

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

        filename = save_uploaded_log(file)


        upload_folder = Path(
            current_app.config["UPLOAD_FOLDER"]
        )


        file_path = upload_folder / filename



        job = Job(

            filename=filename,

            status="queued",

            progress=0,

        )


        db.session.add(job)

        db.session.commit()



        queue.enqueue(
            "app.workers.log_worker.process_log_job",
            job.id,
            str(file_path),
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



    except ValueError as error:

        return jsonify(
            {
                "error": str(error)
            }
        ), 400



    except Exception as error:

        return jsonify(

            {

                "error":
                    "Upload failed.",


                "details":
                    str(error)

            }

        ), 500





@upload_bp.route("/demo", methods=["GET"])
def demo_log():
    """
    Queue demo attack log processing.
    """

    try:


        demo_file = (

            Path(current_app.root_path)
            .parent
            .parent
            / "sample_logs"
            / "attack_test.log"

        )



        if not demo_file.exists():

            return jsonify(
                {
                    "error":
                        "Demo log file not found."
                }
            ), 404




        job = Job(

            filename="attack_test.log",

            status="queued",

            progress=0,

        )


        db.session.add(job)

        db.session.commit()



        queue.enqueue(

            "app.workers.log_worker.process_log_job",

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
                    "attack_test.log"

            }

        ), 202




    except Exception as error:


        return jsonify(

            {

                "error":
                    "Demo processing failed.",


                "details":
                    str(error)

            }

        ), 500