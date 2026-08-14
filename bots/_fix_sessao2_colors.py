#!/usr/bin/env python3
"""Colore a SESSION 1 (Macro Design) da sessao-2 para iguar a SESSION 2
(Visual Diagrams), que ja tem os 4 designs separados por cor.

Os 4 designs (cores extraidas EXATAS da imagem do PDF):
  red   #d25e61  (covenant rounds)
  green #39946a  (promise / failure)
  blue  #5288d7  (Lot)
  gray  #b0b8c0  (container neutro)

Em Section 2: caixas externas (container) = gray; so caixas de proposito unico
recebem cor. Mapeamento identico aqui:
  - caixa externa (macro-subbadge range) -> gray, EXCETO 20:1-18=green, 22:1-19=red
  - <li> verse-link -> cor daquele versiculo (separado, um design por versiculo)

Uso: python3 bots/_fix_sessao2_colors.py [--dry]
"""
import sys

PATH = "abraao/modulo-1/sessao-2.html"
HEX = {"red": "#d25e61", "green": "#39946a", "blue": "#5288d7", "gray": "#b0b8c0"}

# caixas externas da Section 1 (range do macro-subbadge) -> cor da CAIXA
BOX_COLOR = {
    "11:27-14:24": "gray", "15:1-17:27": "gray", "18:1-19:38": "gray",
    "20:1-18": "green", "21:1-34": "gray", "22:1-19": "red",
    "22:20-24": "gray", "23:1-20": "gray", "24:1-67": "gray", "25:1-18": "gray",
}
# <li> verse-link -> cor (design separado por versiculo)
LI_COLOR = {
    "11:27-12:5": "gray", "12:6-13:18": "gray", "14:1-24": "gray",
    "15:1-21": "red", "16:1-16": "green", "17:1-27": "red",
    "18:1-15": "green", "18:16-33": "gray", "19:1-39": "blue",
    "20:1-2": "gray", "20:3-13": "gray", "20:14-18": "gray",
    "21:1-21": "red", "21:22-34": "green",
    "22:1-3": "gray", "22:4-14": "gray", "22:15-19": "gray",
}
BOX = '<div class="border-[1.5px] border-slate-400 rounded-md p-3 bg-white">'
CSS = """
.box-red   { border-color:#d25e61 !important; }
.box-green { border-color:#39946a !important; }
.box-blue  { border-color:#5288d7 !important; }
.box-gray  { border-color:#b0b8c0 !important; }
.box-red .macro-subbadge   { background:#d25e61 !important; }
.box-green .macro-subbadge { background:#39946a !important; }
.box-blue .macro-subbadge  { background:#5288d7 !important; }
.box-gray .macro-subbadge  { background:#b0b8c0 !important; }
.vlink-red   { color:#d25e61 !important; }
.vlink-green { color:#39946a !important; }
.vlink-blue  { color:#5288d7 !important; }
.vlink-gray  { color:#7a828c !important; }
"""

def ref_of(s, start):
    k = s.find("data-reference=", start)
    if k == -1:
        return None
    p = s.find("+", k)
    if p == -1:
        return None
    e = p
    while e < len(s) and s[e] not in "\"'":
        e += 1
    return s[p+1:e]

def main():
    dry = "--dry" in sys.argv
    html = open(PATH, encoding="utf-8").read()
    if "box-red" not in html:
        html = html.replace("</style>", CSS + "</style>", 1)
    # 1) boxes externos da Section 1 (ate o Section 2 comeca em "VISUAL DIAGRAM 1")
    sec2 = html.find("<!-- VISUAL DIAGRAM 1 -->")
    s1 = html[:sec2]
    s2 = html[sec2:]
    out, i, nb = [], 0, 0
    while True:
        j = s1.find(BOX, i)
        if j == -1:
            out.append(s1[i:]); break
        out.append(s1[i:j])
        ref = ref_of(s1, j + len(BOX))
        color = BOX_COLOR.get(ref)
        out.append(BOX.replace("border-slate-400", "box-" + color) if color else BOX)
        if color: nb += 1
        i = j + len(BOX)
    s1 = "".join(out)
    # 2) <li> verse-links (só na Section 1)
    out, i, nv = [], 0, 0
    while True:
        j = s1.find("<li>", i)
        if j == -1:
            out.append(s1[i:]); break
        out.append(s1[i:j])
        ref = ref_of(s1, j)
        color = LI_COLOR.get(ref)
        if color and color != "gray":
            a = s1.find("<a ", j)
            if a != -1:
                b = s1.find(">", a)
                if b != -1 and "vlink-" not in s1[a:b]:
                    s1 = s1[:b] + ' class="vlink-' + color + '"' + s1[b:]
                    nv += 1
        out.append("<li>")
        i = j + 4
    s1 = "".join(out)
    html = s1 + s2
    if dry:
        print(f"[dry] boxes: {nb}, vlinks: {nv}")
        return
    open(PATH, "w", encoding="utf-8").write(html)
    print(f"boxes: {nb}, vlinks: {nv}")

if __name__ == "__main__":
    main()
