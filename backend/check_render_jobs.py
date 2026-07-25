import os
from time import perf_counter

from sqlalchemy import create_engine, text


DATABASE_URL = os.environ["DATABASE_URL"]


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


with engine.connect() as conn:

    print("=" * 60)
    print("POSTGRESQL PERFORMANCE TEST")
    print("=" * 60)

    start = perf_counter()

    conn.execute(text("SELECT 1"))

    elapsed = perf_counter() - start

    print(f"\nSELECT 1 round trip : {elapsed:.3f}s")

    start = perf_counter()

    result = conn.execute(
        text("SELECT COUNT(*) FROM detections")
    )

    count = result.scalar()

    elapsed = perf_counter() - start

    print(f"Detection count     : {count:,}")
    print(f"COUNT(*) time       : {elapsed:.3f}s")

    start = perf_counter()

    result = conn.execute(
        text("""
            SELECT
                id,
                attack_type,
                severity,
                source_ip
            FROM detections
            ORDER BY id DESC
            LIMIT 100;
        """)
    )

    rows = result.fetchall()

    elapsed = perf_counter() - start

    print(f"\nLatest 100 rows     : {len(rows)}")
    print(f"Latest query time   : {elapsed:.3f}s")

    start = perf_counter()

    result = conn.execute(
        text("""
            SELECT COUNT(*)
            FROM detections
            WHERE severity = 'High';
        """)
    )

    high_count = result.scalar()

    elapsed = perf_counter() - start

    print(f"\nHigh detections     : {high_count:,}")
    print(f"Severity query time : {elapsed:.3f}s")

    start = perf_counter()

    result = conn.execute(
        text("""
            SELECT
                id,
                status,
                progress,
                started_at,
                completed_at
            FROM jobs
            ORDER BY id DESC
            LIMIT 1;
        """)
    )

    latest_job = result.fetchone()

    elapsed = perf_counter() - start

    print(f"\nLatest job          : {latest_job}")
    print(f"Job query time      : {elapsed:.3f}s")

    print("\n" + "=" * 60)
    print("INDEX INFORMATION")
    print("=" * 60)

    indexes = conn.execute(
        text("""
            SELECT
                indexname,
                indexdef
            FROM pg_indexes
            WHERE tablename = 'detections'
            ORDER BY indexname;
        """)
    )

    for index in indexes:
        print(
            f"\n{index.indexname}\n"
            f"  {index.indexdef}"
        )

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)