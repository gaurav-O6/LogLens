from app.database.db import db
from app.models.log_entry import LogEntry


def save_logs(parsed_logs: list[dict]) -> list[LogEntry]:
    """
    Save parsed log entries to the database.
    """

    log_entries = []

    for log in parsed_logs:
        entry = LogEntry(
            ip_address=log.get("ip", ""),
            timestamp=log.get("timestamp", ""),
            method=log.get("method", ""),
            path=log.get("path", ""),
            status_code=log.get("status_code", 0),
            user_agent=log.get("user_agent", ""),
        )

        log_entries.append(entry)

    db.session.add_all(log_entries)
    db.session.commit()

    return log_entries