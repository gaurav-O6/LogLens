from flask import Blueprint, jsonify, Response, request
import csv
import io
import json

from sqlalchemy import func, text

from app.database.db import db
from app.models.detection import Detection


analysis_bp = Blueprint(
    "analysis",
    __name__,
    url_prefix="/api/v1/analysis",
)


# ==========================================================
# HELPERS
# ==========================================================

def detection_to_dict(detection):
    return {
        "id": detection.id,
        "job_id": detection.job_id,
        "attack_type": detection.attack_type,
        "severity": detection.severity,
        "source_ip": detection.source_ip,
        "is_private_ip": detection.is_private_ip,
        "country": detection.country,
        "city": detection.city,
        "latitude": detection.latitude,
        "longitude": detection.longitude,
        "timestamp": detection.timestamp,
        "matched_pattern": detection.matched_pattern,
        "http_method": detection.http_method,
        "request_path": detection.request_path,
        "status_code": detection.status_code,
        "raw_log": detection.raw_log,
        "created_at": (
            detection.created_at.isoformat()
            if detection.created_at
            else None
        ),
    }


def get_job_id():
    raw_job_id = request.args.get("job_id")

    if raw_job_id is None or raw_job_id == "":
        return None, None

    try:
        job_id = int(raw_job_id)
    except (TypeError, ValueError):
        return None, (
            jsonify(
                {
                    "error": "job_id must be an integer."
                }
            ),
            400,
        )

    if job_id <= 0:
        return None, (
            jsonify(
                {
                    "error": "job_id must be greater than 0."
                }
            ),
            400,
        )

    return job_id, None


def apply_job_filter(query, job_id):
    """
    Apply the optional job filter before any LIMIT/OFFSET.

    This ordering is important because SQLAlchemy does not allow
    Query.filter() after limit() or offset() has already been applied.
    """
    if job_id is not None:
        query = query.filter(
            Detection.job_id == job_id
        )

    return query


# ==========================================================
# PAGINATED DETECTIONS
# ==========================================================

@analysis_bp.route("/detections", methods=["GET"])
def get_detections():

    job_id, error = get_job_id()

    if error:
        return error

    try:
        page = max(
            int(request.args.get("page", 1)),
            1
        )
    except (TypeError, ValueError):
        return jsonify(
            {
                "error": "page must be an integer."
            }
        ), 400

    try:
        limit = int(
            request.args.get("limit", 50)
        )
    except (TypeError, ValueError):
        return jsonify(
            {
                "error": "limit must be an integer."
            }
        ), 400

    # Keep pagination bounded.
    limit = min(
        max(limit, 1),
        200
    )

    # ------------------------------------------------------
    # IMPORTANT:
    # Apply job filter BEFORE ordering/pagination.
    # ------------------------------------------------------

    query = Detection.query

    query = apply_job_filter(
        query,
        job_id
    )

    pagination = (
        query
        .order_by(
            Detection.created_at.desc()
        )
        .paginate(
            page=page,
            per_page=limit,
            error_out=False
        )
    )

    return jsonify(
        {
            "items": [
                detection_to_dict(d)
                for d in pagination.items
            ],
            "page": pagination.page,
            "pages": pagination.pages,
            "total": pagination.total,
            "job_id": job_id,
        }
    ), 200


# ==========================================================
# SUMMARY
# ==========================================================

@analysis_bp.route("/summary", methods=["GET"])
def get_summary():

    job_id, error = get_job_id()

    if error:
        return error

    # ======================================================
    # BASE FILTER
    # ======================================================

    base_filter = []

    if job_id is not None:
        base_filter.append(
            Detection.job_id == job_id
        )

    # ======================================================
    # ATTACK TYPES
    # ======================================================

    attack_types_query = (
        db.session.query(
            Detection.attack_type,
            func.count(Detection.id)
        )
    )

    if base_filter:
        attack_types_query = (
            attack_types_query
            .filter(*base_filter)
        )

    attack_types_query = (
        attack_types_query
        .group_by(
            Detection.attack_type
        )
    )

    attack_types = dict(
        attack_types_query.all()
    )

    # ======================================================
    # SEVERITY
    # ======================================================

    severity_query = (
        db.session.query(
            Detection.severity,
            func.count(Detection.id)
        )
    )

    if base_filter:
        severity_query = (
            severity_query
            .filter(*base_filter)
        )

    severity_query = (
        severity_query
        .group_by(
            Detection.severity
        )
    )

    severity = dict(
        severity_query.all()
    )

    # ======================================================
    # COUNTRIES
    # ======================================================

    countries_query = (
        db.session.query(
            Detection.country,
            func.count(Detection.id)
        )
        .filter(
            Detection.country.isnot(None)
        )
    )

    if base_filter:
        countries_query = (
            countries_query
            .filter(*base_filter)
        )

    countries_query = (
        countries_query
        .group_by(
            Detection.country
        )
    )

    countries = dict(
        countries_query.all()
    )

    # ======================================================
    # SOURCE IPS
    # ======================================================

    # IMPORTANT:
    # Filter FIRST, then group/order, then limit.
    #
    # The previous implementation applied .limit(10) before
    # the job filter. SQLAlchemy therefore raised:
    #
    # InvalidRequestError:
    # Query.filter() being called on a Query which already
    # has LIMIT or OFFSET applied.
    # ======================================================

    source_ips_query = (
        db.session.query(
            Detection.source_ip,
            func.count(Detection.id)
        )
    )

    if base_filter:
        source_ips_query = (
            source_ips_query
            .filter(*base_filter)
        )

    source_ips_query = (
        source_ips_query
        .group_by(
            Detection.source_ip
        )
        .order_by(
            func.count(Detection.id).desc()
        )
        .limit(10)
    )

    source_ips = dict(
        source_ips_query.all()
    )

    # ======================================================
    # THREAT INTELLIGENCE
    # ======================================================

    most_active_ip_query = (
        db.session.query(
            Detection.source_ip,
            func.count(Detection.id)
        )
    )

    if base_filter:
        most_active_ip_query = (
            most_active_ip_query
            .filter(*base_filter)
        )

    most_active_ip_query = (
        most_active_ip_query
        .group_by(
            Detection.source_ip
        )
        .order_by(
            func.count(Detection.id).desc()
        )
    )

    most_active_ip = (
        most_active_ip_query.first()
    )

    # ======================================================
    # MOST ACTIVE COUNTRY
    # ======================================================

    most_active_country_query = (
        db.session.query(
            Detection.country,
            func.count(Detection.id)
        )
        .filter(
            Detection.country.isnot(None)
        )
    )

    if base_filter:
        most_active_country_query = (
            most_active_country_query
            .filter(*base_filter)
        )

    most_active_country_query = (
        most_active_country_query
        .group_by(
            Detection.country
        )
        .order_by(
            func.count(Detection.id).desc()
        )
    )

    most_active_country = (
        most_active_country_query.first()
    )

    # ======================================================
    # TOP ENDPOINT
    # ======================================================

    top_endpoint_query = (
        db.session.query(
            Detection.request_path,
            func.count(Detection.id)
        )
        .filter(
            Detection.request_path.isnot(None)
        )
    )

    if base_filter:
        top_endpoint_query = (
            top_endpoint_query
            .filter(*base_filter)
        )

    top_endpoint_query = (
        top_endpoint_query
        .group_by(
            Detection.request_path
        )
        .order_by(
            func.count(Detection.id).desc()
        )
    )

    top_endpoint = (
        top_endpoint_query.first()
    )

    # ======================================================
    # NETWORK TYPE
    # ======================================================

    network_query = (
        db.session.query(
            Detection.is_private_ip,
            func.count(Detection.id)
        )
    )

    if base_filter:
        network_query = (
            network_query
            .filter(*base_filter)
        )

    network_query = (
        network_query
        .group_by(
            Detection.is_private_ip
        )
    )

    network_rows = network_query.all()

    network = dict(network_rows)

    # ======================================================
    # TOTAL
    # ======================================================

    total_query = (
        db.session.query(
            func.count(Detection.id)
        )
    )

    if base_filter:
        total_query = (
            total_query
            .filter(*base_filter)
        )

    total = total_query.scalar()

    # ======================================================
    # LATEST
    # ======================================================

    latest_query = Detection.query

    if job_id is not None:
        latest_query = (
            latest_query
            .filter(
                Detection.job_id == job_id
            )
        )

    latest_query = (
        latest_query
        .order_by(
            Detection.created_at.desc()
        )
    )

    latest = latest_query.first()

    # ======================================================
    # HIGHEST RISK
    # ======================================================

    highest_risk_query = (
        Detection.query
        .filter(
            Detection.severity == "High"
        )
    )

    if job_id is not None:
        highest_risk_query = (
            highest_risk_query
            .filter(
                Detection.job_id == job_id
            )
        )

    highest_risk_query = (
        highest_risk_query
        .order_by(
            Detection.created_at.desc()
        )
    )

    highest_risk = (
        highest_risk_query.first()
    )

    # ======================================================
    # TIMELINE
    # ======================================================

    timeline = {}

    timeline_sql = """
        SELECT
            SUBSTRING(timestamp FROM 13 FOR 2) AS hour,
            COUNT(id) AS total

        FROM detections

        WHERE timestamp IS NOT NULL
    """

    params = {}

    if job_id is not None:
        timeline_sql += """
            AND job_id = :job_id
        """

        params["job_id"] = job_id

    timeline_sql += """
        GROUP BY
            SUBSTRING(timestamp FROM 13 FOR 2)

        ORDER BY
            hour
    """

    timeline_rows = db.session.execute(
        text(timeline_sql),
        params
    ).fetchall()

    for row in timeline_rows:

        hour = str(row.hour).strip()

        try:
            hour_number = int(hour)
        except (TypeError, ValueError):
            continue

        if 0 <= hour_number <= 23:
            timeline[
                f"{hour_number:02}:00"
            ] = row.total

    # Always return all 24 hours.
    for hour in range(24):
        timeline.setdefault(
            f"{hour:02}:00",
            0
        )

    # ======================================================
    # RESPONSE
    # ======================================================

    return jsonify(
        {
            "job_id": job_id,

            "total_attacks": total or 0,

            "attack_types": attack_types,

            "severity": severity,

            "countries": countries,

            "source_ips": source_ips,

            "most_active_ip": (
                most_active_ip[0]
                if most_active_ip
                else None
            ),

            "most_active_country": (
                most_active_country[0]
                if most_active_country
                else "Unknown"
            ),

            "top_endpoint": (
                top_endpoint[0]
                if top_endpoint
                else None
            ),

            "network_type": {
                "private": network.get(True, 0),
                "public": network.get(False, 0),
            },

            "timeline": dict(
                sorted(
                    timeline.items()
                )
            ),

            "latest_attack": (
                latest.created_at.isoformat()
                if latest
                else None
            ),

            "highest_risk_attack": (
                highest_risk.attack_type
                if highest_risk
                else None
            ),
        }
    ), 200


# ==========================================================
# CSV EXPORT
# ==========================================================

@analysis_bp.route("/export/csv", methods=["GET"])
def export_csv():

    job_id, error = get_job_id()

    if error:
        return error

    query = Detection.query

    # Filter before yield_per / iteration.
    query = apply_job_filter(
        query,
        job_id
    )

    query = query.order_by(
        Detection.created_at.desc()
    )

    def generate():

        output = io.StringIO()

        writer = csv.writer(output)

        writer.writerow(
            [
                "ID",
                "Job ID",
                "Attack Type",
                "Severity",
                "Source IP",
                "Country",
                "City",
                "Latitude",
                "Longitude",
                "Timestamp",
            ]
        )

        yield output.getvalue()

        output.seek(0)
        output.truncate(0)

        for d in query.yield_per(1000):

            writer.writerow(
                [
                    d.id,
                    d.job_id,
                    d.attack_type,
                    d.severity,
                    d.source_ip,
                    d.country,
                    d.city,
                    d.latitude,
                    d.longitude,
                    d.timestamp,
                ]
            )

            yield output.getvalue()

            output.seek(0)
            output.truncate(0)

    filename = (
        f"detections_job_{job_id}.csv"
        if job_id is not None
        else "detections.csv"
    )

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
                f"attachment; filename={filename}"
        }
    )


# ==========================================================
# JSON EXPORT
# ==========================================================

@analysis_bp.route("/export/json", methods=["GET"])
def export_json():

    job_id, error = get_job_id()

    if error:
        return error

    query = Detection.query

    # Filter before iteration.
    query = apply_job_filter(
        query,
        job_id
    )

    query = query.order_by(
        Detection.created_at.desc()
    )

    def generate():

        yield "["

        first = True

        for d in query.yield_per(1000):

            if not first:
                yield ","

            yield json.dumps(
                detection_to_dict(d)
            )

            first = False

        yield "]"

    filename = (
        f"detections_job_{job_id}.json"
        if job_id is not None
        else "detections.json"
    )

    return Response(
        generate(),
        mimetype="application/json",
        headers={
            "Content-Disposition":
                f"attachment; filename={filename}"
        }
    )