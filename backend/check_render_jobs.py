import os

from sqlalchemy import create_engine, text


DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL environment variable is not set."
    )


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


with engine.connect() as conn:

    print_section("DATABASE CONNECTION")

    db_name = conn.execute(
        text("SELECT current_database();")
    ).scalar()

    current_user = conn.execute(
        text("SELECT current_user;")
    ).scalar()

    print(f"Database : {db_name}")
    print(f"User     : {current_user}")

    print_section("JOB STATUS COUNTS")

    rows = conn.execute(
        text(
            """
            SELECT
                status,
                COUNT(*) AS total
            FROM jobs
            GROUP BY status
            ORDER BY status;
            """
        )
    ).fetchall()

    if not rows:
        print("No jobs found.")
    else:
        for row in rows:
            print(f"{row.status:<15}{row.total}")

    print_section("ACTIVE JOBS")

    rows = conn.execute(
        text(
            """
            SELECT
                id,
                filename,
                status,
                progress,
                created_at,
                started_at,
                completed_at
            FROM jobs
            WHERE status IN ('queued','processing')
            ORDER BY id;
            """
        )
    ).fetchall()

    if not rows:
        print("No active jobs.")
    else:
        for row in rows:
            print("-" * 70)
            print(f"ID         : {row.id}")
            print(f"Filename   : {row.filename}")
            print(f"Status     : {row.status}")
            print(f"Progress   : {row.progress}")
            print(f"Created    : {row.created_at}")
            print(f"Started    : {row.started_at}")
            print(f"Completed  : {row.completed_at}")

    print_section("LATEST 20 JOBS")

    rows = conn.execute(
        text(
            """
            SELECT
                id,
                filename,
                status,
                progress,
                created_at,
                completed_at
            FROM jobs
            ORDER BY id DESC
            LIMIT 20;
            """
        )
    ).fetchall()

    for row in rows:
        print(
            f"{row.id:>4} | "
            f"{row.status:<11} | "
            f"{row.progress:>3}% | "
            f"{row.filename}"
        )

    print_section("CLEAR STUCK JOBS")

    result = conn.execute(
        text(
            """
            UPDATE jobs
            SET
                status='failed',
                progress=100,
                completed_at=NOW()
            WHERE status IN ('queued','processing');
            """
        )
    )

    conn.commit()

    print(
        f"Updated {result.rowcount} stuck jobs."
    )

    print_section("ACTIVE JOBS AFTER CLEANUP")

    remaining = conn.execute(
        text(
            """
            SELECT COUNT(*)
            FROM jobs
            WHERE status IN ('queued','processing');
            """
        )
    ).scalar()

    print(f"Remaining active jobs: {remaining}")

    print("\nDone.")