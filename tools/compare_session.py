#!/usr/bin/env python3
"""
compare_session.py — compare a session page against its teacher-notes PDF.

The token audit only answers "does the HTML use documented tokens?". It cannot
answer "does it look like the PDF?". This does: it extracts the colours the PDF
actually paints with, the colours the HTML actually renders, and reports the
difference. It also renders page images so the pair can be inspected visually.

Usage:
    python3 tools/compare_session.py 4              # session number (braaa)
    python3 tools/compare_session.py --all           # all 30
    python3 tools/compare_session.py 4 --render      # also write PNGs
"""
import argparse
import collections
import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSE = os.path.join(ROOT, "abraao")


SHOT_JS = r'''
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [htmlArg, outDir] = process.argv.slice(2);
  const b = await chromium.launch({ channel: 'chrome' });
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  await p.goto('file://' + path.resolve(htmlArg), { waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(2500);
  // fatias de viewport: a pagina inteira pode ter >13000px e um PNG unico
  // ficaria ilegivel para comparar com a pagina do PDF.
  const h = await p.evaluate(() => document.documentElement.scrollHeight);
  const STEP = 1100, OVERLAP = 60;
  let i = 1, y = 0;
  while (y < h) {
    await p.evaluate(v => window.scrollTo(0, v), y);
    await p.waitForTimeout(350);
    const n = String(i++).padStart(2, '0');
    await p.screenshot({ path: path.join(outDir, `html-${n}.png`) });
    y += STEP - OVERLAP;
  }
  await b.close().catch(() => {});
  process.exit(0);
})();
'''


def hexof(rgb):
    if rgb is None:
        return None
    return "#%02x%02x%02x" % tuple(int(round(c * 255)) for c in rgb)


def pdf_colors(pdf_path):
    """Colours the PDF paints with, by area: vector fills, strokes, text."""
    import fitz
    doc = fitz.open(pdf_path)
    fills, strokes, texts = collections.Counter(), collections.Counter(), collections.Counter()
    for page in doc:
        for d in page.get_drawings():
            if d.get("fill"):
                fills[hexof(d["fill"])] += 1
            if d.get("color"):
                strokes[hexof(d["color"])] += 1
        for blk in page.get_text("dict")["blocks"]:
            for line in blk.get("lines", []):
                for span in line.get("spans", []):
                    c = span.get("color")
                    if c is not None:
                        texts["#%06x" % (c & 0xFFFFFF)] += 1
    doc.close()
    return fills, strokes, texts


def html_colors(html_path, tmp_js):
    """Colours the browser actually paints, via Playwright.

    cwd must be the repo root and tmp_js must be absolute, or node cannot
    resolve `playwright` from node_modules.
    """
    script = os.path.abspath(tmp_js)
    out = subprocess.run(["node", script, os.path.abspath(html_path)],
                         capture_output=True, text=True, cwd=ROOT)
    if out.returncode != 0:
        return None, (out.stderr.strip().splitlines() or ["?"])[:4]
    try:
        return json.loads(out.stdout), None
    except json.JSONDecodeError as e:
        return None, [f"JSON invalido: {e}", out.stdout[:200]]


COLLECT_JS = r'''
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ channel: 'chrome' });
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  const errs = [];
  p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + process.argv[2], { waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(2500);
  const r = await p.evaluate(() => {
    // getComputedStyle returns rgb()/rgba(), never hex. Convert, or nothing
    // is ever collected.
    const toHex = (v) => {
      if (!v) return null;
      const m = v.match(/rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)/);
      if (!m) return null;
      const h = n => Math.max(0, Math.min(255, Math.round(+n))).toString(16).padStart(2, '0');
      return '#' + h(m[1]) + h(m[2]) + h(m[3]);
    };
    const counts = {};
    const bump = (rgbStr, n, where) => {
      const hex = toHex(rgbStr);
      if (!hex) return;
      if (hex === '#ffffff' || hex === '#000000') return;  // canvas, not ink
      counts[hex] = counts[hex] || { n: 0, where: {} };
      counts[hex].n += n;
      counts[hex].where[where] = (counts[hex].where[where] || 0) + n;
    };
    for (const el of document.querySelectorAll('*')) {
      const cs = getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      if (rect.width < 1 || rect.height < 1) continue;
      const area = rect.width * rect.height;
      const where = el.tagName.toLowerCase() +
        (el.className && typeof el.className === 'string'
          ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
      bump(cs.color, Math.max(1, area / 4000), where + ' (texto)');
      if (cs.backgroundColor && !/rgba\(0, 0, 0, 0\)/.test(cs.backgroundColor))
        bump(cs.backgroundColor, area / 4000, where + ' (fundo)');
      for (const side of ['Top', 'Right', 'Bottom', 'Left']) {
        const w = parseFloat(cs['border' + side + 'Width']) || 0;
        if (w > 0 && cs['border' + side + 'Style'] !== 'none')
          bump(cs['border' + side + 'Color'], (w * rect.height) / 20, where + ' (borda)');
      }
    }
    return { counts,
             h: document.documentElement.scrollHeight,
             sw: document.documentElement.scrollWidth,
             cw: document.documentElement.clientWidth };
  });
  r.errors = errs;   // node scope, not the browser scope
  console.log(JSON.stringify(r));
  await b.close().catch(() => {});
  process.exit(0);
})();
'''


def session_paths(n):
    html = glob.glob(os.path.join(COURSE, "modulo-*", f"sessao-{n}.html"))
    pdf = os.path.join(COURSE, "pdf-sessoes", f"sessao-{n}.pdf")
    return (html[0] if html else None), (pdf if os.path.exists(pdf) else None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("session", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--top", type=int, default=18)
    a = ap.parse_args()

    tmp = os.path.join(ROOT, "tools", ".collect.tmp.js")
    open(tmp, "w").write(COLLECT_JS)
    try:
        nums = range(1, 31) if a.all else [int(a.session)]
        for n in nums:
            report(n, tmp, a.render, a.top)
            print()
    finally:
        os.unlink(tmp)
    return 0


def report(n, tmp, render, top):
    html, pdf = session_paths(n)
    print(f"{'=' * 78}\nSESSÃO {n}\n  HTML: {os.path.relpath(html, ROOT) if html else 'NAO ENCONTRADO'}"
          f"\n  PDF:  {os.path.relpath(pdf, ROOT) if pdf else 'NAO ENCONTRADO'}")
    if not html or not pdf:
        print("  -> sem par HTML/PDF, nada a comparar")
        return

    fills, strokes, texts = pdf_colors(pdf)
    hc, err = html_colors(html, tmp)
    if hc is None:
        print("  !! nao consegui renderizar o HTML:", err)
        return

    hcc = {k: v["n"] for k, v in hc["counts"].items()}
    pdf_all = set(fills) | set(strokes) | set(texts)
    pdf_all.discard(None)

    print(f"  PDF: {len(fills)} preenchimentos, {len(strokes)} traços, {len(texts)} cores de texto")
    print(f"  HTML: {len(hcc)} cores pintadas")

    print(f"\n  --- CORES DO PDF AUSENTES NO HTML (top {top}) ---")
    missing = sorted(pdf_all - set(hcc))
    if not missing:
        print("      nenhuma")
    for c in missing[:top]:
        where = []
        if c in fills: where.append(f"preenchimento x{fills[c]}")
        if c in strokes: where.append(f"traço x{strokes[c]}")
        if c in texts: where.append(f"texto x{texts[c]}")
        print(f"      {c}  ({', '.join(where)})")

    print(f"\n  --- CORES DO HTML AUSENTES NO PDF (top {top}) ---")
    extra = sorted(set(hcc) - pdf_all)
    if not extra:
        print("      nenhuma")
    for c in sorted(extra, key=lambda x: -hcc[x])[:top]:
        ex = ", ".join(list(hc["counts"][c]["where"])[:2])
        print(f"      {c}  (peso {hcc[c]:.0f})  ex.: {ex}")

    print(f"\n  render: altura {hc['h']}px, scroll horizontal "
          f"{'SIM (' + str(hc['sw']) + '>' + str(hc['cw']) + ')' if hc['sw'] > hc['cw'] else 'nao'}"
          f", erros JS: {len(hc.get('errors') or [])}")

    if render:
        out = f"/tmp/cmp-s{n}"
        os.makedirs(out, exist_ok=True)
        subprocess.run(["pdftoppm", "-png", "-r", "90", pdf, f"{out}/pdf"],
                       capture_output=True)
        # --render precisa do screenshot do HTML: sem isso a comparação fica
        # só com o PDF e o passo "olhe as imagens" fica impossível.
        # Este script escrevia .collect.tmp.js mas chamava .shot.tmp.js sem
        # nunca cria-lo, entao --render falhava em silencio. Agora ele mesmo
        # gera o helper e apaga no fim.
        shot = os.path.join(ROOT, "tools", ".shot.tmp.js")
        with open(shot, "w") as fh:
            fh.write(SHOT_JS)
        try:
            subprocess.run(["node", shot, os.path.abspath(html), out],
                           capture_output=True)
        finally:
            try:
                os.unlink(shot)
            except OSError:
                pass
        print(f"  imagens em {out}/")


if __name__ == "__main__":
    sys.exit(main())