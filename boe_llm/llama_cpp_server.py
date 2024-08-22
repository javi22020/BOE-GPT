from llama_cpp.server.app import create_app
from llama_cpp.server.settings import ModelSettings, ServerSettings
import json, uvicorn, wget, os
os.makedirs("models", exist_ok=True)
models = json.load(open("models.json", "r", encoding="utf-8"))
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
                "n_ctx": m["config"]["n_ctx"]
            }
        )
        
    )

app = create_app(
    model_settings=model_settings,
    server_settings=ServerSettings(
        host="0.0.0.0",
        port=4550
    )
)

@app.get("/download")
def download_model(model: dict):
    filename = model["filename"]
    url = model["url"]
    wget.download(url, out=f"models/{filename}")
    return {"message": f"Downloaded {filename}"}

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=4550)