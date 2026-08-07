#!/usr/bin/env python3.14
"""Render PDF session pages + HTML to images and compose side-by-side for 1:1 style check."""
import os, sys, subprocess, shutil, argparse
import fitz
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERIFY = os.path.join(ROOT, "verify")
os.makedirs(VERIFY, exist_ok=True)
PY = "/usr/local/opt/python@3.14/bin/python3.14"
NODE = "/usr/local/bin/node"
PW = os.path.expanduser("~/GitHub/biblia-estudo/node_modules/playwright")

def render_pdf(session):
    pdf = os.path.join(ROOT, "pdf-sessoes", f"sessao-{session}.pdf")
    out = []
    d = fitz.open(pdf)
    for i, p in enumerate(d):
        pix = p.get_pixmap(dpi=110)
        fn = os.path.join(VERIFY, f"pdf-s{session}-p{i+1}.png")
        pix.save(fn)
        out.append(fn)
    # combine all pdf pages into one tall strip
    imgs = [Image.open(fn).convert("RGB") for fn in out]
    w = max(im.width for im in imgs)
    strip = Image.new("RGB", (w, sum(im.height for im in imgs)))
    y = 0
    for im in imgs:
        strip.paste(im, (0, y)); y += im.height
    sp = os.path.join(VERIFY, f"pdf-s{session}-strip.png")
    strip.save(sp)
    return sp

def render_html(session, module):
    html_path = os.path.join(ROOT, module, f"sessao-{session}.html")
    url = "file://" + html_path
    js = f"""
    const {{ chromium }} = require({PW!r});
    (async () => {{
      const browser = await chromium.launch({{
        executablePath: '/Users/macbook/Library/Caches/ms-playwright/chromium-1228/chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',
        args: ['--no-sandbox']
      }});
      const page = await browser.newPage({{ viewport: {{ width: 935, height: 1200 }} }});
      await page.goto({url!r}, {{ waitUntil: 'networkidle' }});
      await page.evaluate(() => {{ document.documentElement.lang='pt'; document.querySelectorAll('.reveal').forEach(e=>e.classList.add('visible')); }});
      await page.waitForTimeout(400);
      await page.pdf({{ path: {os.path.join(VERIFY, f'html-s{session}.pdf')!r}, printBackground: true, format: 'A4', preferCSSPageSize: false }});
      await browser.close();
    }})();
    """
    script = os.path.join(VERIFY, f"render-{session}.js")
    with open(script, "w") as f:
        f.write(js)
    subprocess.run([NODE, script], check=True)
    # convert html pdf to strip
    d = fitz.open(os.path.join(VERIFY, f"html-s{session}.pdf"))
    imgs = []
    for i, p in enumerate(d):
        pix = p.get_pixmap(dpi=110)
        fn = os.path.join(VERIFY, f"html-s{session}-p{i+1}.png")
        pix.save(fn); imgs.append(fn)
    pimgs = [Image.open(fn).convert("RGB") for fn in imgs]
    w = max(im.width for im in pimgs)
    strip = Image.new("RGB", (w, sum(im.height for im in pimgs)))
    y = 0
    for im in pimgs:
        strip.paste(im, (0, y)); y += im.height
    sp = os.path.join(VERIFY, f"html-s{session}-strip.png")
    strip.save(sp)
    return sp

def compose(sess, pdf_strip, html_strip, maxw=860):
    a = Image.open(pdf_strip).convert("RGB")
    b = Image.open(html_strip).convert("RGB")
    # scale to same width
    for im in (a, b):
        if im.width > maxw:
            r = maxw / im.width
            im.thumbnail((maxw, int(im.height * r)))
    bar = Image.new("RGB", (maxw, 40), (230,230,230))
    gap = 24
    total_w = maxw * 2 + gap
    # align heights: stack side by side, pad shorter
    h = max(a.height, b.height)
    canvas = Image.new("RGB", (total_w, h + 60), (255,255,255))
    canvas.paste(a, (0, 60))
    canvas.paste(b, (maxw + gap, 60))
    # labels
    lab = Image.new("RGB", (total_w, 60), (250,250,250))
    lab.paste(Image.open(pdf_strip).convert("RGB").crop((0,0,2,2)), (0,0))  # placeholder
    canvas.paste(lab, (0,0))
    out = os.path.join(VERIFY, f"compare-s{sess}.png")
    canvas.save(out)
    # also make smaller jpg for vision
    sm = canvas.copy()
    sm.thumbnail((1100, 1400))
    sm.save(os.path.join(VERIFY, f"compare-s{sess}-sm.jpg"), quality=82)
    return out

if __name__ == "__main__":
    session = int(sys.argv[1])
    module = sys.argv[2] if len(sys.argv) > 2 else "modulo-1"
    ps = render_pdf(session)
    hs = render_html(session, module)
    out = compose(session, ps, hs)
    print("WROTE", out)
