# Conflicts & Tensions Tracker

> Cross-plan tensions identified from interview decisions (2026-07-23).
> Updated 2026-07-23 with D01-D23 strategic decisions (Central URLs primary, staging workflow, Railway monorepo, no TTL, HTTP status codes, error detail field).

## Hard conflicts

### H1: Tabbed app (Q2) × Masks F2 (Q4)

**Files**: `nety-frontend.md`
**Status**: Resolved — global mask bar above tabs

The tabbed layout has no natural place for mask switching. Masks affect every tab's content.

**Resolution**: Global mask selector bar above the tab strip. Adds ~40px vertical space. All tabs read current mask from shared state.

### H2: Weighted ranking (Q6) × Self-selected curators (Q7)

**Files**: `nety-trust.md`
**Status**: Resolved — curator bonus with decay

Trust-weighted ranking means higher-stage users have more influence. But curators are self-selected with community veto.

**Resolution**: Curator status grants ×3 weight bonus that decays 10%/week. Full resolution requires the trust layer to work first.

### H3: Multi-repo (SD01) × Full test suite (SD13)

**Files**: `standards.md`
**Status**: Resolved — shared CI infrastructure across repos

**Resolution**: Shared test runner script invoked from any repo. CI config duplicated per repo with shared workflow template.

### H4: PR merge deploy (C70) × central/ has both backend + apps (C72)

**Files**: `central-backend.md`, `plans/index.md`
**Status**: Resolved — directory split ✅ Implemented 2026-08-01

The `central/` branch contains both the FastAPI backend (needs Railway deploy) and modified app versions (need flove.org deploy, same as main). A PR could change both, but the deploy pipeline is PR→Railway for backend. App changes in `central/` would need a separate deploy path.

**Resolution**: Split `central/` into three directories:
- `central/backend/` — FastAPI + Turso, deployed by Railway (path filter in `railway.toml`)
- `central/apps/` — Central app HTML files, deployed to flove.org via GitHub Pages
- `central/shared/` — Shared libs (`libs/`), read-only for both pipelines

Railway CI watches `backend/` only. GitHub Pages CI watches `apps/` only. A single PR can touch both, but deploy pipelines are independent. `shared/` is bundled into both at deploy time.

## Soft tensions

### S1: Hybrid abuse (Q8) × Deferred infrastructure

**Files**: `nety-trust.md`
**Status**: Resolved — Tier 1 defined

Tier 1 = self-selection + community veto + simple report form. Tier 2 (jury) deferred.

### S2: Profily-integrated MyNet (Q9) × Tabbed app (Q2)

**Files**: `nety-frontend.md`
**Status**: Accepted — discoverability trade-off

MyNet tab is prominent (tab #3 of 5). Social features are the headline content.

### S3: Masks F2 (Q4) × Deferred crypto recovery (Q5)

**Files**: `nety-frontend.md`
**Status**: Resolved — recovery code v1

Recovery code displayed once at mask creation, user writes down. Lost code = new mask only.

### S4: Full offline (SD04) × Privacy-first analytics (SD02)

**Files**: `standards.md`
**Status**: Accepted — analytics degraded offline

Plausible needs network. When offline, analytics don't fire.

### S5: Anonymous device ID (C51) × data permanence

**Files**: `central-backend.md`
**Status**: Accepted — user must claim data before clearing browser

Auto-sync uses a device-generated UUID. If the user clears browser data (localStorage, OPFS), the UUID is lost and server data becomes orphaned. The claim flow (email) fixes this, but only if the user claims before clearing data.

**Resolution**: Document in Central modal: "Your data is linked to this device. Set an email to keep it if you clear your browser data."

## Coherent clusters

### C1: "Decide Now" (Q6 + Q7 + Q8)

All three overrode "Defer" suggestions. Tightly coupled: ranking needs curators, curators need abuse system.

### C2: "Privacy-First" (Q4 + Q9)

Early masks + integrated social = privacy-by-design in the social layer.

### C3: "Simple Wins" (Q2 + Q10)

Tabbed app (simple) + defer vizy XR/VR (don't add complexity).

### C4: "libSQL Everywhere" (C64 + C65 + C66 + CA37)

Same engine across SoloRich, Central, Decentral, DecentralRich. One API (`@libsql/client`), one schema, trivial SoloRich→Central migration (change connection string from local file to remote).

## Resolved this session

| Conflict | Resolution |
|----------|------------|
| H2: ranking × curators | ×3 bonus, 10%/week decay |
| H4: deploy pipeline ambiguity | Split `central/` into `backend/` + `apps/` + `shared/` |
| S1: abuse × deferred | Tier 1 = self-selection + veto + report form |
| S3: masks × recovery | Recovery code, lost = new mask |
| C16: milestone scope | JSON distro + trusty cleanup + app links |
| C07: deep link direction | One-way, trusty → maty/evily |
| C14: deep link params | `?from={app}&item={id}` |
| C11: deep link mechanism | URL params |
| C26: deep link HTML | Separate div below item |
| C04: MongoDB × SQLite/Turso | No MongoDB — Turso for serverless SQLite, PostgreSQL for CentralRich |
| C15: central/solo branch name | Renamed to `central/` |
| C18: local persistence | libSQL via `@libsql/client` (sql.js WASM + OPFS), fallback localStorage |
| D07: central/apps vs main/apps | Central apps are their own, share names only — two different things |
| D10: Central app serving | Same origin (`flove.org/api/*` proxy), no cross-origin issues |
| D20: URL hierarchy | Central URLs become primary; Solo URLs on main maintained as fallback |
| NEW: Browsy = main nav | Browsy replaces Central nav, gets HTML from Central or solo fallback |
| NEW: Central = data bank | Central enriches browsy navigations + frontend apps |
| NEW: Trust visibility | Trust acceptances need visibility parameter: first circle, second circle, social groups, public |
| NEW: Webhook exports | Generic webhooks, manual trigger, user-configurable auth |
| NEW: CRDT conflict resolution | Replace last-write-wins with CRDT-style merge for trust data |
| NEW: Unified browsy storage | Extension storage for all browsy data (trust, profiles, webhooks, panel state) |
| NEW: Trust sync endpoint | Separate `POST /api/trust/sync` — not batched with profile/app data |
| NEW: Per-app schema validation | Validate `data` against `collect-schemas.json` on server, reject malformed |
| NEW: Versioned ping | `/api/ping` returns version + feature flags for browsy feature detection |
| H7: Q16 (6 groups) × Q19 (4 groups) | 4 groups wins, Q16 removed |
| S7: Delegation in trust logic × v1 scope | Delegation is v2, direct vouches only in v1 |
| S8: "Closest" × "Close" naming | "Close" wins, browser-extension.md historical |
| S9: Friends × Close group | Same thing — friends list = Close group member list |

### S10: Per-app schema validation × undefined app datafields

**Files**: `central-backend.md`, `plans/index.md`
**Status**: Active — blocked

Per-app schema validation was resolved as a feature to implement, but the
datafields for each app have not been defined yet (questy Q010). Until the
app schemas exist, collect() validation cannot be implemented.

**Resolution**: Define per-app datafields first, then implement collect-schemas.json.
Moved to pendings.md as PEN001.

## New conflicts identified

### H5: Browsy main nav × Central nav

**Files**: `browser-extension.md`, `central-backend.md`
**Status**: Resolved — Browsy replaces Central nav

Browsy is now the main navigation app. Central apps get their nav from browsy.

**Resolution**: Browsy loads HTML from Central (or solo fallback). Updates via central/shared.

### H6: Offline trust × Central enrichment

**Files**: `browser-extension.md`, `central-backend.md`
**Status**: Resolved — Hybrid mode

Web of trust can be fully offline. Central provides optional enrichment.

**Resolution**: Browsy computes trust locally. Central can provide additional data when online.

### S6: Webhook exports × Privacy

**Files**: `browser-extension.md`, `central-backend.md`
**Status**: Resolved — User-configurable

Exports are manual, user controls what gets sent where.

**Resolution**: Manual trigger, user-configurable auth, visibility parameter for trust data.

### H7: Q16 (6 groups) × Q19 (4 groups)

**Files**: `2026-07-25-browsy-keys-trust-performance.md`
**Status**: Resolved — 4 groups wins

Q16 said 6 groups (3 defaults + 3 custom). Q19 said 4 groups (Close, Public, Private + 1 custom). Later decision supersedes earlier.

**Resolution**: 4 groups total, flat, no nesting. Q16 removed from decisions table. Q19 is authoritative.

### S7: Delegation in trust logic × v1 scope

**Files**: `2026-07-25-browsy-trust-logic-audit.md`, `2026-07-25-browsy-keys-trust-performance.md`
**Status**: Resolved — Delegation is v2

Trust logic spec included delegation as a core feature. Browsy plan says v1 = direct vouches only, no chains.

**Resolution**: Delegation, chain depth, key rotation all marked v2 in trust logic spec. v1 is direct vouches only. Friends list = Close group.

### S8: "Closest" naming × "Close" naming

**Files**: `browser-extension.md`, `2026-07-25-browsy-keys-trust-performance.md`, `2026-07-25-browsy-trust-logic-audit.md`
**Status**: Resolved — "Close" wins

browser-extension.md uses "Closest" (Q130-Q145, 8 references). Keys spec and trust logic spec use "Close". Later specs are authoritative.

**Resolution**: "Close" is the standard name. browser-extension.md references are historical, not updated.

### S9: Friends concept × Close group

**Files**: `2026-07-25-browsy-trust-logic-audit.md`, `2026-07-25-browsy-keys-trust-performance.md`
**Status**: Resolved — They're the same thing

"Friends" is the human term. "Close group" is the technical term. A friend = someone with a direct vouch relationship. The friends list IS the Close group member list.

**Resolution**: Friends section added to both specs. Friends = Close group, no separate data structure.
