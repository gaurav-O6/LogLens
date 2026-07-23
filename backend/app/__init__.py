from pathlib import Path

from dotenv import load_dotenv


# ==========================================================
# LOAD ENVIRONMENT VARIABLES FIRST
# ==========================================================

project_root = Path(__file__).resolve().parents[2]

env_path = project_root / ".env"

load_dotenv(env_path)



# ==========================================================
# FLASK IMPORTS
# ==========================================================

from flask import Flask

from flask_cors import CORS



# ==========================================================
# APPLICATION IMPORTS
# ==========================================================

from app import models


from app.api.health import health_bp
from app.api.upload import upload_bp
from app.api.analysis import analysis_bp
from app.api.jobs import jobs_bp
from app.api.admin import admin_bp


from app.config import Config


from app.database.db import db
from app.database.migrate import migrate





def create_app() -> Flask:
    """
    Create and configure Flask application.
    """


    app = Flask(__name__)




    # ======================================================
    # CORS CONFIGURATION
    # ======================================================

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "*"
            }
        },
        methods=[
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "OPTIONS"
        ],
        allow_headers=[
            "Content-Type",
            "Authorization"
        ],
    )




    # ======================================================
    # LOAD CONFIGURATION
    # ======================================================

    app.config.from_object(
        Config
    )




    # ======================================================
    # INITIALIZE EXTENSIONS
    # ======================================================

    db.init_app(
        app
    )


    migrate.init_app(
        app,
        db
    )




    # ======================================================
    # REGISTER BLUEPRINTS
    # ======================================================

    app.register_blueprint(
        health_bp
    )


    app.register_blueprint(
        upload_bp
    )


    app.register_blueprint(
        analysis_bp
    )


    app.register_blueprint(
        jobs_bp
    )


    app.register_blueprint(
        admin_bp
    )




    return app