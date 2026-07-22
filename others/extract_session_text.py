import fitz, re, os, json

ROOT = "/Users/macbook/Documents/GitHub/abraao-estudo"

def extract_session(doc, sess_num, next_sess, a=None, b=None):
    if a is None:
        a = 0
    if b is None:
        b = doc.page_count
    out = []
    for i in range(a, b):
        t = doc[i].get_text()
        out.append(t)
    text = "\n".join(out)
    # keep from the session heading that precedes 'Key Takeaways'
    kt = text.find("Key Takeaways")
    if kt == -1:
        kt = len(text)
    last = -1
    for m in re.finditer(r'Session\s+%d\s*:' % sess_num, text):
        if m.start() < kt:
            last = m.start()
    if last != -1:
        text = text[last:]
    text = re.sub(r'Class Notes:[^\n]*\n\d+ of \d+\s*', '', text)
    text = re.sub(r'\nModule \d+:.*$', '', text, flags=re.S)
    return text.strip()

if __name__ == "__main__":
    doc = fitz.open(os.path.join(ROOT, "heaven-and-earth", "heaven-and-earth-teacher-notes.pdf"))
    # map session -> first page that has 'Session N:' AND 'Key Takeaways' (the real body, not TOC)
    starts = {}
    for i in range(doc.page_count):
        t = doc[i].get_text()
        for m in re.finditer(r'Session\s+(\d+)\s*:', t):
            n = int(m.group(1))
            if n not in starts and 'Key Takeaways' in t:
                starts[n] = i
    sessions_order = sorted(starts)
    for s in sessions_order:
        a = starts[s]
        # next session start
        nxt = [x for x in sessions_order if x > s]
        b = starts[nxt[0]] if nxt else doc.page_count
        txt = extract_session(doc, s, None, a, b)
        open(f"/tmp/he_session_{s}.txt","w").write(txt)
        print(f"S{s}: p{a}-{b-1} {len(txt)} chars")
    doc.close()
