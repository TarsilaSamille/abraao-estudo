from pdf2image import convert_from_path
import os

# Create directory if it doesn't exist
os.makedirs("pdf-images", exist_ok=True)

pages = convert_from_path("rise-of-the-messiah-teacher-notes.pdf")
for idx, page in enumerate(pages):
    page.save(f"pdf-images/page_{idx}.png", "PNG")

print(f"Extracted {len(pages)} pages to pdf-images/")
