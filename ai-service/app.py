from flask import Flask
from routes.categorise import categorise_bp
from routes.batch_categorise import batch_bp
from routes.similar import similar_bp
app = Flask(__name__)

# Register routes
app.register_blueprint(categorise_bp)
app.register_blueprint(batch_bp)
app.register_blueprint(similar_bp)
if __name__ == "__main__":
    app.run(debug=True)