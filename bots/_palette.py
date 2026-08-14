#!/usr/bin/env python3
import struct,zlib
from collections import Counter
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
w,h,o,ch=px('/tmp/s2h-3.png')
c=Counter()
for y in range(0,h):
    for x in range(0,w):
        ii=(y*w+x)*ch;r,g,b=o[ii],o[ii+1],o[ii+2]
        mx,mn=max(r,g,b),min(r,g,b)
        if mx-mn>=30 and not(r>235 and g>235 and b>235) and not(r<35 and g<35 and b<35):
            c[(r//8*8,g//8*8,b//8*8)]+=1
# agrupa por matiz amplo p/ dedup; pega o mais escuro (stroke) e o mais claro (fill) de cada grupo
groups={}
for (r,g,b),n in c.items():
    if n<400: continue
    mx,mn=max(r,g,b),min(r,g,b)
    if r>=g and r>=b: hue='R'
    elif g>=r and g>=b: hue='G'
    else: hue='B'
    key=hue
    groups.setdefault(key,[]).append((n,r,g,b))
out=[]
for hue in ['G','R','B']:
    lst=sorted(groups.get(hue,[]),key=lambda t:-t[0])
    if not lst: continue
    # stroke = mais escuro entre os top; fill = mais claro
    dark=min(lst[:8],key=lambda t:sum(t[1:]))
    light=max(lst,key=lambda t:sum(t[1:]))
    out.append((hue+'_STROKE',dark[1],dark[2],dark[3],dark[0]))
    out.append((hue+'_FILL',light[1],light[2],light[3],light[0]))
# greys
greyc=[(n,r,g,b) for (r,g,b),n in c.items() if abs(r-g)<12 and abs(g-b)<12 and 90<r<210 and n>=400]
gs=sorted(greyc,key=lambda t:-t[0])
for n,r,g,b in gs[:4]:
    out.append(('GREY',r,g,b,n))
for name,r,g,b,n in out:
    print(f'{name}: #{r:02x}{g:02x}{b:02x} n={n}')
