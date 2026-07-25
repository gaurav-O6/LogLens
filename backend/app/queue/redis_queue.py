import os

import redis
from rq import Queue


# ============================================================
# REDIS CONFIGURATION
# ============================================================

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://redis:6379/0",
)

QUEUE_NAME = "log_processing"


redis_connection = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=False,
)


print(
    f"[REDIS] {REDIS_URL}",
    flush=True,
)


# ============================================================
# REDIS CONNECTION CHECK
# ============================================================

try:

    redis_connection.ping()

    print(
        "[REDIS PING] True",
        flush=True,
    )

except Exception as error:

    print(
        f"[REDIS ERROR] {error}",
        flush=True,
    )

    raise


# ============================================================
# RQ QUEUE
# ============================================================

queue = Queue(
    name=QUEUE_NAME,
    connection=redis_connection,
)


print(
    f"[RQ] Queue name: {queue.name}",
    flush=True,
)

print(
    f"[RQ] Queue key: {queue.key}",
    flush=True,
)