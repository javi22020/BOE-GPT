import os, wget
from chromadb import Documents, EmbeddingFunction, Embeddings
from llama_cpp import Llama
class LlamaCPPEmbeddings(EmbeddingFunction):
    def __init__(self) -> None:
        super().__init__()
        if not os.path.exists("models/nomic-embed-text-v1.5.Q4_K_M.gguf"):
            os.makedirs("models", exist_ok=True)
            wget.download("https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF/resolve/main/nomic-embed-text-v1.5.Q4_K_M.gguf", "models/nomic-embed-text-v1.5.Q4_K_M.gguf")
        self.llama = Llama(
            model_path="models/nomic-embed-text-v1.5.Q4_K_M.gguf",
            n_gpu_layers=12,
            n_threads=8,
            embedding=True
        )
    def __call__(self, input_docs: Documents) -> Embeddings:
        return self.llama.embed(input_docs, normalize=True)
    
    def embed_query(self, query: str) -> Embeddings:
        return self.llama.embed(query, normalize=True)