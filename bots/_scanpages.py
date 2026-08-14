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
for pg in [1,2,3,4]:
    w,h,o,ch=px('/tmp/s2h-%d.png'%pg)
    c=Counter()
    for y in range(0,h):
        for x in range(0,w):
            ii=(y*w+x)*ch;r,g,b=o[ii],o[ii+1],o[ii+2]
            mx,mn=max(r,g,b),min(r,g,b)
            if mx-mn>=30 and not(r>235 and g>235 and b>235) and not(r<35 and g<35 and b<35):
                c[(r//6*6,g//6*6,b//6*6)]+=1
    print(f"--- page {pg} ({w}x{h}) saturated top ---")
    for k,n in c.most_common(12): print(f"  #{k[0]:02x}{k[1]:02x}{k[2]:02x} n={n}")
