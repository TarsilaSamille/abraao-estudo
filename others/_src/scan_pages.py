import fitz, re, os
pdf="/Users/macbook/Documents/GitHub/abraao-estudo/abraao/abraham-teacher-notes.pdf"
doc=fitz.open(pdf)
print("total pages:", doc.page_count)
print("="*60)
# Scan pages 95..120 to find session boundaries by header text
for i in range(95, 121):
    t=doc[i].get_text()
    # Look for session markers / headings (first ~200 chars, strip page numbers)
    lines=[l.strip() for l in t.splitlines() if l.strip()]
    # try to find a "Session N" or module header
    head=" | ".join(lines[:6])
    # detect page number like "103 of 230"
    pgnum=re.search(r'(\d+) of 230', t)
    pg = pgnum.group(1) if pgnum else "?"
    # detect session label
    sess=re.search(r'Session\s+(\d+)', t)
    mod=re.search(r'Module\s+(\d+)', t)
    tag=[]
    if sess: tag.append(f"SESSION {sess.group(1)}")
    if mod: tag.append(f"MOD {mod.group(1)}")
    print(f"idx{i:3} pdf{pg:>3}  {' '.join(tag) if tag else '':20} {head[:90]}")
