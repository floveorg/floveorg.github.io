#!/usr/bin/env node
// translaty validity check — HTML / CSS / JS sanity for a translated file.
// Catches the mistakes the translation pass realistically introduces; it is not
// a full W3C validator (prefer html-validate/stylelint if installed), but it is
// a hard gate the skill must pass before finishing.
//
// Usage: node check.js <file.html>      exit 0 = clean, 1 = issues, 2 = bad args
const fs = require('fs');
const vm = require('vm');

const file = process.argv[2];
if (!file) { console.error('usage: node check.js <file.html>'); process.exit(2); }
const h = fs.readFileSync(file, 'utf8');
const issues = [];

// 1. spans where phrasing content isn't allowed — must use data-* instead
for (const tag of ['option', 'textarea', 'title', 'select']) {
  const re = new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)<\\/${tag}>`, 'gi');
  let m; while ((m = re.exec(h))) if (/<span\b/i.test(m[1]))
    issues.push(`<span> inside <${tag}> is invalid — translate via data-* attributes instead`);
}

// 2. <span> balance
const so = (h.match(/<span\b/gi) || []).length, sc = (h.match(/<\/span>/gi) || []).length;
if (so !== sc) issues.push(`<span> imbalance: ${so} open vs ${sc} close`);

// 3. language spans missing a lang attribute (a11y pronunciation)
const langRe = /<span\b[^>]*\bclass="[^"]*\b(?:en|es|fr|pt|pt-br|de|it|ca|gl|eu|nl)\b[^"]*"[^>]*>/gi;
let lm, noLang = 0; while ((lm = langRe.exec(h))) if (!/\blang=/.test(lm[0])) noLang++;
if (noLang) issues.push(`${noLang} language span(s) missing a lang attribute`);

// 4. duplicate ids
const ids = {}; let im; const idRe = /\bid="([^"]+)"/g;
while ((im = idRe.exec(h))) ids[im[1]] = (ids[im[1]] || 0) + 1;
for (const [id, n] of Object.entries(ids)) if (n > 1) issues.push(`duplicate id="${id}" (${n}×)`);

// 5. exactly one worldball
const dl = (h.match(/<details\b[^>]*class="[^"]*\blang\b/gi) || []).length;
if (dl > 1) issues.push(`${dl} worldball switchers found (should be 1)`);

// 6. unescaped specials in data-* attribute values (would break the attribute)
let dm; const dataRe = /\bdata-(?:[a-z-]+)="([^"]*)"/gi;
while ((dm = dataRe.exec(h))) if (/[<]/.test(dm[1]) || /&(?!(amp|lt|gt|quot|#\d+|#x[0-9a-f]+);)/i.test(dm[1]))
  { issues.push(`unescaped < or & in a data-* value: "${dm[1].slice(0, 40)}…" (escape as &lt; / &amp;)`); break; }

// 7. CSS brace + comment balance inside <style>
let cssO = 0, cssC = 0, cmtO = 0, cmtC = 0, sRe = /<style\b[^>]*>([\s\S]*?)<\/style>/gi, sm;
while ((sm = sRe.exec(h))) {
  cssO += (sm[1].match(/{/g) || []).length; cssC += (sm[1].match(/}/g) || []).length;
  cmtO += (sm[1].match(/\/\*/g) || []).length; cmtC += (sm[1].match(/\*\//g) || []).length;
}
if (cssO !== cssC) issues.push(`CSS brace imbalance: ${cssO} { vs ${cssC} }`);
if (cmtO !== cmtC) issues.push(`CSS comment imbalance: ${cmtO} /* vs ${cmtC} */`);

// 8. JS syntax — compile every inline classic script (skips external + module/json)
let sc2 = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi, jm, n = 0;
while ((jm = sc2.exec(h))) {
  const attrs = jm[1], code = jm[2];
  if (/\bsrc=/i.test(attrs)) continue;
  if (/type=/i.test(attrs) && !/type="(?:text\/javascript|application\/javascript)"/i.test(attrs)) continue;
  n++;
  try { new vm.Script(code); }
  catch (e) { issues.push(`JS syntax error in inline <script> #${n}: ${String(e.message).split('\n')[0]}`); }
}

if (issues.length) { console.log('translaty check: ISSUES'); issues.forEach(i => console.log('  ✗ ' + i)); process.exit(1); }
console.log('translaty check: OK — spans balanced & legally placed, lang attrs present, ids unique, data-* escaped, CSS balanced, inline JS compiles');
