import redis

from rq import Queue

from app.config import Config


redis_connection = redis.from_url(
    Config.REDIS_URL
)


print(
    "[REDIS]",
    Config.REDIS_URL
)


try:
    print(
        "[REDIS PING]",
        redis_connection.ping()
    )

except Exception as error:
    print(
        "[REDIS ERROR]",
        error
    )


queue = Queue(
    "log_processing",
    connection=redis_connection
)