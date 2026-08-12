// Verify all sessao-*.html: catches JS errors and truly-empty pages.
// Usage: node verify-sessions.js [root-dir]
// Exit 1 if any session is broken (CI-friendly); 0 if all OK.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = process.argv[2] ? path.resolve(process.argv[2]) : __dirname;

function walk(dir, acc = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) { if (e.name === 'node_modules' || e.name === '.git') continue; walk(p, acc); }
    else if (/sessao-.*\.html$/.test(e.name)) acc.push(p);
  }
  return acc;
}

(async () => {
  const files = walk(ROOT);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const broken = [];
  let checked = 0;
  for (const f of files) {
    const errs = [];
    const h = e => errs.push(String(e));
    page.on('pageerror', h);
    try {
      await page.goto('file://' + f, { waitUntil: 'load', timeout: 15000 });
      await page.waitForTimeout(100);
      const bodyText = await page.evaluate(() => (document.body.innerText || '').replace(/\s+/g, ' ').trim().length);
      const course = path.relative(ROOT, f).split(path.sep)[0];
      if (errs.length) broken.push({ course, f, reason: 'JS-error: ' + errs[0].slice(0, 90) });
      else if (bodyText < 50) broken.push({ course, f, reason: 'empty: bodyText=' + bodyText });
    } catch (e) {
      broken.push({ course: path.relative(ROOT, f).split(path.sep)[0], f, reason: 'goto/err: ' + e.message.slice(0, 90) });
    } finally { page.off('pageerror', h); }
    checked++;
  }
  await browser.close();

  if (broken.length === 0) {
    console.log(`OK — ${checked} sessions, 0 broken across all courses.`);
    process.exit(0);
  }
  const byCourse = {};
  for (const b of broken) (byCourse[b.course] = byCourse[b.course] || []).push(b);
  console.log(`BROKEN ${broken.length}/${checked}:`);
  for (const c of Object.keys(byCourse).sort()) {
    console.log(`\n${c} (${byCourse[c].length}):`);
    for (const b of byCourse[c]) console.log(`  ${path.basename(b.f)} :: ${b.reason}`);
  }
  process.exit(1);
})().catch(e => { console.error('FATAL', e.message); process.exit(2); });
