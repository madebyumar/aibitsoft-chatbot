# src/rag_agent.py
from openai import OpenAI
import chromadb, os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma_client = chromadb.PersistentClient(path="data/chroma_db")
collection = chroma_client.get_or_create_collection("aibitsoft")

def retrieve_context(question, k=6):
    q_emb = client.embeddings.create(
        input=question,
        model="text-embedding-3-small"
    ).data[0].embedding
    results = collection.query(query_embeddings=[q_emb], n_results=k)
    docs = results["documents"][0]
    context = "\n\n".join(docs)
    return context


def ask_agent(question):
    context = retrieve_context(question)
    messages = [
        {"role": "system", "content": (
            "You are an AI assistant for https://aibitsoft.com. "
            "Answer ONLY using the provided context. "
            "If unsure, say 'I don't know'. Be concise."
            "Always provide the answer in the same language as the question."
            "Be concise, but complete."
            "When asked about:- process, methodology, or steps → look for terms like Discover, Design, Develop, Deliver, Grow."
        )},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300,
        temperature=0.2
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    while True:
        q = input("Ask Aibitsoft Agent: ")
        print(ask_agent(q))
