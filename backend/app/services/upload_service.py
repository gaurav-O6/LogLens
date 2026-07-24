from pathlib import Path
import uuid

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.services.r2_service import r2_service


ALLOWED_EXTENSIONS = {
    ".log"
}



def save_uploaded_log(file: FileStorage) -> str:
    """
    Save upload temporarily,
    push to R2,
    remove local copy.
    """


    if not file.filename:

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



    temp_file = (
        upload_folder /
        filename
    )



    print(
        "[UPLOAD] Writing temporary file:",
        filename,
        flush=True
    )



    with open(
        temp_file,
        "wb"
    ) as output:


        while True:


            chunk = file.stream.read(
                1024 * 1024
            )


            if not chunk:
                break


            output.write(
                chunk
            )



    try:


        print(
            "[UPLOAD] Sending to R2:",
            filename,
            flush=True
        )


        r2_service.upload_file(
            temp_file,
            filename
        )


    finally:


        temp_file.unlink(
            missing_ok=True
        )


    print(
        "[UPLOAD COMPLETE]",
        filename,
        flush=True
    )


    return filename