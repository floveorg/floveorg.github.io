# Flove Feature Matrix

**Architecture rule: Browsy = backend only. Central = all frontends.**

---

## Implemented (59 features)

### Browsy — Backend (22)

#### Identity (9)
| # | Feature | What it does |
|---|---------|-------------|
| 1 | Ed25519 keypair generation | Creates device-bound signing key |
| 2 | Key storage (chrome.storage) | Persists keys locally |
| 3 | Key recovery (12-word mnemonic) | Backup/restore via seed phrase |
| 4 | Auth: device layer | Device-only auth path |
| 5 | Auth: Telegram layer | Telegram-linked auth |
| 6 | Auth: email layer | Email-linked auth |
| 7 | Auth: trust vouches layer | Vouch-based auth |
| 8 | Composite signing key | Combines layers into one key |
| 9 | Profile bridge API | `window.flove.browsy.identity.getProfile()` |

#### Trust (7)
| # | Feature | What it does |
|---|---------|-------------|
| 10 | Trust score storage | Saves scores to chrome.storage |
| 11 | Facet scores | personal/local/social/global |
| 12 | Vouch creation & storage | Creates and persists vouches |
| 13 | 3-hop chain calculation | Computes trust chains |
| 14 | Heritage contacts | Stores heritage contacts |
| 15 | Recovery contacts | Stores recovery contacts |
| 16 | Permission groups | Stores permission groups |

#### Extension Backend (3)
| # | Feature | What it does |
|---|---------|-------------|
| 17 | Context menus (Save/Share) | Right-click actions |
| 18 | Badge detection | Detects badges on pages |
| 19 | Extension background service worker | Core extension lifecycle |

#### Bridge APIs (3)
| # | Feature | What it does |
|---|---------|-------------|
| 20 | Trust bridge API | `window.flove.browsy.trust.getScore()` etc. |
| 21 | Trust sync to central | Pushes trust data to central |
| 22 | Profile sync to central | Pushes identity data to central |

---

### Central — Frontend (37)

#### Settings UI (9)
| # | Feature | What it does |
|---|---------|-------------|
| 23 | Theme toggle (light/dark/system) | `data-theme` attr |
| 24 | Language selector (en/es/fr) | |
| 25 | Sound on/off | |
| 26 | Sound depth level (5 levels) | off/mini/basic/normal/advanced/super |
| 27 | Notifications toggle | UI only; browsy backend |
| 28 | Wizy suggestions toggle | UI only; browsy backend |
| 29 | Settings persistence (localStorage) | Fallback without browsy |
| 30 | Settings UI (sety panel) | Panel with toggles |
| 31 | Settings bridge (browsy↔localStorage) | Dual persistence |

#### Nav & Panels (6)
| # | Feature | What it does |
|---|---------|-------------|
| 32 | Bottom nav bar | Visual; needs browsy for actions |
| 33 | Panel switching | Routes between sections |
| 34 | Top bar (search, ago, +) | Header |
| 35 | MyNet panel (categories + circles) | browsy actions render here |
| 36 | Notifications panel | browsy data renders here |
| 37 | Security panel | browsy security state renders here |

#### Content (6)
| # | Feature | What it does |
|---|---------|-------------|
| 38 | Feed with thematic tabs | blogy embedded; garden/trade/community/growth/wellness |
| 39 | Appy agent | browsy actions effective on them |
| 40 | Trust network display | 4 themes |
| 41 | Per Scores (4 facets) | personal/local/social/global from browsy trust |
| 42 | Identity scale | Visual scale |
| 43 | Profile card | browsy identity renders here |

#### Design System (6)
| # | Feature | What it does |
|---|---------|-------------|
| 44 | flove.css | ~759 lines, 17 sections |
| 45 | Theme vars + data-theme attrs | light/dark |
| 46 | Glassmorphism cards | |
| 47 | Avatar gradients | |
| 48 | Animations + reveals | |
| 49 | Reduced motion | `prefers-reduced-motion` |

#### Sound (6)
| # | Feature | What it does |
|---|---------|-------------|
| 50 | flove-sound.js | Derived from blogy |
| 51 | flove-settings.js | |
| 52 | Web Audio synth engine | PACK_SOFT sine tones |
| 53 | Delegated click sounds | `data-sound` attr |
| 54 | Speech synthesis | |
| 55 | Sound level selector UI | |

#### Export & UI (4)
| # | Feature | What it does |
|---|---------|-------------|
| 56 | Export buttons | |
| 57 | Cube modal | |
| 58 | Central backend ping | |
| 59 | flove-i18n.js | 115 lines |

---

## Summary

| Owner | Backend | Frontend | Total |
|-------|---------|----------|-------|
| Browsy | 22 | 0 | 22 |
| Central | 0 | 37 | 37 |
| **Total** | **22** | **37** | **59** |

## Data flow

```
browsy backend                     central frontend
─────────────                      ────────────────
keypair ──────────────────────────► profile card
trust score ──────────────────────► per scores, trust network
facet scores ─────────────────────► per scores columns
vouches ──────────────────────────► trust network
heritage/recovery ────────────────► security panel
permission groups ───────────────► security panel
auth state ──────────────────────► identity scale, nav state
context menus ───────────────────► (extension chrome)
badge detection ─────────────────► (extension chrome)
```

## Serverless → browsy persistence

Central uses free/serverless features that browsy must mirror:

| Central feature | localStorage key | browsy chrome.storage key |
|----------------|-----------------|--------------------------|
| Theme | `flove:theme` | `flove-theme` |
| Language | `flove:language` | `flove-language` |
| Sound | `flove:sound` | `flove-sound` |
| Sound level | `flove:soundLevel` | `flove-soundLevel` |
| Notifications | `flove:notifications` | `flove-notifications` |
| Wizy | `flove:wizy` | `flove-wizy` |

**Source of truth:** browsy chrome.storage when installed, central localStorage when not.

## Decisions

| Topic | Decision |
|-------|----------|
| Calculations | On-demand only (click) — lightest for browsy |
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
| Profile data | Identity + settings |
| browsy-trust data | MyNet + vouches + chain + facets |

---

## Planned — Next (19 features)

### Architecture (5) — HIGH
| # | Feature | Why |
|---|---------|-----|
| 60 | Component registry | Pages declare once, central initializes |
| 61 | Event bus | Decouple browsy bridge from DOM |
| 62 | Page manifest (JSON) | Central renders nav/panels from data |
| 63 | CSS `--page-*` cascade | Pages override theme safely |
| 64 | Module loader | Pages load only what they need |

### UI (5) — HIGH/MED
| # | Feature | Why |
|---|---------|-----|
| 65 | Skeleton loading states | Per panel, perceived perf |
| 66 | Transition manager | Consistent crossfade/slide |
| 67 | Keyboard nav | a11y, power users |
| 68 | Toast system | Replace scattered `.showToast()` |
| 69 | Responsive breakpoints | Consistent tokens |

### Data (3) — HIGH/MED
| # | Feature | Why |
|---|---------|-----|
| 70 | IndexedDB cache | Offline-first |
| 71 | Conflict resolution | Multi-device |
| 72 | Delta sync | Bandwidth |

### Extensibility (6) — MED
| # | Feature | Why |
|---|---------|-----|
| 73 | Plugin hooks | Third-party pages |
| 74 | Page templates | New apps in 5 min |
| 75 | Micro-components | badge, chip, progress |
| 76 | Browsy settings bridge | chrome.storage ↔ localStorage |
| 77 | Central browsy settings panel | Settings UI for browsy features |
| 78 | Central browsy content panels | MyNet, notifications, security, scores rendered |

---

## Future (10 features)

| # | Feature | When |
|---|---------|------|
| 79 | Service worker (offline) | All pages stable |
| 80 | Web push | Backend supports |
| 81 | Background sync | Offline-first real |
| 82 | Share Target API | browsy+central merge |
| 83 | File System Access | Export grows |
| 84 | Protocol handlers (`flove://`) | Deep linking |
| 85 | PWA manifest | Installable |
| 86 | CRDT sync | Multi-device real |
| 87 | i18n plural rules | More languages |
| 88 | CSP hardening | Production |

---

## Grand total: 88 features
| | Done | Next | Future |
|--|------|------|--------|
| Browsy | 22 | 0 | 0 |
| Central | 37 | 19 | 10 |
| **Total** | **59** | **19** | **10** |
