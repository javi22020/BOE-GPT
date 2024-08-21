from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
def get_documents_from_pdfs(folder: str):
    loader = PyPDFDirectoryLoader(
        path=folder,
        recursive=True
    )
    docs = loader.load()
    docs_contents, ids = [d.page_content for d in docs], [d.id for d in docs]
    return docs_contents, ids

def divide_documents(documents: list):
    splitter = RecursiveCharacterTextSplitter()
    docs = splitter.split_documents(documents=documents)
    return docs