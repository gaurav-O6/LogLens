import os


class Config:
    """Base configuration for the LogLens application."""

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://loglens:loglens@db:5432/loglens",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis
    REDIS_URL = os.getenv(
        "REDIS_URL",
        "redis://redis:6379/0",
    )

    # File Uploads
    MAX_CONTENT_LENGTH = 1024 * 1024 * 1024  # 1 GB