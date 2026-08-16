from PIL import Image

# Bera box at yMin=1389 (page 2 cumulative). page height 792 => page2, offset y=1389-792=597
# rendered 3300px / 792pt = 4.1667
S=3300/792.0
im=Image.open("/tmp/a10-2.png").convert("RGB"); W,H=im.size
# text "Bera" box: xMin 150 xMax 263 yMin 1389 yMax 1442 => page2 local y = 597..650
x0=int(150*S); x1=int(263*S); y0=int((792-650)*S); y1=int((792-597)*S)
# crop a bit wider to catch left/right border of the box
crop=im.crop((max(0,x0-40), max(0,y0-40), min(W,x1+40), min(H,y1+40)))
crop.save("/tmp/s10_bera_box.png")
px=crop.load(); w,h=crop.size
from collections import Counter
c=Counter()
for yy in range(h):
    for xx in range(w):
        r,g,b=px[xx,yy]
        sat=max(r,g,b)-min(r,g,b)
        if sat<60: continue
        if r>235 and g>235 and b>235: continue
        if r<40 and g<40 and b<40: continue
        c[(r//16*16,g//16*16,b//16*16)]+=1
print("s10 Bera box border colors top:")
for (br,bg,bb),n in c.most_common(8):
    print(f"  #{br:02x}{bg:02x}{bb:02x} x{n}")
