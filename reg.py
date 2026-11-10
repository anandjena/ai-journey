import requests
import os
import chromadb
from dotenv import load_dotenv
from embed import embed
import time

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-3.5-flash"
GEN_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
HEADERS = {'X-goog-api-key':API_KEY,"Content-Type":"application/json"}
MIN_SCORE = 0.58

def retrive(question,collection_name='knowledge',n_results=4):
    client = chromadb.PersistentClient('./chroma_db')
    collection = client.get_collection(collection_name)

    query_vector = embed(question)

    if query_vector is None:
        return None

    results = collection.query(query_embeddings=[query_vector],n_results=n_results)

    macthes = []

    for doc,dist in zip(results["documents"][0],results['distances'][0]):
        score = 1- dist
        if score > MIN_SCORE:
            macthes.append((score,doc))

    if not macthes:
        return []

    return macthes

def ask_llm(prompt,retries=3):

    payload = {
        "contents":[
            {
                "parts":[{"text":prompt}]
            }
        ]
    }

    for attempt in range(retries):

        response = requests.post(GEN_URL,headers=HEADERS,json=payload,timeout=30)

        if response.status_code in (429,503):
            wait = 15 * (attempt + 1)
            print(f"API busy (HTTP{response.status_code}), Retrying in {wait}s...")
            time.sleep(wait)
            continue

        if response.status_code != 200:
            print("API error:",response.status_code,response.text)
            return None
        else:
            try:
                data = response.json()
                text = data['candidates'][0]['content']['parts'][0]['text']
            except(KeyError,IndexError):
                print("Unexpected response shape:",response.text)
                return None
            answer = text.strip()

            return answer

def build_prompt(question, docs):
    context = "\n\n".join(docs)
    return (
        "You are a customer support assistant. "
        "Answer the question using ONLY the policy text below. Be concise. "
        "If the policy text does not state the answer, reply exactly: "
        "\"I don't know based on our policy. Please contact customer support.\" "
        "Do not guess or use outside knowledge.\n\n"
        f"Policy text:\n{context}\n\n"
        f"Question: {question}"
    )

def answer_question(question):
    matches = retrive(question,"knowledge",4)
    if matches is None:
        return None,[]
    if not matches:
        return "I  couldn't find anything relevant.",[]
    docs = [doc for score,doc in matches]
    prompt = build_prompt(question,docs)
    answer = ask_llm(prompt)

    if answer is None:
        return None,matches
    return answer,matches

