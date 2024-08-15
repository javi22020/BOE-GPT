import chromadb, requests as r
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from .pdf_service import get_boe_pdfs
from .llamacpp_embeddings import LlamaCPPEmbeddings
vector_db = chromadb.PersistentClient("./chroma")
embedding_function = LlamaCPPEmbeddings("model/nomic-embed-text-v1.5.Q4_K_M.gguf")
collection = vector_db.get_or_create_collection("boes", embedding_function=embedding_function)
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Chroma API"}

@app.get("/query/{query}")
def query(query: str):
    collection.query(query)

@app.post("/download/{date}")
async def download_boe(date: str):
    await get_boe_pdfs(date)