import redis

from rq import Queue

from app.config import Config



redis_connection = redis.from_url(
    Config.REDIS_URL
)



queue = Queue(
    "log_processing",
    connection=redis_connection
)