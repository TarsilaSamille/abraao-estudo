import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const file = p => 'file://' + resolve(ROOT, p);
const assert = (c, m) => { if (!c) throw new Error(m); };

const browser = await chromium.launch({ args: ['--no-sandbox', '--allow-file-access-from-files'] });

// ---- Root index: bilingual catalog ----
{
  const page = await browser.newPage({ viewport: { width: 1100, height: 1600 } });
  await page.goto(file('index.html'), { waitUntil: 'networkidle', timeout: 30000 });
  assert((await page.textContent('h1')).trim() === 'Estudos Bíblicos', 'root PT h1 wrong');
  const cards = await page.$$eval('#grid > a', els => els.length);
  assert(cards === 15, `root: expected 15 cards, got ${cards}`);
  assert(await page.$$eval('#grid img', e => e.length === 15 && e.every(i => i.naturalWidth > 0)), 'root: covers not loaded');
  await page.click('#lang-en'); await page.waitForTimeout(300);
  assert((await page.textContent('h1')).trim() === 'Bible Studies', 'root EN h1 wrong');
  await page.close();
}

// ---- Abraham index: bilingual + back button ----
{
  const page = await browser.newPage({ viewport: { width: 1200, height: 1400 } });
  await page.addInitScript(() => localStorage.clear());
  await page.goto(file('abraao/index.html'), { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(200);
  assert((await page.textContent('h1')).trim() === 'Abraão', 'abraao PT h1 wrong');
  assert((await page.$$eval('#modgrid > a', els => els.length)) === 6, 'abraao: expected 6 module cards');
  assert(await page.$$eval('#modgrid img', e => e.length === 6 && e.every(i => i.naturalWidth > 0)), 'abraao: module imgs not loaded');
  const back = await page.$eval('a[href="../index.html"]', el => el.textContent.trim());
  assert(/Voltar/.test(back), 'abraao: back button missing/PT');
  await page.click('#lang-en'); await page.waitForTimeout(250);
  assert((await page.textContent('h1')).trim() === 'Abraham', 'abraao EN h1 wrong');
  assert(/Back/.test(await page.$eval('a[href="../index.html"]', el => el.textContent)), 'abraao: back not translated');
  await page.close();
}

// ---- Rise of the Messiah index: bilingual + back button + module images ----
{
  const page = await browser.newPage({ viewport: { width: 1200, height: 1400 } });
  await page.addInitScript(() => localStorage.clear());
  await page.goto(file('rise-of-the-messiah/index.html'), { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(200);
  assert((await page.textContent('h1')).trim() === 'A Ascensão do Messias', 'rise PT h1 wrong');
  assert((await page.$$eval('#modgrid > a', els => els.length)) === 3, 'rise: expected 3 module cards');
  assert(await page.$$eval('#modgrid img', e => e.length === 3 && e.every(i => i.naturalWidth > 0)), 'rise: module imgs not loaded');
  assert(await page.$eval('img', i => i.naturalWidth > 0), 'rise: cover not loaded');
  assert(await page.$('a[href="../index.html"]'), 'rise: back button missing');
  await page.click('#lang-en'); await page.waitForTimeout(250);
  assert((await page.textContent('h1')).trim() === 'Rise of the Messiah', 'rise EN h1 wrong');
  await page.close();
}

// ---- 12 course indexes: mirror abraao layout + PT/EN toggle ----
const COURSES = {
  'heaven-and-earth': [7, 'Céus e Terra', 'Heaven and Earth'],
  'adam-to-noah': [6, 'De Adão a Noé', 'Adam to Noah'],
  'jacob': [6, 'Jacó', 'Jacob'],
  'joseph': [7, 'José', 'Joseph'],
  'exodus-overview': [5, 'Panorama de Êxodo', 'Exodus Overview'],
  'ezekiel': [6, 'Ezequiel', 'Ezekiel'],
  'jonah': [8, 'Jonas', 'Jonah'],
  'messianic-torah': [4, 'A Torá Messiânica', 'The Messianic Torah'],
  '1-corinthians': [8, '1 Coríntios', '1 Corinthians'],
  'ephesians': [11, 'Efésios', 'Ephesians'],
  'intro-hebrew-bible': [5, 'Introdução à Bíblia Hebraica', 'Introduction to the Hebrew Bible'],
  'art-of-biblical-words': [1, 'A Arte das Palavras Bíblicas', 'Art of Biblical Words'],
};

for (const [slug, [n, ptTitle, enTitle]] of Object.entries(COURSES)) {
  const page = await browser.newPage({ viewport: { width: 1200, height: 1400 } });
  await page.addInitScript(() => localStorage.clear());
  await page.goto(file(`${slug}/index.html`), { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(200);
  await page.click('#lang-pt'); await page.waitForTimeout(200);
  assert((await page.textContent('h1')).trim() === ptTitle, `${slug}: PT h1 = "${await page.textContent('h1')}", want "${ptTitle}"`);
  const cards = await page.$$eval('#modgrid > a', els => els.length);
  assert(cards === n, `${slug}: expected ${n} module cards, got ${cards}`);
  assert(await page.$eval('img', i => i.naturalWidth > 0), `${slug}: cover not loaded`);
  assert(await page.$('a[href="../index.html"]'), `${slug}: back button missing`);
  const modImgsOk = await page.$$eval('#modgrid img', els => els.length > 0 && els.every(i => i.naturalWidth > 0));
  assert(modImgsOk, `${slug}: module card images not loaded`);
  assert(/Sess[õãe]es/.test(await page.$eval('#modgrid a p.uppercase', el => el.textContent)), `${slug}: PT sessions label missing`);
  await page.click('#lang-en'); await page.waitForTimeout(250);
  assert((await page.textContent('h1')).trim() === enTitle, `${slug}: EN h1 wrong`);
  assert(/Sessions/.test(await page.$eval('#modgrid a p.uppercase', el => el.textContent)), `${slug}: EN sessions label missing`);
  await page.close();
}

// ---- Module indexes: sample one module per course (bilingual, image, back, sessions grid) ----
{
  const page = await browser.newPage({ viewport: { width: 1000, height: 1200 } });
  for (const [slug, mod, nSess] of [
    ['heaven-and-earth', 1, 5], ['adam-to-noah', 6, 3], ['jacob', 3, 5], ['joseph', 7, 4],
    ['exodus-overview', 4, 6], ['ezekiel', 5, 6], ['jonah', 8, 6], ['messianic-torah', 2, 7],
    ['1-corinthians', 8, 5], ['ephesians', 11, 4], ['intro-hebrew-bible', 3, 4], ['art-of-biblical-words', 1, 5],
  ]) {
    await page.goto(file(`${slug}/modulo-${mod}/index.html`), { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(150);
    await page.click('#lang-pt'); await page.waitForTimeout(150);
    assert(await page.$eval('img', i => i.naturalWidth > 0), `${slug}/m${mod}: module image not loaded`);
    assert(await page.$('a[href="../index.html"]'), `${slug}/m${mod}: back button missing`);
    const cards = await page.$$eval('#sessgrid > a', els => els.length);
    assert(cards === nSess, `${slug}/m${mod}: expected ${nSess} session cards, got ${cards}`);
    const ptSess = await page.$eval('h2[data-i18n="sessions"]', el => el.textContent);
    assert(/Sess[õãe]es/.test(ptSess), `${slug}/m${mod}: PT sessions label ("${ptSess}")`);
    await page.click('#lang-en'); await page.waitForTimeout(200);
    const enSess = await page.$eval('h2[data-i18n="sessions"]', el => el.textContent);
    assert(/Sessions/.test(enSess), `${slug}/m${mod}: EN sessions label ("${enSess}")`);
  }
  await page.close();
}

await browser.close();
console.log(`PASS verify-index: root catalog (15) + 12 course indexes bilingual, covers loaded, PT↔EN OK`);
