from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from chain import BOEGPTChain
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chain = BOEGPTChain()

@app.post("/chat")
def chat(query: str = Body(..., embed=True)):
    r = chain.query(query)
    return JSONResponse(content=r)

@app.post("/chat_stream")
async def stream_chat(query: str = Body(..., embed=True)):
    async def event_generator():
        for chunk in chain.query_stream(query):
            yield f"data: {chunk}\n\n"
            await asyncio.sleep(0)  # Allow other tasks to run
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/heartbeat")
def heartbeat():
    return {"message": "Alive"}

@app.get("/available_models")
def available_models():
    return chain.available_models()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3550)