import os
from langchain_community.document_loaders.pdf import PDFMinerLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
def get_documents_from_pdfs(folder: str):
    docs = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".pdf"):
                loader = PDFMinerLoader(file_path=os.path.join(root, file))
                doc = loader.load()[0]
                doc.metadata = {
                    "filename": file.replace(".pdf", ""),
                    "date": root.split("/")[-1]
                }
                docs.append(doc)
    return docs

def divide_documents(documents: list):
    splitter = RecursiveCharacterTextSplitter()
    docs = splitter.split_documents(documents=documents)
    return [d.page_content for d in docs], [d.metadata["filename"] for d in docs]

if __name__ == "__main__":
    docs = get_documents_from_pdfs("pdfs/20230301")
