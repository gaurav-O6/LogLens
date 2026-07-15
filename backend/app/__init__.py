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

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)

    # Load application configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(upload_bp)

    return app