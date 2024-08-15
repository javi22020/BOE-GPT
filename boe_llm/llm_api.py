from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from llama_cpp_llm import LlamaCPPLLM
import json, os, wget
app = FastAPI()

@app.post("/start_llm")
def start_llm(model_path: str, n_gpu_layers: int = 32, n_ctx: int = 128000):
    global llm
    try:
        llm = LlamaCPPLLM(model_path=model_path, n_gpu_layers=n_gpu_layers, n_ctx=n_ctx)
        return {"message": "LLM started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/chat_stream")
def chat_stream(messages: list, max_tokens: int):
    try:
        return StreamingResponse(llm.chat_stream(messages=messages, max_tokens=max_tokens))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/all_llms")
def get_all_llms():
    models = json.load(open("models.json", "r", encoding="utf-8"))
    return models

@app.get("/downloaded_llms")
def get_llms():
    models = json.load(open("models.json", "r", encoding="utf-8"))
    llms = []
    files = os.listdir("models")
    for model in models:
        if model["filename"] in files:
            llms.append(model)
    return llms

@app.post("/download_llm")
def download_llm(model_index: int):
    models = json.load(open("models.json", "r", encoding="utf-8"))
    if model_index >= len(models):
        raise HTTPException(status_code=404, detail="Model not found")
    if os.path.exists("models/" + models[model_index]["filename"]):
        return JSONResponse(content={"message": "Model already downloaded"})
    else:
        try:
            wget.download(models[model_index]["url"], "models/" + models[model_index]["filename"])
            return JSONResponse(content={"message": "Model downloaded"})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))