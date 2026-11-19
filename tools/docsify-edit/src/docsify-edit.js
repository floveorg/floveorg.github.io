/* docsify-edit — in-browser WYSIWYG editor for docsify.
 *
 * A docsify plugin plus a tiny local save API. It stays invisible on a static
 * site: it pings the API and only then shows the Edit button.
 *
 * Edit → the rendered docsify article becomes contenteditable. Save → the DOM
 * is turned back into Markdown (turndown) and POSTed to the save API, which
 * writes the .md file and keeps a backup. Untouched blocks keep their original
 * source text (and line wrapping); only the blocks you actually edited are
 * re-serialized.
 *
 * Usage:
 *   <script src="vendor/docsify-edit.js"></script>
 *   window.$docsify = {
 *     edit: { endpoint: '/__edit' },
 *     plugins: [DocsifyEdit.plugin]
 *   };
 *
 * Markdown serialization uses Turndown (MIT) + turndown-plugin-gfm, both
 * configurable via edit.paths so they can be vendored or served from a CDN.
 */
(function (global) {
  'use strict';

  var VERSION = '1.0.0';

  var DEFAULTS = {
    endpoint: '/__edit',
    scope: null,
    paths: {
      turndown: 'vendor/turndown.min.js',
      gfm: 'vendor/turndown-plugin-gfm.min.js'
    },
    labels: {
      edit: '✎ Edit page',
      save: 'Save',
      cancel: 'Cancel',
      editing: 'Editing',
      saving: 'Saving',
      saved: 'Saved',
      unsaved: 'unsaved',
      nothing: 'Nothing to save.',
      hint: 'Edit mode — Ctrl+S saves, Esc cancels.'
    },
    width: 80,
    toolbar: true,
    reloadOnSave: true,
    allowRemote: false,
    unregisterServiceWorker: true,
    token: null,
    onSaved: null
  };

  var CFG = mergeConfig(null);

  var RAW_SELECTOR = 'div,section,figure,figcaption,details,summary,iframe,' +
                     'video,audio,svg,script,style';

  var state = {
    editing: false,
    dirty: false,
    saving: false,
    loading: false,
    article: null,
    pagePath: '',
    raw: '',
    bodyRaw: '',
    frontmatter: '',
    base: null,
    originalHTML: '',
    td: null,
    toolbar: null,
    status: null,
    openBtn: null,
    saveBtn: null,
    toastBox: null,
    vm: null,
    booted: false,
    rendering: false
  };

  function mergeConfig(vm) {
    var src = (vm && vm.config && vm.config.edit) ||
              (global.$docsify && global.$docsify.edit) || {};
    var out = {};
    for (var k in DEFAULTS) {
      if (!DEFAULTS.hasOwnProperty(k)) continue;
      out[k] = DEFAULTS[k];
    }
    for (var key in src) {
      if (!src.hasOwnProperty(key)) continue;
      if (key === 'paths' || key === 'labels') {
        out[key] = {};
        for (var a in DEFAULTS[key]) out[key][a] = DEFAULTS[key][a];
        if (src[key] && typeof src[key] === 'object') {
          for (var b in src[key]) out[key][b] = src[key][b];
        }
      } else {
        out[key] = src[key];
      }
    }
    return out;
  }

  function endpoints() {
    var base = String(CFG.endpoint || '/__edit').replace(/\/+$/, '');
    return { ping: base + '/ping', save: base + '/save' };
  }

  function authHeaders() {
    var h = {};
    if (CFG.token) h['X-Edit-Token'] = CFG.token;
    return h;
  }

  function copyHeaders(extra) {
    var h = authHeaders();
    if (extra) for (var k in extra) if (extra.hasOwnProperty(k)) h[k] = extra[k];
    return h;
  }

  // fetch, but never leave the UI waiting forever
  function request(url, options, timeoutMs) {
    options = options || {};
    if (typeof AbortController === 'undefined') return fetch(url, options);
    var controller = new AbortController();
    var timer = setTimeout(function () { controller.abort(); }, timeoutMs || 15000);
    options.signal = controller.signal;
    return fetch(url, options).then(function (res) {
      clearTimeout(timer);
      return res;
    }, function (err) {
      clearTimeout(timer);
      if (err && err.name === 'AbortError') throw new Error('the save server did not answer in time');
      throw err;
    });
  }

  function sha256(text) {
    try {
      if (!global.crypto || !global.crypto.subtle || typeof TextEncoder === 'undefined') {
        return Promise.resolve(null);
      }
      return global.crypto.subtle.digest('SHA-256', new TextEncoder().encode(text))
        .then(function (buf) {
          return Array.prototype.map.call(new Uint8Array(buf), function (b) {
            return ('0' + b.toString(16)).slice(-2);
          }).join('');
        })
        .catch(function () { return null; });
    } catch (e) {
      return Promise.resolve(null);
    }
  }


  /* ---------- tiny helpers ------------------------------------------- */

  function el(tag, attrs, text) {
    var n = document.createElement(tag);
    if (attrs) { for (var k in attrs) if (attrs.hasOwnProperty(k)) n.setAttribute(k, attrs[k]); }
    if (text != null) n.textContent = text;
    return n;
  }

  function on(target, type, fn, capture) {
    target.addEventListener(type, fn, !!capture);
    return function () { target.removeEventListener(type, fn, !!capture); };
  }

  function toast(message, bad) {
    if (!state.toastBox) {
      state.toastBox = el('div', { id: 'docsify-edit-toast', role: 'status', 'aria-live': 'polite' });
      document.body.appendChild(state.toastBox);
    }
    var box = state.toastBox;
    box.textContent = message;
    box.className = bad ? 'is-bad is-on' : 'is-on';
    clearTimeout(box._timer);
    box._timer = setTimeout(function () { box.className = ''; }, bad ? 6000 : 2800);
  }

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = src;
      s.onload = function () { resolve(); };
      s.onerror = function () { reject(new Error('could not load ' + src)); };
      document.head.appendChild(s);
    });
  }

  function currentPath() {
    var vm = state.vm;
    if (vm && vm.route && typeof vm.route.path === 'string') {
      var route = vm.route.path.replace(/^\//, '').split('?')[0];
      if (!route) route = (vm.config && vm.config.homepage) || 'README.md';
      try { route = decodeURIComponent(route); } catch (e) {}
      return route.replace(/\.md$/i, '') + '.md';
    }
    var hash = location.hash.replace(/^#/, '').replace(/^\//, '');
    hash = hash.split('?')[0];
    try { hash = decodeURIComponent(hash); } catch (e) {}
    if (!hash) hash = (global.$docsify && global.$docsify.homepage) || 'README.md';
    return hash.replace(/\.md$/i, '') + '.md';
  }

  function rawUrl(pagePath) {
    var base = location.href.split('#')[0];
    var u = new URL(pagePath, base);
    u.searchParams.set('_', String(Date.now()));
    return u.href;
  }

  function escapeHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  /* ---------- block-level markdown helpers --------------------------- */

  // Lines that belong to a list item, its indented continuation, or a quote.
  function continuesBlock(line) {
    return /^\s{0,3}([-*+]|\d+[.)])\s+/.test(line) ||
           /^( {2,}|\t)\S/.test(line) ||
           /^\s{0,3}>/.test(line);
  }

  // headings outside fenced code — used to check the article is the right page
  function headingTexts(md) {
    var out = [];
    var fence = null;
    var lines = String(md).replace(/\r\n/g, '\n').split('\n');
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i];
      var f = line.match(/^ {0,3}(`{3,}|~{3,})/);
      if (fence) {
        if (f && f[1].charAt(0) === fence.charAt(0) && f[1].length >= fence.length) fence = null;
        continue;
      }
      if (f) { fence = f[1]; continue; }
      var h = line.match(/^#{1,6}\s+(.+)$/);
      if (h) out.push(h[1]);
    }
    return out;
  }

  // Split markdown into top-level blocks, keeping fenced code blocks whole and
  // blank lines inside loose lists / multi-paragraph quotes with their block.
  function splitBlocks(md) {
    var lines = md.replace(/\r\n/g, '\n').split('\n');
    var blocks = [];
    var cur = [];
    var fence = null;

    function push() {
      if (cur.length) { blocks.push(cur.join('\n')); cur = []; }
    }

    function blankKeepsBlock(blankAt) {
      var last = '', next = '';
      for (var a = cur.length - 1; a >= 0; a--) {
        if (!/^\s*$/.test(cur[a])) { last = cur[a]; break; }
      }
      for (var b = blankAt + 1; b < lines.length; b++) {
        if (!/^\s*$/.test(lines[b])) { next = lines[b]; break; }
      }
      if (!cur.length || next === '') return false;
      // loose lists and multi-paragraph quotes
      if (continuesBlock(last) && continuesBlock(next)) return true;
      var isList = function (l) { return /^\s{0,3}([-*+]|\d+[.)])\s+/.test(l); };
      var isPlain = function (l) {
        return !/^\s{0,3}(#{1,6}\s|>|\||[-*+]\s|\d+[.)]\s|<|`{3,}|~{3,})/.test(l);
      };
      var first = '';
      for (var f = 0; f < cur.length; f++) {
        if (cur[f].trim()) { first = cur[f]; break; }
      }
      // a plain paragraph immediately followed by a list is one source block
      // when the author left no blank line; turndown always inserts one, so
      // merge both sides to keep the original text
      if (isList(next) && isPlain(last) && isPlain(first)) return true;
      return false;
    }

    for (var i = 0; i < lines.length; i++) {
      var line = lines[i];
      var m = line.match(/^ {0,3}(`{3,}|~{3,})/);
      if (fence) {
        cur.push(line);
        if (m && m[1].charAt(0) === fence.charAt(0) && m[1].length >= fence.length) {
          fence = null;
          push(); // a fence is always its own block
        }
        continue;
      }
      if (m) { push(); fence = m[1]; cur.push(line); continue; }
      if (/^\s*$/.test(line)) {
        if (blankKeepsBlock(i)) { cur.push(line); continue; }
        push();
        continue;
      }
      cur.push(line);
    }
    push();
    return blocks;
  }

  function normBlock(s) {
    // compare content, not formatting: blockquote markers, link depth,
    // table padding and line wrapping are all allowed to differ
    s = s.replace(/^ {0,3}>\s?/gm, '');
    s = s.replace(/^(\s*)\d+[.)]\s+/gm, '$1- ');
    s = s.replace(/\\/g, '');
    s = s.replace(/\]\(([^)\s]*)\)/g, function (m, url) {
      return '](' + url.replace(/(?:\.\.\/|\.\/)+/g, '').replace(/^#\//, '') + ')';
    });
    // compare the visible text, not link/image punctuation
    s = s.replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1');
    s = s.replace(/\[([^\]]*)\]\([^)]*\)/g, '$1');
    s = s.split('\n').map(function (line) {
      if (/^\s*\|[\s:|-]+\|\s*$/.test(line)) {
        return line.replace(/\s+/g, '').replace(/:?-+:?/g, '-');
      }
      return /^\s*\|/.test(line) ? line.replace(/\s+/g, '') : line;
    }).join('\n');
    return s
      .replace(/\s+/g, ' ')
      .replace(/[*_`]{1,2}/g, '')   // __x__, **x** and `x` compare equal
      .trim();
  }

  // Greedy wrap for plain paragraphs only; tables, lists, code, HTML and
  // hard-break blocks are left exactly as produced.
  function wrapPlain(block) {
    if (/^\s{0,3}(#{1,6}\s|[-*+]\s|\d+[.)]\s|>|\||<|`{3,}|~{3,})/.test(block)) return block;
    if (/^( {4}|\t)/.test(block)) return block;
    if (/\n\s*\n/.test(block)) return block;       // more than one block inside
    if (/ {2,}\n|\\\n/.test(block)) return block; // explicit hard breaks
    var words = block.split(/\s+/).filter(Boolean);
    var out = [];
    var line = '';
    for (var i = 0; i < words.length; i++) {
      var w = words[i];
      if (!line) line = w;
      else if ((line + ' ' + w).length <= (CFG.width || 80)) line += ' ' + w;
      else { out.push(line); line = w; }
    }
    if (line) out.push(line);
    return out.join('\n');
  }

  // Join each original block to the exact whitespace run that followed it, so
  // blank-line spacing survives a save untouched.
  function withGaps(md, blocks) {
    var pos = 0;
    var out = [];
    for (var i = 0; i < blocks.length; i++) {
      var at = md.indexOf(blocks[i], pos);
      if (at < 0) { out.push({ text: blocks[i], gap: '\n\n' }); continue; }
      var end = at + blocks[i].length;
      var next = i + 1 < blocks.length ? md.indexOf(blocks[i + 1], end) : md.length;
      if (next < 0) next = md.length;
      out.push({ text: blocks[i], gap: md.slice(end, next) });
      pos = end;
    }
    return out;
  }

  // Match a generated chunk against a run of original blocks (one block for a
  // paragraph, several for a loose list or a multi-paragraph blockquote).
  function matchRun(orig, start, chunk, loose) {
    var target = loose ? looseNorm(chunk) : normBlock(chunk);
    var acc = '';
    for (var n = 0; n < 20 && start + n < orig.length; n++) {
      acc += (n ? '\n\n' : '') + orig[start + n].text;
      var key = loose ? looseNorm(acc) : normBlock(acc);
      if (key === target) return n + 1;
      if (key.length > target.length + 80) break;
    }
    return 0;
  }

  function looseNorm(s) {
    return normBlock(s).replace(/[\s`]+/g, '');
  }

  function restoreHrefsFromOriginal(chunk, originalBlock) {
    if (!originalBlock) return chunk;
    var map = {};
    var re = /\[([^\]]*)\]\(([^)]+)\)/g;
    var m;
    while ((m = re.exec(originalBlock))) map[m[1]] = m[2];
    if (!Object.keys(map).length) return chunk;
    return chunk.replace(/\[([^\]]*)\]\(([^)]+)\)/g, function (all, text, href) {
      return map.hasOwnProperty(text) ? '[' + text + '](' + map[text] + ')' : all;
    });
  }

  function blockKind(s) {
    var t = s.replace(/^\s+/, '');
    if (/^#{1,6}\s/.test(t)) return 'h';
    if (/^\|/.test(t)) return 'table';
    if (/^(```|~~~)/.test(t)) return 'code';
    if (/^>/.test(t)) return 'quote';
    if (/^([-*+]|\d+[.)])\s/.test(t)) return 'list';
    if (/^</.test(t)) return 'html';
    if (/^(-{3,}|\*{3,}|_{3,})\s*$/.test(t)) return 'hr';
    return 'p';
  }

  function normalizeListMarkers(md) {
    return md
      .replace(/^(\s*)[-*+] {2,}/gm, '$1- ')
      .replace(/^(\s*\d+)\. {2,}/gm, '$1. ')
      .replace(/^(\s*[-*+] )\[([ x])\] +/gm, '$1[$2] ');
  }

  function serialize(article, force) {
    // nothing touched → the file on disk is already correct; return it byte
    // for byte (this also makes a stray Ctrl+S / synthetic input a no-op)
    var touched = [];
    Array.prototype.slice.call(article.children).forEach(function (node) {
      if (!node.hasAttribute('data-docsify-edit-touched')) return;
      var t = normBlock(node.textContent || '');
      if (t) touched.push(t);
    });
    if (!touched.length && !force && !window.__docsifyEditForce) return state.raw;

    var clone = article.cloneNode(true);
    normalizeEditorBlocks(clone);

    // cloneNode copies the checked *attribute*, not the live property; sync it
    // so a checkbox the author toggled is written as [x] / [ ] correctly
    var liveBoxes = article.querySelectorAll('input[type="checkbox"]');
    var copyBoxes = clone.querySelectorAll('input[type="checkbox"]');
    for (var b = 0; b < liveBoxes.length && b < copyBoxes.length; b++) {
      if (liveBoxes[b].checked) copyBoxes[b].setAttribute('checked', '');
      else copyBoxes[b].removeAttribute('checked');
    }

    var orig = withGaps(state.bodyRaw, splitBlocks(state.bodyRaw));
    var generated = state.td.turndown(clone).replace(/\n{3,}/g, '\n\n').trim();
    var gen = splitBlocks(generated);

    function isTouched(block) {
      if (!touched.length) return false;
      var key = normBlock(block);
      for (var t = 0; t < touched.length; t++) {
        if (touched[t].length >= 4 && key.indexOf(touched[t]) !== -1) return true;
      }
      return false;
    }

    var j = 0;
    var out = '';

    for (var i = 0; i < gen.length; i++) {
      var block = gen[i];
      var key = normBlock(block);
      if (!key) continue;

      var touchedBlock = isTouched(block);
      // a touched block is always re-serialized — loose matching would drop
      // formatting-only edits (e.g. bold)
      var n = touchedBlock ? 0 : matchRun(orig, j, block, false);
      if (!n && !touchedBlock) n = matchRun(orig, j, block, true);

      if (n) {
        for (var k = 0; k < n; k++) out += orig[j + k].text + orig[j + k].gap;
        j += n;
        continue;
      }

      // This block was edited, inserted or unrecognisable. Before emitting it,
      // move the original pointer past whatever it replaced, using the next
      // block as the anchor.
      var skip = 0;
      var inserted = false;
      var next = gen[i + 1];
      if (next) {
        if (matchRun(orig, j, next, false)) {
          inserted = true; // the next block still lines up: this one is new
        } else {
          for (var s = 1; s <= 4 && j + s < orig.length; s++) {
            if (matchRun(orig, j + s, next, false)) { skip = s; break; }
          }
        }
      }
      if (!inserted && !skip && orig[j] && blockKind(block) === blockKind(orig[j].text)) skip = 1;

      // Reuse the original href for any link whose text survived the edit, so
      // a paragraph edit cannot re-base repo-relative links.
      var source = '';
      if (skip > 0) {
        for (var q = 0; q < skip && j + q < orig.length; q++) {
          source += (q ? '\n\n' : '') + orig[j + q].text;
        }
      }
      j = Math.min(j + skip, orig.length);

      if (out && !/\n\n$/.test(out)) out = out.replace(/\n+$/, '') + '\n\n';
      out += wrapPlain(normalizeListMarkers(source ? restoreHrefsFromOriginal(block, source) : block)) + '\n\n';
    }

    out = out.replace(/^\n+|\n+$/g, '');
    return (state.frontmatter ? state.frontmatter.replace(/\n*$/, '\n\n') : '') + out + '\n';
  }

  /* ---------- markdown serialization --------------------------------- */

  function codeText(root) {
    var out = '';
    (function walk(n) {
      if (n.nodeType === 3) out += n.nodeValue.replace(/\u200b/g, '');
      else if (n.nodeName === 'BR') out += '\n';
      else if (n.nodeType === 1) {
        for (var c = n.firstChild; c; c = c.nextSibling) walk(c);
      }
    })(root);
    return out;
  }

  function addRules(td) {
    // docsify code blocks: <pre v-pre data-lang="js"><code class="lang-js">
    td.addRule('docsifyEditCodeBlock', {
      filter: 'pre',
      replacement: function (content, node) {
        var code = node.querySelector('code') || node;
        var lang = node.getAttribute('data-lang') || '';
        if (!lang && code.className) {
          var m = code.className.match(/(?:lang|language)-([\w+-]+)/);
          if (m) lang = m[1];
        }
        if (lang === 'markup') lang = '';
        var text = codeText(code).replace(/\n$/, '');
        var fence = '```';
        while (text.indexOf(fence) !== -1) fence += '`';
        return '\n\n' + fence + lang + '\n' + text + '\n' + fence + '\n\n';
      }
    });

    // docsify rewrites relative links to router hashes; put them back.
    td.addRule('docsifyEditLink', {
      filter: function (node) { return node.nodeName === 'A' && node.getAttribute('href'); },
      replacement: function (content, node) {
        var href = restoreHref(node.getAttribute('href'));
        var title = node.getAttribute('title');
        return '[' + content + '](' + href + (title ? ' "' + title.replace(/"/g, '\\"') + '"' : '') + ')';
      }
    });

    // images carry data-origin, the exact src written in the markdown
    td.addRule('docsifyEditImage', {
      filter: 'img',
      replacement: function (content, node) {
        var src = node.getAttribute('data-origin') || node.getAttribute('src') || '';
        var alt = node.getAttribute('alt') || '';
        var title = node.getAttribute('title');
        if (/\s/.test(src) && src.charAt(0) !== '<') src = '<' + src + '>';
        return '![' + alt + '](' + src + (title ? ' "' + title + '"' : '') + ')';
      }
    });

    // HTML comments (used as ↗ pendings markers in this wiki)
    td.addRule('docsifyEditComment', {
      filter: function (node) { return node.nodeName === 'SPAN' && node.hasAttribute('data-md-comment'); },
      replacement: function (content, node) {
        return '<!--' + node.getAttribute('data-md-comment') + '-->';
      }
    });

    // raw HTML blocks present before editing: emit them verbatim
    td.addRule('docsifyEditRawBlock', {
      filter: function (node) { return node.nodeName !== '#text' && node.hasAttribute && node.hasAttribute('data-docsify-edit-raw'); },
      replacement: function (content, node) {
        var clone = node.cloneNode(true);
        var marked = clone.querySelectorAll('[data-docsify-edit-raw]');
        for (var i = 0; i < marked.length; i++) marked[i].removeAttribute('data-docsify-edit-raw');
        clone.removeAttribute('data-docsify-edit-raw');
        if (clone.removeAttribute) clone.removeAttribute('data-docsify-edit-touched');
        var touched = clone.querySelectorAll('[data-docsify-edit-touched]');
        for (var t = 0; t < touched.length; t++) touched[t].removeAttribute('data-docsify-edit-touched');
        return '\n\n' + clone.outerHTML + '\n\n';
      }
    });
  }

  function posixRelative(fromDir, to) {
    var a = fromDir.split('/').filter(Boolean);
    var b = to.split('/').filter(Boolean);
    var i = 0;
    while (i < a.length && i < b.length && a[i] === b[i]) i++;
    var parts = [];
    for (var k = i; k < a.length; k++) parts.push('..');
    for (var m = i; m < b.length; m++) parts.push(b[m]);
    return parts.join('/') || b[b.length - 1] || '';
  }

  function restoreHref(href) {
    if (!href) return '';
    if (/^(https?:|mailto:|tel:|\+)/i.test(href)) return href;
    if (href.charAt(0) === '#') {
      var m = href.match(/^#\/(.*)$/);
      if (!m) return href; // in-page anchor
      var target = m[1];
      var query = '';
      var qi = target.indexOf('?');
      if (qi >= 0) { query = target.slice(qi); target = target.slice(0, qi); }
      if (!target) target = (window.$docsify && window.$docsify.homepage) || 'overview.md';
      if (!/\.[a-z0-9]+$/i.test(target) && !/\/$/.test(target)) target += '.md';
      target = target.replace(/^\//, '');
      var frag = '';
      var id = /(?:^|[?&])id=([^&]+)/.exec(query);
      if (id) frag = '#' + decodeURIComponent(id[1]);
      if (frag && target === state.pagePath) return frag;
      var fromDir = state.pagePath.replace(/[^\/]*$/, '');
      return posixRelative(fromDir, target) + frag;
    }
    return href;
  }

  function buildTurndown() {
    var td = new window.TurndownService({
      headingStyle: 'atx',
      hr: '---',
      bulletListMarker: '-',
      codeBlockStyle: 'fenced',
      fence: '```',
      emDelimiter: '*',
      strongDelimiter: '**',
      linkStyle: 'inlined'
    });
    if (window.turndownPluginGfm && window.turndownPluginGfm.gfm) {
      td.use(window.turndownPluginGfm.gfm);
    }
    addRules(td);
    return td;
  }

  /* ---------- DOM preparation ---------------------------------------- */

  function stripRenderedFrontmatter(article) {
    // docsify renders the YAML block as <hr>, paragraph(s), <hr>; it is not
    // part of the editable body (the original text is re-attached on save).
    var nodes = Array.prototype.slice.call(article.childNodes);
    var i = 0;
    while (i < nodes.length && nodes[i].nodeType === 3 && !nodes[i].textContent.trim()) i++;
    if (!nodes[i] || nodes[i].nodeName !== 'HR') return false;
    var end = -1;
    for (var k = i + 1; k < Math.min(nodes.length, i + 30); k++) {
      if (nodes[k].nodeName === 'HR') { end = k; break; }
    }
    if (end < 0) return false;
    for (var m = i; m <= end; m++) nodes[m].parentNode.removeChild(nodes[m]);
    return true;
  }

  function unwrapTaskLabels(root) {
    Array.prototype.slice.call(root.querySelectorAll('li.task-list-item label')).forEach(function (label) {
      if (!label.querySelector('input[type="checkbox"]')) return;
      var parent = label.parentNode;
      while (label.firstChild) parent.insertBefore(label.firstChild, label);
      parent.removeChild(label);
    });
  }

  function commentsToSpans(root) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_COMMENT, null);
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function (c) {
      // comments inside raw HTML blocks are emitted verbatim with the block
      if (c.parentNode.closest && c.parentNode.closest('[data-docsify-edit-raw]')) return;
      var s = el('span', { class: 'docsify-edit-comment', 'data-md-comment': c.nodeValue }, '\u200b');
      // a top-level comment belongs to the block above it (usually an inline
      // ↗ pendings marker): keep it there so a paragraph match preserves it
      if (c.parentNode === root) {
        var prev = c.previousSibling;
        while (prev && prev.nodeType === 3 && !prev.nodeValue.trim()) prev = prev.previousSibling;
        if (prev && prev.nodeType === 1 && /^(P|H[1-6])$/.test(prev.nodeName)) {
          prev.appendChild(s);
          root.removeChild(c);
          return;
        }
      }
      if (c.parentNode) c.parentNode.replaceChild(s, c);
    });
  }

  function prepareArticle(article) {
    // unwrap docsify's heading anchors so the text is directly editable
    Array.prototype.slice.call(article.querySelectorAll('a.anchor')).forEach(function (a) {
      var parent = a.parentNode;
      while (a.firstChild) parent.insertBefore(a.firstChild, a);
      parent.removeChild(a);
    });

    // copy-code buttons are UI, not content
    Array.prototype.slice.call(article.querySelectorAll('button, .docsify-copy-code-button'))
      .forEach(function (b) { b.remove(); });

    // remember which elements are raw HTML written in the markdown
    Array.prototype.slice.call(article.querySelectorAll(RAW_SELECTOR)).forEach(function (n) {
      n.setAttribute('data-docsify-edit-raw', '');
    });

    // Prism's token spans are presentational: flatten them so the code block
    // is plain editable text (the highlighter runs again after reload).
    Array.prototype.slice.call(article.querySelectorAll('pre code .token')).forEach(function (s) {
      var parent = s.parentNode;
      while (s.firstChild) parent.insertBefore(s.firstChild, s);
      parent.removeChild(s);
    });

    // task-list checkboxes become clickable while editing
    Array.prototype.slice.call(article.querySelectorAll('input[type="checkbox"]'))
      .forEach(function (i) { i.removeAttribute('disabled'); });

    unwrapTaskLabels(article);
    commentsToSpans(article);
  }

  // Chrome inserts <div> on Enter in contenteditable; turn those into <p>.
  function normalizeEditorBlocks(clone) {
    unwrapTaskLabels(clone);
    var divs = Array.prototype.slice.call(clone.querySelectorAll('div')).reverse();
    divs.forEach(function (d) {
      if (d.hasAttribute('data-docsify-edit-raw') || (d.closest && d.closest('[data-docsify-edit-raw]'))) return;
      if (d.querySelector('p,div,ul,ol,h1,h2,h3,h4,h5,h6,blockquote,pre,table,section,figure')) {
        while (d.firstChild) d.parentNode.insertBefore(d.firstChild, d);
        d.remove();
      } else {
        var p = el('p');
        while (d.firstChild) p.appendChild(d.firstChild);
        if (!p.textContent.trim() && !p.querySelector('img,br,input')) { d.remove(); return; }
        d.parentNode.replaceChild(p, d);
      }
    });
  }

  /* ---------- UI ------------------------------------------------------ */

  function injectStyles() {
    if (document.getElementById('docsify-edit-styles')) return;
    var css = [
      '#docsify-edit-open{position:fixed;right:18px;bottom:18px;z-index:9998;',
      'font:600 13px/1 "Spectral",Georgia,serif;letter-spacing:.02em;',
      'background:#0c0b18;color:#f6efdc;border:1px solid #c39a45;border-radius:999px;',
      'padding:11px 17px;cursor:pointer;box-shadow:0 6px 22px rgba(12,11,24,.24)}',
      '#docsify-edit-open:hover{background:#c39a45;color:#0c0b18}',
      '#docsify-edit-bar{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);',
      'z-index:9999;display:none;align-items:center;gap:6px;max-width:calc(100vw - 24px);',
      'overflow-x:auto;padding:8px 10px;border-radius:14px;background:#fbf7ec;',
      'border:1px solid #c39a45;box-shadow:0 10px 34px rgba(12,11,24,.28);',
      'font:500 13px/1.2 "Spectral",Georgia,serif;color:#0c0b18}',
      'body.docsify-editing #docsify-edit-bar{display:flex}',
      'body.docsify-editing{padding-bottom:110px}',
      'body.docsify-editing #docsify-edit-open{display:none}',
      '#docsify-edit-bar button{font:600 12px/1 "Spectral",Georgia,serif;color:#0c0b18;',
      'background:#fffdf7;border:1px solid #d9cba5;border-radius:8px;padding:8px 9px;',
      'cursor:pointer;min-width:32px}',
      '#docsify-edit-bar button:hover{background:#f1e6cc;border-color:#c39a45}',
      '#docsify-edit-bar button.primary{background:#0c0b18;color:#f6efdc;border-color:#0c0b18}',
      '#docsify-edit-bar button.primary:hover{background:#c39a45;color:#0c0b18}',
      '#docsify-edit-status{font:600 12px/1.3 "Spectral",Georgia,serif;color:#6f6596;',
      'white-space:nowrap;padding:0 8px;max-width:38vw;overflow:hidden;text-overflow:ellipsis}',
      '#docsify-edit-status b{color:#0c0b18;font-weight:600}',
      '#docsify-edit-bar .sep{width:1px;align-self:stretch;background:#e6dcc0;margin:0 3px}',
      '#docsify-edit-toast{position:fixed;left:50%;bottom:76px;transform:translateX(-50%);',
      'z-index:10000;background:#0c0b18;color:#f6efdc;padding:10px 16px;border-radius:10px;',
      'font:500 13px/1.4 "Spectral",Georgia,serif;box-shadow:0 8px 28px rgba(12,11,24,.3);',
      'opacity:0;pointer-events:none;transition:opacity .18s;max-width:86vw;text-align:center}',
      '#docsify-edit-toast.is-on{opacity:1}',
      '#docsify-edit-toast.is-bad{background:#7c1d2b}',
      '.markdown-section.docsify-editable{outline:2px dashed #c39a45;outline-offset:12px;',
      'background:#fffdf7;caret-color:#0c0b18}',
      '.markdown-section.docsify-editable [data-md-comment]{display:none}',
      'body.docsify-editing .markdown-section a{cursor:text}'
    ].join('\n');
    var style = el('style', { id: 'docsify-edit-styles' });
    style.textContent = css;
    document.head.appendChild(style);
  }

  function buildToolbar() {
    if (state.toolbar) return;
    var bar = el('div', { id: 'docsify-edit-bar', role: 'toolbar', 'aria-label': 'Editor' });
    state.status = el('span', { id: 'docsify-edit-status', 'aria-live': 'polite' });

    var tools = [
      ['bold', 'b', 'Bold', '<b>B</b>'],
      ['italic', 'i', 'Italic', '<i>I</i>'],
      ['h2', 'h2', 'Heading 2', 'H2'],
      ['h3', 'h3', 'Heading 3', 'H3'],
      ['ul', 'ul', 'Bulleted list', '•'],
      ['ol', 'ol', 'Numbered list', '1.'],
      ['quote', 'quote', 'Quote', '❝'],
      ['code', 'code', 'Inline code', '&lt;/&gt;'],
      ['link', 'link', 'Link', '🔗'],
      ['undo', 'undo', 'Undo', '↶'],
      ['redo', 'redo', 'Redo', '↷']
    ];

    bar.appendChild(state.status);
    if (CFG.toolbar) {
      bar.appendChild(el('span', { class: 'sep' }));
      tools.forEach(function (t) {
        var b = el('button', { type: 'button', 'data-act': t[0], title: t[2], 'aria-label': t[2] });
        b.innerHTML = t[3];
        bar.appendChild(b);
      });
    }

    bar.appendChild(el('span', { class: 'sep' }));
    var cancelBtn = el('button', { type: 'button', 'data-act': 'cancel' }, CFG.labels.cancel);
    state.saveBtn = el('button', { type: 'button', 'data-act': 'save', class: 'primary' }, CFG.labels.save);
    bar.appendChild(cancelBtn);
    bar.appendChild(state.saveBtn);

    bar.addEventListener('mousedown', function (e) {
      // keep the caret/selection when pressing a toolbar button
      if (e.target.closest('button')) { e.preventDefault(); saveSelection(); }
    });
    bar.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      var act = b.getAttribute('data-act');
      if (act === 'save') { save(); return; }
      if (act === 'cancel') { cancel(); return; }
      if (act === 'link') { insertLink(); return; }
      if (act === 'code') { insertCode(); return; }
      if (act === 'h2' || act === 'h3') { exec('formatBlock', '<' + act + '>'); return; }
      if (act === 'quote') { exec('formatBlock', '<blockquote>'); return; }
      if (act === 'ul') { exec('insertUnorderedList'); return; }
      if (act === 'ol') { exec('insertOrderedList'); return; }
      exec(act);
    });

    state.toolbar = bar;
    document.body.appendChild(bar);
  }

  function exec(cmd, arg) {
    var article = state.article;
    if (!article) return;
    article.focus();
    restoreSelection();
    try { document.execCommand('styleWithCSS', false, false); } catch (e) {}
    try { document.execCommand(cmd, false, arg || null); } catch (e) {}
    markDirty();
    markTouched();
  }

  var savedRange = null;
  function saveSelection() {
    var sel = window.getSelection();
    savedRange = sel && sel.rangeCount ? sel.getRangeAt(0).cloneRange() : null;
  }
  function restoreSelection() {
    if (!savedRange) return;
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(savedRange);
  }

  function insertLink() {
    var sel = window.getSelection();
    var text = sel ? sel.toString() : '';
    var href = window.prompt('Link URL', 'https://');
    if (!href) return;
    if (!text) text = href;
    exec('insertHTML', '<a href="' + escapeHtml(href) + '">' + escapeHtml(text) + '</a>');
  }

  function insertCode() {
    var sel = window.getSelection();
    if (!sel || !sel.rangeCount) return;
    var text = sel.toString();
    exec('insertHTML', '<code>' + escapeHtml(text || 'code') + '</code>');
  }

  function setStatus(text) {
    if (!state.status) return;
    state.status.innerHTML = text;
  }

  function markDirty() {
    if (!state.editing) return;
    if (!state.dirty) {
      state.dirty = true;
      setStatus('Editing <b>' + escapeHtml(state.pagePath) + '</b> · unsaved');
    }
  }

  // Remember which top-level block the caret was in, so a save never
  // re-serializes a block the author did not touch.
  function markTouched() {
    if (!state.article) return;
    var sel = window.getSelection();
    if (!sel || !sel.rangeCount) return;
    var node = sel.anchorNode;
    var elem = node && (node.nodeType === 1 ? node : node.parentElement);
    var block = elem && elem.closest ? elem.closest('.markdown-section > *') : null;
    if (block && state.article.contains(block)) block.setAttribute('data-docsify-edit-touched', '');
  }

  function onInput(e) {
    markDirty();
    var el = e && e.target;
    if (el && el !== state.article && el.nodeType === 1 && el.closest) {
      var block = el.closest('.markdown-section > *');
      if (block) { block.setAttribute('data-docsify-edit-touched', ''); return; }
    }
    markTouched();
  }

  var blockNav = null;
  var beforeUnload = null;
  var keyNav = null;

  function enterEdit(article) {
    if (state.editing || state.loading) return;
    if (state.rendering) { toast('The page is still rendering — try again in a moment.'); return; }
    state.loading = true;
    state.pagePath = currentPath();
    state.article = article;
    state.dirty = false;
    state.saving = false;
    setStatus('Loading <b>' + escapeHtml(state.pagePath) + '</b>…');

    request(rawUrl(state.pagePath), { cache: 'no-store' }, 15000)
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.text(); })
      .then(function (raw) {
        if (currentPath() !== state.pagePath) {
          throw new Error('the page changed while opening the editor — try again');
        }
        var fm = raw.match(/^---\r?\n([\s\S]*?)\r?\n---[ \t]*\r?\n/);
        if (fm && fm[1].indexOf(':') !== -1) {
          state.frontmatter = raw.slice(0, fm[0].length);
          state.bodyRaw = raw.slice(fm[0].length);
        } else {
          state.frontmatter = '';
          state.bodyRaw = raw;
        }
        state.raw = raw;
        // docsify renders asynchronously: don't edit a stale article during a
        // fast sidebar click. Its first headings must already be on screen.
        var titles = headingTexts(state.bodyRaw).slice(0, 2).map(function (t) {
          return t.replace(/[*_`\[\]]/g, '').trim().slice(0, 24);
        }).filter(Boolean);
        for (var ti = 0; ti < titles.length; ti++) {
          if (article.textContent.indexOf(titles[ti]) === -1) {
            throw new Error('the page is still rendering — try again in a moment');
          }
        }
        return sha256(raw).then(function (hash) {
          state.base = hash;
        }).then(ensureLibs);
      })
      .then(function () {
        if (!window.TurndownService) throw new Error('markdown engine missing');
        state.td = buildTurndown();
        state.originalHTML = article.innerHTML;
        if (state.frontmatter && !stripRenderedFrontmatter(article)) {
          throw new Error('could not isolate this page’s YAML front-matter');
        }
        prepareArticle(article);
        article.classList.add('docsify-editable');
        article.setAttribute('contenteditable', 'true');
        article.setAttribute('spellcheck', 'true');
        article.setAttribute('aria-label', CFG.labels.editing + ' ' + state.pagePath);
        article.setAttribute('role', 'textbox');
        article.setAttribute('aria-multiline', 'true');
        document.body.classList.add('docsify-editing');
        try { document.execCommand('defaultParagraphSeparator', false, 'p'); } catch (e) {}

        article.addEventListener('input', onInput);
        article.addEventListener('change', onInput);
        article.addEventListener('paste', onPaste);
        blockNav = on(document, 'click', function (e) {
          var a = e.target.closest && e.target.closest('a');
          if (!a || a.closest('#docsify-edit-bar') || a.closest('#docsify-edit-open')) return;
          var href = a.getAttribute('href') || '';
          if (href.charAt(0) === '#' || /\.md($|\?)/i.test(href)) {
            e.preventDefault();
            e.stopPropagation();
            toast('Save or cancel the edit first.');
          }
        }, true);
        beforeUnload = on(window, 'beforeunload', function (e) {
          if (state.editing && state.dirty) { e.preventDefault(); e.returnValue = ''; return ''; }
        });
        keyNav = on(document, 'keydown', onKey);
        // If the router still moves (Back button, a programmatic hash change),
        // drop the edit and let docsify render. Never reload from here: a
        // reload can itself re-trigger the router and turn into a loop.
        on(window, 'hashchange', function () {
          if (state.editing) discardEdit();
        });

        state.editing = true;
        state.loading = false;
        state.dirty = false;
        if (window.__docsifyEditDebug) {
          window.__docsifyEdit = {
            path: function () { return state.pagePath; },
            serialize: function () { return serialize(state.article, true); }
          };
        }
        setStatus(CFG.labels.editing + ' <b>' + escapeHtml(state.pagePath) + '</b>');
        toast(CFG.labels.hint);
        var first = article.querySelector('h1, h2, p');
        if (first) { try { article.focus(); } catch (e) {} }
      })
      .catch(function (err) {
        state.loading = false;
        setStatus('');
        toast('Could not start the editor: ' + err.message, true);
      });
  }

  function ensureLibs() {
    var chain = Promise.resolve();
    if (!window.TurndownService) {
      chain = chain.then(function () { return loadScript(CFG.paths.turndown); });
    }
    if (!window.turndownPluginGfm) {
      chain = chain.then(function () { return loadScript(CFG.paths.gfm); });
    }
    return chain;
  }

  function onPaste(e) {
    if (!state.editing) return;
    var text = e.clipboardData && e.clipboardData.getData('text/plain');
    if (text == null) return;
    e.preventDefault();
    try { document.execCommand('insertText', false, text); } catch (err) {}
  }

  function onKey(e) {
    if (!state.editing) return;
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 's') {
      e.preventDefault();
      save();
      return;
    }
    if (e.key === 'Escape') {
      e.preventDefault();
      cancel();
      return;
    }
    // Inside a code block, Enter and Tab should insert text, not leave it.
    var sel = window.getSelection();
    var node = sel && sel.rangeCount ? sel.anchorNode : null;
    var el = node && (node.nodeType === 1 ? node : node.parentElement);
    var pre = el && el.closest ? el.closest('pre') : null;
    if (pre && state.article && state.article.contains(pre)) {
      if (e.key === 'Enter') {
        e.preventDefault();
        insertCodeBreak();
        return;
      }
      if (e.key === 'Tab') {
        e.preventDefault();
        insertTextAtCaret('  ');
      }
    }
  }

  function insertCodeBreak() {
    var sel = window.getSelection();
    if (!sel || !sel.rangeCount) return;
    var range = sel.getRangeAt(0);
    range.deleteContents();
    var br = document.createElement('br');
    var zero = document.createTextNode('\u200b');
    range.insertNode(br);
    br.parentNode.insertBefore(zero, br.nextSibling);
    var after = document.createRange();
    after.setStart(zero, 1);
    after.collapse(true);
    sel.removeAllRanges();
    sel.addRange(after);
    markDirty();
    markTouched();
  }

  function insertTextAtCaret(text) {
    var sel = window.getSelection();
    if (!sel || !sel.rangeCount) return;
    var range = sel.getRangeAt(0);
    range.deleteContents();
    var tn = document.createTextNode(text);
    range.insertNode(tn);
    range.setStart(tn, text.length);
    range.collapse(true);
    sel.removeAllRanges();
    sel.addRange(range);
    markDirty();
    markTouched();
  }

  function save() {
    if (!state.editing || state.saving) return;
    if (!state.dirty) { toast(CFG.labels.nothing); return; }
    state.saving = true;
    if (state.saveBtn) state.saveBtn.disabled = true;
    setStatus(CFG.labels.saving + ' <b>' + escapeHtml(state.pagePath) + '</b>…');
    var markdown;
    try {
      markdown = serialize(state.article);
    } catch (err) {
      state.saving = false;
      if (state.saveBtn) state.saveBtn.disabled = false;
      setStatus(CFG.labels.editing + ' <b>' + escapeHtml(state.pagePath) + '</b> · ' + CFG.labels.unsaved);
      toast('Could not convert the page: ' + err.message, true);
      return;
    }
    if (!markdown.trim()) {
      state.saving = false;
      if (state.saveBtn) state.saveBtn.disabled = false;
      setStatus(CFG.labels.editing + ' <b>' + escapeHtml(state.pagePath) + '</b> · ' + CFG.labels.unsaved);
      toast('Refusing to save an empty page.', true);
      return;
    }

    var payload = { path: state.pagePath, markdown: markdown };
    if (state.base) payload.base = state.base;

    request(endpoints().save, {
      method: 'POST',
      headers: copyHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify(payload)
    }, 30000)
      .then(function (r) {
        return r.text().then(function (text) {
          var json;
          try { json = JSON.parse(text); }
          catch (e) { throw new Error('bad response from the save server'); }
          return { ok: r.ok, status: r.status, j: json };
        });
      })
      .then(function (res) {
        if (!res.ok || !res.j.ok) {
          if (res.status === 409) {
            throw new Error(res.j.error || 'the file changed on disk — reload the page to get the latest version');
          }
          throw new Error((res.j && res.j.error) || 'save failed');
        }
        state.dirty = false;
        state.saving = false;
        if (state.saveBtn) state.saveBtn.disabled = false;
        if (res.j.base) state.base = res.j.base;
        setStatus(CFG.labels.saved + ' <b>' + escapeHtml(state.pagePath) + '</b>');
        if (typeof CFG.onSaved === 'function') {
          CFG.onSaved({ path: state.pagePath, markdown: markdown, response: res.j });
        }
        if (CFG.reloadOnSave) {
          toast('Saved · reloading…');
          setTimeout(reloadPage, 350);
        } else {
          state.raw = markdown;
          state.bodyRaw = state.frontmatter ? markdown.slice(state.frontmatter.length) : markdown;
          Array.prototype.slice.call(state.article.querySelectorAll('[data-docsify-edit-touched]'))
            .forEach(function (n) { n.removeAttribute('data-docsify-edit-touched'); });
          state.originalHTML = state.article.innerHTML;
          toast('Saved.');
        }
      })
      .catch(function (err) {
        state.saving = false;
        if (state.saveBtn) state.saveBtn.disabled = false;
        setStatus(CFG.labels.editing + ' <b>' + escapeHtml(state.pagePath) + '</b> · ' + CFG.labels.unsaved);
        toast('Save failed: ' + err.message, true);
      });
  }

  function cancel() {
    if (!state.editing) return;
    if (state.dirty && !window.confirm('Discard your changes to ' + state.pagePath + '?')) return;
    exitEdit();
    reloadPage();
  }

  // A single reload is fine; several in a row is a bug (or a stale cached
  // script). Stop rather than spin the tab.
  function reloadPage() {
    try {
      var key = 'docsify-edit.reloads';
      var now = Date.now();
      var times = JSON.parse(sessionStorage.getItem(key) || '[]');
      times = times.filter(function (t) { return now - t < 15000; });
      times.push(now);
      sessionStorage.setItem(key, JSON.stringify(times));
      if (times.length > 6) {
        state.saving = false;
        toast('Reload loop stopped — close this tab and open the page again.', true);
        return;
      }
    } catch (e) { /* private mode: fall through */ }
    location.reload();
  }

  function discardEdit() {
    state.editing = false;
    state.dirty = false;
    state.saving = false;
    document.body.classList.remove('docsify-editing');
    if (state.article) {
      state.article.classList.remove('docsify-editable');
      state.article.removeAttribute('contenteditable');
      state.article.removeAttribute('aria-label');
      state.article.removeAttribute('role');
      state.article.removeAttribute('aria-multiline');
    }
    if (blockNav) { blockNav(); blockNav = null; }
    if (beforeUnload) { beforeUnload(); beforeUnload = null; }
    if (keyNav) { keyNav(); keyNav = null; }
    setStatus('');
  }

  function exitEdit() {
    state.editing = false;
    state.dirty = false;
    state.saving = false;
    document.body.classList.remove('docsify-editing');
    if (state.article) {
      state.article.classList.remove('docsify-editable');
      state.article.removeAttribute('contenteditable');
      state.article.removeAttribute('aria-label');
      state.article.removeAttribute('role');
      state.article.removeAttribute('aria-multiline');
      state.article.innerHTML = state.originalHTML;
    }
    if (blockNav) { blockNav(); blockNav = null; }
    if (beforeUnload) { beforeUnload(); beforeUnload = null; }
    if (keyNav) { keyNav(); keyNav = null; }
    setStatus('');
  }

  function openButton() {
    var b = el('button', {
      id: 'docsify-edit-open',
      type: 'button',
      title: CFG.labels.edit
    }, CFG.labels.edit);
    b.addEventListener('click', function () {
      var article = document.querySelector('.markdown-section');
      if (!article) { toast('The page is still loading…'); return; }
      enterEdit(article);
    });
    state.openBtn = b;
    document.body.appendChild(b);
  }

  function boot() {
    if (state.booted) return;
    state.booted = true;
    // a static site has no save API; don't even ping it. Set edit.allowRemote
    // when the save server is somewhere other than localhost.
    if (!CFG.allowRemote &&
        !/^(localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\])$/.test(location.hostname)) return;
    console.info('docsify-edit ' + VERSION);

    injectStyles();
    buildToolbar();
    request(endpoints().ping, {
      cache: 'no-store',
      headers: copyHeaders()
    }, 5000)
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) {
        if (!j || !j.ok) return; // static server / no API — no editor
        if (j.authOk === false) {
          console.warn('docsify-edit: the server rejected the configured edit.token');
          return;
        }
        if (CFG.scope && j.editable !== CFG.scope) {
          console.warn('docsify-edit: save server editable is ' + j.editable + ', expected ' + CFG.scope);
          return;
        }
        if (j.auth === 'token' && !CFG.token) {
          console.warn('docsify-edit: the server requires edit.token');
          return;
        }
        openButton();
        if (CFG.unregisterServiceWorker && 'serviceWorker' in navigator) {
          navigator.serviceWorker.getRegistrations().then(function (rs) {
            rs.forEach(function (r) { r.unregister(); });
            if (navigator.serviceWorker.controller) {
              console.warn('docsify-edit: unregistered the dev service worker — hard-reload once (Ctrl+Shift+R) to drop cached assets.');
            }
          }).catch(function () {});
        }
      })
      .catch(function () { /* static server or file:// — no editor */ });
  }

  var renderTimer = null;

  function plugin(hook, vm) {
    state.vm = vm;
    CFG = mergeConfig(vm);
    hook.mounted(function () { boot(); });
    hook.beforeEach(function () {
      state.rendering = true;
      clearTimeout(renderTimer);
      renderTimer = setTimeout(function () { state.rendering = false; }, 15000);
    });
    hook.doneEach(function () {
      clearTimeout(renderTimer);
      state.rendering = false;
      if (state.editing) discardEdit();
    });
  }

  global.DocsifyEdit = {
    version: VERSION,
    plugin: plugin,
    defaults: DEFAULTS,
    // pure helpers, exposed for unit tests (not part of the public UI API)
    _internal: {
      headingTexts: headingTexts,
      splitBlocks: splitBlocks,
      normBlock: normBlock,
      wrapPlain: wrapPlain,
      normalizeListMarkers: normalizeListMarkers,
      codeText: codeText
    }
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = global.DocsifyEdit;
})(typeof window !== 'undefined' ? window : (typeof globalThis !== 'undefined' ? globalThis : this));
