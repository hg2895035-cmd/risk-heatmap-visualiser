from flask import Blueprint, request, jsonify
from services.groq_client import GroqClient
from services.vector_store import store_risk
import json

batch_bp = Blueprint("batch", __name__)

@batch_bp.route("/batch-categorise", methods=["POST"])
def batch_categorise():

    data = request.get_json()

    if not data or "texts" not in data:
        return jsonify({"error": "Missing 'texts' field"}), 400

    texts = data["texts"]

    results = []

    for text in texts:

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


        Text: {text}
        """

        response = GroqClient.generate_response([
            {"role": "user", "content": prompt}
        ])

        try:
            cleaned = response.strip().replace("```json", "").replace("```", "")
            parsed = json.loads(cleaned)
        except:
            parsed = {
                "category": "Unknown",
                "confidence": 0.0,
                "reasoning": "Failed to parse AI response"
            }
            store_risk(text, parsed)
        results.append(parsed)

    return jsonify(results)