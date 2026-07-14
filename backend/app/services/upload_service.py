from pathlib import Path

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask import current_app

upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
upload_folder.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".log"}


def save_uploaded_log(file: FileStorage) -> str:
    """
    Validate and save an uploaded log file.

    Args:
        file: Uploaded log file.

    Returns:
        The saved filename.

    Raises:
        ValueError: If the uploaded file is invalid.
    """

    if file.filename is None or file.filename == "":
        raise ValueError("No file selected.")

    filename = secure_filename(file.filename)

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Only .log files are allowed.")

    save_path = upload_folder / filename

    file.save(save_path)

    return filename