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
priorities = ["low","medium","high"]

def validate(result):
    if not isinstance(result,dict):
        print("Expected a JSON object, got:", result)
        return None

    category = str(result.get("category","")).strip().lower()
    priority = str(result.get("priority","")).strip().lower()
    summary = str(result.get("summary","")).strip().lower()

    if category not in categories or priority not in priorities or not summary:
        print("Invalid result:", result)
        return None

    return {"category":category,"priority":priority,"summary":summary}

def classify(title):
    prompt = (
       "Analyze this support ticket title and return json with exactly these keys: "
       "category (one of: bug, billing, feature), "
       "priority (one of : low, medium, high), "
       "summary (under 30 words) "
       f"Title : {title}"
    )
    payload = {
        "contents": [
            {
                "parts":[{"text":prompt}]
            }
        ],
        "generationConfig":{"responseMimeType": "application/json"},
    }

    response = requests.post(url,headers=headers,json=payload,timeout=30)
    if response.status_code != 200:
        print("API error:", response.status_code, response.text)
        return None
    else:
       try:
            data = response.json()
            text = data['candidates'][0]['content']['parts'][0]['text']
       except json.JSONDecodeError:
            print("Model returned invalid JSON:", response.text)
            return None
       
    # answer = text.strip().lower().rstrip('.')
    # return answer if answer in categories else "unknown"
    result = json.loads(text)
    return validate(result)
           
    
with open('data.json') as f:
    data = json.load(f)
    for d in data:
        get_text = classify(d['title'])

        if get_text is not None:
            print(f"#{d['id']} | {get_text['category']} | {get_text['priority']} | {get_text['summary']}")






