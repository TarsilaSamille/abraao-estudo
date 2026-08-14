#!/usr/bin/env python3
import struct,zlib
from collections import Counter
IMG='/Users/macbook/Library/Application Support/Hermes/composer-images/composer_2026-08-14_18-23-23-084_6f04e8.png'
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
def mode_of(cond,quant=4):
    c=Counter()
    for y in range(0,h):
        for x in range(0,w):
            ii=(y*w+x)*ch;r,g,b=o[ii],o[ii+1],o[ii+2]
            if cond(r,g,b): c[(r//quant*quant,g//quant*quant,b//quant*quant)]+=1
    if not c: return None
    k,nn=c.most_common(1)[0]; return '#%02x%02x%02x'%k,nn
# condicoes estritas p/ pegar o traço puro (saturado, nao branco/preto)
red=mode_of(lambda r,g,b:r>100 and g<r-55 and b<r-55 and (r+g+b)<430,2)
grn=mode_of(lambda r,g,b:g>80 and g>r+45 and g>b+30,2)
blu=mode_of(lambda r,g,b:b>90 and b>r+45 and b>g+35,2)
gry=mode_of(lambda r,g,b:abs(r-g)<10 and abs(g-b)<10 and 95<r<165,4)
for n,v in [('RED',red),('GREEN',grn),('BLUE',blu),('GREY',gry)]:
    print(n,v)
