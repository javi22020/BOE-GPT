from get_pdfs import PDFSBOE
from divide_pdfs import get_documents_from_pdfs, divide_documents
from llamacpp_embeddings import LlamaCPPEmbeddings
from chromadb import Documents
from fastapi import FastAPI, HTTPException
from chromadb import HttpClient
from tqdm import tqdm
import requests as r
import base64 as b64
import random as rn
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pdfs = PDFSBOE()
chroma_client = HttpClient(host="chroma", port=8000)
collection = chroma_client.get_or_create_collection("docs")
app = FastAPI()

def embed_documents(docs: Documents):
    embeddings = LlamaCPPEmbeddings()
    return embeddings(docs)

@app.get("/")
def root():
    return {"message": "Welcome to the APIBOE API"}

@app.get("/heartbeat")
def heartbeat():
    return {"message": "Alive"}

@app.post("/send_to_chroma/{date}")
def send_to_chroma(date: str):
    try:
        # Download PDFs
        pdf_count = 0
        ids = []
        for name, pdf in tqdm(pdfs.get_boe_by_date(date), desc="Downloading PDFs"):
            if pdf:
                if not os.path.exists(f"pdfs/{date}"):
                    os.makedirs(f"pdfs/{date}", exist_ok=True)
                ids.append(name)
                with open(f"pdfs/{date}/{name}.pdf", "wb") as f:
                    f.write(pdf)
                pdf_count += 1
        logger.info(f"Downloaded {pdf_count} PDFs")

        # Load documents
        docs = get_documents_from_pdfs(f"pdfs/{date}")
        logger.info(f"Loaded {len(docs)} documents")

        # Divide documents
        docs = divide_documents(docs)
        logger.info(f"Divided into {len(docs)} document chunks")
        
        logger.info(f"Generated {len(ids)} document IDs")

        # Generate embeddings
        embeddings = embed_documents(docs)
        logger.info(f"Generated {len(embeddings)} embeddings")

        # Add to collection
        collection.add(ids=ids, embeddings=embeddings, documents=docs)
        logger.info("Added documents to ChromaDB collection")

        return {"message": f"Successfully processed {pdf_count} PDFs and sent to ChromaDB"}

    except Exception as e:
        logger.error(f"Error in send_to_chroma: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing PDFs: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=6550)