# Format recipes — the canonical shapes to repair *toward*

Every flove app was reinventing `toMd`/`toXml`/`renderJpg`/CSV quoting by hand, each slightly
differently — that inconsistency is exactly what `/exporty` exists to fix. These are the canonical
recipes, distilled from the `metas/souls.html` reference. When you repair or scaffold a format,
match these; don't hand-roll a new variant. Adapt names to the app's idiom, keep the behavior.

All of them serialize from the **summary-model** (`references/export-contract.md §A`). Build the
model once, pass it everywhere.

## Shared helpers (one copy per app, reused by all formats)

```js
// Escaping — ONE pair, used by BOTH xml and html. Never hand-roll per format.
const esc     = s => String(s).replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const escAttr = s => esc(s).replace(/"/g, '&quot;');

// Filesystem-safe app slug
const safeName = s => String(s).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

// The active-language word for "summary" (extend per translaty language)
const SUMMARY_WORD = { en:'summary', es:'resumen', fr:'resume', pt:'resumo', de:'zusammenfassung' };
const activeLang = () => document.documentElement.lang || 'en';   // or your i18n hook
const fileBase   = m => `${safeName(m.app)}-${SUMMARY_WORD[activeLang()] || 'summary'}`;

// Universal download — the family pattern. Used by every text format.
function downloadBlob(body, mime, filename){
  const blob = new Blob([body], { type: mime });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
```

## Markdown (`.md` · `text/markdown;charset=utf-8`)

Heading (localized) + phrase + sections; raters as a table. Human prose follows the active language.

```js
function toMd(m){
  let s = `# ${m.app}\n\n${m.phrase}\n\n`;
  m.sections.forEach(sec => {
    s += `## ${sec.label}${sec.title ? ' · ' + sec.title : ''}\n`;
    sec.items.forEach(it => s += `- ${it}\n`);
    s += '\n';
  });
  if (m.raters?.length){
    s += `| rater | value |\n|---|---|\n`;
    m.raters.forEach(r => s += `| ${r.emoji} ${r.key} | ${r.n}/${r.max} |\n`);
  }
  return s;
}
```

## JSON (`.json` · `application/json;charset=utf-8`) — the round-trip format

Always `JSON.stringify`. Never concatenate. Keys stay in stable English.

```js
const toJson = m => JSON.stringify(m, null, 2);
```

## XML (`.xml` · `application/xml;charset=utf-8`)

Well-formed, every value through `esc`/`escAttr`. Element names stay English.

```js
function toXml(m){
  let s = `<?xml version="1.0" encoding="UTF-8"?>\n<flove app="${escAttr(m.app)}" version="${m.version}">\n`;
  s += `  <phrase>${esc(m.phrase)}</phrase>\n  <sections>\n`;
  m.sections.forEach(sec => {
    s += `    <section label="${escAttr(sec.label)}"${sec.title ? ` title="${escAttr(sec.title)}"` : ''}>\n`;
    sec.items.forEach(it => s += `      <item>${esc(it)}</item>\n`);
    s += `    </section>\n`;
  });
  s += `  </sections>\n  <raters>\n`;
  (m.raters||[]).forEach(r => s += `    <rater key="${escAttr(r.key)}" n="${r.n}" max="${r.max}"/>\n`);
  s += `  </raters>\n</flove>\n`;
  return s;
}
```

## HTML (`.html` · `text/html;charset=utf-8`) — also the share-to-mobile artifact

Standalone document, inline `<style>`, no external refs. Title localized. All user values escaped
(this is where injection would happen — escape everything).

```js
function toHtml(m){
  const rows = m.sections.map(sec =>
    `<section><h2>${esc(sec.label)}${sec.title ? ' · ' + esc(sec.title) : ''}</h2><ul>`
    + sec.items.map(it => `<li>${esc(it)}</li>`).join('') + `</ul></section>`).join('');
  return `<!doctype html><html lang="${activeLang()}"><head><meta charset="utf-8">`
    + `<meta name="viewport" content="width=device-width,initial-scale=1">`
    + `<title>${esc(m.app)} · ${SUMMARY_WORD[activeLang()] || 'summary'}</title>`
    + `<style>body{font:15px/1.6 system-ui,sans-serif;max-width:640px;margin:2rem auto;padding:1rem}`
    + `h1{font-weight:600}li{margin:.2rem 0}</style></head>`
    + `<body><h1>${esc(m.app)}</h1><p>${esc(m.phrase)}</p>${rows}</body></html>`;
}
```

## CSV (`.csv` · `text/csv;charset=utf-8`)

RFC-4180 quoting. Headers stay English.

```js
function toCsv(m){
  const q = v => { const s = String(v); return /[",\n]/.test(s) ? `"${s.replace(/"/g,'""')}"` : s; };
  const lines = ['section,title,item'];
  m.sections.forEach(sec => sec.items.forEach(it =>
    lines.push([sec.label, sec.title || '', it].map(q).join(','))));
  return lines.join('\n');
}
```

## JPG (`.jpg` · `image/jpeg`, q≥0.9) — visual-only

Canvas render, ≥1080px wide. Truncate with a **visible `…`**, never silently.

```js
function toJpg(m, cb){
  const W = 1080, H = 720, canvas = document.createElement('canvas');
  canvas.width = W; canvas.height = H;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#14101f'; ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = '#f5b463'; ctx.font = '600 40px Georgia, serif';
  ctx.fillText(m.app, 48, 72);
  ctx.fillStyle = '#fff'; ctx.font = '20px system-ui, sans-serif';
  const lines = m.sections.flatMap(s => [`${s.label}${s.title ? ' · ' + s.title : ''}`,
                                         ...s.items.map(i => '  · ' + i)]);
  const MAX = 26;                                  // rows that fit
  lines.slice(0, MAX).forEach((ln, i) =>
    ctx.fillText(ln.slice(0, 70), 48, 130 + i * 28));
  if (lines.length > MAX) ctx.fillText('…', 48, 130 + MAX * 28);   // never drop in silence
  canvas.toBlob(cb, 'image/jpeg', 0.92);
}
```

## Download dispatcher (one hook vocabulary)

```js
document.querySelectorAll('[data-flove-save]').forEach(btn => btn.addEventListener('click', () => {
  const m = buildModel(), fmt = btn.dataset.floveSave, base = fileBase(m);
  if (fmt === 'jpg'){ toJpg(m, b => downloadBlob(b, 'image/jpeg', base + '.jpg')); return; }
  const f = {
    md:   [toMd(m),   'text/markdown'],
    json: [toJson(m), 'application/json'],
    xml:  [toXml(m),  'application/xml'],
    html: [toHtml(m), 'text/html'],
    csv:  [toCsv(m),  'text/csv'],
  }[fmt];
  downloadBlob(f[0], f[1] + ';charset=utf-8', `${base}.${fmt}`);
}));
```

## Share ladder (`[data-flove-share="mobile"]`)

```js
async function shareMobile(m){
  const html = new File([toHtml(m)], fileBase(m) + '.html', { type: 'text/html' });
  const title = `flove · ${m.app}`;
  if (navigator.canShare && navigator.canShare({ files: [html] })){
    try { await navigator.share({ title, text: m.phrase, files: [html] }); return; } catch(_){}
  }
  if (navigator.share){ try { await navigator.share({ title, text: m.phrase }); return; } catch(_){} }
  try { await navigator.clipboard.writeText(m.phrase); toast('Copied — paste to share'); }
  catch(_){ /* fall to the in-page intent grid: [data-flove-share="apps"] */ }
}
```

## Parse-back / parity test (reuse across apps)

A throwaway `node` check the skill writes once and reuses — proves "exported correctly" mechanically
instead of by eye. Build each format from a sample model (include a hostile item), then assert
parse-back + parity.

```js
// node check.js  — sketch; wire the app's real to* functions in
const sample = { app:'demo', version:1, phrase:'a < b & "c"',
  sections:[{label:'L', title:'T', items:['x, y', 'emoji 🌱', '<script>']}], raters:[{key:'k',n:3,max:5}] };
const items = sample.sections.flatMap(s => s.items);
// JSON: round-trips exactly
const j = JSON.parse(toJson(sample));
assert(j.sections.flatMap(s=>s.items).join('|') === items.join('|'), 'json parity');
// XML: well-formed + no raw <script> leaking as markup
const { DOMParser } = require('@xmldom/xmldom') ;   // or jsdom
const doc = new DOMParser().parseFromString(toXml(sample), 'application/xml');
assert(!doc.getElementsByTagName('parsererror').length, 'xml well-formed');
// HTML: phrase present, the <script> item is escaped (no real script node)
// CSV: the "x, y" item stays in one field (quoted)
```

If `node`/parsers aren't installed, fall back to careful manual inspection — but say so in the
report; a mechanical parse-back is the stronger evidence.
