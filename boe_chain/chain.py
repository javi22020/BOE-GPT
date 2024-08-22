import openai
from langchain_openai.chat_models.base import ChatOpenAI
from chromadb import HttpClient
from langchain_chroma.vectorstores import Chroma
from llamacpp_embeddings import LlamaCPPEmbeddings
from langchain.chains.retrieval_qa.base import VectorDBQA
class BOEGPTChain():
    def __init__(self) -> None:
        self.llm = ChatOpenAI(
            base_url="http://llm:4550/v1",
            streaming=True
        )
        self.chroma = Chroma(client=HttpClient(host="chroma", port=8000), collection_name="docs", embedding_function=LlamaCPPEmbeddings())
        self.vector_db = VectorDBQA.from_llm(vectorstore=self.chroma, llm=self.llm)

    def query(self, query: str):
        for m in self.vector_db.stream(input={"query": query}):
            yield m