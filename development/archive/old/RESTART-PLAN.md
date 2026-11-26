# Plan de ejecución v4.0 — Migración taxonómica flove

Estado: **plan vigente**. Sustituye a v3.2. No ejecutar hasta aprobación explícita.
Sin commit publicado ni push. Se permite **un commit local de línea base** (D-08).
Idioma de trabajo: español.

> Documento de planeación, no contenido. Igual que `RESTART-PLAN-REVIEW.md`, se
> excluye de `check-retired-paths.py`, de `check-links.py` y del grep de barrido.
> v3.2 queda archivado fuera del repo en `/tmp/opencode/RESTART-PLAN-v3.2.md`
> (sha256 `b5f64685…`). Este documento no modifica `archive/` ni publica nada.

**Cambios de v4.0 frente a v3.2**

1. La especificación pasa a ser ejecutable: `map.json`, `contract.json`,
   `paths.py`, `rewrite.py`, fixtures y gates. Las tablas de prosa dejan de ser
   la fuente de verdad.
2. Se corrige la línea base: cifras reales, gates actuales y el `backup.tgz`
   que no coincide con `index.html`.
3. Se separa procedencia de rutas vivas: `owner_origin` e inventarios no se
   reescriben.
4. Se resuelve el archivo: bytes intactos + `legacy_root` en `check-archive`.
5. Se ordena en **slices verdes S0–S6**; cada slice termina sin fallos nuevos.
6. Se reconoce el porte de runtime `toptab`/`capitulo` como trabajo propio.
7. Se reclasifican los 37 redirects: 26 identidades + 11 compatibilidad real.
8. Se decide el árbol de 4 toptabs y se documenta el mapeo de los 26 `section`.

---

## 0. Línea base verificada (2026-11-24)

### 0.1 Registro de páginas y de trabajo

| Clave | Valor real |
|---|---:|
| `pages` | 29 |
| `plans` | 19 |
| `redirects` | 37 (26 identidad + 11 compatibilidad) |
| `aliases` | 42 |
| `field_map` | 29 |
| `labels` | 5 |
| `roots` | 3 |
| `excluded_live` | 2 |
| hitos | 326 |
| tickets | 37 |
| live tasks | 1.559 |
| archived tasks | 805 |
| pendings rows | 75 |
| features | 438 (326 + 37 + 75) |

### 0.2 Campos con rutas (no “presencias”)

| Campo | Presencias | Con ruta `development/…` o URL |
|---|---:|---:|
| `tasks[].owner` | 1.559 | 1.559 |
| `tasks[].owner_origin` | 1.559 | **1.471** (88 no son rutas) |
| `tasks[].evidence.pointer.value` | 1.559 | **1.401** (158 no son rutas) |
| `tasks[].source` | 280 | 280 |
| hito `standards[]` | 140 | 140 |
| hito `notes` | 147 con ruta en prosa | 147 |
| hito `docs[]` | 8 | 8 |
| `pages[].supersedes[]` | 159 | 159 |
| `pages[].detail` | 2 | 2 |

Regla: **ninguna cifra se escribe a mano**. El transformer emite el censo final
y `contract.json` lo compara.

### 0.3 Gates actuales

| Gate | Estado base |
|---|---|
| `build-work-tracker.py --check` | OK |
| `build-common.py --check` | OK |
| `jsony.py --no-write` | OK |
| `skilly.py` | 0 errores, 47 warnings |
| `check-archive.py --check` | OK (2 particiones, 90 ficheros, 67 ledger sources) |
| `check-content.py --check` | OK (1.018 headings, 0 pending) |
| `check-plan-tray.py --check` | OK |
| `check-page-status.py --check` | OK (22 live pages, 19 plans) |
| `check-links.py --check` | OK (128 docs) |
| `check-routing.py` | OK (54 apps) |
| `check-docs-manifest.py --check` | **FAIL 1** (`skills.md` CONTEXT id) |
| `check-taxonomy.py` | **FAIL 497** (4 toptabs, `MAX_DEPTH`, `path` vacíos) |
| `check-retired-paths.py --check` | **FAIL 1** (el propio plan) |

Los tres fallos base tienen dueño y slice de cierre: `check-retired-paths` se
cierra en S0 (exclusión del plan y de esta revisión); `check-docs-manifest` en
S3; `check-taxonomy` en S5.

### 0.4 Línea base del árbol

- `git status --porcelain`: **93 entradas** (39 `M`, 2 `MM`, 28 `D`, 12 `RM`,
  1 `AM`, 1 `R`, 10 `??`). `development/index.html` está en `MM`.
- `backup.tgz` existe en `/tmp/opencode/flove-taxonomy-2026-11-23/`, pero su
  `development/index.html` **no coincide** con el actual
  (`2efd1c42…` vs `81ce8ecb…`). No se usa como rollback principal.
- `RESTART-PLAN.md` es untracked. El commit local de línea base lo incluye.
- El intento anterior está en
  `tools/dev/_archive/taxonomy-migration-2026-11-23/` (`map.json`,
  `apply-taxonomy.py`, `rewrite-links.py`, `audit-taxonomy.py`,
  `recycle-content.py`, `REPORT.md`) y en
  `/tmp/opencode/flove-taxonomy-2026-11-23/` (`main.js`, `NEW-TREE.txt`).
  Se reutiliza como punto de partida, no se ignora.

---

## 1. Principios rectores (no negociables)

1. **Spec primero.** `migration/map.json` es la única fuente de rutas, ids,
   campos, redirects y aliases. Las tablas de este plan lo resumen; no lo
   sustituyen.
2. **Fuente → builder dueño → `--check`.** Nunca editar a mano `common.json`,
   `pages.json`, `INDEX.md`, mapas, ledgers, inventory, `task-recycle*`.
   `pages.json` e `INDEX.md` son **fuentes humanas** tras retirar su one-shot;
   se editan con el transformer, no “se regeneran”.
3. **Procedencia inmutable.** `owner_origin`, `register-path-inventory.baseline`
   y `register-path-migration` conservan rutas históricas. Los gates las leen
   con remap; nunca se reescriben en sitio.
4. **Un solo registro de rutas.** Todo script vive de `tools/dev/paths.py`.
   `check-paths.py` prohíbe prefijos retirados hardcodeados.
5. **Slices verdes.** Cada slice S0–S6 deja el repo ejecutable y sin fallos
   nuevos frente a la línea base. No hay dos fases seguidas en rojo.
6. **Sin rediseño no declarado.** El árbol de 4 toptabs y la URL `capitulo` son
   un cambio de IA declarado en D-10/D-11/D-14, no un efecto colateral.
7. **Archivo intacto.** `archive/` y `_archive/` conservan bytes. El checker
   acepta `legacy_root`; el manifiesto no se reescribe.
8. **Idempotencia.** Dos builds consecutivos producen hashes idénticos;
   `git diff --check` limpio.
9. **Anclas intactas.** Se reescribe el lado fichero de `ruta.md#ancla`; el
   ancla se conserva carácter a carácter. Los 39 `read_next` muertos quedan
   como deuda documentada, sin inventar destinos.
10. **Nada se publica sin aprobación.** Commit local de línea base sí; push,
    `updaty` y release no.

---

## 2. Artefactos de spec (se crean en S0)

### 2.1 `migration/map.json` (schema `flove-migration-map/1`)

Una entrada por:

- carpeta/fichero movido: `from`, `to`, `kind` (`move|rename|retire|freeze`),
  `sha256_before`, `sha256_after`, `owner`;
- página/plan: `id_old`, `id_new`, `path_old`, `path_new`, `detail_new`;
- hito/ticket: `section`, `path` completo (`[toptab, …capítulos]`);
- campo de registro: `json_pointer` permitido (`pages[].path`,
  `milestones[].owner`, `notes`, `supersedes[]`, …) y su regla;
- redirect: `key`, `target`, `kind` (`identity|compat`);
- alias: `key`, `target`;
- URL pública: `old_prefix`, `new_prefix`.

Reglas:

- destinos únicos; sin colisión de mayúsculas; sin mover a un destino que ya
  existe con contenido distinto;
- ninguna entrada `move` cambia bytes (salvo las excepciones declaradas:
  `jev` borrado, `frontend.md` ancla D-06, manifiesto de archivo si se aprueba);
- `python3 tools/dev/migrate/check-map.py` valida el mapa contra el árbol real.

### 2.2 `migration/contract.json`

Invariantes machine-checkables:

- 29 páginas, 19 planes, 42 aliases, 37 redirects (26 identidad + 11 compat);
- 326 hitos, 37 tickets, 1.559 live, 805 archived, 438 features;
- 0 `path` vacíos; 0 owners muertos; 19 pares `plan_id`/`plan_page`;
- censo de `path#ancla` emitido por el transformer, con el ancla intacta;
  31 anclas rotas antes y después;
- `archive/` byte a byte; `check-archive` verde con `legacy_root`;
- dos builds idénticos.

Si el owner elige 331 hitos / 443 features (D-10), el contrato se actualiza
**antes** de S0, no durante la ejecución.

### 2.3 `tools/dev/paths.py`

Constantes únicas:

```python
ROOT, DEVELOPMENT, STANDARDS, PLANS, TASKS, CHECKS
PAGES, INDEX, AGENTS, MILESTONES, COMMON, PENDINGS, MOVES
PLANS_DIR, TASKS_DIR, ARCHIVE
```

Los 15 scripts importan de aquí. `check-paths.py` falla si aparece
`development/wiki`, `tools/dev/wiki` o `tools/dev/work` en un `.py` vivo.

### 2.4 `migration/rewrite.py`

- `--dry-run`: diff por fichero y campo.
- `--check`: falla si el árbol no coincide con `map.json`.
- `--apply`: escribe solo campos de la allowlist.
- Reescritura de prosa **solo** para tokens de ruta completos
  (`plan.md#ancla` → `plans.md#ancla`), nunca para `wiki` como palabra.
- No toca `owner_origin`, inventarios ni `archive/`.

### 2.5 Gates nuevos

| Gate | Qué comprueba |
|---|---|
| `check-map.py` | mapa completo, sin colisiones, destinos existentes |
| `check-paths.py` | 0 prefijos retirados en scripts vivos |
| `check-redirects.py` | 26 identidad + 11 compat; sin self en compat, sin cadena, sin clave viva, destino existente |
| `check-urls.py` | 198 URLs públicas reescritas o cubiertas por 404 |
| `check-links.py` ampliado | `standards/`, `plans/`, `tasks/`, `INDEX.md`, `AGENTS.md`, sidebar por ruta |
| `check-docs-manifest.py` | `pages.json`, 29 páginas, INDEX, sidebar, `supersedes` |
| `check-taxonomy.py` | 4 toptabs, `MAX_DEPTH=4`, `path` en 326+37 |

### 2.6 Fixtures y ensayo

- 1 hito, 1 ticket, 1 tarea, 1 plan, 1 página, 1 redirect y 1 alias
  antes/después en `migration/fixtures/`.
- `migration/rehearsal.md`: recorrido completo en worktree, tiempos y un
  rollback de slice probado.

### 2.7 Worktree y rollback

- Línea base: commit local `migration-baseline-2026-11-24` (no push) con las 93
  entradas actuales. Es el estado real de partida.
- Ejecución: worktree `flove-migration` desde esa etiqueta. El árbol actual
  queda como referencia.
- Rollback de slice: `git restore --source=migration-baseline-2026-11-24 -- <paths>`
  o el inverso de `map.json`. Nunca `reset --hard`.

---

## 3. Árbol objetivo y mapeos

### 3.1 Carpetas y ficheros

| Origen | Destino | Notas |
|---|---|---|
| `development/wiki/plans/` | `development/plans/` | 19 planes + conflicts + debates |
| `development/wiki/work/` | `development/tasks/` | `milestones.json`, `common.json`, `pendings.md`, `measures.md`, `.gitkeep` |
| `development/wiki/archive/` | `development/archive/` | **bytes intactos**; `legacy_root` |
| `development/wiki/wiki.json` | `development/pages.json` | registro canónico |
| `development/wiki/*` (resto) | `development/*` | `INDEX.md`, mapas, ledgers, inventory, migration, recycle |
| `tools/dev/wiki/` | `tools/dev/checks/` | merge con 6 checkers; 15 total |
| `wiki-inventory.py` | `page-inventory.py` | dentro de `checks/` |
| `wiki-resolve.py` | `page-resolve.py` | dentro de `checks/` |
| `tools/dev/work/` | `tools/dev/tasks/` | 9 scripts + 1 config; `chapter-decks` promovido |
| `development/standards/workflow/*.html` | `tools/dev/assets/workflow/` | 3 HTML de demo |
| `development/addons/media/apps/logos/community/community-logos.html` | `.../logos/home/home-logos.html` | 11 links en `standards/Community/index.html` |

Corrección: no existe `logos/community/`; el fichero real está bajo
`development/addons/media/apps/logos/community/`. `development/addons/workflow.html`
es otra página (standing `standing/workflow`) y **no se mueve**.

**Guardarraíl `tools/dev` (2026-11-24):** hay trabajo manual/post-scripty en
`tools/dev/` que debe respetarse. No recrear `tools/dev/wiki/` ni
`tools/dev/work/`; su contenido canónico vive en `tools/dev/checks/` y
`tools/dev/tasks/`. Antes de mover/renombrar scripts en `tools/dev/`, verificar
referencias y cambios locales no committeados.

### 3.2 `development/standards/`

| Origen | Destino |
|---|---|
| `plan.md` | `plans/plans.md` |
| `work.md` | `tasks/tasks.md` |
| `docs.md` | `community/guide/guide.md` (id `community/guide`) |
| `puzzy.md` | `data/schemas/puzzy.md` |
| `Community/**` | `community/**` (feedback con `marc/index.html`, language, channels + `index.html`) |
| `json.md`, `mds.md` | `data/content/json.md`, `frontend/frontend.md#1320-data-depth-levels` (mds.md removed) |
| `schemas.md`, `Data/Schemas/` | `data/schemas/` |
| `skills.md`, `AI/Skills/` | `data/ai/skills/` (**sin `jev/`**, 21 skills) |
| `models.md`, `flows.md` | `data/ai/models/models.md`, `data/ai/flows/flows.md` |
| `Backend/**` | `backend/{scripts,systems,mynet,storage,database/risaliberada}/` |
| `Frontend/**` | `frontend/{apps,accessibility,experience}/` + 7 `.md` compartidos |
| `Docs/Plan/`, `Docs/Work/`, `Data/JSON/`, `Data/MDS/` | directorios vacíos: se retiran |

Nota de dimensión: el **árbol de IA** (`home/community`, `data/ai`) no es el
**árbol de ficheros** (`standards/community`, `standards/data/ai`). `path` en
`milestones.json` es el capítulo de IA; `owner` es la ruta de fichero.

### 3.3 Identificadores y símbolos

| Símbolo | Viejo | Nuevo | Refs |
|---|---|---|---:|
| esquema del registro | `flove-wiki-manifest/1` | `flove-pages-manifest/1` | 2 |
| descriptor | `docs-wiki manifest` | `docs pages manifest` | 4 |
| lane en `tools/README.md` | `wiki/`, `work/` | `checks/`, `tasks/` | tabla |
| `TABS` | 6: docs, backend, frontend, ai, data, community | **4: home, data, backend, frontend** | builder |
| `MAX_DEPTH` | ausente | **4** | builder/checker |
| `filter_order` | 13 grupos | **17** (map.json) | builder |
| `AXES` | dominios planos | árbol `home/data/backend/frontend` | builder |
| `plan_id` | 19 ids | **3 cambios**: `plans/plans`, `tasks/tasks`, `community/guide` | D-05 |
| `pages[].id` | 29 | 26 estables + 3 cambios | D-11 |
| `standing/*` | 6 ids | **estables** (libros, no planes) | D-11 |

### 3.4 Árbol de capítulos (4 toptabs)

```
home       plan · work · community/{docs,feedback,language,channels(+contribution,decisions),levels}
data       content/{index} · schemas/{schemas,mds,json,puzzy(+wire-format,rules)} ·
           ai/{models,skills,flows,levels}
backend    scripts/{contracts,delivery} · systems/{systems} · mynet/{mynet} · storage/{storage}
frontend   apps/{tree,types} · accessibility/{a11y,visual,quality,shell} ·
           experience/{tours,levels}
```

- `section` de cada hito sigue siendo el id de hoja (`contracts`, `tree`, …).
- `path` se escribe completo y empieza por el toptab:
  `contracts → [backend, scripts, contracts]`;
  `levels → [frontend, experience, levels]` (el padre desambigua).
- Las 5 hojas nuevas (`puzzy`, `wire-format`, `rules`, `contribution`,
  `decisions`) son **estructurales** por defecto: `requires_milestone:false`.
  Así se conservan 326 hitos/438 features (D-10).

### 3.5 Profundidad de enlaces relativos y anclas

Se conserva la tabla de v3.2 §3.9 con estas correcciones:

| Origen | Destino | Ajuste |
|---|---|---|
| `plans/**` (sube 1) | `archive/**` (sube 1) | `../` igual |
| `plans/**` | `apps/**`, `tools/**`, `standards/**` | **quitar un** `../` |
| `tasks/**` (sube 1) | `archive/**` | `../` igual |
| `tasks/**` | `standards/**`, `AGENTS.md` | **quitar un** `../` |
| `standards/AI/Skills/**` → `standards/data/ai/skills/**` | standards/tools/AGENTS | **añadir un** `../` |
| `standards/*.md` que baja a `standards/{root}/.../` | fuera de su carpeta | añadir 2–4 `../` |

Regla de anclas: solo cambia el lado fichero; el ancla se conserva. Los
`read_next` muertos (39) se documentan, no se inventan. El ancla rota
`1318-usability-levels-3-minimum-4-function-5-craft` se repara con `<a id>` en
`frontend.md` (D-06), con excepción de bytes en el ledger.

### 3.6 Lo que NO se toca

`tools/docs/**`, `development/standards/index.html` (motor docsify),
`development/blog/**`, `kb/`, `apps/sys/authy/bot/`,
`projects/liberada/risa/build-risa-zip.sh`, subrepo `apps/sys/nety`, contenido
de `archive/` y `tools/dev/_archive/`, los tools del primer intento y los dos
documentos de planeación. `sw.js` y `build-aliases.mjs` **no se editan a mano**;
se regeneran.

---

## 4. Inventario de impacto corregido

### 4.1 Rutas `development/wiki`

| Fichero | refs reales | Acción |
|---|---:|---|
| `development/index.html` | 2.543 | regenerar bloques + 21 líneas estáticas + 13 `wiki/INDEX.md` |
| `development/wiki/work/common.json` | 2.836 | regenerar |
| `development/wiki/port-ledger.json` | 1.569 | remapear 197 destinos; archive-only congelado |
| `development/wiki/chapter-map.json` | 745 | congelar + excluir |
| `register-path-inventory.json` + `.baseline.json` | 427 + 409 | **no regenerar** (procedencia) |
| `development/wiki/wiki.json` | 394 | renombrar + reescribir |
| `milestones.json` | 142 | transformer por allowlist |
| `field-map-review.json` | 55 | congelar + excluir |
| `INDEX.md` | 20 | fuente humana + transformer |
| `task-recycle.json` | ~950 KB | congelar + excluir |

### 4.2 URLs públicas

198 refs en 14 ficheros (`development/index.html` 56, `common.json` 32,
`baseline` 28, `milestones` 27, inventario 27, `field-map-review` 8,
`Community/index.html` 6, `AGENTS.md` 5, migración 4, `skilly.py` 1,
`standards/README.md` 1, `contract.md` 1, 2 skills). Regla:
`https://flove.org/development/wiki/… → https://flove.org/development/…`.

Además, D-14: `404.html` recibe una regla de prefijo
`development/wiki/* → /development/*` para enlaces externos. No es un redirect
de registro; es compatibilidad HTTP generada.

### 4.3 Superficie `standards/` que v3.2 no contaba

| Prefijo | Coincidencias en texto vivo |
|---|---:|
| `standards/AI` | ~1.241 |
| `standards/Frontend` | ~1.466 |
| `standards/Backend` | ~120 |
| `standards/Data`, `standards/Community`, `standards/Docs` | 1, 1, 0 |

Las cifras incluyen proyecciones generadas; tras regenerar bajan. Pero el censo
se hace por campo y fichero, no por un total global.

### 4.4 Campos del registro que v3.2 omitía

`pages[].supersedes[]` (159), `pages[].detail` (2), `labels` (5), `roots` (3),
`milestones[].notes` (147), `milestones[].docs[]` (8),
`development/decision-rules.json` (1), `vocabulary.html` (29),
`pages[].id` de los 29 (19 topics + 6 standing + governance + 2 map).

### 4.5 Redirects, aliases y D-00

- 37 redirects = **26 identidad** (clave = destino, p. ej. `AI/Skills/**`) +
  **11 compatibilidad real**.
- El “9” de v3.2 sale de
  `tools/dev/_archive/taxonomy-migration-2026-11-23/REPORT.md:30`; es el
  subconjunto compat tras colapsar 2. No hay ningún JSON con 9.
- Decisión D-00: conservar las 37 entradas con `kind` (`identity|compat`), o
  podar las 26 identidades y quedarse con 11 (o 9). Default: **37 clasificadas**;
  el gate solo valida las 11 compat.
- 42 aliases → `development/archive/old/…`; sin self, sin cadena, destino
  existente.

### 4.6 Artefactos muertos o congelados

| Artefacto | Consumidor vivo | Política |
|---|---|---|
| `chapter-map.json/.md` | ninguno | congelar + excluir |
| `field-map-review.json/.md` | ninguno | congelar + excluir |
| `task-recycle.json/.md` | `wiki.json` (solo nombre) | congelar + excluir |
| `port-ledger.json` | `check-content`, `check-archive` | remapear destinos (197) |
| `port-ledger.skeleton.json` | ninguno | congelar |
| `register-path-inventory*` | `page-resolve`, provenance | no regenerar |
| `pages.json`, `INDEX.md` | gates | fuente humana + transformer |
| `chapter-decks.py/json` | `index.html` (bloque vivo) | **promover** |
| `build-wiki-skeleton.py` | one-shot | archivar, no regenerar |

### 4.7 Tabla de los 19 planes

| `plan_id` | `plan_page` nuevo | `owner` nuevo |
|---|---|---|
| `ai/flows` | `development/plans/data/flows.md` | `development/standards/data/ai/flows/flows.md` |
| `ai/models` | `development/plans/data/models.md` | `development/standards/data/ai/models/models.md` |
| `ai/skills` | `development/plans/data/skills.md` | `development/standards/data/ai/skills/skills.md` |
| `backend/mynet` | `development/plans/backend/mynet.md` | `development/standards/backend/mynet/mynet.md` |
| `backend/scripts` | `development/plans/backend/scripts.md` | `development/standards/backend/scripts/scripts.md` |
| `backend/storage` | `development/plans/backend/storage.md` | `development/standards/backend/storage/storage.md` |
| `backend/systems` | `development/plans/backend/systems.md` | `development/standards/backend/systems/systems.md` |
| `community/channels` | `development/plans/community/channels/channels.md` | `development/standards/community/channels/channels.md` |
| `community/guide` | `development/plans/community/guide/guide.md` | `development/standards/community/guide/guide.md` |
| `community/feedback` | `development/plans/community/feedback/feedback.md` | `development/standards/community/feedback/feedback.md` |
| `community/language` | `development/plans/community/language/language.md` | `development/standards/community/language/language.md` |
| `data/json` | `development/plans/data/json.md` | `development/standards/data/content/json.md` |
| `data/mds` | `development/plans/frontend/frontend.md` | `development/standards/frontend/frontend.md#1320-data-depth-levels` |
| `data/schemas` | `development/plans/data/schemas.md` | `development/standards/data/schemas/schemas.md` |
| `plans/plans` | `development/plans/plans/plans.md` | `development/standards/plans/plans.md` |
| `tasks/tasks` | `development/plans/tasks/tasks.md` | `development/standards/tasks/tasks.md` |
| `frontend/accessibility` | `development/plans/frontend/accessibility.md` | `development/standards/frontend/accessibility/accessibility.md` |
| `frontend/apps` | `development/plans/frontend/apps.md` | `development/standards/frontend/apps/apps.md` |
| `frontend/experience` | `development/plans/frontend/experience.md` | `development/standards/frontend/experience/experience.md` |

`puzzy.md` no es plan; va a `standards/data/schemas/puzzy.md` y aparece en
`owner_origin` (24 refs, procedencia). `plans/debates/**` no existe hoy; los 747
`owner_origin` históricos se quedan como procedencia o se mapean a
`plans/debates/README.md` según D-03.

---

## 5. Decisiones

### 5.1 Cerradas

| ID | Decisión | Resolución |
|---|---|---|
| D-00 | 9 vs 37 redirects | 37 = 26 identidad + 11 compat. Se conservan clasificadas; el “9” era el subconjunto compat del primer intento |
| D-01 | esquema | `flove-pages-manifest/1`; `check-docs-manifest` actualizado |
| D-02 | enlaces a archive en 5 HTML de apps | reescribir a `development/archive/…` y marcar “(archivado)”; no añadir nuevos |
| D-03 | builders huérfanos | congelar los 3 muertos; remapear `port-ledger`; promover `chapter-decks` |
| D-04 | `jev` | borrar 6 ficheros; limpiar refs; `skilly` 22 → 21 |
| D-05 | ids de plan | 3 cambios (`plans/plans`, `tasks/tasks`, `community/guide`); 16 estables |
| D-06 | ancla rota | `<a id>` en `frontend.md`; excepción de bytes |
| D-07 | 21 líneas estáticas de `index.html` | reescribir rutas/labels; docsify intacto |

### 5.2 Nuevas (requieren respuesta antes de S0)

| ID | Decisión | Default recomendado | ¿Bloquea? |
|---|---|---|---|
| D-08 | ¿Commit local de línea base? | **Sí**, local y etiquetado; sin push | S0 |
| D-09 | Procedencia | **Inmutable**; gates con remap | S2 (default seguro) |
| D-10 | IA: 4 toptabs y 326 vs 331 | **4 toptabs**; 326 hitos y 5 hojas estructurales | **S0** (map/contract) |
| D-11 | IDs: 3 vs 9; `standing/*` | **3 cambios**; `standing/*` estables | **S0** (map/contract) |
| D-12 | Archive vs `check-archive` | **Bytes intactos + `legacy_root`** | S2 (default seguro) |
| D-13 | Artefactos generados | política §4.6 (congelar/promover/fuente) | **S0** (map/contract) |
| D-14 | URLs públicas antiguas | **Prefijo en `404.html`** + breaking documentado | **S0** (map/contract) |
| D-15 | Docsify | motor intacto; contenido y sidebar actualizados | S3 (default seguro) |
| D-16 | Universo de referencias | `development/` + `tools/` obligatorio; `apps/` solo D-02; `whole/`, `docs/` fuera | S4 (default seguro) |
| D-17 | ¿Worktree? | **Sí**, desde la etiqueta de línea base | S1 (default seguro) |

Si el owner acepta los defaults, el plan queda ejecutable de S0 a S6 sin más
preguntas. Si cambia D-10 (331 hitos) o D-11 (9 ids), hay que regenerar
`contract.json` y `map.json` antes de S0.

---

## 6. Ejecución por slices

> “Verde” = sin fallos nuevos frente a §0.3. Los tres fallos base se cierran en
> S0/S3/S5; no se exige que todos estén verdes en cada slice.

### S0 — Spec y línea base (no mueve nada)

1. Crear `migration/` con `map.json`, `contract.json`, fixtures y `rehearsal.md`.
2. Crear `tools/dev/paths.py` con las rutas **actuales**.
3. Crear `check-map.py`, `check-paths.py`, `check-redirects.py`, `check-urls.py`.
   `check-paths.py` arranca en modo **baseline**: registra los prefijos
   hardcodeados que ya existen; solo falla por prefijos nuevos. Se vuelve
   estricto en S1–S2.
4. Añadir `RESTART-PLAN.md` y `RESTART-PLAN-REVIEW.md` al `SKIP` de
   `check-retired-paths.py`; limpiar `__pycache__` y `.kate-swp` del árbol de
   trabajo.
5. Commit local `migration-baseline-2026-11-24`; worktree desde la etiqueta.
6. Gate: `check-retired-paths` verde; el resto igual que §0.3; `check-map`
   verde y `check-paths` verde en modo baseline (0 prefijos nuevos).

### S1 — Herramientas

1. `git mv tools/dev/wiki/*.py tools/dev/checks/`; renombrar
   `wiki-inventory.py → page-inventory.py`, `wiki-resolve.py → page-resolve.py`.
2. `git mv tools/dev/work tools/dev/tasks`; promover `chapter-decks`.
3. Actualizar `jsony.py` (`sys.path`), imports, `check-taxonomy.py`
   (`GEN`/`REG`), `tasky.py` (`REGISTER`) y `tools/README.md`.
4. `paths.py` sigue apuntando a las rutas actuales de `development/`.
5. Gate: `build-work-tracker --check`, `build-common --check`, `jsony`,
   `check-links`, `check-routing`, `skilly` (22 skills todavía; `jev` se borra
   en S3), `check-taxonomy` sigue en 497 (baseline).

### S2 — Registro

1. Mover `development/wiki/archive → development/archive`,
   `plans → development/plans`, `work → development/tasks`,
   `wiki.json → pages.json`, y el resto de `wiki/*` a `development/*`.
2. Cambiar `paths.py` a las rutas nuevas en el mismo commit del slice.
3. Reescribir `pages.json`: 29 páginas, 19 planes, `detail`, `supersedes` (159),
   `labels`, `roots`, `plans[].sources`, `redirects` (26+11), `aliases` (42).
4. Arreglar `LinkIndex` con el emparejamiento `pages[].id → pages[].path`.
5. Actualizar `check-docs-manifest` (`pages.json`, `INDEX.md`, prefijo
   histórico `development/`), `check-page-status`, `check-plan-tray`,
   `check-archive` (`legacy_root`), `check-content` (ruta del ledger; sus
   destinos siguen en `standards/` hasta S3).
6. Regenerar `common.json` y `WORK-DATA`.
7. Gate: **sin fallos nuevos**; `check-docs-manifest` mantiene el error base de
   `skills.md` (se cierra en S3); `LinkIndex` 19/19; `common.json`
   2.690/2.690/2.700; `check-links` verde.

### S3 — Standards

1. Mover `standards/` a subcarpetas y minúsculas (§3.2); retirar directorios
   vacíos; borrar `jev/`.
2. Reescribir `pages[].path`, `field_map` (29), `owner` (1.559), `notes` (147),
   `docs` (8), `standards[]` (140), `supersedes` (159).
3. Frontmatter y `CONTEXT` de los 19 topics; `wiki.md`; `README.md`;
   corregir el checker del sidebar para que exija la ruta relativa, no el
   basename.
4. Remapear los 197 `destination` del `port-ledger` a las rutas nuevas;
   actualizar bases de `check-links`, `check-content`, `check-archive`.
5. Regenerar `common.json` y `WORK-DATA`.
6. Gate: `check-docs-manifest` verde (incluye el id de `skills.md`);
   `check-links` verde; `LinkIndex` 19/19; `check-content` verde; `skilly`
   21 skills sin `jev`.

### S4 — Barrido

1. Tools, skills, `AGENTS.md`, `tools/README.md`, PROC URLs.
2. `index.html`: 21 líneas estáticas, 13 `wiki/INDEX.md`, script-folds, lista de
   checks; `chapter-decks` desde su builder promovido.
3. `apps/` D-02 (5 archivos) y URLs públicas (198 refs).
4. `404.html`: prefijo `development/wiki/*` (D-14); regenerar `sw.js` y aliases.
5. Regenerar **otra vez** las proyecciones tocadas por `AGENTS.md`/notas.
6. Gate: `check-retired-paths` verde con allowlist; `check-urls` verde;
   `skilly` 21; `build-*` verdes.

### S5 — IA y URL

1. `build-work-tracker.py`: `TABS` (4), `MAX_DEPTH=4`, `filter_order` (17),
   `AXES` árbol; `canonical()` con `max_depth` y `path` en cada fila.
2. `milestones.json`: `path` en 326 hitos + 37 tickets; `section` mapeado;
   5 hojas estructurales.
3. Porte del runtime (`main.js`): `TOPTABS`, `TREE`, `PATHS`, `capitulo`,
   alias `docs→home`, `ai→data`.
4. `parseHash`/`writeHash`: `toptab`, `tab`, `capitulo`, `view`, `q`; 4 anchors;
   `#axis-subtabs` intacto.
5. `check-taxonomy`: la spec de 4 raíces ya existe; solo se ajusta la
   derivación de filas si el árbol nuevo lo exige. No se reescribe el contrato
   para hacerlo pasar.
6. Gate: `check-taxonomy` 0; paridad Plan/Work; matriz de URLs; consola limpia;
   640 px; reduced motion.

### S6 — Cierre

1. Doble build de los 5 builders (`build-work-tracker`, `build-common`,
   `build-index-stubs`, `build-community-stages`, `build-chapter-decks`);
   hashes idénticos.
2. Matriz baseline → final de los 13 gates + 4 nuevos.
3. `REPORT.md` + `SHA256SUMS`; `git diff --check`; `git status`.
4. Rollback drill de un slice.
5. Sin commit publicado ni push.

### Mapa con las fases de v3.2

| v3.2 | v4.0 |
|---|---|
| Fase 0 | S0 |
| Fase 1 | S1 + S2 + S3 (tres slices) |
| Fase 2 | S2 + S3 + S5 |
| Fase 3 | S2 + S3 + S4 |
| Fase 4 | S4 |
| Fase 5 | S5 |
| Fase 6 | S5 |
| Fase 7 | S6 |
| Fase 8 | S6 |

---

## 7. Matriz de propiedad

| Fichero | Dueño / política |
|---|---|
| `tools/dev/tasks/build-work-tracker.py` (`TABS`/`AXES`/`MAX_DEPTH`/`parts`) | edición humana |
| `development/tasks/milestones.json` y frontmatter | edición humana + transformer |
| bloque `WORK-DATA` | `build-work-tracker.py` |
| `development/tasks/common.json` | `build-common.py` |
| bloques `STUBS` / `COMMUNITY` | `build-index-stubs.py`, `build-community-stages.py` |
| bloque `CHAPTER-DECKS` | `build-chapter-decks.py` (**promovido**) |
| `development/pages.json` | fuente humana + transformer |
| `development/INDEX.md` | fuente humana + transformer |
| `port-ledger.json` | remapear destinos; no congelar entero |
| `chapter-map`, `field-map-review`, `task-recycle` | congelar + excluir |
| `register-path-inventory*`, `register-path-migration` | procedencia; no regenerar |
| `sw.js`, `404.html` | regenerar; no editar a mano |
| `tools/apps/routing.json` (3 refs a `standards/AI`) | `extract-fields.py --apply` |

---

## 8. Checklist de aceptación

- [ ] Línea base local etiquetada; 13 gates base registrados.
- [ ] `map.json` y `contract.json` verdes; ninguna tabla de prosa decide.
- [ ] `paths.py` centraliza rutas; 0 prefijos retirados en scripts vivos.
- [ ] Ledger: cada movimiento conserva sha256; excepciones declaradas.
- [ ] Archive: bytes intactos **y** `check-archive` verde con `legacy_root`.
- [ ] Procedencia inmutable; `owner_origin` 1.471 con ruta, no 1.559.
- [ ] 29 páginas y 19 planes con `path`, `detail`, `supersedes`, `sources`.
- [ ] 37 redirects clasificados (26 identidad + 11 compat); 42 aliases.
- [ ] `LinkIndex`: 19/19 pares; 2.690/2.690/2.700; 438 features.
- [ ] 326 hitos y 37 tickets con `path`; `check-taxonomy` verde.
- [ ] `standards/` sin rutas viejas; `check-links` verde (128+).
- [ ] `index.html` estático y chapter-decks con dueño; bloques intactos.
- [ ] `toptab`/`capitulo` con compatibilidad de URL antigua.
- [ ] 13 gates + 4 nuevos; doble build idéntico; `git diff --check`.
- [ ] `archive/` y `_archive/` byte a byte; sin push.

---

## 9. Rollback

1. Base: `migration-baseline-2026-11-24`.
2. Un slice = movimientos + rewrites + gate.
3. Revertir un slice con `git restore --source=<baseline> -- <paths>` o el
   inverso de `map.json`.
4. `move-ledger.json` se genera desde `git diff -M --name-status` + hashes.
5. Nunca `reset --hard`; nunca restaurar `archive/`.

---

## 10. Estado de preparación

**Preparado:** el plan ya tiene spec, árbol, mapeos, counts, gates, slices y
rollback. No quedan dudas de contenido; solo decisiones de owner.

**S0 se puede empezar en cuanto respondas las cinco.** D-08 habilita el
baseline; D-10, D-11, D-13 y D-14 fijan `map.json` y `contract.json`. S0 no
mueve ficheros, pero el mapa ya codifica esas cuatro; por eso se resuelven
**antes de escribir el mapa**, no al final.

**Necesito respuesta del owner antes de S0** en estas cinco:

1. **D-08** — ¿Autorizas el commit local de línea base (sin push)?
   Recomendado: sí.
2. **D-10** — ¿4 toptabs y 326 hitos (5 hojas estructurales) o 331 hitos?
   Recomendado: 4 toptabs, 326.
3. **D-11** — ¿3 ids de plan (`plans/plans`, `tasks/tasks`, `community/guide`)
   y `standing/*` estables? Recomendado: sí.
4. **D-13** — ¿Congelar `chapter-map`, `field-map-review` y `task-recycle`, y
   promover `chapter-decks`? Recomendado: sí.
5. **D-14** — ¿Compatibilidad de URLs antiguas vía prefijo en `404.html`, o
   aceptar el 404 y documentarlo? Recomendado: prefijo.

D-09, D-12, D-15, D-16 y D-17 tienen default seguro y no bloquean si no dices
nada.

Con un “adelante con los defaults” empiezo por S0: baseline, mapa, contrato,
`paths.py`, gates y worktree. Te entrego el primer gate verde antes de mover
ningún fichero.
