import chromadb
from embed import embed

client = chromadb.PersistentClient(path='./chroma_db')
collection = client.get_collection('support_docs')

query = input("Ask something:")

query_vector = embed(query)

if query_vector is None:
    raise SystemExit("Could not embed the query")

results = collection.query(query_embeddings=[query_vector],n_results=3)
MIN_SCORE = 0.65
matches = []
for doc,dist in zip(results["documents"][0],results["distances"][0]):
    score = 1- dist
    if score > MIN_SCORE:
        matches.append((score,doc))

if not matches:
    raise SystemExit("No relevant document found.")

for score,doc in matches:
     print(f"{score:.3f} {doc}")