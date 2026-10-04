/**
 * audit_header.js — audita cabecalho, rodape e controles PT/EN em runtime.
 *
 *Responder "o Voltar/Imprimir e o PT/EN estao iguais e funcionando?" so por
 * grep engana: botao pode existir e chamar `setLang()` sem o lang-toggle.js
 * carregado (aí clica e da ReferenceError), e o href do Voltar pode estar
 * com caminho que nao existe. Este script ABRE cada pagina e testa.
 *
 * Testa, por sessao:
 *   1. erros de JS ao carregar
 *   2. botao PT/EN: existe? setLang definido? alterna mesmo o idioma?
 *   3. persistencia: recarrega e confere que o idioma ficou
 *   4. Voltar: existe? o href resolve para um arquivo que existe?
 *   5. Imprimir: existe e esta ligado a window.print()
 *   6. rodape: existe?
 *
 * Uso: node tools/audit_header.js [arquivo.html ...]
 *      node tools/audit_header.js            (todos os modulos)
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const explicit = process.argv.slice(2);

function listSessions() {
  const out = execSync(
    "find . -path ./node_modules -prune -o -name 'sessao-*.html' -print",
    { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 }
  ).split('\n').filter(Boolean).sort();
  return out;
}

(async () => {
  const files = explicit.length ? explicit : listSessions();
  const browser = await chromium.launch({ channel: 'chrome' });
  const rows = [];
  let bad = 0;

  for (const f of files) {
    const abs = path.resolve(f);
    const ctx = await browser.newContext({ viewport: { width: 1400, height: 1000 } });
    const page = await ctx.newPage();
    const errs = [];
    page.on('pageerror', e => errs.push(String(e).split('\n')[0]));
    page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().split('\n')[0]); });
    const r = { file: f, probs: [] };

    try {
      await page.goto('file://' + abs, { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(900);

      // ---- 1. estado inicial
      r.lang0 = await page.evaluate(() => document.documentElement.lang || '(sem lang)');

      // ---- 2. PT/EN
      r.hasBtns = await page.evaluate(() =>
        !!(document.querySelector('#lang-pt') && document.querySelector('#lang-en')));
      r.setLangDefined = await page.evaluate(() => typeof window.setLang === 'function');

      if (r.hasBtns) {
        // clica EN e ve se o idioma muda de verdade
        await page.click('#lang-en').catch(() => {});
        await page.waitForTimeout(400);
        r.langAfterEn = await page.evaluate(() => document.documentElement.lang || '(sem lang)');
        r.enVisible = await page.evaluate(() => {
          const en = document.querySelector('.lang-en');
          const pt = document.querySelector('.lang-pt');
          if (!en || !pt) return null;
          const ev = getComputedStyle(en).display !== 'none';
          const pv = getComputedStyle(pt).display === 'none';
          return ev && pv;
        });
        // recarrega: o idioma tem de persistir
        await page.reload({ waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(900);
        r.langAfterReload = await page.evaluate(() => document.documentElement.lang || '(sem lang)');
        if (r.langAfterReload === 'pt') {           // volta para PT
          await page.click('#lang-pt').catch(() => {});
          await page.waitForTimeout(350);
        }
      }

      // ---- 3. Voltar
      const back = await page.evaluate(() => {
        const a = [...document.querySelectorAll('a')].find(x =>
          /\bvoltar\b|\bback\b/i.test(x.innerText || ''));
        if (!a) return null;
        return { href: a.getAttribute('href'), target: a.getAttribute('target') };
      });
      r.back = back;
      if (!back) r.probs.push('sem botao Voltar');
      else if (!back.href) r.probs.push('Voltar sem href');
      else {
        const resolved = path.resolve(path.dirname(abs), back.href.split('#')[0]);
        if (!fs.existsSync(resolved)) r.probs.push(`Voltar quebrado: ${back.href}`);
      }

      // ---- 4. Imprimir
      r.print = await page.evaluate(() =>
        [...document.querySelectorAll('button')].some(b => /window\.print\(\)/.test(b.getAttribute('onclick') || '')));
      if (!r.print) r.probs.push('sem botao Imprimir');

      // ---- 5. rodape
      r.footer = await page.evaluate(() => !!document.querySelector('footer'));

      // ---- 6. erros
      if (errs.length) r.probs.push('erro JS: ' + errs.slice(0, 2).join(' | '));

      // ---- 7. diagnostico do toggle
      if (r.hasBtns && !r.setLangDefined) r.probs.push('botao PT/EN sem lang-toggle.js (setLang indefinido)');
      if (r.hasBtns && r.setLangDefined && r.langAfterEn === r.lang0) r.probs.push('clicar EN nao muda o idioma');
      if (r.hasBtns && r.enVisible === false) r.probs.push('lang-en/pt nao alternam a visibilidade');
      if (r.hasBtns && r.langAfterReload === r.lang0 && r.lang0 === 'en')
        r.probs.push('idioma EN nao persiste apos recarregar');

      // progresso
      r.hasProgress = await page.evaluate(() => !!document.querySelector('#reading-progress'));
    } catch (e) {
      r.probs.push('EXCECAO: ' + e.message.split('\n')[0]);
    }
    await ctx.close();

    if (r.probs.length) bad++;
    rows.push(r);
    if (r.probs.length) console.log(`FALHA  ${f}\n         ${r.probs.join('\n         ')}`);
  }

  await browser.close();

  const summary = {
    total: rows.length,
    ok: rows.length - bad,
    semVoltar: rows.filter(r => r.probs.some(p => /Voltar/.test(p))).length,
    semImprimir: rows.filter(r => r.probs.some(p => /Imprimir/.test(p))).length,
    semBotaoLang: rows.filter(r => !r.hasBtns).length,
    setLangIndefinido: rows.filter(r => r.probs.some(p => /setLang/.test(p))).length,
    langNaoMuda: rows.filter(r => r.probs.some(p => /nao muda o idioma/.test(p))).length,
    semRodape: rows.filter(r => !r.footer).length,
    comErroJs: rows.filter(r => r.probs.some(p => /erro JS/.test(p))).length,
  };
  console.log('\n' + JSON.stringify(summary, null, 2));
  console.log(`\n${summary.ok}/${summary.total} ok`);
  process.exit(bad ? 1 : 0);
})();