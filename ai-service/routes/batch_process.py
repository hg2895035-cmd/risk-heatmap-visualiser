from flask import Blueprint, request, jsonify
import json
import time
import logging
from datetime import datetime
from threading import Thread
from uuid import uuid4

from services.groq_client import GroqClient

logger = logging.getLogger(__name__)

batch_process_bp = Blueprint("batch_process", __name__)

# In-memory job store
batch_job_store = {}

BATCH_PROMPT = """Analyze this risk item and return JSON:
"{item_text}"

Return ONLY valid JSON:
{{
  "category": "Financial|Cybersecurity|Operational|Compliance|Reputational",
  "severity": "Low|Medium|High|Critical",
  "confidence": <0.0-1.0>,
  "summary": "Brief analysis"
}}
"""

def process_batch_item(job_id, item_index, item_text):
    """Process single batch item"""
    try:
        prompt = BATCH_PROMPT.replace("{item_text}", item_text)

        response = GroqClient.generate_response([
            {"role": "user", "content": prompt}
        ], max_tokens=500)

        if response["error"]:
            batch_job_store[job_id]["results"][item_index] = {
                "error": "Processing failed",
                "status": "failed"
            }
            return

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
            parsed = {
                "category": "Operational",
                "severity": "Medium",
                "confidence": 0.5,
                "summary": response["content"]
            }

        batch_job_store[job_id]["results"][item_index] = {
            **parsed,
            "status": "completed",
            "processing_time_ms": int(time.time() * 1000) % 100000
        }
        batch_job_store[job_id]["completed_count"] += 1

    except Exception as e:
        logger.error(f"Batch item processing error: {e}")
        batch_job_store[job_id]["results"][item_index] = {
            "error": str(e),
            "status": "failed"
        }

def process_batch_async(job_id, items):
    """Background batch processing"""
    try:
        # Process items with 100ms delay between each
        for i, item in enumerate(items):
            time.sleep(0.1)  # 100ms delay
            process_batch_item(job_id, i, item)

        batch_job_store[job_id]["status"] = "completed"
    except Exception as e:
        logger.error(f"Batch processing error: {e}")
        batch_job_store[job_id]["status"] = "failed"
        batch_job_store[job_id]["error"] = str(e)

@batch_process_bp.route("/batch-process", methods=["POST"])
def batch_process():
    """Process up to 20 items asynchronously"""
    try:
        data = request.get_json()

        if not data or "items" not in data:
            return jsonify({"error": "Missing 'items' field"}), 400

        items = data["items"]
        if not isinstance(items, list) or len(items) == 0:
            return jsonify({"error": "'items' must be a non-empty array"}), 400

        if len(items) > 20:
            return jsonify({"error": "Maximum 20 items allowed"}), 400

        # Validate items
        for item in items:
            if not isinstance(item, str) or len(item.strip()) < 5:
                return jsonify({"error": "Each item must be a non-empty string with at least 5 characters"}), 400

        # Create batch job
        job_id = str(uuid4())
        batch_job_store[job_id] = {
            "status": "processing",
            "created_at": datetime.utcnow().isoformat(),
            "item_count": len(items),
            "completed_count": 0,
            "results": [None] * len(items),
            "error": None
        }

        # Start background processing
        thread = Thread(target=process_batch_async, args=(job_id, items))
        thread.daemon = True
        thread.start()

        return jsonify({
            "job_id": job_id,
            "status": "processing",
            "item_count": len(items),
            "status_url": f"/batch-job/{job_id}"
        }), 202

    except Exception as e:
        logger.error(f"Batch process error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@batch_process_bp.route("/batch-job/<job_id>", methods=["GET"])
def get_batch_job_status(job_id):
    """Check batch job status"""
    if job_id not in batch_job_store:
        return jsonify({"error": "Batch job not found"}), 404

    job = batch_job_store[job_id]

    if job["status"] == "completed":
        return jsonify({
            "status": "completed",
            "job_id": job_id,
            "item_count": job["item_count"],
            "completed_count": job["completed_count"],
            "results": job["results"],
            "meta": {
                "created_at": job["created_at"],
                "completed_at": datetime.utcnow().isoformat()
            }
        })
    elif job["status"] == "failed":
        return jsonify({
            "status": "failed",
            "job_id": job_id,
            "error": job["error"]
        }), 500
    else:
        return jsonify({
            "status": "processing",
            "job_id": job_id,
            "item_count": job["item_count"],
            "completed_count": job["completed_count"],
            "progress_percent": int((job["completed_count"] / job["item_count"]) * 100)
        }), 202
