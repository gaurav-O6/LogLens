from pathlib import Path
import uuid

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {".log"}



def save_uploaded_log(file: FileStorage) -> str:
    """
    Validate and save uploaded log file safely.

    Uses chunked writing for large log files.
    """

    if file.filename is None or file.filename == "":
        raise ValueError(
            "No file selected."
        )


    original_filename = secure_filename(
        file.filename
    )


    extension = Path(
        original_filename
    ).suffix.lower()


    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Only .log files are allowed."
        )


    filename = (
        f"{Path(original_filename).stem}_"
        f"{uuid.uuid4().hex[:8]}"
        f"{extension}"
    )


    upload_folder = Path(
        current_app.config["UPLOAD_FOLDER"]
    )


    upload_folder.mkdir(
        parents=True,
        exist_ok=True
    )


    save_path = upload_folder / filename



    print(
        "[UPLOAD] Saving file:",
        filename
    )



    total_bytes = 0



    with open(save_path, "wb") as destination:


        while True:


            chunk = file.stream.read(
                1024 * 1024
            )


            if not chunk:
                break



            destination.write(
                chunk
            )


            total_bytes += len(chunk)



    print(
        "[UPLOAD] Saved:",
        filename,
        total_bytes,
        "bytes"
    )



    return filename