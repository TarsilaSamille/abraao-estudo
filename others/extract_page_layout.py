#!/usr/bin/env python3
"""For a course + page range, extract per-page structured layout (text lines + images
placed at their true PDF positions), writing JSON + extracted images into
<course>/layout/p<page>/. Uses stable doc.extract_image API.
Usage: python3 others/extract_page_layout.py <course> <p0> <p1>
"""
import fitz, os, json, sys

ROOT = "/Users/macbook/Documents/GitHub/abraao-estudo"
course = sys.argv[1]
p0 = int(sys.argv[2])
p1 = int(sys.argv[3])
pdf = os.path.join(ROOT, course, f"{course}-teacher-notes.pdf")
doc = fitz.open(pdf)
base = os.path.join(ROOT, course, "layout")
os.makedirs(base, exist_ok=True)

PW = 792.0  # target CSS page width (matches PDF pt width)

for pno in range(p0, p1 + 1):
    page = doc[pno]
    ph = page.rect.height
    pw = page.rect.width
    scale = PW / pw
    d = page.get_text("dict")
    pdir = os.path.join(base, f"p{pno}")
    os.makedirs(pdir, exist_ok=True)
    text_blocks = []
    imgs = []
    for b in d["blocks"]:
        if b["type"] == 0:
            for line in b["lines"]:
                sp = line["spans"][0]
                txt = "".join(s["text"] for s in line["spans"]).strip()
                if not txt:
                    continue
                r = line["bbox"]
                text_blocks.append({
                    "x": round(r[0] * scale, 1),
                    "y": round(r[1] * scale, 1),
                    "w": round((r[2] - r[0]) * scale, 1),
                    "size": round(sp["size"] * scale, 1),
                    "flags": sp["flags"],
                    "text": txt,
                })
    # images via page.get_images + get_image_rects (dict blocks miss some)
    for img in page.get_images(full=True):
        xref = img[0]
        try:
            rects = page.get_image_rects(xref)
            if not rects:
                continue
            rect = rects[0]
            imginfo = doc.extract_image(xref)
            ext = imginfo["ext"]
            fn = f"img{len(imgs)}.{ext}"
            with open(os.path.join(pdir, fn), "wb") as f:
                f.write(imginfo["image"])
            imgs.append({
                "file": fn,
                "x": round(rect.x0 * scale, 1),
                "y": round(rect.y0 * scale, 1),
                "w": round(rect.width * scale, 1),
                "h": round(rect.height * scale, 1),
            })
        except Exception as e:
            sys.stderr.write(f"img skip p{pno}: {e}\n")
    json.dump({"page_h": round(ph * scale, 1), "text": text_blocks, "imgs": imgs},
              open(os.path.join(pdir, "layout.json"), "w"), ensure_ascii=False, indent=1)
    print(f"p{pno}: {len(text_blocks)} text lines, {len(imgs)} images, page_h={round(ph*scale,1)}")
