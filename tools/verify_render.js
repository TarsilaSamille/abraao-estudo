/**
 * verify_render.js — headless render check for a session page.
 *
 * Catches the regressions that a static audit cannot see: horizontal overflow,
 * JavaScript errors, and diagram content clipped by a scale-to-fit viewport.
 *
 * Usage: node tools/verify_render.js <file.html> [more.html ...]
 * Run from the repo root (playwright is a local dependency).
 */
const { chromium } = require('playwright');
const path = require('path');

const files = process.argv.slice(2);
if (!files.length) {
  console.error('usage: node tools/verify_render.js <file.html> [...]');
  process.exit(2);
}

(async () => {
  const browser = await chromium.launch({ channel: 'chrome' });
  let bad = 0;

  for (const f of files) {
    const abs = path.resolve(f);
    const page = await browser.newPage({ viewport: { width: 1400, height: 1000 } });
    const errs = [];
    page.on('pageerror', e => errs.push(String(e)));
    page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });

    try {
      await page.goto('file://' + abs, { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(2200);

      const r = await page.evaluate(() => {
        const clipped = [...document.querySelectorAll('.diagram-viewport')]
          .map((vp, i) => ({ i, over: vp.scrollWidth - vp.clientWidth }))
          .filter(x => x.over > 1);
        // any element whose content is taller/wider than a clipping box
        const cut = [...document.querySelectorAll('.diagram-canvas *, .mbox, .cx')]
          .filter(e => {
            const cs = getComputedStyle(e);
            return cs.overflow === 'hidden' && e.clientHeight > 0 &&
                   e.scrollHeight > e.clientHeight + 2;
          })
          .map(e => (e.getAttribute('class') || '').slice(0, 60));
        return {
          docSW: document.documentElement.scrollWidth,
          docCW: document.documentElement.clientWidth,
          clipped, cutN: cut.length, cut: cut.slice(0, 4),
          h: document.documentElement.scrollHeight,
        };
      });

      const probs = [];
      if (r.docSW > r.docCW) probs.push(`scroll horizontal ${r.docSW}>${r.docCW}`);
      if (errs.length) probs.push(`erros JS: ${errs.slice(0, 2).join(' | ')}`);
      if (r.clipped.length) probs.push(`diagrama cortado: ${JSON.stringify(r.clipped)}`);
      if (r.cutN) probs.push(`${r.cutN} caixa(es) com texto cortado: ${r.cut.join(' ; ')}`);

      if (probs.length) {
        bad++;
        console.log(`FALHA  ${f}`);
        probs.forEach(p => console.log(`         ${p}`));
      } else {
        console.log(`ok     ${f}  (h=${r.h}px)`);
      }
    } catch (e) {
      bad++;
      console.log(`ERRO   ${f}: ${e.message.split('\n')[0]}`);
    }
    await page.close();
  }

  await browser.close().catch(() => {});
  console.log(`\n${files.length - bad}/${files.length} ok`);
  process.exit(bad ? 1 : 0);
})();
