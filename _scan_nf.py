#!/usr/bin/env python3
"""Re-scan not-found tables WITH course prefix; try verse-ref lookup in teacher-notes.
Outputs /tmp/tables_nf2.json = list of (course, html_rel, base, alt, ref, pg|None)
and /tmp/tables_via_ref.json = (course, html_rel, base, alt, ncols, pg)."""
import re, fitz, glob, os, json
import _convert_batch as cb

def normalize(s):
    return (s.replace('’',"'").replace('“','"').replace('”','"').replace('–','-')
             .replace('×','x').replace('&','and').replace('  ',' ').strip().lower())

def verse_ref(alt):
    m=re.search(r'(?:Gênesis|Genesis|Mateus|Matthew|Êxodo|Exodus|Ezequiel|Ezekiel)\s+(\d+:\d+(?:[–-]\d+)?)', alt)
    return m.group(1) if m else None

def detect_ncols(course, phrase):
    d=fitz.open(cb.COURSES[course])
    for i,p in enumerate(d):
        if phrase.lower() in p.get_text().lower():
            bs=[b for b in p.get_text("blocks") if b[4].strip()]
            xs=[(b[0]+b[2])/2 for b in bs]
            if max(xs)-min(xs)<80: return 1
            xcs=sorted(set(round((b[0]+b[2])/2) for b in bs))
            cs=[];cur=[]
            for x in xcs:
                if cur and x-cur[-1]>70: cs.append(cur);cur=[]
                cur.append(x)
            if cur: cs.append(cur)
            return len(cs)
    return 0

courses=['adam-to-noah','exodus-overview','messianic-torah','ezekiel','joseph','art-of-biblical-words','jacob']
cache={}
all_nf=[]
for c in courses:
    d=fitz.open(cb.COURSES[c]); cache[c]=d
    for html in sorted(glob.glob(f'{c}/**/sessao-*.html', recursive=True)):
        t=open(html,encoding='utf-8').read()
        if 'class="md reveal"' in t: continue
        for m in re.finditer(r'<div class="table-img[^"]*">(.*?)</div>', t, re.S):
            im=re.search(r'<img src="([^"]+)" alt="([^"]*)"', m.group(1))
            if not im: continue
            alt=im.group(2); base=os.path.basename(im.group(1))
            if alt.lower().startswith('page ') or 'diagram' in alt.lower():
                continue
            found=False
            for i,p in enumerate(d):
                if normalize(alt) in normalize(p.get_text()):
                    found=True; break
            if found: continue
            ref=verse_ref(alt); pg=None
            if ref:
                for i,p in enumerate(d):
                    if ref in p.get_text():
                        pg=i+1; break
            all_nf.append((c, html.replace(c+'/',''), base, alt, ref, pg))

via_ref=[r for r in all_nf if r[5]]
still=[r for r in all_nf if not r[5]]
out_via=[]
for r in via_ref:
    nc=detect_ncols(r[0], r[3])
    if nc<2: nc=2
    out_via.append((r[0], r[1], r[2], r[3], nc, r[5]))
json.dump(out_via, open('/tmp/tables_via_ref.json','w'))
json.dump(still, open('/tmp/tables_still_nf.json','w'))
print(f"notfound total: {len(all_nf)} | via ref: {len(via_ref)} | still: {len(still)}")
for r in still:
    print("  STILL:", r[0], r[1], r[2], "|", r[3][:40])
