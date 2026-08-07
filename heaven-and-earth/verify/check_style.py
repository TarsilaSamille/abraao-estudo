#!/usr/bin/env python3.14
"""Style 1:1 check: compare dominant color palette of PDF vs HTML for each
session. Also reports structural element counts. Pure pixel/structure check
(no vision). Outputs a per-session report."""
import os, re, sys, glob
import fitz
from PIL import Image
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERIFY = os.path.join(ROOT, "verify")

# canonical palette from SOUL (measured from PDFs)
CANON = {
    "seed":   "#D3F2CD",
    "beige":  "#FAE4C4",
    "rose":   "#F7E1F5",
    "divine": "#5869CD",
    "action": "#E4E8ED",
    "red":    "#BE4967",
    "grey":   "#6B7384",
    "olive":  "#645537",
    "text":   "#1B1B1B",
}
def hex2rgb(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))

def pdf_palette(session, thr=400):
    """Return set of canonical palette colors found in PDF + dominant non-grey colors."""
    pdf = os.path.join(ROOT, "pdf-sessoes", f"sessao-{session}.pdf")
    d = fitz.open(pdf)
    found = set()
    for p in d:
        pix = p.get_pixmap(dpi=90)
        im = Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        # check each canonical color presence
        for name,h in CANON.items():
            r,g,b = hex2rgb(h)
            # sample
            present=False
            w,h2=im.size
            step=max(1,w//200)
            for y in range(0,h2,step*2):
                for x in range(0,w,step):
                    pr,pg,pb=im.getpixel((x,y))
                    if abs(pr-r)<14 and abs(pg-g)<14 and abs(pb-b)<14:
                        present=True; break
                if present: break
            if present: found.add(name)
    return found

def html_colors(session, module):
    """Extract hex colors referenced in the HTML (style attrs + css + class defs)."""
    path=os.path.join(ROOT, module, f"sessao-{session}.html")
    txt=open(path,encoding='utf-8').read()
    hexes=set(re.findall(r'#[0-9a-fA-F]{6}', txt))
    # also class names that imply palette
    classes=set(re.findall(r'class="([^"]+)"', txt))
    return hexes, classes

def html_struct(session, module):
    path=os.path.join(ROOT, module, f"sessao-{session}.html")
    txt=open(path,encoding='utf-8').read()
    return {
        "figure": txt.count('class="figure'),
        "scripture": txt.count('class="scripture'),
        "bibleref": txt.count('class="bibleref'),
        "section_h2": txt.count('<h2'),
        "sub_h3": txt.count('<h3'),
        "k-": txt.count('k-beige')+txt.count('k-rose')+txt.count('k-seed')+txt.count('k-divine')+txt.count('k-teal')+txt.count('k-purple'),
    }

MODULES = {
 1:"modulo-1",2:"modulo-1",3:"modulo-1",4:"modulo-1",5:"modulo-1",
 6:"modulo-2",7:"modulo-2",8:"modulo-2",9:"modulo-2",10:"modulo-2",11:"modulo-2",12:"modulo-2",
 13:"modulo-3",14:"modulo-3",15:"modulo-3",
 16:"modulo-4",17:"modulo-4",18:"modulo-4",19:"modulo-4",20:"modulo-4",21:"modulo-4",22:"modulo-4",
 23:"modulo-5",24:"modulo-5",25:"modulo-5",26:"modulo-5",
 27:"modulo-6",28:"modulo-6",29:"modulo-6",
 30:"modulo-7",31:"modulo-7",
}

if __name__=="__main__":
    start=int(sys.argv[1]) if len(sys.argv)>1 else 6
    end=int(sys.argv[2]) if len(sys.argv)>2 else 31
    print(f"{'sess':>4} {'mod':>9} {'PDFcolors':>22} {'HTMLhas':>9} {'missing':>16}  struct")
    for s in range(start, end+1):
        m=MODULES[s]
        pcolors=pdf_palette(s)
        hhex,hcls=html_colors(s,m)
        hhex_l={h.lower() for h in hhex}
        # which canonical colors present in HTML?
        html_has=set()
        for name,h in CANON.items():
            if h.lower() in hhex_l: html_has.add(name)
        # also detect by class (k-seed etc imply seed)
        if any('k-seed' in c for c in hcls): html_has.add('seed*')
        if any('k-divine' in c for c in hcls): html_has.add('divine*')
        if any('k-rose' in c for c in hcls): html_has.add('rose*')
        if any('k-beige' in c for c in hcls): html_has.add('beige*')
        missing=pcolors - html_has
        st=html_struct(s,m)
        print(f"{s:>4} {m:>9} {','.join(sorted(pcolors)):>22} {','.join(sorted(html_has)):>9} {','.join(sorted(missing)):>16}  fig={st['figure']} scr={st['scripture']} br={st['bibleref']} k={st['k-']}")
