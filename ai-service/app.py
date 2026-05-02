from flask import Flask
from routes.categorise import categorise_bp
from routes.batch_categorise import batch_bp
from routes.similar import similar_bp
from routes.query import query_bp
from routes.health import health_bp
app = Flask(__name__)
from services.cache import get_stats

@app.route("/health")
def health():
    return {
        "status": "ok",
        "cache": get_stats()
    }
# Register routes
app.register_blueprint(categorise_bp)
app.register_blueprint(batch_bp)
app.register_blueprint(similar_bp)
app.register_blueprint(query_bp)
app.register_blueprint(health_bp)
if __name__ == "__main__":
    app.run(debug=True)