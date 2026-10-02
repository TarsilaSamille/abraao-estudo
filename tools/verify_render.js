/**
 * verify_render.js — headless render check for a session page.
 *
 * Catches the regressions that a static audit cannot see: horizontal overflow,
 * JavaScript errors, and diagram content clipped by a scale-to-fit viewport.
 *
 * Also catches UNBALANCED TAGS and COLLAPSED CONTENT. These two used to slip
 * through: the DOM silently repairs a missing </div>, so the page "renders"
 * without error — but if the unclosed element is the position:fixed nav
 * wrapper, it swallows <main> and the document collapses to one viewport
 * (h === 1000px) while every other check still passes. That shipped broken
 * pages once already, so it is checked explicitly here.
 *
 * Usage: node tools/verify_render.js <file.html> [more.html ...]
 * Run from the repo root (playwright is a local dependency).
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// Tags where an omitted end tag is invalid or changes nesting. <p> and <li>
// are deliberately excluded: HTML5 lets you omit </p> and </li>, so counting
// them would produce false failures.
const STRICT_TAGS = ['html', 'head', 'body', 'main', 'div', 'section', 'figure',
  'figcaption', 'span', 'table', 'thead', 'tbody', 'tfoot', 'tr', 'td', 'th',
  'blockquote', 'footer', 'pre', 'svg', 'h1', 'h2', 'h3', 'h4', 'ul', 'ol'];

/**
 * Raw tag-balance check on the file text, before the browser "fixes" it.
 * Returns a human string describing the first imbalance found.
 */
function tagBalanceProblem(html) {
  const src = html
    .replace(/<script\b[\s\S]*?<\/script>/gi, '')
    .replace(/<style\b[\s\S]*?<\/style>/gi, '')
    .replace(/<!--[\s\S]*?-->/g, '');
  const stack = [];
  const re = /<(\/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?(\/?)>/g;
  let m;
  while ((m = re.exec(src))) {
    const [, closing, rawTag, selfClose] = m;
    const tag = rawTag.toLowerCase();
    if (!STRICT_TAGS.includes(tag)) continue;
    if (selfClose === '/') continue;
    if (closing) {
      if (stack.length && stack[stack.length - 1] === tag) { stack.pop(); continue; }
      if (!stack.includes(tag)) return `</${tag}> sem <${tag}> correspondente`;
      return `</${tag}> fora de ordem (ainda aberto: <${stack[stack.length - 1]}>)`;
    }
    stack.push(tag);
  }
  if (stack.length) return `<${stack[stack.length - 1]}> nunca fechada (${stack.length} aberta(s))`;
  return null;
}

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
      // structural check first: cheap, and it runs before the browser can
      // silently repair the markup and hide the problem
      let balance = null;
      try { balance = tagBalanceProblem(fs.readFileSync(abs, 'utf8')); }
      catch (e) { balance = 'nao consegui ler o arquivo'; }

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
        // the real content container: <main> when the template uses it,
        // otherwise <body> — several courses wrap content in a plain
        // <div class="max-w-4xl"> with no <main> at all, so requiring <main>
        // would be a false failure.
        const main = document.querySelector('main');
        const holder = main || document.body;
        return {
          docSW: document.documentElement.scrollWidth,
          docCW: document.documentElement.clientWidth,
          clipped, cutN: cut.length, cut: cut.slice(0, 4),
          h: document.documentElement.scrollHeight,
          vh: window.innerHeight,
          textLen: (holder.innerText || '').trim().length,
          holderH: holder.getBoundingClientRect().height,
        };
      });

      const probs = [];
      if (balance) probs.push(`tags desbalanceadas: ${balance}`);
      if (r.docSW > r.docCW) probs.push(`scroll horizontal ${r.docSW}>${r.docCW}`);
      if (errs.length) probs.push(`erros JS: ${errs.slice(0, 2).join(' | ')}`);
      if (r.clipped.length) probs.push(`diagrama cortado: ${JSON.stringify(r.clipped)}`);
      if (r.cutN) probs.push(`${r.cutN} caixa(es) com texto cortado: ${r.cut.join(' ; ')}`);
      // Collapsed page. When an unclosed position:fixed wrapper swallows <main>,
      // the text stays in the DOM (so textLen is large) but the content box
      // collapses to ~0 while the fixed element paints the full viewport. That
      // combination is the signature. A legitimately short session renders a
      // short-but-real content box, so it is not flagged.
      if (r.textLen < 60) probs.push(`corpo vazio (${r.textLen} chars)`);
      if (r.holderH < 200) probs.push(`conteudo colapsado (holder com ${Math.round(r.holderH)}px de altura, texto=${r.textLen} chars)`);

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
