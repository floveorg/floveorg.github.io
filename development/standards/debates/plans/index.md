# Plans Index

> Implementation plans derived from interview decisions and pending questions.
> Each plan documents decisions, architecture, tasks, and cross-plan conflicts.
> Updated 2026-07-23 with CA01-CA44 + CB01-CB40 + C01-C76 + D01-D23 + E01-E25 + G01-G55 (Central backend, Turso, serverless Railway, anonymous identity, libSQL everywhere, strategic architecture, Central nav, Nety-Central bridge, profile mirror, error responses, CORS staging, rate limiting post-PoC, schema migration, first 6 apps, rating widget, bottom nav visual spec).

## Active plans

| Plan | Source decisions | Status |
|------|-----------------|--------|
| [nety-frontend.md](nety-frontend.md) | Tabbed app, masks F2, social=MyNet | Ready to build |
| [nety-trust.md](nety-trust.md) | Ranking (×3 bonus), curators (+report), abuse Tier 1 | Ready to build |
| [docs.md](docs.md) | Theme, nav, search, content, contributing, support | Ready to build |
| [JSON distro → `../backend.md` §10.3e](../backend.md) | JSON distro schema, routing.json, build pipeline (merged from `plans/backend.md`, deleted 2026-08-01) | Ready to build |
| [shared-code.md](shared-code.md) | CA01-CA42 (enrichment loader, shared libs, Central detection, DB abstraction) | ✅ Implemented — 47 apps enriched |
| [central-backend.md](central-backend.md) | CB01-CB40 + C01-C76 + D01-D23 + E01-E25 + G01-G55 (FastAPI + Turso, serverless Railway, anonymous identity, libSQL everywhere, Railway monorepo, staging workflow, Nety-Central bridge, profile mirror, error responses, CORS staging, rate limiting post-PoC, schema migration, first 6 apps, rating widget, bottom nav visual spec) | Design complete — ready to build |
| [puzzy.md](puzzy.md) | Aggregation, compute | Ready to build |
| [standards.md](standards.md) | Tokens, testing, mobile, i18n, release checklist, SD18-SD19 distro strategy | Ready to build |
| [trusty-cleanup.md](trusty-cleanup.md) | SIGNALS removal, app links (evily/myfamily) | Ready to build (links added) |
| [browser-extension.md](browser-extension.md) | Browser extension for flove bridge, discovery, offline + latest decisions (2026-07-27): on-demand arch, crypto, storage, bridge API | Design complete — ready to build |
| [conflicts.md](conflicts.md) | Cross-plan tensions | Living document — all resolved |

## Browsy docs

Detailed browsy documentation lives in [`../browsy/`](../browsy/):

| Doc | What it covers |
|-----|---------------|
| [browsy/README.md](../browsy/README.md) | Architecture, decisions, data structures, file map |
| [browsy/TESTING.md](../browsy/TESTING.md) | Risk analysis, test matrices, crypto comparison |

## Feature matrix

**→ [Feature matrix](../features.md)** — all 59 implemented features (22 browsy backend + 37 central frontend) + 19 planned + 10 future = 88 total.

## Roadmap

**→ [Roadmap: Central + Browsy v1](roadmap-central-browsy-v1.md)** — consolidated build order from all plans. One document, one path to v1. Start here.

## Next milestone

**Central backend (design complete, ready to build)** — FastAPI + Turso on Railway (monorepo, two services), flove.js Central detection + sync, libSQL in browser with localStorage fallback. Build order: Railway backend first (deploy when API+tests pass) → flove.js Central module → first 6 Central apps (goddy, souls, pracsys, myfamily, inventary, realy, keys). Central URLs become primary; Solo URLs maintained as fallback.

**Pending enhancements (future):** Social curation bundles with contrast, test app for end-to-end pipeline, per-app collect() schema validation, localhost dev support.

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
