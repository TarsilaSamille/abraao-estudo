from PIL import Image
from collections import Counter

def dominant_fill_of_crop(png, x1p, y1p, x2p, y2p):
    im = Image.open(png).convert("RGB")
    W,H = im.size
    x1=int(W*x1p/100); y1=int(H*y1p/100); x2=int(W*x2p/100); y2=int(H*y2p/100)
    crop = im.crop((x1,y1,x2,y2))
    buckets=Counter()
    px=crop.load(); w,h=crop.size
    for yy in range(h):
        for xx in range(w):
            r,g,b=px[xx,yy]
            sat=max(r,g,b)-min(r,g,b)
            if sat<40: continue
            if r>235 and g>235 and b>235: continue
            if r<40 and g<40 and b<40: continue
            buckets[(r//16*16,g//16*16,b//16*16)]+=1
    if not buckets: return None,0
    (br,bg,bb),n=buckets.most_common(1)[0]
    return f"#{br:02x}{bg:02x}{bb:02x}", n

jobs = [
 ("a8-amber","/tmp/a8-1.png",35.5,60.5,69.5,62.5),
 ("a8-indigo","/tmp/a8-1.png",52.0,65.5,59.0,67.0),
]
for name,png,x1,y1,x2,y2 in jobs:
    col,n=dominant_fill_of_crop(png,x1,y1,x2,y2)
    print(f"{name}: {col} (px={n})")
