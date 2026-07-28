from app.database.db import db
from app.models.log_entry import LogEntry


def save_logs(
    parsed_logs: list[dict],
    job_id: int,
) -> int:
    """
    Bulk insert parsed logs for a specific processing job.

    Every stored log entry is permanently associated with the
    job that produced it.

    Designed for large files and batch processing.
    """

    if not parsed_logs:
        return 0

    if job_id is None:
        raise ValueError(
            "job_id is required when saving log entries."
        )

    rows = []

    for log in parsed_logs:

        rows.append(
            {
                "job_id": job_id,

                "ip_address": log.get(
                    "ip",
                    "",
                ),

                "timestamp": log.get(
                    "timestamp",
                    "",
                ),

                "method": log.get(
                    "method",
                    "",
                ),

                "path": log.get(
                    "path",
                    "",
                ),

                "status_code": log.get(
                    "status_code",
                    0,
                ),

                "user_agent": log.get(
                    "user_agent",
                    "",
                ),
            }
        )

    db.session.bulk_insert_mappings(
        LogEntry,
        rows,
    )

    db.session.flush()

    return len(rows)