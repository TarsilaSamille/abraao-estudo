from PIL import Image
from collections import Counter

def dominant(png, x1p,y1p,x2p,y2p, label, sat_min=40):
    im=Image.open(png).convert("RGB"); W,H=im.size
    crop=im.crop((int(W*x1p/100),int(H*y1p/100),int(W*x2p/100),int(H*y2p/100)))
    crop.save(f"/tmp/r_{label}.png")
    px=crop.load(); w,h=crop.size
    c=Counter()
    for yy in range(h):
        for xx in range(w):
            r,g,b=px[xx,yy]
            sat=max(r,g,b)-min(r,g,b)
            if sat<sat_min: continue
            if r>235 and g>235 and b>235: continue
            if r<40 and g<40 and b<40: continue
            c[(r//16*16,g//16*16,b//16*16)]+=1
    print(f"[{label}] top:", ", ".join(f"#{br:02x}{bg:02x}{bb:02x}x{n}" for (br,bg,bb),n in c.most_common(6)))

# sessao-4 Covenant Round 1 box (red/maroon per vision), page 1 render = s4-01.png
dominant("/tmp/s4-01.png", 43.5,53.5,53.0,62.0, "s4_cov")
