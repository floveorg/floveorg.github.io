# Pendings

Punteros desde los docs: `↗ pendings:#N` (donde N es el ID).

**Interview de decisiones:** en `decisions.html` → entrada "Various — Design Decisions".

**Implementation plans & conflicts:** [`plans/index.md`](plans/index.md) · [`plans/conflicts.md`](plans/conflicts.md)

---

## Pending Items

### Banco Risa
- **BR03** Verificar `/setprivacy` → Disable en BotFather → unanswered (defer to Marc)
- **BR04** ~~Design `risa-banco-telegram-moderation-design.md` — pendiente revisión Marc~~ → ✅ Reciclado al estándar `risaliberada.md` (presentación v1) y retirado (2026-08-16)
- **BR05** ~~Banco Phase 1: swap `banco.json` a cross-origin Pages URL, vaciar placeholder seed, añadir QR code en modal~~ → ✅ Hecho (migración a R2 + `risa.json`; QR y deep link en el modal)

### Git History
- **GH01** Force push a GitHub si es necesario (reescritura de historia)

### Coming Soon (deferred)
- **CS01** Save app button in menús → repo download link (no implementar)

### Nety
- **N01** Reconcile nety master — diverge de GitHub (26+5 commits) → unanswered (defer to Marc)
- **N03** ~~Nety tagline en `flove-tiers-matrix.html`: "coming soon" → definir~~ → ✅ Coming soon (keep placeholder)
- **NF02** Mask data clearing — discussion in progress (needs deeper conversation)

### Architecture
- **ARCH01** MyNet trust computation: Python Central (FastAPI) for now, migrate to Rust Nety later
- **ARCH02** Browser Extension + Central = CORE; Decentral Nety = P2P distributed computation only
- **ARCH03** Repo structure: `central/` + `decentral/` (nety is sub-folder)
- **ARCH04** No fixed first-6 — the canonical set is whatever `central/` holds today (Q007, 2026-08-01); rewrite-from-scratch TBD per app
- **ARCH05** Decentral Nety repo: create `decentral/` with nety as sub-folder
- **ARCH06** ~~Nety ↔ Central authority~~ → ✅ Nety is authoritative (Q197)
- **ARCH07** ~~Decentral → Central data flow~~ → ✅ Nety pushes all public data to Central (Q200)

### Validación & Pulido
- **V03** Workflow de mantenimiento por tiers

### Worldview
- **W01** Dump Whole → worldview §3

### Tiers & Builds
- **T02** Super tier placeholder in-development
- **T03** Mega tier reserved, not featured yet
- **T04** Nano/mega not yet authored
- **T06** ~~Sound-depth control pending a new design~~ → ✅ Volume slider
- **T07** ~~Narrativa/Films axis → standard del tier Super~~ → ✅ Interactive storytelling

### Backend & Export
- **BE02** ~~Publish.md: "more" publish mode placeholder para nety·0asis~~ → ✅ API integration
- **BE03** ~~Coordinates.md: flove-quality measure, Tiers >5, Gitea↔docs sibling rule~~ → ✅ Defer until core features complete
- **CB_S10** Rating widget + puzzy integration — defer to design puzzy more appropriately first

### Designs Pendientes
- **DS01** ~~`flove-pwa-installable-design.md` — pendiente plan de implementación~~ → ✅ Simple install prompt
- **DS02** ~~`flove-private-addon-login-encryption-design.md` — pendiente plan de implementación~~ → ✅ OAuth integration
- **DS03** `appy-advanced-athenea-desk.md` — Tasks 6 (wizy.html), 7 (sety.html), 8 (making-of.html)
- **DS04** `appy-intros-rainbow-roadmap-design.md` — features-intro stubbed, nav location TBD

### Android / APK
- **APK01** Android SDK no instalado — necesario para `bubblewrap build`

### Otros
- **O01** Actualizar MEMORY.md con cambios recientes
- **O02** Propagate Ken Burns minivideo animation to all apps caption sliders (goddy done as template)
- **O03** ~~Browser extension decisions pending: BE07, BE09~~ → ✅ Resolved (Q194–Q204: interoperability & conflict resolution)

### Questy Session 2026-07-29 — Central standards review
- **PEN001** App datafields schema — develop per-app data schemas before defining collect() validation (blocked on Q010)
- **PEN002** collect() POST wire format — define request/response shape for /api/{app}/save (Q013)
- **PEN003** API contract completeness — document error response schema, auth header spec, rate-limit behavior (Q016)
- **PEN004** postMessage race — define polling or event contract for window.flove availability (Q017)
- **PEN005** Contract tests — write test suite verifying browsy bridge window.flove shape (Q018)
- **PEN006** Version negotiation — define min-version field for browsy↔Central compat checking (Q019)

### Context repo sweep 2026-07-31 — pendings ported from `~/Documents/context` (deleted)
- **STM01** Auth & System states (Login / Error page) rows of the tier matrix are **first drafts — open for Marc to refine** (2026-06-12 spec §4.11 · `flove-tiers-matrix.html` cols `Flows & States`). super = "account login (web-of-trust)", mega = "orchestrated auth".
- **STM02** Formal-register surfacing (the tier's technical term shown when the **Formal** labeler is active) — re-verify against the labeler implementation (2026-06-12 spec §4.1).
- **ENR01** SoloRich enrichment never landed on `main` — `flove-loader.js` + `flove-loader-check.py` + markers on 47 apps existed only on the deleted `central/solo` branch (commits `4f6ba5a`/`6303195`). **Resolved 2026-07-31** — moved to `main`: `central/shared/js/flove-loader.js`, `central/shared/scripts/flove-enrich.py` + `flove-loader-check.py`, shared lib at `central/shared/` (css/ + js/). Redesigned as **browsy-gift gated** (CA45-CA48, `plans/shared-code.md`): pro-enrichment loads only on a browsy reputational gift (score ≥ `flove:gift-min`, default 40). PoC: `solo/apps/blogy/blogy-super.html`. Repo-wide rollout (run `flove-enrich.py`, then `flove-loader-check.py`) is the pending remainder.

### Questy Session 2026-08-01 — central-first reorganisation
- **CEN01** Central apps i18n — deferred until the central apps are stable (Q010)
- **CEN02** Gitea backup/mirror — no backup exists yet; single-machine `origin` (Q018)
- **CEN03** Keystore backup — `~/flove-apk/android.keystore` is never committed; back it up off-machine (Q019)

---

## Resolved (archived)

> Merged 2026-08-01 from `pending-questions.md` (deleted). All resolved
> questions live in the plans that made them; next milestone is the JSON distro
> (routing.json + metadata + trusty cleanup + app links).

**Where resolved questions are documented:**
- `plans/browser-extension.md` (BX01-BX10, BF01-BF14, BL01-BL11, BA01-BA03, BD01-BD29)
- `plans/central-backend.md` (CB01-CB40, CB_S01-CB_S10, CA01-CA03)
- `plans/nety-frontend.md` (NF01-NF10, NP01-NP02)
- `plans/nety-trust.md` (NT01-NT10, TV01-TV02)
- `plans/conflicts.md` (conflict resolutions)
- `standards/persistence.md` (CC01)

**Standardisation candidates (2026-06-12 spec §6 — "still open") → all resolved:**

Portado desde `~/Documents/context` (eliminado 2026-07-31). Los cuatro
candidatos que quedaban "open" ya están estandarizados en `standards/`:

- **Color · tokens · theming** → `standards/contract.md` §2 (token discipline,
  surface palette light/dark) + `standards/frontend.md` §13.14 (contrast · theme
  switcher `flove:theme`) + §13.16 (CSS pattern catalog, tiered CSS imports,
  stacking/panel tokens).
- **Surfaces axis (2D → 3D/AR/VR)** → `standards/frontend.md` §13.11.
- **Onboarding paso-a-paso per tier** → `standards/frontend.md` §13.6.
- **Forms-in-iframe (newlabeler · newwizard · newlanguage · newsound)** →
  `standards/frontend.md` §13.3.
