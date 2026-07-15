from pathlib import Path
from dotenv import load_dotenv

# Load environment variables BEFORE importing Config
project_root = Path(__file__).resolve().parents[2]
env_path = project_root / ".env"

load_dotenv(env_path)


from flask import Flask

from app import models
from app.api.health import health_bp
from app.api.upload import upload_bp
from app.config import Config
from app.database.db import db
from app.database.migrate import migrate


def create_app() -> Flask:
    """
    Create and configure the Flask application.
    """

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(upload_bp)

    return app