from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import logging
from datetime import datetime

from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.generate_report import generate_report_bp
from routes.analyse_document import analyse_document_bp
from routes.batch_process import batch_process_bp
from routes.health import health_bp

from services.cache import get_cache_stats, init_cache
from services.vector_store import init_vector_store

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Security
talisman = Talisman(
    app,
    force_https=False,
    strict_transport_security=False,
    content_security_policy={'default-src': "'self'"},
    x_content_type_options=True,
    frame_options='DENY'
)

# Rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"],
    storage_uri="memory://"
)

@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify({
        "error": "Rate limit exceeded",
        "code": "RATE_LIMIT_EXCEEDED",
        "retry_after": "60 seconds"
    }), 429

# Health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "ai-service",
        "timestamp": datetime.utcnow().isoformat(),
        "cache": get_cache_stats()
    })

# Register blueprints
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(generate_report_bp)
app.register_blueprint(analyse_document_bp)
app.register_blueprint(batch_process_bp)
app.register_blueprint(health_bp)

@app.before_request
def init_services():
    init_cache()
    init_vector_store()

if __name__ == "__main__":
    app.run(debug=False, port=5000, use_reloader=False)
