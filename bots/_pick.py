import struct,zlib
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
def pick(cond):
    best=None
    for y in range(0,h,2):
        for x in range(0,w,2):
            ii=(y*w+x)*ch;r,g,b=o[ii],o[ii+1],o[ii+2]
            if cond(r,g,b):
                s=r+g+b
                if best is None or s>best[0]: best=(s,(r,g,b))
    return best
red=pick(lambda r,g,b:r>140 and g<120 and b<120 and r-g>50)
grn=pick(lambda r,g,b:g>120 and r<140 and b<140 and g-r>30 and g-b>20)
blu=pick(lambda r,g,b:b>140 and r<130 and g<150 and b-r>40)
gry=pick(lambda r,g,b:abs(r-g)<20 and abs(g-b)<20 and 70<r<140)
for n,v in [('RED',red),('GREEN',grn),('BLUE',blu),('GREY',gry)]:
    if v: print(n,'#%02x%02x%02x'%v[1])
