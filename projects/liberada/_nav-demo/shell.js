/* ============================================================
   flove nav shell — shared abstraction of first-section navigation
   for risa/ama (clone + ama indexes). Learned from freed.html:
   flove-bar topbar · §13.5 menu (App · Related Apps · Flove) ·
   CSS-only :has() section stepper (radios + cards + next/back).

   Central shared-code compat (tested against central/shared/code):
     · i18n     → uses .es/.en classes + name="lang" radios, honors
                  flove-i18n.js (window.flove.i18n) when loaded.
     · theme    → delegates to flove-settings.js (floveSettings)
                  when loaded; sets data-theme on <html>.
     · sound    → data-sound attributes wired for flove-sound.js.
     · classes  → namespaced fn-* where they'd collide with flove.css
                  (.btn→.fn-btn, .card→.fn-card, .wrap→.fn-wrap).
     · API      → exposes window.flove.nav {sections, go, current}.

   Usage:
     FloveShell.init({
       app, mark, accent*, hero, sections[], related[], menu
     });
   * accent / accentDeep / accentSoft override the palette.
   ============================================================ */
window.FloveShell = (function () {
  "use strict";

  function bi(es, en) {
    return '<span class="es">' + es + '</span><span class="en">' + en + '</span>';
  }

  function renderTopbar(cfg) {
    var related = (cfg.related || []).slice(0, 3);
    var menu =
      '<div class="menu-sec">' + bi('App', 'App') + '</div>' +
      '<li><button type="button" class="menu-act" data-act="about" data-sound="ui:nav">🌿 ' + bi(cfg.menu.about.es, cfg.menu.about.en) + '</button></li>' +
      (cfg.profileUrl
        ? '<li><a href="' + cfg.profileUrl + '" data-sound="ui:nav">👤 ' + bi('Perfil', 'Profile') + '</a></li>'
        : '') +
      '<li class="menu-related"><div class="menu-sec">' + bi('Apps del círculo', 'Related Apps') + '</div></li>' +
      related.map(function (r) {
        return '<li><a href="' + r.url + '" data-sound="ui:nav"><span class="menu-mark">' + (r.mark || '') + '</span><span>' + r.name + '</span></a></li>';
      }).join('') +
      '<li><div class="menu-sec">Flove</div></li>' +
      '<li><a href="' + cfg.flove.about + '" data-sound="ui:nav">🌱 ' + bi('Acerca de flove', 'About flove') + '</a></li>' +
      '<li><a href="' + cfg.flove.apps + '" data-sound="ui:nav">🧩 ' + bi('Todas las apps', 'All apps') + '</a></li>' +
      '<li><a href="' + cfg.flove.home + '" data-sound="ui:nav">🏠 ' + bi('flove.org', 'flove.org') + '</a></li>';

    return (
      '<header class="flove-bar">' +
        '<div class="top-menu">' +
          '<button type="button" class="site-trigger" id="menuBtn" aria-haspopup="true" aria-expanded="false" aria-controls="menuList">' +
            '<span class="logo-wrap">' + cfg.mark + '</span>' +
            '<span class="flove-app-name">' + cfg.app + '</span>' +
            '<span class="caret" aria-hidden="true">▾</span>' +
          '</button>' +
          '<ul class="menu-list" id="menuList" hidden role="menu">' + menu + '</ul>' +
        '</div>' +
        '<div class="bar-utils">' +
          '<button type="button" class="theme-btn" id="themeBtn" data-sound="ui:click" title="◐ ' + bi('Tema', 'Theme') + '">◐</button>' +
          '<details class="lang">' +
            '<summary class="worldball" title="🌐 ' + bi('Idioma', 'Language') + '">🌐</summary>' +
            '<div class="lang-opts">' +
              '<input type="radio" name="lang" id="lang-es" checked><label for="lang-es">Español</label>' +
              '<input type="radio" name="lang" id="lang-en"><label for="lang-en">English</label>' +
            '</div>' +
          '</details>' +
        '</div>' +
      '</header>'
    );
  }

  function renderHero(cfg) {
    var hero = cfg.hero || {};
    var actions = (hero.actions || []).map(function (a) {
      var cls = a.primary ? 'fn-btn' : 'fn-btn fn-btn-ghost';
      var inner = a.label ? bi(a.label.es, a.label.en) : a.label;
      if (a.href) return '<a class="' + cls + '" href="' + a.href + '"' + (a.target ? ' target="_blank" rel="noopener"' : '') + ' data-sound="ui:click">' + inner + '</a>';
      return '<button type="button" class="' + cls + '" data-action="' + a.action + '" data-sound="ui:click">' + inner + '</button>';
    }).join('');
    return (
      '<section class="hero">' +
        (hero.logo ? '<div class="hero-logo">' + hero.logo + '</div>' : '') +
        '<h1>' + cfg.app + '</h1>' +
        (hero.lead ? '<p class="lead">' + bi(hero.lead.es, hero.lead.en) + '</p>' : '') +
        '<div class="hero-actions">' + actions + '</div>' +
      '</section>'
    );
  }

  function renderSections(cfg) {
    var radios = cfg.sections.map(function (s, i) {
      return '<input type="radio" name="secnav" id="sec-' + i + '" class="secnav-radio"' + (i === 0 ? ' checked' : '') + '>';
    }).join('');

    var cards = cfg.sections.map(function (s, i) {
      return (
        '<section class="fn-card" data-sec="' + i + '">' +
          '<h2>' + bi(s.title.es, s.title.en) + '</h2>' +
          (s.lead ? '<p class="fn-card-lead">' + bi(s.lead.es, s.lead.en) + '</p>' : '') +
          s.body +
        '</section>'
      );
    }).join('');

    var buttons = cfg.sections.map(function (s, i) {
      return '<label class="section-btn" for="sec-' + i + '" data-sec="' + i + '" data-sound="ui:tab">' +
        '<span>' + bi(s.label.es, s.label.en) + '</span>' +
        '<span class="sb-icon">' + s.icon + '</span></label>';
    }).join('');

    return (
      '<form id="decl" autocomplete="off">' +
        radios + cards +
        '<div class="section-nav">' +
          '<button type="button" class="sec-move sec-back" id="secBack" data-sound="ui:nav">← <span class="es">Atrás</span><span class="en">Back</span></button>' +
          '<button type="button" class="sec-move sec-next" id="secNext" data-sound="ui:nav"><span class="es">Siguiente</span><span class="en">Next</span> →</button>' +
        '</div>' +
        '<div class="section-buttons">' + buttons + '</div>' +
      '</form>'
    );
  }

  function injectSectionCss(count) {
    var rules = [];
    for (var i = 0; i < count; i++) {
      rules.push(
        '#decl:has(#sec-' + i + ':checked) > .fn-card[data-sec="' + i + '"]{display:block}',
        '#decl:has(#sec-' + i + ':checked) .section-btn[data-sec="' + i + '"]{color:var(--app-accent-deep)}',
        '#decl:has(#sec-' + i + ':checked) .section-btn[data-sec="' + i + '"] .sb-icon{border-color:var(--app-accent);color:var(--app-accent-deep);background:var(--app-accent-soft)}'
      );
    }
    var style = document.createElement('style');
    style.textContent = rules.join('\n');
    document.head.appendChild(style);
  }

  function wireHeroActions() {
    document.querySelectorAll('[data-action]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (b.dataset.action === 'scroll-first') {
          var first = document.querySelector('.fn-card[data-sec="0"]');
          if (first) first.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });
  }

  function wireMenu() {
    var btn = document.getElementById('menuBtn');
    var list = document.getElementById('menuList');
    if (!btn || !list) return;
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = list.hidden;
      list.hidden = !open;
      btn.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('click', function (e) {
      if (!list.hidden && !list.contains(e.target) && !btn.contains(e.target)) {
        list.hidden = true;
        btn.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { list.hidden = true; btn.setAttribute('aria-expanded', 'false'); }
    });
    list.querySelectorAll('[data-act]').forEach(function (el) {
      el.addEventListener('click', function () {
        list.hidden = true;
        var act = el.dataset.act;
        if (act === 'about') {
          var first = document.querySelector('.secnav-radio');
          if (first) { first.checked = true; updateNav(); }
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      });
    });
  }

  function updateNav() {
    var radios = document.querySelectorAll('#decl .secnav-radio');
    var idx = Array.prototype.findIndex.call(radios, function (r) { return r.checked; });
    var back = document.getElementById('secBack');
    var next = document.getElementById('secNext');
    if (back) back.disabled = idx <= 0;
    if (next) next.disabled = idx >= radios.length - 1;
    return idx;
  }

  function wireSectionNav() {
    var radios = document.querySelectorAll('#decl .secnav-radio');
    var back = document.getElementById('secBack');
    var next = document.getElementById('secNext');
    function move(delta) {
      var idx = Array.prototype.findIndex.call(radios, function (r) { return r.checked; });
      var target = idx + delta;
      if (target < 0 || target >= radios.length) return;
      radios[target].checked = true;
      updateNav();
      radios[target].closest('#decl').querySelector('.fn-card[data-sec="' + target + '"]').scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
    if (back) back.addEventListener('click', function () { move(-1); });
    if (next) next.addEventListener('click', function () { move(1); });
    radios.forEach(function (r) { r.addEventListener('change', updateNav); });
    updateNav();
  }

  /* central-compatible theme: flove-settings.js when present, else fallback */
  function currentTheme() {
    if (window.floveSettings) {
      var t = window.floveSettings.get('theme');
      return t === 'dark' ? 'dark' : 'light';
    }
    return document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
  }

  function applyTheme(val) {
    if (window.floveSettings) {
      window.floveSettings.set('theme', val);
    } else {
      var root = document.documentElement;
      if (val === 'dark') root.setAttribute('data-theme', 'dark'); else root.removeAttribute('data-theme');
      try { localStorage.setItem('flove:nav-theme', val); } catch (e) {}
    }
  }

  function wireTheme() {
    var btn = document.getElementById('themeBtn');
    if (!btn) return;
    if (!window.floveSettings) {
      try {
        if (localStorage.getItem('flove:nav-theme') === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
      } catch (e) {}
    }
    btn.addEventListener('click', function () {
      applyTheme(currentTheme() === 'dark' ? 'light' : 'dark');
    });
  }

  /* central-compatible i18n: flove-i18n.js when present, else CSS :has() fallback */
  function wireI18n() {
    if (window.flove && window.flove.i18n) {
      var apply = function () { window.flove.i18n.apply(); };
      document.querySelectorAll('input[name="lang"]').forEach(function (r) {
        r.addEventListener('change', apply);
      });
      try {
        var saved = localStorage.getItem('translaty-lang');
        if (saved) {
          var radio = document.getElementById('lang-' + saved);
          if (radio) radio.checked = true;
        }
      } catch (e) {}
      apply();
    }
  }

  function exposeApi(cfg) {
    window.flove = window.flove || {};
    window.flove.nav = {
      sections: cfg.sections.map(function (s) { return s.id; }),
      go: function (i) {
        var radios = document.querySelectorAll('#decl .secnav-radio');
        if (i >= 0 && i < radios.length) { radios[i].checked = true; updateNav(); }
      },
      current: function () { return updateNav(); }
    };
  }

  function init(cfg) {
    if (!cfg || !cfg.app) { console.warn('FloveShell: missing config.app'); return; }
    if (cfg.accent) {
      var s = document.documentElement.style;
      s.setProperty('--app-accent', cfg.accent);
      if (cfg.accentDeep) s.setProperty('--app-accent-deep', cfg.accentDeep);
      if (cfg.accentSoft) s.setProperty('--app-accent-soft', cfg.accentSoft);
    }
    document.title = cfg.app + (cfg.tagline ? ' · ' + cfg.tagline : '');

    var root = document.getElementById('shell-root');
    root.innerHTML =
      renderTopbar(cfg) +
      '<main>' +
        renderHero(cfg) +
        renderSections(cfg) +
      '</main>';

    injectSectionCss(cfg.sections.length);
    wireHeroActions();
    wireMenu();
    wireSectionNav();
    wireTheme();
    wireI18n();
    exposeApi(cfg);
  }

  return { init: init };
})();
