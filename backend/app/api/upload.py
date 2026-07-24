from pathlib import Path

from flask import (
    Blueprint,
    jsonify,
    request,
)

from app.database.db import db
from app.models.job import Job
from app.services.upload_service import save_uploaded_log
from app.services.r2_service import r2_service
from app.queue.redis_queue import queue


upload_bp = Blueprint(
    "upload",
    __name__,
    url_prefix="/api/v1/logs",
)


def enqueue_processing(job_id, filename):
    """
    Add processing job to RQ queue.

    filename:
        R2 object key
    """

    try:

        rq_job = queue.enqueue(
            "app.workers.log_worker.process_log_job",
            job_id,
            filename,
            job_timeout=900,
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
    Upload log file and queue processing.
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
                "message": "Log processing started.",
                "job_id": job.id,
                "status": job.status,
                "filename": filename,
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
                "error": "Upload failed.",
                "details": str(error),
            }
        ), 500





@upload_bp.route(
    "/demo",
    methods=["GET"]
)
def demo_log():
    """
    Upload demo log to R2
    and queue processing.
    """

    try:

        demo_file = (
            Path(__file__)
            .resolve()
            .parents[3]
            / "sample_logs"
            / "attack_test.log"
        )


        if not demo_file.exists():

            return jsonify(
                {
                    "error": "Demo log file not found.",
                    "searched_path": str(demo_file),
                }
            ), 404



        object_name = (
            "demo_attack_test.log"
        )


        print(
            "[DEMO] Uploading demo log to R2",
            flush=True
        )


        r2_service.upload_file(
            demo_file,
            object_name,
        )



        job = Job(
            filename=object_name,
            status="queued",
            progress=0,
        )


        db.session.add(
            job
        )

        db.session.commit()



        enqueue_processing(
            job.id,
            object_name,
        )


        print(
            "[DEMO QUEUED]",
            object_name,
            job.id,
            flush=True
        )



        return jsonify(
            {
                "message": "Demo processing started.",
                "job_id": job.id,
                "status": job.status,
                "filename": object_name,
            }
        ), 202



    except Exception as error:


        db.session.rollback()


        print(
            "[DEMO FAILED]",
            error,
            flush=True
        )


        return jsonify(
            {
                "error": "Demo processing failed.",
                "details": str(error),
            }
        ), 500