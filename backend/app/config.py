import os


class Config:
    """Base configuration for the LogLens application."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")