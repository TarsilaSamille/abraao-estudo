from PIL import Image
from collections import Counter

def top_colors(png, x1p,y1p,x2p,y2p, label):
    im = Image.open(png).convert("RGB"); W,H=im.size
    crop=im.crop((int(W*x1p/100),int(H*y1p/100),int(W*x2p/100),int(H*y2p/100)))
    crop.save(f"/tmp/crop_{label}.png")
    px=crop.load(); w,h=crop.size
    c=Counter()
    for yy in range(crop.size[1]):
        for xx in range(crop.size[0]):
            r,g,b=px[xx,yy]
            c[(r//16*16,g//16*16,b//16*16)]+=1
    print(f"[{label}] top:", ", ".join(f"#{br:02x}{bg:02x}{bb:02x}x{n}" for (br,bg,bb),n in c.most_common(5)))

# verse 16 indigo pill per vision note
top_colors("/tmp/a8-1.png",26.0,67.5,33.0,69.0,"indigo_v16")
# verse 15c wider
top_colors("/tmp/a8-1.png",50.0,64.5,61.0,68.0,"indigo_v15c_wide")
