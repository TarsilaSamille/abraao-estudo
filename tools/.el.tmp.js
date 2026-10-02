const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [html, sel, out] = process.argv.slice(2);
  const b = await chromium.launch({ channel: 'chrome' });
  const p = await b.newPage({ viewport: { width: 1400, height: 1100 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(html), { waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(2200);
  const el = await p.$(sel);
  if (!el) { console.error('sel nao achado:', sel); process.exit(1); }
  await el.screenshot({ path: out });
  console.log('ok', out);
  await b.close().catch(()=>{});
})();
