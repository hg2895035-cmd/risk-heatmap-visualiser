from flask import Blueprint, request, jsonify
from services.groq_client import GroqClient
from services.vector_store import store_risk
import json

categorise_bp = Blueprint("categorise", __name__)

@categorise_bp.route("/categorise", methods=["POST"])
def categorise():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    user_text = data["text"]

    prompt = f"""
    You are an AI risk analysis system.

Analyze the following text and return:

1. category (choose one):
   Cybersecurity, Financial, Operational, Compliance, Reputational

2. confidence (0 to 1)

3. severity (Low, Medium, High)

4. impact (integer from 1 to 5)

5. reasoning (short explanation)

Return ONLY valid JSON:
{{
  "category": "...",
  "confidence": 0.0,
  "severity": "...",
  "impact": 0,
  "reasoning": "..."
}}


    Text: {user_text}
    """

    response = GroqClient.generate_response([
        {"role": "user", "content": prompt}
    ])

    try:
        parsed = json.loads(response)
        store_risk(user_text, parsed)
        return jsonify(parsed)
    except Exception:
        return jsonify({
            "category": "Unknown",
            "confidence": 0.0,
            "reasoning": "Failed to parse AI response"
        })