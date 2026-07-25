
from time import perf_counter

from sqlalchemy import insert

from app.database.db import db
from app.models.detection import Detection

from app.services.geoip_service import GeoIPService


geoip_service = GeoIPService()

# Keep SQL statements reasonably sized while still using
# PostgreSQL multi-row INSERTs instead of one execution per row.
INSERT_BATCH_SIZE = 500


def save_detections(
    detections: list[dict]
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

    # ---------------------------------------------------------
    # BUILD DETECTION ROWS
    # ---------------------------------------------------------

    geoip_start = perf_counter()

    for detection in detections:

        row_start = perf_counter()

        source_ip = (
            detection.get("source_ip")
            or detection.get("ip")
            or ""
        )

        if source_ip in geoip_cache:

            location = geoip_cache[source_ip]

        else:

            lookup_start = perf_counter()

            location = geoip_service.lookup(
                source_ip
            )

            geoip_time += (
                perf_counter() - lookup_start
            )

            geoip_cache[source_ip] = location

        rows.append(
            {
                "job_id":
                    detection.get("job_id"),

                "attack_type":
                    detection.get(
                        "attack_type",
                        ""
                    ),

                "severity":
                    detection.get(
                        "severity",
                        ""
                    ),

                "source_ip":
                    source_ip,

                "is_private_ip":
                    location.get(
                        "is_private_ip",
                        False
                    ),

                "country":
                    location.get("country"),

                "city":
                    location.get("city"),

                "latitude":
                    location.get("latitude"),

                "longitude":
                    location.get("longitude"),

                "timestamp":
                    detection.get("timestamp"),

                "matched_pattern":
                    detection.get("matched_pattern"),

                "http_method":
                    detection.get("http_method"),

                "request_path":
                    detection.get("request_path"),

                "status_code":
                    detection.get("status_code"),

                "raw_log":
                    detection.get("raw_log"),
            }
        )

        row_build_time += (
            perf_counter() - row_start
        )

    total_geoip_phase = (
        perf_counter() - geoip_start
    )

    cache_hits = (
        len(detections)
        - len(geoip_cache)
    )

    # ---------------------------------------------------------
    # MULTI-ROW DATABASE INSERT
    # ---------------------------------------------------------

    start = perf_counter()

    inserted_rows = 0

    for batch_start in range(
        0,
        len(rows),
        INSERT_BATCH_SIZE
    ):

        batch = rows[
            batch_start:
            batch_start + INSERT_BATCH_SIZE
        ]

        db.session.execute(
            insert(Detection).values(batch)
        )

        inserted_rows += len(batch)

    bulk_insert_time = (
        perf_counter() - start
    )

    # ---------------------------------------------------------
    # FLUSH
    # ---------------------------------------------------------

    start = perf_counter()

    db.session.flush()

    flush_time = (
        perf_counter() - start
    )

    # ---------------------------------------------------------
    # PROFILE
    # ---------------------------------------------------------

    total_time = (
        perf_counter() - total_start
    )

    batch_count = (
        (
            len(rows)
            + INSERT_BATCH_SIZE
            - 1
        )
        // INSERT_BATCH_SIZE
    )

    print(
        "\n"
        "------------------------------------------------------------\n"
        "DETECTION SAVE PROFILE\n"
        "------------------------------------------------------------\n"
        f"Detections             : {len(detections):,}\n"
        f"Inserted rows          : {inserted_rows:,}\n"
        f"Insert batch size      : {INSERT_BATCH_SIZE:,}\n"
        f"Insert batches         : {batch_count:,}\n"
        f"Unique IPs             : {len(geoip_cache):,}\n"
        f"GeoIP cache hits       : {cache_hits:,}\n"
        "\n"
        f"GeoIP lookup time      : {geoip_time:.3f}s\n"
        f"GeoIP phase total      : {total_geoip_phase:.3f}s\n"
        f"Row construction       : {row_build_time:.3f}s\n"
        f"SQLAlchemy INSERT      : {bulk_insert_time:.3f}s\n"
        f"Flush                  : {flush_time:.3f}s\n"
        f"Total save time        : {total_time:.3f}s\n"
        "------------------------------------------------------------\n",
        flush=True,
    )

    return inserted_rows
