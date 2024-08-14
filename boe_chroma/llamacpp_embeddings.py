from chromadb import Documents, EmbeddingFunction, Embeddings
from llama_cpp import Llama
class LlamaCPPEmbeddings(EmbeddingFunction):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.llama = Llama(
            model_path=path,
            embedding=True
        )
    def __call__(self, input_docs: Documents) -> Embeddings:
        return self.llama.embed(input_docs)
