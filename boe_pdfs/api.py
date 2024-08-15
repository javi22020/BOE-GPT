from .pdfs import PDFSBOE
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import json
import asyncio

pdfsboe = PDFSBOE()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the APIBOE API"}

@app.get("/boe_pdfs/{date}")
async def get_boe_by_date(date: str):
    pdfs = pdfsboe.get_boe_by_date(date)
    
    async def pdf_stream_generator():
        pdf_count = 0
        
        async def stream_pdf(pdf_content):
            nonlocal pdf_count
            if pdf_content is not None:
                metadata = json.dumps({"index": pdf_count, "size": len(pdf_content)}).encode()
                yield len(metadata).to_bytes(4, byteorder='big')
                yield metadata
                yield pdf_content
                pdf_count += 1

        try:
            async for pdf in pdfs:
                if pdf is None:
                    break
                async for chunk in stream_pdf(pdf):
                    yield chunk
            
            # Signal the end of the stream
            end_marker = b"EOF"
            yield len(end_marker).to_bytes(4, byteorder='big')
            yield end_marker
        except Exception as e:
            print(f"Error in stream generation: {e}")
            # Ensure we still send an EOF even if an error occurs
            end_marker = b"EOF"
            yield len(end_marker).to_bytes(4, byteorder='big')
            yield end_marker

    return StreamingResponse(pdf_stream_generator(), media_type="application/octet-stream")