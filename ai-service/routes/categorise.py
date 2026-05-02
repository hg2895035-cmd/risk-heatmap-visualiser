from flask import Blueprint, request, jsonify
from services.groq_client import GroqClient
from services.vector_store import store_risk
from services.cache import get_cached, set_cache
import json

categorise_bp = Blueprint("categorise", __name__)

@categorise_bp.route("/categorise", methods=["POST"])
def categorise():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    user_text = data["text"]
    # Check cache first
    cached = get_cached(user_text)
    if cached:
        return jsonify(cached)

    prompt = f"""
    You are a risk analysis AI.

Analyze the following text and return STRICT JSON ONLY.

Text:
"{user_text}"

Return ONLY this JSON format:
{{
  "category": "<Financial | Cybersecurity | Operational | Compliance | Reputational>",
  "confidence": <0 to 1>,
  "severity": "<Low | Medium | High>",
  "impact": <1 to 5>,
  "reasoning": "<short explanation>"
}}

Rules:
- Do NOT add any extra text
- Do NOT explain anything outside JSON
- Do NOT use markdown (no ``` )
- Output MUST be valid JSON only
    """

    response = GroqClient.generate_response([
        {"role": "user", "content": prompt}
    ])

    try:
        
        parsed = json.loads(response)
        store_risk(user_text, parsed)
        set_cache(user_text, parsed)
        return jsonify(parsed)
    except Exception:
        return jsonify({
            "category": "Unknown",
            "confidence": 0.0,
            "reasoning": "Failed to parse AI response"
        })