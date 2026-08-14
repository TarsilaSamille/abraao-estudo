#!/usr/bin/env python3
import struct,zlib
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
def hx(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
# cores EXATAS da BORDA do PDF, por design
D={
 "D1_macro":    ["#6c7080"],
 "D2_diagram1": ["#3a8060","#be4967","#3678b4"],
 "D3_diagram2": ["#3a8060","#be4967","#3678b4","#6898c8"],
 "D4_diagram3": ["#3a8060","#b5543a","#ccf1fa"],
}
SW=140;pad=12;H=SW+pad*2
for name,cols in D.items():
    W=len(cols)*SW+(len(cols)+1)*pad
    m=[[(255,255,255) for _ in range(W)] for _ in range(H)]
    x=pad
    for hexv in cols:
        r,g,b=hx(hexv)
        for rr in range(SW):
            for cc in range(SW): m[pad+rr][x+cc]=(r,g,b)
        x+=SW+pad
    make(f'/tmp/design_{name}.png',m)
    print(name, cols)
