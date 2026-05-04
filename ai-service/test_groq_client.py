from services.groq_client import GroqClient

response = GroqClient.generate_response([
    {"role": "user", "content": "Explain risk in one line"}
])

print(response)