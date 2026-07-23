import { createRequire } from 'node:module';
const require = createRequire('file:///C:/Users/Paul/');
const puppeteer = require('puppeteer');
import { mkdirSync, readdirSync } from 'node:fs';

const url = process.argv[2] || 'http://localhost:3000';
const label = process.argv[3] || '';
const width = parseInt(process.argv[4] || '1440', 10);
const outDir = './temporary screenshots';
mkdirSync(outDir, { recursive: true });

const existing = readdirSync(outDir).filter(f => /^screenshot-\d+/.test(f));
const n = existing.reduce((m, f) => Math.max(m, parseInt(f.match(/^screenshot-(\d+)/)[1], 10)), 0) + 1;
const name = `screenshot-${n}${label ? '-' + label : ''}.png`;

const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
const page = await browser.newPage();
// Emulate reduced-motion so scroll-reveal content is shown and animations are paused for a clean still
await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
await page.setViewport({ width, height: 900, deviceScaleFactor: 1 });
await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });
// Scroll through the page so IntersectionObserver reveals fire, then return to top
await page.evaluate(async () => {
  const step = window.innerHeight * 0.8;
  for (let y = 0; y <= document.body.scrollHeight; y += step) {
    window.scrollTo(0, y);
    await new Promise(r => setTimeout(r, 120));
  }
  window.scrollTo(0, 0);
});
await new Promise(r => setTimeout(r, 900));
await page.screenshot({ path: `${outDir}/${name}`, fullPage: true });
await browser.close();
console.log(`saved ${outDir}/${name}`);
