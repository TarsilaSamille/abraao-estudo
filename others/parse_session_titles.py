import fitz, re, os, json

ROOT = "/Users/macbook/Documents/GitHub/abraao-estudo"
COURSES = ["heaven-and-earth","adam-to-noah","jacob","joseph","exodus-overview",
 "ezekiel","jonah","messianic-torah","1-corinthians","ephesians",
 "intro-hebrew-bible","art-of-biblical-words"]

def get_modules(doc):
    """Return list of (num, first_sess, last_sess) from divider pages."""
    mods = {}
    for i in range(doc.page_count):
        t = doc[i].get_text()
        m = re.search(r'Module\s+(\d+)', t, re.I)
        sr = re.search(r'SESSIONS?\s+(\d+)\s*[-–]\s*(\d+)|SESSIONS?\s+(\d+)\s*$', t, re.I)
        if m and sr:
            n = int(m.group(1))
            if n in mods: continue
            if sr.group(3):
                first = last = int(sr.group(3))
            else:
                first, last = int(sr.group(1)), int(sr.group(2))
            mods[n] = (first, last)
    return [mods[k] for k in sorted(mods)]

def get_sessions(doc):
    """Return dict sess_num -> title from 'Session N: Title' lines (divider + intro pages)."""
    sess = {}
    for i in range(doc.page_count):
        t = doc[i].get_text()
        for line in t.split('\n'):
            m = re.match(r'\s*Session\s+(\d+):\s*(.+)', line, re.I)
            if m:
                n = int(m.group(1))
                title = m.group(2).strip()
                # drop trailing "Class Notes" fragments
                title = re.sub(r'\s*Class Notes:.*$', '', title).strip()
                if n not in sess and title:
                    sess[n] = title
    return sess

out = {}
for slug in COURSES:
    doc = fitz.open(os.path.join(ROOT, slug, f"{slug}-teacher-notes.pdf"))
    mods = get_modules(doc)
    sess = get_sessions(doc)
    out[slug] = {"modules": mods, "sessions": sess}
    doc.close()
    print(f"{slug}: {len(mods)} modules, {len(sess)} session titles")

json.dump(out, open("/tmp/session_titles.json","w"), ensure_ascii=False, indent=1)
print("WROTE /tmp/session_titles.json")
