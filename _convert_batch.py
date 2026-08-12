#!/usr/bin/env python3
"""Batch: replace <img> tables in HTML with <table class="md"> built from the teacher-notes PDF.
Usage: python3 _convert_batch.py
Reads TABLES list below. For each: build HTML via _build_tbl logic, inject, add CSS if missing.
"""
import re, os, html as _html, sys
import fitz

COURSES = {
 'adam-to-noah':'adam-to-noah/adam-to-noah-teacher-notes.pdf',
 'exodus-overview':'exodus-overview/exodus-overview-teacher-notes.pdf',
 'joseph':'joseph/joseph-teacher-notes.pdf',
 'messianic-torah':'messianic-torah/messianic-torah-teacher-notes.pdf',
 'ezekiel':'ezekiel/ezekiel-teacher-notes.pdf',
 'art-of-biblical-words':'art-of-biblical-words/art-of-biblical-words-teacher-notes.pdf',
 'jacob':'jacob/jacob-teacher-notes.pdf',
}
# (course, html_path, img_basename, pdf_title, ncols)
# (course, html_path, img_basename, pdf_search_phrase, ncols, pdf_page)
TABLES = [
 ('adam-to-noah','adam-to-noah/modulo-2/sessao-14.html','p5-vector.png','Trees in Genesis',2,78),
 ('adam-to-noah','adam-to-noah/modulo-4/sessao-22.html','p3-vector.png','Poems as Summary Literary Markers',3,0),
 ('adam-to-noah','adam-to-noah/modulo-4/sessao-24.html','p1-vector.png','Translation and Literary Design of Genesis 3:20-21',3,0),
 ('adam-to-noah','adam-to-noah/modulo-5/sessao-25.html','p1-vector.png','Cain and Abel: A Tale of Two Seeds',2,0),
 ('adam-to-noah','adam-to-noah/modulo-5/sessao-28.html','p7-vector.png','Continuing the Tale of Two Seeds',3,0),
 # exodus-overview
 ('exodus-overview','exodus-overview/modulo-2/sessao-9.html','p2-vector.png','Who Is Doing What',3,28),
 ('exodus-overview','exodus-overview/modulo-2/sessao-13.html','p3-vector.png','Chiasm in the Wilderness Journeys',3,39),
 ('exodus-overview','exodus-overview/modulo-3/sessao-17.html','p2-vector.png','Textual Unity of Exodus 20',3,49),
 ('exodus-overview','exodus-overview/modulo-3/sessao-20.html','p2-vector.png','Literary Structure of the Book of the Covenant',2,57),
 # messianic-torah
 ('messianic-torah','messianic-torah/modulo-1/sessao-2.html','p3-vector.png','Sermon on the Mount',6,15),
 ('messianic-torah','messianic-torah/modulo-1/sessao-2.html','p11-vector.png','Calling All Apprentices',3,23),
 ('messianic-torah','messianic-torah/modulo-2/sessao-7.html','p3-vector.png','Intensity of Actions',4,87),
 ('messianic-torah','messianic-torah/modulo-2/sessao-9.html','p7-vector.png','Matthew 5:32',2,102),
 # ezekiel
 ('ezekiel','ezekiel/modulo-1/sessao-3.html','p1-vector.png','Genesis 1:1-2',2,11),
 ('ezekiel','ezekiel/modulo-1/sessao-3.html','p2-vector.png','Day 2 and Day 5',2,11),
 ('ezekiel','ezekiel/modulo-1/sessao-3.html','p5-vector.png','Cosmic Geography',2,23),
 ('ezekiel','ezekiel/modulo-1/sessao-3.html','p6-vector.png','Cosmic Geography',2,23),
 ('ezekiel','ezekiel/modulo-1/sessao-3.html','p13-vector.png','Tabernacle/Temple',3,23),
 ('ezekiel','ezekiel/modulo-1/sessao-4.html','p2-vector.png','Dated Superscriptions in Ezekiel',3,26),
 ('ezekiel','ezekiel/modulo-1/sessao-4.html','p3-vector.png','Dated Superscriptions in Ezekiel',3,27),
 # art-of-biblical-words
 ('art-of-biblical-words','art-of-biblical-words/modulo-1/sessao-3.html','p11-vector.png','Languages of the Hebrew Bible',2,11),
 # joseph
 ('joseph','joseph/modulo-2/sessao-6.html','p5-vector.png','Non-Chosen',3,34),
 ('joseph','joseph/modulo-2/sessao-7.html','p2-vector.png','Yaaqov, Yoseph, and a Goat',2,39),
 ('joseph','joseph/modulo-2/sessao-7.html','p3-vector.png','two stories of Abraham and Isaac',2,40),
 ('joseph','joseph/modulo-4/sessao-14.html','p2-vector.png','Silver',2,99),
 ('joseph','joseph/modulo-4/sessao-14.html','p5-vector.png','Binyamin, the New Yoseph',2,102),
 ('joseph','joseph/modulo-4/sessao-14.html','p6-vector.png','Genesis 43-45',3,104),
 ('joseph','joseph/modulo-4/sessao-14.html','p7-vector.png','Genesis 43-45',3,104),
 ('joseph','joseph/modulo-5/sessao-20.html','p3-vector.png','Parallels',2,150),
 ('joseph','joseph/modulo-5/sessao-20.html','p6-vector.png','Yoseph and Joshua, Images of Messianic Rule',3,152),
 ('joseph','joseph/modulo-6/sessao-21.html','p2-vector.png','Like Grandson, Like Grandfather',2,156),
 ('joseph','joseph/modulo-6/sessao-21.html','p3-vector.png','son of Israel',3,158),
 ('joseph','joseph/modulo-6/sessao-21.html','p6-vector.png','Pharaoh named Yoseph',2,163),
 ('joseph','joseph/modulo-6/sessao-22.html','p3-vector.png','Isaac and Yaaqov in Genesis 27',2,166),
 ('joseph','joseph/modulo-6/sessao-25.html','p5-vector.png','Yoseph is a rid',2,191),
 ('joseph','joseph/modulo-6/sessao-25.html','p8-vector.png','Symmetry in Blessing',2,193),
 ('joseph','joseph/modulo-6/sessao-25.html','p9-vector.png','The Word About Binyamin',2,194),
 ('joseph','joseph/modulo-6/sessao-25.html','p11-vector.png','Symmetry in Blessing',2,193),
 ('joseph','joseph/modulo-7/sessao-26.html','p8-vector.png','Hyperlinks to Earlier Genesis',2,204),
 ('joseph','joseph/modulo-7/sessao-28.html','p2-vector.png','Yaaqov’s Death Scene',2,213),
 ('joseph','joseph/modulo-7/sessao-28.html','p3-vector.png','Pharaoh and Yoseph in Genesis 50',2,214),
]

def hl(hexcol):
    c=hexcol.lower()
    return {'#713c92':'hl-rose','#972a4e':'hl-rose','#f9e3de':'hl-rose',
            '#645537':'hl-tan','#fae3c3':'hl-tan','#2b6146':'hl-grn','#d3f1cc':'hl-grn',
            '#404ba6':'hl-sky','#d9ecfd':'hl-sky','#b4533a':'hl-brick'}.get(c)

def build(course, title, ncols, page=0):
    doc=fitz.open(COURSES[course])
    if page:
        pages=[doc[page-1]]
    else:
        pages=[p for i,p in enumerate(doc) if title.lower() in p.get_text().lower()]
    for page in pages:
        blocks=[b for b in page.get_text("blocks") if b[4].strip()]
        start=None
        for i,b in enumerate(blocks):
            if title.lower() in b[4].lower(): start=i; break
        end=len(blocks)
        if start is not None:
            for i in range(start+1,len(blocks)):
                if 'created by tim mackie' in blocks[i][4].lower(): end=i; break
        tbl=blocks[start:end]
        if not tbl: return None
        def yc(b): return (b[1]+b[3])/2
        xs=[(b[0]+b[2])/2 for b in tbl]; minx,maxx=min(xs),max(xs)
        def colof(b):
            xc=(b[0]+b[2])/2
            return min(ncols-1,int((xc-minx)/(maxx-minx+1e-9)*ncols))
        def block_hl(b):
            d=page.get_text("dict"); y0,y1=b[1],b[3]
            for bb in d["blocks"]:
                for l in bb.get("lines",[]):
                    for s in l.get("spans",[]):
                        if y0-1<=s["bbox"][1]<=y1+1 and hl(hex(s["color"])):
                            return hl(hex(s["color"]))
            return None
        def cell(b):
            txt=_html.escape(b[4].strip()).replace("\n","<br>")
            c=block_hl(b)
            return f'<span class="{c}">{txt}</span>' if c else txt
        header=tbl[0]
        body=tbl[1:]
        merged=[]
        for b in sorted(body,key=lambda b:(colof(b),yc(b))):
            t=b[4].strip()
            if merged and colof(merged[-1])==colof(b) and t and t[0].islower() and merged[-1][4].strip()[-1] not in '.!?":)':
                p=merged[-1]; merged[-1]=(p[0],p[1],max(p[2],b[2]),max(p[3],b[3]),p[4].rstrip()+"\n"+t,p[5],p[6])
            else: merged.append(b)
        body=merged
        cols=[[] for _ in range(ncols)]
        for b in body: cols[colof(b)].append(b)
        for i in range(ncols): cols[i].sort(key=yc)
        nrows=max(len(c) for c in cols)
        out=["<table class=\"md reveal\">"]
        if "\n" in header[4] and ncols>1:
            hp=[_html.escape(p.strip()) for p in header[4].split("\n") if p.strip()]
            out.append("  <tr>"+"".join(f"<th>{h}</th>" for h in hp[:ncols])+"</tr>")
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
    return None

CSS = '''  table.md { width: 100%; border-collapse: separate; border-spacing: 0; border: 1px solid #d7dde5; border-radius: 12px; overflow: hidden; background: #fff; margin: 1.5rem 0; font-size: .92rem; }
  table.md th { background: #e3e7ec; text-align: left; padding: .8rem 1rem; font-weight: 700; color: #1b1b1b; }
  table.md td { padding: .85rem 1rem; border-top: 1px solid #e5e7eb; vertical-align: top; line-height: 1.65; color: #1b1b1b; }
  table.md td + td, table.md th + th { border-left: 1px solid #e5e7eb; }
  table.md tbody tr:hover td { background: #f8fafc; }
  .hl-tan { background: #fae3c3; color: #90362e; }
  .hl-sky { background: #d9ecfd; color: #404ba6; }
  .hl-grn { background: #d3f1cc; color: #2a6145; }
  .hl-rose { background: #f9e3de; color: #97294e; }
  .hl-brick { background: #b4533a; color: #fff; }'''

def ensure_css(t):
    if 'table.md {' in t: return t
    # insert before .table-img or before </style>
    if '.table-img {' in t:
        return t.replace('.table-img {', CSS+'\n  .table-img {',1)
    return t.replace('</style>', CSS+'\n</style>')

def convert(course, html_path, img, title, ncols, page=0):
    tbl_html=build(course,title,ncols,page)
    if not tbl_html:
        print(f"  !! build failed: {html_path} {img} ({title})"); return False
    t=open(html_path,encoding='utf-8').read()
    esc=re.escape(img)
    # match an optional wrapping div.table-img around the target <img>
    pat=re.compile(r'(<div class="table-img[^"]*"[^>]*>\s*)?<img src="[^"]*'+esc+r'"[^>]*>(.*?)(</div>)', re.S)
    m=pat.search(t)
    if not m:
        # fallback: just the img tag
        pat=re.compile(r'<img src="[^"]*'+esc+r'"[^>]*>')
        m=pat.search(t)
        if not m:
            print(f"  !! no img block: {html_path} {img}"); return False
        cap=None
        repl=tbl_html
        t=t[:m.start()]+repl+t[m.end():]
    else:
        capm=re.search(r'<p class="caption">(.*?)</p>', m.group(0), re.S)
        cap=capm.group(1) if capm else None
        repl=tbl_html + (f'\n  <p class="caption">{cap}</p>' if cap else '')
        t=t[:m.start()]+repl+t[m.end():]
    t=ensure_css(t)
    open(html_path,'w',encoding='utf-8').write(t)
    print(f"  OK: {html_path} {img} -> table ({ncols}col, {title})")
    return True

if __name__=='__main__':
    import json
    TABLES = json.load(open('/tmp/tables_all.json'))
    for c,h,img,title,n,pg in TABLES:
        convert(c,h,img,title,n,pg)
