from pathlib import Path

from flask import (
    Blueprint,
    send_file,
    abort,
    current_app
)


files_bp = Blueprint(
    "files",
    __name__,
    url_prefix="/api/v1/files"
)



@files_bp.route("/<filename>", methods=["GET"])
def download_file(filename):

    upload_folder = Path(
        current_app.config["UPLOAD_FOLDER"]
    )

    file_path = upload_folder / filename


    if not file_path.exists():

        abort(404)


    return send_file(
        file_path,
        as_attachment=True
    )