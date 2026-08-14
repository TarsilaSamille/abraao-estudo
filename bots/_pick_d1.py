#!/usr/bin/env python3
import struct,zlib
from collections import Counter
IMG='/Users/macbook/Library/Application Support/Hermes/composer-images/composer_2026-08-14_18-15-45-943_d6316e.png'
d=open(IMG,'rb').read();i=8;idat=b''
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
# charcoal tag: escuro, baixa saturacao, nao preto puro
c=Counter()
for y in range(0,h):
    for x in range(0,w):
        ii=(y*w+x)*ch;r,g,b=o[ii],o[ii+1],o[ii+2]
        if 25<r<130 and 25<g<130 and 25<b<130 and max(r,g,b)-min(r,g,b)<35 and not(r<50 and g<50 and b<50):
            c[(r//4*4,g//4*4,b//4*4)]+=1
print("Design1 charcoal:", '#%02x%02x%02x'%c.most_common(1)[0][0], c.most_common(1)[0][1])
