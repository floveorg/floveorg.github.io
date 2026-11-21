# Pendings

> **Scope / Ámbito:** EN: Live issue register — a fallback referral mirroring the 75 pendings rows of the 438-item canonical register in Docs · Plan/Work; the other 363 items are 326 milestones, each under its own section\'s field (28 fields in total), plus 37 debate tickets. Milestone tasks and their `depends_on` chains live in `milestones.json`, ordered by the 6 canonical sections; the per-field task breakdown is in [`hitos-audit.md`](../archive/old/hitos-audit.md#fields-and-their-tasks) and is filterable in Work via `State` (`archived · fácil · difícil · muy difícil`). Historical decisions are in `plans/` and the archive. · ES: Registro vivo de incidencias — referencia de fallback que refleja las 75 filas de pendings del registro canónico de 438 ítems en Docs · Plan/Work; los otros 363 son 326 hitos, cada uno bajo el campo propio de su sección (28 campos en total), más 37 tickets de debate. Las tareas y sus dependencias viven en `milestones.json`, ordenadas por las 6 secciones canónicas; el desglose campo→tasks está en [`hitos-audit.md`](../archive/old/hitos-audit.md#fields-and-their-tasks) y se filtra en Work con `Estado / State` (`archived · fácil · difícil · muy difícil`). Las decisiones históricas están en `plans/` y el archivo.

Punteros desde los docs: `↗ pendings:#N` (donde N es el ID).

**Interview de decisiones:** entrada "Various — Design Decisions", reciclada abajo como `VARIOUS_Q01`–`VARIOUS_Q50`; el registro completo está en `archive/making-of/making-of.html`.

**Implementation plans & conflicts:** [`plans/index.md`](../archive/old/plans/index.md) · [`plans/conflicts.md`](../archive/old/plans/conflicts.md)

---

## Pending Items

### Hot

Optimize `development/index.html` (Plan/Work) load without risking navigation or filters (on-demand, externalized).

- Work data: runtime payload `flove-work/1` is compiled by `tools/dev/build-work-tracker.py` from `development/wiki/archive/old/milestones.json` + `pendings.md` and currently inlined as `#work-data` (~lines 1211–57050). Extract to a static asset (e.g. `development/data/work.json`, same schema), fetch + `JSON.parse` + init tracker only on `#work` / Work entry, then apply hash/filter state (`tab`, `subtab`, `q`, view/phase/type…). `milestones.json` stays the canonical source (not runtime-fetched); `--build/--check` must emit/validate the external artifact to avoid drift.
- Plan SVGs: `#dy-decentral-model` thread (~48 KB, line ~1177, inside hidden “See more”) duplicates `development/addons/media/apps/logos/central/decentral-model.thread.svg` — load/inject on panel open (or externalize) and consider SVGO. Tall `.seq` thread (~18 KB, ~line 100659) is a good lazy/external + SVGO candidate; other inline diagrams are smaller. Plan markup/fragments can be fetched on demand.
- Rollout/fallback: clone `development/index.html` → `development/index.legacy.html` (known-good inline). New slim `index.html` loads externals on demand; on fetch/parse/init failure fall back/link to `index.legacy.html` preserving `location.search + location.hash`. Phase 1: externalize + lazy-init Work; Phase 2: lazy-load heavy Plan SVG/fragments.

### Making-of open decisions (recycled 2026-11-19)

> Open questions recovered from the archived decision interviews. IDs are stable and feed the Work tracker (`source=standards`). Decided questions were already absorbed into standards/plans; the full record stays in `archive/`. No retired routes remain.

- **VARIOUS_Q01** What is the nety 'super' tier for? · nety, direction — ◇ Hybrid
- **VARIOUS_Q02** What shape does the real nety frontend take? · nety, frontend — ◇ Hybrid
- **VARIOUS_Q03** When are identity masks (multiple personae per user) needed? · nety, identity — ◇ F5 (late)
- **VARIOUS_Q04** What engagement ranking and anti-gaming mechanics does nety need? · nety, ranking — ◇ Defer
- **VARIOUS_Q05** How should nety curators be selected and held accountable? · nety, curators — ◇ Defer
- **VARIOUS_Q06** How should abuse adjudication work in nety? · nety, moderation — ◇ Defer
- **VARIOUS_Q07** ~~Is the social app standalone or integrated into MyNet?~~ → ✅ Integrated into MyNet (2026-11-20): Social is the MyNet tab (tab 3 of 5), not a standalone app; owner `browsy/spec.md` §3.4 / BSP-M16.
- **VARIOUS_Q08** Should vizy recover its XR/VR direction? · vizy, direction — ◇ Abandon VR
- **VARIOUS_Q09** Should trusty implement crumbly granular mode? · trusty, features — ◇ Defer
- **VARIOUS_Q10** What theming/branding approach for docs? · docs, theme — ◇ Always dark
- **VARIOUS_Q13** What theming/branding approach for docs? · docs, theme — ◇ Always dark
  - options: • Dark theme (manual toggle) — Default dark, user can switch to light. Standard approach, moderate code. · • Auto-detect system theme — Follow OS dark/light setting. No toggle needed, less user control. · • Both (toggle + auto) — Auto-detect with manual override. Most flexible, most code. · • Always light — No theming — always light. Simplest, but mismatches flove's dark aesthetic. · • Always dark — No theming — always dark. Matches flove, simplest, no toggle.
  - options: • Client-side full-text (lunr.js) — Self-contained search, works offline, adds ~50KB JS. Flove-first approach. · • Algolia DocSearch — Fast, hosted, free for OSS. External service dependency. · • Google site search — Easy to set up, external, requires internet. Simple but not flove-first. · • None (just nav) — No search — rely on good navigation and cross-links. Simplest.
- **VARIOUS_Q15** Should docs have cross-links between pages? · docs, navigation — ◇ Inline links in text
  - options: • Inline links in text — Natural hyperlinks within content. Best UX, organic discovery. · • Related-docs section — Explicit 'Related' block at the bottom of each page. Structured but rigid. · • Both — Inline + related section. Maximum discoverability, maximum maintenance. · • None — No cross-links — each page is standalone. Simplest.
  - options: • Sidebar — Persistent left sidebar with section links. Standard docs pattern, always visible. · • Top nav bar — Horizontal nav at the top. Cleaner, less space, but limited depth. · • Breadcrumbs — Path-based breadcrumbs at the top. Good for deep hierarchies, less for flat ones. · • None needed — No dedicated nav — just links in content. Simplest.
  - options: • Copy-paste snippets — Short, focused code blocks. Easy to scan, easy to copy. · • Full file examples — Complete HTML files users can download. More complete, heavier. · • None — No code examples — just prose. Simplest.
  - options: • Yes, contribution guide — Explain how to contribute — structure, style, PR process. Encourages community. · • No, Marc-only — Keep docs editing to Marc only. Simpler, more control.
  - options: • Email link — Simple contact form or mailto link. Direct, personal. · • GitHub issues — Public issue tracker. Transparent, searchable, but requires GitHub account. · • Both — Email for private, GitHub for public. Most flexible. · • None — No explicit support channel — users find Marc through the community.
  - options: • Scheduled reviews — Regular audits (quarterly). Proactive, catches drift early. · • On-demand only — Update when something breaks or changes. Reactive, less work. · • Both — Scheduled audits + on-demand fixes. Most thorough.
  - options: • Plugin system — Document how to build plugins/modules. Useful for developers, adds scope. · • Just standards — Document the standards only — no extensibility docs. Focused. · • Both — Standards + extensibility. Comprehensive but more work.
- **VARIOUS_Q22** How should routing.json be authored? · backend, routing — ◇ Marc-only
  - options: • Community wiki — Anyone can edit. Democratic, fast updates, risk of vandalism. · • Curator-only — Only curators can edit. Safe, slow, controlled. · • Automated (AI) — AI generates/maintains routing. Fast, unpredictable, hard to audit. · • Marc-only — Only Marc edits. Simplest, most control.
- **VARIOUS_Q23** Should cross-links be typed or untyped? · backend, cross-links — ◇ Untyped
  - options: • Typed — Defined relationship types (responds_to, derived_from). Richer querying, more schema. · • Untyped — Simple hyperlinks. Simpler, less metadata, still useful. · • Hybrid — Untyped by default, optional type annotation. Flexible.
- **VARIOUS_Q24** Should flove have per-app cube downloads? · backend, cubes — ◇ Defer
  - options: • Yes, per-app cubes — Each app gets its own zip. Users download what they need. Needs builder script. · • No, flove-localhost.zip only — One big bundle. Simpler, but larger download. · • Defer — Don't build yet — revisit when more apps exist.
- **VARIOUS_Q25** What AI fine-tuning approach for module 42? · backend, ai — ◇ Defer
  - options: • Full fine-tuning — Train entire model. Best quality, highest cost. · • LoRA — Low-rank adaptation. Cheaper, nearly as good, less control. · • No fine-tuning — Use base model as-is. Free, least customized. · • Defer — Don't decide yet — wait until module 42 is closer to shipping.
- **VARIOUS_Q26** What granularity for visibility controls? · backend, visibility — ◇ Hybrid
  - options: • Per-element — Each element has its own visibility. Maximum control, maximum complexity. · • 0asis defaults — Global defaults, no per-element override. Simple, less flexible. · • Hybrid — Default from 0asis, with per-element override option. Balanced.
- **VARIOUS_Q27** How should puzzy aggregate ratings from multiple people? · puzzy, aggregation — ◇ Defer
  - options: • Juxtaposition — Show all raters side by side. Transparent, but cluttered with many raters. · • Mean + dispersion — Statistical summary — average + spread. Clean, hides individual nuance. · • Toggle — User switches between juxtaposition and summary. Most flexible, more UI. · • Defer — Don't decide yet — wait until F3/F5 when puzzy ships.
- **VARIOUS_Q28** Where does the puzzy compute live? · puzzy, compute — ◇ Defer
  - options: • Client-only — All compute in the browser. Privacy-first, limited by device power. · • Module-42-only — Server-side compute. Powerful, centralized, requires trust. · • Hybrid with offline cache — Client-first, server fallback, offline cache. Balanced, complex. · • Defer — Don't decide yet — wait until F5.
- **VARIOUS_Q29** Should flove have an installable PWA button? · pwa, install — ◇ Defer
  - options: • Yes, in-app button — Custom 'Install flove' button using beforeinstallprompt. More discoverable, more code. · • No, browser-only — Rely on browser's install prompt. Simpler, less discoverable. · • Defer — Don't implement yet — revisit after core apps ship.
- **VARIOUS_Q30** How should the multiuser-pack work? · multiuser, pack — ◇ Defer
  - options: • 2 copies default — Default 2 packs — personal + work. Simple, covers most use cases. · • Unlimited — No limit — user creates as many as needed. More flexible, more complexity. · • Defer — Don't design yet — wait until the encryption layer is closer to shipping.
  - options: • Developers — Technical docs — API references, code examples, architecture. Detailed, code-heavy. · • Users — End-user docs — how to use flove apps. Practical, less technical. · • Contributors — How to contribute to flove — standards, workflows, PR process. Community-focused. · • All equally — No primary audience — serve everyone equally. Broad, less focused.
  - options: • Single 'latest' — One set of docs, always current. Simplest, no version sprawl. · • Version per release — Snapshot docs per version. Accurate, but maintenance heavy. · • Inline version markers — Tag sections with 'available since FloveX26-3'. Lightweight, informative.
- **VARIOUS_Q33** Should flove apps have a standardized footer? · apps, design — ◇ Minimal footer
  - options: • Standardized footer — All apps share the same footer component. Consistent, less individuality. · • App-specific footer — Each app designs its own footer. More creative, less consistent. · • Minimal footer — Just version + license, no links. Clean, unobtrusive.
- **VARIOUS_Q34** What is the release cadence for flove? · workflow, releases — ◇ When ready
  - options: • Weekly — Release every week. Fast iteration, potentially rushed. · • Monthly — Release every month. Balanced pace, predictable. · • Quarterly — Release every quarter. Slower, more polished. · • When ready — No fixed cadence — ship when the release is good. Flexible, unpredictable.
- **VARIOUS_Q35** How should flove handle breaking changes? · workflow, versioning — ◇ Deprecation warnings
  - options: • Deprecation warnings — Warn users/developers, give time to migrate. Gentle, requires tooling. · • Automatic migration — Script migrates old apps to new standard. Convenient, risky if wrong. · • Manual updates — Each app updates itself. Simple, potentially slow.
- **VARIOUS_Q36** Should flove adopt a formal RFC process? · workflow, process — ◇ No, keep informal
  - options: • Yes, formal RFC — Structured proposal process — draft, review, decide. More process, clearer decisions. · • No, keep informal — Decisions happen in specs and conversations. Flexible, less structured. · • Lightweight RFC — Template-based proposals, no formal voting. Balanced.
- **VARIOUS_Q37** Should flove have automated testing for apps? · workflow, testing — ◇ Light tests only
  - options: • Yes, full test suite — Unit + integration + visual regression. Catches bugs, adds complexity. · • Light tests only — Just HTML validation + basic smoke tests. Catches obvious issues. · • No tests — Keep manual verification. Simplest, relies on Marc's attention.
- **VARIOUS_Q38** How should flove handle app dependencies? · workflow, dependencies — ◇ Just documented
  - options: • Documented + versioned — Each dependency pinned to a version, documented. Reproducible builds. · • Just documented — List dependencies but don't pin versions. Informal but useful. · • No documentation — Keep dependencies implicit. Simplest, least reproducible.
- **VARIOUS_Q39** Should flove apps have performance budgets? · workflow, performance — ◇ Soft guidelines
  - options: • Yes, strict budgets — E.g., <50KB HTML, <10KB JS, <20KB CSS. Keeps apps lean, adds constraints. · • Soft guidelines — Suggested limits, not enforced. Informal, less pressure. · • No budgets — No size limits — each app is as big as it needs to be. Free-form.
- **VARIOUS_Q40** What is the flove approach to mobile-first design? · standards, mobile — ◇ Strict mobile-first
  - options: • Strict mobile-first — Design for mobile first, enhance for desktop. CSS media queries follow this pattern. · • Desktop-first with mobile — Design for desktop, adapt for mobile. More common, less future-proof. · • Equal targets — Design for both simultaneously. Balanced, more work.
- **VARIOUS_Q41** Should flove adopt a monorepo or multi-repo strategy? · workflow, repo — ◇ Monorepo
  - options: • Monorepo — Everything in one repo. Simple, atomic commits, but grows large. · • Multi-repo — Separate repos per project. Cleaner boundaries, harder cross-project changes. · • Hybrid — Core in monorepo, major projects in separate repos. Balanced.
- **VARIOUS_Q42** How should flove handle design system tokens? · standards, tokens — ◇ Hybrid
  - options: • Centralized tokens — Shared CSS variables across all apps. Consistent, less individual expression. · • Per-app tokens — Each app defines its own variables. Flexible, less consistent. · • Hybrid — Core tokens shared, apps can extend/override. Balanced.
- **VARIOUS_Q43** Should flove apps have analytics? · standards, privacy — ◇ No analytics
  - options: • No analytics — Keep it private. No tracking, no data. Matches §3.10.7. · • Self-hosted (Matomo) — Full control, privacy-respecting, but requires hosting. · • Privacy-first (Plausible) — Lightweight, GDPR-compliant, cloud-hosted. Easy but external. · • Basic counters only — Simple hit counters per page. Minimal, self-contained.
- **VARIOUS_Q44** What is the flove approach to error handling? · standards, ux — ◇ Graceful degradation
  - options: • Graceful degradation — App continues working with reduced functionality. Best UX. · • Error page — Show a friendly error message. Clear, but interrupts flow. · • Silent failure — Fail silently, log to console. Minimal user impact, hard to debug. · • Inline error states — Show error within the relevant UI component. Contextual, non-disruptive.
- **VARIOUS_Q45** Should flove apps support offline mode? · pwa, offline — ◇ Shell + cached content
  - options: • Full offline — All features work offline. Best UX, heaviest caching, most complexity. · • Shell + cached content — App shell loads offline, content may be stale. Balanced, simpler. · • Online only — No offline support — require internet. Simplest, least resilient.
- **VARIOUS_Q46** How should flove handle internationalization beyond en/es? · i18n, languages — ◇ en/es only
  - options: • Community translations — Users contribute translations via PRs. Slow, high quality. · • AI translation — Auto-translate with AI. Fast, variable quality, needs review. · • en/es only — Keep it bilingual. Simplest, matches current capacity. · • Framework ready — en/es now, but build the i18n framework so adding languages is easy later.
- **VARIOUS_Q47** Should flove have a formal deprecation policy? · workflow, deprecation — ◇ Informal notice
  - options: • Yes, formal policy — E.g., 6 months notice, migration guide, version marker. Professional, more process. · • Informal notice — Announce deprecation in changelog, no fixed timeline. Flexible. · • No policy — Just remove/replace when ready. Simplest, potentially abrupt.
- **VARIOUS_Q48** What is the flove approach to accessibility testing? · standards, a11y — ◇ AAA by design
  - options: • Automated + manual — Run axe/Lighthouse + manual screen reader testing. Most thorough. · • Automated only — Just axe/Lighthouse. Catches obvious issues, misses nuance. · • Manual only — Just manual testing. Thorough but slow, easy to skip. · • AAA by design — Follow AAA patterns in development, test periodically. Proactive.
- **VARIOUS_Q49** Should flove apps have a consistent onboarding flow? · standards, onboarding — ◇ Contextual hints
  - options: • Standardized onboarding — All apps share a welcome/tour component. Consistent, more code. · • Per-app onboarding — Each app designs its own. Flexible, potentially inconsistent. · • No onboarding — Apps are self-explanatory. Simplest, assumes user familiarity. · • Contextual hints — First-use tooltips and hints within the app. Non-disruptive, lightweight.
- **VARIOUS_Q50** How should flove handle app state persistence? · standards, persistence — ◇ Preferences only
  - options: • Full session restore — All state persists — user returns exactly where they left off. Heavy, private. · • Preferences only — Just settings and preferences persist. Light, useful. · • Nothing (ephemeral) — No persistence — fresh start each time. Most private, least convenient. · • User choice — Let user decide what persists per app. Flexible, more UI.

### Questy demo (replacement, 2026-11-19)

- **QUESTYDEMO01** Build a clean `questy-html-flove` demo with no legacy sources (replaces the retired `browsy`/`nety-spec` packs and their generator). Not started.

### Banco Risa
- **BR03** Verificar `/setprivacy` → Disable en BotFather → unanswered (defer to Marc)
- **BR04** ~~Design `risa-banco-telegram-moderation-design.md` — pendiente revisión Marc~~ → ✅ Reciclado al estándar `risaliberada.md` (presentación v1) y retirado (2026-08-16)
- **BR05** ~~Banco Phase 1: swap `banco.json` a cross-origin Pages URL, vaciar placeholder seed, añadir QR code en modal~~ → ✅ Hecho (migración a R2 + `risa.json`; QR y deep link en el modal)

### Git History
- **GH01** ~~Force push a GitHub si es necesario (reescritura de historia)~~ → ✅ Obsoleto (2026-11-07): `publish-web.sh` ya hace `push -f` del árbol filtrado a `floveorg/floveorg.github.io`; no existe un mirror completo del desarrollo en GitHub, así que no queda ninguna reescritura de historia pendiente.

### Nety
- **N01** Reconcile nety master — diverge de GitHub (26+5 commits) → unanswered (defer to Marc)
- **N03** ~~Nety tagline en `flove-tiers-matrix.html`: "coming soon" → definir~~ → ✅ Coming soon (keep placeholder)
- **NF02** Mask data clearing — discussion in progress (needs deeper conversation)

### Architecture
- **ARCH06** ~~Nety ↔ Central authority~~ → ✅ Nety is authoritative (Q197)
- **ARCH07** ~~Decentral → Central data flow~~ → ✅ Nety pushes all public data to Central (Q200)

### Validación & Pulido
- **V03** ~~Workflow de mantenimiento por tiers~~ → ⏹ Obsoleto (2026-11-15): los tiers no entran en este trunk (decisión en `plans/2026-11-14-app-tier-planned.md`); el *future wish* queda como nota de diseño en `wiki/archive/old/proposals/frontend-tiers.md` §13.1.

- **A11Y02** axe-core pass — lo estático sigue en `tools/check-a11y.py`; la pasada real usa **`tools/check-a11y-axe.py`** (Chrome headless + axe 4.10.2 vía `tools/dev/a11y-harness.html`), por app, con `--md`/`--json`; el teclado lo cubre **`tools/check-keyboard.py`** (`tools/dev/keyboard-harness.html`). Informe: [`a11y-report.md`](../archive/old/a11y-report.md) — **49 apps, 0 nodos, 0 páginas saltadas** (2026-11-19). **Hecho 2026-11-19:** las 46 apps con nodos bajaron a **0**; nety, sety y vizy2 ya se auditan (copia con recursos remotos neutralizados y espera de 120 s); nety y sety inlinean Fredoka + Space Mono; teclado **49 apps · 72 controles · 0 fallos**; estático **54 archivos · 0**. Sin timeouts ignorados.
- **UX01** Niveles 4–5 de §13.18 — la norma está en [`frontend.md` §13.18](../../standards/frontend/frontend.md) y la tabla de estado vive en `development/index.html` (Data → UX levels). 2026-11-19: **6/18 filas de nivel 4** y **1/18 de nivel 5** con ✓; el resto lleva `+`. **Pendiente:** pasada `optimizy` app por app para confirmar el nivel 4 de cada sección que la app tenga y anotar su hueco de nivel 5 — la foto actual es una encuesta estática de las 49 apps, no una pasada por app. Una app sin esa sección queda exenta (§13.18) y no entra en la cola.

  **Evidence template (2026-11-20)** — the 18 §13.18 rows, seeded from the static survey in `development/index.html` → Data → UX levels. Leave the last two columns empty until the per-app `optimizy` pass records an app with the section; an app without that section is exempt (§13.18). Static totals stay **6/18** at level 4 and **1/18** at level 5; Frontend Advanced/Super milestone states stay `todo` until this table has evidence (Q088).

  | §13.18 section | 4 · static | 5 · static | apps with evidence | gap noted |
  |---|---|---|---|---|
  | Identity & tokens | ✓ | + |  |  |
  | Self-contained | ✓ | ✓ |  |  |
  | Persistence | + | + |  |  |
  | Menu | + | + |  |  |
  | Tour | + | + |  |  |
  | Metadata | + | + |  |  |
  | Stats | + | + |  |  |
  | Summary | ✓ | + |  |  |
  | Export/share | + | + |  |  |
  | Forms | + | + |  |  |
  | Theme | + | + |  |  |
  | Language | + | + |  |  |
  | States | + | + |  |  |
  | Navigation | ✓ | + |  |  |
  | Compass | + | + |  |  |
  | Counters | ✓ | + |  |  |
  | Publish (database) | ✓ | + |  |  |
  | Locking / tiers | — | + |  |  |

  **Next pass:** 2026-11-21 · owner kdeneon · `optimizy` writes app · section · gap into the **task** (Q108/Q110); this table is its mirror, and the last two columns fill from it. Then flip Frontend Advanced/Super from `todo` (Q088).

- **VOCAB02** ~~Deriva de la matriz de vocabulario~~ → ✅ Hecho (2026-11-19): `tools/dev/check-drift.py` da **ALIGNED** con **54/54 apps** y **0 notas**. Las 19 apps que faltaban están en la matriz: 12 con `slotKinds` (media importación), browsy/fity/wizy y chacrikun/electrorchestra/frotis/loly sin campos (`displayOnly`), todas con los 4 slots compartidos. La columna Spanish está poblada para las 19.

### Worldview
- **W01** Dump Whole → worldview §3

### Tiers & Builds
- **T02** ~~Super tier placeholder in-development~~ → ⏹ Sketch de demo únicamente (`apps/blogy/blogy-super.html`); no entra en el trunk
- **T03** ~~Mega tier reserved, not featured yet~~ → ⏹ Reservado, solo diseño
- **T04** ~~Nano/mega not yet authored~~ → ⏹ Solo diseño
- **T06** ~~Sound-depth control pending a new design~~ → ✅ Volume slider
- **T07** ~~Narrativa/Films axis → standard del tier Super~~ → ✅ Interactive storytelling

### Backend & Export
- **BE02** ~~Publish.md: "more" publish mode placeholder para nety·0asis~~ → ✅ API integration
- **CB_S10** Rating widget + puzzy integration — Puzzy ya está cerrado (launcher de 44 campos + adaptador, 2026-11-15); queda el widget de rating del lado Central.

### Puzzy
- **PZ04** P0 (declarar) — añadir el bloque `puzzy` a los campos libres de las apps de referencia (Wisy, Worthing, PracSys, Souls) y verificar que `extract-fields.py --check` lo conserva. No empezado.
- **PZ05** P1 (acuñar) — una app de referencia acuña/enlaza una `PuzzyEntry` local desde un dato libre, con `dataRefs` y privacy heredada. No empezado.
- **PZ06** P4 (compartir) — round-trip de `flove-puzzy/1` en `flove-portrait/1` (import/export sin duplicar por id). No empezado.

### Browsy pre-build (2026-11-18)
- **BROWSY-PB** Open pre-build questions: Q5–Q7, Q9, Q14, Q19–Q23, Q27–Q29, Q31–Q32, plus F3/F6. See [`browsy/browsy-questions.md`](../archive/old/browsy/browsy-questions.md) §Pre-build pendings; closed log in [`browsy/pre-build/open-issues.md`](../archive/old/browsy/pre-build/open-issues.md).
- **BUI01** Browsy UI model + EN/ES copy, only standardised/secure patterns; design only, no code. See [`browsy/pre-build/11-ui-pending.md`](../archive/old/browsy/pre-build/11-ui-pending.md).
- **NUI01** Nety UI model + EN/ES; Social/Public deferred; design only, no code. Same file.
- **RC01** Additional colours for routing fields: separate consumer map, not inside `routing.json`; category base + tone. See [`frontend/routing-colours-db.md`](../../standards/frontend/routing-colours-db.md).
- **RO01** ~~Optimise `tools/routing.json`: schema, dedupe, fieldCount, cross/pending hygiene, size budget.~~ → ✅ 2026-11-18: `check-routing.py`, `build-routing-index.py`, `tools/routing-index.json` (1,288 fields), `floveFieldsFlat()` in every app.
- **RDB01** Future database for routing + colours (SQLite/Turso mirror; JSON remains authored source).

### Wizy
- **WIZY01** Nety: add the same Magic button/panel as Appy/Browsy (three wizards, Myself / With others, three content links + 3 more, MyFamily sentence). Reuse `flove:appy:plays` and `flove:myfamily:state`. Pending.

### Export / Share / Appy (2026-11-17)

- **EXP01** ~~Keys/Souls: compare the renderer HTML with the in-app output; retire `buildPortraitHtml` / `buildSummaryDocHTML` and their format rows only after parity.~~ → ✅ 2026-11-18: serializers retired; Rendery is the HTML view; smoke test passes.
- **EXP02** ~~Keys: convert the summary row to Magic · Share (JSON inside); `jsony --summary` still lists it.~~ → ✅ 2026-11-18: standard surface already in place; `jsony --app keys` 0 advisories.
- **EXP03** Send to Appy over HTTP — verify the one-record write. Open:
  - **EXP03a** Does **every app** do the direct `flove:appy:plays` write, or only **Rendery**?
  - **EXP03b** Is **same-origin** required, or is the `postMessage` handoff used always?
  - **EXP03c** Does Appy **re-validate** each play and **discard a broken one with a visible message**?
- **EXP04** ~~Fix `consult()` schema in `astry`, `blogy`, `cathy`, `daty`; add the missing `merge()` bridges.~~ → ✅ 2026-11-18: `consult()` wrapped as `flove-consult/1` across the app set; probe-safe `merge()` added to astry/blogy/daty; moraly stays read-only but accepts the probe. All four conformance checks pass.
- **EXP05** Decide strict parity via an app-supplied `fieldMap`; decide whether a seeded fixture run joins the harness.
- **EXP06** Appy play card: iframe height/scroll; “See profile” in a new tab or the same tab.
- **EXP07** Inline edit scope and per-language edits; Magic menu everywhere; confirm the `summary.edited` contract.
- **EXP08** ~~Puzzy registry check (parked)~~ → ✅ 2026-11-21: `apps{}` dropped from `tools/puzzy.json`, parked `tools/pending/sync-puzzy.py` deleted, `tools/routing.json` is the single canonical registry; `words{}` stays hand-authored.

### Reviews & polish (owner list, 2026-11-16)
- **REV01 Tours** — pendiente: revisar los recorridos / onboarding.
- **REV02 Fity** — pendiente: revisar Fity.
- **REV03 Appy tests** — pendiente: pasada de pruebas de Appy.
- **REV04 Wizy** — pendiente: revisar Wizy.
- **REV05 Musics last review** — pendiente: última revisión de las apps de música (Chacrikun, electrOrchestra, Frotis) y sus enlaces desde la vista completa de `love`.
- **REV06 Wiki review** — pendiente: revisión de la wiki / docs.
- **…** — la lista del owner continúa; añadir aquí las siguientes.

### Risa / Liberada
- **RISADNS01** Subdominios de autor (DNS + Worker) — pendiente de infraestructura:
  - `liberada.net` en Cloudflare; wildcard **proxied** `*.liberada.net` + route
    `*.liberada.net/*` al Worker; TLS `Full` y «Always Use HTTPS».
  - `usernames.json` / D1 necesita un `url` por usuario y el Worker debe
    **redirigir** a esa URL (hoy `worker.mjs` sirve `liberada.net/usa/<user>/`).
  - Cache de `usernames.json` = 5 min: un claim nuevo puede tardar ese tiempo.
  - El claim **token-in-item es local** y no escribe `usernames.json`, así que no
    crea el subdominio por sí solo: falta el paso de registro (bot `/usuario` o
    endpoint) para que el subdominio exista al reclamar.
  - Dominios propios del autor (CNAME a `liberada.net`) son un caso aparte.

### Designs Pendientes
- **DS01** ~~`flove-pwa-installable-design.md` — pendiente plan de implementación~~ → ✅ Simple install prompt
- **DS02** ~~`flove-private-addon-login-encryption-design.md` — pendiente plan de implementación~~ → ✅ OAuth integration
- **DS03** `appy-advanced-athenea-desk.md` *(no localizado en el árbol; histórico)* — Tasks 6 (wizy.html), 7 (sety.html); task 8 retired 2026-11-19
- **DS04** `appy-intros-rainbow-roadmap-design.md` *(no localizado en el árbol; histórico)* — features-intro stubbed, nav location TBD

### Android / APK
- **APK01** Android SDK no instalado — necesario para `bubblewrap build`

### Otros
- **O01** ~~Actualizar MEMORY.md con cambios recientes~~ → ✅ Índice de memoria reescrito (2026-11-07): descripciones al día + sección "Recent work" con ElectrOrchestra, linguistics/music, GH01/V03 y el flujo de publicación.
- **O02** Propagate Ken Burns minivideo animation to all apps caption sliders (goddy done as template)
- **O03** ~~Browser extension decisions pending: BE07, BE09~~ → ✅ Resolved (Q194–Q204: interoperability & conflict resolution)

### Idioma — norma 13.1 (2026-11-19)
- **LANG01** Aplicar `AGENTS.md` §13.1: todo el contenido de `flove/` en inglés, salvo `liberada`, `futbolia` y `dinámicas electrónicas`. **Pendiente de decisión del owner; no empezado.**
  - **Alcance:** 64 archivos español-first (~37.700 palabras) y ~71 bilingües (~152.000, ya con base inglesa); detección heurística. Zonas: standards 12k; appy 4,2k; sys/nety 3,8k; addons 2,4k; trusty 2,3k; economy 2,2k; chatland 2,2k; docs 1,8k; puzzy 1,5k; resto ~3k.
  - **Conflictos:** bilingües con translaty (mantener o quitar el español); excepción de `risaliberada`/risa y `projects/chatland`; identificadores, clases y claves JSON; histórico/fixtures; `AGENTS.md` en español; exports generados (`development/index.html`, `docs/index.html`, `vocabulary.*`); >20 cambios sin commitear.
  - **Opciones:** **A)** solo contenido vivo español-first, bilingües intactos, sin renombrar identificadores (recomendada); **B)** A + quitar el español de los bilingües; **C)** solo normas/docs vivos; **D)** solo apps/webs; **E)** todo literal.
  - **Ejecución:** rama/worktree, lotes por zona, checks (`check-skills`, `check-distro`, `html-validate`) tras cada lote.

### Questy Session 2026-07-29 — Central standards review
- **PEN001** ~~App datafields schema — develop per-app data schemas before defining collect() validation~~ → ✅ Hecho (2026-11-15): los 48 apps con fuente declaran su árbol `flove-fields` completo en `tools/routing.json` (`extract-fields.py --check` pasa; 0 `partial`).
- **PEN002** collect() POST wire format — define request/response shape for /api/{app}/save (Q013)
- **PEN003** API contract completeness — document error response schema, auth header spec, rate-limit behavior (Q016)
- **PEN004** postMessage race — define polling or event contract for window.flove availability (Q017)
- **PEN005** Contract tests — write test suite verifying browsy bridge window.flove shape (Q018)
- **PEN006** Version negotiation — define min-version field for browsy↔Central compat checking (Q019)

### Backy — levels (planned)

- **BACKY02** Off-machine data (backy2): complete Gitea mirrors (`git clone --mirror`/`git bundle --all`, not the partial working `.git`) + R2 copy, manifest/checksums, encrypted and copied off-machine. **No** Gitea DB, `~/agents`, keystore or SSH/GPG. Compact on the copy — `git gc`/repack or bundle; never `git gc` the live Gitea; R2 is copied with checksums. Absorbs CEN02. Risks: full-history exposure, destination credentials, size/egress, partial uploads, writable remote/ransomware; test restore and use an immutable/versioned destination.
- **BACKY03** Disaster recovery (backy3): BACKY02 + Gitea DB/config, `~/agents` tokens, Android keystore, SSH/GPG, Cloudflare/DNS and an encrypted vault export; off-site cold copy + restore drill. Keystore/tokens go in an encrypted vault or `age`/GPG archive, never plain in the repo or the backy2 bucket. Absorbs CEN03.

---

## Resolved (archived)

### Sesión 2026-11-14/15 — campos, retrato, autosuficiencia (cerrados)
- **FIELDS01** ~~Extracción completa del modelo de campos~~ → ✅ Hecho: 51 manifests `flove-fields/1` embebidos + `routing.json` regenerado (`extract-fields.py --check`); Puzzy launcher cerrado (44 campos, era el último `partial`).
- **PORTRAIT01** ~~Protocolo `flove-portrait/1` solo en Souls~~ → ✅ Hecho: adaptadores en Souls, Goddy, Realy, Inventary, MyFamily, PracSys, Keys, Crafty, Worthing, Lovy y Puzzy; `tools/dev/check-portrait-protocol.py` pasa en los 48.
- **SELF01** ~~Decidir si el código compartido rompe la autosuficiencia~~ → ✅ Hecho: el bloque común (`floveStore`/`floveFields`/`flovePort`) va inline en cada app; `addons/` es copia de referencia, nunca se carga.
- **TIER01** ~~Tiers en el trunk~~ → ✅ Decidido: fuera del trunk; los variantes mini→super quedan como demo en `apps/blogy/`, `apps/economy/dealy/`, `apps/puzzy/keys/` y `apps/appy/` (ver `plans/2026-11-14-app-tier-planned.md`).
- **DEADCss01** ~~CSS muerto acumulado~~ → ✅ Hecho: poda en Fivy, Raty y Socy, y datos en Dealy/Raty/Blogy/Fivy/Souls.
- **A11Y01** ~~Auditoría de accesibilidad~~ → ✅ Hecho (2026-11-15): `lang` en 986 spans, `<main>` en 16 apps, 37 `<h1>` ocultos, `prefers-reduced-motion` en las 7 que faltaban, 60 enlaces `href="#"` → botones accesibles, 151 controles con nombre invisible, foco/teclado en widgets, targets de 40 px en táctil. Puerta estática: `tools/check-a11y.py`.
- **FONTS01** ~~Fuentes e iconos externos~~ → ✅ Hecho (2026-11-15): **todas** las páginas (31) con `@font-face` + woff2 latin inline (+3,5 MB) y **FontAwesome subdividido por app** (4,5–63,6 KB; 146 KB en total, antes 335 KB por app). Se borró `addons/vendor/` completo (4,6 MB) y la línea que lo listaba en `build-flove-zip.sh` — el zip abortaba porque la carpeta no estaba en git. De paso: el `fa-solid-900.woff2` estaba corrupto (brotli inválido) y el navegador caía al TTF de 298 KB; los subsets se generan desde los TTF. El kit reutilizable vive en `tools/fa/` (104 KB: mapa de 2116 iconos + unión de los usados) con `tools/fa-subset.py` (`--check` sin dependencias, `--apply` con fonttools, auto-extend: un icono nuevo = una descarga y queda en caché).
- **EXPORTY01** ~~Contrato de export sin capa de protocolo~~ → ✅ Hecho: `skills/exporty/SKILL.md` + `references/export-contract.md` definen el contrato extractivo Solo ↔ Appy ↔ `routing.json`.

> Merged 2026-08-01 from `pending-questions.md` (deleted). All resolved
> questions live in the plans that made them; next milestone is the JSON distro
> (routing.json + metadata + trusty cleanup + app links).

**Where resolved questions are documented:**
- `browsy/spec.md` (BSP requirements and current decisions)
- `plans/central-backend.md` (CB01-CB40, CB_S01-CB_S10, CA01-CA03)
- `plans/2026-11-17-appy-authy-mynet.md` (Authy/MyNet)
- `plans/conflicts.md` (conflict resolutions)
- `backend.md` §10 (CC01)

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
