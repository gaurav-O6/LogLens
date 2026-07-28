from datetime import datetime
from io import StringIO
from time import perf_counter

from app.database.db import db
from app.services.geoip_service import GeoIPService


geoip_service = GeoIPService()


# ============================================================
# POSTGRESQL BULK INSERT SETTINGS
# ============================================================
#
# PostgreSQL COPY is substantially faster than repeatedly
# executing multi-row INSERT statements for very large batches.
#
# SQLAlchemy ORM defaults are NOT applied when using COPY, so
# created_at is explicitly populated below.
#
# ============================================================


DETECTION_COLUMNS = (
    "job_id",
    "attack_type",
    "severity",
    "source_ip",
    "is_private_ip",
    "country",
    "city",
    "latitude",
    "longitude",
    "timestamp",
    "matched_pattern",
    "http_method",
    "request_path",
    "status_code",
    "raw_log",
    "created_at",
)


def _copy_detections(
    rows: list[dict],
) -> int:
    """
    Insert detection rows using PostgreSQL COPY.

    This avoids generating thousands of individual SQL
    parameter bindings and is designed for large detection
    volumes.
    """

    if not rows:
        return 0

    connection = db.session.connection()

    raw_connection = connection.connection

    psycopg_connection = (
        raw_connection.driver_connection
    )

    buffer = StringIO()

    for row in rows:

        values = []

        for column in DETECTION_COLUMNS:

            value = row.get(column)

            if value is None:

                values.append(
                    "\\N"
                )

                continue

            if isinstance(value, bool):

                values.append(
                    "t"
                    if value
                    else "f"
                )

                continue

            if isinstance(value, datetime):

                value = (
                    value.isoformat(
                        sep=" "
                    )
                )

            value = str(value)

            # -------------------------------------------------
            # PostgreSQL COPY text-format escaping
            # -------------------------------------------------

            value = (
                value
                .replace(
                    "\\",
                    "\\\\",
                )
                .replace(
                    "\t",
                    "\\t",
                )
                .replace(
                    "\n",
                    "\\n",
                )
                .replace(
                    "\r",
                    "\\r",
                )
            )

            values.append(
                value
            )

        buffer.write(
            "\t".join(values)
            + "\n"
        )

    buffer.seek(0)

    copy_sql = f"""
        COPY detections (
            {", ".join(DETECTION_COLUMNS)}
        )
        FROM STDIN
        WITH (
            FORMAT text,
            NULL '\\N'
        )
    """

    with psycopg_connection.cursor() as cursor:

        with cursor.copy(
            copy_sql
        ) as copy:

            while True:

                chunk = buffer.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                copy.write(
                    chunk
                )

    return len(rows)


def save_detections(
    detections: list[dict],
) -> int:

    if not detections:
        return 0

    total_start = perf_counter()

    rows = []

    geoip_time = 0.0
    row_build_time = 0.0
    bulk_insert_time = 0.0
    flush_time = 0.0

    geoip_cache = {}

    # =========================================================
    # BUILD DETECTION ROWS
    # =========================================================

    geoip_start = perf_counter()

    for detection in detections:

        row_start = perf_counter()

        source_ip = (
            detection.get(
                "source_ip"
            )
            or detection.get(
                "ip"
            )
            or ""
        )

        if source_ip in geoip_cache:

            location = geoip_cache[
                source_ip
            ]

        else:

            lookup_start = perf_counter()

            location = (
                geoip_service.lookup(
                    source_ip
                )
            )

            geoip_time += (
                perf_counter()
                - lookup_start
            )

            geoip_cache[
                source_ip
            ] = location

        rows.append(
            {
                "job_id":
                    detection.get(
                        "job_id"
                    ),

                "attack_type":
                    detection.get(
                        "attack_type",
                        "",
                    ),

                "severity":
                    detection.get(
                        "severity",
                        "",
                    ),

                "source_ip":
                    source_ip,

                "is_private_ip":
                    location.get(
                        "is_private_ip",
                        False,
                    ),

                "country":
                    location.get(
                        "country"
                    ),

                "city":
                    location.get(
                        "city"
                    ),

                "latitude":
                    location.get(
                        "latitude"
                    ),

                "longitude":
                    location.get(
                        "longitude"
                    ),

                "timestamp":
                    detection.get(
                        "timestamp"
                    ),

                "matched_pattern":
                    detection.get(
                        "matched_pattern"
                    ),

                "http_method":
                    detection.get(
                        "http_method"
                    ),

                "request_path":
                    detection.get(
                        "request_path"
                    ),

                "status_code":
                    detection.get(
                        "status_code"
                    ),

                "raw_log":
                    detection.get(
                        "raw_log"
                    ),

                # SQLAlchemy's Python-side default is
                # bypassed by COPY, so populate it explicitly.
                "created_at":
                    datetime.utcnow(),
            }
        )

        row_build_time += (
            perf_counter()
            - row_start
        )

    total_geoip_phase = (
        perf_counter()
        - geoip_start
    )

    cache_hits = (
        len(detections)
        - len(geoip_cache)
    )

    # =========================================================
    # POSTGRESQL COPY
    # =========================================================

    start = perf_counter()

    inserted_rows = (
        _copy_detections(
            rows
        )
    )

    bulk_insert_time = (
        perf_counter()
        - start
    )

    # =========================================================
    # FLUSH
    # =========================================================

    start = perf_counter()

    db.session.flush()

    flush_time = (
        perf_counter()
        - start
    )

    # =========================================================
    # PROFILE
    # =========================================================

    total_time = (
        perf_counter()
        - total_start
    )

    print(
        "\n"
        "------------------------------------------------------------\n"
        "DETECTION SAVE PROFILE\n"
        "------------------------------------------------------------\n"
        f"Detections             : "
        f"{len(detections):,}\n"
        f"Inserted rows          : "
        f"{inserted_rows:,}\n"
        f"Unique IPs             : "
        f"{len(geoip_cache):,}\n"
        f"GeoIP cache hits       : "
        f"{cache_hits:,}\n"
        "\n"
        f"GeoIP lookup time      : "
        f"{geoip_time:.3f}s\n"
        f"GeoIP phase total      : "
        f"{total_geoip_phase:.3f}s\n"
        f"Row construction       : "
        f"{row_build_time:.3f}s\n"
        f"PostgreSQL COPY        : "
        f"{bulk_insert_time:.3f}s\n"
        f"Flush                  : "
        f"{flush_time:.3f}s\n"
        f"Total save time        : "
        f"{total_time:.3f}s\n"
        "------------------------------------------------------------\n",
        flush=True,
    )

    return inserted_rows
