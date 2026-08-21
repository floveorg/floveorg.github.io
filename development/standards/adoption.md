# flove · Frontend adoption checklist (§14)

Which harvested standards (`frontend.md §13.x`) each app has adopted. This is
the **frontend roadmap** — each cell is a unit of *pulido* work. A living
table: update it as standards are elevated into each app. The stable index of
what the standards *are* is `README.md`; the full spec is `frontend.md`.

**Before starting adoption work**, check [`plans/conflicts.md`](debates/plans/conflicts.md) for known tensions between plans.

## Architecture

**Browser Extension + Central = CORE** — browsy is the main navigation +
identity/trust bridge; Central is the data bank + frontend apps; Decentral Nety
is an extension for P2P distributed computation only. Repo: `central/` (backend,
storage, API) + `decentral/` (nety + P2P tools). Full spec in [`central.md`](central.md) §1–2.

## Web of Trust Persistence Budget

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Hop depth** | 3 hops | Full network (~1MB) |
| **Max users** | 100 | ~20KB storage |
| **Compression** | JSON | ~70% reduction with gzip |
| **Eviction** | LRU | Least recently used |

**Trust visibility:** first circle, second circle, social groups, public.

| App | Tier model (§13.1) | i18n (§13.2) | Forms-iframe (§13.3) | Compass (§13.4) | Topbar (§13.5) | Onboarding (§13.6) | Vocab (§13.7) | Counters (§13.8) | Summary (§13.9) | Export (§13.12) | Surfaces (§13.11) |
|-----|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| blogy | ✓ (5 of 7) | ✓ | ✓ (4 forms) | ✓ | partial | partial | ✓ (reference) | ✓ | ✓ (reference · advanced) | partial | 2D |
| questy | — | — | — | — | — | — | — | — | — | — | — |
| (all others) | — | — | — | — | — | — | — | — | — | — | — |

Mark **N/A** where a standard doesn't apply (e.g. compass when the app has only
one valid layout). Marking onboarding or vocab as `partial` is acceptable while
migration is in progress (track specific renames via the §13.7 deferred-renames
doc-comment in each file).

> **Reference note:** the `(reference)` cells above point at **blogy**, the Solo
> fallback reference. The **Central** apps (`central/apps/`) are the canonical
> spec — see [`solo/README.md`](solo/README.md).

## CSS abstraction checklist (§13.16)

Per-app CSS abstraction status — tracks whether apps use the shared flove
libraries and canonical tokens.

| App | Imports CSS | Uses canonical tokens | No invented tokens | Shared interaction classes |
|-----|:-----------:|:---------------------:|:------------------:|:--------------------------:|
| questy | ✓ `flove-base.css` | ✓ (aliases for migration) | ⏳ migrating | — |
| blogy | ✓ `flove.css` | ✓ | ✓ | — |
| appy | — (inline) | — | — | — |
| (all others) | — | — | — | — |

**Column definitions:**
- **Imports CSS**: links `flove-base.css` or `flove.css` from `central/shared/`
- **Uses canonical tokens**: `--ink`, `--line`, `--card`, `--signal` (not `--text`, `--border`, `--surface`, `--green`)
- **No invented tokens**: no app-specific surface/semantic tokens beyond `--app-accent*`
- **Shared interaction classes**: uses `.flove-focus`, `.flove-selected`, `.flove-lift` from §13.16

## Publish to Appy (§13.15) — adoption & rollout

The app → Appy bridge (`flove-appy.js`). State today (audit 2026-07-20):

| Role | App(s) | Publish state |
|------|--------|---------------|
| READER | `appy-mini` · `appy-mini-full` · `appy-basic` | ✓ read the bridge (`floveAppy.played` + `onChange`) **and** accept the manual `<app>-summary.json` upload |
| WRITER | `goddy` · `souls` · `pracsys` (`apps/bio/`) · `inventary` (`apps/economy/dealy/`) · `realy` (`apps/psicosocial/`) · `myfamily` (`apps/trusty/`) · `keys` (`apps/puzzy/keys/keys-advanced.html`) | ✓ full trio — script + `window.floveSummary` + `appy/wizy/more` buttons. **All 7 carry a domain `window.floveAgentBlock`** (wizy) and **auto-publish on Update** (F1). souls was the 2026-07-20 reference; keys (the 7th, in `COLOURS`) wired 2026-07-20 alongside its existing CSS-only Go/platforms cycle |

**Rollout order** (scalability): the WRITER trio is now on all **seven** `COLOURS`
emitters above; `souls` was the template and `COLOURS` already held every one, so no
registry edit was needed. Each also ships a domain wizy agent block and auto-publish
(F1, always on, local-only). `mini` never publishes; `basic`+ carry appy/wizy; `more`
(nety / 0asis) waits for F2+. Cross-device sync is a backend milestone, not this phase.
Full rule: [`frontend/publish.md`](frontend/publish.md).

**The current appy apps, per environment** (Marc runs on `file://`):

| Environment | What the appy apps do today |
|---|---|
| `file://` | **Only the manual upload delivers** to the profile — the bridge can't cross `file://` documents. With the new fallback, an app's publish button **downloads its `<app>-summary.json`** for you to drop on Appy's "Upload summary here". |
| `http://localhost:<port>` | **Bridge live**: a WRITER (e.g. `goddy`) publishes → `appy-mini` / `appy-mini-full` / `appy-basic` show it instantly (`onChange`). Manual upload also works. |
| `https://flove.org` | Same as localhost. |

So for a `file://` workflow the real path is **download → upload**; the automatic
bridge is a bonus that only kicks in once the apps are served over http.

## Distro adoption (§13.11) — enrichment rollout

Which apps have adopted the enrichment loader and which distro they target. The
enrichment loader (`flove-loader.js`) is the Solo→SoloRich bridge; Central+ adds
backend depth on separate branches.

**Browsy is the main navigation app.** It gets HTML from Central (or solo fallback backup). Updates via central/shared (JS and CSS). Lightweight, considering browser consumption and persistence.

| App | Enrichment | Distro target | Branch |
|-----|-----------|---------------|--------|
| blogy | ✅ enriched | SoloRich → Central | `main` → `central/` |
| 46 normal/advanced/super apps | ✅ enriched | SoloRich → Central | `main` → `central/` |
| 8 mini/basic apps | ⏸ opt-in | Solo (no enrichment) | `main` |
| 16 support pages | ❌ skipped | — | `main` |

**SoloRich → Central persistence:** libSQL via `@libsql/client` (wraps sql.js
WASM + OPFS) everywhere, single shared `flove.db` with `app` column, fallback
localStorage key `flove:db`. Central backend serves `flove.org/api/*`. Full CRUD
spec in [`plans/central-backend.md`](debates/plans/central-backend.md).

## Generic Webhook Exports

Browsy and Central can export profile data to external services via generic webhooks.

| Parameter | Decision |
|-----------|----------|
| **Storage** | Both (browsy local + Central synced copy) |
| **Trigger** | Manual only (user clicks export) |
| **Auth** | User-configurable (supports all methods) |
| **Proxy** | Both (browsy direct OR via Central) |

**Export targets:** GitHub repo, GitHub Pages, Gitea, custom URL, local file.
