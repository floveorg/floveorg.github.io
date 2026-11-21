# Plans Index

> Implementation plans derived from interview decisions and pending questions.
> Each plan documents decisions, architecture, tasks, and cross-plan conflicts.
> Updated 2026-11-20 with CA01-CA44 + CB01-CB40 + C01-C76 + D01-D23 + E01-E25 + G01-G55 (Central backend, Turso, serverless Railway, anonymous identity, libSQL everywhere, strategic architecture, Central nav, Nety-Central bridge, profile mirror, error responses, CORS staging, rate limiting post-PoC, schema migration, first 6 apps, rating widget, bottom nav visual spec).
> 2026-08-16: absorbed the dated implementation plans (all moved here).
> 2026-11-17: consolidated the export/share/summary/conformance plans into the frontend standards and `../pendings.md`; moved the Browsy spec/rationale to `../browsy/`; removed completed and retired plans.

Task execution order is not a phase order: see
[`../README.md#task-order-proc-07`](../README.md#task-order-proc-07)
(PROC-07, Q127/Q141).

## Active plans

| Plan | Source decisions | Status |
|------|-----------------|--------|
| [Browsy spec-driven plan](../browsy/spec.md) | BSP-A/D/I/M/W/P/N/U/T — Browsy hosts Authy + Wizy, P/L/S classes, risa ladder, Telegram→MyNet, MyFamily records, Nety Social only | ✅ Active specification — supersedes browsy/nety/central plans in part |
| [JSON distro → `../../backend.md` §10.3e](../../backend.md) | JSON distro schema, routing.json, build pipeline (merged from `plans/backend.md`, deleted 2026-08-01) | Ready to build |
| [central-backend.md](central-backend.md) | CB01-CB40 + C01-C76 + D01-D23 + E01-E25 + G01-G55 (FastAPI + Turso, serverless Railway, anonymous identity, libSQL everywhere, Railway monorepo, staging workflow, Nety-Central bridge, profile mirror, error responses, CORS staging, rate limiting post-PoC, schema migration, first 6 apps, rating widget, bottom nav visual spec) | Design complete — ready to build |
| [2026-11-21-app-database-stages.md](2026-11-21-app-database-stages.md) | Stages `seed · infant · mature · grown · full` for app data; minimal model replicated from the Appy index `flove-profile`; first objective = migrate Goddy, Realy and Appy to stage `mature`; activation from Appy Privacy/MyNet/Activity (no separate Sety); embed + sys handoffs mapped to `plays`/`claims`; MyNet Backend tab with six hitos and 44 tasks across all stages; Chatland XMPP hitos across axes with a Docs → Work dependency map; nety-free app tests | Refining — living document |
| [puzzy.md](puzzy.md) | Aggregation, compute | Ready to build |
| [standards.md](standards.md) | Tokens, testing, mobile, i18n, release checklist, SD18-SD19 distro strategy | Historical — live status in Docs · Plan/Work |
| [conflicts.md](conflicts.md) | Cross-plan tensions | Living document — partly open |

## Roadmap at a glance

| Phase | Track | Deliverable |
|-------|-------|-------------|
| **F1** | JS distro | `mini` + `minifull` (local): persisted locally, summary = source of truth + Update, export "what you see"; `miniappy`/`minifull` aggregate your own summaries offline *(in progress)* |
| **F2** | JS distro | `basic` tier: query **MyWizy** (local AI) over your profile + punctual download of others' summaries |
| **F3** | nety (corporate) | Identity (Ed25519, flovenet keystore) + Publish button |
| **F4** | nety (corporate) | Common area: semantic search · whole-matrix · cross-link graph · feed (GraphQL) |
| **F5** | nety (corporate) | AI: **wizy** (module 42 = optional engine via the 0asis add-on) |
| **—** | integration demo | `routing.json` + Publisher adapter → `OasisPublisher` first, then ActivityPub / Matrix / Solid |

### Stage equivalence (Q109/Q114)

One ladder, one name: `stage`. The roadmap letters and the old feature ladder are aliases of these values, never a second scale.

| Stage | Roadmap alias | Retired ladder label | Meaning here |
|-------|---------------|----------------------|--------------|
| `seed` | F1 (F0 folds in) | Raw | JS distro · mini + minifull, local only |
| `infant` | F2 | Basic | basic tier + local MyWizy |
| `mature` | F3 | Normal | nety identity + Publish |
| `grown` | F4 | Advanced | common area + feed |
| `full` | F5 (Next folds in) | Super | wizy engine + full puzzy |


> **Work stages (2026-11-20):** this table is the narrative mirror.
> The canonical Plan/Work surface uses exactly five `stage` values; legacy F0/Next fold into the first and last. The 312 subsection milestones live in
> [Work](https://flove.org/development/index.html#work?tab=docs&view=r2&subtab=work&category=docs&section=plan).

Open questions (deferred): routing authoring (wiki vs curator) · AI fine-tuning
and compute · identity-mask timing · per-element visibility · typed vs untyped
cross-links.

## Trunk polish — 2026-11-14/17

| Plan | Scope | Status |
|------|-------|--------|
| [2026-11-14-app-tier-planned.md](2026-11-14-app-tier-planned.md) | app tiers in `routing.json` | ⏹ Not in this trunk — demos only |
| [2026-11-17-appy-authy-mynet.md](2026-11-17-appy-authy-mynet.md) | Authy levels → MyNet activation; portable `flove-auth/1`; web handoff + Browsy web of trust | 📝 Spec draft |

[`2026-11-19-authy-open-questions.md`](2026-11-19-authy-open-questions.md) is a
pointer, not a sixth plan: the A01–A13 questions are authoritative in
[`../browsy/browsy-questions.md` §A](../browsy/browsy-questions.md).

> **Historical → production standard (1.4c).** Superseded plans are not deleted:
> each keeps its file and points to the live
> [production standard](../README.md) (`contract.md` for rules, `README.md` for
> what exists) as the authoritative home. This index is the map, not the fact.
>
> **Consolidated 2026-11-17.** The export/share/summary/conformance plans were
> folded into the standards and deleted: `frontend/export.md`,
> `frontend/publish.md`, `frontend/summary.md` and the open items in
> [`../pendings.md`](../pendings.md) §Export / Share / Appy. The 10-step
> onboarding copy moved to [`../../apps/onboarding-copy.md`](../../apps/onboarding-copy.md).
> The completed fields and Souls audits were removed; their outcomes live in
> `tools/routing.json` and the app code.

> **Shared code (2026-11-15):** the browsy-gift enrichment loader is retired from
> the trunk. Every app inlines its own copy of the common layer
> (`floveStore`/`floveFields`/`flovePort`, and `flove.js`/`flove-appy.js`/
> `flove-theme.js`/`flove.css` where used); `addons/code/` is the
> reference set shipped in the offline package, never loaded at runtime. No app
> fetches shared code; the only external files are the frozen vendor
> fonts/icons and Freed's local `vendor/leaflet/leaflet.js`.

## App build plans (absorbed 2026-08-16)

Dated implementation plans absorbed here 2026-08-16; their design specs were archived 2026-11-19:

| Plan | Scope | Status |
|------|-------|--------|
| [2026-06-18-nety-frontend-build.md](2026-06-18-nety-frontend-build.md) | miniappy build + Phase A–D roadmap | Built & iterating — wizy/sety/profily pending |

## Browsy docs

Detailed browsy documentation lives in [`../browsy/`](../browsy/):

| Doc | What it covers |
|-----|---------------|
| [browsy/README.md](../browsy/README.md) | Architecture, decisions, data structures, file map |
| [browsy/spec.md](../browsy/spec.md) | Current spec: BSP requirements, phases, acceptance, extension standards |
| [browsy/rationale.md](../browsy/rationale.md) | Vision, data mesh, diagrams, alternatives and the 10 original questions |
| [browsy/browsy-questions.md](../browsy/browsy-questions.md) | Historical decisions + live questions A–L (2026-11-17) |
| [browsy/TESTING.md](../browsy/TESTING.md) | Risk analysis, test matrices, crypto comparison |
| [browsy/port-nety.md](../browsy/port-nety.md) | Crypto/storage seams and Nety port mechanics |
| [browsy/pre-build/README.md](../browsy/pre-build/README.md) | Pre-build contracts: MVP, Authy levels, schemas, MyFamily profile, native host, bridge, lineage |

## Next milestone

**Browsy · Authy · MyNet** — current spec
[`../browsy/spec.md`](../browsy/spec.md) and the active Authy/MyNet plan
[`2026-11-17-appy-authy-mynet.md`](2026-11-17-appy-authy-mynet.md). Authy is
L1–L5 (L3 Telegram verified, L4 phone, L5 bio), MyNet local and publishing both
open at L3, and Browsy is the host extension (pull → suggest → render). Central remains an
optional mirror/host.

**Pending enhancements (Deferred):** social curation bundles, an end-to-end
test app (demo e2e — Deferred, 1.6a), per-app `collect()` validation, and
localhost dev support.

## Pending items (deferred)

These were postponed during the design sessions and can be decided later:

| ID | Topic | Reason deferred |
|----|-------|----------------|
| C15 | blogy Central modifications (minimal vs full vs gradual) | Deferred — E04b decided to adapt blogy later after first 6 apps prove the pattern |
| C24 | Central logging (none vs basic vs file) | Operational detail — start with Railway logs, add file logging later |
| C37 | Localhost dev support | Web-first — Central designed for flove.org. Localhost deferred to CentralRich |
| D06c | Per-app collect() schema validation | Structural validation (valid JSON, non-empty user, ISO timestamp) is enough for proof-of-concept |
| — | Social curation bundles with contrast | Feature enhancement for DecentralRich — not in Central proof-of-concept |
| — | WASM/libSQL preloaded bundled selections | Feature enhancement — not in proof-of-concept |

## How to use this folder

1. **Before starting dev**: read `conflicts.md` to check for known tensions
2. **When answering a new interview question**: add the resulting plan to this folder
3. **When a plan changes**: update `conflicts.md` with new/resolved tensions
4. **Cross-reference**: each plan links back to the interview question and source spec
