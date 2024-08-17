from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
def get_documents_from_pdfs(folder: str):
    loader = PyPDFDirectoryLoader(
        path=folder,
        recursive=True
    )
    docs = loader.load()
    return docs

def divide_documents(documents: list, max_length: int = 4096, overlap: int = 1024):
    splitter = CharacterTextSplitter(chunk_size=max_length, chunk_overlap=overlap)
    docs = splitter.split_documents(documents=documents)
    return docs