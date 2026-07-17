from app.database.db import db
from app.models.detection import Detection

from app.services.geoip_service import GeoIPService


geoip_service = GeoIPService()


def save_detections(detections: list[dict]) -> list[Detection]:
    """
    Save detected security threats.

    Prevent duplicate detections from being stored.
    Enrich detections with GeoIP information.
    """

    detection_entries = []


    for detection in detections:

        source_ip = (
            detection.get("source_ip")
            or detection.get("ip")
            or ""
        )


        existing = Detection.query.filter_by(

            source_ip=source_ip,

            attack_type=detection.get(
                "attack_type",
                ""
            ),

            request_path=detection.get(
                "request_path"
            ),

            timestamp=detection.get(
                "timestamp"
            ),

            matched_pattern=detection.get(
                "matched_pattern"
            )

        ).first()



        if existing:
            continue



        location = geoip_service.lookup(
            source_ip
        )



        entry = Detection(

            attack_type=detection.get(
                "attack_type",
                ""
            ),

            severity=detection.get(
                "severity",
                ""
            ),

            source_ip=source_ip,

            is_private_ip=location.get(
                "is_private_ip",
                False
            ),

            country=location.get(
                "country"
            ),

            city=location.get(
                "city"
            ),

            latitude=location.get(
                "latitude"
            ),

            longitude=location.get(
                "longitude"
            ),


            timestamp=detection.get(
                "timestamp"
            ),

            matched_pattern=detection.get(
                "matched_pattern"
            ),

            http_method=detection.get(
                "http_method"
            ),

            request_path=detection.get(
                "request_path"
            ),

            status_code=detection.get(
                "status_code"
            ),

            raw_log=detection.get(
                "raw_log"
            ),
        )


        detection_entries.append(
            entry
        )



    if detection_entries:

        db.session.add_all(
            detection_entries
        )

        db.session.commit()



    return detection_entries