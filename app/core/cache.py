import redis
import json

try:
    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True,
        socket_connect_timeout=1
    )

    redis_client.ping()
    REDIS_AVAILABLE = True

except Exception:
    REDIS_AVAILABLE = False
    redis_client = None


def set_cache(key, value, ttl=300):
    if not REDIS_AVAILABLE:
        return

    try:
        redis_client.setex(
            key,
            ttl,
            json.dumps(value)
        )
    except Exception:
        pass


def get_cache(key):
    if not REDIS_AVAILABLE:
        return None

    try:
        data = redis_client.get(key)

        if data:
            return json.loads(data)

    except Exception:
        pass

    return None