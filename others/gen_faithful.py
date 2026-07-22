#!/usr/bin/env python3
"""Generate a pixel-faithful HTML recreation of a session from the extracted
per-page layout (text lines + images at true PDF positions). Absolute positioning
is used so the HTML matches the PDF page. One HTML file per session.
Usage: python3 others/gen_faithful.py <course> <session>
Reads pages from others/session_pages.json, layout from <course>/layout/p<page>/.
"""
import os, json, sys, html

ROOT = "/Users/macbook/Documents/GitHub/abraao-estudo"
course = sys.argv[1]
sess = int(sys.argv[2])
sp = json.load(open(os.path.join(ROOT, "others", "session_pages.json")))
entry = next(e for e in sp[course] if e["session"] == sess)
p0, p1 = entry["page_start"], entry["page_end"]
pages = list(range(p0, p1 + 1))

# session title + EN/PT text (already extracted)
prefix = {"heaven-and-earth": "he"}.get(course, course.split("-")[0])
en_path = f"/tmp/{prefix}_session_{sess}.txt"
pt_path = f"/tmp/{prefix}_session_{sess}_pt.txt"
en_text = open(en_path).read() if os.path.exists(en_path) else ""
pt_text = open(pt_path).read() if os.path.exists(pt_path) else ""

# determine module number from modules_en.json
mod_num = None
mods = json.load(open(os.path.join(ROOT, "others", "modules_en.json")))[course]
for md in mods:
    if md["first"] <= sess <= md["last"]:
        mod_num = md["pos"]
        break
if mod_num is None:
    mod_num = 1

PW = 792.0
page_css = []
page_html = []
for pno in pages:
    ld = json.load(open(os.path.join(ROOT, course, "layout", f"p{pno}", "layout.json")))
    ph = ld["page_h"]
    page_css.append(f"""  .pg{pno}{{position:relative;width:{PW}px;height:{ph}px;background:#fff;
    margin:0 auto 8px;box-shadow:0 0 0 1px #e3e3e3;overflow:hidden;}}""")
    inner = []
    # drawn vector shapes (header rules, bullet squares, title underline, dividers, verse boxes)
    draw_file = os.path.join(ROOT, course, "layout", f"p{pno}", "draw.json")
    if os.path.exists(draw_file):
        for dr in json.load(open(draw_file)):
            col = dr["fill"]
            cr = ",".join(str(int(c * 255)) for c in col)
            x, y, w, h = dr["x"], dr["y"], dr["w"], dr["h"]
            # Verse-quote box: dark (near-black) wide rect at left margin -> light box + black left border
            if col == [0.106, 0.106, 0.106] and w > 200 and x < 120:
                inner.append(
                    f'<div style="position:absolute;left:{x}px;top:{y}px;'
                    f'width:{w}px;height:{h}px;background:#E4EAF0;'
                    f'border-left:4px solid #1B1B1B;box-sizing:border-box;z-index:0;"></div>')
                continue
            hh = max(h, 1.5) if h <= 3 else h
            inner.append(
                f'<div style="position:absolute;left:{x}px;top:{y}px;'
                f'width:{w}px;height:{hh}px;background:rgb({cr});'
                f'z-index:0;"></div>')
    # images first (behind text)
    for im in ld["imgs"]:
        src = f"../layout/p{pno}/{im['file']}"
        inner.append(
            f'<img class="pdfimg" src="{src}" alt="" '
            f'style="position:absolute;left:{im["x"]}px;top:{im["y"]}px;'
            f'width:{im["w"]}px;height:{im["h"]}px;object-fit:cover;">')
    # text lines
    for t in ld["text"]:
        bold = "font-weight:700;" if (t.get("flags", 0) & 16) else ""
        size = t["size"]
        # detect centered (x near middle)
        centered = "text-align:center;" if t["x"] > PW * 0.25 and (t["x"] + t["w"]) < PW * 0.95 and t["x"] < PW / 2 else ""
        style = (f'position:absolute;left:{t["x"]}px;top:{t["y"]}px;'
                 f'width:{t["w"]}px;font-size:{size}px;line-height:1.25;{bold}{centered}')
        inner.append(f'<div style="{style}">{html.escape(t["text"])}</div>')
    page_html.append(f'  <div class="pg{pno}">\n' + "\n".join(inner) + "\n  </div>")

CSS = """
  *{box-sizing:border-box;}
  body{margin:0;background:#e9e9e9;font-family:'Helvetica Neue',Arial,sans-serif;color:#1B1B1B;}
  .wrap{max-width:820px;margin:0 auto;background:#e9e9e9;padding:16px 0;}
""" + "\n".join(page_css)

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Session {sess} — {course}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
{chr(10).join(page_html)}
</div>
</body>
</html>"""

outdir = os.path.join(ROOT, course, f"modulo-{mod_num}")
os.makedirs(outdir, exist_ok=True)
outf = os.path.join(outdir, f"sessao-{sess}-faithful.html")
open(outf, "w").write(HTML)
print("wrote", outf, "pages", pages)
