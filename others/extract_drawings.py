#!/usr/bin/env python3
"""Extract all drawn vector shapes (fills) per page -> <course>/layout/p<page>/draw.json.
Skips the full-page white background. Used to faithfully recreate header bars,
title underlines, bullet squares, rule lines, etc."""
import fitz, os, json, sys

ROOT = "/Users/macbook/Documents/GitHub/abraao-estudo"
course = sys.argv[1]
p0 = int(sys.argv[2]); p1 = int(sys.argv[3])
doc = fitz.open(os.path.join(ROOT, course, f"{course}-teacher-notes.pdf"))
PW = 792.0

def rgb(c):
    if not c:
        return None
    try:
        return (round(c[0], 3), round(c[1], 3), round(c[2], 3))
    except Exception:
        return None

for pno in range(p0, p1 + 1):
    page = doc[pno]; scale = PW / page.rect.width
    out = []
    for dr in page.get_drawings():
        r = dr["rect"]
        fill = rgb(dr.get("fill"))
        if fill is None:
            continue
        # skip near-white large background fills
        if fill == (1.0, 1.0, 1.0):
            continue
        x = round(r.x0 * scale, 1); y = round(r.y0 * scale, 1)
        w = round(r.width * scale, 1); h = round(r.height * scale, 1)
        out.append({"x": x, "y": y, "w": w, "h": h, "fill": fill})
    json.dump(out, open(os.path.join(ROOT, course, "layout", f"p{pno}", "draw.json"), "w"))
    print(f"p{pno}: {len(out)} shapes")
