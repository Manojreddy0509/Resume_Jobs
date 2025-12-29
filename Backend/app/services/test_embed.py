import requests
import os
from dotenv import load_dotenv
load_dotenv()


url = "https://openrouter.ai/api/v1/embeddings"

headers = {
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
    "Content-Type": "application/json",
}

payload = {
    "model": "openai/text-embedding-3-small",
    "input": "Hello world"
}

r = requests.post(url, headers=headers, json=payload)
print("Status:", r.status_code)
print("Response:", r.text)
