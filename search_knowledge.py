import chromadb
from embed import embed

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("knowledge")

while True:
    q = input("\nAsk (or type quit): ")
    if q.strip().lower() == "quit":
        break
    vector = embed(q)
    if vector is None:
        continue
    res = collection.query(query_embeddings=[vector], n_results=4)
    for doc, dist in zip(res["documents"][0], res["distances"][0]):
        print(f"{1 - dist:.3f}  {doc[:80]!r}")