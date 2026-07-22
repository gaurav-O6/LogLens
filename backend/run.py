from app import create_app
from flask_migrate import upgrade


app = create_app()


# Temporary: run Alembic migrations on Render startup
with app.app_context():
    upgrade()


if __name__ == "__main__":
    app.run(
        debug=False,
        use_reloader=False
    )