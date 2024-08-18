from get_pdfs import PDFSBOE
from divide_pdfs import get_documents_from_pdfs, divide_documents
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import json
import os

pdfs = PDFSBOE()

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the APIBOE API"}

@app.get("/boe_docs/{date}")
def get_boe_by_date(date: str, max_length: int = 4096, overlap: int = 1024):
    os.makedirs(f"pdfs/{date}", exist_ok=True)
    for i, pdf in enumerate(pdfs.get_boe_by_date(date)):
        with open(f"pdfs/{date}/{i}.pdf", "wb") as f:
            f.write(pdf)
    docs = get_documents_from_pdfs("pdfs")
    docs = divide_documents(documents=docs, max_length=max_length, overlap=overlap)
    def docs_gen():
        for doc in docs:
            yield json.dumps(doc).encode('utf-8') + b'\n'
        return
    return StreamingResponse(docs_gen(), media_type="application/x-ndjson")