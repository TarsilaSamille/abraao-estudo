#!/usr/bin/env python3
"""
Script to extract text from abraham-teacher-notes.pdf
"""
from PyPDF2 import PdfReader
import json

# Input file
input_pdf = "abraham-teacher-notes.pdf"

print(f"Extracting text from {input_pdf}...")

try:
    reader = PdfReader(input_pdf)
    total_pages = len(reader.pages)
    print(f"Total pages: {total_pages}\n")
    
    # Extract text from all pages
    all_text = []
    for i, page in enumerate(reader.pages):
        page_num = i + 1
        text = page.extract_text()
        print(f"Page {page_num} ({len(text)} characters)")
        all_text.append({
            'page': page_num,
            'text': text
        })
    
    # Save to JSON file for easier processing
    output_file = "extracted_text.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_text, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Text extracted and saved to {output_file}")
    
    # Also save as plain text
    text_file = "extracted_text.txt"
    with open(text_file, 'w', encoding='utf-8') as f:
        for item in all_text:
            f.write(f"\n{'='*80}\n")
            f.write(f"PAGE {item['page']}\n")
            f.write(f"{'='*80}\n\n")
            f.write(item['text'])
            f.write("\n\n")
    
    print(f"✅ Plain text saved to {text_file}")

except Exception as e:
    print(f"❌ Error: {e}")
