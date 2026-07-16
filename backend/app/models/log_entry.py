from datetime import datetime

from app.database.db import db


class LogEntry(db.Model):
    """Database model for a parsed log entry."""

    __tablename__ = "log_entries"

    id = db.Column(db.Integer, primary_key=True)

    ip_address = db.Column(
        db.String(45),
        nullable=False,
        index=True,
    )

    timestamp = db.Column(
        db.String(50),
        nullable=False,
    )

    method = db.Column(
        db.String(10),
        nullable=False,
    )

    path = db.Column(
        db.Text,
        nullable=False,
    )

    status_code = db.Column(
        db.Integer,
        nullable=False,
    )

    user_agent = db.Column(
        db.Text,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )