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
def hx(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))

# 4 versoes de paleta (cada uma com os 4 designs)
V=[
 ("V1_pdf-mode",   {"D1":"#a2a2ae","D2g":"#388060","D2r":"#b84860","D2b":"#3078b0","D3v":"#6898c8","D4r":"#b05038","D4b":"#c8f0f8"}),
 ("V2_pdf-edge",   {"D1":"#6c7080","D2g":"#286040","D2r":"#a84860","D2b":"#205090","D3v":"#4a5cb8","D4r":"#9c4028","D4b":"#a8d8e8"}),
 ("V3_bp-brand",   {"D1":"#404853","D2g":"#3a9d6e","D2r":"#e05a5a","D2b":"#3a7bd5","D3v":"#7b5cd6","D4r":"#e8893a","D4b":"#36c5d6"}),
 ("V4_screen",     {"D1":"#6c7080","D2g":"#4c7c60","D2r":"#ae5266","D2b":"#4876ae","D3v":"#7b6fd0","D4r":"#d06a3a","D4b":"#5fb8c8"}),
]
# mockup: para cada versao, 4 linhas (D1..D4), cada uma com caixas coloridas
SW,W,H=70,520,40
def build(v):
    pal=v[1]
    rows=[]
    designs=[("D1",[("grey",pal["D1"])]),
            ("D2",[("green",pal["D2g"]),("red",pal["D2r"]),("blue",pal["D2b"])]),
            ("D3",[("green",pal["D2g"]),("red",pal["D2r"]),("blue",pal["D2b"]),("violet",pal["D3v"])]),
            ("D4",[("green",pal["D2g"]),("orange",pal["D4r"]),("cyan",pal["D4b"])])]
    for name,boxes in designs:
        row=[[(255,255,255)]*W for _ in range(H)]
        x=10
        for lbl,col in boxes:
            r,g,b=hx(col)
            for ry in range(5,H-5):
                for rx in range(SW):
                    if rx<3 or rx>SW-4 or ry<3 or ry>H-4:  # so border
                        row[ry][x+rx]=(r,g,b)
            x+=SW+10
        rows+=row
    return rows
for name,pal in V:
    m=build((name,pal))
    make(f'/tmp/ver_{name}.png',m)
    print(name,'->',pal)
