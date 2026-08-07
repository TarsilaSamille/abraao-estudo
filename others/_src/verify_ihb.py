import sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8411/intro-hebrew-bible"
# path, expected_imgs
pages = [
    ("modulo-2/sessao-10.html", 2),
    ("modulo-3/sessao-11.html", 2),
    ("modulo-3/sessao-12.html", 2),
    ("modulo-3/sessao-13.html", 1),
    ("modulo-3/sessao-14.html", 2),
]

results = []
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 720, "height": 2400})
    errors = []
    pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errors.append("PAGEERR: " + str(e)))
    for path, expect in pages:
        pg.goto(f"{BASE}/{path}", wait_until="networkidle")
        pg.wait_for_timeout(700)
        imgs = pg.evaluate("() => Array.from(document.images).map(i => i.complete && i.naturalWidth>0)")
        pt = pg.evaluate("() => getComputedStyle(document.querySelector('.lang-pt')).display")
        en = pg.evaluate("() => getComputedStyle(document.querySelector('.lang-en')).display")
        pg.click("#lang-en"); pg.wait_for_timeout(250)
        en_t = pg.evaluate("() => getComputedStyle(document.querySelector('.lang-en')).display")
        pt_t = pg.evaluate("() => getComputedStyle(document.querySelector('.lang-pt')).display")
        pg.click("#lang-pt"); pg.wait_for_timeout(150)
        ok = sum(1 for x in imgs if x)
        verdict = "OK" if (ok == expect and pt!="none" and en=="none" and en_t!="none" and pt_t=="none") else "FAIL"
        results.append((path, verdict, f"{ok}/{expect}", f"PTd={pt} ENd={en} ENt={en_t} PTt={pt_t}"))
    b.close()

print("=== AD-HOC VERIFY (S10-S14) ===")
for path, v, img, d in results:
    print(f"{v:4} {path:30} imgs {img:6} {d}")
print(f"JS errors: {len(errors)}")
for e in errors[:8]:
    print("  ERR:", e)
