# Plan: Central Backend

> Decisions: CB01-CB40 + C01-C76 + D01-D23 + E01-E25 + G01-G55 + CB_S01-CB_S10 (FastAPI + Turso backend for Central distro, serverless on Railway, libSQL everywhere, Nety-Central bridge, profile mirror, browsy integration).
> Cross-refs: `plans/shared-code.md` (enrichment loader CA09-CA44),
> `plans/nety-frontend.md` (Nety client architecture),
> `plans/nety-trust.md` (trust in Nety, Central reads only),
> `plans/browser-extension.md` (browsy — CORE trust features),
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
| CB17 | Server structure | Single `main.py` — loads app list from `central/backend/apps.json` registry (simple list) |
| CB18 | Libs folder | Central has its own `central/shared/` (the former `central/libs/`) — NOT `apps/appy/`. Separate from SoloRich. Read-only for both deploy pipelines. |
| CB19 | Branch model | Full fork — `central/` branch diverges from `main`. Selective cherry-pick of bug fixes back to main. Deploy via PR merge → Railway auto-deploy. |
| CB20 | CORS | Configurable via `.env` — `CORS_ORIGINS=https://flove.org` for production, overridable for dev |
| CB20a | CORS staging | Allow both: `CORS_ORIGINS=https://flove.org,https://staging-railway-flove.org`. |
| CB21 | Start script | Railway auto-start via `Procfile` or `railway.toml`. Two services: FastAPI + libSQL server. Connected via internal Railway DNS. Local dev deferred. |
| CB22 | Error handling | Specific error messages from server — shown in the sync button area with "Retry" |
| CB23 | List response | Items only — `{items: [...], next_cursor: "..."}`. No total count. |
| CB24 | Prerequisites | Python 3.10+, `pip install fastapi uvicorn libsql-client` |
| CB25 | Data scope | Everything — full `window.flove.collect()` output stored as `data` JSON. App-defined shape, documented in `central/backend/collect-schemas.json`. |
| CB26 | Deployment | Railway — simple deploy from GitHub, PR merge triggers auto-deploy |
| CB27 | URL | `flove.org/api/` — same domain, no subdomain. GitHub Pages proxies `/api/*` to Railway. |
| CB28 | DB choice | Turso — SQLite-compatible HTTP API, designed for serverless. Same API as local SQLite (libSQL client). |
| CB29 | Discovery | Hybrid: flove.js pings `/api/ping` on `flove.org` (same origin via GitHub Pages proxy), caches result in localStorage for session |
| CB30 | Indexes | `(app, user)` — covers the only list query pattern |
| CB31 | Schema versioning | Yes — `PRAGMA user_version` in SQLite, auto-migrate if schema changes |
| CB31a | Schema migration | SQL migration files in `migrations/`. Simple, explicit, no framework. |
| CB32 | Conflict resolution | CRDT-style merge for trust data (vector clocks, client-side). Last-write-wins for non-trust data (profile, app data). |
| CB33 | Offline queue | IndexedDB log of pending operations (ordered by timestamp). Replays on next connectivity check. `flove:pending-sync` flag shows count of pending items. |
| CB34 | App registration | Registry file `central/backend/apps.json` — simple list `["blogy", "goddy", ...]`, server validates against it |
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
| CB44 | Per-app schema validation | Validate `data` against `central/backend/collect-schemas.json` on POST/PUT. Reject with `{ok: false, error: "schema_violation", detail: "..."}` if invalid. |
| CB45 | Schema validation level | Required fields + types only (not full JSON Schema). Per-app `required` array + `fields` map with type hints. |
| CB46 | Versioned ping | `GET /api/ping` returns `{ok: true, version: "1.0.0", features: ["trust-sync", "schema-validation"]}`. Browsy caches for session. |
| CB47 | Ping feature flags | `features` array lets browsy detect server capabilities (e.g., trust-sync endpoint exists, schema validation active). |
| CB48 | Central directory split | `central/backend/` (Railway deploys), `central/apps/` (GitHub Pages deploys), `central/shared/` (read-only, both pipelines). |
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