import fs from 'fs';
import path from 'path';
import { PNG } from 'pngjs';
import pixelmatch from 'pixelmatch';
import { chromium } from 'playwright';

const URL = 'http://localhost:8000/abraao/modulo-3/sessao-15.html';
const ARTIFACT_PATH = 'tests/artifacts/sessao-15-grid.png';
const DIFF_PATH = 'tests/artifacts/sessao-15-grid-diff.png';
const BASELINE_DEFAULT = process.env.BASELINE || 'tests/baseline/sessao-15-grid.png';

async function screenshotGrid(page) {
  const heading = page.locator('h2:text("Gênesis 15-16 Repete Gênesis 2-11 e 12-14")');
  await heading.waitFor();
  const grid = page.locator('div.grid.grid-cols-4').first();
  await grid.screenshot({ path: ARTIFACT_PATH });
}

function readPng(filePath) {
  return new Promise((resolve, reject) => {
    fs.createReadStream(filePath)
      .pipe(new PNG())
      .on('parsed', function () { resolve(this); })
      .on('error', reject);
  });
}

async function main() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(URL, { waitUntil: 'domcontentloaded' });

  // Ensure artifacts dir exists
  fs.mkdirSync(path.dirname(ARTIFACT_PATH), { recursive: true });

  await screenshotGrid(page);

  if (!fs.existsSync(BASELINE_DEFAULT)) {
    console.error(`Baseline not found: ${BASELINE_DEFAULT}`);
    console.error('Add a baseline grid screenshot to tests/baseline/sessao-15-grid.png');
    await browser.close();
    process.exit(2);
  }

  const baseline = await readPng(BASELINE_DEFAULT);
  const actual = await readPng(ARTIFACT_PATH);

  if (baseline.width !== actual.width || baseline.height !== actual.height) {
    console.error(`Dimension mismatch: baseline=${baseline.width}x${baseline.height} actual=${actual.width}x${actual.height}`);
    console.error('Ensure the baseline is captured from the same region and viewport.');
    await browser.close();
    process.exit(3);
  }

  const diffPng = new PNG({ width: baseline.width, height: baseline.height });
  const mismatch = pixelmatch(baseline.data, actual.data, diffPng.data, baseline.width, baseline.height, {
    threshold: 0.1,
    includeAA: true,
    alpha: 0.7
  });

  fs.writeFileSync(DIFF_PATH, PNG.sync.write(diffPng));

  const totalPixels = baseline.width * baseline.height;
  const percent = (mismatch / totalPixels) * 100;

  console.log(`Pixel diff: mismatched=${mismatch} (${percent.toFixed(3)}%)`);
  console.log(`Diff saved to ${DIFF_PATH}`);

  // Fail if mismatch beyond tolerance (e.g., >0.5%)
  const tolerancePercent = Number(process.env.DIFF_TOLERANCE || 0.5);
  if (percent > tolerancePercent) {
    await browser.close();
    throw new Error(`Visual diff exceeds tolerance (${percent.toFixed(3)}% > ${tolerancePercent}%)`);
  }

  await browser.close();
}

main().catch(err => { console.error(err); process.exit(1); });
