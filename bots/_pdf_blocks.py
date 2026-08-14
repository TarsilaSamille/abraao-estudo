#!/usr/bin/env python3
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
w,h,o,ch=px('/tmp/sall-3.png')
def sat(r,g,b): return max(r,g,b)-min(r,g,b)
def white(r,g,b): return r>235 and g>235 and b>235
def black(r,g,b): return r<35 and g<35 and b<35
def hue(r,g,b):
    if r>=g and r>=b and r-g>40: return 'R'
    if g>=r and g>=b and g-r>40: return 'G'
    return 'B'
def borders(y0f,y1f):
    y0,y1=int(h*y0f/100),int(h*y1f/100)
    seg=defaultdict(list)
    for y in range(y0,min(y1,h)):
        x=0
        while x<w:
            r,g,b=o[(y*w+x)*ch],o[(y*w+x)*ch+1],o[(y*w+x)*ch+2]
            if sat(r,g,b)>=40 and not white(r,g,b) and not black(r,g,b):
                x0=x;left_ok=(x0==0) or white(o[(y*w+(x0-1))*ch],o[(y*w+(x0-1))*ch+1],o[(y*w+(x0-1))*ch+2])
                xx=x0
                while xx<w:
                    rr,gg,bb=o[(y*w+xx)*ch],o[(y*w+xx)*ch+1],o[(y*w+xx)*ch+2]
                    if not(sat(rr,gg,bb)>=40 and not white(rr,gg,bb) and not black(rr,gg,bb)): break
                    xx+=1
                x1=xx;right_ok=(x1>=w) or white(o[(y*w+x1)*ch],o[(y*w+x1)*ch+1],o[(y*w+x1)*ch+2])
                if left_ok or right_ok:
                    k=hue(r,g,b)
                    if k:
                        for cx in range(x0,x1): seg[k].append((o[(y*w+cx)*ch],o[(y*w+cx)*ch+1],o[(y*w+cx)*ch+2]))
                x=x1
            else: x+=1
    out={}
    for k in ['R','G','B']:
        if seg[k]:
            rs=sorted(p[0] for p in seg[k]);gs=sorted(p[1] for p in seg[k]);bs=sorted(p[2] for p in seg[k]);n=len(rs)
            out[k]='#%02x%02x%02x'%(rs[n//2],gs[n//2],bs[n//2])
    return out
# blocos do PDF (vision): macro topo, D1 28-48%, D2 52-70%, D3 75-90%
print("MACRO(top 0-25%):", borders(0,25))
print("D1(28-48%):", borders(28,48))
print("D2(52-70%):", borders(52,70))
print("D3(75-90%):", borders(75,90))
