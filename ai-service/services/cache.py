import os
import redis
import json
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

class CacheService:
    redis_client = None
    cache_ttl = 900  # 15 minutes

    @staticmethod
    def init():
        if CacheService.redis_client is None:
            try:
                redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
                CacheService.redis_client = redis.from_url(redis_url, decode_responses=True)
                CacheService.redis_client.ping()
            except Exception as e:
                logger.warning(f"Redis not available: {e}. Using in-memory cache.")
                CacheService.redis_client = None

    @staticmethod
    def get(key):
        CacheService.init()
        try:
            if CacheService.redis_client:
                value = CacheService.redis_client.get(key)
                return json.loads(value) if value else None
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    @staticmethod
    def set(key, value, ttl=None):
        CacheService.init()
        try:
            if CacheService.redis_client:
                CacheService.redis_client.setex(
                    key,
                    ttl or CacheService.cache_ttl,
                    json.dumps(value)
                )
        except Exception as e:
            logger.error(f"Cache set error: {e}")

    @staticmethod
    def get_stats():
        CacheService.init()
        try:
            if CacheService.redis_client:
                info = CacheService.redis_client.info()
                return {
                    "hits": info.get("keyspace_hits", 0),
                    "misses": info.get("keyspace_misses", 0),
                    "keys": info.get("db0", {}).get("keys", 0)
                }
            return {"hits": 0, "misses": 0, "keys": 0}
        except Exception:
            return {"hits": 0, "misses": 0, "keys": 0}

def init_cache():
    CacheService.init()

def get_cached(key):
    return CacheService.get(key)

def set_cache(key, value):
    CacheService.set(key, value)

def get_cache_stats():
    return CacheService.get_stats()
