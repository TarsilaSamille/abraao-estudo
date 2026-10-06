#!/usr/bin/env python3
"""
diagram_inventory.py — inventaria os diagramas de TODO o repositorio.

Para cada PDF de sessao extrai os rotulos caracteristicos do diagrama (textos
curtos e unicos que aparecem DENTRO de caixas/desenhos, nao da prosa) e procura
essses rotulos nos HTMLs. Serve para responder: "esta sessao ja tem o diagrama
correto em algum lugar do repo?" antes de reconstruir qualquer coisa.

    python3 tools/diagram_inventory.py [curso]
"""
import collections
import glob
import os
import re
import sys

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def pdf_diag_labels(path):
    """Rotulos do diagrama: textos em fonte pequena/colorida ou dentro de
    caixas desenhadas. Heuristica: y dentro da regiao com muitos paths."""
    d = fitz.open(path)
    # regiao com paths = diagrama
    ys = []
    for pg in d:
        for dr in pg.get_drawings():
            r = dr["rect"]
            if r.width > 20 and r.height > 8:
                ys.append((r.y0, r.y1))
    spans = []
    for pi, pg in enumerate(d):
        for b in pg.get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            for l in b["lines"]:
                for s in l["spans"]:
                    t = s["text"].strip()
                    if len(t) < 2 or len(t) > 40:
                        continue
                    # dentro de uma caixa desenhada?
                    x, y = s["bbox"][0], s["bbox"][1]
                    inbox = any(y0 - 2 <= y <= y1 + 2 for y0, y1 in ys)
                    if inbox:
                        spans.append((pi + 1, t))
    d.close()
    return spans


def norm(t):
    return re.sub(r"\s+", " ", t).strip().lower()


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    # 1) coleta rotulos de todos os PDFs
    pdfs = sorted(glob.glob(os.path.join(ROOT, "*", "pdf-sessoes", "*.pdf")))
    htmls = sorted(glob.glob(os.path.join(ROOT, "*", "modulo-*", "*.html")))
    if only:
        pdfs = [p for p in pdfs if f"/{only}/" in p]
    html_text = {}
    for h in htmls:
        try:
            html_text[h] = open(h, encoding="utf-8").read()
        except Exception:
            pass

    rows = []
    for p in pdfs:
        curso = p.split(os.sep)[-3]
        if only and curso != only:
            continue
        nome = os.path.basename(p)[:-4]
        if not nome.startswith("sessao-"):
            continue
        sess = nome[len("sessao-"):]
        if not sess.isdigit():
            continue
        labels = pdf_diag_labels(p)
        uniq = sorted({norm(t) for _, t in labels})
        # assinatura: rotulos raros (nao-genericos) presentes em algum HTML
        signature = [t for t in uniq
                     if 4 <= len(t) <= 30 and not t[0].isdigit()]
        found = []
        for h, txt in html_text.items():
            low = txt.lower()
            hit = sum(1 for t in signature if t in low)
            if signature and hit / len(signature) >= 0.35:
                found.append((hit / len(signature), os.path.relpath(h, ROOT)))
        found.sort(reverse=True)
        rows.append((curso, int(sess), len(uniq), signature[:3], found[:2]))

    for curso, sess, n, sig, found in rows:
        best = found[0] if found else None
        mark = "OK " if best else "--- "
        loc = f"{best[0]:.0%} {best[1]}" if best else "SEM IMPLEMENTACAO"
        print(f"{mark}{curso:22s} S{sess:<3d} rotulos={n:<4d} {loc}")
        if best:
            print(f"      assinatura: {sig}")


if __name__ == "__main__":
    main()
