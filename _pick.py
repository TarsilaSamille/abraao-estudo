import struct, zlib
from PIL import Image

rendered = {1:"/tmp/a8-1.png",2:"/tmp/a8-2.png",3:"/tmp/a8-3.png",4:"/tmp/a8-4.png",5:"/tmp/a8-5.png",
            1:"/tmp/a10-1.png",2:"/tmp/a10-2.png",3:"/tmp/a10-3.png",4:"/tmp/a10-4.png",5:"/tmp/a10-5.png",6:"/tmp/a10-6.png"}
S = 3300/792.0  # rendered px per PDF point (y)

def sample(pt_x, pt_y):
    per = 792.0
    pgnum = int(pt_y // per) + 1
    yy = pt_y - (pgnum-1)*per
    px = int(pt_x * S)
    py = int((per - yy) * S)
    png = rendered[pgnum]
    im = Image.open(png).convert("RGB")
    W,H = im.size
    # sample a small 5x5 block around the computed point, take the most saturated pixel
    best=(0,0,0); bestsat=-1
    cx=min(max(px,W-1),W-1); cy=min(max(py,H-1),H-1)
    for dy in range(-6,7):
        for dx in range(-6,7):
            x=min(max(cx+dx,0),W-1); y=min(max(cy+dy,0),H-1)
            r,g,b=im.getpixel((x,y))
            sat=max(r,g,b)-min(r,g,b)
            if sat>bestsat:
                bestsat=sat; best=(r,g,b)
    return png, px, py, best, bestsat

anchors = {
 "a8-amber(length)": (259.278685,857.376297,390.612924,902.875309),
 "a8-indigo(Lot sep)": (378.158379,1888.613782,590.291317,1934.080294),
 "a8-indigo(lift)": (442.767076,1954.237357,499.977524,1999.703870),
}
for name,(x0,y0,x1,y1) in anchors.items():
    cx=(x0+x1)/2; cy=(y0+y1)/2
    png,px,py,rgb,sat = sample(cx, cy)
    print(f"{name}: page={png.split('-')[-1]}, px=({px},{py}), rgb={rgb} sat={sat}")
