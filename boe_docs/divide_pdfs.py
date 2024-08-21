from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
def get_documents_from_pdfs(folder: str):
    loader = PyPDFDirectoryLoader(
        path=folder,
        recursive=True
    )
    docs = loader.load()
    return docs

def divide_documents(documents: list):
    splitter = RecursiveCharacterTextSplitter()
    docs = splitter.split_documents(documents=documents)
    return [d.page_content for d in docs]