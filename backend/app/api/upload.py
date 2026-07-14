from flask import Blueprint, jsonify, request

from app.services.upload_service import save_uploaded_log

upload_bp = Blueprint(
    "upload",
    __name__,
    url_prefix="/api/v1/logs",
)


@upload_bp.route("/upload", methods=["POST"])
def upload_log():
    """Upload a log file."""

    if "file" not in request.files:
        return jsonify({"error": "No file provided."}), 400

    file = request.files["file"]

    try:
        filename = save_uploaded_log(file)

        return (
            jsonify(
                {
                    "message": "File uploaded successfully.",
                    "filename": filename,
                }
            ),
            201,
        )

    except ValueError as error:
        return jsonify({"error": str(error)}), 400