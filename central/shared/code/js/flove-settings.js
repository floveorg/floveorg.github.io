/* ============================================================
   flove-settings.js · shared settings manager for flove pages
   ============================================================
   Usage:  <script src="shared/js/flove-settings.js"></script>
           (load before page script, after flove.css)

   API:    window.floveSettings
             .get(key)         → current value
             .set(key, val)    → persist + apply + dispatch event
             .toggle(key)      → flip boolean, return new value
             .on(key, fn)      → listen for changes (fn receives {key, value})

   Keys:   'theme'          'light' | 'dark' | 'system'
           'sound'          true | false
           'notifications'  true | false
           'wizy'           true | false
           'language'       'en' | 'es' | 'fr' | ...

   Events: CustomEvent 'flove:setting' on document
           detail: { key, value }
   ============================================================ */

(function () {
  'use strict';

  var PREFIX = 'flove:';
  var DEFAULTS = {
    theme: 'system',
    sound: false,
    soundLevel: 'basic',
    notifications: true,
    wizy: true,
    language: 'en'
  };

  var _listeners = {};
  var _values = {};

  /* ── internal helpers ── */

  function read(key) {
    try { return localStorage.getItem(PREFIX + key); } catch (e) { return null; }
  }

  function write(key, val) {
    try { localStorage.setItem(PREFIX + key, JSON.stringify(val)); } catch (e) {}
  }

  function apply(key, val) {
    switch (key) {
      case 'theme':
        applyTheme(val);
        break;
      case 'language':
        applyLanguage(val);
        break;
      case 'sound':
        applySound(val);
        break;
    }
  }

  function emit(key, val) {
    document.dispatchEvent(new CustomEvent('flove:setting', { detail: { key: key, value: val } }));
    var fns = _listeners[key] || [];
    for (var i = 0; i < fns.length; i++) {
      try { fns[i]({ key: key, value: val }); } catch (e) {}
    }
  }

  /* ── theme ── */

  function applyTheme(val) {
    var root = document.documentElement;
    if (val === 'system') {
      root.removeAttribute('data-theme');
    } else {
      root.setAttribute('data-theme', val);
    }
    // update meta theme-color
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) {
      meta.setAttribute('content', val === 'dark' ? '#0b0b0f' : '#6c5ce7');
    }
  }

  function isDark() {
    var t = _values.theme;
    if (t === 'dark') return true;
    if (t === 'light') return false;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }

  /* ── language ── */

  function applyLanguage(val) {
    document.documentElement.setAttribute('lang', val);
  }

  /* ── sound ── */

  function applySound(val) {
    // stub: pages can listen to flove:setting event for sound key
  }

  /* ── public API ── */

  var api = {
    get: function (key) {
      return _values[key];
    },

    set: function (key, val) {
      if (_values[key] === val) return;
      _values[key] = val;
      write(key, val);
      apply(key, val);
      emit(key, val);
    },

    toggle: function (key) {
      var cur = _values[key];
      if (typeof cur === 'boolean') {
        api.set(key, !cur);
        return _values[key];
      }
      return cur;
    },

    on: function (key, fn) {
      if (!_listeners[key]) _listeners[key] = [];
      _listeners[key].push(fn);
    },

    isDark: isDark,

    /** Bind a checkbox toggle to a setting. Restores state on load. */
    bindToggle: function (el, key) {
      if (!el) return;
      // set initial state from saved value
      el.checked = !!_values[key];
      updateToggleVisual(el, key);
      // on change → persist
      el.addEventListener('change', function () {
        api.set(key, el.checked);
        updateToggleVisual(el, key);
      });
    },

    /** Bind a <select> to a setting. Restores state on load. */
    bindSelect: function (el, key) {
      if (!el) return;
      el.value = _values[key] || DEFAULTS[key];
      el.addEventListener('change', function () {
        api.set(key, el.value);
      });
    }
  };

  function updateToggleVisual(el, key) {
    var row = el.closest('.toggle-row');
    if (!row) return;
    var state = row.querySelector('.toggle-state');
    if (state) {
      state.textContent = el.checked ? 'on' : 'off';
      state.style.color = el.checked ? 'var(--signal)' : 'var(--muted)';
    }
  }

  /* ── init: load from localStorage, fallback to defaults ── */

  function init() {
    var keys = Object.keys(DEFAULTS);
    for (var i = 0; i < keys.length; i++) {
      var k = keys[i];
      var raw = read(k);
      var val;
      if (raw === null) {
        val = DEFAULTS[k];
      } else {
        try { val = JSON.parse(raw); } catch (e) { val = raw; }
      }
      _values[k] = val;
      apply(k, val);
    }
  }

  // run immediately so theme is applied before first paint
  init();

  // expose
  window.floveSettings = api;

})();
