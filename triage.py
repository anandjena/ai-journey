import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')

MODEL = "gemini-3.5-flash"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
headers = {'X-goog-api-key':API_KEY,'content-type':'application/json'}
categories = ["bug","billing","feature"]
def classify(title):
    prompt = (
        "Classify this support ticket title as exactly one of : bug,billing,feature. "
        "reply in one word.\n"
        f"Title:{title}"
    )
    payload = {
        "contents": [
            {
                "parts":[{"text":prompt}]
            }
        ]
    }

    response = requests.post(url,headers=headers,json=payload,timeout=30)
    if response.status_code != 200:
        print("API error:", response.status_code, response.text)
        return None
    else:
       try:
            data = response.json()
            text = data['candidates'][0]['content']['parts'][0]['text']
       except(KeyError,IndexError):
            print("Unexpected response shape:", response.text)
            return None
       answer = text.strip().lower().rstrip('.')
       return answer if answer in categories else "unknown"
           
    
with open('data.json') as f:
    data = json.load(f)
    for d in data:
        get_text = classify(d['title'])

        if get_text is not None:
            print(f"#{d['id']} {d['title']} -> {get_text}")






