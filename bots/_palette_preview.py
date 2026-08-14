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
# cores distintas do PDF (top, com n>=800), dedup proximas
cols=[("#388060",26740),("#b84860",17856),("#c8f0f8",14383),("#3078b0",13912),
      ("#b05038",9620),("#d0f0c8",7402),("#5868c8",5690),("#205090",1136),
      ("#609880",1854),("#c86880",1664),("#78a890",1157),("#a0c0b0",1283),
      ("#c8d8e8",1051),("#a0c0d8",949),("#6898c8",863),("#9098d8",863)]
SW=120;pad=8;H=SW+pad*2
W=len(cols)*SW+(len(cols)+1)*pad
m=[[(255,255,255) for _ in range(W)] for _ in range(H)]
x=pad
for hexv,_ in cols:
    r=int(hexv[1:3],16);g=int(hexv[3:5],16);b=int(hexv[5:7],16)
    for rr in range(SW):
        for cc in range(SW):
            m[pad+rr][x+cc]=(r,g,b)
    x+=SW+pad
make('/tmp/palette_full.png',m)
with open('/tmp/palette_full.txt','w') as f:
    for hexv,n in cols: f.write(f"{hexv} n={n}\n")
print("palette:",'/tmp/palette_full.png')
for hexv,n in cols: print(hexv,n)
