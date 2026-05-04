# ai-service/test_groq.py
import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")  # loads .env from project root

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def test_groq_connection():
    if not GROQ_API_KEY:
        print("❌ GROQ_API_KEY not found in .env")
        return

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": "Say hello in one sentence."}
        ],
        "max_tokens": 50,
        "temperature": 0.3
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        print(f"✅ Groq API working. Response: {reply}")
    except Exception as e:
        print(f"❌ Groq API call failed: {e}")

if __name__ == "__main__":
    test_groq_connection()