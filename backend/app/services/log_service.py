from app.database.db import db
from app.models.log_entry import LogEntry


def save_logs(parsed_logs: list[dict]) -> list[dict]:
    """
    Save only new log entries.

    Returns only the newly inserted parsed logs.
    """

    new_logs = []

    for log in parsed_logs:

        existing = LogEntry.query.filter_by(
            ip_address=log.get("ip", ""),
            timestamp=log.get("timestamp", ""),
            method=log.get("method", ""),
            path=log.get("path", ""),
            status_code=log.get("status_code", 0),
            user_agent=log.get("user_agent", ""),
        ).first()

        if existing:
            continue

        entry = LogEntry(
            ip_address=log.get("ip", ""),
            timestamp=log.get("timestamp", ""),
            method=log.get("method", ""),
            path=log.get("path", ""),
            status_code=log.get("status_code", 0),
            user_agent=log.get("user_agent", ""),
        )

        db.session.add(entry)
        new_logs.append(log)

    db.session.commit()

    return new_logs