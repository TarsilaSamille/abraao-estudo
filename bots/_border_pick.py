#!/usr/bin/env python3
# MELHOR METODO: isola apenas a BORDA (linha fina) e le o pixel exato.
# Uma borda = sequencia de pixels saturados cercada por branco de ambos os lados.
# Pega o pixel mediano de cada segmento de borda -> cor exata da tinta, sem fill.
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
w,h,o,ch=px('/tmp/sall-3.png')
def sat(r,g,b): return max(r,g,b)-min(r,g,b)
def white(r,g,b): return r>235 and g>235 and b>235
def black(r,g,b): return r<35 and g<35 and b<35
def hue(r,g,b):
    if r>=g and r>=b and r-g>40: return 'R'
    if g>=r and g>=b and g-r>40: return 'G'
    return 'B'
# para cada linha horizontal, acha segmentos de pixels saturados (borda) cercados por branco
seg=defaultdict(list)  # hue -> lista de (r,g,b) de bordas
for y in range(0,h):
    x=0
    while x<w:
        r,g,b=o[(y*w+x)*ch],o[(y*w+x)*ch+1],o[(y*w+x)*ch+2]
        if sat(r,g,b)>=40 and not white(r,g,b) and not black(r,g,b):
            # inicio de segmento
            x0=x
            # verifica branco a esquerda (borda, nao fill interno)
            left_ok = (x0==0) or white(*[o[(y*w+(x0-1))*ch+i] for i in range(3)])
            xx=x0
            while xx<w:
                rr,gg,bb=o[(y*w+xx)*ch],o[(y*w+xx)*ch+1],o[(y*w+xx)*ch+2]
                if not(sat(rr,gg,bb)>=40 and not white(rr,gg,bb) and not black(rr,gg,bb)): break
                xx+=1
            x1=xx
            # branco a direita
            right_ok = (x1>=w) or white(*[o[(y*w+x1)*ch+i] for i in range(3)])
            if left_ok or right_ok:  # pelo menos um lado branco = provavelmente borda
                k=hue(r,g,b)
                if k:
                    for cx in range(x0,x1):
                        rr,gg,bb=o[(y*w+cx)*ch],o[(y*w+cx)*ch+1],o[(y*w+cx)*ch+2]
                        seg[k].append((rr,gg,bb))
            x=x1
        else:
            x+=1
for k in ['R','G','B']:
    if seg[k]:
        # mediana dos pixels de borda
        rs=[p[0] for p in seg[k]];gs=[p[1] for p in seg[k]];bs=[p[2] for p in seg[k]]
        rs.sort();gs.sort();bs.sort();n=len(rs)
        print(f"{k}: #{rs[n//2]:02x}{gs[n//2]:02x}{bs[n//2]:02x}  (border px={n})")
    else:
        print(k,"NONE")
