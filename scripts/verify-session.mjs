import { chromium } from 'playwright';

const URL = 'http://localhost:8000/abraao/modulo-3/sessao-15.html';
function rgb(hex){ const h=hex.replace('#',''); return `rgb(${parseInt(h.slice(0,2),16)}, ${parseInt(h.slice(2,4),16)}, ${parseInt(h.slice(4,6),16)})`; }

async function checkColor(page, selector, expected){
  const el = page.locator(selector).first();
  await el.waitFor();
  const bg = await el.evaluate(e=>getComputedStyle(e).backgroundColor);
  const color = await el.evaluate(e=>getComputedStyle(e).color);
  if(bg !== rgb(expected.bg) || color !== rgb(expected.text)){
    throw new Error(`${selector} color mismatch: bg=${bg} text=${color}`);
  }
}

async function main(){
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(URL, { waitUntil: 'domcontentloaded' });

  // Macro design 3 boxes exist
  const macroBoxes = page.locator('h3:text("Design Macro de Gênesis 17")').locator('xpath=..').locator('div.border').count();
  const count = await macroBoxes;
  if(count < 3){ throw new Error(`Expected 3 macro boxes, got ${count}`); }

  // Check highlight palettes
  await checkColor(page, '.hl.hl-blue', { bg: '8eaee8', text: 'ffffff' });
  await checkColor(page, '.hl.hl-green', { bg: 'c7e7a6', text: '335b1f' });
  await checkColor(page, '.hl.hl-purple', { bg: 'e2dcf5', text: '674ea7' });
  await checkColor(page, '.hl.hl-amber', { bg: 'ffe29a', text: '6f460d' });
  await checkColor(page, '.hl.hl-rose', { bg: 'a64d79', text: 'ffffff' });
  await checkColor(page, '.hl.hl-mauve', { bg: 'f3e5f5', text: '741b47' });

  // Screenshot the detailed section
  const detail = page.locator('h3:text("Gênesis 17:1-3")').locator('xpath=..');
  await detail.screenshot({ path: 'tests/artifacts/sessao-15-detalhe.png' });

  console.log('Session highlights verified; screenshots saved.');
  await browser.close();
}

main().catch(err => { console.error(err); process.exit(1); });
