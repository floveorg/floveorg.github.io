#!/usr/bin/env node
/*
 * strip.js — remove one language from a translaty page.
 *
 *   node tools/dev/strip.js app.html --lang es          # dry-run
 *   node tools/dev/strip.js app.html --lang es --write
 *
 * Removes `span.<lang>`, `data-<lang>` / `data-ph-<lang>` / `data-aria-<lang>`
 * / `data-title-<lang>`, the worldball option `lang-<lang>` and its CSS
 * toggles. Refuses to strip the base language and stops before writing if a
 * leftover would remain. Run `check.js` afterwards.
 */
'use strict';

const fs = require('fs');

function usage(msg) {
  if (msg) console.error(msg);
  console.error('usage: strip.js <file.html> --lang <code> [--write] [--base <code>]');
  process.exit(2);
}

const argv = process.argv.slice(2);
if (!argv.length) usage();
const file = argv[0];
let lang = null, baseArg = null, write = false;
for (let i = 1; i < argv.length; i++) {
  const a = argv[i];
  if (a === '--lang') lang = argv[++i] || usage('missing --lang value');
  else if (a === '--base') baseArg = argv[++i] || usage('missing --base value');
  else if (a === '--write') write = true;
  else if (a === '-h' || a === '--help') usage();
  else usage(`unknown argument: ${a}`);
}
if (!lang) usage('missing --lang');
if (!/^[A-Za-z0-9-]+$/.test(lang)) usage(`invalid language code: ${lang}`);
const escRe = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const escLang = escRe(lang);

let src;
try { src = fs.readFileSync(file, 'utf8'); }
catch (e) { console.error(`strip: cannot read ${file}: ${e.message}`); process.exit(1); }

const baseMatch = src.match(/<html\b[^>]*\bdata-base\s*=\s*["']([^"']+)["']/i);
const base = baseArg || (baseMatch && baseMatch[1]) || 'en';
if (lang === base) {
  console.error(`strip: refusing to strip the base language "${base}"`);
  process.exit(1);
}

let text = src;
const stats = { spans: 0, attrs: 0, worldballs: 0, css: 0 };

/* ── span.<lang> (tag-balanced) ─────────────────────────────────────────── */
function isTargetSpan(tag) {
  const cls = tag.match(/\bclass\s*=\s*["']([^"']*)["']/i);
  if (cls && cls[1].split(/\s+/).includes(lang)) return true;
  const l = tag.match(/\blang\s*=\s*["']([^"']+)["']/i);
  return !!(l && l[1].toLowerCase() === lang.toLowerCase());
}
function stripSpans(s) {
  let out = '', i = 0;
  while (i < s.length) {
    const m = /<span\b[^>]*>/i.exec(s.slice(i));
    if (!m) { out += s.slice(i); break; }
    const start = i + m.index;
    out += s.slice(i, start);
    if (!isTargetSpan(m[0])) { out += m[0]; i = start + m[0].length; continue; }
    // Walk to the matching </span>, counting nested spans.
    let depth = 1, j = start + m[0].length;
    const tagRe = /<span\b[^>]*>|<\/span\s*>/gi;
    let end = -1;
    while (depth > 0) {
      tagRe.lastIndex = j;
      const t = tagRe.exec(s);
      if (!t) break;
      if (/^<\/span/i.test(t[0])) depth--; else depth++;
      if (depth === 0) end = t.index + t[0].length;
      j = t.index + t[0].length;
    }
    if (end === -1) { out += m[0]; i = start + m[0].length; continue; }
    stats.spans++;
    i = end;
  }
  return out;
}

/* ── data-<lang> family ──────────────────────────────────────────────────── */
function stripAttrs(s) {
  const names = ['data-' + lang, 'data-ph-' + lang, 'data-aria-' + lang, 'data-title-' + lang]
    .map(n => escRe(n));
  const re = new RegExp('\\s+(?:' + names.join('|') + ')\\s*=\\s*(?:"[^"]*"|\'[^\']*\'|[^\\s>]+)', 'gi');
  return s.replace(re, () => { stats.attrs++; return ''; });
}

/* ── worldball input + label ─────────────────────────────────────────────── */
function stripWorldball(s) {
  const pair = new RegExp(
    '<input\\b[^>]*\\bid\\s*=\\s*["\']lang-' + escLang + '["\'][^>]*>\\s*' +
    '<label\\b[^>]*\\bfor\\s*=\\s*["\']lang-' + escLang + '["\'][^>]*>[\\s\\S]*?</label\\s*>', 'gi');
  s = s.replace(pair, () => { stats.worldballs++; return ''; });
  const loneLabel = new RegExp(
    '<label\\b[^>]*\\bfor\\s*=\\s*["\']lang-' + escLang + '["\'][^>]*>[\\s\\S]*?</label\\s*>', 'gi');
  s = s.replace(loneLabel, () => { stats.worldballs++; return ''; });
  const loneInput = new RegExp(
    '<input\\b[^>]*\\bid\\s*=\\s*["\']lang-' + escLang + '["\'][^>]*>', 'gi');
  s = s.replace(loneInput, () => { stats.worldballs++; return ''; });
  return s;
}

/* ── CSS toggle rules ────────────────────────────────────────────────────── */
function stripCss(s) {
  const styleRe = /(<style\b[^>]*>)([\s\S]*?)(<\/style\s*>)/gi;
  return s.replace(styleRe, (all, open, css, close) => {
    const rules = css.replace(/([^{}]+)\{([^{}]*)\}/g, (rule, sel, body) => {
      const s = sel.trim();
      const targets = new RegExp('#lang-' + escLang + '\\b|\\.lang-' + escLang + '\\b|\\.' + escLang + '\\b', 'i');
      if (!targets.test(s)) return rule;
      stats.css++;
      return '';
    });
    return open + rules + close;
  });
}

text = stripSpans(text);
text = stripAttrs(text);
text = stripWorldball(text);
text = stripCss(text);

/* ── leftover guard ──────────────────────────────────────────────────────── */
const leftovers = [];
function scan(re, label) {
  const m = text.match(re);
  if (m) leftovers.push(`${label}: ${m[0].slice(0, 120)}`);
}
scan(new RegExp('\\blang\\s*=\\s*["\']' + escLang + '["\']', 'i'), 'lang');
scan(new RegExp('\\bclass\\s*=\\s*["\'][^"\']*\\b' + escLang + '\\b', 'i'), 'class');
scan(new RegExp('\\bdata-(?:ph-|aria-|title-)?' + escLang + '\\s*=', 'i'), 'data');
scan(new RegExp('\\bid\\s*=\\s*["\']lang-' + escLang + '["\']', 'i'), 'worldball id');
scan(new RegExp('\\bfor\\s*=\\s*["\']lang-' + escLang + '["\']', 'i'), 'worldball label');
scan(new RegExp('#lang-' + escLang + '\\b|\\.lang-' + escLang + '\\b', 'i'), 'css toggle');

console.log(`strip ${lang} from ${file} (base ${base})`);
console.log(`  spans ${stats.spans} · attrs ${stats.attrs} · worldball ${stats.worldballs} · css ${stats.css}`);
if (leftovers.length) {
  console.error('strip: leftovers remain — not writing');
  for (const l of leftovers) console.error('  ' + l);
  process.exit(1);
}
if (!write) {
  console.log('  dry-run — add --write to apply');
  process.exit(0);
}
fs.writeFileSync(file, text);
console.log('  written');
