from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/ask")
async def ask(q: str):
    return JSONResponse({"answer": f"You asked: {q}"})
