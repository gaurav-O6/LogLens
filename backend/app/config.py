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
        "dev-secret-key"
    )


    DEBUG = os.getenv(
        "FLASK_DEBUG",
        "False"
    ).lower() == "true"



    # ==========================================================
    # Database
    # ==========================================================

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://loglens:loglens@postgres:5432/loglens"
    )


    SQLALCHEMY_TRACK_MODIFICATIONS = False



    # ==========================================================
    # Redis
    # ==========================================================

    REDIS_URL = os.getenv(
        "REDIS_URL",
        "redis://redis:6379/0"
    )



    # ==========================================================
    # Uploads
    # ==========================================================

    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        "uploads"
    )


    # Allow large security log files
    MAX_CONTENT_LENGTH = (
        2 * 1024 * 1024 * 1024
    )


    # Disable unnecessary caching
    SEND_FILE_MAX_AGE_DEFAULT = 0