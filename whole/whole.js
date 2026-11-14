/* whole · shared page behaviour.
   - logo/title opens the wiki menu
   - child menus (Music under Language, Economy under Psychosocial) open
     automatically on their own section; the parent link navigates normally
   - app <details> deep links open on arrival                             */
(function () {
  function openFromHash() {
    var id = location.hash.slice(1);
    if (!id) return;
    var el = document.getElementById(id);
    if (!el) return;
    if (el.tagName === 'DETAILS') el.open = true;
    if (el.classList.contains('whole-appcard')) {
      el.classList.remove('is-flash');
      void el.offsetWidth;
      el.classList.add('is-flash');
      window.setTimeout(function () { el.classList.remove('is-flash'); }, 1900);
    }
  }
  window.addEventListener('hashchange', openFromHash);


  /* §13.14 — light/dark theme. flove:theme persists; CSS owns the palettes. */
  (function () {
    var root = document.documentElement;
    var KEY = 'flove:theme';
    var toggles = Array.prototype.slice.call(document.querySelectorAll('[data-whole-theme-toggle]'));
    if (!toggles.length) return;
    var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
    function stored() {
      try { var v = localStorage.getItem(KEY); return (v === 'light' || v === 'dark') ? v : null; }
      catch (e) { return null; }
    }
    function effective() {
      return root.getAttribute('data-theme') || (mq && mq.matches ? 'dark' : 'light');
    }
    function sync() {
      var dark = effective() === 'dark';
      toggles.forEach(function (btn) {
        btn.setAttribute('aria-pressed', String(dark));
        btn.setAttribute('title', dark ? 'Switch to light theme' : 'Switch to dark theme');
        btn.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
      });
      var meta = document.querySelector('meta[name="theme-color"]');
      if (meta) meta.setAttribute('content', dark ? '#161114' : '#fff8f1');
    }
    function apply(theme) {
      root.setAttribute('data-theme', theme);
      try { localStorage.setItem(KEY, theme); } catch (e) {}
      sync();
    }
    toggles.forEach(function (btn) {
      btn.addEventListener('click', function () { apply(effective() === 'dark' ? 'light' : 'dark'); });
    });
    if (mq) {
      var follow = function () {
        if (stored()) return;
        if (mq.matches) root.setAttribute('data-theme', 'dark');
        else root.removeAttribute('data-theme');
        sync();
      };
      if (mq.addEventListener) mq.addEventListener('change', follow);
      else if (mq.addListener) mq.addListener(follow);
    }
    sync();
  })();

  var brand = document.querySelector('.whole-brand');
  var menu = document.getElementById('whole-menu');

  function closeMenu() {
    if (menu) { menu.hidden = true; if (brand) brand.setAttribute('aria-expanded', 'false'); }
  }

  if (brand && menu) {
    brand.addEventListener('click', function (e) {
      e.preventDefault();
      var open = menu.hidden;
      closeMenu();
      menu.hidden = !open;
      brand.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('click', function (e) {
      if (!e.target.closest || !e.target.closest('.whole-brand-wrap')) closeMenu();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu();
    });
  }


/* last updated of the published whole/ folder (GitHub commit, cached per session) */
(function () {
  var el = document.querySelector('[data-whole-updated]');
  if (!el) return;
  var KEY = 'whole-updated-v1';
  function fmt(d) {
    return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
  }
  try {
    var cached = sessionStorage.getItem(KEY);
    if (cached) {
      var cd = new Date(cached);
      if (!isNaN(cd)) { el.textContent = fmt(cd); el.setAttribute('datetime', cached); return; }
    }
  } catch (e) {}
  fetch('https://api.github.com/repos/floveorg/floveorg.github.io/commits?path=whole&per_page=1', {
    headers: { Accept: 'application/vnd.github+json' }
  }).then(function (r) { return r.ok ? r.json() : Promise.reject(); })
    .then(function (data) {
      var c = data && data[0] && data[0].commit;
      var iso = c && (c.committer && c.committer.date || c.author && c.author.date);
      if (!iso) throw 0;
      var d = new Date(iso);
      el.textContent = fmt(d);
      el.setAttribute('datetime', iso);
      try { sessionStorage.setItem(KEY, iso); } catch (e) {}
    })
    .catch(function () { el.textContent = 'recently'; });
})();


/* app preview modal — cards expand; the modal carries the final Play link */
(function () {
  var cards = Array.prototype.slice.call(document.querySelectorAll('.whole-appcard'));
  if (!cards.length || typeof HTMLDialogElement === 'undefined') return;
  var dialog = document.createElement('dialog');
  dialog.className = 'whole-appmodal';
  dialog.setAttribute('aria-labelledby', 'whole-appmodal-title');
  dialog.innerHTML = '<div class="whole-appmodal__inner">'
    + '<button class="whole-appmodal__close" type="button" aria-label="Close app preview">×</button>'
    + '<div class="whole-appmodal__media"></div>'
    + '<div class="whole-appmodal__body"><p class="whole-appmodal__kicker"></p>'
    + '<h2 id="whole-appmodal-title"></h2><p class="whole-appmodal__tag" hidden></p>'
    + '<p class="whole-appmodal__desc"></p><div class="whole-appmodal__vals" hidden></div>'
    + '<a class="whole-appmodal__play" href="#">Play in →</a>'
    + '<p class="whole-appmodal__hint">Click Play in to open the app.</p></div></div>';
  document.body.appendChild(dialog);
  var media = dialog.querySelector('.whole-appmodal__media');
  var kick = dialog.querySelector('.whole-appmodal__kicker');
  var title = dialog.querySelector('h2');
  var desc = dialog.querySelector('.whole-appmodal__desc');
  var tagEl = dialog.querySelector('.whole-appmodal__tag');
  var valsEl = dialog.querySelector('.whole-appmodal__vals');
  var play = dialog.querySelector('.whole-appmodal__play');
  var lastCard = null;

  function open(card) {
    var img = card.querySelector('.whole-appcard__shot img');
    var name = card.querySelector('.whole-appcard__name');
    var text = card.querySelector('.whole-appcard__desc');
    var href = card.getAttribute('href');
    var ctx = card.getAttribute('data-context') || 'App';
    var cat = card.getAttribute('data-cat') || '';
    var tag = card.getAttribute('data-tag') || '';
    var long = card.getAttribute('data-long') || '';
    var vals = (card.getAttribute('data-vals') || '').split('|').filter(Boolean);
    media.innerHTML = img ? '<img alt="">' : '<span class="whole-appmodal__media--empty"></span>';
    if (img) media.querySelector('img').src = img.currentSrc || img.src;
    else media.querySelector('.whole-appmodal__media--empty').textContent = (name ? name.textContent : '?').trim().slice(0, 1);
    kick.textContent = 'App · ' + ctx + (cat ? ' · ' + cat : '');
    title.textContent = name ? name.textContent.trim() : '';
    tagEl.textContent = tag;
    tagEl.hidden = !tag;
    desc.textContent = long || (text ? text.textContent.trim() : '');
    valsEl.innerHTML = '';
    valsEl.hidden = !vals.length;
    vals.forEach(function (v) {
      var chip = document.createElement('span');
      chip.textContent = v;
      valsEl.appendChild(chip);
    });
    play.href = href;
    play.setAttribute('aria-label', 'Play in ' + (name ? name.textContent.trim() : 'app'));
    lastCard = card;
    if (typeof dialog.showModal === 'function') dialog.showModal();
    else dialog.setAttribute('open', '');
  }
  cards.forEach(function (card) {
    card.setAttribute('aria-haspopup', 'dialog');
    card.addEventListener('click', function (e) {
      if (typeof dialog.showModal !== 'function') return;
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
      e.preventDefault();
      open(card);
    });
  });
  dialog.querySelector('.whole-appmodal__close').addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('click', function (e) { if (e.target === dialog) dialog.close(); });
  dialog.addEventListener('close', function () { if (lastCard) lastCard.focus(); });
})();

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', openFromHash);
  else openFromHash();
})();

/* ── albums ──────────────────────────────────────────────── */
/* ── album player ──────────────────────────────────────────── */
(function () {
  if (!document.querySelector(".album")) return;
  var player = document.getElementById("album-player");
  if (!player) {
    player = document.createElement("audio");
    player.id = "album-player";
    player.preload = "none";
    player.setAttribute("aria-hidden", "true");
    document.body.appendChild(player);
  }
  var tracks = Array.prototype.slice.call(document.querySelectorAll(".album .track"));
  var current = null;

  function label(tr, on) {
    var b = tr.querySelector(".track-btn");
    var verb = tr.dataset.kind === "video" ? "Watch" : (on ? "Pause" : "Play");
    var suffix = tr.dataset.kind === "video" ? " (opens in a new tab)" : "";
    b.setAttribute("aria-label", verb + " " + tr.dataset.title + suffix);
  }
  function reset(tr) {
    if (!tr) return;
    tr.classList.remove("is-playing");
    var bar = tr.querySelector(".track-bar i");
    if (bar) bar.style.width = "0";
    label(tr, false);
  }
  function playNext(from) {
    var i = tracks.indexOf(from), nxt = null;
    for (var j = i + 1; j < tracks.length; j++) {
      if (tracks[j].dataset.kind === "song") { nxt = tracks[j]; break; }
    }
    if (!nxt) { for (var k = 0; k < tracks.length; k++) { if (tracks[k].dataset.kind === "song") { nxt = tracks[k]; break; } } }
    if (nxt && nxt !== from) {
      current = nxt; player.src = nxt.dataset.src; player.play();
    }
  }

  tracks.forEach(function (tr) {
    var btn = tr.querySelector(".track-btn");
    btn.addEventListener("click", function () {
      if (tr.dataset.kind === "video") { window.open(tr.dataset.src, "_blank", "noopener"); return; }
      if (current === tr && !player.paused) { player.pause(); return; }
      if (current && current !== tr) reset(current);
      if (current !== tr) { current = tr; player.src = tr.dataset.src; }
      tr.classList.add("is-playing");
      label(tr, true);
      var p = player.play();
      if (p && p.catch) p.catch(function () { reset(tr); });
    });
  });

  player.addEventListener("play", function () { if (current) { current.classList.add("is-playing"); label(current, true); } });
  player.addEventListener("pause", function () { if (current) { current.classList.remove("is-playing"); label(current, false); } });
  player.addEventListener("timeupdate", function () {
    if (!current || !player.duration) return;
    var bar = current.querySelector(".track-bar i");
    if (bar) bar.style.width = (player.currentTime / player.duration * 100).toFixed(2) + "%";
  });
  player.addEventListener("ended", function () {
    var done = current; reset(done);
    if (done) playNext(done);
  });
})();
