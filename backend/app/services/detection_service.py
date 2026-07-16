from app.database.db import db
from app.models.detection import Detection


def save_detections(detections: list[dict]) -> list[Detection]:
    """
    Save detected security threats to the database.
    """

    detection_entries = []

    for detection in detections:

        entry = Detection(

            attack_type=detection.get("attack_type", ""),

            severity=detection.get("severity", ""),

            source_ip=detection.get("source_ip", ""),

            timestamp=detection.get("timestamp"),

            matched_pattern=detection.get("matched_pattern"),

            http_method=detection.get("http_method"),

            request_path=detection.get("request_path"),

            status_code=detection.get("status_code"),

            raw_log=detection.get("raw_log"),

        )

        detection_entries.append(entry)


    db.session.add_all(detection_entries)

    db.session.commit()


    return detection_entries