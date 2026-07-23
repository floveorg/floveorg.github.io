# Pendings

Punteros desde los docs: `↗ pendings:#N` (donde N es el ID).

**Interview de decisiones:** en `making-of.html` → entrada "Various — Design Decisions". Ver también `pending-questions.md` para las 28 que faltan (K·L·M).

**Implementation plans & conflicts:** [`plans/index.md`](plans/index.md) · [`plans/conflicts.md`](plans/conflicts.md)

---

## Docs (Questionnaire)

### Respondidas
1. ✅ ephemerall = standard de persistencia
3. ✅ Sí, todos responsive
4. ✅ AAA
7. ✅ Bilingüe en/es con icono en menú
8. ✅ Enlace floveslides26.2 + solo .ods
11. ✅ `Flove[Feature]26-6`, changelog button
12. ✅ Changelog en menú (excepto main/apps-intro/apps-graph/launchers)
15. ✅ Nada, privacidad
16. ✅ Linkchecker automático
17. ✅ Open Graph completo
18. ✅ Lighthouse 90+
- ✅ **D05** Buscar en docs → None (just nav)
- ✅ **D06** Theming/branding → Standard toggle of day/night
- ✅ **D09** Ejemplos de código → None

### Pendientes
- **D02** ~~Links cruzados entre docs pages~~ → ✅ None (cada página standalone)
- **D10** ~~Navegación entre secciones~~ → ✅ Top nav bar (estandarizar existente)
- **D13** ~~Contribuir a docs~~ → ✅ Sí, contribution guide (estructura, estilo, PR)
- **D14** ~~Contacto/soporte~~ → ✅ Both (email + GitHub)
- **D19** Extensibilidad (plugins) → pendiente
- **D20** ~~Mantenimiento futuro~~ → ✅ Scheduled reviews (quarterly audits)
- **D21** Audience → All equally (no primary)
- **D22** Versioning → Version per release
- **D23** Footer → No footer for now

---

## AAA Implementation

- **AAA01** Implementar WCAG AAA en `docs/index.html` — contraste 7:1, skip links, aria-describedby, expandir abreviaciones (3-4h)

---

## Build & Deploy

- **BD01** Rebuild `flove.zip` — paquete descargable actualizado
- **BD02** `update-web` — regenerar `sw.js` + `flove.zip` + push a GitHub Pages

---

## Banco Risa

- **BR01** Cablear `CLOUDINARY_URL` con la key que sube
- **BR02** Test end-to-end: audio → moderación → Cloudinary → banco.json
- **BR03** Verificar `/setprivacy` → Disable en BotFather
- **BR04** Design `risa-banco-telegram-moderation-design.md` — pendiente revisión Marc
- **BR05** Banco Phase 1: swap `banco.json` a cross-origin Pages URL, vaciar placeholder seed, añadir QR code en modal

---

## Git History

- **GH01** Force push a GitHub si es necesario (reescritura de historia)

---

## Coming Soon (deferred)

- **CS01** Save app button in menús → repo download link (no implementar)

---

## Nety

- **N01** Reconcile nety master — diverge de GitHub (26+5 commits)
- **N02** Choque rename flovenet→nety (1905 hits)
- **N03** Nety tagline en `flove-tiers-matrix.html`: "coming soon" → definir
- **NYB01** ~~Decidir nety target shape: tabbed app / section-stacked / hybrid~~ → ✅ Tabbed app

### Nety Ecosystem (§13 deferred)
- **NEC01** ~~Definir dirección `super` tier: network powers vs self-sovereignty~~ → ✅ Self-sovereignty
- **NEC02** ~~Fijar quotas concretos por tier de hardware nety (bandwidth, storage, compute)~~ → ✅ Defer again
- **NEC03** ~~Implementar crypto real de key recovery/rotation para identidad nety~~ → ✅ Defer (esperar athenea/wizy)
- **NEC04** ~~Diseñar ranking real de engagement y anti-gaming para likes/reposts~~ → ✅ Weighted by trust/stage
- **NEC05** ~~Especificar mecánicas de curadores: selección, quorum, accountability~~ → ✅ Self-selected + community veto
- **NEC06** ~~Diseñar flujo de adjudicación de abusos: peer reports, jurors, staking~~ → ✅ Hybrid (curators urgent, jury complex)
- **NEC07** ~~Diseñar SSB identity recovery sidechain (keypair + social vouchers)~~ → ✅ Social recovery (N-of-M vouchers)

---

## Validación & Pulido

- **V01** Fix `<a>`-en-`<ul>` de worthing.html
- **V02** Propagar validación a appy/diesafe/crumbly
- **V03** Workflow de mantenimiento por tiers

---

## Worldview

- **W01** Dump Whole → worldview §3

---

## Tiers & Builds

- **T01** Mini app build pending — tier/build rename + optimización
- **T02** Super tier placeholder in-development
- **T03** Mega tier reserved, not featured yet
- **T04** Nano/mega not yet authored
- **T05** Counters: mini/basic/advanced-placeholder/super-placeholder sin counters
- **T06** Sound-depth control pending a new design
- **T07** Narrativa/Films axis → standard del tier Super

---

## Backend & Export

- **BE01** backend.md draft v0.3 — documento incompleto
- **BE02** Publish.md: "more" publish mode placeholder para nety·0asis
- **BE03** Coordinates.md: flove-quality measure, Tiers >5, Gitea↔docs sibling rule
- **BE06** Per-app cube downloads — construir paquetes zip por app (necesita builder script)

### Backend Open Questions (§12)
- **BEQ01** ~~Decidir modelo de autoría de `routing.json`: wiki comunitaria vs solo curadores~~ → ✅ Automated (AI)
- **BEQ02** ~~Decidir approach de fine-tuning para AI module 42: full vs LoRA, ¿cuyo compute?~~ → ✅ Depends on athenea/wizy
- **BEQ03** ~~Decidir timing de identity masks (múltiples pseudónimos por usuario): ¿F2 o F5?~~ → ✅ F2 (early)
- **BEQ04** ~~Decidir granularidad de visibilidad por elemento vs depender de defaults 0asis~~ → ✅ Hybrid (default from 0asis + override)
- **BEQ05** ~~Decidir semántica de cross-links: tipados (`responds_to`, `derived_from`) vs sin tipos~~ → ✅ Typed
- **BEQ06** Cubes: No, flove.zip only (simpler, one big bundle)

---

## Designs Pendientes

- **DS01** `flove-pwa-installable-design.md` — pendiente plan de implementación
- **DS02** `flove-private-addon-login-encryption-design.md` — pendiente plan de implementación
- **DS03** `appy-advanced-athenea-desk.md` — Tasks 6 (wizy.html), 7 (sety.html), 8 (making-of.html)
- **DS04** `appy-intros-rainbow-roadmap-design.md` — features-intro stubbed, nav location TBD
- **PWA01** ~~Construir botón "Install flove" in-app usando `beforeinstallprompt`~~ → ✅ Defer (revisar después de core apps)
- **MUP01** ~~Diseñar mecánicas multiuser-pack: copy count, distroId, launcher UX, aislamiento~~ → ✅ Defer (esperar capa de encryption)

---

## Puzzy Open Questions

- **PZQ01** ~~Decidir modelo de agregación multi-rater en common area (juxtaposición, mean+dispersión, toggle)~~ → ✅ Mean + dispersion
- **PZQ02** ~~Decidir arquitectura de compute de puzzy: client-only, module-42-only, híbrido con cache~~ → ✅ Hybrid with offline cache
- **PZQ03** Rellenar catálogo canónico de free-tags por app en `mapping.json` (entregable F1)

---

## Appy Open Questions

- **APR01** Decidir rendering de rainbow roadmap: ¿idéntico en ambos archivos o variante "reached" en appy-basic?
- **AF01** ~~Decidir social app: ¿standalone `apps/social.html` o profily-integrated MyNet?~~ → ✅ Profily-integrated MyNet
- **AF02** ~~Decidir vizy XR/VR: ¿recuperar `apps/flovy/vr` de git o abandonar dirección VR?~~ → ✅ Defer again

---

## Trusty Open Questions

- **TR01** ~~Trusty Q3: ¿fusionar Conditions en Protection fields o mantener separado?~~ → ✅ Conditional merge (merge UI, separate data model)
- **TR02** ~~Trusty Q4: ¿implementar crumbly granular mode o descartar?~~ → ✅ Discard

---

## Shared Code Abstraction (2026-07)

All decided. Source: interview section K.

| ID | Topic | Decision |
|----|-------|----------|
| CA01 | flove.js/flove.css location | `apps/appy/` |
| CA02 | Loading method | Hybrid (external dev, inlined prod) |
| CA03 | First wave flove.js | Incremental (one module at a time) |
| CA04 | First wave flove.css | Just flove-bar first |
| CA05 | apps/index.html theme | Keep its own pattern |
| CA06 | Dark-by-design toggle | Toggle flips variant |
| CA07 | System preference | System default + override |
| CA08 | Transition animation | JS-controlled fade |

---

## Backend Deployment (2026-07)

Partially decided. Source: interview section L. L04/L05/L06 still pending.

| ID | Topic | Decision |
|----|-------|----------|
| DEP01 | Hosting | Hybrid (local dev + cloud prod, GitHub) |
| DEP02 | Auth | OAuth (GitHub/Google) — "in this version" |
| DEP03 | Database | JSON files — "in this version" |
| DEP07 | Logging | Structured JSON logs — "in this version" |
| DEP08 | Backups | Automated (cron) |
| DEP09 | Deployment | CI/CD (GitHub Actions) |
| DEP10 | Initial scope | Minimal (routing.json + metadata) |

---

## Trusty — SIGNALS Cleanup (2026-07)

All decided. Source: interview section M.

| ID | Topic | Decision |
|----|-------|----------|
| TRU01 | Reciprocity in SIGNALS | Remove (keep only in CONDITIONS) |
| TRU02 | Transparency in SIGNALS | Remove (keep only in CONDITIONS) |
| TRU06 | "Respect a no" → evily | Add link |
| TRU07 | "Keep a secret" → evily | Add link |
| TRU08 | "Let a bond end kindly" → myfamily | Add link |
| TRU09 | Other PEOPLE links | No other links needed |
| TRU10 | Other overlaps | No other overlaps |
| M03 | Other SIGNALS to remove | Keep remaining 4 |
| M04 | "See I'm not okay" → maty | Don't add link (generic) |
| M05 | "Speak well of me" → maty | Don't add link (generic) |

---

## Nety Trust — Curator & Abuse (2026-07)

All decided. Source: conflict resolution questions.

| ID | Topic | Decision |
|----|-------|----------|
| C01 | Curator bonus weight | ×3, decays 10%/week |
| C02 | Tier 1 abuse | Self-selection + community veto + simple report form |
| C03 | Mask recovery v1 | Recovery code displayed once, user writes down |
| C15 | Lost recovery code | New mask only (no recovery of old) |

---

## Deep Links (2026-07)

All decided. Source: conflict resolution questions.

| ID | Topic | Decision |
|----|-------|----------|
| C07 | Direction | One-way: trusty → maty/evily |
| C11 | Mechanism | URL params |
| C14 | Param schema | `?from={source_app}&item={item_id}` |
| C26 | HTML format | Separate div below item |

---

## Release & Milestone (2026-07)

All decided. Source: conflict resolution questions.

| ID | Topic | Decision |
|----|-------|----------|
| C06 | Migration script | Defer until first breaking change |
| C09 | "Ready" definition | Checklist: core features + mobile + no crashes + docs |
| C12 | Core features | Scoped to current adoption milestone |
| C16 | Next milestone | JSON distro + trusty SIGNALS cleanup + app links |
| C34 | Distribution | Download button + GitHub Releases + direct URL |

---

## JSON Distro (2026-07)

All decided. Source: advanced + conflict resolution questions.

| ID | Topic | Decision |
|----|-------|----------|
| A03/C20 | Routing schema | `{version, lastUpdated, apps: [{id, name, url, tier, description, tags}]}` |
| C21 | App discovery | Flat scan `apps/*/[name].html` |
| C22 | Build script | Reuse `build-flove-zip.sh` |
| C23 | routing.json location | Root of zip |
| C24 | Runtime loading | Fetch on load, same-origin |
| C27 | Version field | Yes |
| C28 | Metadata extraction | Parse `<meta>` tags from HTML |
| C30 | App ID | Filename without extension |
| C31 | Tier values | nano, mini, basic, normal, advanced, super, mega |
| C32 | Meta tags | `tier` from `<meta name="tier">` |
| C33 | Timestamp | Auto-generated yy-mm by build script |
| C35 | Full metadata | `tier` + `description` + `tags` |
| C36 | Validation | Check required fields, warn on missing |
| C37 | README.md | Minimal: what flove + how to open + credits |
| C38 | Tags format | JSON array in meta: `["social","trust"]` |
| C40 | Upload to releases | `update-web` skill handles it |

---

## Implementation Decisions (2026-07)

All decided. Source: I01-I10.

| ID | Topic | Decision |
|----|-------|----------|
| I01 | App link rendering | Auto-generate `<a>` from `app` field |
| I02 | Missing deep link params | Show target app normally, ignore |
| I03 | routing.json caching | No fetch — static in zip |
| I04 | Meta tag format | Three separate metas (tier, description, tags) |
| I05 | Build validation | Interactive prompt — ask Marc to fix |
| I06 | README content | App list with one-line descriptions |
| I07 | Abuse report form | Checkbox list + text (predefined options) |
| I08 | Mask recovery code | Downloadable file, field in `souls-summary.json` |
| I09 | Release checklist | Part of `update-web` skill |
| I10 | App link style | Small muted text with arrow |

---

## Standards — New Decisions (2026-07)

All decided. Source: interview rounds 1-3.

| ID | Topic | Decision |
|----|-------|----------|
| SD01 | Repo strategy | Multi-repo (separate repos per project) |
| SD02 | Analytics | Privacy-first (Plausible, cloud-hosted) |
| SD03 | Error handling | Graceful degradation (app continues with reduced functionality) |
| SD04 | Offline | Full offline (all features work offline) |
| SD05 | i18n | Framework ready (en/es now, build framework for easy language addition) |
| SD06 | Deprecation | Yes, formal policy (6 months notice, migration guide, version marker) |
| SD07 | A11y testing | AAA by design (follow patterns in dev, test periodically) |
| SD08 | Onboarding | No onboarding (apps are self-explanatory) |
| SD09 | State persistence | Ephemerall standard (survive close, reload resets) |
| SD10 | Tokens | Hybrid (core shared, apps can extend/override) |
| SD11 | Performance | Soft guidelines (suggested limits, not enforced) |
| SD12 | Mobile-first | Strict mobile-first (design for mobile, enhance for desktop) |
| SD13 | Testing | Yes, full test suite (unit + integration + visual regression) |
| SD14 | Dependencies | Just documented (list deps, don't pin versions) |
| SD15 | RFC process | No, keep informal (decisions in specs and conversations) |
| SD16 | Breaking changes | Automatic migration (script migrates old apps to new standard) |
| SD17 | Release cadence | When ready (no fixed cadence, ship when good) |

---

## Android / APK

- **APK01** Android SDK no instalado — necesario para `bubblewrap build`

---

## Otros

- **O01** Actualizar MEMORY.md con cambios recientes
- **O02** Propagate Ken Burns minivideo animation to all apps caption sliders (goddy done as template)
