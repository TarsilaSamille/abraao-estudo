#!/usr/bin/env python3
"""Build a <table class="md"> from a teacher-notes PDF table, using text blocks (one block = one cell).
Usage: python3 _build_tbl.py <course> <title> [ncols=2]
Wraps colored words via per-block hl class (whole cell tinted if block has colored spans).
Header = block(s) containing the title. Footer ("Created by...") excluded.
"""
import sys, os, glob, html
import fitz

COURSES = {
 'adam-to-noah':'adam-to-noah/adam-to-noah-teacher-notes.pdf',
 'exodus-overview':'exodus-overview/exodus-overview-teacher-notes.pdf',
 'joseph':'joseph/joseph-teacher-notes.pdf',
 'messianic-torah':'messianic-torah/messianic-torah-teacher-notes.pdf',
 'ezekiel':'ezekiel/ezekiel-teacher-notes.pdf',
 'art-of-biblical-words':'art-of-biblical-words/art-of-biblical-words-teacher-notes.pdf',
}
def hl(hexcol):
    c=hexcol.lower()
    return {'#713c92':'hl-rose','#972a4e':'hl-rose','#f9e3de':'hl-rose',
            '#645537':'hl-tan','#fae3c3':'hl-tan','#2b6146':'hl-grn','#d3f1cc':'hl-grn',
            '#404ba6':'hl-sky','#d9ecfd':'hl-sky','#b4533a':'hl-brick'}.get(c)

def block_hl(block, page):
    # find a colored word within this block's y-range
    d=page.get_text("dict")
    y0,y1=block[1],block[3]
    for b in d["blocks"]:
        for l in b.get("lines",[]):
            for s in l.get("spans",[]):
                if y0-1<=s["bbox"][1]<=y1+1 and hl(hex(s["color"])):
                    return hl(hex(s["color"]))
    return None

def build(course, title, ncols=2):
    pdf=COURSES.get(course)
    if not pdf or not os.path.exists(pdf):
        g=glob.glob(f'{course}/*teacher-notes.pdf') or glob.glob(f'{course}/**/*teacher-notes.pdf',recursive=True)
        pdf=g[0] if g else None
    doc=fitz.open(pdf)
    for pi,page in enumerate(doc):
        if title.lower() not in page.get_text().lower(): continue
        blocks=[b for b in page.get_text("blocks") if b[4].strip()]
        # isolate: from block containing title to block containing "Created by"
        start=None
        for i,b in enumerate(blocks):
            if title.lower() in b[4].lower(): start=i; break
        end=len(blocks)
        if start is not None:
            for i in range(start+1,len(blocks)):
                if 'created by tim mackie' in blocks[i][4].lower():
                    end=i; break
        tbl=blocks[start:end]
        if not tbl: return "<!-- empty -->"
        # x column bands
        xs=[(b[0]+b[2])/2 for b in tbl]
        minx,maxx=min(xs),max(xs)
        def colof(b):
            xc=(b[0]+b[2])/2
            return min(ncols-1,int((xc-minx)/(maxx-minx+1e-9)*ncols))
        # header = first block (contains title)
        header=tbl[0]
        def cell(b,th=False):
            txt=html.escape(b[4].strip())
            c=block_hl(b,page)
            return (f'<span class="{c}">{txt}</span>' if c else txt)
        # body rows: split by column, pair by index (comparison tables have equal row counts)
        body=tbl[1:]
        def yc(b): return (b[1]+b[3])/2
        def colof_b(b):
            xc=(b[0]+b[2])/2
            return min(ncols-1,int((xc-minx)/(maxx-minx+1e-9)*ncols))
        # merge continuation fragments (colored text split into separate blocks)
        merged=[]
        for b in sorted(body,key=lambda b:(colof_b(b),yc(b))):
            t=b[4].strip()
            if merged and colof_b(merged[-1])==colof_b(b) and t and t[0].islower() and merged[-1][4].strip()[-1] not in '.!?":)':
                p=merged[-1]
                merged[-1]=(p[0],p[1],max(p[2],b[2]),max(p[3],b[3]),p[4].rstrip()+"\n"+t,p[5],p[6])
            else:
                merged.append(b)
        body=merged
        cols=[[],[],[],[],[]]
        for b in body: cols[colof_b(b)].append(b)
        for i in range(ncols):
            cols[i].sort(key=yc)
        nrows=max(len(c) for c in cols)
        out=["<table class=\"md reveal\">"]
        if "\n" in header[4] and ncols>1:
            hparts=[html.escape(p.strip()) for p in header[4].split("\n") if p.strip()]
            out.append("  <tr>"+"".join(f"<th>{h}</th>" for h in hparts[:ncols])+"</tr>")
        else:
            out.append("  <tr>"+"".join(f"<th>{cell(b)}</th>" for b in [header])+"</tr>")
        for r in range(nrows):
            tds=[]
            for i in range(ncols):
                b=cols[i][r] if r<len(cols[i]) else None
                tds.append(f"<td>{cell(b) if b else ''}</td>")
            out.append("  <tr>"+"".join(tds)+"</tr>")
        out.append("</table>")
        return "\n".join(out)
    return "<!-- NO MATCH -->"

if __name__=='__main__':
    course=sys.argv[1]; title=sys.argv[2]
    ncols=int(sys.argv[3]) if len(sys.argv)>3 else 2
    print(build(course,title,ncols))
