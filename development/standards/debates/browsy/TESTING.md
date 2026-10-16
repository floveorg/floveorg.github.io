# Browsy Testing & Risk Analysis

## Decisions made

| # | Question | Decision |
|---|----------|----------|
| 1 | Calculations/refreshes/syncs | **On-demand only** (click) — lightest for browsy |
| 2 | Vouch data structure | Array of objects (defined below) |
| 3 | Mnemonic BIP39 | Reply later |
| 4 | tweetnacl vs Web Crypto | **Web Crypto primary + tweetnacl fallback** (see pros/cons) |
| 5 | Key generation location | **Background service worker** (off main thread) |
| 6 | Cross-browser testing | **No** — Chrome only |
| 7 | Expected vouches | **20–100 per user** |
| 8 | Trust chain calculation | **On demand** |
| 9 | Vouch revocation | **Recalculate in bundled session daily** when growing too much |
| 10 | Settings sync direction | **Browsy → central only** (unidirectional) |
| 11 | Conflict resolution | **Browsy wins** |
| 12 | chrome.storage.sync for settings | **Yes** (multi-device) |
| 13 | Web Workers for crypto | **Yes**, if loads exceed 30s service worker lifetime |
| 14 | Cache bridge in central | **Yes** — central caches, browsy stays lighter |
| 15 | Bridge API response target | **< 100ms** |
| 16 | Test both installed/not | **Both** |
| 17 | Cross-browser | **Yes** — Firefox, Safari too |
| 18 | Mock bridge for tests | **Yes** |
| 19 | Profile data | **Identity (me) + some settings** |
| 20 | browsy-trust data | **MyNet + vouches + trust chain + facets** |

---

## Architecture recap

```
browsy (chrome extension)         central (flove.org page)
──────────────────────            ─────────────────────────
backend only                      all frontends
chrome.storage.local              localStorage (fallback)
chrome.storage.sync               chrome.storage.sync (multi-device)
crypto (ed25519)                  UI panels
content script (bridge API)       design system
background.js (service worker)    sound, i18n, settings
web worker (heavy crypto)         cache bridge responses
```

**Core rule:** Browsy is on-demand only. No background calculations. No auto-sync. User clicks → browsy computes → central displays.

---

## 1 · Vouch data structure

### What is a vouch?

A vouch is one person saying "I trust this person." It's an array entry.

```js
// browsy-vouches (chrome.storage.local)
[
  {
    id: "v_abc123",
    from: "ed25519_pubkey_of_truster",     // who vouched
    to: "ed25519_pubkey_of_trusted",       // who is vouched
    score: 0.85,                           // trust level 0-1
    facets: {
      personal: 0.9,                       // I know them personally
      local: 0.7,                          // same city/region
      social: 0.8,                         // same community
      global: 0.6                          // reputation
    },
    message: "Known for 3 years",          // optional note
    created: "2026-07-27T10:00:00Z",       // when vouch was made
    revoked: null                          // null = active, date = revoked
  },
  // ... 20-100 of these per user
]
```

### UI representation

```
┌─────────────────────────────────┐
│  🟢 María vouched for you       │
│  Score: 0.85 · Personal: 0.9   │
│  "Known for 3 years"            │
│  2026-07-27                     │
├─────────────────────────────────┤
│  🟡 Carlos vouched for you      │
│  Score: 0.70 · Social: 0.8     │
│  "Met at conference"            │
│  2026-06-15                     │
└─────────────────────────────────┘
```

### Storage estimate

| Vouches | Size (approx) | % of 5MB |
|---------|---------------|----------|
| 20 | ~8 KB | 0.2% |
| 50 | ~20 KB | 0.4% |
| 100 | ~40 KB | 0.8% |
| 200 | ~80 KB | 1.6% |

**Verdict:** 20-100 vouches = well under 5MB. Safe.

---

## 2 · Crypto: tweetnacl vs Web Crypto

### Comparison

| Factor | tweetnacl | Web Crypto Ed25519 |
|--------|-----------|-------------------|
| Browser support | All (polyfill) | Chrome 113+, Edge 113+, no Firefox/Safari yet |
| Size | ~20KB minified | 0 (built-in) |
| Async | No (sync, blocks thread) | Yes (Promise-based) |
| Speed | Fast for small ops | Faster for large ops |
| Service worker | Works | Works |
| Web Worker | Works | Works |
| Maintenance | Stable, unmaintained | Browser-native, auto-updates |
| Dependencies | None | None |
| Future-proof | Risk (unmaintained) | Yes (standard) |

### Decision: Web Crypto primary + tweetnacl fallback

```
if (window.crypto && window.crypto.subtle && ed25519Supported) {
  // use Web Crypto (Chrome 113+)
} else {
  // fallback to tweetnacl (older Chrome, Firefox, Safari)
}
```

**Why:**
- Web Crypto is async → doesn't block main thread
- No polyfill needed on modern Chrome
- tweetnacl covers older browsers
- Future-proof as Web Crypto gets Ed25519 everywhere

### Pros/cons summary

**Web Crypto pros:** native, async, no bundle, future-proof
**Web Crypto cons:** Chrome 113+ only, no Firefox/Safari yet

**tweetnacl pros:** all browsers, proven, tiny
**tweetnacl cons:** sync (blocks thread), unmaintained, adds 20KB

---

## 3 · Browsy performance risks

### Service worker lifecycle
| Risk | Severity | Mitigation |
|------|----------|------------|
| Killed after 30s idle | HIGH | On-demand only, no background work |
| Killed after 5min max | HIGH | Crypto ops < 500ms, trust chains < 2s |
| No persistent state | HIGH | All state in `chrome.storage.local` |
| No `window`/`document` | HIGH | Web Worker for heavy ops |
| Re-created on event | MED | Re-register bridge on restart |

### Storage limits
| Limit | Value | Our usage (100 vouches) |
|-------|-------|------------------------|
| `chrome.storage.local` total | 5 MB | ~40KB vouches + ~1KB keys + ~1KB trust |
| `chrome.storage.local` per item | 1 MB | Vouch array ~40KB (safe) |
| `chrome.storage.sync` total | 100 KB | Settings only (~1KB) |
| `chrome.storage.sync` per item | 8 KB | Each setting < 100 bytes |

**Verdict:** Well within limits at 20-100 vouches. Monitor at 500+.

### Content script timing
| Risk | Severity | Mitigation |
|------|----------|------------|
| Injected after DOM ready | MED | Central waits for bridge, fallback to localStorage |
| SPA navigation | MED | Re-inject on `popstate`/`pushState` |
| Message timeout | LOW | 100ms timeout, fallback to cached data |

### Crypto operations (with Web Worker)
| Risk | Severity | Mitigation |
|------|----------|------------|
| Key gen in worker | LOW | Off main thread, < 500ms |
| Trust chain in worker | LOW | Off main thread, < 2s for 100 vouches |
| Worker killed by browser | MED | Restart on demand, cache results |

### Cross-origin (patched)
| Risk | Severity | Mitigation |
|------|----------|------------|
| Content script can't access page JS | MED | Bridge uses `chrome.runtime.sendMessage` |
| flove.org vs localhost | LOW | Badge: check `flove.org` OR `localhost:*` OR `127.0.0.1:*` |
| CSP blocks inline script | LOW | Bridge is injected as content script, not inline |

---

## 4 · What's implemented vs stubbed

### Implemented (real code)
- [x] Context menus (background.js)
- [x] Badge detection (background.js)
- [x] Popup UI (popup.html/popup.js)
- [x] Content script bridge skeleton (content.js)
- [x] `chrome.storage.onChanged` listener

### Stubbed (returns null/empty)
- [ ] Ed25519 keypair generation
- [ ] Key storage
- [ ] Key recovery (mnemonic)
- [ ] Auth layers
- [ ] Composite signing key
- [ ] Trust score storage
- [ ] Facet scores
- [ ] Vouch creation
- [ ] 3-hop chain calculation
- [ ] Heritage contacts
- [ ] Recovery contacts
- [ ] Permission groups
- [ ] Trust sync to central
- [ ] Profile sync to central

**Status: 0/14 backend features work. All bridge APIs return empty.**

---

## 5 · Settings sync (browsy ← central, unidirectional)

### Flow
```
User changes setting in central
  → floveSettings.set(key, val)
  → writes to localStorage (flove:key)
  → if browsy installed:
      → chrome.runtime.sendMessage({ type: 'setting-changed', key, val })
      → background.js writes to chrome.storage.local (flove-key)
      → background.js writes to chrome.storage.sync (flove-key) [if < 8KB]
```

### Conflict resolution: browsy wins
```
If browsy has value → use browsy
If browsy has no value → use localStorage
If neither → use default
```

### Storage keys
| Setting | localStorage | chrome.storage.local | chrome.storage.sync |
|---------|-------------|---------------------|-------------------|
| Theme | `flove:theme` | `flove-theme` | `flove-theme` |
| Language | `flove:language` | `flove-language` | `flove-language` |
| Sound | `flove:sound` | `flove-sound` | `flove-sound` |
| Sound level | `flove:soundLevel` | `flove-soundLevel` | `flove-soundLevel` |
| Notifications | `flove:notifications` | `flove-notifications` | `flove-notifications` |
| Wizy | `flove:wizy` | `flove-wizy` | `flove-wizy` |

---

## 6 · Profile data structure

```js
// browsy-profile (chrome.storage.local)
{
  pubkey: "ed25519_public_key_hex",
  displayName: "Marc",
  avatar: null,                    // or URL
  settings: {
    theme: "dark",
    language: "es",
    sound: true,
    soundLevel: "basic",
    notifications: true,
    wizy: true
  },
  created: "2026-01-01T00:00:00Z",
  lastSync: "2026-07-27T10:00:00Z"
}
```

---

## 7 · browsy-trust data structure

```js
// browsy-trust (chrome.storage.local)
{
  score: 0.78,                     // overall trust score
  facets: {
    personal: 0.85,                // from vouches
    local: 0.70,
    social: 0.80,
    global: 0.65
  },
  mynet: {
    categories: ["garden", "trade", "community"],
    circles: ["friends", "colleagues"]
  },
  vouchCount: 47,
  lastCalculated: "2026-07-27T10:00:00Z"
}
```

---

## 8 · Suggestions (prioritized)

### Priority 1: Make bridge work
1. Implement real `getKeypair()` → Web Crypto in background SW
2. Implement real `getProfile()` → return profile object
3. Implement real `getScore()` → return trust score
4. Implement real `getFacets()` → return 4 facet scores
5. Test central reads bridge on load

### Priority 2: Settings sync
6. Add `chrome.storage.local` mirror to `flove-settings.js`
7. `floveSettings.set()` → localStorage + chrome.storage when browsy installed
8. Central caches bridge responses (browsy lighter)

### Priority 3: On-demand crypto
9. Key generation → background SW via message
10. Trust chain → Web Worker, < 2s for 100 vouches
11. Vouch signing → background SW
12. Cache results in central (avoids re-computation)

### Priority 4: Reliability
13. 100ms timeout on bridge calls → fallback to cache
14. Retry logic (1 retry, then fallback)
15. Service worker restart → re-bridge automatically
16. `chrome.storage.onChanged` listener in central

### Priority 5: Testing
17. `browsy/test.html` with sample content
18. Mock bridge for automated tests
19. Performance benchmarks (key gen, trust chain)
20. Test both installed + not-installed

---

## 9 · Test matrix

### A · Browsy standalone
| Test | Expected | Pass |
|------|----------|------|
| Extension loads, no errors | Clean console | |
| Context menus on right-click | "Save to flove" + "Share to Nety" | |
| Badge ★ on flove.org | Purple star | |
| Badge empty on non-flove | No badge | |
| Popup shows app info | Correct app name | |
| chrome.storage writable | Data persists | |

### B · Bridge API
| Test | Expected | Pass |
|------|----------|------|
| `window.flove.browsy` exists | Object present | |
| `getKeypair()` → real key | Ed25519 keypair | |
| `getProfile()` → profile obj | { pubkey, displayName, ... } | |
| `getScore()` → number | 0-1 | |
| `getFacets()` → 4 scores | { personal, local, social, global } | |
| `getVouches()` → array | 20-100 vouch objects | |
| `onUpdate()` fires | On storage change | |
| Response time < 100ms | Fast | |

### C · Settings sync
| Test | Expected | Pass |
|------|----------|------|
| Central: toggle → localStorage | `flove:theme` set | |
| Central: toggle → chrome.storage | `flove-theme` set | |
| Browsy: change → central updates | Central reads chrome.storage | |
| No browsy: localStorage only | Current behavior | |
| Browsy wins on conflict | chrome.storage value used | |

### D · Performance
| Test | Threshold | Pass |
|------|-----------|------|
| Bridge response | < 100ms | |
| Key generation (Web Worker) | < 500ms | |
| Trust chain (20 vouches) | < 200ms | |
| Trust chain (100 vouches) | < 2s | |
| Storage (100 vouches) | < 50KB | |
| Storage (total) | < 500KB | |

### E · Edge cases
| Test | Expected | Pass |
|------|----------|------|
| Service worker killed | Restart, no data loss | |
| Storage full | Error handled | |
| Bridge timeout (100ms) | Fallback to cache | |
| No browsy installed | Central works, trust empty | |
| Multiple tabs | Settings sync | |
| Chrome restart | Everything persists | |
| 500 vouches | Daily recalculation triggered | |

---

## 10 · File structure

```
browsy/
├── manifest.json          # MV3
├── background.js          # SW: context menus, badge, crypto, settings mirror
├── content.js             # bridge API (identity + trust)
├── popup.html             # extension popup
├── popup.js               # popup logic
├── icons/                 # icon-16/48/128/512.png
├── logos.html             # logo options
├── TESTING.md             # this file
└── lib/
    ├── tweetnacl.min.js   # ed25519 fallback (~20KB)
    └── worker.js          # Web Worker for heavy crypto

central/
├── index.html
├── features.md
├── libs/
│   ├── flove.css          # shared design system
│   ├── flove-settings.js  # shared settings (localStorage + chrome.storage)
│   ├── flove-sound.js     # shared sound engine
│   └── flove-i18n.js      # shared language toggle
└── apps/
    ├── blogy/
    ├── gody/
    └── ...
```
