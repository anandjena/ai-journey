import chromadb
from embed import embed

client = chromadb.PersistentClient(path='./chroma_db')
collection = client.get_or_create_collection(
    name = "support_docs",
    metadata= {"hnsw:space":"cosine"}
)

with open("docs.txt") as f:
    docs = [line.strip() for line in f if line.strip()]

ids = []
vectors = []
kept_docs = []

for i,doc in enumerate(docs):
    vector = embed(doc)

    if vector is None:
        print("skipping (embedding failed):",doc)
        continue
    ids.append(f"doc{i}")
    vectors.append(vector)
    kept_docs.append(doc)

collection.upsert(ids=ids,documents=kept_docs,embeddings=vectors)
print("Stores",collection.count(),"documents")

