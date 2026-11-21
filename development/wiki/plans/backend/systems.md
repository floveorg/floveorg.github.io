---
status: stable
section: backend/systems
created: 2026-11-21
also: [development/standards/systems.md, development/standards/storage.md, development/standards/mynet.md, development/standards/mds.md, development/standards/experience.md]
---

# Central backend plan

> Source: `development/wiki/archive/old/plans/central-backend.md` (archived 2026-11-21).
> Status 2026-11-17: superseded in part by `browsy/spec.md`; Central is now an optional mirror/host.

> **Status 2026-11-17 — superseded in part.** Current spec:
> [`spec.md`](../../archive/old/browsy/spec.md).
> Central is now optional mirror/host; its permissions and identity authority sections are superseded.

> Decisions: CB01-CB40 + C01-C76 + D01-D23 + E01-E25 + G01-G55 + CB_S01-CB_S10 (FastAPI + Turso backend for Central distro, serverless on Railway, libSQL everywhere, Nety-Central bridge, profile mirror, browsy integration).
> Cross-refs: `../../../standards/frontend/frontend.md` (self-contained apps),
> `../../archive/old/browsy/spec.md` (Authy/Wizy/Browsy model),
> `plans/2026-11-17-appy-authy-mynet.md` (Authy/MyNet),
> `plans/conflicts.md` (conflict resolutions),
> `plans/standards.md` §SD18 (distro strategy).

## Architecture Decision: Browser Extension + Central = CORE

**Key insight:** Browser Extension (browsy) + Central are the CORE of flove's trust/social features. Decentral Nety is an extension for P2P distributed computation only.

**Central = Data bank to enrich browsy navigations + frontend apps.**

**Key insight:** Central only hosts files and aggregates overwriting fields. Users may update their profile at GitHub, others at somewhere else. Central uses a single feed. Central host offers options that should be specced.

| Layer | Role | Location |
|-------|------|----------|
| **Browser Extension** | CORE — local score, web of trust, client-side trust features, main navigation | Browser addon |
| **Central** | DATA BANK + FRONTEND — hosts files, aggregates fields, single feed, enriches browsy | Railway backend + `central/apps/` |
| **Decentral Nety** | EXTENSION — P2P distributed computation only | Sub-folder in `decentral/` repo |

**Repo structure:**
- `central/` — backend, storage, API
- `decentral/` — nety + other P2P tools (extensible)

## Decisions made

### Core backend (CB01-CB40)

| ID | Topic | Decision |
|----|-------|----------|
| CB01 | Backend stack | Python/FastAPI, async, Turso (SQLite-compatible HTTP API). Serverless on Railway. No MongoDB. |
| CB02 | First app | blogy — prove Turso pattern before expanding |
| CB03 | API pattern | `POST /api/{app}/save`, `PUT /api/{app}/{id}`, `DELETE /api/{app}/{id}` |
| CB04 | Save response | `{ok: true, id: "..."}` — returns rowid for document reference |
| CB05 | List endpoint | `GET /api/{app}/list?user=name` — retrieves all docs for user |
| CB06 | Pagination | Cursor-based, page size 20, `?cursor=...` for next page |
| CB07 | Port | Part of Railway deployment — no fixed port |
| CB08 | API discovery | Relative `/api/` on same origin. Via GitHub Pages proxy on `flove.org`. No subdomain. |
| CB09 | User identity | Device-generated UUID first (anonymous). Claim with email later via settings modal. |
| CB10 | Authentication | None for proof-of-concept — device UUID, no passwords |
| CB11 | Sync trigger | Both: one-time auto-modal on first Central detection + permanent "Sync" button in topbar. Auto-sync on every load (silent). |
| CB12 | Sync UX | Button disabled while syncing. On success: resets. On error: specific server message + "Retry". Auto-sync failures are silent (retry next load). |
| CB13 | Central modal | One-time auto for advanced/super — shows explanation + "Got it, don't show again". No email prompt in modal (email on first sync click). |
| CB14 | Database | Turso (SQLite-compatible HTTP API). libSQL fork initially, migrate to Turso Database when stable. Self-hosted libSQL server on Railway (persistent volume). |
| CB15 | Data model | Full summary JSON — `{app, user, timestamp, data}` stored as JSON column |
| CB16 | Connection config | `.env` for `CORS_ORIGINS=https://flove.org` and `TURSO_URL=libsql://...` |
| CB17 | Server structure | Single `main.py` — loads app list from `addons/backend/apps.json` registry (simple list) |
| CB18 | Libs folder | Central has its own `addons/` (the former `central/libs/`) — NOT `apps/appy/`. Separate from SoloRich. Read-only for both deploy pipelines. |
| CB19 | Branch model | Full fork — `central/` branch diverges from `main`. Selective cherry-pick of bug fixes back to main. Deploy via PR merge → Railway auto-deploy. |
| CB20 | CORS | Configurable via `.env` — `CORS_ORIGINS=https://flove.org` for production, overridable for dev |
| CB20a | CORS staging | Allow both: `CORS_ORIGINS=https://flove.org,https://staging-railway-flove.org`. |
| CB21 | Start script | Railway auto-start via `Procfile` or `railway.toml`. Two services: FastAPI + libSQL server. Connected via internal Railway DNS. Local dev deferred. |
| CB22 | Error handling | Specific error messages from server — shown in the sync button area with "Retry" |
| CB23 | List response | Items only — `{items: [...], next_cursor: "..."}`. No total count. |
| CB24 | Prerequisites | Python 3.10+, `pip install fastapi uvicorn libsql-client` |
| CB25 | Data scope | Everything — full `window.flove.collect()` output stored as `data` JSON. App-defined shape, documented in `addons/backend/collect-schemas.json`. |
| CB26 | Deployment | Railway — simple deploy from GitHub, PR merge triggers auto-deploy |
| CB27 | URL | `flove.org/api/` — same domain, no subdomain. GitHub Pages proxies `/api/*` to Railway. |
| CB28 | DB choice | Turso — SQLite-compatible HTTP API, designed for serverless. Same API as local SQLite (libSQL client). |
| CB29 | Discovery | Hybrid: flove.js pings `/api/ping` on `flove.org` (same origin via GitHub Pages proxy), caches result in localStorage for session |
| CB30 | Indexes | `(app, user)` — covers the only list query pattern |
| CB31 | Schema versioning | Yes — `PRAGMA user_version` in SQLite, auto-migrate if schema changes |
| CB31a | Schema migration | SQL migration files in `migrations/`. Simple, explicit, no framework. |
| CB32 | Conflict resolution | CRDT-style merge for trust data (vector clocks, client-side). Last-write-wins for non-trust data (profile, app data). |
| CB33 | Offline queue | IndexedDB log of pending operations (ordered by timestamp). Replays on next connectivity check. `flove:pending-sync` flag shows count of pending items. |
| CB34 | App registration | Registry file `addons/backend/apps.json` — simple list `["blogy", "goddy", ...]`, server validates against it |
| CB34a | apps.json structure | Flat list with category — `{"apps": [{"name": "goddy", "category": "metas"}, ...]}`. Minimal metadata, category for menu grouping. |
| CB35 | Testing | Unit tests — pytest on FastAPI endpoints with in-memory SQLite |
| CB36 | Backport | Selective cherry-pick — backport bug fixes from `central/` to `main` manually |
| CB37 | Rate limiting | None for proof-of-concept |
| CB37a | Rate limiting post-PoC | Per-IP, 100 req/min. Add after Railway deploy is stable. |
| CB38 | DB path | Turso handles it — no local file path on server |
| CB39 | DB auto-init | Auto — `CREATE TABLE IF NOT EXISTS` on FastAPI startup event |
| CB40 | API prefix | No version prefix — `/api/{app}/save` |
| CB41 | Trust sync endpoint | `POST /api/trust/sync` — separate from app data sync. Immediate processing, CRDT merge, delta-only payload. |
| CB42 | Trust sync payload | `{user, vouches: [{from, to, timestamp, trustLevel, signature, vectorClock}], lastSync}` — delta only (changed vouches since lastSync) |
| CB43 | Trust sync merge | Client-side CRDT: vector clocks determine causality. Server stores merged result. Conflicts surfaced to browsy for display. |
| CB44 | Per-app schema validation | Validate `data` against `addons/backend/collect-schemas.json` on POST/PUT. Reject with `{ok: false, error: "schema_violation", detail: "..."}` if invalid. |
| CB45 | Schema validation level | Required fields + types only (not full JSON Schema). Per-app `required` array + `fields` map with type hints. |
| CB46 | Versioned ping | `GET /api/ping` returns `{ok: true, version: "1.0.0", features: ["trust-sync", "schema-validation"]}`. Browsy caches for session. |
| CB47 | Ping feature flags | `features` array lets browsy detect server capabilities (e.g., trust-sync endpoint exists, schema validation active). |
| CB48 | Central directory split | `addons/backend/` (Railway deploys), `central/apps/` (GitHub Pages deploys), `addons/` (read-only, both pipelines). |
| CB49 | Schema validation error behavior | Reject + log. Malformed data is NOT stored. Server returns specific error with field name. |
| CB50 | Rate limiting during PoC | None for initial deploy. CB37a (per-IP, 100 req/min) added once Railway deploy is stable. |

### Strategic architecture (D01-D23)

| ID | Topic | Decision |
|----|-------|----------|
| D01 | Anonymous data TTL | No TTL — keep forever. User can claim data years later. |
| D02 | Data portability | Export endpoint — `GET /api/{app}/export?user=ID` returns all user data as downloadable JSON. |
| D03 | Branch lifecycle | Permanent divergence — `central/` never merges back to `main`. Bug fixes cherry-picked both ways. |
| D04 | Error codes | Simple string — `{ok: false, error: "not_found"}`. Client matches against known list. |
| D05 | Data size limits | None — any app, any user, any data size. |
| D06 | Input validation | Structural — validate `data` is valid JSON, `user` is non-empty string, `timestamp` is ISO format. Per-app schema validation pending. |
| D07 | central/apps/ relationship | Central apps are their own apps, not copies of main. Share names and little more else — two different things. |
| D08 | Build order | Railway backend first (deploy FastAPI + libSQL, verify with curl). Test app pending — skip to real apps. |
| D09 | WASM pre-cache | Pre-cache in sw.js — add `@libsql/client` and WASM binary to sw.js cache list. |
| D10 | App serving URL | Same origin — Railway backend serves API at `flove.org/api/*` via GitHub Pages proxy. Central apps in `central/apps/` on the `central/` branch are deployed separately. |
| D11 | Email verification | Confirmation email — send verification link via SMTP Railway. |
| D12 | Monitoring | None for proof-of-concept — rely on Railway logs, check manually. |
| D13 | Email sending | SMTP via Railway — configure SMTP credentials in `.env`, FastAPI sends verification emails directly. |
| D14 | App navigation | Launcher + index — `central/index.html` as launcher, `central/apps/` with standalone files, full-page navigation. Like Solo. |
| D15 | Cross-app isolation | None — any app can read any other app's data. Trust-based. |
| D16 | Nav architecture | Bottom fixed bar, logo on left → click opens homogenized menu with chapters → expand to lists. All apps under chapters within the logo menu. Same pattern across all Central apps. Navigation injected by flove.js. |
| D16a | Nav visual spec | Compact 48px bar + full-screen menu overlay. Logo on left, tabs below. |
| D16b | Current app detection | URL parsing (`/apps/goddy.html` → "goddy"). Simple, no extra attributes. |
| D17 | Dev workflow | Railway staging — `staging-railway-flove.org` (via Railway domain + GitHub Pages proxy) for testing changes. No local dev. |
| D18 | Persistence recovery | Recovery modal — "Reset DB?" prompt with export option before clearing OPFS. |
| D19 | Railway structure | Monorepo — one Railway project with two services: `fastapi` (Python) and `libsql` (Docker). |
| D20 | Apps folder structure | Flat — `central/apps/blogy.html`, same pattern as Solo. Central URLs become primary; Solo URLs maintained as fallback. |
| D21 | Ready signal | Backend API stable — deploy backend first when endpoints work and tests pass. Apps are separate work. |
| D22 | HTTP status codes | Always 200 with error body `{ok, error, detail}`. Client checks `ok` field. Avoids proxy/CORS issues with non-200. |
| D23 | Error detail field | Add `detail: "human-readable message"` to error responses. `{ok: false, error: "code", detail: "Expected object at line 3"}`. |

### Central app development (E01-E25)

| ID | Topic | Decision |
|----|-------|----------|
| E01 | apps.json format | Flat list — `["blogy", "goddy", ...]`. |
| E02 | collect-schemas.json format | Inline — schema inline in one file per app. |
| E03 | Export format | NDJSON — one JSON object per line, downloadable as `.ndjson`. |
| E04 | First 5 Central apps | appy-mini apps: blogy, souls, inventary, myfamily, keys. |
| E04a | First 6 apps | Goddy, Souls, Pracsys, Myfamily, Inventary, Realy, Keys (all 7 from appy-mini.html minus blogy). |
| E04b | blogy Central | Deferred — adapted later after first 6 prove the pattern. |
| E05 | Central index.html | Minimal list — simple row of links. Matches Solo's index. |
| E06 | Error codes | Expanded set: `not_found`, `invalid_json`, `missing_user`, `bad_timestamp`, `app_not_registered`, `method_not_allowed`, `server_error`, `db_error`. |
| E07 | Email verification expiry | 24 hours. |
| E08 | flove.js Central module | Same file, organized by commented sections (`// CENTRAL DETECTION`, `// DB`, `// SYNC`). |
| E09 | Domain | Same domain — `flove.org/api/*` routed to Railway. No subdomain. |
| E10 | Routing mechanism | GitHub Pages proxy — redirect `/api/*` to Railway. |
| E11 | SMTP config | `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM`. |
| E12 | Railway project name | `flove-central`. |
| E13 | Email template | Plain text — "Click here to verify: {{link}}". |
| E14 | Git strategy | Initial commit (skeleton) + feature branches off `central/`. |
| E15 | libSQL Docker image | Official — `ghcr.io/tursodatabase/libsql-server:latest`. |
| E16 | railway.toml | Minimal — Railway auto-detects services. |
| E17 | libSQL volume | Fixed — `/data/flove.db`. |
| E18 | App launch order | blogy first → add goddy second. Prove pattern with 2 categories. |
| E19 | blogy filename | `blogy.html` — same as Solo. The `central/` branch distinguishes it. |
| E20 | First sync scope | Current session only. No historical data. |
| E21 | goddy focus | Publish — goddy items published to a public profile page. First step toward social publishing on Central. |
| E22 | Solo vs Central visual diff | Central apps are more similar navigation, less code overall, more shared libs. Sync + status bar. No per-app redesigns. |
| E23 | Central nav | Bottom fixed bar. Logo on left → onclick opens homogenized menu. Chapters expand to further lists. All apps under chapters within the logo menu. Same across all Central apps. Injected by flove.js. |
| E24 | flove.js shared behaviors | Sync + bottom bar injection + shared layout CSS + JS components (rating widget, card view, modal, expandable menus). Maximum code sharing. |
| E25 | Menu tree depth | Two levels — Category Chapter → App. Auto-mirrors the `apps/` directory structure from the `main` branch. |

### Shared code abstraction (CA01-CA44)

| ID | Topic | Decision |
|----|-------|----------|
| CA43a | Nav injection | Fixed bottom tabs + logo menu. Logo on left, tabs below. Logo click opens big menu overlay. |
| CA44a | Rating widget | 5-star click. Classic rating. Apps can override with custom ratings. |

### Nety-Central bridge (G01-G55)

| ID | Topic | Decision |
|----|-------|----------|
| G54 | Nety→Central data flow | Nety pushes profile + public items. Private items stay in Nety only. Central stores and serves the public bundle. |
| G55 | Profile sync endpoint | `POST /api/nety/sync`. Nety POSTs `{profile, items[]}`. Central replaces stored data. Simple, atomic. |

### Central-Browsy integration (CB_S01-CB_S10)

| ID | Topic | Decision |
|----|-------|----------|
| CB_S01 | Large payloads | 1MB limit for app data. Trust sync is separate (delta-only, stays under limit). |
| CB_S02 | Railway downtime | Show error message. |
| CB_S03 | pending-sync flag | IndexedDB log of pending operations (ordered by timestamp). Boolean flag + count. |
| CB_S04 | collect-schemas.json | JSON Schema-lite format: `required` array + `fields` map with type hints. Versioned with `schema_version` field. |
| CB_S05 | Nety bridge auth | OAuth token. |
| CB_S06 | Staging workflow | Branch-based deployment (`staging` branch). |
| CB_S07 | libSQL → Turso testing | Defer until Turso Database is stable. |
| CB_S08 | First 6 apps porting | Rewrite from scratch (to be done). |
| CB_S09 | Bottom nav with many apps | Collapsible chapters. |
| CB_S10 | Rating widget + puzzy | Defer — design puzzy more appropriately first. |

## Architecture

### Tech stack

- **Framework:** Python/FastAPI with `libsql-client` or `turso-client` (Turso HTTP API)
- **Database:** Turso — SQLite-compatible, serverless. libSQL fork initially, Turso Database later.
- **Table:** `app_data(app TEXT, user TEXT, timestamp TEXT, data_json TEXT)` — indexed by `(app, user)`
- **User table:** `user_config(user TEXT, email TEXT, created_at TEXT)` — separate from app data
- **Documents:** `data_json` stores the full `window.flove.collect()` JSON — no schema, stored as-is

### API endpoints

```
POST   /api/{app}/save           → {ok: true, id: "..."}
PUT    /api/{app}/{id}           → {ok: true}
DELETE /api/{app}/{id}           → {ok: true}
GET    /api/{app}/list           → {items: [...], next_cursor: "..." | null}
       ?user=NAME                filter by user
       &cursor=TOKEN             cursor-based pagination (page size 20)
POST   /api/{app}/sync-existing  → {ok: true, count: N}
POST   /api/trust/sync           → {ok: true, merged: N, conflicts: [...]}
GET    /api/ping                 → {ok: true, version: "1.0.0", features: [...]}
```

### Error responses

All endpoints return HTTP 200. Client checks `ok` field:

- Success: `{ok: true, id: "...", ...}`
- Error: `{ok: false, error: "code_string", detail: "human-readable message"}`

Error codes: `not_found`, `invalid_json`, `missing_user`, `bad_timestamp`, `app_not_registered`, `method_not_allowed`, `server_error`, `db_error`.

### Data flow (web)

```
User opens blogy on flove.org
  → flove.js loads (via enrichment loader)
  → flove.js pings /api/ping (same origin, GitHub Pages proxies to Railway)
  → caches "central=available" in localStorage (session)
  → if first detection: auto-modal shows "Central found" with "Got it, don't show again"
  → flove.js injects bottom nav bar (48px, logo left → menu → chapters → app lists)
  → auto-sync triggers silently:
      → collects data via default collect() {timestamp, selections, ratings}
      → sends POST /api/blogy/save with device UUID as user
      → on success: done (no feedback)
      → on failure: silent retry on next load
  → on first manual Sync click:
      → modal asks for email (validates format)
      → confirmation email sent via SMTP (plain text, 24h expiry)
      → subsequent syncs use email as identity
  → on error after email set: button shows specific server message + "Retry"
  → on success with email: button resets to "Sync"
```

### Server structure (central/ branch — directory split)

```
central/
  backend/             ← Railway watches this, deploys FastAPI
    main.py            — FastAPI app, Turso init, all routes (auto-creates tables)
    apps.json          — registry: [{"name": "goddy", "category": "metas"}, ...]
    collect-schemas.json — per-app schema (required fields + types)
    requirements.txt   — fastapi, uvicorn, libsql-client
    .env               — CORS_ORIGINS=https://flove.org,https://staging-railway-flove.org, SMTP_*, TURSO_*
    migrations/        — SQL migration files
    trust.py           — trust sync endpoint logic (CRDT merge, vector clocks)
  apps/                ← GitHub Pages watches this, serves flove.org
    index.html         — Central launcher (minimal link list)
    goddy.html         — Central app, flove.js-powered (bottom nav, sync, shared CSS)
    souls.html
    pracsys.html
    myfamily.html
    inventary.html
    realy.html
    keys.html
  shared/              ← Read-only for both pipelines
    libs/              — flove.js, flove.css, shared JS components
```

Central apps are thinner than Solo apps: no topbar, no individual nav — flove.js injects the shared bottom bar and menu. Each app provides only its core content + interaction JS. Shared CSS (flove.css) provides layout, cards, forms, 5-star rating widget, expandable menu components.

### Identity model (progressive)

**Phase 1 (anonymous):** Device-generated UUID stored in SQLite (`user_config` table). Auto-sync uses this UUID. No email needed to use Central.

**Phase 2 (claim):** User clicks "Claim your data" in the Central settings modal. Enters email (validated for format). Confirmation email sent via SMTP (plain text, 24h expiry). Past data merges to the email identity. Future syncs use email.

**Phase 3 (future):** More identity methods — Telegram, mobile, biometrics. Deferred.

Multi-user auth deferred to CentralRich.

### Browser-side persistence (SoloRich + Central)

**Primary:** libSQL via `@libsql/client` in the browser, wrapping sql.js WASM + OPFS. Single shared `flove.db` with `app` column. Init is lazy — first call to `flove.db.query()` triggers WASM load.

**Fallback:** localStorage key `flove:db` stores everything as one JSON blob. Used when WASM/OPFS isn't available (old browser, WASM fails to load). Silent fallback — no user-facing message.

**Central detection:** flove.js pings `/api/ping` on `flove.org` (same origin, GitHub Pages proxies to Railway). Caches result in localStorage for the session. On success: enables sync button + auto-sync + bottom nav. On failure: no nav, no sync, app works as SoloRich.

### Conflict resolution

**Non-trust data (profile, app data):** Last-write-wins by client timestamp. The server trusts the latest `timestamp` field in the document. For the same document edited on two devices, the one with the later timestamp wins.

**Trust data:** CRDT-style merge with vector clocks. Client (browsy) computes vector clocks locally. Server stores merged result. Conflicts are surfaced to browsy for display (not silently resolved). Delta-only sync: browsy sends only changed vouches since last sync.

### Trust sync

Browsy pushes trust deltas to `POST /api/trust/sync`. Payload: `{user, vouches: [{from, to, timestamp, trustLevel, signature, vectorClock}], lastSync}`. Server merges using vector clock causality. Returns `{ok: true, merged: N, conflicts: [...]}` where conflicts are vouches that couldn't be auto-merged (server sends both versions to browsy for user resolution).

### Central modal

Auto-shows once on first Central detection (for advanced/super tiers). Shows:
- Brief explanation of Central sync
- "Got it, don't show again" checkbox
- Email input (only on first sync click, not in the auto-modal)

After dismissal, the "Sync" button stays accessible via the bottom nav menu.

### Central navigation (bottom bar)

flove.js injects a **bottom fixed bar** (48px) across all Central apps:

- **Left:** flove logo (clickable)
- **Click → full-screen menu** overlay with chapters
- **Chapters:** mirror the `apps/` directory structure from `main` branch — categories as chapters
- **Chapters expand** to show app lists (two levels: Category → App)
- **Current app detected** via URL parsing (`/apps/goddy.html` → "goddy")
- All Central apps, categories, and future features accessible from this menu

No individual topbar or per-app nav in Central apps. flove.js handles the shared navigation layer.

### Nety→Central bridge

- Nety pushes public profile + public items to Central via `POST /api/nety/sync`
- Data shape: `{profile: {username, displayName, avatar}, items: [{app, data, timestamp}]}`
- Private items stay in Nety only — never synced
- Central profile page at `flove.org/nety/{username}` serves the public bundle
- Profile mirror is one-way: Nety pushes, Central stores

### Future: CentralRich (PostgreSQL + JSONB)

When Central grows beyond Turso:
- FastAPI stays, Turso replaced with `asyncpg` for PostgreSQL
- JSONB columns: `CREATE TABLE app_data (id UUID, app TEXT, user TEXT, ts TIMESTAMPTZ, data JSONB)`
- JSONB `@>` operator queries the same `collect()` JSON — no client-side change
- Migration from Turso: export to Parquet → pgloader bulk-insert
- PostgreSQL's JOINs enable trust graph queries and cross-app aggregation

### Conflicts

- CB09 (email-only) × future multi-user: email is not secure auth. Migration: add password or OAuth when CentralRich arrives.
- CB11 (manual sync) × offline-first: SoloRich apps with SQLite accumulate changes locally. An IndexedDB log tracks pending operations; the Sync button shows a count.
- Turso (libSQL) × Turso Database (beta): start with libSQL (production fork), migrate to Turso Database (Rust rewrite, concurrent writes) when stable.
- CB32 (CRDT for trust) × CB_S01 (1MB limit): trust sync is delta-only to stay under limit. Full graph rebuild happens client-side in browsy.

<a id="browsy-readme"></a>
## Browsy README — architecture, decisions, file map

> Source: `development/wiki/archive/old/browsy/README.md` (archived 2026-11-21).

> **Status 2026-11-17 — superseded in part.** Current spec:
> [`spec.md`](../../archive/old/browsy/spec.md).
> Identity/hash and the pull model live in **§3.8**; open standards are in
> [`browsy-questions.md`](../../archive/old/browsy/browsy-questions.md) §K.
> Pre-build contracts: [`pre-build/README.md`](../../archive/old/browsy/pre-build/README.md).
> Browsy is the host and pulls public pages on demand; pages do not query
> identity or vault. The older “backend only / Central is the hub” text below is
> historical. Keep MV3, storage split, crypto primitives and F2F.

Chrome extension that hosts Authy and Wizy, pulls public pages on demand and renders local suggestions. Central is optional.

### Architecture

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

**Core rule:** On-demand only. No background calculations. No auto-sync. User clicks → Browsy pulls, computes locally and renders; Central is optional.

**What central adds:** Trust graph across all users, multi-device sync, F2F record storage, permissions enforcement, URL obfuscation, group management, encrypted content storage, key rotation. browsy can't do any of this alone.

### Decisions

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

### File structure

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

### What's implemented

- [x] Context menus (Save/Share)
- [x] Badge detection (★ on flove pages)
- [x] Popup UI (app suggestions)
- [x] Content script bridge skeleton
- [x] `chrome.storage.onChanged` listener

### What's stubbed

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

### Data structures

#### Vouch
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

#### Profile
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

#### Trust
```js
{
  score: 0.78,
  facets: { personal: 0.85, local: 0.70, social: 0.80, global: 0.65 },
  mynet: { categories: ["garden","trade","community"], circles: ["friends","colleagues"] },
  vouchCount: 47,
  lastCalculated: "2026-07-27T10:00:00Z"
}
```

### Setup

1. Go to `chrome://extensions`
2. Enable Developer mode
3. Click Load unpacked
4. Select `browsy/` folder

### Testing

See [TESTING.md](../../archive/old/browsy/TESTING.md) for full test plan and risk analysis.

<a id="browsy-testing"></a>
## Browsy TESTING — risk matrix and test plan

> Source: `development/wiki/archive/old/browsy/TESTING.md` (archived 2026-11-21).

> **Status 2026-11-17 — superseded in part.** Current spec:
> [`spec.md`](../../archive/old/browsy/spec.md).
> Keep the risk matrix; extend it with the acceptance tests in §7 of the new plan.

### Decisions made

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

### Architecture recap

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

### 1 · Vouch data structure

#### What is a vouch?

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

#### UI representation

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

#### Storage estimate

| Vouches | Size (approx) | % of 5MB |
|---------|---------------|----------|
| 20 | ~8 KB | 0.2% |
| 50 | ~20 KB | 0.4% |
| 100 | ~40 KB | 0.8% |
| 200 | ~80 KB | 1.6% |

**Verdict:** 20-100 vouches = well under 5MB. Safe.

---

### 2 · Crypto: tweetnacl vs Web Crypto

#### Comparison

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

#### Decision: Web Crypto primary + tweetnacl fallback

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

#### Pros/cons summary

**Web Crypto pros:** native, async, no bundle, future-proof
**Web Crypto cons:** Chrome 113+ only, no Firefox/Safari yet

**tweetnacl pros:** all browsers, proven, tiny
**tweetnacl cons:** sync (blocks thread), unmaintained, adds 20KB

---

### 3 · Browsy performance risks

#### Service worker lifecycle
| Risk | Severity | Mitigation |
|------|----------|------------|
| Killed after 30s idle | HIGH | On-demand only, no background work |
| Killed after 5min max | HIGH | Crypto ops < 500ms, trust chains < 2s |
| No persistent state | HIGH | All state in `chrome.storage.local` |
| No `window`/`document` | HIGH | Web Worker for heavy ops |
| Re-created on event | MED | Re-register bridge on restart |

#### Storage limits
| Limit | Value | Our usage (100 vouches) |
|-------|-------|------------------------|
| `chrome.storage.local` total | 5 MB | ~40KB vouches + ~1KB keys + ~1KB trust |
| `chrome.storage.local` per item | 1 MB | Vouch array ~40KB (safe) |
| `chrome.storage.sync` total | 100 KB | Settings only (~1KB) |
| `chrome.storage.sync` per item | 8 KB | Each setting < 100 bytes |

**Verdict:** Well within limits at 20-100 vouches. Monitor at 500+.

#### Content script timing
| Risk | Severity | Mitigation |
|------|----------|------------|
| Injected after DOM ready | MED | Central waits for bridge, fallback to localStorage |
| SPA navigation | MED | Re-inject on `popstate`/`pushState` |
| Message timeout | LOW | 100ms timeout, fallback to cached data |

#### Crypto operations (with Web Worker)
| Risk | Severity | Mitigation |
|------|----------|------------|
| Key gen in worker | LOW | Off main thread, < 500ms |
| Trust chain in worker | LOW | Off main thread, < 2s for 100 vouches |
| Worker killed by browser | MED | Restart on demand, cache results |

#### Cross-origin (patched)
| Risk | Severity | Mitigation |
|------|----------|------------|
| Content script can't access page JS | MED | Bridge uses `chrome.runtime.sendMessage` |
| flove.org vs localhost | LOW | Badge: check `flove.org` OR `localhost:*` OR `127.0.0.1:*` |
| CSP blocks inline script | LOW | Bridge is injected as content script, not inline |

---

### 4 · What's implemented vs stubbed

#### Implemented (real code)
- [x] Context menus (background.js)
- [x] Badge detection (background.js)
- [x] Popup UI (popup.html/popup.js)
- [x] Content script bridge skeleton (content.js)
- [x] `chrome.storage.onChanged` listener

#### Stubbed (returns null/empty)
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

### 5 · Settings sync (browsy ← central, unidirectional)

#### Flow
```
User changes setting in central
  → floveSettings.set(key, val)
  → writes to localStorage (flove:key)
  → if browsy installed:
      → chrome.runtime.sendMessage({ type: 'setting-changed', key, val })
      → background.js writes to chrome.storage.local (flove-key)
      → background.js writes to chrome.storage.sync (flove-key) [if < 8KB]
```

#### Conflict resolution: browsy wins
```
If browsy has value → use browsy
If browsy has no value → use localStorage
If neither → use default
```

#### Storage keys
| Setting | localStorage | chrome.storage.local | chrome.storage.sync |
|---------|-------------|---------------------|-------------------|
| Theme | `flove:theme` | `flove-theme` | `flove-theme` |
| Language | `flove:language` | `flove-language` | `flove-language` |
| Sound | `flove:sound` | `flove-sound` | `flove-sound` |
| Sound level | `flove:soundLevel` | `flove-soundLevel` | `flove-soundLevel` |
| Notifications | `flove:notifications` | `flove-notifications` | `flove-notifications` |
| Wizy | `flove:wizy` | `flove-wizy` | `flove-wizy` |

---

### 6 · Profile data structure

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

### 7 · browsy-trust data structure

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

### 8 · Suggestions (prioritized)

#### Priority 1: Make bridge work
1. Implement real `getKeypair()` → Web Crypto in background SW
2. Implement real `getProfile()` → return profile object
3. Implement real `getScore()` → return trust score
4. Implement real `getFacets()` → return 4 facet scores
5. Test central reads bridge on load

#### Priority 2: Settings sync
6. Add `chrome.storage.local` mirror to `flove-settings.js`
7. `floveSettings.set()` → localStorage + chrome.storage when browsy installed
8. Central caches bridge responses (browsy lighter)

#### Priority 3: On-demand crypto
9. Key generation → background SW via message
10. Trust chain → Web Worker, < 2s for 100 vouches
11. Vouch signing → background SW
12. Cache results in central (avoids re-computation)

#### Priority 4: Reliability
13. 100ms timeout on bridge calls → fallback to cache
14. Retry logic (1 retry, then fallback)
15. Service worker restart → re-bridge automatically
16. `chrome.storage.onChanged` listener in central

#### Priority 5: Testing
17. `browsy/test.html` with sample content
18. Mock bridge for automated tests
19. Performance benchmarks (key gen, trust chain)
20. Test both installed + not-installed

---

### 9 · Test matrix

#### A · Browsy standalone
| Test | Expected | Pass |
|------|----------|------|
| Extension loads, no errors | Clean console | |
| Context menus on right-click | "Save to flove" + "Share to Nety" | |
| Badge ★ on flove.org | Purple star | |
| Badge empty on non-flove | No badge | |
| Popup shows app info | Correct app name | |
| chrome.storage writable | Data persists | |

#### B · Bridge API
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

#### C · Settings sync
| Test | Expected | Pass |
|------|----------|------|
| Central: toggle → localStorage | `flove:theme` set | |
| Central: toggle → chrome.storage | `flove-theme` set | |
| Browsy: change → central updates | Central reads chrome.storage | |
| No browsy: localStorage only | Current behavior | |
| Browsy wins on conflict | chrome.storage value used | |

#### D · Performance
| Test | Threshold | Pass |
|------|-----------|------|
| Bridge response | < 100ms | |
| Key generation (Web Worker) | < 500ms | |
| Trust chain (20 vouches) | < 200ms | |
| Trust chain (100 vouches) | < 2s | |
| Storage (100 vouches) | < 50KB | |
| Storage (total) | < 500KB | |

#### E · Edge cases
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

### 10 · File structure

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

<a id="browsy-port-nety"></a>
## Browsy port-nety — crypto/storage seams

> Source: `development/wiki/archive/old/browsy/port-nety.md` (archived 2026-11-21).

> **Status 2026-11-17 — superseded in part.** Current spec:
> [`spec.md`](../../archive/old/browsy/spec.md).
> Keep crypto/store port seams and namespacing; the Central permissions layer is replaced by signed grants.

> What to change in browsy NOW so nety can extend it cleanly later.

### The relationship

```
browsy (base)              nety (extension)
─────────────              ───────────────
identity keys        ───►  P2P identity
trust (local)        ───►  trust (network)
storage (chrome)     ───►  storage (P2P)
crypto (local)       ───►  crypto (E2E)
settings (local)     ───►  settings (synced)
```

nety extends browsy. Browsy must be pluggable.

---

### 1 · Extract crypto into lib/crypto.js

**Why:** nety needs the same Ed25519 + ChaCha20 but with P2P transport. If crypto is a module, nety imports it directly.

**Now:**
```js
// background.js — crypto mixed into message handler
chrome.storage.local.get('browsy-keys', function(d) { ... });
```

**After:**
```js
// lib/crypto.js — standalone module
window.floveCrypto = {
  generateKeypair: function() { ... },      // Web Crypto / tweetnacl
  sign: function(key, data) { ... },
  verify: function(pubkey, data, sig) { ... },
  deriveCompositeKey: function(factors) { ... },
  mnemonicGenerate: function(key) { ... },
  mnemonicRestore: function(words) { ... }
};

// background.js — imports crypto module
importScripts('lib/crypto.js');
// uses window.floveCrypto.*
```

**Files:** Create `lib/crypto.js`, update `background.js`

---

### 2 · Abstract storage behind an interface

**Why:** browsy uses `chrome.storage.local`. nety might use IndexedDB, IndexedDB + P2P, or a different backend. If storage is abstracted, nety swaps the implementation.

**Now:**
```js
chrome.storage.local.get('browsy-keys', function(d) { ... });
chrome.storage.local.set({ 'browsy-vouches': vouches });
```

**After:**
```js
// lib/store.js — pluggable storage
window.floveStore = {
  get: function(key, cb) {
    chrome.storage.local.get(key, function(d) { cb(d[key] || null); });
  },
  set: function(key, val, cb) {
    var obj = {}; obj[key] = val;
    chrome.storage.local.set(obj, cb || function() {});
  },
  getAll: function(keys, cb) {
    chrome.storage.local.get(keys, cb);
  },
  remove: function(key, cb) {
    chrome.storage.local.remove(key, cb);
  },
  // nety overrides this with P2P storage
  _impl: 'chrome'
};

// background.js — uses store module
importScripts('lib/store.js');
window.floveStore.get('browsy-keys', function(key) { ... });
```

**nety port:** Replace `lib/store.js` with P2P-backed implementation. Same API.

**Files:** Create `lib/store.js`, update `background.js`

---

### 3 · Match vouch format to nety's trust protocol

**Why:** nety's trust graph uses `{ from, to, timestamp, trustLevel, signature }`. If browsy's vouch format matches, nety imports vouches directly.

**Now (browsy):**
```js
{ id, from, to, score, facets, message, created, revoked }
```

**nety format:**
```js
{ from, to, timestamp, trustLevel, signature, vectorClock }
```

**Compatible format (browsy uses this):**
```js
{
  id: "v_abc123",
  from: "ed25519_pubkey_hex",
  to: "ed25519_pubkey_hex",
  // nety-compatible fields:
  timestamp: "2026-07-27T10:00:00Z",     // was 'created'
  trustLevel: "close",                     // nety tier name
  signature: "ed25519_signature_hex",      // nety needs this
  vectorClock: { "user-a": 5 },            // nety CRDT
  // browsy-only fields (nety ignores):
  score: 0.85,
  facets: { personal: 0.9, local: 0.7, social: 0.8, global: 0.6 },
  message: "Known for 3 years",
  revoked: null
}
```

**Why this works:** nety reads `from, to, timestamp, trustLevel, signature, vectorClock` and ignores the rest. Browsy uses all fields. Zero conflict.

**Files:** Update `content.js` data structures, `background.js` storage format

---

### 4 · Message type registry (extensible)

**Why:** nety adds P2P messages (send-vouch, request-trust, sync-graph). If browsy uses a registry, nety registers new types without forking.

**Now:**
```js
// background.js — hardcoded if/else chain
if (msg.type === 'get-keypair') { ... }
if (msg.type === 'get-profile') { ... }
```

**After:**
```js
// lib/handler.js — message registry
window.floveHandlers = {};

window.floveHandlers.register = function(type, fn) {
  window.floveHandlers[type] = fn;
};

// background.js — registers browsy handlers
importScripts('lib/handler.js', 'lib/store.js', 'lib/crypto.js');

window.floveHandlers.register('get-keypair', function(msg, sender, cb) {
  window.floveStore.get('browsy-keys', function(key) {
    cb({ ok: true, data: key });
  });
});

// nety registers additional handlers:
window.floveHandlers.register('send-vouch', function(msg, sender, cb) {
  // P2P vouch sending
});

window.floveHandlers.register('sync-graph', function(msg, sender, cb) {
  // P2P trust graph sync
});
```

**Files:** Create `lib/handler.js`, update `background.js`

---

### 5 · Auth pipeline (layered, extensible)

**Why:** nety adds P2P auth (SSB, biometry). If browsy's auth is a pipeline, nety adds layers without touching core.

**Now:**
```js
// stubbed — no real auth
```

**After:**
```js
// lib/auth.js — auth pipeline
window.floveAuth = {
  layers: [
    { name: 'device', weight: 1, verify: function() { ... } },
    { name: 'telegram', weight: 2, verify: function() { ... } },
    { name: 'email', weight: 2, verify: function() { ... } },
    { name: 'trust', weight: 3, verify: function() { ... } }
  ],

  // nety adds layers:
  // { name: 'ssb', weight: 2, verify: function() { ... } }
  // { name: 'biometry', weight: 1, verify: function() { ... } }

  getCompositeKey: function() {
    // derive signing key from all active layers
  },

  getFactorCount: function() {
    // returns count for display ("3-factor signed")
  },

  addLayer: function(layer) {
    window.floveAuth.layers.push(layer);
  }
};
```

**Files:** Create `lib/auth.js`, update `background.js`

---

### 6 · Pluggable trust computation

**Why:** browsy computes trust locally (on-demand). nety computes trust over P2P network. If computation is pluggable, nety swaps the engine.

**Now:**
```js
// stubbed — trust returns 0
```

**After:**
```js
// lib/trust.js — pluggable trust engine
window.floveTrust = {
  computeScore: function(vouches) {
    // browsy: local only, simple average
    // nety: replaces with P2P graph traversal
    return localCompute(vouches);
  },

  computeFacets: function(vouches) {
    return { personal: 0, local: 0, social: 0, global: 0 };
  },

  computeChain: function(vouches, depth) {
    // browsy: depth 3, local
    // nety: depth 3, P2P
    return localChain(vouches, depth);
  },

  // nety overrides:
  // window.floveTrust.computeScore = p2pCompute;
};
```

**Files:** Create `lib/trust.js`, update `background.js`

---

### 7 · Bridge API versioning

**Why:** nety extends the bridge API (adds `nety.p2p.*`, `nety.sync.*`). If browsy's bridge has a version + extension point, nety adds without breaking.

**Now:**
```js
window.flove.browsy = { ... }; // fixed
```

**After:**
```js
window.flove = window.flove || {};
window.flove.browsy = { ... }; // browsy core

// extension point:
window.flove.extend = function(namespace, api) {
  window.flove[namespace] = api;
};

// nety uses:
window.flove.extend('nety', {
  p2p: { send: function() { ... }, receive: function() { ... } },
  sync: { push: function() { ... }, pull: function() { ... } }
});
```

**Files:** Update `content.js`

---

### 8 · Storage key namespacing

**Why:** browsy uses `browsy-keys`, `browsy-trust`, etc. nety uses `nety-keys`, `nety-trust`. If keys are namespaced, both coexist.

**Now:**
```js
chrome.storage.local.get('browsy-keys', ...);
chrome.storage.local.get('browsy-trust', ...);
```

**After:**
```js
// lib/store.js — namespaced
var NAMESPACE = 'browsy'; // nety sets 'nety'

window.floveStore = {
  get: function(key, cb) {
    chrome.storage.local.get(NAMESPACE + '-' + key, function(d) {
      cb(d[NAMESPACE + '-' + key] || null);
    });
  },
  set: function(key, val, cb) {
    var obj = {}; obj[NAMESPACE + '-' + key] = val;
    chrome.storage.local.set(obj, cb || function() {});
  }
};

// background.js — uses short keys
window.floveStore.get('keys', function(key) { ... });
window.floveStore.get('trust', function(trust) { ... });
```

**nety port:** Set `NAMESPACE = 'nety'`. Same API, different keys.

**Files:** Update `lib/store.js`

---

### Summary: what to create now

| File | Purpose | nety reuses |
|------|---------|-------------|
| `lib/crypto.js` | Ed25519, signing, mnemonic | Yes — same crypto |
| `lib/store.js` | Pluggable storage | Yes — swap backend |
| `lib/handler.js` | Message registry | Yes — add P2P handlers |
| `lib/auth.js` | Auth pipeline | Yes — add P2P layers |
| `lib/trust.js` | Trust computation | Yes — swap engine |
| `lib/vouch.js` | Vouch format (nety-compatible) | Yes — same format |

**Estimated effort:** ~2 hours to extract and refactor.
**nety port savings:** ~1-2 days (don't rewrite crypto, storage, auth, trust).

---

### Implementation order

1. `lib/store.js` — extract from background.js (15 min)
2. `lib/crypto.js` — extract stubs + add Web Crypto (30 min)
3. `lib/handler.js` — extract message routing (15 min)
4. `lib/vouch.js` — define nety-compatible format (15 min)
5. `lib/auth.js` — extract auth pipeline (15 min)
6. `lib/trust.js` — extract trust computation (15 min)
7. Update `background.js` — use all modules (15 min)
8. Update `content.js` — add `flove.extend()` (10 min)

---

### 9 · F2F (Face-to-Face) verification

**Why:** Strongest trust signal. "I met this person in real life." Can't be faked remotely. Feeds into the local facet (weight: 1.0).

#### How it works

```
User A                          User B
──────                          ──────
shows QR code ──────────────► scans QR
  (pubkey + nonce)                │
                                  signs nonce with their key
◄────────────────────────── sends signed nonce
verifies signature               │
  │                              │
  └─ both sign "A↔B verified" ──┘
     central stores F2F record
```

#### Data structure
```js
{
  type: "f2f",
  from: "pubkey_a",
  to: "pubkey_b",
  timestamp: "2026-07-27T10:00:00Z",
  nonce: "random_32_bytes",
  sigA: "ed25519_sig_of_nonce",
  sigB: "ed25519_sig_of_nonce",
  location: "optional_gps_or_null",
  trustLevel: "f2f",    // highest weight
  signature: "combined_sig"
}
```

#### Where it lives
- **browsy:** generates QR, signs challenge, stores F2F record locally
- **central:** stores F2F record as special vouch type, includes in trust graph

#### Trust weight
| Trust type | Weight | Why |
|-----------|--------|-----|
| f2f | 1.0 | Met in person, can't fake |
| vouch | 0.7 | Online trust statement |
| self | 0.3 | Self-declared |

**Files:** Create `lib/f2f.js`, update `background.js`, central `POST /api/trust/f2f`

---

### 10 · Permissions layer

**Why:** Not just "public or private" — granular access control. Who can see, comment, edit, admin.

#### Permission levels
| Level | Can do |
|-------|--------|
| `none` | Can't see it exists |
| `view` | Can read |
| `comment` | Can read + comment |
| `edit` | Can modify |
| `admin` | Can change permissions |

#### Where it lives
- **central:** permissions table (authoritative)
- **browsy:** caches permissions locally (fast check)

#### Flow
```
User visits page
  → browsy checks local cache
  → cache miss? asks central: "can I see this?"
  → central checks permissions table
  → returns: yes/no + level
  → browsy caches result (TTL: 5 min)
  → shows or hides content
```

#### Central API
| Endpoint | What it does |
|----------|-------------|
| `GET /api/permissions/:content_id` | Check if user can access content |
| `POST /api/permissions/:content_id` | Set permissions for content |
| `DELETE /api/permissions/:content_id/:user` | Revoke access |

**Files:** Central `permissions.py`, browsy `lib/permissions.js`

---

### 11 · URL obfuscation

**Why:** Hide private content URLs. Prevents snooping, guessing, indexing. Group members see real URLs, strangers see nothing.

#### URL format
```
Public:    https://flove.org/apps/garden/public-post-123
Private:   https://flove.org/p/a1b2c3d4           ← obfuscated
Protected: https://flove.org/p/a1b2c3d4?token=xyz  ← signed, expires
```

#### How it works
```
Central stores:
  content_id: "a1b2c3d4"
  real_path: "/my-secret-project/notes"
  owner: "pubkey_owner"

When user requests /p/a1b2c3d4:
  1. Central checks: is user authorized?
  2. If yes → redirects to real path (or serves content)
  3. If no → shows "access denied" or "request access"
```

#### browsy's role
- Detects `/p/` URLs
- Asks central: "what is this?"
- Central checks permissions
- If authorized: browsy decrypts and renders
- If not: shows "request access" or "join group"

#### Group alternative
Instead of per-user permissions:
```
User shares page with group "project-x"
  → all group members can access /p/a1b2c3d4
  → non-members see "access denied"
  → add/remove people from group → permissions update automatically
```

**Files:** Central `obfuscate.py`, browsy detects `/p/` URLs

---

### 12 · Group-based access

**Why:** Manage 1 group instead of 50 individual grants. Add/remove people → permissions update automatically.

#### Group data structure
```js
{
  id: "grp_abc123",
  name: "project-x",
  owner: "pubkey_owner",
  members: ["alice_key", "bob_key", "carol_key"],
  permissions: { view: true, comment: true, edit: false },
  created: "2026-07-27T10:00:00Z",
  expiry: null  // or "2026-08-27T10:00:00Z"
}
```

#### How it works
```
User creates group:
  name: "project-x"
  members: ["alice", "bob", "carol"]
  permissions: { view: true, comment: true }

User shares page with group:
  central: page_abc123 → group "project-x" → view+comment

All 3 members can view + comment

User removes bob from group:
  bob can no longer see page_abc123
```

#### Relationship to browsy's existing groups
- browsy has: Close, Public, Private, 1 custom
- central extends: groups with members, permissions, expiry
- browsy checks central: "is user in my group?"
- central answers: yes/no + what level

#### Central API
| Endpoint | What it does |
|----------|-------------|
| `POST /api/groups` | Create group |
| `GET /api/groups` | List user's groups |
| `POST /api/groups/:id/members` | Add member |
| `DELETE /api/groups/:id/members/:user` | Remove member |
| `POST /api/groups/:id/permissions` | Set group permissions |

**Files:** Central `groups.py`, browsy `lib/groups.js`

---

### 13 · Auto-decrypt for protected pages

**Why:** Like a password manager but for flove content. No manual password entry. browsy stores keys, central stores encrypted content. Central NEVER sees plaintext.

#### Security model

```
Owner encrypts page:
  content → encrypt with key X → stored on central
  key X → encrypt with owner's pubkey → stored on central

Grant access to alice:
  key X → encrypt with alice's pubkey → stored on central

alice visits:
  central sends: key_X_for_alice (encrypted)
  alice's browsy: decrypts with private key → gets key X
  alice's browsy: decrypts content with key X
  alice sees: plaintext

central's view: encrypted content + encrypted keys
browsy's view: plaintext content + private key
nobody else sees anything
```

**What central knows:** that alice has access (permissions table)
**What central never sees:** the content or the decryption key in plaintext

#### Attack scenarios

| Scenario | Result | Mitigation |
|----------|--------|------------|
| Central hacked | Attacker gets encrypted blobs, useless | Need private keys (in browsy) |
| Device stolen | Attacker gets private key + cache | Device auth layer |
| Member removed | Old key deleted, content re-encrypted | Key rotation |
| Man-in-the-middle | Can't decrypt (TLS + E2E) | Key never travels in plaintext |

#### Key rotation (when member removed)

```
Owner removes bob:
  1. Generate new key Y
  2. Re-encrypt content with key Y
  3. Re-encrypt key Y for remaining members (alice, carol)
  4. Delete key X entirely
  5. bob's cached key X is useless (content re-encrypted with Y)
```

#### How it appears in the feed

The feed mixes public and private posts. Private posts show a small indicator:

```
┌─────────────────────────────────────────┐
│  🌿 María shared a garden post          │
│  "How to grow tomatoes in shade"        │
│  2 hours ago                  public    │
├─────────────────────────────────────────┤
│  🔒 project-x · team only               │
│  "Sprint planning notes"                │
│  1 hour ago                   🔑 auto   │  ← you have access, auto-decrypts
├─────────────────────────────────────────┤
│  🌿 Carlos shared a garden post          │
│  "Best soil for containers"             │
│  30 min ago                  public     │
├─────────────────────────────────────────┤
│  🔒 🔒 encrypted                        │
│  "Q3 budget"                            │
│  5 min ago                   🔒 locked  │  ← no access
└─────────────────────────────────────────┘
```

**Three states:**
| State | Icon | What you see | What happens |
|-------|------|-------------|-------------|
| Public | `public` | Full content | Nothing |
| Private + access | `🔑 auto` | Full content (auto-decrypted) | browsy decrypts silently, <10ms |
| Private + no access | `🔒 locked` | Title only + "request access" | Can't see content |

#### Flow

```
central returns feed items:
  [
    { id: "post_1", public: true, content: "..." },
    { id: "post_2", encrypted: true, group: "project-x", title: "Sprint planning" },
    { id: "post_3", encrypted: true, title: "Q3 budget" }
  ]

browsy checks each:
  if public → show full content
  if encrypted + you have key → auto-decrypt, show full content
  if encrypted + no key → show title + "request access"
```

#### browsy's role
- Stores private key (never leaves device)
- Detects encrypted pages (checks `encrypted: true` flag)
- Requests encrypted key from central
- Decrypts locally (<10ms)
- Caches decrypted key (TTL: 1 hour)

#### central's role
- Stores encrypted content
- Manages per-user encrypted keys
- Checks permissions before releasing keys
- Rotates keys when members are removed

#### Central API
| Endpoint | What it does |
|----------|-------------|
| `POST /api/content/:id/encrypt` | Owner encrypts content |
| `GET /api/content/:id/decrypt-key` | Get encrypted decryption key |
| `POST /api/content/:id/grant/:user` | Grant access (encrypt key for user) |
| `DELETE /api/content/:id/revoke/:user` | Revoke access (delete user's key) |
| `POST /api/content/:id/rotate` | Rotate encryption key |

---

### How all 5 connect

```
F2F verify
  → high trust score
  → join group
  → group grants permissions
  → permissions allow access to obfuscated URL
  → central releases encrypted key
  → browsy auto-decrypts content
```

**Trust chain:**
```
meet in person → verify identity → trust score → group access → see content → auto-decrypt
```

#### Central API summary (all 5 features)

| Endpoint | Feature | What it does |
|----------|---------|-------------|
| `POST /api/trust/f2f` | F2F | Store F2F verification record |
| `GET /api/permissions/:id` | Permissions | Check access level |
| `POST /api/permissions/:id` | Permissions | Set access level |
| `GET /api/p/:id` | Obfuscation | Resolve obfuscated URL |
| `POST /api/groups` | Groups | Create group |
| `POST /api/groups/:id/members` | Groups | Add/remove member |
| `POST /api/content/:id/decrypt-key` | Auto-decrypt | Get encrypted decryption key |
| `POST /api/content/:id/rotate-key` | Auto-decrypt | Rotate encryption key |

#### browsy module summary

| Module | Feature | What it does |
|--------|---------|-------------|
| `lib/f2f.js` | F2F | QR generation, challenge signing |
| `lib/permissions.js` | Permissions | Cache + check access |
| `lib/decrypt.js` | Auto-decrypt | Decrypt content locally |
| `lib/groups.js` | Groups | Cache group membership |

<a id="oasis-bridge"></a>
## Oasis / 0asis bridge

> Source: `development/wiki/archive/old/bridges/oasis.md` (archived 2026-11-21).

The reference map of **Oasis** (the 0asis backend) and how **flove adapts onto
it**. Read this before touching anything that publishes flove content to the
network. It feeds directly into the backend roadmap: this is the deep reference
behind **F1 `routing.json`** and **F2 `OasisPublisher`** (→ `backend.md` §2,
§6, §7; `backend.md` + `plans/index.md`).

---

### 0 · What Oasis is (and which Oasis)

**Oasis = a libre, P2P, encrypted, federated social ecosystem built on Secure
Scuttlebutt (SSB).** You are the centre of your own append-only feed; "pubs"
are always-on relay nodes that gossip content across the mesh. No accounts, no
passwords — identities are randomly-generated keypairs.

There are **two** Oasis codebases — don't confuse them:

| | Origin | What it is |
|---|--------|-----------|
| `fraction/oasis` | Christian Bundy | the **original**, minimal SSB web client |
| **`epsylon/oasis`** | psy / **KrakenLabs · SolarNET.HuB** | the **fork we run** — hugely expanded (45+ modules, ECOin economy, AI "42", Parliament, Courts, LARP) |

**Ours is `epsylon/oasis`.** Canonical homes:
- Code: `github.com/epsylon/oasis` (also `code.03c8.net/epsylon/oasis`)
- Project site: **`0asis.net`** · pub directory: **`oasis-project.pub`**
- Wiki: `wiki.solarnethub.com` · org: `solarnethub.com` / `krakenslab.com`
- License: **AGPL-3.0** · author: psy `<epsylon@riseup.net>`

This is the "API de 0asis disponible" referenced in the flove backend plan.

---

### 1 · Local deployment reality

Lives at **`/home/kdeneon/oasis`** (cloned + extracted; git remote = `epsylon/oasis`,
currently **v0.8.1**).

- **Start:** `cd /home/kdeneon/oasis && sh oasis.sh --port=3001 --no-open`
  - **Port 3000 (the default) is taken by docker-proxy** → always pass `--port=3001`.
  - GUI then on `http://localhost:3001`; SSB protocol on `:8008`.
- **Modes:** `sh oasis.sh` (GUI, default) · `sh oasis.sh server` (headless pub) ·
  `sh oasis.sh help`. PUB admin: `whoami`, `invite [N]`, `name`, `announce`,
  `follow`, `status`, `gossip`.
- **Deps live in `src/server/node_modules`** (≈1130 pkgs). `backend.js` requires
  them via relative paths like `../server/node_modules/<pkg>`. If a module dir
  exists but is **empty** → the install was interrupted; fix with
  `cd src/server && npm install`. (`postinstall` patches `ssb-ref` + `ssb-blobs`.)
- **AI is off** (no `src/AI/*.gguf` model downloaded). `oasis.sh` auto-flips
  `aiMod` on/off in the config depending on whether the model file exists, so
  leaving it absent keeps the AI tabs hidden. Enabling full AI = ~3.9 GB download.
- Node v24 works (installer asks for 22; fine).

---

### 2 · Architecture (the parts that matter for flove)

```
browser (pure HTML+CSS, NO client JS)
   │  GET/POST form submits
   ▼
Koa + @koa/router  ──►  src/backend/backend.js   (the one ~400KB router file)
   │                         │ calls
   │                         ▼
   │                    src/models/<x>_model.js   (read/write SSB messages)
   │                         │ via "cooler"
   ▼                         ▼
src/views/<x>_view.js     src/server/SSB_server.js  (the sbot: SecretStack + ssb-db2 + plugins)
   (hyperaxe → HTML)
```

- **No browser JavaScript.** The whole UI is server-rendered HTML+CSS; every
  interaction is a plain `<form method=GET/POST>`. This is a hard project rule
  ("A really secure frontend"). **→ this is the single most important fact for
  flove adaptation (§4).**
- **Views** are built with **hyperaxe** (JS functions `div()`, `form()`,
  `button()`… that emit HTML strings), wrapped in `template(title, …)` from
  `main_views.js`. No template files.
- **The sbot** (`SSB_server.js`) is a `SecretStack` with ssb-db2 + the classic
  plugin set: `ssb-gossip`, `ssb-ebt`, `ssb-friends`, `ssb-blobs`, `ssb-conn`,
  `ssb-invite`, `ssb-about`, `ssb-backlinks`, `ssb-private`, `ssb-onion` (Tor)…
- **`cooler`** (`src/client/gui.js`) is the lazy connection handle every model
  receives: `const ssb = await cooler.open()` → then `ssb.publish`, `ssb.get`,
  `ssb.createLogStream`.

---

### 3 · The SSB data model + module anatomy

#### Data model (append-only, no edits/deletes)
Every record is an **SSB message** identified by a `content.type` string. SSB is
append-only, so "edit" and "delete" are emulated:
- **Edit** → publish a new message with `replaces: <oldKey>`; the model's index
  ignores superseded messages.
- **Delete** → publish a `{ type: "tombstone", target: <oldKey> }` message.

Example published content (the `bookmark` module):
```js
{ type: "bookmark", author: ssb.id, url, tags, description, category,
  createdAt, updatedAt, opinions: {}, opinions_inhabitants: [] }
```

#### Module anatomy — the 8 touch-points to add a feature
Reference module to copy: **`bookmark`** (`bookmarking_model.js` + `bookmark_view.js`).

1. **Model** — `src/models/<name>_model.js`: `module.exports = ({ cooler }) => {…}`,
   define `type:"<name>"`, expose `listAll / getById / create / update / delete /
   createOpinion`. Read via `ssb.createLogStream`, write via `ssb.publish`.
2. **Register model** — in `backend.js` (~line 554):
   `const xModel = require("../models/<name>_model")({ cooler, isPublic: config.public })`.
3. **View** — `src/views/<name>_view.js`: hyperaxe functions returning HTML;
   forms POST to the routes; texts via `i18n`.
4. **Routes** — in `backend.js`, guarded by `checkMod(ctx,'<name>Mod')`:
   `GET /<name>` (list), `GET /<name>/:id`, `GET /<name>/edit/:id`,
   `POST /<name>/create`, `POST /<name>/update/:id`, `POST /<name>/delete/:id`,
   `POST /<name>/opinions/:id/:cat`.
5. **Menu link** — `src/views/main_views.js`: `renderXLink()` gated on
   `getConfig().modules.<name>Mod === "on"`.
6. **Modules admin** — add to the `modules` array in `src/views/modules_view.js`.
7. **Config flag** — `src/configs/oasis-config.json` → `"modules": { "<name>Mod": "on" }`.
   Saved/toggled via `POST /save-modules`.
8. **i18n** — add keys to `src/client/assets/translations/oasis_<lang>.js`
   (langs: en es fr eu de it pt zh ar hi ru; loaded by `i18n.js`).

#### Key files
| Purpose | Path |
|---|---|
| Router (all routes) | `src/backend/backend.js` |
| Module flags | `src/configs/oasis-config.json` |
| Model template | `src/models/bookmarking_model.js` |
| View template | `src/views/bookmark_view.js` |
| Menu / `template()` / `i18n` | `src/views/main_views.js` |
| Modules admin UI | `src/views/modules_view.js` |
| SSB connection handle | `src/client/gui.js` (`cooler`) |
| sbot bootstrap | `src/server/SSB_server.js` |
| Translations | `src/client/assets/translations/` |

---

### 4 · Mapping flove → Oasis

The thesis: **a flove app becomes an Oasis module; a flove element becomes an SSB
message type.** The pieces already named in the flove backend plan line up:

| flove concept | Oasis equivalent | Notes |
|---|---|---|
| **CSS-pure distro** (tiers `mini`/`basic`, 0 JS) | Oasis frontend (HTML+CSS, no client JS) | **Strongest alignment.** Oasis *forbids* browser JS; flove's CSS-first stance is native here. The JS distro (`flove.js`) does **not** port — only the CSS-pure surface does. |
| **`FloveElement`** + `asterism_path` | one SSB `content.type` (e.g. `type:"flove.<class>"`) | the 9 universal classes (Act·Wish·Bond·Place·Person·Time·Object·Freedom·Rating) → typed messages |
| **`OasisPublisher`** adapter (F2) | `ssb.publish(content)` via a model's `create()` | the Publisher adapter wraps exactly the §3 model write path |
| **`routing.json`** (F1) | app → module + field → message-type map | declarative map from each flove app field to an Oasis module/route |
| **common traceable area** (F4) | SSB feed + `ssb-backlinks` / `ssb-tangle` / search | cross-app querying rides on SSB links + backlinks |
| **identity + Publish button** (F3) | SSB keypair (`@…​.ed25519`); no login | identity is the feed id; "masks" = managing which feed |
| **puzzy engine** (F6) | could live as `opinions`/ratings on messages | Oasis already has an opinions/voting primitive per message |
| **module 42 (fine-tuned AI)** (F5) | Oasis AI "42" (`aiMod`, gguf model) | only if a model is downloaded; off by default |

**Practical consequence:** to adapt a flove app, build it as an Oasis module
(the §3 8-step recipe) whose `view.js` renders the app's **CSS-pure** markup and
whose `model.js` publishes the app's fields as a typed SSB message. The CSS-pure
flove apps are the portable ones; anything depending on `flove.js` (drag&drop,
dynamic lists, SVG editing, live selection) has no home in the no-JS frontend and
must be redesigned as form round-trips or dropped for the Oasis surface.

→ This is the "distro CSS-pura (spec portable a otras plataformas)" of the two
flove distros, with Oasis as its first real target platform.

---

### 5 · Open questions / next steps

- **Module-per-app vs one flove module?** Either 1 Oasis module per flove app, or
  a single `flove` module routing internally by `asterism_path`. (Mirrors the
  routing-authoring open question in `backend.md` §9/§12.)
- **Message-type namespacing:** `type:"flove.act"` vs reusing Oasis native types
  (e.g. flove "bonds" → Oasis `bookmark`/`opinions`)? Reuse buys interop with
  existing Oasis modules; custom types keep the flove ontology clean.
- **Upstream vs fork:** contribute flove modules to `epsylon/oasis`, or maintain a
  flove overlay? AGPL-3.0 either way.
- **No-JS redesign:** audit which flove apps survive the pure-HTML+CSS constraint
  (CSS-pure tiers pass; advanced JS apps need rework). Tie to the tier model.
- **Pub hosting:** if flove wants its own always-on relay, run `sh oasis.sh server`
  + `announce` and list on `oasis-project.pub`.

---

### Links

- Code: `github.com/epsylon/oasis` · `code.03c8.net/epsylon/oasis`
- Site: `0asis.net` · Pub directory: `oasis-project.pub`
- Wiki: `wiki.solarnethub.com` (modules, roadmap, LARP houses, ECOin)
- SSB protocol guide: `ssbc.github.io/scuttlebutt-protocol-guide`

*Deep reference for the flove→0asis adaptation. The roadmap that consumes it is
`backend.md` §2/§6/§7 + [`plans/index.md`](../../archive/old/plans/index.md) (phases F1–F6).*

<a id="performance-review"></a>
## Browsy + FastAPI + libSQL review

> Source: `development/wiki/archive/old/reviews/2026-07-25-browsy-fastapi-libsql-performance-review.md` (archived 2026-11-21).

> 2026-07-25. Audit of all browsy, Central, and shared-code plans through the lens of performance, consistency, and build-readiness.

### The Architecture (What's Decided)

**Browsy** (browser extension) is the **CORE navigation layer**. **Central** (FastAPI + Turso/libSQL) is the **data bank** that enriches it. Three layers total:

```
browsy (extension, local trust)  →  Central (FastAPI+Turso, cloud sync)  →  Nety (P2P extension)
```

Key specs: 50MB storage / 100MB memory / 1% CPU idle budget. 3-hop web of trust, 100 users LRU in IndexedDB (~1.2MB). libSQL everywhere (SoloRich local WASM + Central remote Turso). CRDT-based conflict resolution.

#### Key Clarifications (from Marc, 2026-07-25)

1. **Solo vs Central are different code.** Solo(Rich) files are NOT the same code as Central — only names are preserved. Solo stays frozen or low-development when Central/Decentral evolve. Solo is for `file://` use, not for local server use.
2. **WASM needs headroom.** Other features must save latency and memory so WASM can run ok. If WASM is too heavy, document alternatives — don't force it.
3. **Unify local persistence.** Browsy storage across 4 APIs (IndexedDB, Extension storage, localStorage, sessionStorage) must be harmonized into a single approach.
4. **CRDTs for conflict resolution.** Adopt CRDT-style merge for trust data (Alternative 2 accepted).
5. **H4 resolved.** Split `central/` into `addons/backend/` and `central/apps/` folders.
6. **Trust sync = separate endpoint.** Don't batch trust with profile/app data.
7. **Per-app schema validation.** Validate against `collect-schemas.json` on the server.
8. **Document WASM footprint.** Measure and publish actual numbers.
9. **Versioned ping.** `/api/ping` returns server version + feature flags.
10. **Trust sync protocol.** Define payload shape, conflict strategy, merge behavior explicitly.
11. **Centralize browsy storage.** Use Extension storage everywhere for browsy.
12. **Schema versioning.** `collect-schemas.json` gets a `schema_version` field.
13. **MV3 WASM pre-cache.** Document how WASM binary stays cached across service worker restarts.

### Sources Reviewed

| File | Lines | Focus |
|------|-------|-------|
| removed: browser-extension plan | 865 | Browsy features, sync, trust tiers, identity model |
| [`../plans/central-backend.md`](../../archive/old/plans/central-backend.md) | 311 | FastAPI endpoints, Turso/libSQL, deployment, identity |
| removed: shared-code plan | 152 | Enrichment loader, DB abstraction, flove.js |
| removed: nety-frontend plan | 105 | Nety tabs, mask system, MyNet architecture |
| [`../plans/standards.md`](../../archive/old/plans/standards.md) | 139 | Distro strategy, SD18, enrichment contract |
| [`../plans/conflicts.md`](../../archive/old/plans/conflicts.md) | 149 | Cross-plan tensions, H1-H6, S1-S6 |
| [`../../backend.md`](../../archive/old/root/backend.md) §16 | 139 | Storage tiers, budgets, eviction, compression |
| [`../../adoption.md`](../../archive/old/root/adoption.md) | 110 | Distro matrix, Central+Browsy=CORE |

---

### Strengths

1. **libSQL Everywhere (C4)** — One API across SoloRich/Central/Decentral means `@libsql/client` works locally (sql.js WASM + OPFS) and remotely (Turso HTTP). SoloRich→Central migration is just changing a connection string.
2. **Offline-first trust** — browsy computes trust locally, Central enriches when online (H6). No trust computation depends on network.
3. **Progressive identity** — Device UUID → email claim → future OAuth. No friction at install, no lock-in.
4. **Minimal API surface** — 4 endpoints (`save`, `put`, `delete`, `list`) with cursor pagination. Simple enough to implement fast.
5. **CSP-safe enrichment** — `flove-loader.js` is external, no `'unsafe-inline'`. Silent failure preserves Solo mode.

---

### Cons & Risks

#### 1. WASM in the Browser is Heavy
**Problem:** `@libsql/client` loads sql.js WASM (~1-2MB) on first `flove.db` call. In a browser extension context this adds latency and memory pressure against the 100MB/1% CPU budget.

**Where it hurts:** Every SoloRich app pays this cost on first DB operation. The lazy init (CA40) helps but doesn't eliminate the cold-start hit.

#### 2. IndexedDB vs Extension Storage Confusion
**Problem:** The plan splits browsy data across IndexedDB (trust scores, profiles), Extension storage (webhook configs), localStorage (export history), and sessionStorage (panel state) — four different APIs with different limits, different persistence semantics, and different eviction behaviors.

**Where it hurts:** Complex code paths for what should be simple reads/writes. Debugging storage issues becomes nightmare. The "user-managed" 100MB limit (BL01) has no enforcement mechanism documented.

#### 3. Last-Write-Wins Conflict Resolution is Fragile
**Problem:** CB32 + BF03 both decide last-write-wins by client timestamp. But clock skew exists (Q195 accepts the risk). Two devices editing the same trust vouch within a 5-minute window will silently lose one update.

**Where it hurts:** Trust data is the CORE of browsy. Silent data loss in the trust graph is worse than showing a conflict.

#### 4. Railway Monorepo Deploy Ambiguity (H4 — Still Open)
**Problem:** `central/` branch contains both FastAPI backend (needs Railway deploy) AND modified app files (needs flove.org deploy). H4 in conflicts.md is explicitly "Open — deploy pipeline needs to distinguish backend changes from app changes."

**Where it hurts:** A single PR could break both the API and the frontend with no way to test them independently.

#### 5. No Rate Limiting Until Post-PoC (CB37)
**Problem:** Zero rate limiting initially. While CB37a plans per-IP 100 req/min later, the PoC window is exploitable. Any script can POST unlimited data to Turso.

#### 6. 1MB Payload Limit (CB_S01) May Be Too Low
**Problem:** Web of trust at 3 hops is ~1MB. Profile data is ~100KB. If browsy pushes full trust graph + profile + app data in one sync, it hits the limit immediately.

#### 7. No Offline Queue for Central (CB33)
**Problem:** "No queue, no auto-retry for Central" — changes are lost if the user edits while offline. The `flove:pending-sync` flag (CB_S03) just tells the button to show a count, but there's no actual queue backing it.

#### 8. WASM Pre-caching in sw.js (D09) Has Browser Extension Tension
**Problem:** Browser extensions have their own caching model. Service workers (MV3) and extension storage don't mix cleanly. Pre-caching WASM in sw.js may not work from the extension context.

#### 9. 5-Minute Sync Batching is Arbitrary
**Problem:** BF01 + BE20 decide 5-minute batched sync. But trust changes are real-time (Q210). The plan says "batched 5 min + real-time for trust changes" — but the trust sync mechanism isn't specified beyond this sentence.

#### 10. No Server-Side Validation of Data Shape (D06)
**Problem:** "Validate `data` is valid JSON, `user` is non-empty string" — that's it. No per-app schema validation. A malformed trust vouch POSTed by a buggy browsy version gets stored permanently (D01: no TTL).

---

### Alternatives (with Pros/Cons)

#### Alternative 1: WASM Local Persistence — sql.js vs wa-sqlite vs IndexedDB wrapper

| Option | WASM size | SQLite compat | Async | OPFS support | Maintenance |
|--------|-----------|---------------|-------|--------------|-------------|
| **sql.js** (current) | ~1.5MB | Full | Callback-wrapped | Yes | Active, mature |
| **wa-sqlite** | ~400KB | Full | Native async | Yes | Active, smaller community |
| **IndexedDB wrapper** (idb/kysely) | 0 (no WASM) | None | Native async | N/A | Active, lightweight |

| | Pros | Cons |
|---|------|------|
| **sql.js** | Battle-tested, full SQLite, OPFS | Largest WASM, cold-start ~200ms, ~8MB peak memory |
| **wa-sqlite** | 75% smaller WASM, faster compile, same API | Less documentation, smaller community, same OPFS complexity |
| **IndexedDB wrapper** | Zero WASM overhead, instant init, tiny bundle | No SQL — apps lose `flove.db` schema, migration needed for SoloRich |

**Decision:** Keep sql.js for SoloRich (where full SQLite schema is needed). Document wa-sqlite as drop-in alternative if WASM budget is exceeded. IndexedDB wrapper only if SoloRich schema simplifies enough to drop SQL.

#### Alternative 2: CRDTs for Trust Conflict Resolution (ACCEPTED)

| | Pros | Cons |
|---|------|------|
| **Vector clocks** | Eliminates clock skew risk, causally ordered | ~20% storage overhead per vouch entry, more complex merge logic |
| **Yjs integration** | Battle-tested CRDT, handles concurrent merges natively | ~100KB additional WASM/library, adds dependency |
| **Custom CRDT** | Minimal overhead, tailored to trust model | Must implement and test merge correctly, no community support |

**Decision:** Start with custom vector clocks (low overhead, trust-specific). Evaluate Yjs if the merge logic becomes complex. CRDT merge happens client-side (browsy); server stores merged result.

#### Alternative 3: Central Directory Split (ACCEPTED — resolves H4)

```
central/
  backend/           ← Railway watches this, deploys FastAPI
    main.py
    apps.json
    collect-schemas.json
    requirements.txt
    .env
    migrations/
  apps/              ← GitHub Pages watches this, serves flove.org
    index.html
    goddy.html
    souls.html
    ...
  shared/            ← Both deploy pipelines read (read-only)
    libs/
```

| | Pros | Cons |
|---|------|------|
| **Split dirs** | Independent deploy, independent testing, clear ownership | Shared libs need a read-only contract, slightly more complex PR workflow |
| **Keep monorepo** | Simpler git history, single PR for coupled changes | Deploy ambiguity (H4), can't test independently |

**Decision:** Split into `backend/` + `apps/` + `shared/`. Railway CI watches `backend/`, GitHub Pages CI watches `apps/`. `shared/` is read-only for both.

#### Alternative 4: Turso Embedded Replicas (FUTURE — when Turso Database is stable)

| | Pros | Cons |
|---|------|------|
| **Embedded replicas** | Zero WASM cold-start (native SQLite file), reads in microseconds, writes replicate to cloud | Requires Turso Database (beta), not available today, Rust-only server |
| **Current WASM approach** | Works today, no Turso dependency, full SQLite in browser | Cold-start latency, memory pressure, OPFS browser support varies |

**Decision:** Defer to CentralRich phase. WASM is the v1 path. Embedded replicas are the v2 path when Turso Database stabilizes.

#### Alternative 5: Event-Driven Sync (ACCEPTED — replaces 5-min batching)

| | Pros | Cons |
|---|------|------|
| **chrome.alarms** | Trust syncs immediately, profile syncs on idle, battery-friendly | Requires `alarms` permission, more complex scheduling logic |
| **5-min batch** (current) | Simple, predictable, easy to debug | Trust changes delayed up to 5 min, arbitrary interval |
| **WebSocket push** | True real-time, server→client push for notifications | Requires persistent connection, server scaling complexity, battery drain |

**Decision:** `chrome.alarms` for browsy. Trust changes = immediate push. Profile/app data = sync on idle (no arbitrary timer). WebSocket deferred to CentralRich when server infrastructure supports it.

#### Alternative 6: Unified Browsy Storage — Extension storage vs IndexedDB vs Hybrid

| | Pros | Cons |
|---|------|------|
| **Extension storage only** | Synchronous API, persistent, same 10MB quota in MV3, simple | 10MB limit (enough for browsy's ~1.2MB trust data), no structured queries |
| **IndexedDB only** | Structured queries, 50-200MB quota, async | Async API adds complexity, different persistence semantics per browser |
| **Hybrid (current)** | Best tool per data type | 4 APIs = 4 code paths, debugging nightmare, inconsistent eviction |

**Decision:** Extension storage for browsy (trust, profiles, webhook configs, panel state). It's persistent, synchronous, and 10MB is plenty for browsy's ~1.2MB working set. IndexedDB stays only for apps that need structured queries (nety circles).

---

### Suggestions

#### High Priority

1. **Resolve H4 now.** The open deploy conflict will block Central from going live. Split the directory structure before building anything.
2. **Add a real offline queue for Central.** The `flove:pending-sync` flag is a boolean, not a queue. Use IndexedDB to store pending operations as an ordered log, replay on next connectivity check.
3. **Implement trust sync as a separate endpoint.** Don't batch trust with profile/app data. Give trust its own `POST /api/trust/sync` with immediate processing and conflict detection at the vouch level.
4. **Add per-app schema validation to Central.** At minimum, validate required fields per `collect-schemas.json`. Reject and log malformed data instead of storing garbage permanently.

#### Medium Priority

5. **Document the WASM memory footprint.** Add actual measurements: sql.js init time, memory usage, OPFS write latency on Chrome/Firefox. The 100MB budget is a guess without numbers.
6. **Consider wa-sqlite as sql.js replacement.** Smaller WASM, same API surface, better async support.
7. **Add a `GET /api/ping` health endpoint that also returns server version.** Current ping just confirms Central is available. Adding version lets browsy know what features are supported (e.g., trust sync endpoint existence).
8. **Define the trust sync protocol explicitly.** "Batched 5 min + real-time for trust changes" is not a protocol. Specify: what payload shape, what conflict detection, what merge strategy, what happens when the trust graph exceeds 1MB.

#### Low Priority (Polish)

9. **Centralize browsy storage into fewer APIs.** Use Extension storage for everything browsy-related (it's persistent, synchronous, and has the same quota as IndexedDB in MV3). Remove the IndexedDB/localStorage/sessionStorage split.
10. **Add a `collect-schemas.json` version field.** Per D06, the server accepts any schema. Add a `schema_version` field so browsy can detect if its schema is stale and prompt the user.
11. **Document the WASM pre-cache behavior in MV3.** Service workers in MV3 have limited lifetime. Explain how WASM binary stays cached across service worker restarts.

---

### Open Questions Requiring Answers Before Build

| # | Question | Blocks | Status |
|---|----------|--------|--------|
| 1 | H4 deploy pipeline split — `backend/` + `apps/` + `shared/` | Central backend go-live | **Resolved** (Alt 3) |
| 2 | Trust sync: payload shape + conflict strategy | Trust feature completeness | **Accepted** (separate endpoint, CRDTs) — needs protocol spec |
| 3 | WASM actual memory/latency measurements | Performance budget validation | **Accepted** — needs measurements |
| 4 | Rate limiting strategy during PoC window | Security posture | Open |
| 5 | 1MB payload limit: enough for trust-only sync? | Sync reliability | Open — trust graph ~1MB alone |
| 6 | Offline queue: IndexedDB log or abandon? | Offline-first promise | **Accepted** — needs implementation spec |
| 7 | CRDT library choice: custom vector clocks vs Yjs? | Trust merge complexity | Open — start custom, evaluate Yjs later |
| 8 | `chrome.alarms` permission: justify to Chrome Web Store? | Extension approval | Open — may need "minimum permission" justification |
| 9 | Extension storage 10MB limit: enough for browsy long-term? | Storage budget | Open — current ~1.2MB, but grows with trust graph |
| 10 | Solo freeze policy: when exactly does Solo stop receiving updates? | Solo user migration | Open |
| 11 | `shared/` contract: what's read-only vs modifiable by each pipeline? | Deploy safety | Open |
| 12 | Schema version migration: how does browsy detect stale `collect-schemas.json`? | Data integrity | Open |

---

### Further Questions (from Marc's Replies)

These questions arise from Marc's clarifications and need answers before implementation.

#### Solo Freeze & Migration

| # | Question | Context |
|---|----------|---------|
| FQ01 | When exactly does Solo stop receiving feature updates? Is it frozen at current state, or does it get security patches only? | Solo is for `file://` use, Central evolves separately |
| FQ02 | Does the enrichment loader (`flove-loader.js`) still need to support Solo, or does Solo ship fully self-contained with no external deps? | If Solo is frozen, loader may not need Solo path |
| FQ03 | What happens to Solo users when Central is live? Is there a migration path, or are they separate audiences forever? | Solo = `file://` users, Central = `flove.org` users |

#### WASM Budget & Alternatives

| # | Question | Context |
|---|----------|---------|
| FQ04 | What's the maximum acceptable WASM cold-start time? 100ms? 500ms? 1s? | "Save latency and memory from other features for WASM to run ok" |
| FQ05 | What's the WASM memory ceiling during init? 10MB? 20MB? Needs to fit within 100MB total budget | Other features must yield memory |
| FQ06 | Should browsy defer non-essential features (discovery scoring, notification badge) until WASM is loaded? | Feature scheduling to protect WASM init |
| FQ07 | If WASM fails to load, does the app fall back to localStorage only, or does it show an error? | Silent fallback is current plan — is that still ok? |
| FQ08 | Is wa-sqlite worth evaluating now, or only if WASM budget is exceeded? | "Document alternatives to it" — when to actually switch? |

#### Unified Storage

| # | Question | Context |
|---|----------|---------|
| FQ09 | Is Extension storage the definitive unified API for browsy? Or is IndexedDB still needed for structured queries? | "Definitely harmonize, unify" |
| FQ10 | What's the migration path from existing IndexedDB data to Extension storage? One-time export/import on update? | Current users have trust data in IndexedDB |
| FQ11 | Does Extension storage support binary data (ArrayBuffer) for compressed trust graphs? | gzip-compressed JSON needs binary write |
| FQ12 | What happens to `sessionStorage` usage (panel state)? Is that truly ephemeral, or should it also move to Extension storage? | Panel state = P1 (session), does it need persistence? |

#### CRDT Conflict Resolution

| # | Question | Context |
|---|----------|---------|
| FQ13 | Which trust fields need CRDT merge? All fields, or only timestamps and trust levels? | "Alternative 2 to implement unified yes" |
| FQ14 | Does CRDT merge happen in browsy (client-side) or in Central (server-side)? | Affects server complexity |
| FQ15 | What's the CRDT overhead per vouch entry? How much does vector clocks add to the ~200B/entry budget? | "Save memory" — CRDT adds metadata |
| FQ16 | Should non-trust data (profile, app data) also use CRDTs, or only trust? | Trust is CORE, but profile conflicts also exist |
| FQ17 | How does CRDT merge interact with the 1MB payload limit? Does CRDT metadata push us over? | Trust graph is already ~1MB |

#### Central Directory Split

| # | Question | Context |
|---|----------|---------|
| FQ18 | Does `addons/` contain only `libs/`, or also `apps.json` and `collect-schemas.json`? | Both deploy pipelines reference these |
| FQ19 | Can a single PR touch both `backend/` and `apps/`, or must they be separate PRs? | "Create backend/ and apps/ folders in central/" |
| FQ20 | How does Railway detect changes in `backend/` only? Path filter in `railway.toml`? | Avoids redeploying on app-only changes |
| FQ21 | Does `addons/` deploy to flove.org, or is it bundled into both `backend/` and `apps/`? | Shared libs availability |

#### Trust Sync Protocol

| # | Question | Context |
|---|----------|---------|
| FQ22 | What's the trust sync endpoint shape? `POST /api/trust/sync` with what body? | "Trust as diff sync endpoint, yes" |
| FQ23 | Does trust sync use delta (only changed vouches) or full graph replacement? | Affects payload size vs complexity |
| FQ24 | What happens when trust graph exceeds 1MB? Truncate oldest? Paginate? Reject? | 1MB limit (CB_S01) vs 3-hop graph ~1MB |
| FQ25 | Does browsy push trust to Central, or does Central pull from browsy? | Direction affects latency and offline behavior |
| FQ26 | Can trust sync happen without a full profile sync, or are they coupled? | Trust is real-time, profile is batched |

#### Per-App Schema Validation

| # | Question | Context |
|---|----------|---------|
| FQ27 | What's the validation error behavior? Reject + return error, or store + log warning? | "Add per-app schema validation yes" |
| FQ28 | Does `collect-schemas.json` define required fields, types, or full JSON Schema? | Affects validation complexity |
| FQ29 | Who maintains `collect-schemas.json`? Auto-generated from app code, or manually maintained? | Staleness risk if manual |
| FQ30 | Does schema validation apply to trust sync endpoint too, or only app data? | Trust has its own endpoint |

#### Versioned Ping

| # | Question | Context |
|---|----------|---------|
| FQ31 | What features does `/api/ping` advertise? Version number, feature flags, or capability list? | "Add ping with version yes" |
| FQ32 | Does browsy cache the ping response, or re-check on every load? | Current: cache in localStorage for session |
| FQ33 | What happens if Central is downgraded (version goes backward)? Does browsy handle it? | Edge case for feature detection |

#### MV3 WASM Pre-Cache

| # | Question | Context |
|---|----------|---------|
| FQ34 | In MV3, does the service worker cache WASM, or does the extension storage cache it? | "Document WASM pre-cache behavior in MV3" |
| FQ35 | MV3 service workers terminate after 30s idle. Does WASM survive termination? | WASM binary needs to survive SW restarts |
| FQ36 | Is WASM pre-caching even necessary if lazy init (CA40) already loads on first use? | May be premature optimization |

## Source index

### apps/README.md — 2026-11-09

- Archive: `development/wiki/archive/old/apps/README.md`
- Stable home: `development/standards/systems.md`
- Status: summarised in the stable page; no open decision is recorded here.

### bridges/oasis.md — 2026-08-01

- Archive: `development/wiki/archive/old/bridges/oasis.md`
- Stable home: `development/standards/systems.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/README.md — 2026-08-01

- Archive: `development/wiki/archive/old/browsy/README.md`
- Stable home: `development/standards/systems.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/TESTING.md — 2026-08-01

- Archive: `development/wiki/archive/old/browsy/TESTING.md`
- Stable home: `development/standards/systems.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/browsy-questions.md — 2026-08-01

- Archive: `development/wiki/archive/old/browsy/browsy-questions.md`
- Stable home: `development/standards/systems.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/port-nety.md — 2026-08-01

- Archive: `development/wiki/archive/old/browsy/port-nety.md`
- Stable home: `development/standards/systems.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/pre-build/05-native-host.md — 2026-11-17

- Archive: `development/wiki/archive/old/browsy/pre-build/05-native-host.md`
- Stable home: `development/standards/systems.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/pre-build/06-bridge-threat-model.md — 2026-11-17

- Archive: `development/wiki/archive/old/browsy/pre-build/06-bridge-threat-model.md`
- Stable home: `development/standards/systems.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/rationale.md — 2026-11-17

- Archive: `development/wiki/archive/old/browsy/rationale.md`
- Stable home: `development/standards/systems.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/spec.md — 2026-11-17

- Archive: `development/wiki/archive/old/browsy/spec.md`
- Stable home: `development/standards/systems.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/2026-11-17-appy-authy-mynet.md — 2026-11-17

- Archive: `development/wiki/archive/old/plans/2026-11-17-appy-authy-mynet.md`
- Stable home: `development/standards/systems.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/2026-11-21-app-database-stages.md — 2026-11-21

- Archive: `development/wiki/archive/old/plans/2026-11-21-app-database-stages.md`
- Stable home: `development/standards/systems.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/central-backend.md — 2026-08-01

- Archive: `development/wiki/archive/old/plans/central-backend.md`
- Stable home: `development/standards/systems.md`
- Status: summarised in the stable page; no open decision is recorded here.

### reviews/2026-07-25-browsy-fastapi-libsql-performance-review.md — 2026-07-25

- Archive: `development/wiki/archive/old/reviews/2026-07-25-browsy-fastapi-libsql-performance-review.md`
- Stable home: `development/standards/systems.md`
- Status: summarised in the stable page; no open decision is recorded here.

### root/adoption.md — 2026-08-01

- Archive: `development/wiki/archive/old/root/adoption.md`
- Stable home: `development/standards/systems.md`
- Status: summarised in the stable page; no open decision is recorded here.

### root/backend.md — 2026-08-01

- Archive: `development/wiki/archive/old/root/backend.md`
- Stable home: `development/standards/systems.md`
- Status: summarised in the stable page; no open decision is recorded here.

### root/worldview.md — 2026-08-01

- Archive: `development/wiki/archive/old/root/worldview.md`
- Stable home: `development/standards/systems.md`
- Status: summarised in the stable page; no open decision is recorded here.
