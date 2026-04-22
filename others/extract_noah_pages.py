import fitz  # PyMuPDF
import os
import sys

def extract_pages_as_images(pdf_path, output_folder):
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found.")
        return

    os.makedirs(output_folder, exist_ok=True)
    
    doc = fitz.open(pdf_path)
    print(f"Total pages: {len(doc)}")
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better quality
        output_path = os.path.join(output_folder, f"page_{page_num}.png")
        pix.save(output_path)
        if page_num % 10 == 0:
            print(f"Saved page {page_num}")
            
    print(f"✅ Extracted {len(doc)} pages to '{output_folder}'")

if __name__ == "__main__":
    pdf = "others/noah-to-abraham-teacher-notes.pdf"
    output = "others/noah-images"
    extract_pages_as_images(pdf, output)
