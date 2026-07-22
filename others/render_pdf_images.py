#!/usr/bin/env python3
"""Render every teacher-notes PDF to pdf-images/page_N.png (0-indexed), matching abraao/pdf-images convention."""
import fitz, os

ROOT = "/Users/macbook/Documents/GitHub/abraao-estudo"
folders = ["heaven-and-earth","adam-to-noah","jacob","joseph","exodus-overview",
 "ezekiel","jonah","messianic-torah","1-corinthians","ephesians",
 "intro-hebrew-bible","art-of-biblical-words"]

for f in folders:
    pdf = os.path.join(ROOT, f, f"{f}-teacher-notes.pdf")
    outdir = os.path.join(ROOT, f, "pdf-images")
    os.makedirs(outdir, exist_ok=True)
    doc = fitz.open(pdf)
    n = doc.page_count
    for i, page in enumerate(doc):
        out = os.path.join(outdir, f"page_{i}.png")
        if os.path.exists(out):
            continue
        pix = page.get_pixmap(dpi=110)
        pix.save(out)
    print(f"{f}: {n} pages")
    doc.close()
print("DONE")
