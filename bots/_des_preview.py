#!/usr/bin/env python3
import struct,zlib
from collections import Counter
def png_chunk(typ,data):
    c=typ+data; return struct.pack('>I',len(data))+c+struct.pack('>I',zlib.crc32(c)&0xffffffff)
def make(path,matrix):
    h=len(matrix); w=len(matrix[0])
    raw=b''.join(b'\x00'+b''.join(bytes(p) for p in row) for row in matrix)
    comp=zlib.compress(raw)
    ihdr=struct.pack('>IIBBBBB',w,h,8,2,0,0,0)
    with open(path,'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(png_chunk(b'IHDR',ihdr)); f.write(png_chunk(b'IDAT',comp)); f.write(png_chunk(b'IEND',b''))
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
def topcols(y0,y1):
    c=Counter()
    for y in range(y0,min(y1,h)):
        for x in range(0,w):
            ii=(y*w+x)*ch;r,g,b=o[ii],o[ii+1],o[ii+2]
            mx,mn=max(r,g,b),min(r,g,b)
            if mx-mn>=30 and not(r>235 and g>235 and b>235) and not(r<35 and g<35 and b<35):
                c[(r//8*8,g//8*8,b//8*8)]+=1
    return [( '#%02x%02x%02x'%k,n) for k,n in c.most_common(7)]
bands=[("D2",600,1200),("D3",1200,1800),("D4",1800,2400)]
SW=110;pad=8;H=SW+pad*2
for name,y0,y1 in bands:
    cols=topcols(y0,y1)
    W=len(cols)*SW+(len(cols)+1)*pad
    m=[[(255,255,255) for _ in range(W)] for _ in range(H)]
    x=pad
    for hexv,n in cols:
        r=int(hexv[1:3],16);g=int(hexv[3:5],16);b=int(hexv[5:7],16)
        for rr in range(SW):
            for cc in range(SW): m[pad+rr][x+cc]=(r,g,b)
        x+=SW+pad
    make(f'/tmp/des_{name}.png',m)
    print(name, cols)
