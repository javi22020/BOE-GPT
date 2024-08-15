from llama_cpp.llama import Llama

class LlamaCPPLLM:
    def __init__(self, model_path: str, n_gpu_layers: int = 32, n_ctx: int = 128000) -> None:
        self.llm = Llama(
            model_path=model_path,
            n_gpu_layers=n_gpu_layers,
            n_ctx=n_ctx,
            flash_attn=True,
            n_threads=8
        )

if __name__ == "__main__":
    llm = LlamaCPPLLM("models/Starling-LM-7B-beta-Q4_K_M.gguf", n_ctx=8192)
    for m in llm.llm(prompt="Hello, my name is Javier, and this is my story: ", max_tokens=1024, stream=True):
        print(m["choices"][0]["text"], end="")