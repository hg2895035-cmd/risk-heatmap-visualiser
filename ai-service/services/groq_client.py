import os
import requests
import time
import logging
from dotenv import load_dotenv
from pathlib import Path

# Load .env
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

# Setup logging
logging.basicConfig(level=logging.INFO)

class GroqClient:

    @staticmethod
    def generate_response(messages, max_tokens=1000, temperature=0.3):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found")

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        retries = 3
        backoff = 2

        for attempt in range(retries):
            try:
                response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=10)
                data = response.json()

                content = data.get("choices", [{}])[0].get("message", {}).get("content")
                if not content:
                    raise ValueError("Empty response from Groq API")
                return {
                        "content": content,
                        "tokens": data.get("usage", {}).get("total_tokens", 0), 
                        "error":False}
            

            except Exception as e:
                logging.error(f"Groq API error (attempt {attempt+1})/{retries}): {e}")
                time.sleep(backoff ** attempt)

        # fallback if all retries fail
        return {
            
            "content": "",
            "tokens": 0,
            "error": True

        }