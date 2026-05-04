from flask import Blueprint, request, jsonify
from routes.sanitise import sanitise_input

test_bp = Blueprint("test", __name__)

@test_bp.route("/test-sanitise", methods=["POST"])
def test_sanitise():
    data = request.get_json()
    text = data.get("text", "") if data else ""

    clean_text, error = sanitise_input(text)
    if error:
        return error

    return jsonify({
        "status": "ok",
        "clean_input": clean_text
    }), 200