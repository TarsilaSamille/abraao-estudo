#!/usr/bin/env python3.14
"""Final style 1:1 check: for each session, count colored regions in PDF vs
colored elements in HTML. Reports divergences. Pure pixel/structure (no vision)."""
import os, re, sys
import fitz
from PIL import Image
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = {"seed":"#D3F2CD","beige":"#FAE4C4","rose":"#F7E1F5","divine":"#5869CD",
         "action":"#E4E8ED","red":"#BE4967","grey":"#6B7384","olive":"#645537"}

def h2rgb(h): h=h.lstrip('#');return tuple(int(h[i:i+2],16) for i in (0,2,4))

def count_regions(mask):
    if not mask.any(): return 0
    H,W=mask.shape; lab=np.zeros((H,W),dtype=int); cur=0
    for y in range(H):
        for x in range(W):
            if mask[y,x] and lab[y,x]==0:
                cur+=1; stack=[(y,x)]
                while stack:
                    yy,xx=stack.pop()
                    if lab[yy,xx]:continue
                    lab[yy,xx]=cur
                    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
                        ny,nx=yy+dy,xx+dx
                        if 0<=ny<H and 0<=nx<W and mask[ny,nx] and lab[ny,nx]==0:
                            stack.append((ny,nx))
    sizes={}
    for v in lab.reshape(-1):
        if v>0: sizes[v]=sizes.get(v,0)+1
    return sum(1 for v in sizes.values() if v>=40)

def pdf_regions(s):
    d=fitz.open(os.path.join(ROOT,"pdf-sessoes",f"sessao-{s}.pdf"))
    counts={k:0 for k in CANON}
    for p in d:
        pix=p.get_pixmap(dpi=72)
        im=np.asarray(Image.frombytes('RGB',[pix.width,pix.height],pix.samples)).astype(int)
        for name,h in CANON.items():
            t=np.array(h2rgb(h))
            mask=np.all(np.abs(im-t)<=18,axis=2)
            counts[name]+=count_regions(mask)
    return counts

def html_classes(s,m):
    txt=open(os.path.join(ROOT,m,f"sessao-{s}.html"),encoding='utf-8').read()
    # count color-class occurrences actually used in markup
    used={}
    for c in ["k-seed","k-beige","k-rose","k-rose2","k-divine","k-blue","k-purple","k-teal","k-grey","k-red","k-olive","k-day","k-night","k-dome"]:
        used[c]=len(re.findall(r'class="[^"]*\b'+c+r'\b',txt))
    return used

MODULES={6:"modulo-2",7:"modulo-2",8:"modulo-2",9:"modulo-2",10:"modulo-2",11:"modulo-2",12:"modulo-2",
 13:"modulo-3",14:"modulo-3",15:"modulo-3",
 16:"modulo-4",17:"modulo-4",18:"modulo-4",19:"modulo-4",20:"modulo-4",21:"modulo-4",22:"modulo-4",
 23:"modulo-5",24:"modulo-5",25:"modulo-5",26:"modulo-5",
 27:"modulo-6",28:"modulo-6",29:"modulo-6",
 30:"modulo-7",31:"modulo-7"}

if __name__=="__main__":
    print(f"{'s':>3} {'mod':>9} | {'PDF color regions':>52} | HTML k-* used")
    for s in sorted(MODULES):
        m=MODULES[s]
        pr=pdf_regions(s)
        hc=html_classes(s,m)
        hc_used={k:v for k,v in hc.items() if v>0}
        pdfsum=sum(pr.values())
        pr_s=f"seed={pr['seed']} beige={pr['beige']} rose={pr['rose']} divine={pr['divine']} action={pr['action']} olive={pr['olive']}"
        print(f"{s:>3} {m:>9} | {pr_s:>52} | {hc_used}")
