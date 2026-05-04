from flask import Flask, jsonify, request

#  Security & Rate Limiting (from main)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

#  Your routes (from ayushi)
from routes.categorise import categorise_bp
from routes.batch_categorise import batch_bp
from routes.similar import similar_bp
from routes.query import query_bp
from routes.health import health_bp
from routes.generate_report import generate_report_bp

#  Optional test route (from main)
from routes.test_route import test_bp

#  Cache stats
from services.cache import get_stats

app = Flask(__name__)

# =========================
#  SECURITY (from main)
# =========================
talisman = Talisman(
    app,
    force_https=False,
    strict_transport_security=False,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self'",
        'style-src': "'self'"
    },
    x_content_type_options=True,
    frame_options='DENY',
    referrer_policy='strict-origin-when-cross-origin'
)

# =========================
#  RATE LIMITING (from main)
# =========================
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

# =========================
#  HEALTH CHECK (MERGED)
# =========================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "ai-service",
        "cache": get_stats()
    })

# =========================
#  REGISTER YOUR ROUTES
# =========================
app.register_blueprint(categorise_bp)
app.register_blueprint(batch_bp)
app.register_blueprint(similar_bp)
app.register_blueprint(query_bp)
app.register_blueprint(health_bp)
app.register_blueprint(generate_report_bp)
app.register_blueprint(test_bp)

# =========================
#  RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)