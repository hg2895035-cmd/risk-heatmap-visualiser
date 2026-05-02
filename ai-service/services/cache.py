import redis
import hashlib
import json
# Local fallback cache (if Redis fails)
local_cache = {}

# Try Redis connection
try:
    r = redis.Redis(
    host='redis-17264.c114.us-east-1-4.ec2.cloud.redislabs.com',
    port=17264,
    username='default',
    password='X1VaNKMFA8ZMflrImhGfplbFlYJiJz4X',
    decode_responses=True,
    ssl=True
)
    r.ping()
    print("Connected to Redis successfully")

except Exception as e:
    print(" Redis failed, switching to local cache:", e)
    r = None

# Counters
HIT_KEY = "cache_hits"
MISS_KEY = "cache_misses"


def generate_key(text):
    return hashlib.sha256(text.encode()).hexdigest()


def get_cached(text):
    key = generate_key(text)
    if r:
        data = r.get(key)
        if data:
            r.incr(HIT_KEY)
            return json.loads(data)

        r.incr(MISS_KEY)
        return None

    # fallback (no Redis)
    if key in local_cache:
        return local_cache[key]

    return None

    if data:
        r.incr(HIT_KEY)
        return json.loads(data)

    r.incr(MISS_KEY)
    return None


def set_cache(text, value):
    key = generate_key(text)
    if r:
        r.setex(key, 900, json.dumps(value)) 
    else:
        local_cache[key] = value     


def get_stats():
    if r:
        return {
            "hits": int(r.get(HIT_KEY) or 0),
            "misses": int(r.get(MISS_KEY) or 0)
        }

    return {
        "hits": 0,
        "misses": 0,
        "mode": "local_cache"
    }