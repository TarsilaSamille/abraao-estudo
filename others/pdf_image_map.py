#!/usr/bin/env python3
"""Map embedded images to their page + bbox, and copy them into a session-usable
folder <course>/image-extracted/ with a manifest mapping page->[images sorted top->bottom]."""
import fitz, os, json, sys, shutil

ROOT = "/Users/macbook/Documents/GitHub/abraao-estudo"
course = sys.argv[1] if len(sys.argv) > 1 else "heaven-and-earth"
pdf = os.path.join(ROOT, course, f"{course}-teacher-notes.pdf")
doc = fitz.open(pdf)
out = os.path.join(ROOT, course, "image-extracted")
os.makedirs(out, exist_ok=True)
# clean old
for f in os.listdir(out):
    if f.endswith(".png") or f.endswith(".json"):
        os.remove(os.path.join(out, f))

manifest = {}  # pageno(0-idx) -> [ {file, x0,y0,x1,y1, w,h} ... ] sorted by y0
for pno in range(doc.page_count):
    page = doc[pno]
    d = page.get_text("dict")
    ph = page.rect.height
    imgs = []
    for b in d["blocks"]:
        if b["type"] == 1:
            r = b["bbox"]
            xref = b["image"]
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.n - pix.alpha >= 4:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                fn = f"page_{pno}_{len(imgs)}.png"
                pix.save(os.path.join(out, fn))
                imgs.append({"file": fn, "y0": round(r[1]), "y1": round(r[3]),
                             "x0": round(r[0]), "x1": round(r[2]),
                             "top": round(100*r[1]/ph, 1),
                             "h": round(r[3]-r[1]), "w": round(r[2]-r[0])})
            except Exception as e:
                print("skip", pno, e)
    if imgs:
        imgs.sort(key=lambda x: x["y0"])
        manifest[pno] = imgs
json.dump(manifest, open(os.path.join(out, "manifest.json"), "w"), indent=1)
print(f"mapped images for {len(manifest)} pages -> {out}/manifest.json")
