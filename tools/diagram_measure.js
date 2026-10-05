#!/usr/bin/env node
/*
 * diagram_measure.js — mede a geometria renderizada de um diagrama e a
 * imprime em PONTOS DE PDF (1pt = 1.3333px a 96dpi), para comparar com as
 * coordenadas medidas direto do PDF de origem.
 *
 *   node tools/diagram_measure.js <html> [en|pt] [seletor]
 *
 * Exemplo:
 *   node tools/diagram_measure.js joseph/modulo-1/sessao-1.html en
 *
 * Naosa saida: posicao x/width, y/height de cada .dg-panel/.dg-sub, a altura
 * do <ul> interno e a contagem de <li>. As alturas sao o dado que mais importa:
 * no PDF de sessao-1 do curso joseph as caixas de 1/2/3 linhas medem
 * respectivamente 60 / 75.8 / 91.5 pt.
 */
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch({ channel: 'chrome' });
  const p = await b.newPage({ viewport: { width: 1100, height: 1000 } });
  await p.goto('file://' + path.resolve(process.argv[2]), { waitUntil: 'domcontentloaded' });
  if (process.argv[3]) await p.evaluate(l => { document.documentElement.lang = l; }, process.argv[3]);
  await p.waitForTimeout(1500);
  const rows = await p.evaluate(() => {
    const out = [];
    const fig = document.querySelector('.dg');
    const fr = fig.getBoundingClientRect();
    const px = v => (v / 1.3333).toFixed(1);
    fig.querySelectorAll('.dg-panel, .dg-sub').forEach(el => {
      const r = el.getBoundingClientRect();
      const tag = el.querySelector(':scope > .dg-tag');
      const ul = el.querySelector(':scope > ul');
      out.push([
        (el.className.includes('dg-panel') ? 'PAINEL ' : '  sub   ') + (tag ? tag.textContent.slice(0, 22) : '?'),
        'x=' + px(r.left - fr.left), 'w=' + px(r.width),
        'y=' + px(r.top - fr.top), 'h=' + px(r.height),
        ul ? 'ul_y=' + px(ul.getBoundingClientRect().top - r.top) + ' linhas=' + ul.children.length : ''
      ].join('  '));
    });
    return out;
  });
  rows.forEach(r => console.log(r));
  await b.close();
})();
