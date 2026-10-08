from google import genai
import os

client = genai.Client(api_key=os.environ.get("GENAI_API_KEY"))

for model in client.models.list():
    print(model.name)