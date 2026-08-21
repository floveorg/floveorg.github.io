# Review: Browsy + FastAPI + libSQL — Standards & Plans

> 2026-07-25. Audit of all browsy, Central, and shared-code plans through the lens of performance, consistency, and build-readiness.

## The Architecture (What's Decided)

**Browsy** (browser extension) is the **CORE navigation layer**. **Central** (FastAPI + Turso/libSQL) is the **data bank** that enriches it. Three layers total:

```
browsy (extension, local trust)  →  Central (FastAPI+Turso, cloud sync)  →  Nety (P2P extension)
```

Key specs: 50MB storage / 100MB memory / 1% CPU idle budget. 3-hop web of trust, 100 users LRU in IndexedDB (~1.2MB). libSQL everywhere (SoloRich local WASM + Central remote Turso). CRDT-based conflict resolution.

### Key Clarifications (from Marc, 2026-07-25)

1. **Solo vs Central are different code.** Solo(Rich) files are NOT the same code as Central — only names are preserved. Solo stays frozen or low-development when Central/Decentral evolve. Solo is for `file://` use, not for local server use.
2. **WASM needs headroom.** Other features must save latency and memory so WASM can run ok. If WASM is too heavy, document alternatives — don't force it.
3. **Unify local persistence.** Browsy storage across 4 APIs (IndexedDB, Extension storage, localStorage, sessionStorage) must be harmonized into a single approach.
4. **CRDTs for conflict resolution.** Adopt CRDT-style merge for trust data (Alternative 2 accepted).
5. **H4 resolved.** Split `central/` into `central/backend/` and `central/apps/` folders.
6. **Trust sync = separate endpoint.** Don't batch trust with profile/app data.
7. **Per-app schema validation.** Validate against `collect-schemas.json` on the server.
8. **Document WASM footprint.** Measure and publish actual numbers.
9. **Versioned ping.** `/api/ping` returns server version + feature flags.
10. **Trust sync protocol.** Define payload shape, conflict strategy, merge behavior explicitly.
11. **Centralize browsy storage.** Use Extension storage everywhere for browsy.
12. **Schema versioning.** `collect-schemas.json` gets a `schema_version` field.
13. **MV3 WASM pre-cache.** Document how WASM binary stays cached across service worker restarts.

## Sources Reviewed

| File | Lines | Focus |
|------|-------|-------|
| `plans/browser-extension.md` | 865 | Browsy features, sync, trust tiers, identity model |
| `plans/central-backend.md` | 311 | FastAPI endpoints, Turso/libSQL, deployment, identity |
| `plans/shared-code.md` | 152 | Enrichment loader, DB abstraction, flove.js |
| `plans/nety-frontend.md` | 105 | Nety tabs, mask system, MyNet architecture |
| `plans/standards.md` | 139 | Distro strategy, SD18, enrichment contract |
| `plans/conflicts.md` | 149 | Cross-plan tensions, H1-H6, S1-S6 |
| `standards/persistence.md` | 139 | Storage tiers, budgets, eviction, compression |
| `standards/adoption.md` | 110 | Distro matrix, Central+Browsy=CORE |

---

## Strengths

1. **libSQL Everywhere (C4)** — One API across SoloRich/Central/Decentral means `@libsql/client` works locally (sql.js WASM + OPFS) and remotely (Turso HTTP). SoloRich→Central migration is just changing a connection string.
2. **Offline-first trust** — browsy computes trust locally, Central enriches when online (H6). No trust computation depends on network.
3. **Progressive identity** — Device UUID → email claim → future OAuth. No friction at install, no lock-in.
4. **Minimal API surface** — 4 endpoints (`save`, `put`, `delete`, `list`) with cursor pagination. Simple enough to implement fast.
5. **CSP-safe enrichment** — `flove-loader.js` is external, no `'unsafe-inline'`. Silent failure preserves Solo mode.

---

## Cons & Risks

### 1. WASM in the Browser is Heavy
**Problem:** `@libsql/client` loads sql.js WASM (~1-2MB) on first `flove.db` call. In a browser extension context this adds latency and memory pressure against the 100MB/1% CPU budget.

**Where it hurts:** Every SoloRich app pays this cost on first DB operation. The lazy init (CA40) helps but doesn't eliminate the cold-start hit.

### 2. IndexedDB vs Extension Storage Confusion
**Problem:** The plan splits browsy data across IndexedDB (trust scores, profiles), Extension storage (webhook configs), localStorage (export history), and sessionStorage (panel state) — four different APIs with different limits, different persistence semantics, and different eviction behaviors.

**Where it hurts:** Complex code paths for what should be simple reads/writes. Debugging storage issues becomes nightmare. The "user-managed" 100MB limit (BL01) has no enforcement mechanism documented.

### 3. Last-Write-Wins Conflict Resolution is Fragile
**Problem:** CB32 + BF03 both decide last-write-wins by client timestamp. But clock skew exists (Q195 accepts the risk). Two devices editing the same trust vouch within a 5-minute window will silently lose one update.

**Where it hurts:** Trust data is the CORE of browsy. Silent data loss in the trust graph is worse than showing a conflict.

### 4. Railway Monorepo Deploy Ambiguity (H4 — Still Open)
**Problem:** `central/` branch contains both FastAPI backend (needs Railway deploy) AND modified app files (needs flove.org deploy). H4 in conflicts.md is explicitly "Open — deploy pipeline needs to distinguish backend changes from app changes."

**Where it hurts:** A single PR could break both the API and the frontend with no way to test them independently.

### 5. No Rate Limiting Until Post-PoC (CB37)
**Problem:** Zero rate limiting initially. While CB37a plans per-IP 100 req/min later, the PoC window is exploitable. Any script can POST unlimited data to Turso.

### 6. 1MB Payload Limit (CB_S01) May Be Too Low
**Problem:** Web of trust at 3 hops is ~1MB. Profile data is ~100KB. If browsy pushes full trust graph + profile + app data in one sync, it hits the limit immediately.

### 7. No Offline Queue for Central (CB33)
**Problem:** "No queue, no auto-retry for Central" — changes are lost if the user edits while offline. The `flove:pending-sync` flag (CB_S03) just tells the button to show a count, but there's no actual queue backing it.

### 8. WASM Pre-caching in sw.js (D09) Has Browser Extension Tension
**Problem:** Browser extensions have their own caching model. Service workers (MV3) and extension storage don't mix cleanly. Pre-caching WASM in sw.js may not work from the extension context.

### 9. 5-Minute Sync Batching is Arbitrary
**Problem:** BF01 + BE20 decide 5-minute batched sync. But trust changes are real-time (Q210). The plan says "batched 5 min + real-time for trust changes" — but the trust sync mechanism isn't specified beyond this sentence.

### 10. No Server-Side Validation of Data Shape (D06)
**Problem:** "Validate `data` is valid JSON, `user` is non-empty string" — that's it. No per-app schema validation. A malformed trust vouch POSTed by a buggy browsy version gets stored permanently (D01: no TTL).

---

## Alternatives (with Pros/Cons)

### Alternative 1: WASM Local Persistence — sql.js vs wa-sqlite vs IndexedDB wrapper

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

### Alternative 2: CRDTs for Trust Conflict Resolution (ACCEPTED)

| | Pros | Cons |
|---|------|------|
| **Vector clocks** | Eliminates clock skew risk, causally ordered | ~20% storage overhead per vouch entry, more complex merge logic |
| **Yjs integration** | Battle-tested CRDT, handles concurrent merges natively | ~100KB additional WASM/library, adds dependency |
| **Custom CRDT** | Minimal overhead, tailored to trust model | Must implement and test merge correctly, no community support |

**Decision:** Start with custom vector clocks (low overhead, trust-specific). Evaluate Yjs if the merge logic becomes complex. CRDT merge happens client-side (browsy); server stores merged result.

### Alternative 3: Central Directory Split (ACCEPTED — resolves H4)

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

### Alternative 4: Turso Embedded Replicas (FUTURE — when Turso Database is stable)

| | Pros | Cons |
|---|------|------|
| **Embedded replicas** | Zero WASM cold-start (native SQLite file), reads in microseconds, writes replicate to cloud | Requires Turso Database (beta), not available today, Rust-only server |
| **Current WASM approach** | Works today, no Turso dependency, full SQLite in browser | Cold-start latency, memory pressure, OPFS browser support varies |

**Decision:** Defer to CentralRich phase. WASM is the v1 path. Embedded replicas are the v2 path when Turso Database stabilizes.

### Alternative 5: Event-Driven Sync (ACCEPTED — replaces 5-min batching)

| | Pros | Cons |
|---|------|------|
| **chrome.alarms** | Trust syncs immediately, profile syncs on idle, battery-friendly | Requires `alarms` permission, more complex scheduling logic |
| **5-min batch** (current) | Simple, predictable, easy to debug | Trust changes delayed up to 5 min, arbitrary interval |
| **WebSocket push** | True real-time, server→client push for notifications | Requires persistent connection, server scaling complexity, battery drain |

**Decision:** `chrome.alarms` for browsy. Trust changes = immediate push. Profile/app data = sync on idle (no arbitrary timer). WebSocket deferred to CentralRich when server infrastructure supports it.

### Alternative 6: Unified Browsy Storage — Extension storage vs IndexedDB vs Hybrid

| | Pros | Cons |
|---|------|------|
| **Extension storage only** | Synchronous API, persistent, same 10MB quota in MV3, simple | 10MB limit (enough for browsy's ~1.2MB trust data), no structured queries |
| **IndexedDB only** | Structured queries, 50-200MB quota, async | Async API adds complexity, different persistence semantics per browser |
| **Hybrid (current)** | Best tool per data type | 4 APIs = 4 code paths, debugging nightmare, inconsistent eviction |

**Decision:** Extension storage for browsy (trust, profiles, webhook configs, panel state). It's persistent, synchronous, and 10MB is plenty for browsy's ~1.2MB working set. IndexedDB stays only for apps that need structured queries (nety circles).

---

## Suggestions

### High Priority

1. **Resolve H4 now.** The open deploy conflict will block Central from going live. Split the directory structure before building anything.
2. **Add a real offline queue for Central.** The `flove:pending-sync` flag is a boolean, not a queue. Use IndexedDB to store pending operations as an ordered log, replay on next connectivity check.
3. **Implement trust sync as a separate endpoint.** Don't batch trust with profile/app data. Give trust its own `POST /api/trust/sync` with immediate processing and conflict detection at the vouch level.
4. **Add per-app schema validation to Central.** At minimum, validate required fields per `collect-schemas.json`. Reject and log malformed data instead of storing garbage permanently.

### Medium Priority

5. **Document the WASM memory footprint.** Add actual measurements: sql.js init time, memory usage, OPFS write latency on Chrome/Firefox. The 100MB budget is a guess without numbers.
6. **Consider wa-sqlite as sql.js replacement.** Smaller WASM, same API surface, better async support.
7. **Add a `GET /api/ping` health endpoint that also returns server version.** Current ping just confirms Central is available. Adding version lets browsy know what features are supported (e.g., trust sync endpoint existence).
8. **Define the trust sync protocol explicitly.** "Batched 5 min + real-time for trust changes" is not a protocol. Specify: what payload shape, what conflict detection, what merge strategy, what happens when the trust graph exceeds 1MB.

### Low Priority (Polish)

9. **Centralize browsy storage into fewer APIs.** Use Extension storage for everything browsy-related (it's persistent, synchronous, and has the same quota as IndexedDB in MV3). Remove the IndexedDB/localStorage/sessionStorage split.
10. **Add a `collect-schemas.json` version field.** Per D06, the server accepts any schema. Add a `schema_version` field so browsy can detect if its schema is stale and prompt the user.
11. **Document the WASM pre-cache behavior in MV3.** Service workers in MV3 have limited lifetime. Explain how WASM binary stays cached across service worker restarts.

---

## Open Questions Requiring Answers Before Build

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

## Further Questions (from Marc's Replies)

These questions arise from Marc's clarifications and need answers before implementation.

### Solo Freeze & Migration

| # | Question | Context |
|---|----------|---------|
| FQ01 | When exactly does Solo stop receiving feature updates? Is it frozen at current state, or does it get security patches only? | Solo is for `file://` use, Central evolves separately |
| FQ02 | Does the enrichment loader (`flove-loader.js`) still need to support Solo, or does Solo ship fully self-contained with no external deps? | If Solo is frozen, loader may not need Solo path |
| FQ03 | What happens to Solo users when Central is live? Is there a migration path, or are they separate audiences forever? | Solo = `file://` users, Central = `flove.org` users |

### WASM Budget & Alternatives

| # | Question | Context |
|---|----------|---------|
| FQ04 | What's the maximum acceptable WASM cold-start time? 100ms? 500ms? 1s? | "Save latency and memory from other features for WASM to run ok" |
| FQ05 | What's the WASM memory ceiling during init? 10MB? 20MB? Needs to fit within 100MB total budget | Other features must yield memory |
| FQ06 | Should browsy defer non-essential features (discovery scoring, notification badge) until WASM is loaded? | Feature scheduling to protect WASM init |
| FQ07 | If WASM fails to load, does the app fall back to localStorage only, or does it show an error? | Silent fallback is current plan — is that still ok? |
| FQ08 | Is wa-sqlite worth evaluating now, or only if WASM budget is exceeded? | "Document alternatives to it" — when to actually switch? |

### Unified Storage

| # | Question | Context |
|---|----------|---------|
| FQ09 | Is Extension storage the definitive unified API for browsy? Or is IndexedDB still needed for structured queries? | "Definitely harmonize, unify" |
| FQ10 | What's the migration path from existing IndexedDB data to Extension storage? One-time export/import on update? | Current users have trust data in IndexedDB |
| FQ11 | Does Extension storage support binary data (ArrayBuffer) for compressed trust graphs? | gzip-compressed JSON needs binary write |
| FQ12 | What happens to `sessionStorage` usage (panel state)? Is that truly ephemeral, or should it also move to Extension storage? | Panel state = P1 (session), does it need persistence? |

### CRDT Conflict Resolution

| # | Question | Context |
|---|----------|---------|
| FQ13 | Which trust fields need CRDT merge? All fields, or only timestamps and trust levels? | "Alternative 2 to implement unified yes" |
| FQ14 | Does CRDT merge happen in browsy (client-side) or in Central (server-side)? | Affects server complexity |
| FQ15 | What's the CRDT overhead per vouch entry? How much does vector clocks add to the ~200B/entry budget? | "Save memory" — CRDT adds metadata |
| FQ16 | Should non-trust data (profile, app data) also use CRDTs, or only trust? | Trust is CORE, but profile conflicts also exist |
| FQ17 | How does CRDT merge interact with the 1MB payload limit? Does CRDT metadata push us over? | Trust graph is already ~1MB |

### Central Directory Split

| # | Question | Context |
|---|----------|---------|
| FQ18 | Does `central/shared/` contain only `libs/`, or also `apps.json` and `collect-schemas.json`? | Both deploy pipelines reference these |
| FQ19 | Can a single PR touch both `backend/` and `apps/`, or must they be separate PRs? | "Create backend/ and apps/ folders in central/" |
| FQ20 | How does Railway detect changes in `backend/` only? Path filter in `railway.toml`? | Avoids redeploying on app-only changes |
| FQ21 | Does `central/shared/` deploy to flove.org, or is it bundled into both `backend/` and `apps/`? | Shared libs availability |

### Trust Sync Protocol

| # | Question | Context |
|---|----------|---------|
| FQ22 | What's the trust sync endpoint shape? `POST /api/trust/sync` with what body? | "Trust as diff sync endpoint, yes" |
| FQ23 | Does trust sync use delta (only changed vouches) or full graph replacement? | Affects payload size vs complexity |
| FQ24 | What happens when trust graph exceeds 1MB? Truncate oldest? Paginate? Reject? | 1MB limit (CB_S01) vs 3-hop graph ~1MB |
| FQ25 | Does browsy push trust to Central, or does Central pull from browsy? | Direction affects latency and offline behavior |
| FQ26 | Can trust sync happen without a full profile sync, or are they coupled? | Trust is real-time, profile is batched |

### Per-App Schema Validation

| # | Question | Context |
|---|----------|---------|
| FQ27 | What's the validation error behavior? Reject + return error, or store + log warning? | "Add per-app schema validation yes" |
| FQ28 | Does `collect-schemas.json` define required fields, types, or full JSON Schema? | Affects validation complexity |
| FQ29 | Who maintains `collect-schemas.json`? Auto-generated from app code, or manually maintained? | Staleness risk if manual |
| FQ30 | Does schema validation apply to trust sync endpoint too, or only app data? | Trust has its own endpoint |

### Versioned Ping

| # | Question | Context |
|---|----------|---------|
| FQ31 | What features does `/api/ping` advertise? Version number, feature flags, or capability list? | "Add ping with version yes" |
| FQ32 | Does browsy cache the ping response, or re-check on every load? | Current: cache in localStorage for session |
| FQ33 | What happens if Central is downgraded (version goes backward)? Does browsy handle it? | Edge case for feature detection |

### MV3 WASM Pre-Cache

| # | Question | Context |
|---|----------|---------|
| FQ34 | In MV3, does the service worker cache WASM, or does the extension storage cache it? | "Document WASM pre-cache behavior in MV3" |
| FQ35 | MV3 service workers terminate after 30s idle. Does WASM survive termination? | WASM binary needs to survive SW restarts |
| FQ36 | Is WASM pre-caching even necessary if lazy init (CA40) already loads on first use? | May be premature optimization |
