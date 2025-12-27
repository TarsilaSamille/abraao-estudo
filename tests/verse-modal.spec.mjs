import { chromium } from 'playwright';

const BASE = 'http://localhost:8000/abraao/modulo-3/sessao-15.html';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  page.on('console', msg => console.log('[console]', msg.type(), msg.text()));
  await page.goto(BASE, { waitUntil: 'domcontentloaded' });
  // Click first verse-link
  const link = page.locator('a.verse-link').first();
  await link.click();
  // Wait for modal to open
  await page.waitForSelector('#verse-modal:not(.hidden)', { timeout: 8000 });
  const title = await page.locator('#modal-title').innerText();
  const content = await page.locator('#modal-content').innerText();
  console.log('Modal title:', title);
  console.log('Modal content snippet:', content.slice(0, 200));
  await browser.close();
})();
