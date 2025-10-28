import os
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Use in-memory Chroma for hosting
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("aibitsoft")

app = FastAPI(title="Aibitsoft Chatbot API")

def retrieve_context(question, k=6):
    q_emb = client.embeddings.create(
        input=question,
        model="text-embedding-3-small"
    ).data[0].embedding
    results = collection.query(query_embeddings=[q_emb], n_results=k)
    docs = results["documents"][0]
    return "\n\n".join(docs)

@app.get("/ask")
async def ask(q: str = Query(...)):
    context = retrieve_context(q)
    if not context:
        return JSONResponse({"answer": "I don't know."})
    messages = [
        {"role": "system", "content": (
            "You are an AI assistant for https://aibitsoft.com. "
            "Answer ONLY using the provided context. "
            "If unsure, say 'I don't know'. Be concise."
            "When asked about process, methodology, or steps, refer to Discover, Design, Develop, Deliver, and Grow."
        )},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{q}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2,
        max_tokens=400
    )
    answer = response.choices[0].message.content.strip()
    return JSONResponse({"answer": answer})

@app.get("/")
def root():
    return {"status": "ok", "message": "Aibitsoft chatbot is live!"}
