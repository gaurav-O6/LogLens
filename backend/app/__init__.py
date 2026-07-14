from flask import Flask

from app.api.health import health_bp
from app.api.upload import upload_bp
from app.config import Config


def create_app() -> Flask:
    """
    Create and configure the Flask application.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)

    # Load application configuration
    app.config.from_object(Config)

    # Register Blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(upload_bp)

    return app