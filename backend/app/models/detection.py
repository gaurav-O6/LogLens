from datetime import datetime

from app.database.db import db


class Detection(db.Model):
    """
    Database model for detected security threats.
    """

    __tablename__ = "detections"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    attack_type = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    severity = db.Column(
        db.String(20),
        nullable=False,
        index=True
    )

    source_ip = db.Column(
        db.String(45),
        nullable=False,
        index=True
    )

    country = db.Column(
        db.String(100),
        nullable=True,
    )

    city = db.Column(
        db.String(100),
        nullable=True,
    )

    latitude = db.Column(
        db.Float,
        nullable=True,
    )

    longitude = db.Column(
        db.Float,
        nullable=True,
    )

    timestamp = db.Column(
        db.String(50),
        nullable=True
    )

    matched_pattern = db.Column(
        db.Text,
        nullable=True
    )

    http_method = db.Column(
        db.String(10),
        nullable=True
    )

    request_path = db.Column(
        db.Text,
        nullable=True
    )

    status_code = db.Column(
        db.Integer,
        nullable=True
    )

    raw_log = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )