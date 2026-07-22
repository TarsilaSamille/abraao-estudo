#!/usr/bin/env python3
"""Extract embedded raster images from a course PDF, grouped by page.
Saves to <course>/image-extracted/page_<P>_<i>.png  (P = fitz 0-idx page)."""
import fitz, os, sys, json

ROOT = "/Users/macbook/Documents/GitHub/abraao-estudo"
course = sys.argv[1] if len(sys.argv) > 1 else "heaven-and-earth"
pdf = os.path.join(ROOT, course, f"{course}-teacher-notes.pdf")
doc = fitz.open(pdf)
out = os.path.join(ROOT, course, "image-extracted")
os.makedirs(out, exist_ok=True)
total = 0
for pno in range(doc.page_count):
    page = doc[pno]
    imgs = page.get_images(full=True)
    for idx, im in enumerate(imgs):
        xref = im[0]
        try:
            pix = fitz.Pixmap(doc, xref)
            if pix.n - pix.alpha >= 4:  # CMYK: convert
                pix = fitz.Pixmap(fitz.csRGB, pix)
            fn = os.path.join(out, f"page_{pno}_{idx}.png")
            pix.save(fn)
            total += 1
        except Exception as e:
            print("skip", pno, idx, e)
print(f"extracted {total} images -> {out}")
