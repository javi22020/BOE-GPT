from .llamacpp_embeddings import LlamaCPPEmbeddings
from chromadb import Documents
def embed_documents(docs: Documents):
    embeddings = LlamaCPPEmbeddings()
    return embeddings(docs)