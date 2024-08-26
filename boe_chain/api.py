from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from chain import BOEGPTChain

app = FastAPI()

# Configuración CORS
origins = [
    "http://localhost:3000",  # URL de tu aplicación React
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
def stream_chat(query: str = Body(..., embed=True)):
    return StreamingResponse(chain.query_stream(query), media_type="text/event-stream")

@app.get("/heartbeat")
def heartbeat():
    return {"message": "Alive"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3550)