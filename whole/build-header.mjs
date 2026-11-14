#!/usr/bin/env node
// Re-inject the shared wiki header into every whole page.
// Run after editing this file:  node whole/build-header.mjs
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));

const TOP = [
  ['metaphysics/', 'Metaphysics', 'metaphysics'],
  ['science/', 'Science', 'science'],
  ['biology/', 'Biology', 'biology'],
];
const PARENTS = [
  { key: 'linguistics', slug: 'linguistics/', name: 'Language', children: [
    { key: 'music', slug: 'linguistics/music/', label: 'Music', small: '' },
  ]},
  { key: 'psychosocial', slug: 'psychosocial/', name: 'Psychosocial', children: [
    { key: 'economy', slug: 'economy/', label: 'Economy', small: '' },
  ]},
];

const THEME_TOGGLE = '<button class="whole-theme-toggle" type="button" aria-label="Toggle theme" aria-pressed="false" title="Toggle theme" data-whole-theme-toggle><span aria-hidden="true">◐</span></button>';

const THEME_HEAD = '<script>try{var t=localStorage.getItem("flove:theme");'
  + 'if(t==="light"||t==="dark"){document.documentElement.dataset.theme=t}'
  + 'else if(window.matchMedia&&matchMedia("(prefers-color-scheme: dark)").matches){document.documentElement.dataset.theme="dark"}}catch(e){}</script>';

const SPROUT = '<svg class="whole-sprout" viewBox="0 0 100 100" width="27" height="27" aria-hidden="true"><defs><linearGradient id="wholeSproutGrad" x1="12" y1="0" x2="88" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#ff3344"/><stop offset=".5" stop-color="#ff8a3a"/><stop offset="1" stop-color="#ffd633"/></linearGradient></defs><path d="M50 60C22 60 12 38 16 18C38 22 54 38 50 60Z" fill="url(#wholeSproutGrad)"/><path d="M50 60C78 60 88 38 84 18C62 22 46 38 50 60Z" fill="url(#wholeSproutGrad)"/><path d="M50 58C50 72 50 84 50 92" stroke="url(#wholeSproutGrad)" stroke-width="5" stroke-linecap="round" fill="none"/></svg>';

function header(root, active) {
  const cur = slug => active === slug ? ' aria-current="page"' : '';
  const home = `<a href="${root || './'}"${active === '' ? ' aria-current="page"' : ''}>Whole</a>`;
  const topLinks = home + TOP.map(([slug, name, key]) =>
    `<a href="${root}${slug}"${cur(key)}>${name}</a>`).join('');

  const parents = PARENTS.map(p => {
    const parentCurrent = active === p.key;
    const childCurrent = p.children.some(c => c.key === active);
    const kids = p.children.map(c => {
      const ccur = active === c.key ? ' aria-current="page"' : '';
      const small = c.small ? ` <small>${c.small}</small>` : '';
      return `<a href="${root}${c.slug}"${ccur}>${c.label}${small}</a>`;
    }).join('');
    const open = parentCurrent || childCurrent;
    return `<span class="whole-parent${open ? ' is-current is-open' : ''}">`
      + `<a class="whole-parent-link" href="${root}${p.slug}"${parentCurrent ? ' aria-current="page"' : ''}>${p.name}</a>`
      + `<div class="whole-child-menu" id="whole-sub-${p.key}"${open ? '' : ' hidden'}>${kids}</div></span>`;
  }).join('');

  const menu = `<a href="https://github.com/floveorg/floveorg.github.io/blob/main/whole/README.md" target="_blank" rel="noopener">About <small>wiki ↗</small></a>`
    + `<a href="https://github.com/floveorg/floveorg.github.io/tree/main/whole" target="_blank" rel="noopener">Download <small>GitHub ↗</small></a>`
    + `<a href="https://github.com/floveorg/floveorg.github.io/commits/main/whole" target="_blank" rel="noopener">Updates <small>recent changes ↗</small></a>`
    + `<span class="whole-menu__last">Last updated <time data-whole-updated>recently</time></span>`
    + `<div class="whole-menu__sep"></div><p class="whole-menu__k">Flove</p>`
    + `<a href="https://flove.org/docs/index.html">Docs</a>`
    + `<a href="https://flove.org/development/">Development</a>`
    + `<a href="https://flove.org/development/blog/">News</a>`
    + `<a href="https://flove.org/">Home</a>`;

  return `<header class="whole-top"><div class="whole-wrap whole-top__in">`
    + `<div class="whole-brand-wrap">`
    + `<button class="whole-brand" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="whole-menu" title="Menu">`
    + `<span class="whole-logo" aria-hidden="true">${SPROUT}</span><span class="whole-title">whole</span></button>`
    + `<div class="whole-menu" id="whole-menu" hidden>${menu}</div></div>`
    + `<nav class="whole-pages" aria-label="Wiki pages">${topLinks}${parents}</nav>`
    + `</div></header>`;
}

const PAGES = [
  ['', '', ''],
  ['metaphysics/', '../', 'metaphysics'],
  ['science/', '../', 'science'],
  ['biology/', '../', 'biology'],
  ['linguistics/', '../', 'linguistics'],
  ['psychosocial/', '../', 'psychosocial'],
  ['economy/', '../', 'economy'],
  ['linguistics/music/', '../../', 'music'],
];

for (const [slug, root, active] of PAGES) {
  const file = join(HERE, slug, 'index.html');
  let html = readFileSync(file, 'utf8');
  const h = header(root, active);
  if (/<header class="whole-top">[\s\S]*?<\/header>/.test(html)) {
    html = html.replace(/<header class="whole-top">[\s\S]*?<\/header>/, h);
  } else {
    html = html.replace(/(<body[^>]*>)/, `$1\n${h}`);
  }

  // §13.14 theme: resolve flove:theme before first paint, add a ◐ toggle after the page title.
  if (!/flove:theme/.test(html)) {
    html = html.replace('</head>', `${THEME_HEAD}\n</head>`);
  }
  if (!/name="theme-color"/.test(html)) {
    html = html.replace('<meta name="viewport"', '<meta name="theme-color" content="#fff8f1">\n<meta name="viewport"');
  }
  if (!/data-whole-theme-toggle/.test(html)) {
    const m = html.match(/<h1\b[^>]*>[\s\S]*?<\/h1>/);
    if (m) {
      const bare = /class="(?:sr-only|whole-sr-only)"/.test(m[0]);
      html = html.replace(m[0], `<div class="whole-title-row${bare ? ' whole-title-row--bare' : ''}">${m[0]}${THEME_TOGGLE}</div>`);
    } else {
      console.warn('no h1 for theme toggle →', file);
    }
  }

  writeFileSync(file, html);
  console.log('header →', file);
}
