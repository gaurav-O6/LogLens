from flask import Flask
from app.api.health import health_bp


def create_app() -> Flask:
    """
    Create and configure the Flask application.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(health_bp)

    return app