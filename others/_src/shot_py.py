import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1]
out = sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 720, "height": 2400})
    pg.goto(url, wait_until="networkidle")
    pg.wait_for_timeout(1500)
    imgs = pg.evaluate("() => Array.from(document.images).map(i => ({src: i.currentSrc.split('/').pop(), ok: i.complete && i.naturalWidth>0, w: i.naturalWidth}))")
    pg.screenshot(path=out, full_page=True)
    b.close()
    print("IMAGES:", imgs)
