from flask import Blueprint, jsonify

from app.database.db import db

from app.models.detection import Detection
from app.models.log_entry import LogEntry
from app.models.job import Job


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/v1/admin"
)


@admin_bp.route("/reset-database", methods=["POST"])
def reset_database():
    """
    Temporary production database reset endpoint.

    Used once to clear demo/testing data from production.
    Remove this endpoint after cleanup.
    """

    try:

        # Delete dependent records first
        detections_deleted = Detection.query.delete()

        logs_deleted = LogEntry.query.delete()

        jobs_deleted = Job.query.delete()


        db.session.commit()


        return jsonify(
            {
                "message": "Production database reset complete",

                "deleted": {
                    "detections": detections_deleted,
                    "logs": logs_deleted,
                    "jobs": jobs_deleted,
                }
            }
        ), 200



    except Exception as error:


        db.session.rollback()


        return jsonify(
            {
                "message": "Database reset failed",
                "error": str(error)
            }
        ), 500