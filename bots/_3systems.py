#!/usr/bin/env python3
# 3 SISTEMAS DIFERENTES de extracao de cor do PDF (pagina 3, 300dpi).
# Cada um tem filosofia distinta de onde/co mo amostrar a "tinta".
import struct,zlib
from collections import Counter,defaultdict

def px(p):
    d=open(p,'rb').read();i=8;idat=b''
    while i<len(d):
        ln=struct.unpack('>I',d[i:i+4])[0];t=d[i+4:i+8];c=d[i+8:i+8+ln]
        if t==b'IHDR':w,h,bd,ct=struct.unpack('>IIBB',c[:10])
        elif t==b'IDAT':idat+=c
        elif t==b'IEND':break
        i+=12+ln
    raw=zlib.decompress(idat);ch=3 if ct==2 else 4;st=w*ch;o=bytearray();pr=bytearray(st);pos=0
    for _ in range(h):
        f=raw[pos];pos+=1;ln=bytearray(raw[pos:pos+st]);pos+=st
        for x in range(st):
            a=ln[x-ch] if x>=ch else 0;b=pr[x];c=pr[x-ch] if x>=ch else 0
            if f==1:ln[x]=(ln[x]+a)&255
            elif f==2:ln[x]=(ln[x]+b)&255
            elif f==3:ln[x]=(ln[x]+(a+b)//2)&255
            elif f==4:
                p=a+b-c;pa,pb,pc=abs(p-a),abs(p-b),abs(p-c)
                pr2=a if(pa<=pb and pa<=pc) else(b if pb<=pc else c);ln[x]=(ln[x]+pr2)&255
        o+=ln;pr=ln
    return w,h,o,ch

W,H,O,CH=px('/tmp/s2h-3.png')
N=W*H
def get(x,y):
    if 0<=x<W and 0<=y<H:
        i=(y*W+x)*CH; return O[i],O[i+1],O[i+2]
    return (255,255,255)
def sat(r,g,b): return max(r,g,b)-min(r,g,b)
def white(r,g,b): return r>235 and g>235 and b>235
def black(r,g,b): return r<35 and g<35 and b<35
def hue(r,g,b):
    if r>=g and r>=b and r-g>40: return 'R'
    if g>=r and g>=b and g-r>40: return 'G'
    return 'B'
def tohex(r,g,b): return '#%02x%02x%02x'%(r,g,b)

# ---------- SISTEMA 1: MODO global (pixel saturado mais frequente por matiz) ----------
def system1():
    c=defaultdict(Counter)
    for y in range(0,H,1):
        for x in range(0,W,1):
            r,g,b=get(x,y)
            if sat(r,g,b)>=30 and not white(r,g,b) and not black(r,g,b):
                k=hue(r,g,b)
                if k: c[k][(r//4*4,g//4*4,b//4*4)]+=1
    out={}
    for k in ['R','G','B']:
        if c[k]:
            (rr,gg,bb),_=c[k].most_common(1)[0]; out[k]=tohex(rr,gg,bb)
    return out

# ---------- SISTEMA 2: TINTA PURA (pixel de MAIOR saturacao por matiz, sem diluted) ----------
def system2():
    best=defaultdict(list)
    for y in range(0,H,1):
        for x in range(0,W,1):
            r,g,b=get(x,y)
            if sat(r,g,b)>=30 and not white(r,g,b) and not black(r,g,b):
                k=hue(r,g,b)
                if k: best[k].append((sat(r,g,b),r,g,b))
    out={}
    for k in ['R','G','B']:
        if best[k]:
            best[k].sort(reverse=True)
            top=best[k][:max(1,len(best[k])//50)]  # 2% mais puros
            r=sum(t[1] for t in top)//len(top); g=sum(t[2] for t in top)//len(top); b=sum(t[3] for t in top)//len(top)
            out[k]=tohex(r,g,b)
    return out

# ---------- SISTEMA 3: BORDA/STROKE (pixel saturado com vizinho branco = linha da borda) ----------
def system3():
    edge=defaultdict(list)
    for y in range(0,H,1):
        for x in range(0,W,1):
            r,g,b=get(x,y)
            if sat(r,g,b)>=30 and not white(r,g,b) and not black(r,g,b):
                # tem vizinho branco? entao esta na borda do travo
                neigh=[get(x-1,y),get(x+1,y),get(x,y-1),get(x,y+1)]
                if any(white(*n) for n in neigh):
                    k=hue(r,g,b)
                    if k: edge[k].append((r,g,b))
    out={}
    for k in ['R','G','B']:
        if edge[k]:
            r=sum(t[0] for t in edge[k])//len(edge[k]); g=sum(t[1] for t in edge[k])//len(edge[k]); b=sum(t[2] for t in edge[k])//len(edge[k])
            out[k]=tohex(r,g,b)
    return out

# GREY (neutro) comum aos 3: mediana dos cinzas medios
def grey_common():
    c=Counter()
    for y in range(0,H,1):
        for x in range(0,W,1):
            r,g,b=get(x,y)
            if abs(r-g)<10 and abs(g-b)<10 and 90<r<200: c[(r//4*4,g//4*4,b//4*4)]+=1
    (rr,gg,bb),_=c.most_common(1)[0]; return tohex(rr,gg,bb)

s1=system1(); s2=system2(); s3=system3(); g=grey_common()
for name,s in [("S1-MODO",s1),("S2-PURA",s2),("S3-BORDA",s3)]:
    print(f"{name}: red={s.get('R')} green={s.get('G')} blue={s.get('B')} grey={g}")
