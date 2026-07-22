#!/usr/bin/env python3
import os, json, sys, html
ROOT = "/Users/macbook/Documents/GitHub/abraao-estudo"
pages = list(range(100, 114))
PW = 792.0
page_css = []
page_html = []
for pno in pages:
    ld = json.load(open(os.path.join(ROOT, "abraao", "layout", f"p{pno}", "layout.json")))
    ph = ld["page_h"]
    page_css.append(f"  .pg{pno}{{position:relative;width:{PW}px;height:{ph}px;background:#fff;margin:0 auto 8px;box-shadow:0 0 0 1px #e3e3e3;overflow:hidden;}}")
    inner = []
    draw_file = os.path.join(ROOT, "abraao", "layout", f"p{pno}", "draw.json")
    if os.path.exists(draw_file):
        for dr in json.load(open(draw_file)):
            col = dr["fill"]; cr = ",".join(str(int(c * 255)) for c in col)
            x, y, w, h = dr["x"], dr["y"], dr["w"], dr["h"]
            if col == [1.0, 1.0, 1.0] and w > 500:
                continue
            hh = max(h, 1.5) if h <= 3 else h
            inner.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{hh}px;background:rgb({cr});z-index:0;"></div>')
    for t in ld["text"]:
        bold = "font-weight:700;" if (t.get("flags", 0) & 16) else ""
        size = max(t["size"], 8)
        centered = "text-align:center;" if t["x"] > PW * 0.25 and (t["x"] + t["w"]) < PW * 0.95 and t["x"] < PW / 2 else ""
        style = f'position:absolute;left:{t["x"]}px;top:{t["y"]}px;width:{t["w"]}px;font-size:{size}px;line-height:1.25;{bold}{centered}'
        inner.append(f'<div style="{style}">{html.escape(t["text"])}</div>')
    page_html.append(f'  <div class="pg{pno}">\n' + "\n".join(inner) + "\n  </div>")
CSS = "\n".join(page_css)
HTML = f'''<!doctype html>
<html lang="pt">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Sessão 15: A Aliança da Circuncisão (Faithful)</title>
<style>
*{{box-sizing:border-box;}}
body{{margin:0;background:#e9e9e9;font-family:"Helvetica Neue",Arial,sans-serif;color:#1B1B1B;}}
.wrap{{max-width:820px;margin:0 auto;background:#e9e9e9;padding:16px 0;}}
{CSS}
</style>
</head>
<body>
<div class="wrap">
{chr(10).join(page_html)}
</div>
</body>
</html>'''
outdir = os.path.join(ROOT, "abraao", "modulo-3")
os.makedirs(outdir, exist_ok=True)
open(os.path.join(outdir, "sessao-15-faithful.html"), "w").write(HTML)
print("wrote sessao-15-faithful.html pages", pages)
