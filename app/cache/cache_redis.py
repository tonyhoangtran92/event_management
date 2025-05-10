import json
from functools import wraps

import redis

from app.core.logger import logger
from app.settings import config


def redis_connection():
    cache = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        password=config.REDIS_PASSWORD,
    )
    return cache


def redis_cache(cache_key, expire_time: int = 3600):  # default expire in 1 hour
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                redis_connect = redis_connection()
                cached_data = redis_connect.get(cache_key)
                if cached_data:
                    logger.info(f"Cache hit for {cache_key}")
                    data = json.loads(cached_data)
                    redis_connect.close()
                    return data

                logger.info(f"Cache miss for {cache_key}, fetching from database.")
                result = func(*args, **kwargs)

                serialized_result = json.dumps(result)

                redis_connect.setex(cache_key, expire_time, serialized_result)
                redis_connect.close()

                return result

            except (ConnectionError, TimeoutError):
                logger.info("Redis unavailable, skipping cache")
                return func(*args, **kwargs)

        return wrapper

    return decorator


if __name__ == "__main__":
    cache_test = redis_connection()
    # Test the connection
    try:
        cache_test.ping()
        logger.info("Connected to Redis successfully!")
    except redis.AuthenticationError:
        logger.info("Authentication failed.")
