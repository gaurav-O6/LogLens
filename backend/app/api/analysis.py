from flask import Blueprint, jsonify, Response, request
import json

from sqlalchemy import func, text

from app.database.db import db
from app.models.detection import Detection


analysis_bp = Blueprint(
    "analysis",
    __name__,
    url_prefix="/api/v1/analysis",
)



def detection_to_dict(detection):

    return {

        "id": detection.id,

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

        "created_at":
            (
                detection.created_at.isoformat()
                if detection.created_at
                else None
            ),

    }





# ==========================================================
# PAGINATED DETECTIONS
# ==========================================================

@analysis_bp.route("/detections", methods=["GET"])
def get_detections():


    page = max(
        int(request.args.get("page",1)),
        1
    )


    limit = min(
        int(request.args.get("limit",50)),
        200
    )



    pagination = (

        Detection.query

        .order_by(
            Detection.created_at.desc()
        )

        .paginate(
            page=page,
            per_page=limit,
            error_out=False
        )

    )



    return jsonify({

        "items":
            [
                detection_to_dict(d)
                for d in pagination.items
            ],

        "page":
            pagination.page,

        "pages":
            pagination.pages,

        "total":
            pagination.total

    }),200






# ==========================================================
# SUMMARY
# ==========================================================

@analysis_bp.route("/summary", methods=["GET"])
def get_summary():



    attack_types = dict(

        db.session.query(
            Detection.attack_type,
            func.count(Detection.id)
        )

        .group_by(
            Detection.attack_type
        )

        .all()

    )



    severity = dict(

        db.session.query(
            Detection.severity,
            func.count(Detection.id)
        )

        .group_by(
            Detection.severity
        )

        .all()

    )



    countries = dict(

        db.session.query(
            Detection.country,
            func.count(Detection.id)
        )

        .filter(
            Detection.country.isnot(None)
        )

        .group_by(
            Detection.country
        )

        .all()

    )



    source_ips = dict(

        db.session.query(
            Detection.source_ip,
            func.count(Detection.id)
        )

        .group_by(
            Detection.source_ip
        )

        .order_by(
            func.count(Detection.id).desc()
        )

        .limit(10)

        .all()

    )




    # ======================================================
    # THREAT INTELLIGENCE
    # ======================================================


    most_active_ip = (

        db.session.query(

            Detection.source_ip,
            func.count(Detection.id)

        )

        .group_by(
            Detection.source_ip
        )

        .order_by(
            func.count(Detection.id).desc()
        )

        .first()

    )




    most_active_country = (

        db.session.query(

            Detection.country,
            func.count(Detection.id)

        )

        .filter(
            Detection.country.isnot(None)
        )

        .group_by(
            Detection.country
        )

        .order_by(
            func.count(Detection.id).desc()
        )

        .first()

    )




    top_endpoint = (

        db.session.query(

            Detection.request_path,
            func.count(Detection.id)

        )

        .filter(
            Detection.request_path.isnot(None)
        )

        .group_by(
            Detection.request_path
        )

        .order_by(
            func.count(Detection.id).desc()
        )

        .first()

    )







    network_rows = (

        db.session.query(
            Detection.is_private_ip,
            func.count(Detection.id)
        )

        .group_by(
            Detection.is_private_ip
        )

        .all()

    )


    network = dict(network_rows)





    total = (

        db.session.query(
            func.count(Detection.id)
        )

        .scalar()

    )





    latest = (

        Detection.query

        .order_by(
            Detection.created_at.desc()
        )

        .first()

    )





    highest_risk = (

        Detection.query

        .filter(
            Detection.severity=="High"
        )

        .order_by(
            Detection.created_at.desc()
        )

        .first()

    )





    # ======================================================
    # TIMELINE
    # ======================================================


    timeline = {}



    timeline_rows = db.session.execute(

        text(

            """
            SELECT
                SUBSTRING(timestamp FROM 13 FOR 2) AS hour,
                COUNT(id) AS total
            FROM detections
            WHERE timestamp IS NOT NULL
            GROUP BY SUBSTRING(timestamp FROM 13 FOR 2)
            ORDER BY hour
            """

        )

    ).fetchall()



    for row in timeline_rows:

        hour = row.hour.strip()

        timeline[f"{hour}:00"] = row.total





    for hour in range(24):

        timeline.setdefault(
            f"{hour:02}:00",
            0
        )







    return jsonify({


        "total_attacks":
            total,


        "attack_types":
            attack_types,


        "severity":
            severity,


        "countries":
            countries,


        "source_ips":
            source_ips,



        "most_active_ip":
            (
                most_active_ip[0]
                if most_active_ip
                else None
            ),



        "most_active_country":
            (
                most_active_country[0]
                if most_active_country
                else "Unknown"
            ),



        "top_endpoint":
            (
                top_endpoint[0]
                if top_endpoint
                else None
            ),



        "network_type":
            {

                "private":
                    network.get(True,0),

                "public":
                    network.get(False,0)

            },



        "timeline":
            dict(
                sorted(
                    timeline.items()
                )
            ),




        "latest_attack":
            (
                latest.created_at.isoformat()
                if latest
                else None
            ),




        "highest_risk_attack":
            (
                highest_risk.attack_type
                if highest_risk
                else None
            )


    }),200







# ==========================================================
# CSV EXPORT
# ==========================================================

@analysis_bp.route("/export/csv")
def export_csv():


    def generate():


        yield (
            "ID,Attack Type,Severity,Source IP,"
            "Country,City,Latitude,Longitude,Timestamp\n"
        )



        for d in Detection.query.yield_per(1000):


            yield (

                f"{d.id},"
                f"{d.attack_type},"
                f"{d.severity},"
                f"{d.source_ip},"
                f"{d.country},"
                f"{d.city},"
                f"{d.latitude},"
                f"{d.longitude},"
                f"{d.timestamp}\n"

            )



    return Response(

        generate(),

        mimetype="text/csv",

        headers={

            "Content-Disposition":
                "attachment; filename=detections.csv"

        }

    )







# ==========================================================
# JSON EXPORT
# ==========================================================

@analysis_bp.route("/export/json")
def export_json():


    def generate():

        yield "["

        first=True



        for d in Detection.query.yield_per(1000):


            if not first:

                yield ","



            yield json.dumps(
                detection_to_dict(d)
            )


            first=False



        yield "]"




    return Response(

        generate(),

        mimetype="application/json",

        headers={

            "Content-Disposition":
                "attachment; filename=detections.json"

        }

    )