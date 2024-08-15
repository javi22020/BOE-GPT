import chromadb, requests as r
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import os, base64
from pdf_reader import PDFReader
from pdf_service import get_boe_pdfs
from llamacpp_embeddings import LlamaCPPEmbeddings
vector_db = chromadb.PersistentClient("./chroma")
embedding_function = LlamaCPPEmbeddings("model/nomic-embed-text-v1.5.Q4_K_M.gguf")
collection = vector_db.get_or_create_collection("boes", embedding_function=embedding_function)
app = FastAPI()
reader = PDFReader()
@app.get("/")
async def root():
    return {"message": "Welcome to the Chroma API"}

@app.post("/compute_embeddings")
async def compute_embeddings():
    documents = await reader.extract_texts_from_folder("pdfs")
    print(f"Extracted {len(documents)} documents")
    ids = [base64.b64encode(doc.encode()).decode()[len(doc)//2:len(doc)//2 + 8] for doc in documents]
    collection.add(ids=ids, documents=documents)

@app.get("/query/{query}")
def query(query: str):
    collection.query(query)

@app.post("/download/{date}")
async def download_boe(date: str):
    try:
        await get_boe_pdfs(date)
        return JSONResponse(content={"message": "Downloaded BOE PDFs"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))