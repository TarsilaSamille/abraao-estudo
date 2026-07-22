const { chromium } = require('/Users/macbook/.hermes/hermes-agent/apps/desktop/node_modules/playwright');
(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox','--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 1100, height: 1600 } });
  const url = process.argv[2] || 'http://localhost:8080/modulo-3/sessao-15.html';
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 }).catch(e=>console.error('goto warn:', e.message));
  await page.waitForTimeout(1500);
  const out = process.argv[3] || '/tmp/shot-s15.png';
  await page.screenshot({ path: out, fullPage: true });
  console.log('screenshot saved:', out);
  await browser.close();
})();
