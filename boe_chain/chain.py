import openai
from langchain_openai.chat_models.base import ChatOpenAI
from chromadb import HttpClient
from langchain_chroma.vectorstores import Chroma
from llamacpp_embeddings import LlamaCPPEmbeddings
from langchain.chains.retrieval_qa.base import VectorDBQA
class BOEGPTChain():
    def __init__(self) -> None:
        self.llm = ChatOpenAI(
            base_url="http://127.0.0.1:4550/v1",
            streaming=True
        )
        self.chroma = Chroma(client=HttpClient(host="127.0.0.1", port=8000), collection_name="docs", embedding_function=LlamaCPPEmbeddings())
        self.vector_db = VectorDBQA.from_llm(vectorstore=self.chroma, llm=self.llm)

if __name__ == "__main__":
    chain = BOEGPTChain()
    for m in chain.vector_db.stream(input={"query": "Qué sabes del BOE?"}):
        print(m)