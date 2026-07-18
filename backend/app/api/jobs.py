from flask import Blueprint, jsonify

from app.models.job import Job



jobs_bp = Blueprint(
    "jobs",
    __name__,
    url_prefix="/api/v1/jobs",
)





@jobs_bp.route("/<int:job_id>", methods=["GET"])
def get_job_status(job_id):
    """
    Return processing status of a log processing job.
    """



    job = Job.query.get(job_id)



    if not job:

        return jsonify(
            {
                "error": "Job not found."
            }
        ), 404





    return jsonify(
        {
            "id": job.id,

            "filename": job.filename,

            "status": job.status,

            "progress": job.progress,

            "error": job.error_message,

            "created_at": (
                job.created_at.isoformat()
                if job.created_at
                else None
            ),

            "started_at": (
                job.started_at.isoformat()
                if job.started_at
                else None
            ),

            "completed_at": (
                job.completed_at.isoformat()
                if job.completed_at
                else None
            ),
        }
    ), 200