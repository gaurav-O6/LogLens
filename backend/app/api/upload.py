from pathlib import Path

from flask import (
    Blueprint,
    jsonify,
    request,
    current_app
)

from app.services.upload_service import save_uploaded_log
from app.services.processing_service import ProcessingService


upload_bp = Blueprint(
    "upload",
    __name__,
    url_prefix="/api/v1/logs",
)



@upload_bp.route("/upload", methods=["POST"])
def upload_log():
    """
    Upload and analyze a log file.

    Flow:

    File Upload
        ↓
    Save File
        ↓
    Parse Logs
        ↓
    Save Logs
        ↓
    Detect Threats
        ↓
    Save Detections
        ↓
    Return Summary
    """


    if "file" not in request.files:

        return jsonify(
            {
                "error": "No file provided."
            }
        ), 400



    file = request.files["file"]


    if file.filename == "":

        return jsonify(
            {
                "error": "No file selected."
            }
        ),400



    try:

        # Save uploaded file

        filename = save_uploaded_log(file)



        upload_folder = Path(
            current_app.config["UPLOAD_FOLDER"]
        )


        file_path = upload_folder / filename



        # Process file

        processor = ProcessingService()

        result = processor.process_file(
            file_path
        )



        return jsonify(
            {

                "message":
                    "Log processed successfully.",


                "filename":
                    filename,


                "parsed_logs":
                    len(result["parsed_logs"]),


                "detections":
                    len(result["detections"]),


                "summary":
                    result["summary"]

            }

        ),200



    except ValueError as error:


        return jsonify(
            {
                "error": str(error)
            }
        ),400




    except Exception as error:


        return jsonify(
            {
                "error":
                    "Processing failed.",

                "details":
                    str(error)
            }
        ),500