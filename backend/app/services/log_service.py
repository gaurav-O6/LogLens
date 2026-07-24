from app.database.db import db
from app.models.log_entry import LogEntry


def save_logs(
    parsed_logs: list[dict]
) -> int:
    """
    Bulk insert parsed logs.

    Designed for large files.
    """

    if not parsed_logs:
        return 0


    rows = []


    for log in parsed_logs:

        rows.append(
            {
                "ip_address": log.get(
                    "ip",
                    ""
                ),

                "timestamp": log.get(
                    "timestamp",
                    ""
                ),

                "method": log.get(
                    "method",
                    ""
                ),

                "path": log.get(
                    "path",
                    ""
                ),

                "status_code": log.get(
                    "status_code",
                    0
                ),

                "user_agent": log.get(
                    "user_agent",
                    ""
                ),
            }
        )


    db.session.bulk_insert_mappings(
        LogEntry,
        rows
    )


    db.session.flush()


    return len(rows)