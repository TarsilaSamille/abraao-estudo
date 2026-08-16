from PIL import Image
# Sample pixels behind each "Negev" word to see if there's a colored fill
S=3300/792.0
rendered={i:f"/tmp/s5-{i:02d}.png" for i in range(1,13)}
# (xMin,yMin,xMax,yMax) from bbox above
occ=[
 (1385.600158,2141.711030,1522.490330,2187.210043),
 (659.386968,810.489568,796.277235,855.988580),
 (478.235552,1832.337268,615.125819,1877.836280),
 (1226.119725,1832.337268,1363.009991,1877.836280),
 (1976.735035,1832.337268,2113.625302,1877.836280),
 (1770.777801,2013.583334,1902.724464,2059.082346),
]
for i,(x0,y0,x1,y1) in enumerate(occ):
    per=792.0
    pg=int(y0//per)+1
    yy=y0-(pg-1)*per
    cx=int((x0+x1)/2*S); cy=int((per-yy)/2*S + (per-yy)/2*S)  # wrong; recompute
    # center of box
    cyy=int((per - (y0+y1)/2 + (pg-1)*per)*S)
    cx2=int((x0+x1)/2*S)
    png=rendered[pg]
    im=Image.open(png).convert("RGB"); W,H=im.size
    # sample a 3x3 around center
    rgbs=[]
    for dy in (-2,0,2):
        for dx in (-2,0,2):
            x=min(max(cx2+dx,0),W-1); y=min(max(cyy+dy,0),H-1)
            rgbs.append(im.getpixel((x,y)))
    print(f"occ{i} pg{pg} center=({cx2},{cyy}) samples={rgbs}")
