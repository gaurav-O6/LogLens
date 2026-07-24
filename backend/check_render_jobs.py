from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg://loglens:Qksfwv0QEFlNPriomFTAme1CzZC2KaHI@dpg-d9gau9f41pts738de1t0-a.singapore-postgres.render.com/loglens_nd3w"

engine = create_engine(DATABASE_URL)

with engine.begin() as conn:

    print("===== CURRENT JOBS =====")

    rows = conn.execute(text("""
        SELECT
            id,
            status,
            progress,
            created_at,
            started_at,
            completed_at
        FROM jobs
        ORDER BY id DESC
        LIMIT 20;
    """))

    for row in rows:
        print(row)

    result = conn.execute(text("""
        UPDATE jobs
        SET
            status='failed',
            progress=0,
            completed_at=NOW(),
            error_message='Worker abandoned'
        WHERE status='processing';
    """))

    print(f"\nUpdated {result.rowcount} jobs.")

    print("\n===== AFTER UPDATE =====")

    rows = conn.execute(text("""
        SELECT
            id,
            status,
            progress
        FROM jobs
        ORDER BY id DESC
        LIMIT 20;
    """))

    for row in rows:
        print(row)