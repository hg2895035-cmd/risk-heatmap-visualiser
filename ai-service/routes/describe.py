from flask import Blueprint, request, jsonify
import json
import time
import logging
from datetime import datetime

from services.groq_client import GroqClient
from services.cache import get_cached, set_cache
from services.vector_store import add_to_vector_store

logger = logging.getLogger(__name__)

describe_bp = Blueprint("describe", __name__)

def load_prompt_template():
    try:
        with open("prompts/describe.txt", "r") as f:
            return f.read()
    except Exception:
        return """You are a risk analysis AI. Analyze: "{input}" and return JSON with:
        title, category (Financial|Cybersecurity|Operational|Compliance|Reputational),
        severity (Low|Medium|High|Critical), confidence (0-1), description, impact, root_causes, mitigation."""

@describe_bp.route("/describe", methods=["POST"])
def describe():
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' field"}), 400

        user_text = data["text"]
        if not user_text or len(user_text.strip()) < 5:
            return jsonify({"error": "Text must be at least 5 characters"}), 400

        start_time = time.time()

        # Check cache
        cache_key = f"describe:{hash(user_text)}"
        cached = get_cached(cache_key)
        if cached:
            cached["meta"]["cached"] = True
            return jsonify(cached)

        # Load prompt template and format
        prompt_template = load_prompt_template()
        prompt = prompt_template.replace("{input}", user_text)

        # Call Groq
        response = GroqClient.generate_response([
            {"role": "user", "content": prompt}
        ])

        if response["error"]:
            return jsonify({
                "error": "AI service unavailable",
                "fallback": True,
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
            logger.warning("Failed to parse Groq response as JSON")
            parsed = {
                "title": "Risk Analysis",
                "category": "Operational",
                "severity": "Medium",
                "confidence": 0.5,
                "description": response["content"],
                "impact": {"business": "Unknown", "financial": "Unknown", "stakeholders": "Unknown"},
                "root_causes": [],
                "mitigation": "Further investigation required"
            }

        response_time = int((time.time() - start_time) * 1000)

        parsed["meta"] = {
            "model": response["model"],
            "tokens_used": response["tokens"],
            "response_time_ms": response_time,
            "cached": False,
            "generated_at": datetime.utcnow().isoformat()
        }

        # Cache and store in vector DB
        set_cache(cache_key, parsed)
        add_to_vector_store(
            f"describe_{hash(user_text)}",
            user_text,
            {"type": "describe", "category": parsed.get("category")}
        )

        return jsonify(parsed)

    except Exception as e:
        logger.error(f"Describe endpoint error: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500
