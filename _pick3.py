from PIL import Image
from collections import Counter

im = Image.open("/tmp/a8-1.png").convert("RGB")
W,H = im.size
x1=int(W*52.0/100); y1=int(H*65.5/100); x2=int(W*59.0/100); y2=int(H*67.0/100)
crop = im.crop((x1,y1,x2,y2))
crop.save("/tmp/indigo_crop.png")
px=crop.load(); w,h=crop.size
c=Counter()
for yy in range(h):
    for xx in range(w):
        r,g,b=px[xx,yy]
        c[(r//16*16,g//16*16,b//16*16)]+=1
print("top colors in indigo crop:")
for (br,bg,bb),n in c.most_common(8):
    print(f"  #{br:02x}{bg:02x}{bb:02x} x{n}")
