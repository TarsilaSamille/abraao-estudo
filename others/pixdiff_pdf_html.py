#!/usr/bin/env python3
"""
pixdiff_pdf_html.py -- Architecture-2 TEXT-MASKED PIXEL DIFF (PIL-only, no cv2/numpy).

WHY: the DOM tool (diff_pdf_html.py) only checks border/bold/line on the macro
family. But each literary design is different (verse grids, word-study
highlights, speech/ref boxes, chiasms...). A hand-coded check per design does
not scale. This tool instead rasterizes BOTH the HTML and the PDF, MASKS OUT
TEXT, and diffs the remaining structure (fills, borders, padding, overlaps,
alignment). It catches non-text divergences automatically for ANY design.

HOW (text-masked, alignment-free):
  1. HTML  -> Playwright full-page screenshot, all text set to `color:transparent`
              (keeps layout/spacing/fills/borders, hides glyphs), cropped to the
              union bbox of the matched selector(s).
  2. PDF   -> PyMuPDF render at the SAME pixel width (720). Text glyph bboxes
              are known, so we build a TEXT MASK and EXCLUDE those pixels from
              the structural score (so a translation difference is NOT counted
              as a structural defect).
  3. ALIGN -> vertical scan: slide a PDF-height window over the (taller) HTML,
              pick the offset minimizing the masked diff. No manual anchor.
  4. DIFF  -> absdiff of the aligned pair, text pixels excluded; count changed
              structural pixels; emit changed-region bounding boxes + a diff PNG.

>>> HONEST LIMITATION (do NOT use PASS/FAIL as proof of fidelity) <<<
The HTML sessions and the PDF lay out the SAME content at NON-UNIFORM scales:
the HTML is compact, the PDF page is tall with wide spacing. A uniform
`--stretch` aligns extents but smears edges and yields unreliable numbers (a
faithful page can read >15% structural change, and a REAL defect can read
LOWER than the clean page). This tool is therefore only useful for a ROUGH
visual diff PNG (`--out`) to eyeball gross breaks. For deterministic, correct
fidelity checking use `diff_pdf_html.py` (semantic) — see others/literary_designs.md.

Usage:
  python3 others/pixdiff_pdf_html.py <html_rel> <pdf_page0> [--sel "<css>"] [--out <png>] [--stretch]

  html_rel   : e.g. abraao/modulo-3/sessao-15.html
  pdf_page0  : 0-indexed PDF page (page_103.png -> 103)
  --sel      : section selector (default: "main" = whole session content)
  --out      : path for the diff visualization PNG
  --stretch  : stretch the HTML section to the PDF page size before diffing
               (aligns content extent, but introduces resampling artifacts)

Output: structural-change %, #changed regions, their bboxes, and (if --out) a PNG.
Exit 0 if structural change < threshold (default 4%), else 1.

NOTE: DEV/VERIFY tool, NOT the forbidden `npm run test` suite.
"""
import os, re, sys, json, subprocess, tempfile, argparse
from pathlib import Path

ROOT = Path("/Users/macbook/Documents/GitHub/abraao-estudo")
PW = "/Users/macbook/.hermes/hermes-agent/apps/desktop/node_modules/playwright"
PDF = ROOT / "abraao" / "abraham-teacher-notes.pdf"
WIDTH = 720  # shared render width for HTML and PDF

# ---------- HTML non-text screenshot (Playwright) ----------
def html_nont_png(html_rel, sel, out_png):
    """Full-page screenshot with all text made transparent (keeps layout /
    fills / borders / spacing), then crop in PIL to the union bounding box of
    the matched selector(s). Robust for single OR group selectors and avoids
    clip/viewport coordinate pitfalls."""
    import http.server, threading, functools
    from PIL import Image
    os.chdir(ROOT)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler)
    srv = http.server.HTTPServer(("127.0.0.1", 0), handler)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True); t.start()
    full_png = out_png + ".full.png"
    runner = tempfile.NamedTemporaryFile("w", suffix=".cjs", delete=False)
    runner.write(
        "const { chromium } = require(" + repr(PW) + ");\n"
        "(async () => {\n"
        "  const b = await chromium.launch({args:['--no-sandbox']});\n"
        "  const pg = await b.newPage({viewport:{width:" + str(WIDTH) + ",height:2600},deviceScaleFactor:1});\n"
        "  await pg.goto('http://127.0.0.1:" + str(port) + "/" + html_rel + "');\n"
        "  await pg.waitForTimeout(500);\n"
        "  const data = await pg.evaluate(async ({sel}) => {\n"
        "    const s=document.createElement('style');\n"
        "    s.textContent='*{color:transparent !important;}';\n"
        "    document.head.appendChild(s);\n"
        "    const els=[...document.querySelectorAll(sel)];\n"
        "    if(!els.length) return null;\n"
        "    let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;\n"
        "    for(const el of els){const r=el.getBoundingClientRect();\n"
        "      x0=Math.min(x0,r.left);y0=Math.min(y0,r.top);\n"
        "      x1=Math.max(x1,r.right);y1=Math.max(y1,r.bottom);}\n"
        "    return {x:Math.round(x0),y:Math.round(y0),w:Math.round(x1-x0),h:Math.round(y1-y0)};\n"
        "  }, {sel:" + repr(sel) + "});\n"
        "  if(!data){console.error('NO MATCH for'," + repr(sel) + ");process.exit(1);}\n"
        "  await pg.screenshot({path:" + repr(full_png) + ", fullPage:true});\n"
        "  const fs=require('fs'); fs.writeFileSync(" + repr(out_png + ".bbox.json") + ", JSON.stringify(data));\n"
        "  await b.close();\n"
        "})().catch(e=>{console.error('ERR',e);process.exit(1)});\n"
    )
    runner.close()
    out = subprocess.run(["node", runner.name], capture_output=True, text=True)
    srv.shutdown(); os.unlink(runner.name)
    if out.returncode != 0:
        print("PLAYWRIGHT ERROR:", out.stderr[:400], file=sys.stderr); return False
    # crop full-page png to union bbox
    try:
        bbox = json.loads(open(out_png + ".bbox.json").read())
    except Exception:
        print("BBOX read failed"); return False
    os.unlink(out_png + ".bbox.json")
    full = Image.open(full_png).convert("RGB")
    # fullPage screenshot width should equal WIDTH (viewport width)
    crop = full.crop((bbox["x"], bbox["y"], bbox["x"] + bbox["w"], bbox["y"] + bbox["h"]))
    crop.save(out_png)
    os.unlink(full_png)
    return True

# ---------- PDF render + text mask (fitz) ----------
def pdf_render_and_mask(page0, width=WIDTH):
    import fitz
    from PIL import Image, ImageDraw
    doc = fitz.open(str(PDF))
    page = doc[page0]
    scale = width / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    # text mask (L, 255 = text glyph area, dilated slightly)
    mask = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(mask)
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if not s["text"].strip():
                    continue
                x0, y0, x1, y1 = s["bbox"]
                # shrink height to glyph band so highlight fills survive
                h = y1 - y0
                gy0 = y0 + h * 0.18
                gy1 = y1 - h * 0.12
                d.rectangle([x0 * scale - 1, gy0 * scale - 1, x1 * scale + 1, gy1 * scale + 1],
                            fill=255)
    doc.close()
    return img, mask

# ---------- diff engine (PIL only) ----------
def scan_align(html_img, pdf_img, inv_mask, scan_w=240):
    """Slide a PDF-height window over the (taller) HTML to locate the matching
    section. Returns best HTML offset (full-res)."""
    from PIL import Image, ImageChops, ImageStat
    pw, ph = pdf_img.size
    hw, hh = html_img.size
    # if html shorter than one pdf page, pad html with white
    if hh < ph:
        html_img = _white_pad(html_img, ph)
        hh = html_img.size[1]
    def ds(im):
        return im.resize((scan_w, max(1, int(im.size[1] * scan_w / im.size[0]))))
    H = ds(html_img)
    P = ds(pdf_img)
    M = ds(inv_mask)  # same height as P (derived from pdf)
    ph2 = P.size[1]
    hh2 = H.size[1]
    win = ph2  # window = one pdf page height
    best_off, best_score = 0, float("inf")
    step = max(1, win // 200)
    for off in range(0, max(1, hh2 - win + 1), step):
        hc = H.crop((0, off, pw, off + win))
        d = ImageChops.difference(hc.convert("L"), P.convert("L"))
        md = ImageChops.multiply(d, M.convert("L"))
        score = sum(ImageStat.Stat(md).sum)
        if score < best_score:
            best_score, best_off = score, off
    # refine at full res
    full_off = int(best_off * hh / hh2)
    best_off_f, best_score_f = full_off, float("inf")
    for off in range(max(0, full_off - 12), min(hh - ph + 1, full_off + 13)):
        hc = html_img.crop((0, off, pw, off + ph))
        d = ImageChops.difference(hc.convert("L"), pdf_img.convert("L"))
        md = ImageChops.multiply(d, inv_mask.convert("L"))
        score = sum(ImageStat.Stat(md).sum)
        if score < best_score_f:
            best_score_f, best_off_f = score, off
    return best_off_f

def _white_pad(im, target_h):
    from PIL import Image
    if im.size[1] >= target_h:
        return im
    new = Image.new(im.mode, (im.size[0], target_h), (255,) * len(im.mode))
    new.paste(im, (0, 0))
    return new

def _white_pad_mask(im, target_h):
    from PIL import Image
    if im.size[1] >= target_h:
        return im
    # mask: 255=ignore(text). padding = no text = keep(0). build black.
    new = Image.new("L", (im.size[0], target_h), 0)
    new.paste(im, (0, 0))
    return new

def structural_diff(html_img, pdf_img, inv_mask, offset, out_png=None, thr=26):
    from PIL import Image, ImageChops, ImageStat
    pw, ph = pdf_img.size
    # crop the HTML at the located offset to one pdf-page window
    hc = html_img.crop((0, offset, pw, offset + ph))
    mc = inv_mask.crop((0, 0, pw, ph)).convert("L")
    d = ImageChops.difference(hc.convert("L"), pdf_img.convert("L"))  # L
    md = ImageChops.multiply(d, mc)  # mask out text
    # changed structural pixels
    bw = md.point(lambda p: 255 if p > thr else 0)
    changed = sum(ImageStat.Stat(bw).sum) // 255  # pixel count
    total = bw.size[0] * bw.size[1]
    pct = 100.0 * changed / total
    # connected regions via BFS
    boxes = []
    if changed > 0:
        px = bw.load()
        w, h = bw.size
        visited = [[False] * w for _ in range(h)]
        from collections import deque
        for y0 in range(h):
            for x0 in range(w):
                if px[x0, y0] and not visited[y0][x0]:
                    q = deque([(x0, y0)])
                    visited[y0][x0] = True
                    minx = maxx = x0; miny = maxy = y0
                    while q:
                        x, y = q.popleft()
                        minx = min(minx, x); maxx = max(maxx, x)
                        miny = min(miny, y); maxy = max(maxy, y)
                        for dx in (-1, 0, 1):
                            for dy in (-1, 0, 1):
                                nx, ny = x + dx, y + dy
                                if 0 <= nx < w and 0 <= ny < h and px[nx, ny] and not visited[ny][nx]:
                                    visited[ny][nx] = True
                                    q.append((nx, ny))
                    if (maxx - minx) >= 3 or (maxy - miny) >= 3:
                        boxes.append((minx, miny, maxx + 1, maxy + 1))
        boxes.sort(key=lambda b: (b[1], b[0]))
    if out_png:
        red = Image.new("RGB", pdf_img.size, (200, 30, 30))
        overlay = Image.composite(red, pdf_img, bw)
        overlay.save(out_png)
    # metric: largest changed region area (a real defect = concentrated big box;
    # baseline anti-alias noise = many tiny specks). Also count "big" regions.
    big = [b for b in boxes if (b[2] - b[0]) * (b[3] - b[1]) >= 400]
    max_area = max(((b[2] - b[0]) * (b[3] - b[1]) for b in boxes), default=0)
    return pct, boxes, len(big), max_area

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html_rel")
    ap.add_argument("pdf_page0", type=int)
    ap.add_argument("--sel", default="main")
    ap.add_argument("--out", default="")
    ap.add_argument("--thr", type=int, default=26)
    ap.add_argument("--maxpct", type=float, default=4.0)
    ap.add_argument("--stretch", action="store_true",
                    help="stretch the HTML section crop to the PDF page size before "
                         "diffing (aligns content extent; HTML/PDF differ in scale)")
    a = ap.parse_args()

    html_png = tempfile.mktemp(suffix=".png")
    if not html_nont_png(a.html_rel, a.sel, html_png):
        print("HTML screenshot failed"); sys.exit(1)
    from PIL import Image
    html_img = Image.open(html_png).convert("RGB")
    if html_img.size[0] != WIDTH:
        html_img = html_img.resize((WIDTH, int(html_img.size[1] * WIDTH / html_img.size[0])))
    pdf_img, textmask = pdf_render_and_mask(a.pdf_page0, WIDTH)
    inv_mask = Image.eval(textmask, lambda p: 255 - p)  # 255 = keep (non-text)
    # Architecture-2 alignment: HTML and PDF lay out the same content at very
    # different scales. Stretch the (smaller) HTML section to the PDF page so
    # content extent matches before diffing. inv_mask must be stretched too.
    if a.stretch and html_img.size != pdf_img.size:
        html_img = html_img.resize(pdf_img.size)
        inv_mask = inv_mask.resize(pdf_img.size)

    offset = scan_align(html_img, pdf_img, inv_mask)
    pct, boxes, n_big, max_area = structural_diff(html_img, pdf_img, inv_mask, offset,
                                 out_png=a.out or None, thr=a.thr)
    print(f"# PIXDIFF  html={a.html_rel}  pdf_page={a.pdf_page0}  sel={a.sel}")
    print(f"# html={html_img.size}  pdf={pdf_img.size}  align_offset={offset}px")
    print(f"# STRUCTURAL change = {pct:.2f}%  (threshold {a.maxpct}%)")
    print(f"# changed regions = {len(boxes)}  | big regions(>=400px) = {n_big}  | largest region = {max_area}px")
    print(f"# changed regions (first 20):")
    for (x0, y0, x1, y1) in boxes[:20]:
        print(f"    x[{x0}-{x1}] y[{y0}-{y1}]  w={x1-x0} h={y1-y0}")
    if a.out:
        print(f"# diff PNG -> {a.out}")
    # divergence if EITHER global % high OR a concentrated big region appears
    ok = (pct <= a.maxpct) and (n_big == 0)
    print("=== SUMMARY:", "STRUCTURAL MATCH" if ok else "STRUCTURAL DIVERGENCE", "===")
    os.unlink(html_png)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
