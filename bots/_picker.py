#!/usr/bin/env python3
# Picker real: decodifica PNG, acha o pixel de TRAVO (borda) mais puro por matiz.
# Borda = pixel saturado que NAO e branco nem preto, pega o de saturação máxima
# (a tinta da borda é a mais saturada; fill/claro é menos saturado).
import struct,zlib
from collections import defaultdict
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
P='/tmp/s2h-2.png'  # pagina do design colorido
w,h,o,ch=px(P)
def sat(r,g,b): return max(r,g,b)-min(r,g,b)
buckets=defaultdict(list)  # 'R'/'G'/'B' -> lista de (sat,(r,g,b),x,y)
for y in range(0,h,1):
    for x in range(0,w,1):
        ii=(y*w+x)*ch;r,g,b=o[ii],o[ii+1],o[ii+2]
        if sat(r,g,b)>=55 and not(r>235 and g>235 and b>235) and not(r<40 and g<40 and b<40):
            if r>g and r>b and r-g>40: k='R'
            elif g>r and g>b and g-r>40: k='G'
            else: k='B'
            buckets[k].append((sat((r,g,b)),(r,g,b),x,y))
for k in ['R','G','B']:
    lst=buckets[k]
    if not lst: print(k,'NONE'); continue
    # pixel de MAIOR saturacao = tinta pura da borda
    lst.sort(reverse=True)
    s,(r,g,b),x,y=lst[0]
    # pega a MODA entre os 50 pixels mais saturados (estavel)
    from collections import Counter
    cc=Counter((r//3*3,g//3*3,b//3*3) for _,(r,g,b),_,_ in lst[:50])
    (rr,gg,bb),_=cc.most_common(1)[0]
    print(f"{k} #{rr:02x}{gg:02x}{bb:02x}  (top-sat pixel #{r:02x}{g:02x}{b:02x} at {x},{y})")
