import os
from pathlib import Path

from dotenv import load_dotenv

import redis
from rq import Worker, Queue


# Load .env
project_root = Path(__file__).resolve().parent.parent
env_path = project_root / ".env"

load_dotenv(env_path)


listen = [
    "log_processing"
]


redis_url = os.getenv(
    "REDIS_URL"
)


if not redis_url:
    raise RuntimeError(
        "REDIS_URL is missing. Check your .env file."
    )


redis_connection = redis.from_url(
    redis_url
)


if __name__ == "__main__":

    queue = Queue(
        "log_processing",
        connection=redis_connection
    )

    worker = Worker(
        [queue],
        connection=redis_connection
    )

    worker.work()