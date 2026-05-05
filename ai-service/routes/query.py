from flask import Blueprint, request, jsonify
from services.vector_store import search_similar
from services.groq_client import GroqClient

query_bp = Blueprint("query", __name__)

@query_bp.route("/query", methods=["POST"])
def query():

    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question'"}), 400

    question = data["question"]

    # Retrieve context from DB
    similar = search_similar(question)

    context = "\n".join([item["text"] for item in similar])

    prompt = f"""
Answer the question based on context below.

Context:
{context}

Question:
{question}

Return JSON:
{{
  "answer": "...",
  "sources": ["..."]
}}
"""

    response = GroqClient.generate_response([
        {"role": "user", "content": prompt}
    ])

    return jsonify({"response": response})