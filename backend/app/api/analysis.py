from flask import Blueprint, jsonify

from app.models.detection import Detection


analysis_bp = Blueprint(
    "analysis",
    __name__,
    url_prefix="/api/v1/analysis",
)


@analysis_bp.route("/detections", methods=["GET"])
def get_detections():
    """
    Return all detected security threats.
    """

    detections = Detection.query.order_by(
        Detection.created_at.desc()
    ).all()

    result = []

    for detection in detections:
        result.append(
            {
                "id": detection.id,

                "attack_type": detection.attack_type,
                "severity": detection.severity,

                "source_ip": detection.source_ip,
                "timestamp": detection.timestamp,

                "matched_pattern": detection.matched_pattern,

                "http_method": detection.http_method,
                "request_path": detection.request_path,
                "status_code": detection.status_code,
                "raw_log": detection.raw_log,
            }
        )

    return jsonify(result), 200



@analysis_bp.route("/summary", methods=["GET"])
def get_summary():
    """
    Return dashboard statistics.
    """

    detections = Detection.query.all()

    severity_count = {}
    attack_count = {}
    ip_count = {}

    for detection in detections:

        severity_count[detection.severity] = (
            severity_count.get(detection.severity, 0) + 1
        )

        attack_count[detection.attack_type] = (
            attack_count.get(detection.attack_type, 0) + 1
        )

        ip_count[detection.source_ip] = (
            ip_count.get(detection.source_ip, 0) + 1
        )


    return jsonify(
        {
            "total_attacks": len(detections),
            "attack_types": attack_count,
            "severity": severity_count,
            "source_ips": ip_count,
        }
    ), 200