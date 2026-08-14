#!/usr/bin/env python3
# Gera preview PNG: 3 linhas (S1/S2/S3), cada uma com 4 swatches (red/green/blue/grey)
# e o hex embaixo. Usa only stdlib (sem PIL).
import struct
def png_chunk(typ,data):
    import zlib
    c=typ+data; return struct.pack('>I',len(data))+c+struct.pack('>I',zlib.crc32(c)&0xffffffff)
def make_png(path,w,h,rgb_rows):
    import zlib
    raw=b''
    for row in rgb_rows:
        raw+=b'\x00'+row
    comp=zlib.compress(raw)
    ihdr=struct.pack('>IIBBBBB',w,h,8,2,0,0,0)
    with open(path,'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(png_chunk(b'IHDR',ihdr))
        f.write(png_chunk(b'IDAT',comp))
        f.write(png_chunk(b'IEND',b''))
def hex2rgb(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
S=[("S1-MODO",  {"R":"#bc4864","G":"#388060","B":"#ccf0f8","K":"#b0b4bc"}),
   ("S2-PURA",  {"R":"#b5543a","G":"#3a8060","B":"#3678b4","K":"#b0b4bc"}),
   ("S3-BORDA", {"R":"#cd7d85","G":"#639a81","B":"#adc6da","K":"#b0b4bc"})]
SW,W,H=120,640,260  # swatch size
pad=10; labelh=40
rowh=SW+labelh+pad
Wtot=4*SW+5*pad
Htot=len(S)*rowh+pad+30
rows=[]
# fundo branco
def bg(w): return b'\xff\xff\xff'*w
y=pad+20
for name,s in S:
    x=pad
    for key,col in [("R","red"),("G","green"),("B","blue"),("K","grey")]:
        rgb=hex2rgb(s[key])
        # swatch
        for r in range(SW):
            rows.append(b''.join(bytes(rgb) for _ in range(SW)))
        # label (hex como texto simples nao implementado; usamos cor sólida + guardamos legenda em arquivo txt)
        x+=SW+pad
    y+=rowh
# reconstrói linha-a-linha em ordem certa: precisamos montar a imagem completa
# abordagem simples: uma unica matriz
matrix=[[ (255,255,255) for _ in range(Wtot)] for _ in range(Htot)]
yy=pad+20
for name,s in S:
    xx=pad
    for key in ["R","G","B","K"]:
        rgb=hex2rgb(s[key])
        for r in range(SW):
            for c in range(SW):
                matrix[yy+r][xx+c]=rgb
        xx+=SW+pad
    yy+=rowh
raw=b''
for row in matrix:
    raw+=b'\x00'+b''.join(bytes(p) for p in row)
make_png('/tmp/preview_3systems.png',Wtot,Htot,[] )  # placeholder
# reescreve make_png para aceitar matriz
import zlib
def make2(path,matrix):
    h=len(matrix); w=len(matrix[0])
    raw=b''.join(b'\x00'+b''.join(bytes(p) for p in row) for row in matrix)
    comp=zlib.compress(raw)
    ihdr=struct.pack('>IIBBBBB',w,h,8,2,0,0,0)
    with open(path,'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(png_chunk(b'IHDR',ihdr)); f.write(png_chunk(b'IDAT',comp)); f.write(png_chunk(b'IEND',b''))
make2('/tmp/preview_3systems.png',matrix)
# legenda txt
with open('/tmp/preview_3systems.txt','w') as f:
    for name,s in S:
        f.write(f"{name}: red={s['R']} green={s['G']} blue={s['B']} grey={s['K']}\n")
print("preview:",'/tmp/preview_3systems.png')
for name,s in S: print(f"{name}: red={s['R']} green={s['G']} blue={s['B']} grey={s['K']}")
