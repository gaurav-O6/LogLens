import uuid
from pathlib import Path

from flask import (
    Blueprint,
    jsonify,
    request,
    current_app,
)

from app.database.db import db
from app.models.job import Job
from app.queue.redis_queue import queue
from app.services.r2_service import r2_service


upload_bp = Blueprint(
    "upload",
    __name__,
    url_prefix="/api/v1/logs",
)


MAX_ACTIVE_JOBS = 3


ALLOWED_EXTENSIONS = {
    ".log",
}


def enqueue_processing(
    job_id,
    file_reference,
):
    """
    Add processing task to Redis queue.
    """

    try:

        print(
            f"[QUEUE] Enqueuing job_id={job_id} "
            f"file={file_reference} "
            f"queue={queue.name}",
            flush=True,
        )

        rq_job = queue.enqueue(
            "app.workers.log_worker.process_log_job",
            job_id,
            file_reference,
            job_timeout=3600,
        )

        print(
            f"[QUEUE] RQ job created "
            f"id={rq_job.id} "
            f"status={rq_job.get_status()}",
            flush=True,
        )

        return rq_job

    except Exception as error:

        print(
            f"[QUEUE ERROR] {error}",
            flush=True,
        )

        raise RuntimeError(
            f"Redis queue unavailable: {error}"
        )


def check_active_jobs():

    count = Job.query.filter(
        Job.status.in_(
            [
                "queued",
                "processing",
            ]
        )
    ).count()

    return count


def validate_log_filename(
    filename,
):
    """
    Validate that the uploaded object has a .log extension.
    """

    if not filename:

        return False

    suffix = Path(
        filename
    ).suffix.lower()

    return suffix in ALLOWED_EXTENSIONS


@upload_bp.route(
    "/upload-url",
    methods=["POST"],
)
def generate_upload_url():
    """
    Generate a presigned R2 URL for direct browser upload.

    The browser uploads the actual log file directly to R2.
    Render only handles this small JSON request.
    """

    print(
        "[UPLOAD URL REQUEST RECEIVED]",
        flush=True,
    )

    data = request.get_json(
        silent=True
    ) or {}

    original_filename = str(
        data.get(
            "filename",
            "",
        )
    ).strip()

    content_type = str(
        data.get(
            "content_type",
            "application/octet-stream",
        )
    ).strip()

    if not original_filename:

        return jsonify(
            {
                "error":
                "Filename is required.",
            }
        ), 400

    if not validate_log_filename(
        original_filename
    ):

        return jsonify(
            {
                "error":
                "Only .log files are supported.",
            }
        ), 400

    try:

        extension = Path(
            original_filename
        ).suffix.lower()

        object_name = (
            f"uploads/"
            f"{uuid.uuid4().hex}"
            f"{extension}"
        )

        upload_url = (
            r2_service.generate_presigned_upload_url(
                object_name=object_name,
                content_type=content_type,
                expires_in=900,
            )
        )

        print(
            "[UPLOAD URL CREATED]",
            object_name,
            flush=True,
        )

        return jsonify(
            {
                "upload_url":
                upload_url,

                "object_name":
                object_name,

                "filename":
                original_filename,
            }
        ), 200

    except Exception as error:

        print(
            "[UPLOAD URL FAILED]",
            error,
            flush=True,
        )

        return jsonify(
            {
                "error":
                "Unable to create upload URL.",

                "details":
                str(error),
            }
        ), 500


@upload_bp.route(
    "/process",
    methods=["POST"],
)
def process_uploaded_log():
    """
    Create a processing job for a file that has already
    been uploaded directly to R2.
    """

    print(
        "[PROCESS REQUEST RECEIVED]",
        flush=True,
    )

    if check_active_jobs() >= MAX_ACTIVE_JOBS:

        return jsonify(
            {
                "error":
                "Too many active processing jobs. "
                "Please try again later.",
            }
        ), 429

    data = request.get_json(
        silent=True
    ) or {}

    object_name = str(
        data.get(
            "object_name",
            "",
        )
    ).strip()

    filename = str(
        data.get(
            "filename",
            "",
        )
    ).strip()

    if not object_name:

        return jsonify(
            {
                "error":
                "R2 object name is required.",
            }
        ), 400

    if not filename:

        filename = Path(
            object_name
        ).name

    if not validate_log_filename(
        filename
    ):

        return jsonify(
            {
                "error":
                "Only .log files are supported.",
            }
        ), 400

    try:

        print(
            "[PROCESS] Checking R2 object:",
            object_name,
            flush=True,
        )

        if not r2_service.exists(
            object_name
        ):

            return jsonify(
                {
                    "error":
                    "Uploaded file was not found in storage.",
                }
            ), 404

        job = Job(
            filename=filename,
            status="queued",
            progress=0,
        )

        db.session.add(
            job
        )

        db.session.commit()

        rq_job = enqueue_processing(
            job.id,
            object_name,
        )

        print(
            f"[PROCESS QUEUED] "
            f"filename={filename} "
            f"db_job_id={job.id} "
            f"rq_job_id={rq_job.id}",
            flush=True,
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

                "rq_job_id":
                rq_job.id,
            }
        ), 202

    except Exception as error:

        db.session.rollback()

        print(
            "[PROCESS FAILED]",
            error,
            flush=True,
        )

        return jsonify(
            {
                "error":
                "Unable to start log processing.",

                "details":
                str(error),
            }
        ), 500


@upload_bp.route(
    "/demo",
    methods=["GET"],
)
def demo_log():
    """
    Process built-in demo attack log.
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

        rq_job = enqueue_processing(
            job.id,
            str(demo_file),
        )

        print(
            f"[DEMO QUEUED] "
            f"db_job_id={job.id} "
            f"rq_job_id={rq_job.id}",
            flush=True,
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

                "rq_job_id":
                rq_job.id,
            }
        ), 202

    except Exception as error:

        db.session.rollback()

        print(
            "[DEMO FAILED]",
            error,
            flush=True,
        )

        return jsonify(
            {
                "error":
                "Demo processing failed.",

                "details":
                str(error),
            }
        ), 500


@upload_bp.errorhandler(413)
def file_too_large(error):

    return jsonify(
        {
            "error":
            "File too large.",

            "limit":
            "700MB",
        }
    ), 413