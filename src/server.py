# src/server.py
from fastapi import FastAPI
from rag_agent import ask_agent

app = FastAPI()

@app.get("/ask")
def ask(q: str):
    answer = ask_agent(q)
    return {"answer": answer}

# Run: uvicorn src.server:app --reload
