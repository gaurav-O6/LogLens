from app import create_app
from app.database.db import db

from app.models.detection import Detection
from app.models.log_entry import LogEntry
from app.models.job import Job


def reset_database():

    app = create_app()

    with app.app_context():

        print("Starting production database reset...")

        detections = Detection.query.count()
        logs = LogEntry.query.count()
        jobs = Job.query.count()


        print(f"Detections before: {detections}")
        print(f"Logs before: {logs}")
        print(f"Jobs before: {jobs}")


        Detection.query.delete()
        LogEntry.query.delete()
        Job.query.delete()


        db.session.commit()


        print("--------------------------------")
        print("Production database reset complete")
        print(f"Deleted detections: {detections}")
        print(f"Deleted logs: {logs}")
        print(f"Deleted jobs: {jobs}")
        print("--------------------------------")


if __name__ == "__main__":

    reset_database()