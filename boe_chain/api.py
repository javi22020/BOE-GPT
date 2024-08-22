from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
import json
from chain import BOEGPTChain
app = FastAPI()
chain = BOEGPTChain()
@app.get("/chat")
def chat(query: str):
    r = chain.query(query)
    return JSONResponse(content=r)

@app.get("/chat_stream")
def stream_chat(query: str):
    return StreamingResponse(chain.query_stream(query), media_type="text/stream")

@app.get("/heartbeat")
def heartbeat():
    return {"message": "Alive"}