# flove — Central distro standards

The Central distro runs on FastAPI + Turso (Railway), served via GitHub Pages
proxy at `flove.org/api/*`. Apps are single-file HTML like Solo, but with
backend sync. The browsy browser extension handles identity, trust, and sync —
**apps stay light**.

This document is the single home for Central-specific rules. It covers both
frontend (app structure) and backend (API contract, extension bridge). For Solo/F0
standards see `backend.md`; for the general frontend catalogue see `frontend.md`.

---

## 1 · What Central is

| Property | Value |
|----------|-------|
| Backend | FastAPI + Turso (libSQL), serverless on Railway |
| Serving | GitHub Pages (`floveorg.github.io`) with API proxy |
| Apps | Single-file HTML, self-contained, no build step |
| Identity | browsy extension (Ed25519 keys, email + Telegram) |
| Trust | 3-hop web of trust, CRDT vector clocks |
| Sync | Batched 5 min, offline queue in IndexedDB |
| Branch | `central/` (full fork of `main`) |

**Core principle:** the extension does the heavy lifting. Apps are thin
presentation layers. If a feature requires identity, trust, or sync, delegate
to the extension — don't reimplement it in the app.

---

## 2 · Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Central app   │────▶│  browsy extension │────▶│ Central backend │
│  (single HTML)  │◀────│  (chrome.storage) │◀────│ (FastAPI+Turso) │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                       │                         │
        │   window.flove       │   chrome.storage.local  │  /api/*
        │   postMessage        │   Ed25519 keys          │  REST JSON
        │                      │   CRDT sync             │
```

**Communication paths:**
- App ↔ Extension: `window.flove` namespace + `postMessage` bridge
- Extension ↔ Backend: `fetch('/api/...')`, batched sync
- App ↔ Backend: direct `fetch` for simple reads (ping, list)

---

## 3 · API contract

All endpoints at `flove.org/api/*` (proxied to Railway).

| Endpoint | Method | Purpose | Response |
|----------|--------|---------|----------|
| `/api/ping` | GET | Health check + version | `{ok, version, features[]}` |
| `/api/{app}/save` | POST | Save document | `{ok, id}` |
| `/api/{app}/{id}` | PUT | Update document | `{ok}` |
| `/api/{app}/{id}` | DELETE | Delete document | `{ok}` |
| `/api/{app}/list` | GET | List user docs | `{items[], next_cursor}` |
| `/api/{app}/export` | GET | Export all as NDJSON | file download |
| `/api/trust/sync` | POST | Trust delta sync | `{ok, merged, conflicts[]}` |
| `/api/nety/sync` | POST | Nety profile sync | `{ok}` |

**Identity:** device UUID first (anonymous), email claim later.
**Conflict resolution:** LWW for app data, CRDT vector clocks for trust.
**Page size:** 20, cursor-based pagination.

---

## 4 · Extension bridge

The browsy extension exposes APIs to apps via `window.flove`:

```js
window.flove = {
  distro: 'central',        // set by extension
  tier: 'normal',           // set by extension
  app: 'appy',              // set by app
  profile: {                // from extension storage
    handle: '@marc',
    avatar: 'M',
    trustScore: 42,
    facets: { personal: 0, local: 0, social: 0, global: 0 }
  },
  sync: { status: 'on', lastSync: '...' },
  emit(event, data),        // dispatch custom event
  on(event, fn)             // listen for custom event
};
```

**What the extension provides (don't reimplement):**

| Feature | Extension provides | App should... |
|---------|-------------------|---------------|
| Profile | handle, avatar, trust score | Display from `window.flove.profile` |
| Trust scores | facets, web of trust graph | Show scores, delegate actions to extension |
| Sync | status, last sync time | Display status indicator |
| Auth | email magic link + Telegram | Show auth sheet, delegate to extension |
| Identity links | linked accounts | Don't re-implement identity scale |
| Key rotation | Ed25519 key management | Delegate to extension UI |

---

## 5 · App structure contract

Every Central app must follow:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <meta name="flove:distro" content="central">
  <meta name="flove:tier" content="normal">
  <meta name="flove:app" content="myapp">
  <title>myapp · Central</title>
  <!-- one font max, or system fonts -->
  <style>/* self-contained CSS */</style>
</head>
<body>
  <!-- top bar, main content, bottom nav -->
  <script>/* self-contained JS */</script>
</body>
</html>
```

### Rules

| Rule | Detail |
|------|--------|
| Single file | Everything in one HTML file, no external JS/CSS (except fonts) |
| One font max | Space Mono for body, or system fonts. No more than one Google Font |
| No heavy animation | No mesh gradients, aurora, glassmorphism, or multi-ring SVGs |
| Inline SVG ≤ 24×24 | Use simple shapes. Complex graphics → external or CSS |
| Max ~500 lines | Target for normal tier. Advanced can go to ~800 |
| `collect()` | Define `window.flove.collect()` for Central sync |
| `flove:*` meta tags | Must include distro, tier, app name |
| `window.flove` | Namespace with distro, tier, app, version |
| Dark mode | Single `@media (prefers-color-scheme: dark)` override |
| Reduced motion | Single `@media (prefers-reduced-motion: reduce)` rule |
| Safe areas | Use `env(safe-area-inset-*)` for notched devices |

---

## 6 · Navigation

Central apps use **bottom nav** (no topbar, no hamburger).

### Bottom nav spec

- Fixed bottom, `z-index: 500`
- 4 buttons max: apps, mynet, notifs, settings
- Each button: icon (≤24×24 SVG) + label (uppercase, 0.42rem)
- Active state: accent color + subtle glow
- Safe area padding at bottom

### Panel switching

```css
.nav-panel { display: none; }
.nav-panel.active { display: block; }
```

No animation or minimal `reveal-up` (0.2s max). No fullscreen overlays.

### Menu abstraction

Reusable across all Central apps:

```css
.folder { margin-bottom: 0.15rem; }
.folder-head { display: flex; align-items: center; gap: 0.4rem;
  padding: 0.4rem 0.55rem; border-radius: 8px; cursor: pointer; }
.folder-body { max-height: 0; overflow: hidden; transition: max-height 0.28s; }
.folder-body.open { max-height: 500px; opacity: 1; }
.menu-item { display: flex; align-items: center; gap: 0.4rem;
  padding: 0.3rem 0.55rem 0.3rem 1.4rem; font-size: 0.52rem; }
```

Folders are collapsed by default. Click head to toggle. Items link to
`../<folder>/<app>.html` (relative paths, `target="_blank"`).

---

## 7 · Auth model

Central apps use a **minimal auth overlay**:

- Profile card with avatar (initial) + handle + badges
- Auth button opens slide-up sheet
- Password gate for recovery (password: `flove`)
- Trust scores displayed as **single number** (not 4 SVG rings)
- Seed phrase, quorum, key rotation → handled by extension, not app

### What the auth overlay shows

1. Profile handle + badges (LIVE, CENTRAL)
2. Trust score number
3. Password gate → recovery trusts
4. Close button

### What it does NOT show (extension handles these)

- 5-step identity scale
- Seed phrase display
- Social quorum peer list
- Key rotation / probation
- Loss vs compromise explanation

---

## 8 · Persistence model

| Level | Store | What |
|-------|-------|------|
| P0 | `chrome.storage.local` (extension) | Identity, trust, profile, settings |
| P1 | `localStorage` (app) | UI state, open panels, form drafts |
| P2 | In-memory | This session only |

### Key convention

All keys prefixed with `flove:`:
- `flove:lang` — shared language
- `flove:theme` — shared theme
- `flove:pending-sync` — sync queue flag
- `flove:version` — app version
- `flove:<app>:items` — app data
- `flove:<app>:v` — app version

### collect() contract

Every app defines what syncs to Central:

```js
window.flove.collect = function() {
  return {
    app: 'happy',
    version: '1.0.0',
    items: [],      // what to sync
    metadata: {}    // app-specific
  };
};
```

---

## 9 · Sync model

```
App (P1)  ──collect()──▶  Extension  ──batch/5min──▶  Central API
   ▲                           │                          │
   └───── render from ─────────┘◀──── merge/conflict ──────┘
```

- Extension batches every 5 minutes
- Offline: queue in IndexedDB, retry on reconnect
- Conflict: LWW for app data, CRDT for trust data
- App shows status via `/api/ping` response
- `flove:pending-sync` flag indicates queue has items

---

## 10 · Minimal CSS template

```css
/* Reset */
* { margin: 0; padding: 0; box-sizing: border-box; }

/* Variables */
:root {
  --bg: #f3f4fb; --ink: #16141f; --muted: #4a4e5a;
  --accent: #6c5ce7; --signal: #02855c;
  --card: #fff; --line: #e3e5f0;
  --nav-h: 56px;
  --safe-b: env(safe-area-inset-bottom, 0px);
}

/* Layout */
.wrap { max-width: 960px; margin: 0 auto; padding: 1rem clamp(1rem,4vw,2rem); }
.sec { font-size: 0.54rem; letter-spacing: 0.3em; text-transform: uppercase;
  color: var(--muted); margin: 1.2rem 0 0.65rem; }

/* Card */
.card { background: var(--card); border: 1px solid var(--line);
  border-radius: 12px; padding: 1rem; }

/* Bottom nav */
.bottom-nav { position: fixed; bottom: 0; left: 0; right: 0;
  height: calc(var(--nav-h) + var(--safe-b)); z-index: 500;
  background: rgba(255,255,255,.95); backdrop-filter: blur(20px);
  border-top: 1px solid var(--line); display: flex;
  align-items: center; justify-content: space-around; }

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root { --bg: #1a1b26; --ink: #e0e0e0; --muted: #9aa5ce;
    --line: #2f3347; --card: #24283b; --accent: #7aa2f7; --signal: #9ece6a; }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```

---

## 11 · Relationship to other standards

| Standard | Central apps must... |
|----------|---------------------|
| §13.1 Tier model | Follow tier rules (mini→super) |
| §13.2 i18n | Support `.t-en`/`.t-es` if multilingual |
| §13.6 Onboarding | Include first-use intro |
| §13.10 Nav-tab title | `<App> · FLOVE` format |
| §13.14 Theme | Support light/dark via `flove:theme` |
| `contract.md` | Follow all mandatory rules (§0–8) |
| `persistence.md` | Follow P0/P1/P2 model |
| This doc (`central.md`) | Follow Central-specific rules above |
