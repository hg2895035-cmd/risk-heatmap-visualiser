from flask import Blueprint, request, jsonify
import json
import time
import logging
from datetime import datetime

from services.groq_client import GroqClient
from services.cache import get_cached, set_cache

logger = logging.getLogger(__name__)

analyse_document_bp = Blueprint("analyse_document", __name__)

ANALYSIS_PROMPT = """You are a document risk analyst. Analyze the document text and extract key insights, risks, and findings.

Document text:
"{document_text}"

Return ONLY valid JSON:
{{
  "document_summary": "Brief summary of document content",
  "key_insights": [
    {{
      "insight": "Important finding or observation",
      "relevance": "Why this matters",
      "confidence": <0.0-1.0>
    }},
    {{
      "insight": "Important finding or observation",
      "relevance": "Why this matters",
      "confidence": <0.0-1.0>
    }},
    {{
      "insight": "Important finding or observation",
      "relevance": "Why this matters",
      "confidence": <0.0-1.0>
    }}
  ],
  "identified_risks": [
    {{
      "risk": "Specific risk identified",
      "severity": "Low|Medium|High|Critical",
      "impact_area": "Business/Technical/Compliance/Reputational",
      "mitigation": "Recommended action"
    }},
    {{
      "risk": "Specific risk identified",
      "severity": "Low|Medium|High|Critical",
      "impact_area": "Business/Technical/Compliance/Reputational",
      "mitigation": "Recommended action"
    }}
  ],
  "findings_array": [
    {{
      "finding": "Key finding",
      "type": "Positive|Negative|Neutral",
      "evidence": "Supporting details"
    }},
    {{
      "finding": "Key finding",
      "type": "Positive|Negative|Neutral",
      "evidence": "Supporting details"
    }}
  ]
}}

Rules:
- Output ONLY valid JSON
- Extract at least 3 key insights and 2 risks
- Base findings on document content
- Set severity and confidence appropriately
"""

@analyse_document_bp.route("/analyse-document", methods=["POST"])
def analyse_document():
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' field"}), 400

        document_text = data["text"]
        if not document_text or len(document_text.strip()) < 20:
            return jsonify({"error": "Document text must be at least 20 characters"}), 400

        start_time = time.time()

        # Check cache
        cache_key = f"analyse:{hash(document_text)}"
        cached = get_cached(cache_key)
        if cached:
            cached["meta"]["cached"] = True
            return jsonify(cached)

        # Format prompt
        prompt = ANALYSIS_PROMPT.replace("{document_text}", document_text[:3000])  # Limit to 3000 chars

        # Call Groq
        response = GroqClient.generate_response([
            {"role": "user", "content": prompt}
        ], max_tokens=3000)

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
            logger.warning("Failed to parse analysis as JSON")
            parsed = {
                "document_summary": document_text[:200],
                "key_insights": [],
                "identified_risks": [],
                "findings_array": []
            }

        response_time = int((time.time() - start_time) * 1000)

        parsed["meta"] = {
            "model": response["model"],
            "tokens_used": response["tokens"],
            "response_time_ms": response_time,
            "cached": False,
            "generated_at": datetime.utcnow().isoformat(),
            "document_length": len(document_text)
        }

        # Cache result
        set_cache(cache_key, parsed)

        return jsonify(parsed)

    except Exception as e:
        logger.error(f"Analyse document error: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500
