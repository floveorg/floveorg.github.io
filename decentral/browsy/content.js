// browsy · content script
// Bridge API only. On-demand — no background work.
// Central caches responses. Browsy stays light.

(function() {
  if (window.__browsyLoaded) return;
  window.__browsyLoaded = true;

  var TIMEOUT = 100; // ms — fallback to cache if slow
  var _cache = {};   // central caches bridge responses

  // ── detect app ──
  var url = window.location.href;
  var app = 'unknown';
  if (url.includes('/apps/appy/')) app = 'appy';
  else if (url.includes('/apps/blogy/')) app = 'blogy';
  else if (url.includes('/apps/nety/')) app = 'nety';
  else if (url.includes('/apps/sety/')) app = 'sety';
  else if (url.includes('/apps/gody/')) app = 'gody';

  // ── message helper with timeout ──
  function ask(msg, cb) {
    var done = false;
    var timer = setTimeout(function() {
      if (!done) {
        done = true;
        cb(_cache[msg.type] || null);
      }
    }, TIMEOUT);
    chrome.runtime.sendMessage(msg, function(resp) {
      if (done) return;
      done = true;
      clearTimeout(timer);
      if (resp && resp.ok) {
        _cache[msg.type] = resp.data;
        cb(resp.data);
      } else {
        cb(_cache[msg.type] || null);
      }
    });
  }

  // ── bridge API ──
  window.flove = window.flove || {};
  window.flove.browsy = {
    app: app,
    version: '0.2.0',
    isFlove: true,

    // identity (on-demand)
    identity: {
      getKeypair: function(cb) {
        ask({ type: 'get-keypair' }, cb);
      },
      getProfile: function(cb) {
        ask({ type: 'get-profile' }, cb);
      },
      isUnlocked: function() {
        return !!window.flove.browsy._unlocked;
      }
    },

    // trust (on-demand)
    trust: {
      getScore: function(cb) {
        ask({ type: 'get-trust-score' }, cb);
      },
      getFacets: function(cb) {
        ask({ type: 'get-trust-facets' }, cb);
      },
      getVouches: function(cb) {
        ask({ type: 'get-vouches' }, cb);
      },
      onUpdate: function(fn) {
        chrome.storage.onChanged.addListener(function(changes, area) {
          if (area === 'local' && (changes['browsy-trust'] || changes['browsy-vouches'])) {
            fn();
          }
        });
      }
    },

    // settings (on-demand, unidirectional: browsy → central)
    settings: {
      get: function(key, cb) {
        ask({ type: 'get-setting', key: key }, cb);
      },
      getAll: function(cb) {
        ask({ type: 'get-settings' }, cb);
      }
    },

    // events from background
    on: function(type, fn) {
      chrome.runtime.onMessage.addListener(function(msg) {
        if (msg.type === type) fn(msg);
      });
    },

    // internal
    _unlocked: false,
    _cache: _cache
  };

  // ── notify background ──
  chrome.runtime.sendMessage({ type: 'flove-detected', app: app });
})();
