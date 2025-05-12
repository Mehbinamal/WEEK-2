import pymupdf  

def extract_text_from_pdf(pdf_path):
    # Open the PDF
    doc = pymupdf.open(pdf_path)
    
    all_text = ""  
    # Iterate through each page and extract text
    for page in doc:
        all_text += page.get_text()
    
    # Close the document
    doc.close()
    return all_text

# Example usage:
pdf_text = extract_text_from_pdf('sample-pdf-file.pdf')
print(pdf_text)
