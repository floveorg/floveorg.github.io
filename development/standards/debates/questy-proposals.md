# Questy proposals — resolved record

> **Current task set (2026-11-20):** **1,455 live tasks + 805 archived**; see
> [`task-set-plan.md`](task-set-plan.md). The counts below are historical and
> do not describe the current register.

> **Scope / Ámbito:** EN: Historical record of the questy skill proposals (P001–P009), all resolved. · ES: Registro histórico de las propuestas de questy (P001–P009), todas resueltas.

## P001 [resolved] Archive resolved items instead of deleting

**Source:** questy skill enhancement
**Status:** resolved
**Description:** When a user selects the "archive" option in the questy HTML survey, resolved items should be moved to an archive file instead of being deleted. This preserves history while keeping the main file clean.

**Resolution:** Implemented in SKILL.md — archive mode moves resolved items to archived-questions.md instead of deleting them. HTML toggle exists in Addons → Agents.md → archive.

**Date resolved:** 2026-07-27

## P002 [resolved] Addon row layout and Continue config

**Source:** questy HTML redesign
**Status:** resolved
**Description:** Restructure addons layout with Archive/Pro on left and Scripts on right. Move .github before HTML. Workflows only shown when Git is selected. Add Continue Addons Config button to show additional settings.

**Resolution:** Implemented — layout restructured, workflows conditional on Git, Continue button added with per-addon config fields.

**Date resolved:** 2026-07-27

## P003 [resolved] Info texts for Archive, Pro, Scripts

**Source:** questy UX enhancement
**Status:** resolved
**Description:** Show info texts when Archive, Pro, or Scripts are checked. One row per addon with X to hide. Info stays visible when collapsed.

**Resolution:** Implemented — addon-info-row elements with close button, shown on check, hidden on uncheck or X click.

**Date resolved:** 2026-07-27

## P004 [resolved] Human icon and use case button

**Source:** questy UX enhancement
**Status:** resolved
**Description:** Add human icon floating top right that shows humanized descriptions. Move Scripts to Continue config section. Add info button at bottom that generates use case narrative.

**Resolution:** Implemented — 👤 icon toggles human descriptions, Scripts in Continue config, ℹ button generates use case text based on selections.

**Date resolved:** 2026-07-27

## P005 [resolved] Scripts row layout and Demonstrative Use Cases

**Source:** questy UX enhancement
**Status:** resolved
**Description:** Rename Continue Addons Config to Scripts. Show scripts one per row with tech description on click. Convert ℹ button to option style, rename to Demonstrative Use Cases, request use case generation in prompt.

**Resolution:** Implemented — Scripts button shows script rows with expandable descriptions, Demonstrative Use Cases option triggers use case generation request in prompt.

**Date resolved:** 2026-07-27

---

> Consolidated 2026-08-01 from the older `debates/PROPOSALS.md` snapshot
> (deleted — this file is the single home for questy proposals).

## P006 [resolved] Move questy out of .agents/skills

**Source:** project structure cleanup
**Status:** resolved
**Description:** All questy files should live in visible project dirs, not hidden `~/.agents/skills/`.
**Resolution:** Moved out of `~/.agents/skills` into the visible flove tree. Final location (2026-08-01): `development/standards/skills/questy/` — skill (SKILL.md), web app (index.html, crowd-questy.html, tour.html), and shared assets (presets/, templates/) together as one real copy, loaded via the `~/.agents/skills` symlink. `~/.agents/skills/questy/` removed.
**Date resolved:** 2026-07-28

## P007 [resolved] Consolidate questy-html

**Source:** project structure cleanup
**Status:** resolved
**Description:** Two questy-html files existed separately. Consolidate into tools/questy-html/ folder.
**Resolution:** Consolidated at `development/standards/skills/questy-html/` with SKILL.md, README.md, questy-html-flove.md, DESIGN-questy-html.md, gen-feeds.js, template.html, template123.html. Old pointer SKILL.md and `central/questy/tools/questy-html/` removed (2026-08-01).
**Date resolved:** 2026-07-28

## P008 [resolved] standards.md for questy

**Description:** Create questy's own development standards (official routes, rules, error handling, version format, preset authoring guide).
**Resolution:** Created at `development/standards/debates/standards.md`. Expanded with error handling, version/changelog, preset authoring, commands reference, proposals format.

## P009 [resolved] Tour HTML

**Description:** Create professional 5-slide graphical tour explaining why/what/how questy works.
**Resolution:** Created at `development/standards/skills/questy/tour.html`. 5 slides (problem, solution, system, workflow, get started), keyboard nav, dark theme.

## Conflict resolution — skill standard vs HTML form

### Naming (resolved)

| # | Area | Decision |
|---|------|----------|
| 1 | Types | **Words only** — vision, arch, trust, data, integration (no colors) |
| 2 | Hats yellow | **optimism** (not vision) |
| 3 | Hats blue | **make** (not process) |
| 4 | Lens type | **Removed** — not in KISS |
| 5 | Agents.md naming | **Current technical names** (shortcuts, constraints, etc.) |

### Structure (resolved)

| # | Area | Decision |
|---|------|----------|
| 6 | File count question | **Not needed** — routes field covers it |
| 7 | Resume flow | **Not needed** — will add later if needed |
| 8 | Addons naming | **Keep both** — skill uses folders, form uses addons |
| 9 | Workflows | **Added to skill** — full section |
| 10 | PR standards | **Added to skill** — full section |

### Agents.md (resolved)

| # | Area | Decision |
|---|------|----------|
| 11-14 | Existing sections | **Keep** — shortcuts, constraints, pending-resolutions, decision-log |
| 15-21 | New sections | **Added** — batch-overrides, export-prefs, territory, aliases, danger zone, archive |

## Deferred

| # | Area | Decision |
|---|------|----------|
| 1 | questy-html progress indicator | Defer — implement when questy-html is active |
| 2 | questy-html save/load state | Defer — localStorage already handles this |
| 3 | Multi-user scenarios | Defer — not needed yet |
| 4 | Error recovery for malformed config | Deferred — fallback to defaults works for now |

## Q061–Q090 — hitos y estándares (2026-11-20)

Thirty decisions on the milestone tracker and the standard/checker map. The
canonical register is [`milestones.json`](milestones.json); the agent-facing
detail of the execution policy is [`development/AGENTS.md`](https://flove.org/development/AGENTS.md),
indexed in [`../README.md#procedures`](https://flove.org/development/standards/README.md#procedures).

**Later move (2026-11-21):** the PROC policy itself moved out of `milestones.json`
into `development/AGENTS.md`; the JSON block was retired and both projections are
regenerated from the Markdown source. The Q062 row below records the earlier state.

| Range | Decision carried into the files |
|-------|---------------------------------|
| Q061 | `depends_on` stays optional — a hito may stand alone. |
| Q062–Q064 · Q068 · Q071 · Q076 · Q079–Q082 | `procedures` is one root roadmap execution policy (`id · title · standard · checker · advice · inputs · outputs · gates`) in `milestones.json`; `standards/README.md` owns its mirror and the one checker map. |
| Q065–Q067 · Q075 · Q085 | Section URLs keep anchors, derived from MD headings by the wiki slug rule and verified by both validators. |
| Q069 · Q070 · Q073 · Q078 · Q083 | Hito-level `skill:stage` arrays are gone; their URLs folded into `standards[]`. Q070/Q078 closed by Q083; Q077 closed by Q076. |
| Q074 · Q087 | Each of the 60 top hitos has one section-specific acceptance sentence. |
| Q088 | Frontend Advanced/Super stay `todo` until the UX01 evidence pass. |
| Q089 | Builder and `check-skills.py` fail on missing fields, bad anchors, duplicate owners and stale hito fields. |
| Q090 | Decisions applied; Q084 later closed with three added policy fields (inputs, outputs, gates). |


## Q091–Q120 — hitos, tasks y stage (2026-11-20)

Thirty questions on milestone identity, evidence, vocabulary and tasks.
Decisions are applied additively to [`milestones.json`](milestones.json);
the old keys stay as mirrors until the page code is migrated (see tasks below).

| Q | Decision |
|---|----------|
| Q091 | One opaque id per hito; `ticket` becomes a group label and dependencies use the id. |
| Q092 | The UX01 table drives `todo → part → on`; evidence means app + section + gap. |
| Q093 | The 1–5 ladder becomes an explicit field on every hito. |
| Q094 | The value protected is the done-criterion per section. |
| Q095 | Work must show state and evidence in the same row. |
| Q096 | Debate tickets are generators, not hitos (free answer corrected the premise: S1 ≠ F3). |
| Q097 | Rename fields, keep structure: `phase→stage`, `axes→sections`, `boxes→subsections`; 425 items unchanged. |
| Q098 | `state` belongs to the task; the hito derives it from its tasks. |
| Q099 | *Hecho · fácil · difícil* classifies tasks only; hitos keep the 1–5 ladder. |
| Q100 | Every hito must have tasks; dependencies are separate and free per item. |
| Q101 | No need to tell debates / plans / pendings apart — only task effort matters. |
| Q102 | Colours: green = hecha, yellow = fácil, red = difícil. |
| Q103 | Dependencies go task → task, with no inheritance from the hito. |
| Q104 | The hito row shows a counter (`2/3 hechas`), not a traffic light. |
| Q105 | Hitos are task containers; refine the hitos themselves in a later questy before generating more tasks. |
| Q106 | Closed 2026-11-20 — the "2" was option B: the first three roadmap stages, now `seed · infant · mature`. |
| Q107 | A hito groups ≥2 tasks; a single action is reclassified as a task. |
| Q108 / Q110 | `optimizy` generates the evidence and writes it into the task; the 18-row table is its mirror. |
| Q109 / Q114 | One field called `stage`, values `seed · infant · mature · grown · full`; `degree`, `phase` and "etapa" are retired. |
| Q111 | Closed 2026-11-20 by the owner — confirmed option B of Q106, so 945 tasks (3 per hito) stand. |
| Q112 / Q113 | Dismissed; regenerated as Q115 / Q119. |
| Q115 | Closed 2026-11-20 — one `stage` scale, no type discriminator. Subsections are the filter/list unit and are treated as sections via the `section` field. |
| Q116 | Short id `<section>-<n>` (e.g. `map-01`). |
| Q117 / Q118 | Q084 was closed later: `inputs` / `outputs` / `gates` were added to the six PROC. |
| Q119 | Audit coherence: every hito has a coherent structure and associated tasks; flag single-action rows. |
| Q120 | Apply all resolutions to the documents and list easy follow-ups. |

**Applied to `milestones.json`:** 315 opaque ids, 315 `stage` values, 945 tasks
(3 per hito: `seed · infant · mature`), 124 dependencies rewritten to ids, 99 rows
flagged `needs_split: true` for the refining questy. `new_tickets[]` gained a
`stage` alias of `phase`. The builder now rejects a hito without id, stage,
coherent tasks or optimizy evidence.

**Open items carried forward:** none from Q091–Q120.
**Closed afterwards:** Q084 (inputs/outputs/gates added to the six PROC), Q106/Q111
(confirmed as seed · infant · mature), Q105/Q119 (the 99 `needs_split` rows were split
into concrete stage tasks and cleared), Q115 (one `stage` scale; subsections filter and
list as sections), and the code migration of `axes→sections` / `boxes→subsections` in
builder and page.

### Follow-ups applied (2026-11-20)

1. `axes → sections`, `boxes → subsections` and `axis → section` in `milestones.json`, the builder and the page JSON reader; 425 items and `--check` counts unchanged.
2. `degreeLadder → stageNames` with `seed · infant · mature · grown · full`; Raw…Super labels retired from the embedded JSON and the Prose.
3. Work rows show a `<done>/<total>` task counter (Q104) with an expandable task list (Q102/Q110).
4. ~~Task chips carry green = *hecha*, yellow = *fácil*, red = *difícil* (Q102); no new column.~~ **Superseded by Q123/Q124:** colour is effort (green/yellow/red); `✓` marks `hecha`.
5. Expanding a row shows app · section · gap from `optimizy` evidence (Q113), with an explicit empty state while the arrays are unfilled. *(Evidence display still holds; the old colour note in item 4 does not.)*
6. ~~A `needs_split` filter chip exposes the group; the canonical `groups[]` keeps it.~~ **Superseded by Q152:** the retired chip was replaced by `Estado de tareas / Task state`; the 99 flagged hitos were cleared in item 11.
7. Stage equivalence F1–F5 → seed…full published in `plans/index.md`.
8. Q106/Q111 closed by the owner: the "2" was option B, so 945 tasks in `seed · infant · mature` stand.
9. `hitos-audit.md` carries the per-section refinement plan and its executed result.
10. One sr-only bilingual `<h1>` added; the static a11y gate is now clean.
11. The 99 flagged hitos were split into concrete stage tasks — `define locally` ·
    `apply in the basic flow` · `publish in the canonical index` — all three marked
    `fácil`; every hito now has `needs_split: false`, and 315/945 counts are intact.
12. Q084 closed: the six PROC gained `inputs`, `outputs` and `gates`; the builder
    validates all eight fields.
13. ~~The `needs_split` chip sorts the flagged value ahead of `ready`.~~ **Superseded by Q152:** the chip no longer exists; the task-state chips use the canonical `hecha · fácil · difícil · muy difícil` order.
14. Q115 closed: counting stays on one `stage` scale; Work and Docs · Plan keep
    filtering and listing by subsection (`section` field), treated as section values.
15. Degree-card milestones carry the same `x/y hechas` counter as the Work table.
16. The Stage filter shows canonical `seed (F1) … full (F5)` names; `check.js`
    guards the sr-only `<h1>` against regression.

## Q121–Q141 · conflictos, orden y procedures (2026-11-20)

Config: 30 questions (Q121–Q150), batches of 3, six hats, simple + ★, no extra
lenses, no audio. Asked so far: Q121–Q141.

| Q | Decisión |
|---|----------|
| Q121 | Cerrada por Q133: «nivel» era sinónimo de stage; se ignoran los números. |
| Q122 | Sin respuesta directa; reformulada y cerrada como Q134. |
| Q123 | Escala de esfuerzo de tres valores: `fácil · difícil · muy difícil`. |
| Q124 | Color = esfuerzo (verde/amarillo/rojo); `✓` marca `hecha`, independiente del color. |
| Q125 | Sin respuesta directa; reformulada y cerrada como Q134. |
| Q126 | El valor se deriva de los dependientes del hito (0–1 fácil, 2 difícil, ≥3 muy difícil) y se aplica solo a la task `mature`. |
| Q127 | Cola: desbloqueantes primero, luego fáciles; el `stage` no ordena la ejecución. |
| Q128 | El registro de conflictos vive en `hitos-audit.md`. |
| Q129 | Éxito = menos retrabajo: no empezar un dependiente antes de su prerrequisito. |
| Q130 | C6 se registra como excepción; no se cambian estados ni aristas. |
| Q131 / Q135 | Fusionar `contracts-04` + `quality-02`; sobrevive `contracts-04`. |
| Q132 | La sección de Procedure va en `standards/README.md` más una entrada PROC-07. |
| Q133 | «Nivel» era sinónimo: crear tasks generalistas derivadas de los hitos `grown`/`full`. |
| Q134 | Fusionar los tres duplicados en `work-15`. |
| Q136 | Una task generalista por hito, con el `stage` del hito. |
| Q137 / Q140 | PROC-07 es recomendación, no gate duro: si hay ciclo, avisar y seguir. |
| Q138 | Tabla de conflictos con tres columnas: ID · Conflicto · Decisión. |
| Q139 | Las tasks nuevas son `difícil` (o `muy difícil` con ≥3 dependientes), con dependencias task→task derivadas del hito. Las 124 aristas hito→hito quedan reflejadas en las tasks de valoración (`.3`/`.4`), sin ciclos. |
| Q141 | El desplegable de tasks del Work sigue la cola de Q127. |

**Efecto en datos:** 312 hitos, 1012 tasks (76 generalistas), 7 PROC,
422 features y `--check` en verde. Q121–Q141 cerradas (Q122/Q125 vía Q134);
la continuación Q142–Q150 está registrada en la sección siguiente.

## Q142–Q150 · cierre de la sesión (2026-11-20)

Config heredada de Q121: 30 preguntas, tandas de 3, seis sombreros, simple + ★,
sin lentes extra, sin audio. Q148b corrige una premisa errónea de Q146.

| Q | Decisión |
|---|----------|
| Q142 | Sin respuesta útil: el usuario confundió `ticket` con tasks; reformulada como Q145. |
| Q143 | `--check` avisa de ciclos task→task como warning no bloqueante, según Q140. |
| Q144 | No mostrar `unlocks=N` en el detalle de Work; el orden de Q141 basta. |
| Q145 | Quitar el campo `ticket` de los 312 hitos; el id opaco es la única clave. Los 33 tickets de debate conservan el suyo. |
| Q146 | El usuario pidió explicar `keep` antes de decidir; respondido en Q148. |
| Q147 | No publicar la cifra de 11 tasks que desbloquean 36 aristas; queda como principio, no como métrica. |
| Q148 | «Quitar `keep`», revocada por Q148b al descubrir que es load-bearing. |
| Q148b | Conservar `keep` y documentarlo: 127 `true` → `feature / stage-matrix / production`, 185 `false` → `question / debate / plansdebates`. |
| Q149 | Añadir guarda de igualdad `state_mirror == state` en el builder. |
| Q150 | Puntero de una línea en `debates/INDEX.md` a `README.md#task-order-proc-07` y cierre del log. |

**Estado final:** 312 hitos · 1012 tasks · 124 dependencias hito→hito y sus
124 espejos task→task · 7 PROC · 422 features. Gates verdes: builder `--check`,
`check.js`, `check-skills.py` (0/0) y a11y. Sin commit. Q121–Q150 cerradas
(Q122/Q125 vía Q134, Q142 vía Q145, Q148 vía Q148b).

**Mantenimiento posterior:** dos guardas nuevas en `--check` (ningún
`needs_split` pendiente y aviso si C6 deja de tener 7 inversiones), bloque
«Verificar el Work» en `README.md` con los gates permitidos, puntero en
`plans/index.md` y seis pruebas negativas sobre copias temporales: effort
inválido, dependencia task colgante, `state_mirror` roto y `needs_split`
activo fallan con mensaje propio; los ciclos task→task y un C6 con 8
inversiones solo avisan. El skill externo no rastreado `jev/` se movió a
`/tmp/opencode/jev-external` para recuperar los 18 skills canónicos.

## Q151–Q153 · corrección de la auditoría y filtros del Work (2026-11-20)

| Q | Decisión |
|---|----------|
| Q151 | La auditoría no puede usar las subsecciones de `docs` para todas las secciones: cada sección tiene sus propios campos (`docs`→map/plan/work; `backend`→contracts/delivery/storage/systems; `frontend`→a11y/levels/quality/shell/tours/tree/types/visual; `ai`→flows/levels/models/skills; `data`→index/json/mds/schemas; `community`→channels/docs/feedback/language/levels). `hitos-audit.md` regenera la tabla campo→tasks desde `milestones.json`: 28 campos, 312 hitos, 1012 tasks (903/98/11 esfuerzo, 345/19/648 estado). Los ids inventados (`docs-01` bajo `community`) desaparecen; `levels` son tres campos distintos (`levels-01`/`levels-15`/`levels-20`). |
| Q152 | En Work se elimina el filtro «Por dividir / Needs split» (`needs_split`, vacío desde Q119) y se sustituye por «Estado de tareas / Task state» con `hecha · fácil · difícil · muy difícil`. Cada feature deriva `taskcat` de las `state`/`effort` de sus tasks; el filtro usa OR sobre las tasks del hito (115 hitos con `hecha`, 312 `fácil`, 98 `difícil`, 11 `muy difícil`). |
| Q153 | Se documenta el cambio en README y se regenera el tracker. Gates verdes: `--check` (422 features, 14 grupos), `check.js`, `check-skills.py` (0/0) y a11y. Sin commit. |

## Q154 · registro de `jev` y cierre de lote (2026-11-20)

| Q | Decisión |
|---|----------|
| Q154 | Se registra el skill externo `jev` — antes en `/tmp/opencode/jev-external` — en `development/standards/skills/jev/`: categoría `utility`, H1 `# jev`, trigger `Use for`, cuerpo comprimido a ~700 palabras y 5 referencias planas enlazadas por URL de flove.org (sin carpeta `references/`). Contadores 18→19 skills y `utility` 2→3 en builder, chips y README. Gates verdes: `--check`, `check.js`, `check-skills.py` (0/0) y a11y. Sin commit. |

## Q155 · `/optimizy3` sobre `development/index.html` (2026-11-20)

| Q | Decisión |
|---|----------|
| Q155.1 | Nivel 1: `html-validate` pasa de 2 errores a 0 — se retira un `style=` redundante del SVG y el `aria-label` inválido del contenedor `#work-tabs`. El menú devuelve el foco a `#brand-map` al cerrar con Esc. Muros load-bearing verificados antes y después: `:has(#lang-en:checked)` (795–796), pares `for=`/`id=` de idioma, `#work-data` y `hashchange`. Sin refactor ni reformato. |
| Q155.2 | Nivel 2: `export` = N/A (índice de documentación, sin retrato ni modelo de usuario); `texty` sin cambios de nombre; `translaty` ya en 100 % en/es. No se tocó `routing.json`, `APP_ROUTING` ni envelopes → `jsony` = N/A. |
| Q155.3 | Nivel 3 contra [§13.18](https://flove.org/development/standards/frontend/frontend.md#1318--usability-levels--3-minimum--4-function--5-craft) (la matriz vive allí, no se copia): se corrigen los huecos reales de `States` y `Language` — estado vacío de Work bilingüe y accionable vía «Limpiar» (5 call sites → `emptyMsg()`), `Fase/Stage` y los `aria-label`/placeholder de la barra de Work con pares en/es. Tour, Summary, Export/share, Publish, Counters y Locking = N/A en una página de docs; Metadata sin OG = N/A (los índices de desarrollo no comparten tarjeta, coherente con `standards/index.html`); Google Fonts = mejora progresiva con fallback `system-ui`, patrón de todo el sitio. |
| Q155.4 | Gates finales: `html-validate` 0 errores, `check.js` en/es 100 %, builder `--check` 422 features/14 grupos, `check-skills.py` 0/0, a11y limpio. Filtro `taskcat` verificado (115/312/98/11). Sin commit. |

## Q156 · `/optimizy4` sobre `development/index.html` (2026-11-20)

| Q | Decisión |
|---|----------|
| Q156.1 | `Theme` (nivel 4): el `<head>` aplica antes del primer paint la preferencia guardada o, si no hay, `prefers-color-scheme: light`; `applyTheme(light, persist)` no escribe `flove:theme` cuando el valor viene del sistema, así que un cambio del SO se sigue respetando. El toggle explícito sí persiste. Sin flash y con `meta[color-scheme]` sincronizado. |
| Q156.2 | `Counters`/`Language`: la tira generada por `updateStrip()` estaba solo en inglés (`rows`, `Planned`, `View in tracker ↓`); ahora usa `degText` en/es como el resto del Work. `Metadata`: se añade `rel=canonical`; la tarjeta OG sigue siendo N/A en índices de desarrollo, coherente con `standards/index.html`. |
| Q156.3 | Nivel 4 N/A en esta página de docs: PWA/cached shell (no reclama instalación; `sw.js` queda para `updaty4`), Tour, Summary, Export/share, formularios largos con autosave/undo, reset destructivo, offline notice y Publish. `Identity`, `Menu`, `Navigation` (6 pestañas + `hashchange` + `replaceState`), `Compass` (las pestañas principales) y `States` ya cumplen sin cambios. |
| Q156.4 | Gates: `html-validate` 0, `check.js` 100 % en/es, builder 422/14, `check-skills.py` 0/0, a11y limpio. Sin commit. |
