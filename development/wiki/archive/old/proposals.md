# Proposals — flove central

> **Scope / Ámbito:** EN: Historical snapshot of the questy central proposals — decisions, plan status and open items. · ES: Instantánea histórica de las propuestas centrales de questy — decisiones, estado de planes y temas abiertos. Live state: [`pendings.md`](pendings.md) and [`plans/index.md`](plans/index.md). Generated 2026-07-29; last revised 2026-11-15.

## Active proposals

| ID | Title | Plan | Status |
|----|-------|------|--------|
| P01 | Central backend (FastAPI + Turso + Railway) | `plans/central-backend.md` | Design complete — ready to build |
| P02 | Browsy extension (Ed25519 bridge) | [`browsy/spec.md`](browsy/spec.md) | ✅ Active specification (2026-11-17) |
| P03 | Nety frontend (tabbed app, masks, MyNet) | [`browsy/spec.md`](browsy/spec.md) | ⏹ Retired; MyNet lives in Appy/Browsy |
| P04 | Nety trust (ranking, curators, abuse) | [`browsy/spec.md`](browsy/spec.md) | ⏹ Retired; Browsy trust is local |
| P05 | Shared code (enrichment loader, DB abstraction) | — | ⏹ Retired (2026-11-15); apps are self-contained |
| P06 | Standardisation (tokens, testing, mobile, i18n) | `plans/standards.md` | Ready to build |
| P07 | JSON distro (routing, metadata, build pipeline) | `backend.md` §10.3e | ✅ `tools/routing.json` vivo (`flove-routing/3`) + `extract-fields.py` |
| P08 | Puzzy engine (aggregation, compute) | `plans/puzzy.md` | Ready to build |
| P09 | Trusty cleanup (SIGNALS removal, app links) | — | ✅ Done (links added) |
| P10 | Docs infrastructure (theme, nav, search) | `development/standards/` | ✅ Implemented |
| P11 | Browsy-less fallback (localStorage stub mode) | questy Q007 | Ready to design |
| P12 | Decentral Nety repo (Rust stubs) | questy Q008 | Ready to build |
| P13 | Claim flow (warn at first sync, reclaim via authy) | questy Q015, Q025 | Ready to design |
| P14 | Central split (`backend/` + `apps/` + `shared/`) | `plans/conflicts.md` H4 | ✅ Implemented 2026-08-01 |
| P15 | Central download package (dual-package; solo as optional fallback) | questy 2026-08-01 Q002 | Ready to design |
| P16 | Backends overview (Central · Decentral · Browsy) | `backend.md` | ✅ Implemented 2026-08-01 |
| P17 | Publish-web.sh relocation (out of the distro folder) | `development/standards/scripts/` | ✅ Implemented 2026-08-01 |

## Resolved decisions

- **Architecture**: Central = data bank + frontend; Browsy = main nav + identity/trust bridge
- **Storage**: libSQL (`@libsql/client`) everywhere — same engine across SoloRich, Central, Decentral, DecentralRich
- **Identity**: Ed25519 keys via Browsy bridge API (`window.flove.browsy.identity.*`)
- **Trust**: 4 groups (Close, Public, Private + 1 custom), direct vouches only in v1, delegation deferred to v2
- **URL hierarchy**: Central URLs become primary; Solo URLs maintained on main as fallback
- **Deploy**: Railway CI watches `backend/` only; GitHub Pages CI watches `apps/` only; `shared/` bundled into both
- **Conflicts**: All 10+ cross-plan tensions resolved (see `plans/conflicts.md`)
- **Solo status**: Fallback reference only, **low-maintenance (not frozen)**, no retirement plan (Q001, Q004, Q016)

### Trunk polish 2026-11-15 — self-contained apps, no tiers

- **Campos completos**: los 48 apps con fuente declaran su árbol `flove-fields/1`
  (0 `partial`); `tools/extract-fields.py --check` lo reproduce en `routing.json`
  (`flove-routing/3`).
- **Protocolo de retrato**: `flove-portrait/1` con adaptador real en Souls,
  Goddy, Realy, Inventary, MyFamily, PracSys, Keys, Crafty, Worthing, Lovy y
  Puzzy; `flovePort` como fachada (`floveNet` alias deprecado).
- **Autosuficiencia**: `floveStore`/`floveFields`/`flovePort` inline en cada app;
  `addons/code/` es copia de referencia, nunca se carga. Sin `src=`
  externos salvo el `vendor/leaflet/leaflet.js` local de Freed.
- **Tiers fuera del trunk**: stepper de Puzzy, `data-tier`, `tier-locked`,
  `tier-pop` de `flove.js`, tiles/cubos de Blogy en el catálogo y metas
  `flove:tier` de la distro central eliminados. Los variantes mini→super quedan
  como demo en `apps/blogy/`, `apps/economy/dealy/`, `apps/puzzy/keys/` y
  `apps/appy/`.
- **Poda**: CSS muerto fuera en Fivy/Raty/Socy; cláusulas, raters, labelers y
  mazos generados desde datos en Dealy/Raty/Blogy/Fivy/Souls.

### Questy survey 2026-08-01 — central-first reorganisation
- **Dual packages**: Solo keeps its own download package; Central gets its own (central-first); the central package downloader may offer solo as an optional fallback (Q002)
- **central/dev retired**: refs fixed to `development/standards/`; the standards book lives there (Q003)
- **Backends overview**: `backend.md` = all backends (Central FastAPI · Decentral nety · Browsy); deep Central spec in `plans/central-backend.md`; canonical development = `central/apps/` (Q006)
- **Canonical set**: no fixed first-6 — the canonical set is whatever `central/` holds today (Q007)
- **Central split**: `central/` split into `backend/` + `apps/` + `shared/` — implemented 2026-08-01 (Q008, H4)
- **Browsy-less stub**: design + test stub mode before central apps ship (Q009)
- **Publish-web.sh**: moved out of the distro folder to `development/standards/scripts/` (Q011)
- **Enrichment scope**: pro-enrichment targets central apps only (Q012) → ⏹ retirado del trunk (2026-11-15): ninguna app carga la librería; la capa común va inlineada.
- **Sequencing**: structure first (split + overview), then package builder, then stub (Q014)
- **Publish security**: status quo kept (deny-list + gitignore, no new guard) (Q015)
- **sw.js**: regenerate + bump cache version in the same commit as the split (Q017)
- **Split checks**: automated checks before commit — grep old-path refs, verify internal links, local serve test (Q020)
- **Questy decisions**: Exported survey HTML → `decisions.html` (Q002)
- **central/ sync**: Auto-push to Gitea + GitHub on every commit (Q006)
- **Browsy fallback**: localStorage stub mode when extension not installed (Q007)
- **Decentral repo**: Create `decentral/` now with nety sub-folder, Rust stubs (Q008)
- **Shared libs**: Never diverge — same version for all consumers (Q009)
- **Solo/Central separation**: Different origins to avoid localStorage collision (Q011)
- **Central export**: NDJSON sufficient — no 6-format pipeline needed (Q012)
- **Trust CRDT**: Per-field merge with vector clocks (Q014)
- **Claim-or-lose**: Warn user at first sync before orphaned data (Q015, Q024)
- **Trust identity**: Per-device, email binds one account, Telegram allows many (Q022)
- **Reclaim**: via authy — p2p network + email + Telegram (Q025)

## Open items

- Central logging — basic vs file logging deferred
- ~~Per-app collect() schema validation — blocked until app datafields are defined (PEN001)~~ → ✅ Resolved 2026-11-15: every app with a source declares its `flove-fields/1` tree in `tools/routing.json` (`extract-fields.py --check` passes; 0 `partial`). What remains is the *contract test* (PEN005).
- Social curation bundles with contrast — deferred to DecentralRich
- WASM/libSQL preloaded bundled selections — not in PoC
- SoloRich enrichment not on `main` — loader+markers only ever lived on the deleted `central/solo` branch (ENR01, `pendings.md`)

## Pending questions

See `pendings.md` for unresolved items:
- BR03: `/setprivacy` verification in BotFather
- N01: Nety master reconciliation with GitHub
- NF02: Mask data on browser clear
- ~~PEN001: App datafields schema needed before defining collect() validation~~ → ✅ Done 2026-11-15 (see `pendings.md` §Resolved)
- PEN002: collect() POST wire format to define
- PEN003: API contract completeness (errors, auth, rate-limit)
- PEN004: postMessage vs window.flove race handling
- PEN005: Contract test suite for browsy bridge
- PEN006: Version negotiation between browsy & Central apps
