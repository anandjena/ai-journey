import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')

MODEL = "gemini-3.5-flash"   # change this if you get "model not found"

url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

headers = {"X-goog-api-key":API_KEY,"Content-Type":"application/json"}

payload = {
    "contents" : [
        {
            "parts":[{"text":"Explain what an API is in 2 sentences, for a PHP developer"}]
        }
    ]
}

response = requests.post(url,headers=headers, json=payload)

if response.status_code != 200:
    print("Error:", response.status_code,response.text)
else :
    data = response.json()
    print(data['candidates'][0]['content']['parts'][0]['text'])