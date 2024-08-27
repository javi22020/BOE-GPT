import openai
from langchain_openai.chat_models.base import ChatOpenAI
from chromadb import HttpClient
from langchain.prompts.prompt import PromptTemplate
from langchain_chroma.vectorstores import Chroma
from llamacpp_embeddings import LlamaCPPEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

class BOEGPTChain():
    def __init__(self) -> None:
        base_url = "http://localhost:4550"
        api_key="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"
        self.client = openai.OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.llm = ChatOpenAI(
            base_url=base_url, # Comentar para usar el servidor de OpenAI
            api_key=api_key,
            model="phi-3.5-mini-instruct",
            streaming=True
        )
        self.chroma = Chroma(client=HttpClient(host="chroma", port=8000), collection_name="docs", embedding_function=LlamaCPPEmbeddings())
        prompt_docs = PromptTemplate.from_template(open("prompt_docs.md", "r", encoding="utf-8").read())
        self.doc_chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt=prompt_docs
        )
        self.chain = create_retrieval_chain(
            retriever=self.chroma.as_retriever(),
            combine_docs_chain=self.doc_chain
        )

    def query(self, query: str):
        r = self.chain.invoke(input={"input": query})
        return r["answer"]
    
    def available_models(self):
        return [m.model_dump_json() for m in self.client.models.list()]
    
    def query_stream(self, query: str):
        for r in self.chain.stream(input={"input": query}):
            if isinstance(r, dict) and "answer" in r:
                yield r["answer"]