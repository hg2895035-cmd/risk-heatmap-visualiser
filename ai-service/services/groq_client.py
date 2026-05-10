import os
from groq import Groq
import logging

logger = logging.getLogger(__name__)

class GroqClient:
    client = None
    model = "llama-3.3-70b-versatile"

    @staticmethod
    def init():
        if GroqClient.client is None:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not set in environment")
            GroqClient.client = Groq(api_key=api_key)

    @staticmethod
    def generate_response(messages, temperature=0.7, max_tokens=1024):
        try:
            GroqClient.init()
            response = GroqClient.client.messages.create(
                model=GroqClient.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return {
                "content": response.content[0].text,
                "tokens": response.usage.output_tokens,
                "model": GroqClient.model,
                "error": None
            }
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            return {
                "content": None,
                "tokens": 0,
                "model": GroqClient.model,
                "error": str(e)
            }
