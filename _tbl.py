#!/usr/bin/env python3
"""Extract a table from a course's teacher-notes PDF by title, dumping color-coded cells.
Usage: python3 _tbl.py <course> <title-substr>
Maps color codes to hl-* classes. Prints rows grouped left/right by x-center.
"""
import sys, os, glob, re
import fitz

COURSES = {
 'adam-to-noah':'adam-to-noah/adam-to-noah-teacher-notes.pdf',
 'exodus-overview':'exodus-overview/exodus-overview-teacher-notes.pdf',
 'joseph':'joseph/joseph-teacher-notes.pdf',
 'messianic-torah':'messianic-torah/messianic-torah-teacher-notes.pdf',
 'ezekiel':'ezekiel/ezekiel-teacher-notes.pdf',
 'art-of-biblical-words':'art-of-biblical-words/art-of-biblical-words-teacher-notes.pdf',
}
# color -> hl class (from PDF text colors)
def hl(hexcol):
    c = hexcol.lower()
    m = {
      '#713c92':'hl-rose', '#972a4e':'hl-rose', '#f9e3de':'hl-rose',
      '#645537':'hl-tan', '#fae3c3':'hl-tan',
      '#2b6146':'hl-grn', '#d3f1cc':'hl-grn',
      '#404ba6':'hl-sky', '#d9ecfd':'hl-sky',
      '#b4533a':'hl-brick',
    }
    return m.get(c)

def main():
    course, title = sys.argv[1], sys.argv[2]
    pdf = COURSES.get(course)
    if not pdf or not os.path.exists(pdf):
        # try glob
        g = glob.glob(f'{course}/*teacher-notes.pdf')
        if not g: g = glob.glob(f'{course}/**/*teacher-notes.pdf', recursive=True)
        if not g: print("NO PDF"); sys.exit(1)
        pdf = g[0]
    doc = fitz.open(pdf)
    for pi, page in enumerate(doc):
        t = page.get_text().lower()
        if title.lower() not in t: continue
        d = page.get_text("dict")
        print(f"=== {course} :: page {pi+1} (match '{title}') ===")
        # gather ALL spans
        allc=[]
        for b in d["blocks"]:
            for l in b.get("lines",[]):
                for s in l.get("spans",[]):
                    txt=s["text"]
                    if not txt.strip(): continue
                    bx=s["bbox"]
                    cls=hl(hex(s["color"]))
                    bold = "bold" in s["font"].lower() or s["flags"] & 2
                    allc.append((bx[0],bx[1],bx[2],bx[3],txt,cls,bold))
        # isolate table region: from the line containing title to the "Created by" footer
        ymin=None; ymax=None
        for c in allc:
            if title.lower() in c[4].lower() and ymin is None:
                ymin=c[1]
            if 'created by tim mackie' in c[4].lower() and ymin is not None:
                ymax=c[3]; break
        if ymin is None:
            print("(title not found as table header; dumping full page below)")
            ymin,ymax=-1,1e9
        cells=[c for c in allc if ymin-2 <= c[1] <= (ymax if ymax else 1e9)]
        if not cells: cells=allc
        xs=[(c[0]+c[2])/2 for c in cells]
        mid=(min(xs)+max(xs))/2 if xs else 0
        cells.sort(key=lambda c:(round(c[1]/6), c[0]))
        for c in cells:
            side = 'L' if (c[0]+c[2])/2 < mid else 'R'
            star = '*' if c[6] else ''
            print(f"{side} {round(c[1])} | {c[4]} [{c[5] or ''}{star}]")
        print()
        # also show plain text for reference
        print("PLAINTEXT:")
        print(page.get_text())
        return
    print("NO MATCH for", title)

if __name__=='__main__':
    main()
