import fitz, re, os, json

ROOT = "/Users/macbook/Documents/GitHub/abraao-estudo"
COURSES = ["heaven-and-earth","adam-to-noah","jacob","joseph","exodus-overview",
 "ezekiel","jonah","messianic-torah","1-corinthians","ephesians",
 "intro-hebrew-bible","art-of-biblical-words"]

def largest_image_on_page(doc, page):
    imgs = page.get_images(full=True)
    best = None; best_area = 0
    for img in imgs:
        xref = img[0]
        try:
            base = doc.extract_image(xref)
        except Exception:
            continue
        w, h = base.get("width", 0), base.get("height", 0)
        area = w * h
        if area > best_area:
            best_area = area; best = base
    return best

report = {}
for slug in COURSES:
    doc = fitz.open(os.path.join(ROOT, slug, f"{slug}-teacher-notes.pdf"))
    outdir = os.path.join(ROOT, slug, "image")
    os.makedirs(outdir, exist_ok=True)
    found = []
    for i in range(doc.page_count):
        t = doc[i].get_text()
        m = re.search(r'Module\s+(\d+)', t, re.I)
        sr = re.search(r'SESSIONS?\s+\d+\s*[-–]\s*\d+|SESSIONS?\s+\d+\s*$', t, re.I)
        if m and sr:
            num = int(m.group(1))
            if any(f[0] == num for f in found):
                continue  # first divider page per module wins
            base = largest_image_on_page(doc, doc[i])
            if base:
                ext = base["ext"]
                path = os.path.join(outdir, f"img-{num}.{ext}")
                with open(path, "wb") as f:
                    f.write(base["image"])
                found.append((num, i, f"img-{num}.{ext}", base.get("width"), base.get("height")))
    doc.close()
    report[slug] = found
    print(f"{slug}: {len(found)} module images -> {[f'{n}:{fn}' for n,_,fn,_,_ in found]}")

json.dump(report, open("/tmp/module_images.json","w"), indent=1)
print("DONE")
