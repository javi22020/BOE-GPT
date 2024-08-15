from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
import asyncio
import os
class PDFReader:
    def __init__(self) -> None:
        pass

    async def extract_text_from_pdf(self, pdf_path):
        try:
            return extract_text(pdf_path, laparams=LAParams())
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            return ""
    
    async def extract_texts_from_folder(self, folder_path):
        texts = []
        tasks = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_path = os.path.join(root, file)
                    tasks.append(self.extract_text_from_pdf(pdf_path))

        extracted_texts = await asyncio.gather(*tasks)

        texts = [text for text in extracted_texts if text]

        return texts