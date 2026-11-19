// browsy · background service worker
// On-demand only. No background calculations.
// Handles: context menus, badge, settings mirror, crypto stubs.

// ── context menus ──

chrome.runtime.onInstalled.addListener(function() {
  chrome.contextMenus.create({
    id: 'browsy-save',
    title: 'Save to flove',
    contexts: ['selection', 'link', 'image']
  });
  chrome.contextMenus.create({
    id: 'browsy-nety',
    title: 'Share to Nety',
    contexts: ['page', 'selection']
  });
});

chrome.contextMenus.onClicked.addListener(function(info, tab) {
  if (info.menuItemId === 'browsy-save') {
    chrome.tabs.sendMessage(tab.id, { type: 'save-triggered', info: info });
  }
  if (info.menuItemId === 'browsy-nety') {
    chrome.tabs.sendMessage(tab.id, { type: 'share-triggered', info: info });
  }
});

// ── badge detection ──

chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
  if (changeInfo.status !== 'complete') return;
  var u = tab.url || '';
  var isFlove = u.includes('flove.org') || u.includes('localhost') || u.includes('127.0.0.1');
  chrome.action.setBadgeText({ text: isFlove ? '★' : '', tabId: tabId });
  chrome.action.setBadgeBackgroundColor({ color: '#6c5ce7', tabId: tabId });
});

// ── message handler (bridge API) ──

chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {

  // identity
  if (msg.type === 'get-keypair') {
    chrome.storage.local.get('browsy-keys', function(d) {
      sendResponse({ ok: true, data: d['browsy-keys'] || null });
    });
    return true; // async
  }

  if (msg.type === 'get-profile') {
    chrome.storage.local.get('browsy-profile', function(d) {
      sendResponse({ ok: true, data: d['browsy-profile'] || null });
    });
    return true;
  }

  // trust
  if (msg.type === 'get-trust-score') {
    chrome.storage.local.get('browsy-trust', function(d) {
      var t = d['browsy-trust'] || {};
      sendResponse({ ok: true, data: t.score || 0 });
    });
    return true;
  }

  if (msg.type === 'get-trust-facets') {
    chrome.storage.local.get('browsy-trust', function(d) {
      var t = d['browsy-trust'] || {};
      sendResponse({ ok: true, data: t.facets || { personal: 0, local: 0, social: 0, global: 0 } });
    });
    return true;
  }

  if (msg.type === 'get-vouches') {
    chrome.storage.local.get('browsy-vouches', function(d) {
      sendResponse({ ok: true, data: d['browsy-vouches'] || [] });
    });
    return true;
  }

  // settings (unidirectional: browsy → central)
  if (msg.type === 'get-setting') {
    chrome.storage.local.get('flove-' + msg.key, function(d) {
      sendResponse({ ok: true, data: d['flove-' + msg.key] || null });
    });
    return true;
  }

  if (msg.type === 'get-settings') {
    var keys = ['theme', 'language', 'sound', 'soundLevel', 'notifications', 'wizy'];
    var storageKeys = keys.map(function(k) { return 'flove-' + k; });
    chrome.storage.local.get(storageKeys, function(d) {
      var settings = {};
      keys.forEach(function(k) {
        settings[k] = d['flove-' + k] || null;
      });
      sendResponse({ ok: true, data: settings });
    });
    return true;
  }

  // settings mirror (central → browsy)
  if (msg.type === 'setting-changed') {
    var obj = {};
    obj['flove-' + msg.key] = msg.value;
    chrome.storage.local.set(obj, function() {
      // also mirror to sync if small enough
      try {
        chrome.storage.sync.set(obj);
      } catch (e) {}
      sendResponse({ ok: true });
    });
    return true;
  }

  // detected
  if (msg.type === 'flove-detected') {
    // could track stats here
    sendResponse({ ok: true });
    return false;
  }
});
