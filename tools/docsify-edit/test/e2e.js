'use strict';

/*
 * Browser smoke test. Set DOCSIFY_EDIT_URL to a running docsify site with the
 * plugin + save server, e.g.:
 *
 *   DOCSIFY_EDIT_URL=http://127.0.0.1:8642/docs/#/page node test/e2e.js
 *
 * It edits the current page, then cancels, so it does not write anything.
 * Skipped automatically when DOCSIFY_EDIT_URL is not set.
 */

const url = process.env.DOCSIFY_EDIT_URL;
if (!url) {
  console.log('skip e2e: DOCSIFY_EDIT_URL is not set');
  process.exit(0);
}

const puppeteer = require('puppeteer-core');
const executablePath = process.env.CHROME_PATH || '/usr/bin/google-chrome';

(async () => {
  const browser = await puppeteer.launch({
    executablePath,
    headless: 'new',
    args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
  });
  const page = await browser.newPage();
  page.on('pageerror', (err) => { throw err; });
  page.on('dialog', (dialog) => dialog.accept());

  await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
  await page.waitForSelector('.markdown-section h1', { timeout: 30000 });
  await page.waitForSelector('#docsify-edit-open', { timeout: 15000 });
  await page.click('#docsify-edit-open');
  await page.waitForSelector('.docsify-editable', { timeout: 15000 });

  const editable = await page.$eval('.markdown-section', (n) => n.getAttribute('contenteditable'));
  if (editable !== 'true') throw new Error('the article is not contenteditable');

  await page.evaluate(() => {
    const p = document.querySelector('.markdown-section p');
    if (!p) return;
    p.focus();
    const range = document.createRange();
    range.selectNodeContents(p);
    range.collapse(false);
    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
  });
  await page.keyboard.type(' e2e');
  await page.click('#docsify-edit-bar button[data-act="cancel"]');
  await page.waitForSelector('.docsify-editable', { hidden: true, timeout: 15000 }).catch(() => {});
  console.log('e2e ok:', url);
  await browser.close();
})().catch((err) => {
  console.error('e2e failed:', err);
  process.exit(1);
});
