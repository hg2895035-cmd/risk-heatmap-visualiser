from flask import Blueprint, request, jsonify
from threading import Thread
from services.job_store import create_job, update_job, get_job
from services.groq_client import GroqClient
import json
import logging

generate_report_bp = Blueprint("generate_report", __name__)

#  Background processing
def process_report(job_id, user_text):
    prompt = f"""
    You are a risk analysis AI.

    Generate a COMPLETE and VALID JSON response ONLY.

    Do NOT cut off mid sentence.
    Do NOT add any explanation.
    Do NOT use markdown.

    Return STRICT JSON in this format:

    {{
      "title": "...",
      "executive_summary": "...",
      "overview": "...",
      "top_items": [],
      "recommendations": []
    }}

    Text: {user_text}
    """

    response = GroqClient.generate_response([
        {"role": "user", "content": prompt}
    ])
    

    try:
        response_text = response["content"]  
        cleaned = response_text.strip().replace("```json", "").replace("```", "")
        
        # extract JSON safely
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1:
            cleaned = cleaned[start:end+1]
            try:
                parsed = json.loads(cleaned)
            except Exception:
                
                parsed = {
                    "title": "Risk Report",
                    "executive_summary": "Unable to generate full report",
                    "overview": "Partial failure in AI response",
                    "top_items": [],
                    "recommendations": []
                }    
            update_job(job_id, parsed)

    except Exception as e:
        logging.error(f"Report generation failed: {e}")
        update_job(job_id, {"error": "Unable to generate report"})


# Create job (ASYNC)
@generate_report_bp.route("/generate-report", methods=["POST"])
def generate_report():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text'"}), 400

    user_text = data["text"]

    job_id = create_job()

    thread = Thread(target=process_report, args=(job_id, user_text))
    thread.start()

    return jsonify({
        "job_id": job_id,
        "status": "processing"
    })


#  Check job status
@generate_report_bp.route("/job/<job_id>", methods=["GET"])
def get_job_status(job_id):
    job = get_job(job_id)

    if not job:
        return jsonify({"error": "Invalid job_id"}), 404

    return jsonify(job)