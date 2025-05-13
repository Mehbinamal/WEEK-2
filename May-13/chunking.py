from typing import List
import pymupdf  
from langchain.docstore.document import Document

#manual Chunking
def chunk_text(text: str):
    chunks = []
    chunk_size = 500 # Characters
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
        documents = [Document(page_content=chunk, metadata={"source": "local"}) for chunk in chunks]
        print(documents)


#function to extract text from pdf
def extract_text_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)   
    all_text = ""  
    for page in doc:
        all_text += page.get_text()
    doc.close()
    return all_text

# Example usage:
pdf_text = extract_text_from_pdf('May-13/sample-pdf-file.pdf')
chunks = chunk_text(pdf_text)