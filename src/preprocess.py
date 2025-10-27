# src/preprocess.py
import os, re, tiktoken

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

enc = tiktoken.get_encoding("cl100k_base")

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def chunk_text(text, max_tokens=800, overlap=100):
    tokens = enc.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens - overlap):
        chunk = enc.decode(tokens[i:i + max_tokens])
        chunks.append(chunk)
    return chunks

if __name__ == "__main__":
    for file in os.listdir(RAW_DIR):
        with open(os.path.join(RAW_DIR, file), encoding="utf-8") as f:
            content = f.read()
        chunks = chunk_text(clean_text(content))
        for i, chunk in enumerate(chunks):
            with open(f"{PROCESSED_DIR}/{file[:-4]}_{i}.txt", "w", encoding="utf-8") as out:
                out.write(chunk)
    print("[✔] Text cleaned and chunked.")
