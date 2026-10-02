const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [html, topSel, botSel, out] = process.argv.slice(2);
  const b = await chromium.launch({ channel: 'chrome' });
  const p = await b.newPage({ viewport: { width: 1400, height: 1100 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(html), { waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(2200);
  const box = async s => { const e = await p.$(s); return e ? await e.boundingBox() : null; };
  const a = await box(topSel), z = await box(botSel);
  if (!a || !z) { console.error('sel nao achado', !!a, !!z); process.exit(1); }
  await p.screenshot({ path: out, clip: { x: a.x - 10, y: a.y - 6, width: a.width + 20, height: (z.y + z.height) - a.y + 12 } });
  console.log('ok', out);
  await b.close().catch(()=>{});
})();
