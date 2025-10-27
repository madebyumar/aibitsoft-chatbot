# src/embed_store.py
import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATA_DIR = "data/processed"
chroma_client = chromadb.PersistentClient(path="data/chroma_db")
collection = chroma_client.get_or_create_collection("aibitsoft")

for file in os.listdir(DATA_DIR):
    path = os.path.join(DATA_DIR, file)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    emb = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    ).data[0].embedding
    collection.add(
        ids=[file],
        embeddings=[emb],
        documents=[text],
        metadatas=[{"source": file}]
    )

print("[✔] Embeddings created and stored in ChromaDB.")
