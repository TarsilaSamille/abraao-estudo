import fitz

doc = fitz.open('others/noah-to-abraham-teacher-notes.pdf')
for page_num in [0, 4]: # TOC and Session 1
    page = doc[page_num]
    print(f"\n--- Page {page_num+1} ---")
    blocks = page.get_text("dict")["blocks"]
    for block in blocks:
        if block["type"] == 0:
            text = ""
            max_size = 0
            for line in block["lines"]:
                for span in line["spans"]:
                    text += span["text"]
                    max_size = max(max_size, span["size"])
            if "Session" in text:
                print(f"Size: {max_size:.1f} | Text: [{text.strip()}]")
