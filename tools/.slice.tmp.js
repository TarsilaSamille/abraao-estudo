const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [htmlArg, outDir] = process.argv.slice(2);
  const b = await chromium.launch({ channel: 'chrome' });
  const p = await b.newPage({ viewport: { width: 1400, height: 1100 } });
  await p.goto('file://' + path.resolve(htmlArg), { waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(2500);
  const h = await p.evaluate(() => document.documentElement.scrollHeight);
  const STEP = 1100, OVERLAP = 60;
  let i = 1, y = 0;
  while (y < h) {
    await p.evaluate(v => window.scrollTo(0, v), y);
    await p.waitForTimeout(350);
    const n = String(i++).padStart(2, '0');
    await p.screenshot({ path: path.join(outDir, `html-${n}.png`) });
    y += STEP - OVERLAP;
  }
  console.log('altura total', h, 'fatias', i - 1);
  await b.close().catch(() => {});
})();
