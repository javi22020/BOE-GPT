from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from llama_cpp.server.app import create_app
from llama_cpp.server.settings import ModelSettings, ServerSettings
import json, uvicorn, wget, os, threading
os.makedirs("models", exist_ok=True)
models = json.load(open("models.json", "r", encoding="utf-8"))
UPLOAD_DIR = "models"
model_settings = []
if len(os.listdir("models")) == 0:
    wget.download(models[0]["url"], out=f"models/{models[0]['filename']}")
for m in models:
    model_settings.append(
        ModelSettings(
            **{
                "model": "models/" + m["filename"],
                "model_alias": m["alias"],
                "n_gpu_layers": m["config"]["n_gpu_layers"],
                "n_ctx": m["config"]["n_ctx"],
            },
            flash_attn=True
        )
    )

app = create_app(
    model_settings=model_settings,
    server_settings=ServerSettings(
        host="0.0.0.0",
        port=4550
    )
)

@app.get("/heartbeat")
def heartbeat():
    return {"message": "Alive"}

@app.post("/receive")
async def receive_file_chunk(request: Request):
    # Extract file information from headers
    file_name = request.headers.get("X-File-Name")
    chunk_number = int(request.headers.get("X-Chunk-Number"))
    total_chunks = int(request.headers.get("X-Total-Chunks"))

    if not all([file_name, chunk_number, total_chunks]):
        raise HTTPException(status_code=400, detail="Missing required headers")

    # Create a unique file name to avoid conflicts
    base_name, extension = os.path.splitext(file_name)
    unique_file_name = f"{base_name}_{chunk_number}{extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_file_name)

    # Read the chunk data
    chunk_data = await request.body()

    # Write the chunk to a file
    with open(file_path, "wb") as f:
        f.write(chunk_data)

    # If this is the last chunk, combine all chunks
    if chunk_number == total_chunks - 1:
        await combine_chunks(file_name, total_chunks)
        
        return JSONResponse(content={"message": "File upload completed"}, status_code=200)
    
    return JSONResponse(content={"message": f"Chunk {chunk_number + 1} of {total_chunks} received"}, status_code=200)

async def combine_chunks(file_name: str, total_chunks: int):
    base_name, extension = os.path.splitext(file_name)
    final_file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(final_file_path, "wb") as final_file:
        for i in range(total_chunks):
            chunk_file_name = f"{base_name}_{i}{extension}"
            chunk_file_path = os.path.join(UPLOAD_DIR, chunk_file_name)
            
            with open(chunk_file_path, "rb") as chunk_file:
                final_file.write(chunk_file.read())
            
            # Remove the chunk file after combining
            os.remove(chunk_file_path)
            
if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=4550)

    