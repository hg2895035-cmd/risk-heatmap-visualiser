from flask import Blueprint, jsonify
import time
from services.vector_store import collection
from services.cache import get_stats

health_bp = Blueprint("health", __name__)

start_time = time.time()

@health_bp.route("/health", methods=["GET"])
def health():

    uptime = time.time() - start_time
    try:
        chroma_count = collection.count()
    except Exception:
        chroma_count = 0
    response_time_ms = int((time.time() - start_time) * 1000)    
    return jsonify({
        "model": "llama-3.3-70b-versatile",
        "cache": get_stats(),
        "uptime_seconds": round(uptime, 2),
        "chroma_count": chroma_count,
        "response_time_ms": response_time_ms,
        "status": "Healthy"
    })