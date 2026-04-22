import fitz
import json

doc = fitz.open('abraao/abraham-teacher-notes.pdf')
page = doc[0]
blocks = page.get_text("dict")["blocks"]

for i, block in enumerate(blocks[:5]):
    if block["type"] == 0:  # text
        print(f"Block {i} (TEXT):")
        for line in block["lines"]:
            for span in line["spans"]:
                print(f"  Span keys: {span.keys()}")
                print(f"  Span sample: {span['text'][:20]}... Font: {span['font']} Size: {span['size']}")
                break
            break
