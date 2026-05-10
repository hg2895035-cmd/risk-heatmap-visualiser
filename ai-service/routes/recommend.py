from flask import Blueprint, request, jsonify
import json
import time
import logging
from datetime import datetime

from services.groq_client import GroqClient
from services.cache import get_cached, set_cache

logger = logging.getLogger(__name__)

recommend_bp = Blueprint("recommend", __name__)

RECOMMEND_PROMPT = """You are a risk mitigation expert. Based on the risk description, provide exactly 3 actionable recommendations.

Risk: "{risk_text}"

Return ONLY valid JSON with exactly 3 recommendations:
{{
  "recommendations": [
    {{
      "action_type": "Preventive|Detective|Corrective",
      "description": "Clear action to take",
      "priority": "High|Medium|Low",
      "timeline": "Immediate|Short-term|Long-term",
      "effort": "Low|Medium|High",
      "expected_outcome": "What will be achieved"
    }},
    {{
      "action_type": "Preventive|Detective|Corrective",
      "description": "Clear action to take",
      "priority": "High|Medium|Low",
      "timeline": "Immediate|Short-term|Long-term",
      "effort": "Low|Medium|High",
      "expected_outcome": "What will be achieved"
    }},
    {{
      "action_type": "Preventive|Detective|Corrective",
      "description": "Clear action to take",
      "priority": "High|Medium|Low",
      "timeline": "Immediate|Short-term|Long-term",
      "effort": "Low|Medium|High",
      "expected_outcome": "What will be achieved"
    }}
  ]
}}

Rules:
- Output ONLY valid JSON
- Must include exactly 3 recommendations
- Vary action types (preventive, detective, corrective)
- Set priorities based on risk impact
"""

@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' field"}), 400

        risk_text = data["text"]
        if not risk_text or len(risk_text.strip()) < 5:
            return jsonify({"error": "Text must be at least 5 characters"}), 400

        start_time = time.time()

        # Check cache
        cache_key = f"recommend:{hash(risk_text)}"
        cached = get_cached(cache_key)
        if cached:
            cached["meta"]["cached"] = True
            return jsonify(cached)

        # Format prompt
        prompt = RECOMMEND_PROMPT.replace("{risk_text}", risk_text)

        # Call Groq
        response = GroqClient.generate_response([
            {"role": "user", "content": prompt}
        ], max_tokens=2048)

        if response["error"]:
            return jsonify({
                "error": "AI service unavailable",
                "fallback": True,
                "recommendations": [
                    {
                        "action_type": "Preventive",
                        "description": "Implement monitoring and detection systems",
                        "priority": "High",
                        "timeline": "Short-term",
                        "effort": "Medium",
                        "expected_outcome": "Early detection of similar risks"
                    }
                ],
                "meta": {
                    "model": "llama-3.3-70b-versatile",
                    "response_time_ms": int((time.time() - start_time) * 1000),
                    "cached": False
                }
            }), 503

        # Parse JSON response
        try:
            cleaned = response["content"].strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.replace("```json", "").replace("```", "").strip()

            start_idx = cleaned.find("{")
            end_idx = cleaned.rfind("}")
            if start_idx != -1 and end_idx != -1:
                cleaned = cleaned[start_idx:end_idx+1]

            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            logger.warning("Failed to parse recommendations as JSON")
            parsed = {
                "recommendations": [
                    {
                        "action_type": "Preventive",
                        "description": response["content"],
                        "priority": "Medium",
                        "timeline": "Short-term",
                        "effort": "Medium",
                        "expected_outcome": "Risk reduction"
                    }
                ]
            }

        response_time = int((time.time() - start_time) * 1000)

        parsed["meta"] = {
            "model": response["model"],
            "tokens_used": response["tokens"],
            "response_time_ms": response_time,
            "cached": False,
            "generated_at": datetime.utcnow().isoformat()
        }

        # Cache result
        set_cache(cache_key, parsed)

        return jsonify(parsed)

    except Exception as e:
        logger.error(f"Recommend endpoint error: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500
