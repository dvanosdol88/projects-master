import os
import redis

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
client = redis.Redis(host=redis_host, port=redis_port)
