from flask import Blueprint, request, jsonify
from services.vector_store import search_similar

similar_bp = Blueprint("similar", __name__)

@similar_bp.route("/similar-risks", methods=["POST"])
def similar_risks():

    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text'"}), 400

    user_text = data["text"]

    results = search_similar(user_text)

    formatted = []

    for item in results:
        metadata = item["metadata"]

        formatted.append({
            "text": item["text"],
            "category": metadata.get("category"),
            "confidence": metadata.get("confidence")
        })

    return jsonify(formatted)