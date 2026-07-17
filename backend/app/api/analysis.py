from flask import Blueprint, jsonify, Response
from io import StringIO
import csv

from app.models.detection import Detection


analysis_bp = Blueprint(
    "analysis",
    __name__,
    url_prefix="/api/v1/analysis",
)



def detection_to_dict(detection):
    """
    Convert Detection model into API response format.
    """

    return {
        "id": detection.id,

        "attack_type": detection.attack_type,
        "severity": detection.severity,

        "source_ip": detection.source_ip,

        "is_private_ip": detection.is_private_ip,

        # GeoIP information
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





@analysis_bp.route("/detections", methods=["GET"])
def get_detections():
    """
    Return all detected security threats.
    """

    detections = Detection.query.order_by(
        Detection.created_at.desc()
    ).all()


    result = [
        detection_to_dict(detection)
        for detection in detections
    ]


    return jsonify(result), 200





@analysis_bp.route("/summary", methods=["GET"])
def get_summary():
    """
    Return dashboard statistics and threat intelligence.
    """


    detections = Detection.query.all()


    severity_count = {}
    attack_count = {}
    ip_count = {}
    country_count = {}
    endpoint_count = {}


    network_type_count = {
        "private": 0,
        "public": 0,
    }




    for detection in detections:


        severity_count[detection.severity] = (
            severity_count.get(
                detection.severity,
                0
            )
            + 1
        )



        attack_count[detection.attack_type] = (
            attack_count.get(
                detection.attack_type,
                0
            )
            + 1
        )



        ip_count[detection.source_ip] = (
            ip_count.get(
                detection.source_ip,
                0
            )
            + 1
        )



        if detection.is_private_ip:

            network_type_count["private"] += 1

        else:

            network_type_count["public"] += 1




        if detection.country:


            country_count[detection.country] = (
                country_count.get(
                    detection.country,
                    0
                )
                + 1
            )




        if detection.request_path:


            endpoint_count[detection.request_path] = (
                endpoint_count.get(
                    detection.request_path,
                    0
                )
                + 1
            )





    most_active_ip = (

        max(
            ip_count,
            key=ip_count.get
        )

        if ip_count

        else None

    )



    most_active_country = (

        max(
            country_count,
            key=country_count.get
        )

        if country_count

        else None

    )



    top_endpoint = (

        max(
            endpoint_count,
            key=endpoint_count.get
        )

        if endpoint_count

        else None

    )




    latest_attack = None



    if detections:


        latest_detection = max(

            detections,

            key=lambda d: d.created_at

        )


        latest_attack = (
            latest_detection.created_at.isoformat()
        )





    severity_rank = {

        "High": 3,

        "Medium": 2,

        "Low": 1,

    }





    highest_risk_attack = None




    if detections:


        highest = max(

            detections,

            key=lambda d:
                severity_rank.get(
                    d.severity,
                    0
                )

        )


        highest_risk_attack = (
            highest.attack_type
        )





    return jsonify(

        {

            "total_attacks": len(detections),


            "attack_types": attack_count,


            "severity": severity_count,


            "source_ips": ip_count,


            "countries": country_count,


            "network_type": network_type_count,



            "most_active_ip": most_active_ip,


            "most_active_country": most_active_country,


            "top_endpoint": top_endpoint,


            "latest_attack": latest_attack,


            "highest_risk_attack": highest_risk_attack,

        }

    ), 200







@analysis_bp.route("/export/json", methods=["GET"])
def export_json():
    """
    Export detections as JSON.
    """


    detections = Detection.query.order_by(
        Detection.created_at.desc()
    ).all()



    result = [

        detection_to_dict(detection)

        for detection in detections

    ]



    return Response(

        jsonify(result).get_data(as_text=True),

        mimetype="application/json",

        headers={

            "Content-Disposition":
                "attachment; filename=detections.json"

        },

    )








@analysis_bp.route("/export/csv", methods=["GET"])
def export_csv():
    """
    Export detections as CSV.
    """



    detections = Detection.query.order_by(
        Detection.created_at.desc()
    ).all()



    output = StringIO()


    writer = csv.writer(output)



    writer.writerow(

        [

            "ID",

            "Attack Type",

            "Severity",

            "Source IP",

            "Private IP",

            "Country",

            "City",

            "Latitude",

            "Longitude",

            "Timestamp",

            "HTTP Method",

            "Request Path",

            "Status Code",

            "Matched Pattern",

            "Raw Log",

        ]

    )





    for detection in detections:



        writer.writerow(

            [

                detection.id,

                detection.attack_type,

                detection.severity,

                detection.source_ip,

                detection.is_private_ip,

                detection.country,

                detection.city,

                detection.latitude,

                detection.longitude,

                detection.timestamp,

                detection.http_method,

                detection.request_path,

                detection.status_code,

                detection.matched_pattern,

                detection.raw_log,

            ]

        )





    return Response(

        output.getvalue(),

        mimetype="text/csv",

        headers={

            "Content-Disposition":
                "attachment; filename=detections.csv"

        },

    )