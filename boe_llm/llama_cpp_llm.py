from llama_cpp.llama import Llama
from typing import Union
class LlamaCPPLLM:
    def __init__(self, model_path: str, n_gpu_layers: int = 32, n_ctx: int = 128000) -> None:
        self.llm = Llama(
            model_path=model_path,
            n_gpu_layers=n_gpu_layers,
            n_ctx=n_ctx,
            flash_attn=True,
            n_threads=8
        )
    
    def chat_stream(self, messages: list, max_tokens: Union[int, None] = None):
        for m in self.llm.create_chat_completion(messages=messages, max_tokens=max_tokens, stream=True):
            if "content" in m["choices"][0]["delta"].keys():
                yield m["choices"][0]["delta"]["content"]