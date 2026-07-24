import os
from pathlib import Path

import boto3
from botocore.config import Config


class R2Service:
    """
    Cloudflare R2 object storage service.
    """

    def __init__(self):

        self.bucket = os.getenv(
            "R2_BUCKET_NAME"
        )

        self.client = boto3.client(

            "s3",

            endpoint_url=os.getenv(
                "R2_ENDPOINT"
            ),

            aws_access_key_id=os.getenv(
                "R2_ACCESS_KEY_ID"
            ),

            aws_secret_access_key=os.getenv(
                "R2_SECRET_ACCESS_KEY"
            ),

            region_name="auto",

            config=Config(
                signature_version="s3v4"
            ),

        )

    def upload_file(
        self,
        local_path: Path,
        object_name: str,
    ):
        """
        Upload local file to R2.
        """

        print(
            "[R2] Uploading:",
            object_name,
            flush=True,
        )

        self.client.upload_file(
            str(local_path),
            self.bucket,
            object_name,
        )

        print(
            "[R2] Upload complete:",
            object_name,
            flush=True,
        )

    def download_file(
        self,
        object_name: str,
        local_path: Path,
    ):
        """
        Download object from R2.
        """

        local_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        print(
            "[R2] Downloading:",
            object_name,
            flush=True,
        )

        self.client.download_file(
            self.bucket,
            object_name,
            str(local_path),
        )

        print(
            "[R2] Download complete:",
            object_name,
            flush=True,
        )

    def delete_file(
        self,
        object_name: str,
    ):
        """
        Delete object from R2.
        """

        self.client.delete_object(
            Bucket=self.bucket,
            Key=object_name,
        )

        print(
            "[R2] Deleted:",
            object_name,
            flush=True,
        )

    def exists(
        self,
        object_name: str,
    ) -> bool:
        """
        Check if object exists.
        """

        try:

            self.client.head_object(
                Bucket=self.bucket,
                Key=object_name,
            )

            return True

        except Exception:

            return False


r2_service = R2Service()