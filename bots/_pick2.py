#!/usr/bin/env python3
import subprocess
IMG="/Users/macbook/Library/Application Support/Hermes/composer-images/composer_2026-08-14_18-23-23-084_6f04e8.png"
pts={"RED":(520,200),"GREEN":(110,200),"BLUE":(425,200),"GREY":(325,200)}
for name,(x,y) in pts.items():
    x1,y1=x-8,y-8
    out=subprocess.run(["convert",IMG,"-crop","16x16+%d+%d"%(x1,y1),"-resize","1x1","-format","%[pixel:p{0,0}]","info:"],
                        capture_output=True,text=True).stdout.strip()
    # out ex: srgb(175,82,103) ou srgba(...)
    import re
    m=re.search(r"\((\d+),(\d+),(\d+)",out)
    if m:
        r,g,b=int(m.group(1)),int(m.group(2)),int(m.group(3))
        print(name,"#%02x%02x%02x"%(r,g,b),"at",(x,y))
    else:
        print(name,"RAW:",out)
