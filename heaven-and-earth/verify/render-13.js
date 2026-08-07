
    const { chromium } = require('/Users/macbook/GitHub/biblia-estudo/node_modules/playwright');
    (async () => {
      const browser = await chromium.launch();
      const page = await browser.newPage({ viewport: { width: 935, height: 1200 } });
      await page.goto('file:///Users/macbook/GitHub/biblia-estudo/heaven-and-earth/modulo-3/sessao-13.html', { waitUntil: 'networkidle' });
      await page.evaluate(() => { document.documentElement.lang='pt'; document.querySelectorAll('.reveal').forEach(e=>e.classList.add('visible')); });
      await page.waitForTimeout(400);
      await page.pdf({ path: '/Users/macbook/GitHub/biblia-estudo/heaven-and-earth/verify/html-s13.pdf', printBackground: true, format: 'A4', preferCSSPageSize: false });
      await browser.close();
    })();
    