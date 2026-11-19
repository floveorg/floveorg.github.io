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
- **GH01** ~~Force push a GitHub si es necesario (reescritura de historia)~~ → ✅ Obsoleto (2026-11-07): `publish-web.sh` ya hace `push -f` del árbol filtrado a `floveorg/floveorg.github.io`; no existe un mirror completo del desarrollo en GitHub, así que no queda ninguna reescritura de historia pendiente.

### Nety
- **N01** Reconcile nety master — diverge de GitHub (26+5 commits) → unanswered (defer to Marc)
- **N03** ~~Nety tagline en `flove-tiers-matrix.html`: "coming soon" → definir~~ → ✅ Coming soon (keep placeholder)
- **NF02** Mask data clearing — discussion in progress (needs deeper conversation)

### Architecture
- **ARCH06** ~~Nety ↔ Central authority~~ → ✅ Nety is authoritative (Q197)
- **ARCH07** ~~Decentral → Central data flow~~ → ✅ Nety pushes all public data to Central (Q200)

### Validación & Pulido
- **V03** ~~Workflow de mantenimiento por tiers~~ → ⏹ Obsoleto (2026-11-15): los tiers no entran en este trunk (decisión en `plans/2026-11-14-app-tier-planned.md`); el *future wish* queda como nota de diseño en `standards/debates/proposals/frontend-tiers.md` §13.1.

- **A11Y02** axe-core pass — lo estático sigue en `tools/check-a11y.py`; la pasada real usa **`tools/check-a11y-axe.py`** (Chrome headless + axe 4.10.2 vía `development/standards/scripts/a11y-harness.html`), por app, con `--md`/`--json`. Informe: [`a11y-report.md`](a11y-report.md) — 49 apps, 911 nodos, 13 reglas. **Hecho 2026-11-18:** `meta-viewport` eliminado en 8 apps (sety, inventary, goddy, socy, astry, lovy, diesafe, myfamily). **También 2026-11-18:** H1 oculto en souls, keys, shareful y freed; nombre en el progreso de realy, el corazón de lovy y los selects de export de lowy; `intro-track` enfocable en fivy/keys; enlace de browsy subrayado. **blogy 2026-11-18:** 486 → **0** nodos (`aria-label` en los 283 `input.ctl` + el bloque de estado en `role=region`). Pendiente: `region` en el resto, `color-contrast` (72 / 9), `aria-allowed-role` (34 / 9), `nested-interactive` (19 / 4). Timeout ignorado por decisión del owner: nety, sety, vizy2.
- **VOCAB02** ~~Deriva de la matriz de vocabulario~~ → ✅ Hecho (2026-11-19): `scripts/check-drift.py` da **ALIGNED** con **54/54 apps** y **0 notas**. Las 19 apps que faltaban están en la matriz: 12 con `slotKinds` (media importación), browsy/fity/wizy y chacrikun/electrorchestra/frotis/loly sin campos (`displayOnly`), todas con los 4 slots compartidos. La columna Spanish está poblada para las 19.

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
- **BROWSY-PB** Open pre-build questions: Q5–Q7, Q9, Q14, Q19–Q23, Q27–Q29, Q31–Q32, plus F3/F6. See [`browsy/browsy-questions.md`](browsy/browsy-questions.md) §Pre-build pendings; closed log in [`browsy/pre-build/open-issues.md`](browsy/pre-build/open-issues.md).
- **BUI01** Browsy UI model + EN/ES copy, only standardised/secure patterns; design only, no code. See [`browsy/pre-build/11-ui-pending.md`](browsy/pre-build/11-ui-pending.md).
- **NUI01** Nety UI model + EN/ES; Social/Public deferred; design only, no code. Same file.
- **RC01** Additional colours for routing fields: separate consumer map, not inside `routing.json`; category base + tone. See [`frontend/routing-colours-db.md`](../frontend/routing-colours-db.md).
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
- **EXP08** Puzzy registry check (parked): decide whether `tools/puzzy.json` `apps{}` is generated, read live from routing, or dropped.

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
- **DS03** `appy-advanced-athenea-desk.md` — Tasks 6 (wizy.html), 7 (sety.html), 8 (making-of.html)
- **DS04** `appy-intros-rainbow-roadmap-design.md` — features-intro stubbed, nav location TBD

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
- **PORTRAIT01** ~~Protocolo `flove-portrait/1` solo en Souls~~ → ✅ Hecho: adaptadores en Souls, Goddy, Realy, Inventary, MyFamily, PracSys, Keys, Crafty, Worthing, Lovy y Puzzy; `development/scripts/check-portrait-protocol.py` pasa en los 48.
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
