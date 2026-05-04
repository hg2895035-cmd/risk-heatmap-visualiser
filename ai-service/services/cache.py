import hashlib
import logging

# In-memory store
cache_store = {}

# Counters
HIT_KEY = 0
MISS_KEY = 0


def generate_key(text):
    return hashlib.sha256(text.encode()).hexdigest()


def get_cached(text):
    global HIT_KEY, MISS_KEY

    key = generate_key(text)

    if key in cache_store:
        HIT_KEY += 1
        logging.info(f"Cache hit: {key}")
        return cache_store[key]

    MISS_KEY += 1
    logging.info(f"Cache miss: {key}")
    return None


def set_cache(text, value):
    key = generate_key(text)
    cache_store[key] = value
    logging.info(f"Stored in cache: {key}")


def get_stats():
    return {
        "hits": HIT_KEY,
        "misses": MISS_KEY
    }