import fitz, re, os, json

ROOT = "/Users/macbook/Documents/GitHub/abraao-estudo"

COURSES = ["heaven-and-earth","adam-to-noah","jacob","joseph","exodus-overview",
 "ezekiel","jonah","messianic-torah","1-corinthians","ephesians",
 "intro-hebrew-bible","art-of-biblical-words"]

def detect_sessions(pdf_path):
    """Return ordered list of (session_num, start_page, end_page) where end_page is exclusive
    boundary (start of next session). Uses first page containing 'Session N:' AND 'Key Takeaways'."""
    doc = fitz.open(pdf_path)
    starts = {}
    for i in range(doc.page_count):
        t = doc[i].get_text()
        for m in re.finditer(r'Session\s+(\d+)\s*:', t):
            n = int(m.group(1))
            if n not in starts and 'Key Takeaways' in t:
                starts[n] = i
    order = sorted(starts)
    out = []
    for idx, n in enumerate(order):
        a = starts[n]
        b = starts[order[idx+1]] if idx+1 < len(order) else doc.page_count
        out.append({"session": n, "page_start": a, "page_end": b})
    doc.close()
    return out

def main():
    manifest = {}
    for slug in COURSES:
        pdf = os.path.join(ROOT, slug, f"{slug}-teacher-notes.pdf")
        if not os.path.exists(pdf):
            print("MISSING", pdf); continue
        sessions = detect_sessions(pdf)
        manifest[slug] = sessions
        print(f"{slug}: {len(sessions)} sessions")
    # write per-course mapping file
    os.makedirs(os.path.join(ROOT, "others"), exist_ok=True)
    with open(os.path.join(ROOT, "others", "session_pages.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print("WROTE others/session_pages.json")

if __name__ == "__main__":
    main()
