from get_pdfs import PDFSBOE
from divide_pdfs import get_documents_from_pdfs, divide_documents
from llamacpp_embeddings import LlamaCPPEmbeddings
from chromadb import Documents
from fastapi import FastAPI, HTTPException
from chromadb import HttpClient
from fastapi.responses import StreamingResponse
from tqdm import tqdm
import requests as r
import json
import os

pdfs = PDFSBOE()
chroma_client = HttpClient(host="chroma", port=5550)
collection = chroma_client.get_or_create_collection("docs")
app = FastAPI()

def embed_documents(docs: Documents):
    embeddings = LlamaCPPEmbeddings()
    return embeddings(docs)

@app.get("/")
def root():
    return {"message": "Welcome to the APIBOE API"}

@app.post("/send_to_chroma/{date}")
def send_to_chroma(date: str):
    try:
        for name, pdf in tqdm(pdfs.get_boe_by_date(date), desc="Downloading PDFs"):
            if pdf:
                if not os.path.exists(f"pdfs/{date}"):
                    os.makedirs(f"pdfs/{date}", exist_ok=True)
                with open(f"pdfs/{date}/{name}.pdf", "wb") as f:
                    f.write(pdf)
        docs, ids = get_documents_from_pdfs(f"pdfs/{date}")
        print("Documents loaded")
        docs = divide_documents(docs)
        print("Documents divided")
        embeddings = embed_documents(docs)
        print("Embeddings generated")
        collection.add(ids=ids, embeddings=embeddings)
    except:
        raise HTTPException(status_code=500, detail="Error processing PDFs")
    
    return {"message": "PDFs processed and sent to ChromaDB"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=6550)