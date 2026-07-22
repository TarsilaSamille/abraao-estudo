import fitz, re, json, os

ROOT = "/Users/macbook/Documents/GitHub/abraao-estudo"
# folder -> pdf slug base (folder name matches pdf file prefix)
MISSING = ["jonah","messianic-torah","1-corinthians","ephesians","intro-hebrew-bible","art-of-biblical-words"]

def parse(folder):
    doc = fitz.open(os.path.join(ROOT, folder, f"{folder}-teacher-notes.pdf"))
    mods = {}
    for i in range(doc.page_count):
        t = doc[i].get_text()
        # Module divider pages contain: "Module N: <title...>" then "SESSIONS X-Y" then description
        # Join wrapped lines
        raw = [l.strip() for l in t.split("\n") if l.strip()]
        for j, l in enumerate(raw):
            m = re.match(r'Module\s+(\d+):\s*(.*)', l, re.I)
            if not m:
                continue
            num = int(m.group(1))
            # gather title until we hit SESSIONS marker
            title_parts = [m.group(2)] if m.group(2) else []
            sess_range = None
            desc = ""
            k = j + 1
            while k < len(raw) and k < j + 8:
                s = raw[k]
                sr = re.match(r'SESSIONS?\s+(\d+)\s*[-–]\s*(\d+)', s, re.I)
                sr1 = re.match(r'SESSIONS?\s+(\d+)\s*$', s, re.I)
                if sr:
                    sess_range = (int(sr.group(1)), int(sr.group(2)))
                    # description is the next line(s)
                    if k+1 < len(raw):
                        desc = raw[k+1]
                    break
                elif sr1:
                    sess_range = (int(sr1.group(1)), int(sr1.group(1)))
                    if k+1 < len(raw):
                        desc = raw[k+1]
                    break
                elif re.match(r'Session\s+\d+', s, re.I):
                    break
                else:
                    title_parts.append(s)
                k += 1
            if sess_range:  # only keep divider pages (they have SESSIONS X-Y)
                title = " ".join(title_parts).strip()
                title = re.sub(r'\s+', ' ', title)
                if num not in mods or (not mods[num].get("desc") and desc):
                    mods[num] = {"pos": num, "title": title, "first": sess_range[0],
                                 "last": sess_range[1], "n": sess_range[1]-sess_range[0]+1, "desc": desc}
    doc.close()
    return [mods[k] for k in sorted(mods)]

out = {}
for f in MISSING:
    out[f] = parse(f)
    print(f"### {f}")
    for m in out[f]:
        print(f"   M{m['pos']} S{m['first']}-{m['last']}: {m['title']}")
    print()

json.dump(out, open("/tmp/pdf_modules.json","w"), ensure_ascii=False, indent=2)
print("WROTE /tmp/pdf_modules.json")
