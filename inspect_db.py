import chromadb

client = chromadb.PersistentClient(path="./chroma_store")
collection = client.get_or_create_collection(name="documents")

# Total chunks stored
print(f"Total chunks stored: {collection.count()}")
print("-" * 60)

# Pehle 5 chunks dekho
results = collection.get(limit=5, include=["documents", "embeddings"])

for i, doc in enumerate(results["documents"]):
    print(f"\nChunk {i+1}:")
    print(f"Text     : {doc[:200]}...")
    print(f"Vector   : {results['embeddings'][i][:5]}...") # sirf pehle 5 values
    print(f"ID       : {results['ids'][i]}")
