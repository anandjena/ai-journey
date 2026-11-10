from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from reg import answer_question

app = FastAPI(title="Policy Support Bot")

class Question(BaseModel):
    question: str = Field(min_length=3,max_length=500)

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/ask")
def ask(body:Question):
    answer, matches = answer_question(body.question)
    if answer is None:
        raise HTTPException(status_code=503,detail="The model is busy, try again shortly.")
    return {
        "answer":answer,
        "sources":[{"score":round(score,3), "text":doc[:200]} for score, doc in matches]
    }