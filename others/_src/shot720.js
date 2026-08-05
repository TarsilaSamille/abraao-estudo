const { chromium } = require('/Users/macbook/GitHub/biblia-estudo/node_modules/playwright');
(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox','--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 720, height: 2400 } });
  await page.goto(process.argv[2], { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: process.argv[3], fullPage: true });
  await browser.close();
  console.log('saved', process.argv[3]);
})();
