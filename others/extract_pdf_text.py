from pdf2image import convert_from_path

pages = convert_from_path("abraham-teacher-notes.pdf")
for idx, page in enumerate(pages):
    page.save(f"pdf-images/page_{idx}.png", "PNG")
