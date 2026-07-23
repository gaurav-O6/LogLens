from app.database.db import db
from app.models.log_entry import LogEntry


def save_logs(parsed_logs: list[dict]) -> list[dict]:
    """
    Save a batch of parsed log entries.

    Every log event is stored.
    Duplicate requests are valid events in security analysis.

    Transaction is controlled by the worker.
    """

    if not parsed_logs:
        return []


    entries = []


    for log in parsed_logs:

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


        entries.append(
            entry
        )


    if entries:

        db.session.bulk_save_objects(
            entries
        )

        db.session.flush()


    return parsed_logs