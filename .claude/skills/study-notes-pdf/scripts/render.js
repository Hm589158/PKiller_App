// Render an assembled notes HTML file to an A4 PDF with a page-number footer.
// Usage: NODE_PATH=$(npm root -g) node render.js in.html out.pdf --footer "text" [--dir rtl|ltr] [--lang ar|en]
const { chromium } = require('playwright');
const path = require('path');

const args = process.argv.slice(2);
const [inp, out] = args;
const opt = (name, def) => { const i = args.indexOf('--' + name); return i > -1 ? args[i + 1] : def; };
const dir = opt('dir', 'ltr');
const lang = opt('lang', dir === 'rtl' ? 'ar' : 'en');
const footer = (opt('footer', '') || '').replace(/[<>&]/g, c => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;' }[c]));
const pageWord = lang === 'ar'
  ? 'صفحة <span class="pageNumber"></span> من <span class="totalPages"></span>'
  : 'Page <span class="pageNumber"></span> of <span class="totalPages"></span>';

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(inp), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.emulateMedia({ media: 'print' });
  // The footer is rendered in a separate context: web fonts and base64 @font-face do not
  // load there, so use a font installed on the system (DejaVu Sans covers Arabic and Latin).
  await p.pdf({
    path: out, format: 'A4', printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: `<div dir="${dir}" style="width:100%;font-family:'DejaVu Sans',sans-serif;font-size:8.5px;color:#5a6474;padding:0 11mm;display:flex;justify-content:space-between"><span>${footer}</span><span>${pageWord}</span></div>`,
  });
  await b.close();
})();
