from time import perf_counter

from sqlalchemy import insert, text

from app.database.db import db
from app.models.detection import Detection

from app.services.geoip_service import GeoIPService


geoip_service = GeoIPService()

_DIAGNOSTICS_PRINTED = False


def _print_detection_db_diagnostics():

    global _DIAGNOSTICS_PRINTED

    if _DIAGNOSTICS_PRINTED:
        return

    _DIAGNOSTICS_PRINTED = True

    print(
        "\n"
        "============================================================\n"
        "DETECTION DATABASE DIAGNOSTICS\n"
        "============================================================",
        flush=True,
    )

    try:

        row = db.session.execute(
            text(
                """
                SELECT
                    current_database(),
                    current_user,
                    version()
                """
            )
        ).fetchone()

        print(f"[DB] Database : {row[0]}", flush=True)
        print(f"[DB] User     : {row[1]}", flush=True)
        print(f"[DB] Version  : {row[2]}", flush=True)

        indexes = db.session.execute(
            text(
                """
                SELECT
                    indexname,
                    indexdef
                FROM pg_indexes
                WHERE schemaname = 'public'
                  AND tablename = 'detections'
                ORDER BY indexname
                """
            )
        ).fetchall()

        print("\n[DB] DETECTION INDEXES", flush=True)

        if indexes:
            for index in indexes:
                print(f"    {index[0]}", flush=True)
                print(f"        {index[1]}", flush=True)
        else:
            print("    NONE", flush=True)

        constraints = db.session.execute(
            text(
                """
                SELECT
                    conname,
                    contype,
                    pg_get_constraintdef(oid)
                FROM pg_constraint
                WHERE conrelid = 'public.detections'::regclass
                ORDER BY conname
                """
            )
        ).fetchall()

        print("\n[DB] DETECTION CONSTRAINTS", flush=True)

        if constraints:
            for constraint in constraints:
                print(
                    f"    {constraint[0]} | type={constraint[1]}",
                    flush=True,
                )
                print(
                    f"        {constraint[2]}",
                    flush=True,
                )
        else:
            print("    NONE", flush=True)

        triggers = db.session.execute(
            text(
                """
                SELECT
                    tgname,
                    pg_get_triggerdef(oid)
                FROM pg_trigger
                WHERE tgrelid = 'public.detections'::regclass
                  AND NOT tgisinternal
                ORDER BY tgname
                """
            )
        ).fetchall()

        print("\n[DB] DETECTION TRIGGERS", flush=True)

        if triggers:
            for trigger in triggers:
                print(f"    {trigger[0]}", flush=True)
                print(f"        {trigger[1]}", flush=True)
        else:
            print("    NONE", flush=True)

        size = db.session.execute(
            text(
                """
                SELECT
                    pg_size_pretty(
                        pg_total_relation_size(
                            'public.detections'::regclass
                        )
                    ),
                    pg_total_relation_size(
                        'public.detections'::regclass
                    )
                """
            )
        ).fetchone()

        print("\n[DB] DETECTION TABLE SIZE", flush=True)
        print(f"    Size  : {size[0]}", flush=True)
        print(f"    Bytes : {size[1]:,}", flush=True)

        count = db.session.execute(
            text(
                """
                SELECT COUNT(*)
                FROM public.detections
                """
            )
        ).scalar()

        print(
            f"\n[DB] Existing rows : {count:,}",
            flush=True,
        )

        print(
            "============================================================\n",
            flush=True,
        )

    except Exception as error:

        print(
            "[DB DIAGNOSTICS ERROR]",
            repr(error),
            flush=True,
        )

        db.session.rollback()


def save_detections(
    detections: list[dict]
) -> int:

    if not detections:
        return 0

    total_start = perf_counter()

    _print_detection_db_diagnostics()

    rows = []

    geoip_time = 0.0
    row_build_time = 0.0
    bulk_insert_time = 0.0
    flush_time = 0.0

    geoip_cache = {}

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

    start = perf_counter()

    db.session.execute(
        insert(Detection),
        rows
    )

    bulk_insert_time = (
        perf_counter() - start
    )

    start = perf_counter()

    db.session.flush()

    flush_time = (
        perf_counter() - start
    )

    total_time = (
        perf_counter() - total_start
    )

    print(
        "\n"
        "------------------------------------------------------------\n"
        "DETECTION SAVE PROFILE\n"
        "------------------------------------------------------------\n"
        f"Detections             : {len(detections):,}\n"
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

    return len(rows)
