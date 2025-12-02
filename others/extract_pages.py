#!/usr/bin/env python3
"""
Script to extract pages 55-75 from abraham-teacher-notes.pdf
"""
from PyPDF2 import PdfReader, PdfWriter

# Input and output files
input_pdf = "abraham-teacher-notes.pdf"
output_pdf = "abraham-pages-55-75.pdf"

# Page range (0-indexed, so page 55 is index 54)
start_page = 54  # Page 55
end_page = 74    # Page 75

print(f"Extracting pages {start_page + 1} to {end_page + 1} from {input_pdf}...")

try:
    # Create PDF reader and writer
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    
    # Get total pages
    total_pages = len(reader.pages)
    print(f"Total pages in PDF: {total_pages}")
    
    # Check if requested pages exist
    if end_page >= total_pages:
        print(f"Warning: PDF only has {total_pages} pages. Adjusting end page to {total_pages}")
        end_page = total_pages - 1
    
    # Extract pages
    for page_num in range(start_page, end_page + 1):
        page = reader.pages[page_num]
        writer.add_page(page)
        print(f"Added page {page_num + 1}")
    
    # Write to output file
    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)
    
    print(f"\n✅ Successfully created {output_pdf} with {end_page - start_page + 1} pages!")
    print(f"   Pages extracted: {start_page + 1} to {end_page + 1}")

except FileNotFoundError:
    print(f"❌ Error: Could not find {input_pdf}")
except Exception as e:
    print(f"❌ Error: {e}")
