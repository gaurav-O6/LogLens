import os


class Config:
    """
    Base configuration for LogLens.
    """

    # ==========================================================
    # Flask
    # ==========================================================

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key",
    )


    DEBUG = (
        os.getenv(
            "FLASK_DEBUG",
            "False",
        ).lower()
        == "true"
    )


    # ==========================================================
    # Database
    # ==========================================================

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://loglens:loglens@postgres:5432/loglens",
    )


    SQLALCHEMY_TRACK_MODIFICATIONS = False



    # ==========================================================
    # Redis
    # ==========================================================

    REDIS_URL = os.getenv(
        "REDIS_URL",
        "redis://redis:6379/0",
    )



    # ==========================================================
    # Local Upload Cache
    #
    # Temporary storage only.
    # Files are uploaded to R2 and removed.
    # ==========================================================

    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        "uploads",
    )


    #
    # Maximum uploaded log size:
    #
    # 700 MB
    #
    # Protects against:
    # - accidental huge uploads
    # - storage abuse
    # - memory/disk pressure
    #
    MAX_CONTENT_LENGTH = (
        700 * 1024 * 1024
    )


    SEND_FILE_MAX_AGE_DEFAULT = 0



    # ==========================================================
    # Cloudflare R2
    # ==========================================================

    R2_ACCOUNT_ID = os.getenv(
        "R2_ACCOUNT_ID"
    )


    R2_BUCKET_NAME = os.getenv(
        "R2_BUCKET_NAME"
    )


    R2_ENDPOINT = os.getenv(
        "R2_ENDPOINT"
    )


    R2_ACCESS_KEY_ID = os.getenv(
        "R2_ACCESS_KEY_ID"
    )


    R2_SECRET_ACCESS_KEY = os.getenv(
        "R2_SECRET_ACCESS_KEY"
    )