#!/usr/bin/env node
// translaty check / audit / portfolio ledger.
//
// Usage:
//   node check.js <file.html> [--base en]
//   node check.js --audit <file.html> [--base en] [--json]
//   node check.js --all [<dir>] [--base en] [--json|--md]
//                [--out <file>] [--strict] [--quiet]
//
// check (default): structural gate + every translaty-marked group has the base
// language. A single-language page with no spans passes.
// --audit: read-only report (missing base, coverage, orphan spans) for one file.
// --all: walk .html files and emit the flove-i18n/1 ledger.
//
// Exit: 0 clean, 1 issues (check/audit; --all only with --strict), 2 bad args.
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const LANGS = new Set(['en', 'es', 'fr', 'de', 'it', 'pt', 'pt-br', 'nl', 'ca', 'gl', 'eu']);
const SKIP_DIRS = new Set(['.git', 'node_modules', 'vendor', 'dist', 'build', '.cache', '__pycache__', 'translaty-workspace']);
const EXEMPT = ['projects/liberada', 'projects/futbolia', 'projects/dinamicas-electronicas'];

function usage() {
  console.log(`usage:
  node check.js <file.html> [--base en]
  node check.js --audit <file.html> [--base en] [--json]
  node check.js --all [<dir>] [--base en] [--json|--md] [--out <file>] [--strict] [--quiet]

base defaults to en. Audit ignores script/style/pre/code/kbd and only looks at
translaty-marked strings (language spans and data-* attributes).`);
}

function parseArgs(argv) {
  const o = { mode: 'check', base: 'en', file: null, root: null, json: false, md: false, out: null, strict: false, quiet: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--audit') o.mode = 'audit';
    else if (a === '--all') o.mode = 'all';
    else if (a === '--json') o.json = true;
    else if (a === '--md') o.md = true;
    else if (a === '--strict') o.strict = true;
    else if (a === '--quiet') o.quiet = true;
    else if (a === '--base') o.base = (argv[++i] || '').toLowerCase();
    else if (a === '--out') o.out = argv[++i];
    else if (a === '-h' || a === '--help') { usage(); process.exit(0); }
    else if (a.startsWith('-')) { console.error(`unknown option: ${a}`); process.exit(2); }
    else if (o.mode === 'all' && o.root === null) o.root = a;
    else if (o.file === null) o.file = a;
    else { console.error(`unexpected argument: ${a}`); process.exit(2); }
  }
  if (!/^[a-z]{2}(-[a-z]{2})?$/.test(o.base)) { console.error(`bad base language: ${o.base}`); process.exit(2); }
  if (o.mode === 'all') o.root = o.root || process.cwd();
  else if (!o.file) { usage(); process.exit(2); }
  return o;
}

function readFile(file) {
  return fs.readFileSync(file, 'utf8');
}

function lineIndex(text) {
  const starts = [0];
  for (let i = 0; i < text.length; i++) if (text[i] === '\n') starts.push(i + 1);
  return (idx) => {
    let lo = 0, hi = starts.length - 1;
    while (lo < hi) {
      const mid = (lo + hi + 1) >> 1;
      if (starts[mid] <= idx) lo = mid; else hi = mid - 1;
    }
    return lo + 1;
  };
}

function attr(attrs, name) {
  const re = new RegExp(`\\b${name}\\s*=\\s*("([^"]*)"|'([^']*)'|([^\\s>]+))`, 'i');
  const m = attrs.match(re);
  return m ? (m[2] ?? m[3] ?? m[4] ?? '') : null;
}

function langFromClass(cls, declared, langAttr) {
  if (!cls) return [];
  const out = [];
  const la = (langAttr || '').toLowerCase();
  for (const tok of cls.split(/\s+/)) {
    const m = tok.match(/^(?:t-)?([a-z]{2}(?:-[a-z]{2})?)$/i);
    if (!m) continue;
    const code = m[1].toLowerCase();
    const hasLang = la === code || (la && la.split('-')[0] === code.split('-')[0]);
    if (declared.has(code) || hasLang) out.push(code);
  }
  return [...new Set(out)];
}

function maskIgnored(html) {
  let mask = html;
  const patterns = [
    /<!--[\s\S]*?-->/g,
    /<script\b[^>]*>[\s\S]*?<\/script>/gi,
    /<style\b[^>]*>[\s\S]*?<\/style>/gi,
    /<pre\b[^>]*>[\s\S]*?<\/pre>/gi,
    /<code\b[^>]*>[\s\S]*?<\/code>/gi,
    /<kbd\b[^>]*>[\s\S]*?<\/kbd>/gi,
  ];
  for (const re of patterns) mask = mask.replace(re, (m) => ' '.repeat(m.length));
  return mask;
}

function collectSpans(mask, declared) {
  const re = /<span\b([^>]*)>|<\/span>/gi;
  const stack = [];
  const spans = [];
  let m;
  while ((m = re.exec(mask))) {
    if (m[0].startsWith('</')) {
      const open = stack.pop();
      if (open && open.langs.length) spans.push({ start: open.start, end: m.index + m[0].length, langs: open.langs });
    } else {
      const attrs = m[1];
      const langAttr = attr(attrs, 'lang');
      stack.push({ start: m.index, attrs, langs: langFromClass(attr(attrs, 'class'), declared, langAttr) });
    }
  }
  return spans;
}

function groupSpans(spans, mask) {
  spans.sort((a, b) => a.start - b.start);
  const groups = [];
  for (const s of spans) {
    const last = groups[groups.length - 1];
    if (last && (s.start <= last.end || mask.slice(last.end, s.start).trim() === '')) {
      last.end = Math.max(last.end, s.end);
      for (const l of s.langs) last.langs.add(l);
    } else {
      groups.push({ start: s.start, end: s.end, langs: new Set(s.langs) });
    }
  }
  return groups;
}

function collectDataGroups(mask, declared) {
  const tagRe = /<([a-z][a-z0-9-]*)\b([^>]*)>/gi;
  const groups = [];
  let m;
  while ((m = tagRe.exec(mask))) {
    const attrs = m[2];
    const fams = new Map();
    const re = /\bdata-(ph-|aria-|title-)?([a-z]{2}(?:-[a-z]{2})?)\s*=\s*("([^"]*)"|'([^']*)'|([^\s>]+))/gi;
    let a;
    while ((a = re.exec(attrs))) {
      const fam = (a[1] || 'plain').replace(/-$/, '');
      const code = a[2].toLowerCase();
      if (!LANGS.has(code) && !(declared && declared.has(code))) continue;
      if (!fams.has(fam)) fams.set(fam, new Set());
      fams.get(fam).add(code);
    }
    for (const [fam, langs] of fams) {
      groups.push({ start: m.index, end: m.index + m[0].length, langs, kind: fam === 'plain' ? 'data' : `data-${fam}`, tag: m[1].toLowerCase() });
    }
  }
  return groups;
}

function structuralIssues(h, declared) {
  const issues = [];
  // spans where phrasing content isn't allowed — must use data-* instead
  for (const tag of ['option', 'textarea', 'title', 'select']) {
    const re = new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)<\\/${tag}>`, 'gi');
    let m;
    while ((m = re.exec(h))) if (/<span\b/i.test(m[1]))
      issues.push(`<span> inside <${tag}> is invalid — translate via data-* attributes instead`);
  }
  // <span> balance
  const so = (h.match(/<span\b/gi) || []).length;
  const sc = (h.match(/<\/span>/gi) || []).length;
  if (so !== sc) issues.push(`<span> imbalance: ${so} open vs ${sc} close`);
  // language spans missing a lang attribute (a11y pronunciation)
  let lm, noLang = 0;
  const spanRe = /<span\b([^>]*)>/gi;
  while ((lm = spanRe.exec(h))) {
    const attrs = lm[1];
    const cls = attr(attrs, 'class');
    if (!cls) continue;
    const langTokens = cls.split(/\s+/)
      .map((t) => t.match(/^(t-)?([a-z]{2}(?:-[a-z]{2})?)$/i))
      .filter(Boolean);
    if (!langTokens.length) continue;
    const hasLang = attr(attrs, 'lang');
    const isLang = langTokens.some((m) => m[1] === 't-' || hasLang || (declared && declared.has(m[2].toLowerCase())));
    if (isLang && !hasLang) noLang++;
  }
  if (noLang) issues.push(`${noLang} language span(s) missing a lang attribute`);
  // duplicate ids
  const ids = {};
  let im;
  const idRe = /\bid="([^"]+)"/g;
  while ((im = idRe.exec(h))) ids[im[1]] = (ids[im[1]] || 0) + 1;
  for (const [id, n] of Object.entries(ids)) if (n > 1) issues.push(`duplicate id="${id}" (${n}×)`);
  // exactly one worldball
  const dl = (h.match(/<details\b[^>]*class="[^"]*\blang\b/gi) || []).length;
  if (dl > 1) issues.push(`${dl} worldball switchers found (should be 1)`);
  // unescaped specials in data-* attribute values
  let dm;
  const dataRe = /\bdata-(?:[a-z-]+)="([^"]*)"/gi;
  while ((dm = dataRe.exec(h))) if (/[<]/.test(dm[1]) || /&(?!(amp|lt|gt|quot|#\d+|#x[0-9a-f]+);)/i.test(dm[1])) {
    issues.push(`unescaped < or & in a data-* value: "${dm[1].slice(0, 40)}…" (escape as &lt; / &amp;)`);
    break;
  }
  // CSS brace + comment balance
  let cssO = 0, cssC = 0, cmtO = 0, cmtC = 0, sRe = /<style\b[^>]*>([\s\S]*?)<\/style>/gi, sm;
  while ((sm = sRe.exec(h))) {
    cssO += (sm[1].match(/{/g) || []).length; cssC += (sm[1].match(/}/g) || []).length;
    cmtO += (sm[1].match(/\/\*/g) || []).length; cmtC += (sm[1].match(/\*\//g) || []).length;
  }
  if (cssO !== cssC) issues.push(`CSS brace imbalance: ${cssO} { vs ${cssC} }`);
  if (cmtO !== cmtC) issues.push(`CSS comment imbalance: ${cmtO} /* vs ${cmtC} */`);
  // JS syntax — compile every inline classic script
  let sc2 = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi, jm, n = 0;
  while ((jm = sc2.exec(h))) {
    const attrs = jm[1], code = jm[2];
    if (/\bsrc=/i.test(attrs)) continue;
    if (/type=/i.test(attrs) && !/type="(?:text\/javascript|application\/javascript)"/i.test(attrs)) continue;
    n++;
    try { new vm.Script(code); }
    catch (e) { issues.push(`JS syntax error in inline <script> #${n}: ${String(e.message).split('\n')[0]}`); }
  }
  return issues;
}

function analyze(html, base, file) {
  const declared = new Set();
  for (const m of html.matchAll(/\bid="lang-([a-z0-9-]+)"/gi)) {
    const code = m[1].toLowerCase();
    if (/^[a-z]{2}(-[a-z]{2})?$/.test(code)) declared.add(code);
  }
  const mask = maskIgnored(html);
  const spans = collectSpans(mask, declared);
  const grouped = groupSpans(spans, mask);
  const dataGroups = collectDataGroups(mask, declared);
  const line = lineIndex(html);
  const groups = [
    ...grouped.map((g) => ({ line: line(g.start), langs: g.langs, kind: 'span' })),
    ...dataGroups.map((g) => ({ line: line(g.start), langs: g.langs, kind: g.kind, tag: g.tag })),
  ];
  const languages = new Set([...declared]);
  for (const g of groups) for (const l of g.langs) languages.add(l);
  const covered = {};
  for (const l of languages) covered[l] = 0;
  for (const g of groups) for (const l of g.langs) covered[l]++;
  const missing = groups.filter((g) => !g.langs.has(base));
  const orphan = [];
  if (declared.size) {
    for (const s of spans) for (const l of s.langs) if (!declared.has(l))
      orphan.push({ line: line(s.start), msg: `language span "${l}" is not in the worldball` });
    for (const g of dataGroups) for (const l of g.langs) if (!declared.has(l))
      orphan.push({ line: line(g.start), msg: `${g.kind} "${l}" is not in the worldball` });
  }
  const structural = structuralIssues(html, declared);
  return { file, base, declared: [...declared], languages: [...languages], groups, covered, missing, orphan, structural, line };
}

function pct(n, d) {
  return d ? Math.round((10000 * n) / d) / 100 : null;
}

function coverageText(a) {
  if (!a.groups.length) return 'no translaty-marked strings';
  return a.languages
    .map((l) => `${l} ${pct(a.covered[l], a.groups.length)}%`)
    .join(' · ');
}

function reportFile(a, opts) {
  if (opts.json) {
    process.stdout.write(JSON.stringify(fileLedger(a), null, 2) + '\n');
    return a.structural.length === 0 && a.missing.length === 0;
  }
  console.log(`translaty audit: ${a.file}`);
  console.log(`  base: ${a.base} · groups: ${a.groups.length} · missing base: ${a.missing.length} · coverage: ${coverageText(a)}`);
  for (const i of a.structural) console.log(`  ✗ ${i}`);
  for (const g of a.missing) console.log(`  ✗ line ${g.line}: ${g.kind} group has ${[...g.langs].join('/')} but no "${a.base}"`);
  for (const o of a.orphan) console.log(`  warn line ${o.line}: ${o.msg}`);
  const ok = a.structural.length === 0 && a.missing.length === 0;
  console.log(ok ? 'translaty audit: OK' : 'translaty audit: ISSUES');
  return ok;
}

function fileLedger(a) {
  const { line, ...rest } = a;
  return {
    path: a.file,
    base: a.base,
    languages: a.languages,
    groups: a.groups.length,
    missingBase: a.missing.length,
    coverage: Object.fromEntries(a.languages.map((l) => [l, pct(a.covered[l], a.groups.length)])),
    issues: [
      ...a.structural,
      ...a.missing.map((g) => `line ${g.line}: ${g.kind} group has ${[...g.langs].join('/')} but no "${a.base}"`),
      ...a.orphan.map((o) => `line ${o.line}: ${o.msg}`),
    ],
  };
}

function checkFile(a, opts) {
  const hard = [...a.structural, ...a.missing.map((g) => `line ${g.line}: ${g.kind} group has ${[...g.langs].join('/')} but no "${a.base}"`)];
  if (hard.length) {
    console.log('translaty check: ISSUES');
    for (const i of hard) console.log('  ✗ ' + i);
    for (const o of a.orphan) console.log('  warn line ' + o.line + ': ' + o.msg);
    process.exit(1);
  }
  if (!opts.quiet) {
    console.log(`translaty check: OK — spans balanced & legally placed, lang attrs present, ids unique, data-* escaped, CSS balanced, inline JS compiles; ${coverageText(a)}`);
    for (const o of a.orphan) console.log('  warn line ' + o.line + ': ' + o.msg);
  }
}

function walk(dir, out) {
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch (e) { return out; }
  for (const e of entries) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (SKIP_DIRS.has(e.name)) continue;
      walk(p, out);
    } else if (e.isFile() && /\.html?$/i.test(e.name)) {
      out.push(p);
    }
  }
  return out;
}

function rel(root, p) {
  return path.relative(root, p).split(path.sep).join('/');
}

function isExempt(relPath) {
  return EXEMPT.some((x) => relPath === x || relPath.startsWith(x + '/'));
}

function auditAll(opts) {
  const root = path.resolve(opts.root);
  const files = walk(root, []);
  const perFile = [];
  const excluded = [];
  let groups = 0, missingBase = 0, structural = 0;
  const coveredByLang = {};
  const allLangs = new Set();
  for (const f of files) {
    const r = rel(root, f);
    if (isExempt(r)) { excluded.push(r); continue; }
    let html;
    try { html = readFile(f); } catch (e) { continue; }
    const a = analyze(html, opts.base, r);
    if (!a.groups.length && !a.structural.length) continue;
    perFile.push(a);
    groups += a.groups.length;
    missingBase += a.missing.length;
    structural += a.structural.length;
    for (const l of a.languages) {
      allLangs.add(l);
      if (!(l in coveredByLang)) coveredByLang[l] = 0;
    }
    for (const g of a.groups) for (const l of g.langs) coveredByLang[l] = (coveredByLang[l] || 0) + 1;
  }
  perFile.sort((a, b) => b.missing.length - a.missing.length || a.file.localeCompare(b.file));
  const languages = [...allLangs].sort();
  const ledger = {
    schema: 'flove-i18n/1',
    generated: new Date().toISOString(),
    root,
    base: opts.base,
    languages,
    summary: {
      files: perFile.length,
      filesWithMarkers: perFile.filter((a) => a.groups.length).length,
      groups,
      missingBase,
      structural,
      coverage: Object.fromEntries(languages.map((l) => [l, pct(coveredByLang[l] || 0, groups)])),
    },
    excluded,
    files: perFile.map(fileLedger),
  };
  if (opts.out) {
    fs.mkdirSync(path.dirname(path.resolve(opts.out)), { recursive: true });
    fs.writeFileSync(opts.out, JSON.stringify(ledger, null, 2) + '\n');
  }
  if (opts.json && !opts.out) process.stdout.write(JSON.stringify(ledger, null, 2) + '\n');
  if (!opts.quiet && !opts.json) {
    if (opts.md) {
      console.log('# translaty audit\n');
      console.log(`- root: \`${root}\``);
      console.log(`- base: \`${opts.base}\` · files: ${ledger.summary.files} · groups: ${groups} · missing base: ${missingBase}`);
      console.log(`- coverage: ${Object.entries(ledger.summary.coverage).map(([l, v]) => `${l} ${v}%`).join(' · ')}`);
      console.log('\n| File | Groups | Missing base | Coverage |');
      console.log('|---|---:|---:|---|');
      for (const a of perFile.slice(0, 20)) {
        console.log(`| \`${a.file}\` | ${a.groups.length} | ${a.missing.length} | ${coverageText(a)} |`);
      }
      if (perFile.length > 20) console.log(`\n… ${perFile.length - 20} more file(s).`);
    } else {
      console.log(`translaty audit: ${ledger.summary.files} file(s), ${groups} group(s), ${missingBase} missing "${opts.base}", ${structural} structural issue(s)`);
      console.log(`  coverage: ${Object.entries(ledger.summary.coverage).map(([l, v]) => `${l} ${v}%`).join(' · ') || 'n/a'}`);
      if (excluded.length) console.log(`  excluded: ${excluded.length} path(s) — ${excluded.slice(0, 5).join(', ')}${excluded.length > 5 ? '…' : ''}`);
      for (const a of perFile.filter((x) => x.missing.length).slice(0, 10)) {
        console.log(`  ✗ ${a.file}: ${a.missing.length} group(s) without ${opts.base} (${coverageText(a)})`);
      }
      if (opts.out) console.log(`  ledger: ${opts.out}`);
    }
  }
  return opts.strict ? missingBase === 0 : true;
}

function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.mode === 'all') {
    const ok = auditAll(opts);
    process.exit(ok ? 0 : 1);
  }
  const html = readFile(opts.file);
  const a = analyze(html, opts.base, opts.file);
  if (opts.mode === 'audit') {
    const ok = reportFile(a, opts);
    process.exit(ok ? 0 : 1);
  }
  checkFile(a, opts);
}

main();
