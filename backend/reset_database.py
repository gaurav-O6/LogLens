from app import create_app
from app.database.db import db

from app.models.detection import Detection
from app.models.log_entry import LogEntry
from app.models.job import Job


def reset_database():

    app = create_app()

    with app.app_context():

        print("Starting database reset...")

        detections = Detection.query.delete()
        logs = LogEntry.query.delete()
        jobs = Job.query.delete()

        db.session.commit()

        print("--------------------------------")
        print("Database reset complete")
        print(f"Detections deleted: {detections}")
        print(f"Logs deleted: {logs}")
        print(f"Jobs deleted: {jobs}")
        print("--------------------------------")


if __name__ == "__main__":

    reset_database()