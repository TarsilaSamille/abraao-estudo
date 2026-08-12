#!/usr/bin/env python3
"""Auto-build TABLES list: for each HTML table-img with a meaningful alt, locate it in the
course teacher-notes PDF and record (course, html, img, alt, ncols, page)."""
import re, fitz, glob, os, json
import _convert_batch as cb

def normalize(s):
    return (s.replace('’',"'").replace('“','"').replace('”','"').replace('–','-')
             .replace('×','x').replace('&','and').replace('  ',' ').strip().lower())

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
TABLES=[]
notfound=[]
for c in courses:
    doc_cache={}
    for html in sorted(glob.glob(f'{c}/**/sessao-*.html', recursive=True)):
        t=open(html,encoding='utf-8').read()
        if 'class="md reveal"' in t: continue
        for m in re.finditer(r'<div class="table-img[^"]*">(.*?)</div>', t, re.S):
            im=re.search(r'<img src="([^"]+)" alt="([^"]*)"', m.group(1))
            if not im: continue
            alt=im.group(2); base=os.path.basename(im.group(1))
            if alt.lower().startswith('page ') or 'diagram' in alt.lower():
                continue
            if c not in doc_cache:
                doc_cache[c]=fitz.open(cb.COURSES[c])
            d=doc_cache[c]
            found=None
            for i,p in enumerate(d):
                if normalize(alt) in normalize(p.get_text()):
                    found=i; break
            if found is None:
                notfound.append((html.replace(c+'/',''), base, alt))
                continue
            nc=detect_ncols(c, alt)
            if nc<2: nc=2
            TABLES.append((c, html, base, alt, nc, found+1))

json.dump(TABLES, open('/tmp/tables_auto.json','w'))
json.dump(notfound, open('/tmp/tables_notfound.json','w'))
print(f"TABLES: {len(TABLES)} | notfound: {len(notfound)}")
for h,b,a in notfound:
    print("  NF:", h, b, "|", a[:40])
