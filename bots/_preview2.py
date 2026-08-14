#!/usr/bin/env python3
import struct,zlib
def png_chunk(typ,data):
    c=typ+data; return struct.pack('>I',len(data))+c+struct.pack('>I',zlib.crc32(c)&0xffffffff)
def hex2rgb(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
def make(path,matrix):
    h=len(matrix); w=len(matrix[0])
    raw=b''.join(b'\x00'+b''.join(bytes(p) for p in row) for row in matrix)
    comp=zlib.compress(raw)
    ihdr=struct.pack('>IIBBBBB',w,h,8,2,0,0,0)
    with open(path,'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(png_chunk(b'IHDR',ihdr)); f.write(png_chunk(b'IDAT',comp)); f.write(png_chunk(b'IEND',b''))
S=[("S1-MODO",  {"R":"#bc4864","G":"#388060","B":"#ccf0f8","K":"#b0b4bc"}),
   ("S2-PURA",  {"R":"#b5543a","G":"#3a8060","B":"#3678b4","K":"#b0b4bc"}),
   ("S3-BORDA", {"R":"#cd7d85","G":"#639a81","B":"#adc6da","K":"#b0b4bc"})]
SW=200; label=60; pad=20
Wtot=4*SW+5*pad
for idx,(name,s) in enumerate(S,1):
    Htot=SW+label+2*pad
    m=[[(255,255,255) for _ in range(Wtot)] for _ in range(Htot)]
    xx=pad
    for key in ["R","G","B","K"]:
        rgb=hex2rgb(s[key])
        for r in range(SW):
            for c in range(SW):
                m[pad+r][xx+c]=rgb
        xx+=SW+pad
    make(f'/tmp/sys{idx}.png',m)
    print(name, f'/tmp/sys{idx}.png', {k:s[k] for k in 'RGBK'})
