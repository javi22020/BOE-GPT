from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from typing import List, Optional
from llamacpp_embeddings import LlamaCPPEmbeddings
app = FastAPI()
embedding_function = LlamaCPPEmbeddings()
# Initialize ChromaDB client
client = chromadb.PersistentClient()

class Document(BaseModel):
    id: str
    content: str
    metadata: Optional[dict] = None

@app.post("/collections/{collection_name}")
async def create_collection(collection_name: str):
    try:
        collection = client.create_collection(name=collection_name)
        return {"message": f"Collection '{collection_name}' created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/collections")
async def list_collections():
    collections = client.list_collections()
    return {"collections": [c.name for c in collections]}

@app.post("/collections/{collection_name}/add")
async def add_documents(collection_name: str, documents: List[Document]):
    try:
        collection = client.get_or_create_collection(name=collection_name, embedding_function=embedding_function)
        ids = [doc.id for doc in documents]
        contents = [doc.content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        collection.add(ids=ids, documents=contents, metadatas=metadatas)
        return {"message": f"Added {len(documents)} documents to collection '{collection_name}'"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/collections/{collection_name}/query")
async def query_collection(collection_name: str, query_text: str, n_results: int = 5):
    try:
        collection = client.get_collection(name=collection_name)
        results = collection.query(query_texts=[query_text], n_results=n_results)
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/collections/{collection_name}")
async def delete_collection(collection_name: str):
    try:
        client.delete_collection(name=collection_name)
        return {"message": f"Collection '{collection_name}' deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5550)