/* ============================================================
   flove-loader.js · pro-enrichment loader (browsy-gift gated)
   ------------------------------------------------------------
   Moved from the retired `central/solo` branch (2026-07-31).

   Pro-enrichment — the shared 🌱 library loaded on top of a
   self-contained app at normal/advanced/super tier — is enabled
   ONLY by a browsy reputational action: a *gift* granted from
   scorings. Without the gift the app stays at its base tier.

   Contract (per app):
     <meta name="flove:lib-base"   content="../../central/shared">
     <meta name="flove:gift-min"    content="40">          (optional, default 40)
     <script src=".../shared/code/js/flove-loader.js" defer></script>
     <link   data-flove-css href="flove.css">              (inert: no rel)
     <script data-flove-js  src="flove.js" type="text/plain"></script>
   Markers are inert — the browser never fetches them; the loader
   turns them into real <link rel=stylesheet>/<script> pointing at
   the lib base, resolving code/css/ and code/js/ subfolders from the file
   extension. Advanced variant: add data-flove-advanced to a
   marker to also fetch `flove-advanced.<ext>` from the same subfolder.

   Gift sources (first that answers):
     1. browsy bridge  → window.flove.browsy.trust.getScore(cb)
        (used when browsy exposes the bridge to the page — currently
        its content script runs in the isolated world, so the
        reliable path is #2)
     2. localStorage   → flove:gift = {"score": <n>, ...} written
        by the browsy content script (shared page storage) after the
        reputational action, or by the PoC's simulate control

   Signals on <html>:  data-flove-pro = "loading" | "on" | "off"
   Events on document: flove:gift {granted, score, threshold, source}
                        flove:enriched {libBase}
   Failure skip: localStorage flove:enriched = "false" (session).

   CSP-safe: external file only, no inline script. Never minified.
   ============================================================ */
(function () {
  'use strict';
  if (window.__floveLoaderLoaded) return;
  window.__floveLoaderLoaded = true;

  var ROOT = document.documentElement;

  function meta(name) {
    var m = document.querySelector('meta[name="' + name + '"]');
    return m ? m.getAttribute('content') : null;
  }

  function setPro(state, detail) {
    ROOT.setAttribute('data-flove-pro', state);
    document.dispatchEvent(new CustomEvent('flove:gift', { detail: detail }));
  }

  var libBase = meta('flove:lib-base');
  if (!libBase) return;                       // not an enriched app

  var GIFT_MIN = parseInt(meta('flove:gift-min') || '40', 10) || 40;
  var skipped = false;
  try { skipped = localStorage.getItem('flove:enriched') === 'false'; } catch (e) {}

  function readStoredScore() {
    try {
      var g = JSON.parse(localStorage.getItem('flove:gift') || 'null');
      return g && typeof g.score === 'number' ? g.score : 0;
    } catch (e) { return 0; }
  }

  function persistGift(score) {
    try {
      localStorage.setItem('flove:gift', JSON.stringify({
        score: score,
        source: 'browsy',
        grantedAt: Date.now()
      }));
    } catch (e) {}
  }

  function resolve(score, source) {
    var granted = !skipped && score >= GIFT_MIN;
    if (!granted) {
      setPro('off', { granted: false, score: score, threshold: GIFT_MIN, source: source });
      return;
    }
    setPro('loading', { granted: true, score: score, threshold: GIFT_MIN, source: source });
    inject(libBase, source);
  }

  var bridge = window.flove && window.flove.browsy && window.flove.browsy.trust;

  if (bridge && typeof bridge.getScore === 'function') {
    var settled = false;
    var fallback = setTimeout(function () {
      if (settled) return;
      settled = true;
      resolve(readStoredScore(), 'storage');
    }, 400);
    bridge.getScore(function (score) {
      if (settled) return;
      settled = true;
      clearTimeout(fallback);
      score = typeof score === 'number' ? score : 0;
      if (score > 0) persistGift(score);
      resolve(score, 'browsy');
    });
  } else {
    resolve(readStoredScore(), 'storage');
  }

  function inject(base, source) {
    var loaded = 0;
    window.__floveLoadedFiles = window.__floveLoadedFiles || {};
    var pre = document.createElement('link');
    if (/^https?:/.test(base)) {
      pre.rel = 'preconnect';
      pre.href = base;
      document.head.appendChild(pre);
    }
    document.head.querySelectorAll('[data-flove-css],[data-flove-js]').forEach(function (e) {
      var name = e.getAttribute('href') || e.getAttribute('src');
      if (!name) return;
      // duplicates: already tracked here, or a real (non-marker) tag already present
      var seen = window.__floveLoadedFiles[name] ||
        document.querySelector('link[rel="stylesheet"][href*="' + name + '"]:not([data-flove-css]),' +
                               'script[src*="' + name + '"]:not([data-flove-js])');
      if (seen) { console.warn('flove:skip', name); return; }
      var isCss = e.hasAttribute('data-flove-css');
      var folder = isCss ? 'code/css' : 'code/js';
      var el = document.createElement(isCss ? 'link' : 'script');
      if (isCss) { el.rel = 'stylesheet'; el.href = base + '/' + folder + '/' + name; }
      else { el.src = base + '/' + folder + '/' + name; }
      el.onerror = function () {
        try { localStorage.setItem('flove:enriched', 'false'); } catch (err) {}
        el.remove();
        ROOT.setAttribute('data-flove-pro', 'off');
      };
      document.head.appendChild(el);
      window.__floveLoadedFiles[name] = true;
      loaded++;
      if (e.hasAttribute('data-flove-advanced')) {
        var advName = 'flove-advanced.' + name.split('.').pop();
        var adv = document.createElement(isCss ? 'link' : 'script');
        if (isCss) { adv.rel = 'stylesheet'; adv.href = base + '/' + folder + '/' + advName; }
        else { adv.src = base + '/' + folder + '/' + advName; }
        adv.onerror = function () { adv.remove(); };
        document.head.appendChild(adv);
      }
    });
    if (loaded) {
      ROOT.setAttribute('data-flove-pro', 'on');
      document.dispatchEvent(new CustomEvent('flove:enriched', {
        detail: { libBase: base, source: source }
      }));
    }
  }
})();
