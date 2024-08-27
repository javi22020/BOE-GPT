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
        api_key="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"
        self.client = openai.OpenAI(api_key=api_key)
        self.llm = ChatOpenAI(
            # base_url="http://llm:4550/v1",
            api_key=api_key,
            model="gpt-4o-mini",
            streaming=True
        )
        self.chroma = Chroma(client=HttpClient(host="127.0.0.1", port=8000), collection_name="docs", embedding_function=LlamaCPPEmbeddings())
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
            yield str(r) + "\n"