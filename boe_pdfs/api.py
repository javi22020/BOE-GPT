from .pdfs import PDFSBOE
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

pdfsboe = PDFSBOE()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the APIBOE API"}

@app.get("/boe_pdfs/{date}")
async def get_boe_by_date(date: str):
    pdfs = pdfsboe.get_boe_by_date(date)
    first_pdf = await pdfs.__anext__()
    if first_pdf is None:
        raise HTTPException(status_code=404, detail="BOE not found")
    
    async def pdf_generator():
        yield first_pdf
        async for pdf in pdfs:
            yield pdf

    return StreamingResponse(pdf_generator(), media_type="application/octet-stream")