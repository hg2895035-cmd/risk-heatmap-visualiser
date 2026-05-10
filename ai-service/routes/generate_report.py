from flask import Blueprint, request, jsonify, Response
import json
import time
import logging
from datetime import datetime
from threading import Thread
from uuid import uuid4

from services.groq_client import GroqClient
from services.cache import get_cached, set_cache

logger = logging.getLogger(__name__)

generate_report_bp = Blueprint("generate_report", __name__)

# In-memory job store
job_store = {}

REPORT_PROMPT = """Generate a comprehensive risk report for the following input.

Input: "{input_text}"

Return ONLY valid JSON in this exact format:
{{
  "title": "Report title",
  "executive_summary": "2-3 sentences summarizing key risks and recommendations",
  "overview": "Detailed overview of the situation",
  "top_items": [
    {{
      "item": "Key finding or risk",
      "impact": "High|Medium|Low",
      "description": "Details"
    }},
    {{
      "item": "Key finding or risk",
      "impact": "High|Medium|Low",
      "description": "Details"
    }},
    {{
      "item": "Key finding or risk",
      "impact": "High|Medium|Low",
      "description": "Details"
    }}
  ],
  "recommendations": [
    {{
      "recommendation": "Actionable recommendation",
      "priority": "High|Medium|Low",
      "timeline": "Immediate|Short-term|Long-term"
    }},
    {{
      "recommendation": "Actionable recommendation",
      "priority": "High|Medium|Low",
      "timeline": "Immediate|Short-term|Long-term"
    }},
    {{
      "recommendation": "Actionable recommendation",
      "priority": "High|Medium|Low",
      "timeline": "Immediate|Short-term|Long-term"
    }}
  ]
}}

Rules:
- Output ONLY valid JSON, no explanation or markdown
- Include at least 3 top_items and 3 recommendations
- Do NOT cut off mid-sentence
- All fields are required
"""

def process_report(job_id, input_text, use_stream=False):
    """Background job to generate report"""
    try:
        prompt = REPORT_PROMPT.replace("{input_text}", input_text)

        response = GroqClient.generate_response([
            {"role": "user", "content": prompt}
        ], max_tokens=4096)

        if response["error"]:
            job_store[job_id]["status"] = "failed"
            job_store[job_id]["error"] = "AI service error"
            return

        # Parse JSON
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
            logger.warning("Failed to parse report as JSON")
            parsed = {
                "title": "Risk Report",
                "executive_summary": response["content"][:200],
                "overview": response["content"],
                "top_items": [],
                "recommendations": []
            }

        job_store[job_id]["status"] = "completed"
        job_store[job_id]["data"] = parsed
        job_store[job_id]["tokens"] = response["tokens"]
        job_store[job_id]["model"] = response["model"]

    except Exception as e:
        logger.error(f"Report processing error: {e}")
        job_store[job_id]["status"] = "failed"
        job_store[job_id]["error"] = str(e)

@generate_report_bp.route("/generate-report", methods=["POST"])
def generate_report():
    """Create an async report generation job"""
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' field"}), 400

        input_text = data["text"]
        if not input_text or len(input_text.strip()) < 10:
            return jsonify({"error": "Text must be at least 10 characters"}), 400

        # Check cache first
        cache_key = f"report:{hash(input_text)}"
        cached = get_cached(cache_key)
        if cached:
            cached["meta"]["cached"] = True
            return jsonify(cached)

        # Create job
        job_id = str(uuid4())
        job_store[job_id] = {
            "status": "processing",
            "created_at": datetime.utcnow().isoformat(),
            "data": None,
            "error": None,
            "tokens": 0,
            "model": "llama-3.3-70b-versatile"
        }

        # Start background job
        thread = Thread(target=process_report, args=(job_id, input_text, False))
        thread.daemon = True
        thread.start()

        return jsonify({
            "job_id": job_id,
            "status": "processing",
            "status_url": f"/job/{job_id}"
        }), 202

    except Exception as e:
        logger.error(f"Generate report error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@generate_report_bp.route("/job/<job_id>", methods=["GET"])
def get_job_status(job_id):
    """Check job status"""
    if job_id not in job_store:
        return jsonify({"error": "Job not found"}), 404

    job = job_store[job_id]

    if job["status"] == "completed":
        result = {
            **job["data"],
            "meta": {
                "job_id": job_id,
                "status": "completed",
                "model": job["model"],
                "tokens_used": job["tokens"],
                "generated_at": job["created_at"]
            }
        }
        return jsonify(result)
    elif job["status"] == "failed":
        return jsonify({
            "status": "failed",
            "error": job["error"]
        }), 500
    else:
        return jsonify({
            "status": "processing",
            "job_id": job_id
        }), 202

@generate_report_bp.route("/report-stream/<job_id>", methods=["GET"])
def stream_report(job_id):
    """SSE stream for job progress"""
    if job_id not in job_store:
        return jsonify({"error": "Job not found"}), 404

    def generate():
        while True:
            job = job_store[job_id]
            if job["status"] == "completed":
                yield f"data: {json.dumps({'status': 'completed', 'data': job['data']})}\n\n"
                break
            elif job["status"] == "failed":
                yield f"data: {json.dumps({'status': 'failed', 'error': job['error']})}\n\n"
                break
            else:
                yield f"data: {json.dumps({'status': 'processing'})}\n\n"
                time.sleep(1)

    return Response(generate(), mimetype="text/event-stream")
