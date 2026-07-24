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
    Validate uploaded log.

    Stream to temporary local storage.

    Upload to Cloudflare R2.

    Delete temporary local copy.
    """

    if (
        file.filename is None
        or file.filename == ""
    ):

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
        "[UPLOAD] Saving temporary file:",
        filename,
        flush=True
    )

    total_bytes = 0

    with open(
        temp_file,
        "wb"
    ) as destination:

        while True:

            chunk = file.stream.read(
                1024 * 1024
            )

            if not chunk:
                break

            destination.write(
                chunk
            )

            total_bytes += len(
                chunk
            )

    print(
        "[UPLOAD] Uploading to Cloudflare R2...",
        flush=True
    )

    r2_service.upload_file(
        temp_file,
        filename
    )

    print(
        "[UPLOAD] Removing temporary file...",
        flush=True
    )

    temp_file.unlink(
        missing_ok=True
    )

    print(
        "[UPLOAD] Finished:",
        filename,
        total_bytes,
        "bytes",
        flush=True
    )

    return filename