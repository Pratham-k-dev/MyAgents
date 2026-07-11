import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.models.generate_content(
    model="gemma-4-26b-a4b-it",
    contents="Say hello in one sentence."
)

print(response.text)

# for model in client.models.list():
#     if "generateContent" in model.supported_actions:
#         print(model.name)