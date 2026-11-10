# Policy Support Bot

A RAG (retrieval-augmented generation) chatbot that answers customer questions
about shipping, returns, refunds, cancellations and warranty, using only the
policy text. If the policy doesn't cover a question, it says "I don't know"
instead of guessing.

**Live demo:** https://ai-journey-bsjr4umuuuztufwkhtwq38.streamlit.app/


<img width="1110" height="785" alt="image" src="https://github.com/user-attachments/assets/1bb7731e-57f2-40bb-86d2-7c8967f95434" />


## How it works
1. The policy text is split into paragraphs (chunks) and embedded with Gemini.
2. Chunks are stored in ChromaDB.
3. A question is embedded, and the closest chunks are retrieved.
4. Chunks below a similarity score of 0.58 are dropped.
5. Gemini answers using only the retrieved text.

## What I learned
- Fixed-size chunks cut the Returns Policy in half and missed the "30 days" rule.
  Splitting by paragraph fixed it.
- A similarity score alone can't tell whether a chunk contains the answer, so the
  prompt also tells the model to refuse when the answer is missing.

## Run locally
```bash
pip install -r requirements.txt
```
Create a `.env` file containing:
```
GEMINI_API_KEY=your_key
```
Then start the app:
```bash
streamlit run streamlit_app.py
```

## Tech stack
Python, Gemini API (generation and embeddings), ChromaDB, Streamlit, FastAPI

## Test results
10 test questions (facts, a reasoning question, and questions the policy doesn't cover).
Result: X/10 passed. [One line on what failed and why, if anything.]

## Limitations
- Works on one short policy document, not thousands of pages.
- Free-tier rate limits (5 requests per minute) can cause delays.
- Topic-related questions the policy doesn't answer rely on the prompt to refuse, not on the score filter.
