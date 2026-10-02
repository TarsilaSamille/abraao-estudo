/**
 * .shot.tmp.js — full-page screenshot helper used by compare_session.py --render.
 *
 * compare_session.py writes .collect.tmp.js itself but referenced this file
 * without ever creating it, so `--render` silently produced only the PDF PNGs.
 * Kept as a dotfile to match that convention; delete after use.
 *
 * Usage: node tools/.shot.tmp.js <abs html path> <out dir>
 * Run from the repo root so `require('playwright')` resolves from node_modules.
 */
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [htmlArg, outDir] = process.argv.slice(2);
  if (!htmlArg || !outDir) {
    console.error('usage: node tools/.shot.tmp.js <abs html> <out dir>');
    process.exit(2);
  }
  const browser = await chromium.launch({ channel: 'chrome' });
  try {
    const page = await browser.newPage({
      viewport: { width: 1400, height: 1000 },
      deviceScaleFactor: 1,
    });
    await page.goto('file://' + path.resolve(htmlArg), { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2500);
    await page.screenshot({ path: path.join(outDir, 'html.png'), fullPage: true });
  } finally {
    await browser.close().catch(() => {});
  }
  process.exit(0);
})();