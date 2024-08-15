import chromadb, requests as r
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import os, base64, random as rn
from pdf_reader import PDFReader
from pdf_service import get_boe_pdfs
from llamacpp_embeddings import LlamaCPPEmbeddings
vector_db = chromadb.PersistentClient("./chroma")
embedding_function = LlamaCPPEmbeddings("model/nomic-embed-text-v1.5.Q4_K_M.gguf")
collection = vector_db.get_or_create_collection("boes", embedding_function=embedding_function)
app = FastAPI()
reader = PDFReader()

def divide_text(text: str, max_length: int = 4096):
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

@app.get("/")
async def root():
    return {"message": "Welcome to the Chroma API"}

@app.post("/compute_embeddings")
async def compute_embeddings(max_length: int = 2048):
    documents = await reader.extract_texts_from_folder("pdfs")
    final_docs = []
    for doc in documents:
        final_docs.extend(divide_text(doc, max_length=max_length))
    print(f"Extracted {len(documents)} documents and divided them into {len(final_docs)} parts")
    rn.seed(5)
    ids = []
    for doc in documents:
        doc_id = list(base64.b64encode(doc.encode()).decode())
        rn.shuffle(doc_id)
        ids.append("".join(doc_id[:16]))
        print(f"Document ID: {ids[-1]}")
    print(f"Adding {len(documents)} documents to the collection")
    collection.add(ids=ids, documents=documents)
    return JSONResponse(content={"message": "Embeddings computed and added to the collection"})

@app.get("/query/{query}")
def query(query: str):
    return collection.query(query_texts=[query])

@app.post("/download/{date}")
async def download_boe(date: str):
    try:
        await get_boe_pdfs(date)
        return JSONResponse(content={"message": "Downloaded BOE PDFs"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))