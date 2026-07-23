#!/usr/bin/env python3
"""
diff_pdf_html.py  --  FAST, DETERMINISTIC PDF<->HTML visual diff (no vision).

Why: comparing a literary-design HTML section to its source PDF page by
screenshot+vision is slow and unreliable (vision hallucinates, pixel scans
catch text strokes). This tool instead extracts the SAME measurable facts from
both sides and diffs them numerically:

  For every "box" (PDF drawn rectangle / HTML bordered container):
    - border thickness (px)        -> PDF stroke width vs HTML borderTopWidth
    - border color (rgb)           -> PDF stroke color  vs HTML borderTopColor
    - text boldness                -> PDF span flags(16) vs HTML letter/body fontWeight
    - line-break (1 line vs wrap)  -> PDF line count     vs HTML wrap detection

Usage:
  python3 others/diff_pdf_html.py <html_rel_path> <pdf_page0> [pdf_page1] [--sel "<css>"]

  html_rel_path : path relative to repo root, e.g. abraao/modulo-3/sessao-15.html
  pdf_page0     : 0-indexed PDF page (page_103.png -> 103)
  pdf_page1     : optional last page (inclusive); default = pdf_page0
  --sel         : optional CSS selector for which HTML boxes to check
                  (default: .macro-box,.sp-red,.sp-grey,.sp-light,.sp-dark,
                   .ref-pill,.ref-grey,.ref-red,.ref-dark)

Matching: PDF boxes are matched to HTML boxes by their label text (the first
text span / first words inside the container). A mismatch in count is reported.

Output: one compact table per matched box (PASS/FAIL per dimension) + a summary
line. Exit code 0 if all matched boxes pass, 1 otherwise.

NOTE: this is a DEV/VERIFY tool, not the forbidden project test suite. Run it
ad-hoc; it makes no claims about `npm run test`.
"""
import os, re, sys, json, subprocess, tempfile
from pathlib import Path

ROOT = Path("/Users/macbook/Documents/GitHub/abraao-estudo")
PW = "/Users/macbook/.hermes/hermes-agent/apps/desktop/node_modules/playwright"

# ---------- PDF extraction ----------
def _pdf_bold(span, fonts):
    """Bold if flags bit4 set OR font name contains 'Bold'/'Black'."""
    if span.get("flags", 0) & 16:
        return True
    fid = span.get("font")
    fn = fonts.get(fid, "")
    return any(k in fn for k in ("Bold", "Black", "Heavy"))

def pdf_boxes(pdf_path, p0, p1):
    import fitz
    doc = fitz.open(pdf_path)
    out = []
    for pi in range(p0, p1 + 1):
        page = doc[pi]
        fonts = {f[0]: f[4] for f in page.get_fonts(full=True)}
        # drawn rectangles with a stroke (the box borders)
        draws = page.get_drawings()
        rects = []
        for d in draws:
            r = d.get("rect")
            col = d.get("color")
            w = d.get("width")
            if r and col and w:
                rects.append({"x": r[0], "y": r[1], "w": r[2] - r[0], "h": r[3] - r[1],
                              "sw": round(w, 2), "col": tuple(int(255 * c) for c in col)})
        # text spans with geometry + bold (flags OR font name)
        spans = []
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    if s["text"].strip():
                        spans.append({"x": s["bbox"][0], "y": s["bbox"][1],
                                      "text": s["text"].strip(),
                                      "bold": _pdf_bold(s, fonts),
                                      "size": round(s["size"], 1)})
        # assign each text span to the rect that contains it
        for r in rects:
            inside = [s for s in spans if r["x"] - 1 <= s["x"] and s["x"] <= r["x"] + r["w"] + 1
                      and r["y"] - 1 <= s["y"] and s["y"] <= r["y"] + r["h"] + 1]
            label = " ".join(s["text"] for s in inside[:3]).strip()
            # BODY lines only: exclude the topmost label line (contains the ref,
            # e.g. "Genesis 17:1-16") so we measure the sentence, not label+body.
            if inside:
                top_y = min(s["y"] for s in inside)
                body = [s for s in inside if s["y"] > top_y + 2]
            else:
                body = []
            body_ys = sorted({round(s["y"] / 3) for s in body})
            body_lines = max(1, len(body_ys)) if body else 1
            bold_n = sum(1 for s in inside if s["bold"])
            out.append({"label": label[:40], "page": pi,
                        "sw": r["sw"], "col": r["col"],
                        "body_lines": body_lines, "bold_spans": bold_n,
                        "total_spans": len(inside), "y": round(r["y"])})
        doc.close()
    # sort by page then y
    out.sort(key=lambda b: (b["page"], b["y"]))
    return out

# ---------- HTML extraction (Playwright) ----------
def html_boxes(html_path, sel):
    import http.server, threading, functools
    # serve repo root so relative assets (../js, images) resolve
    os.chdir(ROOT)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler)
    srv = http.server.HTTPServer(("127.0.0.1", 0), handler)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    try:
        import nodejs_playwright as _np  # placeholder; real import below
    except Exception:
        pass
    # write a tiny cjs runner (matches the known-working debug pattern)
    runner = tempfile.NamedTemporaryFile("w", suffix=".cjs", delete=False)
    runner.write(
        "const { chromium } = require(" + repr(PW) + ");\n"
        "(async () => {\n"
        "  const b = await chromium.launch({args:['--no-sandbox']});\n"
        "  const pg = await b.newPage({viewport:{width:720,height:2400},deviceScaleFactor:1});\n"
        "  await pg.goto('http://127.0.0.1:" + str(port) + "/" + html_path + "');\n"
        "  await pg.waitForTimeout(500);\n"
        "  const data = await pg.evaluate(async ({sel}) => {\n"
        "    const els = [...document.querySelectorAll(sel)];\n"
        "    const res=[];\n"
        "    for (const el of els){\n"
        "      const cs=getComputedStyle(el); const r=el.getBoundingClientRect();\n"
        "      // wrap detection: count BODY visual lines only. The first child is\n"
        "      // the badge/pill (its own line) — hide it so we measure the body\n"
        "      // sentence, not badge+body (which would always be 2 lines).\n"
        "      const badge=el.firstElementChild;\n"
        "      const bDisp = badge? badge.style.display : null;\n"
        "      if(badge) badge.style.display='none';\n"
        "      const rg=document.createRange(); rg.selectNodeContents(el);\n"
        "      const rects=rg.getClientRects();\n"
        "      // cluster tops within 4px (subpixel rounding splits one line)\n"
        "      const ts=[...rects].map(r=>Math.round(r.top/4)*4).sort((a,b)=>a-b);\n"
        "      const lines=ts.filter((v,i)=>i===0||v-ts[i-1]>4).length;\n"
        "      if(badge) badge.style.display=bDisp||'';\n"
        "      const wraps = lines > 1;\n"
        "      const strong=el.querySelector('strong,b');\n"
        "      const letterW=strong?getComputedStyle(strong).fontWeight:cs.fontWeight;\n"
        "      res.push({label:(el.innerText||'').replace(/\\s+/g,' ').trim().slice(0,40),borderW:cs.borderTopWidth,borderCol:cs.borderTopColor,fontWeight:cs.fontWeight,letterW,wraps,y:Math.round(r.top),w:Math.round(r.width)});\n"
        "    }\n"
        "    return res;\n"
        "  }, {sel:" + repr(sel) + "});\n"
        "  console.log(JSON.stringify(data));\n"
        "  await b.close();\n"
        "})().catch(e=>{console.error('ERR',e);process.exit(1)});\n"
    )
    runner.close()
    out = subprocess.run(["node", runner.name], capture_output=True, text=True)
    srv.shutdown()
    os.unlink(runner.name)
    if out.returncode != 0:
        print("PLAYWRIGHT ERROR:", out.stderr[:500], file=sys.stderr)
        return []
    return json.loads(out.stdout.strip())

# ---------- helpers ----------
def col_close(a, b, tol=40):
    # b may be a CSS "rgb(r, g, b)" string
    if isinstance(b, str):
        m = re.findall(r"\d+", b)
        if len(m) >= 3:
            b = (int(m[0]), int(m[1]), int(m[2]))
    return sum(abs(x - y) for x, y in zip(a, b)) <= tol

def match_boxes(pdf, html):
    """Match by label substring (case-insensitive)."""
    used = set()
    pairs = []
    for h in html:
        hl = h["label"].lower()
        best, bestk = None, -1
        for i, p in enumerate(pdf):
            if i in used:
                continue
            pl = p["label"].lower()
            score = 0
            for tok in re.findall(r"[A-Za-z0-9:]+", pl):
                if tok in hl:
                    score += 1
            if score > bestk:
                best, bestk = i, score
        if best is not None and bestk >= 1:
            used.add(best)
            pairs.append((pdf[best], h))
    return pairs

def diff_pair(p, h):
    """Return list of (dimension, status, detail)."""
    res = []
    # border thickness (PDF stroke points -> px at 96dpi = pt*96/72; HTML is px)
    pdf_px = round(p["sw"] * 96 / 72, 1)
    html_px = float(re.search(r"[\d.]+", h["borderW"]).group())
    # tolerance 0.6px (a 1px render difference IS a real "border boldness" defect)
    ok_bw = abs(pdf_px - html_px) <= 0.6
    res.append(("border_px", ok_bw, f"pdf={pdf_px}px html={html_px}px"))
    # border color
    ok_col = col_close(p["col"], h["borderCol"])
    res.append(("border_rgb", ok_col, f"pdf={p['col']} html={h['borderCol']}"))
    # boldness: the SOURCE is ambiguous (teacher-notes PDF = regular weight;
    # the pasted classroom slide + user instruction = bold letters). The user
    # explicitly wants the letters bold, so we verify the HTML LETTER IS BOLD
    # (catches a regression where <strong> was dropped). The PDF side is shown
    # for transparency but does NOT fail the check when it is regular.
    html_letter_bold = h["letterW"] in ("700", "bold")
    ok_bold = html_letter_bold
    res.append(("bold_letter", ok_bold, f"html_letterW={h['letterW']} (pdf_bold_spans={p['bold_spans']}/{p['total_spans']}; source page is regular weight)"))
    # line-break: PDF BODY lines vs HTML body wraps
    pdf_lines = p["body_lines"]
    ok_line = (pdf_lines <= 1) == (not h["wraps"])
    res.append(("one_line", ok_line, f"pdf_body_lines={pdf_lines} html_wraps={h['wraps']}"))
    return res

def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__); sys.exit(2)
    html_rel = args[0]
    p0 = int(args[1])
    p1 = int(args[2]) if len(args) > 2 and args[2].lstrip("-") not in ("sel",) else p0
    sel = ".macro-box,.sp-red,.sp-grey,.sp-light,.sp-plain,.ref-pill,.ref-grey,.ref-red,.ref-dark,.ref-green,.hl,.hl-green,.hl-red,.hl-blue,.hl-divine,.hl-mult"
    if "--sel" in args:
        sel = args[args.index("--sel") + 1]
    pdf_path = ROOT / "abraao" / "abraham-teacher-notes.pdf"
    print(f"# DIFF  html={html_rel}  pdf_pages={p0}-{p1}  sel={sel}")
    pdf = pdf_boxes(str(pdf_path), p0, max(p0, p1))
    html = html_boxes(html_rel, sel)
    if not html:
        print("NO HTML BOXES EXTRACTED (playwright failed?)"); sys.exit(1)
    pairs = match_boxes(pdf, html)
    print(f"# pdf boxes={len(pdf)}  html boxes={len(html)}  matched={len(pairs)}")
    allok = True
    for p, h in pairs:
        print(f"\n## '{h['label'][:34]}'")
        for dim, st, det in diff_pair(p, h):
            allok &= st
            print(f"   [{'PASS' if st else 'FAIL'}] {dim:12} {det}")
    un = len(html) - len(pairs)
    if un:
        print(f"\n# WARNING: {un} HTML box(es) unmatched to a PDF box")
        allok = False
    print("\n=== SUMMARY:", "ALL PASS" if allok else "MISMATCH FOUND", "===")
    sys.exit(0 if allok else 1)

if __name__ == "__main__":
    main()
