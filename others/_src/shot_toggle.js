const { chromium } = require('/Users/macbook/.hermes/hermes-agent/apps/desktop/node_modules/playwright');
(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox','--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 760, height: 1000 } });
  const url = process.argv[2];
  const out = process.argv[3];
  const lang = process.argv[4]; // 'en' or 'pt'
  await page.goto(url, { waitUntil: 'networkidle' });
  if (lang === 'en') {
    await page.click('#lang-en-btn');
  } else {
    await page.click('#lang-pt-btn');
  }
  await page.waitForTimeout(400);
  // also dump which content is visible
  const visible = await page.evaluate(() => {
    const en = document.querySelector('.lang-en');
    const pt = document.querySelector('.lang-pt');
    return {
      enHidden: en.classList.contains('hidden'),
      ptHidden: pt.classList.contains('hidden'),
      enBtnBg: document.getElementById('lang-en-btn').className,
      ptBtnBg: document.getElementById('lang-pt-btn').className
    };
  });
  await page.screenshot({ path: out, fullPage: true });
  console.log(JSON.stringify(visible));
  await browser.close();
})();
