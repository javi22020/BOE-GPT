from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from llama_cpp_llm import LlamaCPPLLM
import json, os, wget, yaml
config = yaml.safe_load(open("config.yaml", "r", encoding="utf-8"))
models = json.load(open("models.json", "r", encoding="utf-8"))
model_idx = config["model_index"]
model = models[model_idx]
app = FastAPI()

if not os.path.exists("models"):
    os.makedirs("models", exist_ok=True)

if not os.path.exists(f"models/{model['filename']}"):
    wget.download(model["url"], f"models/{model['filename']}")

llm = LlamaCPPLLM(model_path=f"models/{model['filename']}", n_gpu_layers=model["config"]["n_gpu_layers"], n_ctx=model["config"]["n_ctx"])

@app.get("/heartbeat")
def heartbeat():
    return {"message": "Alive"}

@app.post("/chat_stream")
def chat_stream(messages: list, max_tokens: int):
    try:
        return StreamingResponse(llm.chat_stream(messages=messages, max_tokens=max_tokens), media_type="text/stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/all_llms")
def get_all_llms():
    models = json.load(open("models.json", "r", encoding="utf-8"))
    return models

@app.post("/set_llm/{model_index}")
def set_llm(model_index: int):
    yaml.safe_dump({"model_index": model_index}, open("config.yaml", "w", encoding="utf-8"))
    return JSONResponse(content={"message": "Model set"})

@app.get("/downloaded_llms")
def get_llms():
    llms = []
    files = os.listdir("models")
    for m in models:
        if m["filename"] in files:
            llms.append(m)
    return llms

@app.post("/download_llm/{model_index}")
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4550)