from datetime import datetime

from app.database.db import db


class Job(db.Model):
    """
    Database model representing an asynchronous log
    processing job.
    """

    __tablename__ = "jobs"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    filename = db.Column(
        db.String(255),
        nullable=False,
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="queued",
        index=True,
    )

    progress = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    error_message = db.Column(
        db.Text,
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    started_at = db.Column(
        db.DateTime,
        nullable=True,
    )

    completed_at = db.Column(
        db.DateTime,
        nullable=True,
    )