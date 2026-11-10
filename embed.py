import os
import requests
from dotenv import load_dotenv

import math

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')
MODEL = "gemini-embedding-001"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:embedContent"
HEADERS = {"X-goog-api-key":API_KEY,"Content-Type":"application/json"}

def embed(text):
    payload = {
        "model":f"models/{MODEL}",
        "content": {"parts": [{"text":text}]}
    }

    response = requests.post(URL,headers=HEADERS,json=payload,timeout=30)

    if response.status_code != 200:
        print("API error:", response.status_code,response.text)
        return None
    return response.json()['embedding']['values']

# vector = embed("I was charged twice for my order")

def cosine_similarity(a,b):
    dot = sum(x * y for x , y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    return dot / (norm_a * norm_b)

if __name__ == "__main__":
    docs = [
    "How to reset your password",
    "Refund policy for duplicate charges",
    "Troubleshooting app crashes on Android",
    "Adding dark mode to the dashboard",
    "Payment methods we accept",
    ]
    doc_vectors = [embed(d) for d in docs]

    query = input("Ask something: ")

    query_vectors = embed(query)

    scores = [(cosine_similarity(query_vectors, v),d) for v,d in zip(doc_vectors,docs)]
    scores.sort(reverse = True)

    for score, doc in scores[:3]:
        print(f"{score:.3f} {doc}")





