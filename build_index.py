import time
import chromadb
from embed import embed

# def chunk_test(text, size=600, overlap=100):
#     chunks = []
#     start = 0
#     while start < len(text):
#         end = start + size
#         chunks.append(text[start:end].strip())
#         start = end - overlap
#     return [c for c in chunks if c != ""]

def build_index():

    client = chromadb.PersistentClient(path='./chroma_db')

    try:
        client.delete_collection('knowledge')
    except Exception:
        pass

    collection = client.create_collection(
        name='knowledge',
        metadata={'hnsw:space':'cosine'}
        )

    with open("knowledge.txt", encoding="utf-8") as f:
        text = f.read()


    chunks = [p.strip() for p in text.split("\n\n") if p.strip()]

    ids = []
    vectors = []
    kept_docs = []

    for i,doc in enumerate(chunks):
        vector = embed(doc)
        if vector is None:
            print("Skipping (embedding failed): ",doc)
            continue
        ids.append(f"kb{i}")
        kept_docs.append(doc)
        vectors.append(vector)
        time.sleep(1)

    collection.upsert(ids=ids,documents=kept_docs,embeddings=vectors)
    return len(kept_docs)

if __name__ == "__main__":
    print("Stored",build_index(),"chunks")







