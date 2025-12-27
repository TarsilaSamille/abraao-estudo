import { chromium } from 'playwright';

const URL = 'http://localhost:8000/abraao/modulo-3/sessao-15.html';

function rgb(hex){
  const h = hex.replace('#','');
  const r = parseInt(h.slice(0,2),16);
  const g = parseInt(h.slice(2,4),16);
  const b = parseInt(h.slice(4,6),16);
  return `rgb(${r}, ${g}, ${b})`;
}

async function main(){
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(URL, { waitUntil: 'domcontentloaded' });

  // Locate the grid section by heading text
  const heading = page.locator('h2:text("Gênesis 15-16 Repete Gênesis 2-11 e 12-14")');
  await heading.waitFor();
  const grid = page.locator('div.grid.grid-cols-4').first();

  // Ensure 4 columns grid exists with 16 direct children
  const childCount = await grid.locator(':scope > div').count();
  if(childCount !== 16){
    throw new Error(`Grid child count mismatch: expected 16, got ${childCount}`);
  }

  // Verify badge colors (sample a few unique classes)
  const badgeBlue = page.locator('.badge-blue').first();
  const badgeAmber = page.locator('.badge-amber').first();
  const badgeGrey = page.locator('.badge-grey').first();

  const blueBg = await badgeBlue.evaluate(el => getComputedStyle(el).backgroundColor);
  const blueText = await badgeBlue.evaluate(el => getComputedStyle(el).color);
  const amberBg = await badgeAmber.evaluate(el => getComputedStyle(el).backgroundColor);
  const amberText = await badgeAmber.evaluate(el => getComputedStyle(el).color);
  const greyBg = await badgeGrey.evaluate(el => getComputedStyle(el).backgroundColor);
  const greyText = await badgeGrey.evaluate(el => getComputedStyle(el).color);

  const expect = {
    blueBg: rgb('8eaee8'), blueText: rgb('ffffff'),
    amberBg: rgb('ffe29a'), amberText: rgb('6f460d'),
    greyBg: rgb('e6eef9'), greyText: rgb('334355'),
  };

  const results = { blueBg, blueText, amberBg, amberText, greyBg, greyText };
  const passes = [
    results.blueBg === expect.blueBg,
    results.blueText === expect.blueText,
    results.amberBg === expect.amberBg,
    results.amberText === expect.amberText,
    results.greyBg === expect.greyBg,
    results.greyText === expect.greyText,
  ];

  if(!passes.every(Boolean)){
    console.log('Badge color results:', results);
    throw new Error('Badge colors do not match expected screenshot palette');
  }

  // Verify list density & border color
  const anyCell = grid.locator(':scope > div').first();
  const borderTopColor = await anyCell.evaluate(el => getComputedStyle(el).borderTopColor);
  const expectedBorder = rgb('d7dee9');
  if(borderTopColor !== expectedBorder){
    throw new Error(`Border color mismatch: expected ${expectedBorder}, got ${borderTopColor}`);
  }

  // Highlights sample
  const hlBlue = page.locator('.hl.hl-blue').first();
  const hlBlueBg = await hlBlue.evaluate(el => getComputedStyle(el).backgroundColor);
  if(hlBlueBg !== rgb('8eaee8')){
    throw new Error(`Highlight blue mismatch: expected ${rgb('8eaee8')}, got ${hlBlueBg}`);
  }

  // Screenshot grid area
  await grid.screenshot({ path: 'tests/artifacts/grid-sessao-15.png' });
  console.log('Grid verified: 4x4, colors match, screenshot saved to tests/artifacts/grid-sessao-15.png');
  await browser.close();
}

main().catch(err => { console.error(err); process.exit(1); });
