from chromadb import HttpClient
from chromadb.config import Settings
from langchain_chroma import Chroma
client = HttpClient(host="localhost", port=5550)