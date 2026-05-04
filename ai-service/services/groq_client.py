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
    def generate_response(messages, max_tokens=300, temperature=0.3):
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
                response = requests.post(GROQ_URL, headers=headers, json=payload)
                response.raise_for_status()

                data = response.json()
                return data["choices"][0]["message"]["content"]

            except Exception as e:
                logging.error(f"Groq API error (attempt {attempt+1}): {e}")
                time.sleep(backoff ** attempt)

        # fallback if all retries fail
        return "AI service temporarily unavailable. Please try again later."