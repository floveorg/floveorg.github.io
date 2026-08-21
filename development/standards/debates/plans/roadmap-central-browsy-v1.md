# Roadmap: Central + Browsy v1

> Consolidated build order from all existing plans. One document, one path to v1.
> Created 2026-07-26. Sources: central-backend.md, browser-extension.md, shared-code.md, browsy-keys-trust-performance.md, browsy-trust-logic-audit.md.

---

## Current state (2026-07-26)

| Component | Status |
|-----------|--------|
| Browsy extension | v0.1.0 shell — badge, context menus (log only), popup links, stats overlay |
| Central backend | Zero code. Design complete (CB01–CB50, D01–D23, E01–E25) |
| Central directory | `central/shared/` with css/ + js/ (flove.js, flove.css, flove-i18n.js), routing.json, scripts/ |
| Shared code | 47 apps enriched. Enrichment loader working. |
| Plan docs | 14+ files, ~800 decisions documented |

---

## v1 scope (what ships)

### Browsy v1 — "Ship It"
- Keys (Ed25519, self-contained, deterministic, recoverable)
- Auth (identity links — device + Telegram + email)
- 4 facets (personal/local/social/global)
- Direct vouches only (no delegation)
- Friends list = Close group
- 4 permission groups (Close, Public, Private, 1 custom)
- Publish flow (checkboxes, browsy signs)
- Wizy permission checks
- Audit trail (hash chain, local)
- Contextual trust (per-app)
- Trust portability (via key)
- Templates (maty, myfamily)
- Decryption at rest (extension isolation)
- Finetuner (click-only, flove.org pages only)

### Central v1 — "Data bank + frontend"
- FastAPI + Turso backend on Railway
- CRUD API for app data (save, list, update, delete)
- Trust sync endpoint (CRDT merge, delta-only)
- Device UUID identity → email claim
- flove.js Central module (detection, sync, bottom nav)
- Central modal (one-time onboarding)
- First 7 apps: goddy, souls, pracsys, myfamily, inventary, realy, keys
- `flove.org/api/*` GitHub Pages proxy to Railway

---

## Build phases

### Phase 1 — Central Backend (backend is the foundation)

Everything depends on the backend. Build it first, verify with curl, deploy.

**1a. Railway skeleton**
- [ ] `central/backend/main.py` — FastAPI app, CORS, auto-init tables
- [ ] `central/backend/requirements.txt` — fastapi, uvicorn, libsql-client
- [ ] `central/backend/apps.json` — app registry `[{name, category}]`
- [ ] `central/backend/.env.example` — CORS_ORIGINS, TURSO_URL, SMTP_*
- [ ] `central/backend/Dockerfile` or `railway.toml`
- [ ] Verify: `GET /api/ping` → `{ok: true, version: "1.0.0", features: [...]}`

**1b. CRUD endpoints**
- [ ] `POST /api/{app}/save` → `{ok: true, id: "..."}`
- [ ] `PUT /api/{app}/{id}` → `{ok: true}`
- [ ] `DELETE /api/{app}/{id}` → `{ok: true}`
- [ ] `GET /api/{app}/list?user=X&cursor=Y` → `{items: [...], next_cursor: "..."}`
- [ ] Error responses: always HTTP 200, `{ok: false, error: "code", detail: "..."}`
- [ ] Schema validation against `collect-schemas.json`

**1c. Trust sync**
- [ ] `central/backend/trust.py` — trust sync endpoint logic
- [ ] `POST /api/trust/sync` → `{ok: true, merged: N, conflicts: [...]}`
- [ ] Vector clock CRDT merge
- [ ] Delta-only payload handling

**1d. Identity**
- [ ] `user_config` table (user, email, created_at)
- [ ] Device UUID auto-generation
- [ ] Email claim flow (confirmation email via SMTP, 24h expiry)

**1e. Deploy**
- [ ] Railway project `flove-central` — two services (fastapi + libSQL Docker)
- [ ] libSQL volume at `/data/flove.db`
- [ ] Staging: `staging-railway-flove.org`
- [ ] GitHub Pages proxy: `/api/*` → Railway
- [ ] Verify end-to-end: curl against `flove.org/api/ping`

**1f. Tests**
- [ ] pytest on FastAPI endpoints with in-memory SQLite
- [ ] CRUD happy paths + error cases
- [ ] Trust sync merge + conflict scenarios

**Dependencies:** None. This is the first thing to build.
**Decisions ref:** CB01–CB50, D01–D23, E01–E25, CB_S01–CB_S10

---

### Phase 2 — flove.js Central Module (bridge between backend and apps)

**2a. Central detection**
- [ ] `flove.js` pings `/api/ping` on load (same origin, GitHub Pages proxy)
- [ ] Cache result in `localStorage` for session
- [ ] Expose `window.flove.central.available` (boolean)

**2b. Sync logic**
- [ ] `window.flove.sync()` — triggers manual sync
- [ ] Auto-sync on load (silent, no feedback)
- [ ] `window.flove.collect()` — returns `{timestamp, selections, ratings}`
- [ ] Offline queue: IndexedDB log of pending operations
- [ ] `flove:pending-sync` flag with count

**2c. Bottom nav injection**
- [ ] Bottom fixed bar (48px): logo left → click opens full-screen menu
- [ ] Menu: chapters mirror `apps/` directory structure (Category → App)
- [ ] Current app detection via URL parsing
- [ ] Injected by flove.js, no per-app HTML needed

**2d. Central modal**
- [ ] One-time auto-show on first Central detection (advanced/super tiers)
- [ ] Brief explanation + "Got it, don't show again"
- [ ] Email input on first sync click (not in auto-modal)

**2e. Shared components**
- [ ] Rating widget (5-star click)
- [ ] Card view, modal, form helpers
- [ ] Expandable menu components
- [ ] CSS layout tokens from flove.css

**Dependencies:** Phase 1 deployed and responding.
**Decisions ref:** CA38–CA44, CB11–CB13, E08, E23–E25

---

### Phase 3 — First Central Apps (prove the pattern)

Port from Solo to Central. Central apps are thinner: no topbar, flove.js injects bottom nav.

**3a. goddy** (first app, category: metas)
- [ ] `central/apps/goddy.html` — minimal, flove.js-powered
- [ ] `collect()` returns goddy-specific data
- [ ] Sync works end-to-end

**3b. souls, pracsys, myfamily, inventary, realy, keys**
- [ ] One at a time, same pattern as goddy
- [ ] `apps.json` updated with each app
- [ ] `collect-schemas.json` updated per app
- [ ] Manual testing: each app syncs, lists, updates, deletes

**3c. Central index.html**
- [ ] Minimal launcher with links to all apps
- [ ] Matches Solo's index pattern

**Dependencies:** Phase 2 complete.
**Decisions ref:** E04a, E05, CB_S08

---

### Phase 4 — Browsy Keys + Auth (identity foundation)

The identity layer is prerequisite for everything trust-related.

**4a. Ed25519 key generation**
- [ ] Deterministic key from auth factors (device + Telegram + email)
- [ ] Self-contained: works offline, no server dependency
- [ ] Stored in Extension storage (encrypted at rest via extension isolation)
- [ ] 12-word mnemonic recovery code

**4b. Auth layers**
- [ ] Layer 0: Device (base, always present)
- [ ] Layer 1: Telegram (verified)
- [ ] Layer 2: Email (certified)
- [ ] Layer 3: Trust vouches (web of trust)
- [ ] Composite signing key derived from all layers
- [ ] Factor count visible to receivers ("3-factor signed")

**4c. Recovery**
- [ ] Re-link factors + recovery code at setup
- [ ] 2-of-5 social recovery (recovery contacts)
- [ ] Recovery contacts stored in browsy (never published)

**Dependencies:** None (can parallel with Phase 1–3).
**Decisions ref:** Q93–Q124, browsy-keys-trust-performance.md

---

### Phase 5 — Browsy Trust System (core social features)

**5a. Vouch system**
- [ ] Vouch = signed statement `{from, to, timestamp, trustLevel, signature}`
- [ ] Rules: `from.personal ≥ 5`, `strength ≤ from.facet`, max 50 active vouches
- [ ] One active vouch per `(from, to, facet, scope)` — duplicates overwrite
- [ ] Revocation: original key only, propagates downstream

**5b. 4 facets**
- [ ] Personal: identity links only (anchor, no delegation)
- [ ] Local: peer vouches, chain depth 1, 90d decay
- [ ] Social: network vouches, chain depth 3, 60d decay
- [ ] Global: hardware share + published content, 30d idle decay
- [ ] Each facet 0–100, computed independently

**5c. Friends = Close group**
- [ ] Friend = direct vouch (mutual/outgoing/incoming)
- [ ] Friends list IS the Close group member list
- [ ] Stale after 60 days no interaction
- [ ] Adding = vouching, removing = revoking

**5d. 4 permission groups**
- [ ] Close (default: MyNet), Public, Private, Custom (1 slot)
- [ ] Flat, no nesting, O(1) lookup
- [ ] Group contains: people, rules, context pointers
- [ ] Stored in Extension storage (`browsy:groups:*`)

**5e. Trust contracts**
- [ ] Standard contracts: `publish:{app}:{scope}`, `view:{app}:{scope}`, `vouch:{scope}`
- [ ] Evaluation: `can(keyA, action, context) → contract.evaluate(keyState) → boolean`
- [ ] Templates: maty (personal circle), myfamily (family circle)

**5f. Audit trail**
- [ ] Hash chain: each entry links to previous via `prevHash`
- [ ] SHA-256 of `(seq + action + from + to + ... + prevHash)`
- [ ] Actions: vouch, revoke, permission_check, publish, key_rotate
- [ ] Local only (Extension storage), max 1MB with LRU eviction
- [ ] Merkle summary for pruned entries

**Dependencies:** Phase 4 complete.
**Decisions ref:** browsy-trust-logic-audit.md §2–§10

---

### Phase 6 — Browsy ↔ Central Sync

**6a. Trust sync**
- [ ] `POST /api/trust/sync` — delta-only payload
- [ ] Vector clock CRDT merge (client-side)
- [ ] Conflicts surfaced to browsy for display
- [ ] Immediate on change (real-time)

**6b. Profile sync**
- [ ] Batched 5 min on idle (chrome.alarms)
- [ ] Full profile on each sync
- [ ] Offline queue in IndexedDB

**6c. App data sync**
- [ ] Via flove.js Central module (Phase 2)
- [ ] Auto-sync on load (silent)

**Dependencies:** Phase 1 (backend trust endpoint) + Phase 5 (trust system).
**Decisions ref:** CB41–CB43, Q205–Q224

---

### Phase 7 — Browsy Finetuner (on-demand insights)

**7a. Click-only scoring**
- [ ] Runs when user clicks wizy icon
- [ ] Zero background CPU, no MutationObserver
- [ ] Full navigation only, manual re-score button

**7b. flove.org detection (v1)**
- [ ] HTML parsing for content extraction
- [ ] User-declared interests from profile
- [ ] No external sites (v1)

**7c. Permission check on click**
- [ ] Load groups, trust slice, context pointers
- [ ] Evaluate trust contracts
- [ ] Return filtered results

**7d. Wizy agent**
- [ ] Deep analysis client-side using local trust + profile
- [ ] Summary only (~1KB) to pages
- [ ] Degrades gracefully when Central offline
- [ ] Context doc changes → mark stale, re-score on next click

**Dependencies:** Phase 5 (trust system) + Phase 2 (flove.js).
**Decisions ref:** browsy-keys-trust-performance.md §Finetuner

---

### Phase 8 — Publish Flow + Wizy Integration

**8a. Publish checkboxes**
- [ ] Replace dropdown with checkbox group selection (up to 3 groups)
- [ ] browsy signs content (full content + timestamp + sender key)
- [ ] Save = local only. Publish = local + GitHub + Central

**8b. Wizy permission checks**
- [ ] App queries browsy: "does key X pass the contract?"
- [ ] browsy evaluates trust contract against key state
- [ ] Returns boolean + score + confidence

**8c. Publish consent**
- [ ] Consent at trust time ("Allow B to publish your trust?")
- [ ] Scope: only the fact of trust (A trusts B)
- [ ] Revocable anytime, visible in trusts settings

**Dependencies:** Phase 5 (trust + groups) + Phase 6 (sync).
**Decisions ref:** Q150–Q193, browsy-keys-trust-performance.md §Publish

---

### Phase 9 — Polish + Testing

**9a. Browsy**
- [ ] Firefox compatibility (MV2 adaptation)
- [ ] Icons and badge design
- [ ] Store listings (Chrome + Firefox)
- [ ] Documentation (README, API docs, user guide)
- [ ] Security audit

**9b. Central**
- [ ] Error handling edge cases
- [ ] Rate limiting (per-IP, 100 req/min — post-PoC)
- [ ] Schema migration files
- [ ] Monitoring (Railway logs)

**9c. Integration testing**
- [ ] End-to-end: browsy install → key creation → vouch → sync → Central store
- [ ] Offline → online recovery
- [ ] Multi-device sync
- [ ] Conflict resolution scenarios

**Dependencies:** Phases 1–8 complete.

---

## Execution order (recommended)

```
Week 1-2:  Phase 1 (Central backend) ← blocking everything
Week 2-3:  Phase 2 (flove.js Central module) ← can start with detection while backend stabilizes
Week 3-4:  Phase 4 (Browsy keys + auth) ← parallel with Phase 2-3
Week 4-5:  Phase 3 (First Central apps) ← needs Phase 2
Week 5-7:  Phase 5 (Browsy trust system) ← needs Phase 4
Week 7-8:  Phase 6 (Browsy ↔ Central sync) ← needs Phase 1 + 5
Week 8-9:  Phase 7 (Finetuner) ← needs Phase 5
Week 9-10: Phase 8 (Publish flow) ← needs Phase 5 + 6
Week 10+:  Phase 9 (Polish)
```

**Critical path:** Phase 1 → Phase 2 → Phase 3 → Phase 6
**Parallel track:** Phase 4 → Phase 5 → Phase 7/8

---

## Key decisions to respect

| Rule | Source |
|------|--------|
| v1 = direct vouches only (no delegation/chains) | browsy-trust-logic-audit.md §13 |
| 4 groups, flat (Close, Public, Private, 1 custom) | browsy-keys-trust-performance.md Q19 |
| Friends = Close group | browsy-trust-logic-audit.md §3.3 |
| Finetuner = click-only, flove.org only (v1) | browsy-keys-trust-performance.md Q1-Q2 |
| Central apps = thinner than Solo (no topbar, shared bottom nav) | central-backend.md E22 |
| Backend first, apps second | central-backend.md D08 |
| All HTTP 200 with error body | central-backend.md D22 |
| Extension storage for ALL browsy data | browser-extension.md Unified Storage |
| 50MB storage / 100MB memory / 1% CPU idle | browser-extension.md Q227 |
| Encryption at rest = extension isolation sufficient (v1) | browsy-trust-logic-audit.md §8.4 |
| Trust sync = delta-only, real-time | browser-extension.md Q210 |
| 1MB limit for app data, trust sync separate | central-backend.md CB_S01 |

---

## What stays out of v1

| Feature | Why deferred |
|---------|-------------|
| Delegation / chain trust | Complex, needs chain logic |
| Key rotation + probation | Needs trust revocation propagation |
| External site parsing (finetuner) | v2 scope |
| P2P (nety extension layer) | Optional, nety Rust stack must mature first |
| CentralRich (PostgreSQL + JSONB) | When Turso outgrows needs |
| WASM scoring | Performance optimization, not v1 |
| Anomaly detection | Needs chain analysis |
| Cross-key audit | Needs public entry visibility |
| blogy Central adaptation | After first 6 prove the pattern |
| Rate limiting | Post-PoC, after Railway stable |
| Multi-user auth | CentralRich scope |

---

## Pending — offline via Service Worker (browsy · wisy)

Status: **pending** (added 2026-08-07). Connected apps: **browsy**, **wisy**.

Give **browsy** and **wisy** offline behaviour that matches the `flove-solo.zip`
download, without baking a media copy into the Android TWA. Approach: extend the
**generated** `solo/sw.js` precache (see `solo/README.md` distro pipeline §2) to
cover the resources these apps need offline, so any device that has visited once
while online keeps working offline — instead of shipping the APK with baked-in
assets (apk bloat + a manual rebuild on every content change).

Consequences to settle when the work is picked up:
- Which resources each app needs offline (pages, css/js, small in-app assets —
  **no** audio or big images, matching the zip's text-only packaging rule).
- Precache size vs browser quota/eviction (~50 MB) — keep the subset curated.
- Keep offline behaviour aligned across the three surfaces: zip (text-only),
  live web, and APK wrapper.

---

## Cross-plan dependencies

```
Phase 1 (Central backend)
  ↓
Phase 2 (flove.js Central module)
  ↓
Phase 3 (First Central apps)

Phase 4 (Browsy keys + auth)     ← parallel
  ↓
Phase 5 (Browsy trust system)
  ↓                    ↓
Phase 6 (Sync)    Phase 7 (Finetuner)
  ↓
Phase 8 (Publish flow)

Phase 9 (Polish) ← after all above
```
