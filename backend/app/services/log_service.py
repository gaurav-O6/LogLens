from app.database.db import db
from app.models.log_entry import LogEntry


def save_logs(parsed_logs: list[dict]) -> list[dict]:
    """
    Save a batch of log entries.

    Designed for streaming pipeline batches.
    Does not commit.
    Transaction is controlled by the worker.
    """

    new_logs = []

    for log in parsed_logs:

        existing = LogEntry.query.filter_by(

            ip_address=log.get(
                "ip",
                ""
            ),

            timestamp=log.get(
                "timestamp",
                ""
            ),

            method=log.get(
                "method",
                ""
            ),

            path=log.get(
                "path",
                ""
            ),

            status_code=log.get(
                "status_code",
                0
            ),

            user_agent=log.get(
                "user_agent",
                ""
            ),

        ).first()


        if existing:
            continue


        entry = LogEntry(

            ip_address=log.get(
                "ip",
                ""
            ),

            timestamp=log.get(
                "timestamp",
                ""
            ),

            method=log.get(
                "method",
                ""
            ),

            path=log.get(
                "path",
                ""
            ),

            status_code=log.get(
                "status_code",
                0
            ),

            user_agent=log.get(
                "user_agent",
                ""
            ),

        )


        db.session.add(
            entry
        )


        new_logs.append(
            log
        )


    if new_logs:

        db.session.flush()


    return new_logs