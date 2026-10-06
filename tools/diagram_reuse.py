#!/usr/bin/env python3
"""
diagram_reuse.py — a MESMA ilustracao do BibleProject reaparece em sessoes de
cursos diferentes (a Melodia Tematica de Genese 1-11 esta no abraao S3 e no
joseph S2). Antes de reconstruir um diagrama, extraia os rotulos distintivos do
PDF de uma sessao e procure em TODOS os HTMLs do repo.

    python3 tools/diagram_reuse.py <curso> [sessao|*]

Usa ripgrep para o cruzamento, que e ordens de magnitude mais rapido que
substring em Python.
"""
import glob
import json
import os
import re
import subprocess
import sys

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = "/tmp/diagram_labels.json"
RUIDO = re.compile(r"^[\W\d\s]+$|^\(?\d{4}\)?[.,)]?$|^\(?\d+:\d+")
GENERICO = {"genesis", "exodus", "deuteronomy", "judges", "ruth", "samuel", "kings",
            "chronicles", "ezra", "nehemiah", "esther", "job", "psalms", "proverbs",
            "ecclesiastes", "song", "isaiah", "jeremiah", "lamentations", "ezekiel",
            "daniel", "hosea", "joel", "amos", "obadiah", "jonah", "micah", "nahum",
            "habakkuk", "zephaniah", "haggai", "zechariah", "malachi", "moses",
            "abraham", "isaac", "jacob", "joseph", "ruth ", "samson", "david",
            "solomon", "elijah", "elisha", "job ", "moses ", "creation", "new",
            "the", "and", "for", "with", "from", "into", " bible", "hebrew bible"}


def diagram_labels(pdf):
    d = fitz.open(pdf)
    bands = []
    for pg in d:
        for dr in pg.get_drawings():
            r = dr["rect"]
            if r.width > 25 and r.height > 10:
                bands.append((r.y0 - 3, r.y1 + 3, r.x0 - 3, r.x1 + 3))
    out = set()
    for pg in d:
        for b in pg.get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            for l in b["lines"]:
                for s in l["spans"]:
                    t = re.sub(r"\s+", " ", s["text"]).strip()
                    if not (6 <= len(t) <= 26):
                        continue
                    if RUIDO.match(t) or not re.search(r"[A-Za-zÀ-ÿ]{4}", t):
                        continue
                    if t.lower() in GENERICO:
                        continue
                    x, y = s["bbox"][0], s["bbox"][1]
                    if any(y0 <= y <= y1 and x0 <= x <= x1 for y0, y1, x0, x1 in bands):
                        out.add(t)
    d.close()
    return sorted(out)


def carregar():
    if os.path.exists(CACHE):
        return json.load(open(CACHE))
    res = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "*", "pdf-sessoes", "sessao-*.pdf"))):
        curso = p.split(os.sep)[-3]
        sess = os.path.basename(p)[7:-4]
        res[f"{curso}/{sess}"] = diagram_labels(p)
    json.dump(res, open(CACHE, "w"), ensure_ascii=False)
    return res


def rg(rotulo):
    r = subprocess.run(["rg", "-l", "-F", "--", rotulo, ROOT],
                       capture_output=True, text=True)
    return [x for x in r.stdout.split("\n") if x.endswith(".html")]


def main():
    curso = sys.argv[1]
    sess = sys.argv[2] if len(sys.argv) > 2 else "*"
    todos = carregar()
    for chave, labels in todos.items():
        c, s = chave.split("/")
        if c != curso or (sess != "*" and s != sess):
            continue
        own = os.path.join(ROOT, c, "modulo-x", f"sessao-{s}.html")
        #usa os rotulos mais raros (os mais longos) para reduzir falso positivo
        sondas = sorted(labels, key=len, reverse=True)[:8]
        contagem = {}
        for lb in sondas:
            for h in rg(lb):
                if f"modulo-" in h:
                    contagem[h] = contagem.get(h, 0) + 1
        alvos = [(v, k) for k, v in contagem.items()
                 if os.path.basename(k) != f"sessao-{s}.html"]
        alvos.sort(reverse=True)
        print(f"\n=== {chave}  ({len(labels)} rotulos, sondas={len(sondas)}) ===")
        if not alvos:
            print("    *** NENHUMA implementacao reaproveitavel no repo ***")
        for v, h in alvos[:4]:
            print(f"    {v}/{len(sondas)}  {os.path.relpath(h, ROOT)}")


if __name__ == "__main__":
    main()
