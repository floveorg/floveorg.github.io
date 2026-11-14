# browsy

Chrome extension that bridges flove apps with the web. Backend only — all frontends live in central.

## Architecture

```
browsy (chrome extension)         central (flove.org + FastAPI + LibSQL)
──────────────────────            ─────────────────────────────────────
backend only                      all frontends + trust hub
chrome.storage.local              localStorage (fallback)
chrome.storage.sync               multi-device sync
crypto (ed25519)                  trust graph aggregation
content script (bridge API)       permissions engine
background.js (service worker)    URL obfuscation
web worker (heavy crypto)         group management
F2F verification (QR+challenge)   encrypted content storage
permissions cache                 F2F record storage
auto-decrypt (local keys)         key rotation
```

**Core rule:** On-demand only. No background calculations. No auto-sync. User clicks → browsy computes → central displays.

**What central adds:** Trust graph across all users, multi-device sync, F2F record storage, permissions enforcement, URL obfuscation, group management, encrypted content storage, key rotation. browsy can't do any of this alone.

## Decisions

| Topic | Decision |
|-------|----------|
| Calculations | On-demand only (click) |
| Crypto | Web Crypto primary + tweetnacl fallback |
| Key generation | Background service worker |
| Vouches expected | 20-100 per user |
| Trust chain | On demand, < 2s for 100 vouches |
| Vouch revocation | Recalculate in bundled daily session |
| Settings sync | Unidirectional: browsy → central |
| Conflict resolution | Browsy wins |
| chrome.storage.sync | Yes for settings (multi-device) |
| Web Workers | Yes, if crypto exceeds 30s SW lifetime |
| Cache in central | Yes — central caches bridge responses |
| Bridge response target | < 100ms |
| Testing | Both installed + not-installed |
| Browsers | Chrome, Firefox, Safari |
| Mock bridge | Yes, for automated tests |

## File structure

```
browsy/
├── manifest.json          # MV3 manifest
├── background.js          # service worker: context menus, badge, crypto, settings mirror
├── content.js             # bridge API (identity + trust)
├── popup.html             # extension popup
├── popup.js               # popup logic
├── index.html             # landing page (browsy.flove.org)
├── logos.html             # logo options
├── icons/                 # icon-16/48/128/512.png
└── lib/
    ├── tweetnacl.min.js   # ed25519 fallback (~20KB)
    └── worker.js          # Web Worker for heavy crypto

Docs live in apps/dev/browsy/:
├── README.md              # this file
└── TESTING.md             # test plan + risk analysis
```

## What's implemented

- [x] Context menus (Save/Share)
- [x] Badge detection (★ on flove pages)
- [x] Popup UI (app suggestions)
- [x] Content script bridge skeleton
- [x] `chrome.storage.onChanged` listener

## What's stubbed

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
- [ ] Settings mirror (chrome.storage)
- [ ] Trust sync to central
- [ ] Profile sync to central
- [ ] F2F verification (QR + challenge signing)
- [ ] Permissions cache (check central, cache locally)
- [ ] Obfuscated URL detection (`/p/` routes)
- [ ] Group membership cache
- [ ] Auto-decrypt (decrypt content with stored keys)

## Data structures

### Vouch
```js
{
  id: "v_abc123",
  from: "ed25519_pubkey_hex",
  to: "ed25519_pubkey_hex",
  score: 0.85,
  facets: { personal: 0.9, local: 0.7, social: 0.8, global: 0.6 },
  message: "Known for 3 years",
  created: "2026-07-27T10:00:00Z",
  revoked: null
}
```

### Profile
```js
{
  pubkey: "ed25519_public_key_hex",
  displayName: "Marc",
  avatar: null,
  settings: { theme, language, sound, soundLevel, notifications, wizy },
  created: "2026-01-01T00:00:00Z",
  lastSync: "2026-07-27T10:00:00Z"
}
```

### Trust
```js
{
  score: 0.78,
  facets: { personal: 0.85, local: 0.70, social: 0.80, global: 0.65 },
  mynet: { categories: ["garden","trade","community"], circles: ["friends","colleagues"] },
  vouchCount: 47,
  lastCalculated: "2026-07-27T10:00:00Z"
}
```

## Setup

1. Go to `chrome://extensions`
2. Enable Developer mode
3. Click Load unpacked
4. Select `browsy/` folder

## Testing

See [TESTING.md](TESTING.md) for full test plan and risk analysis.
