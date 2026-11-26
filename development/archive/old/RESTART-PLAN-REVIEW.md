# Revisión del RESTART-PLAN v3.2 — bloqueos, huecos y backlog derivado

Estado: **revisión read-only**, 2026-11-24. No modifica `RESTART-PLAN.md`.
Idioma de trabajo: español. No commit, no push.

> **Actualización:** `RESTART-PLAN.md` ya está en v4.0 e incorpora los
> bloqueos, decisiones y slices de este documento. Esta revisión queda como
> evidencia de por qué v4.0 es así; no es un segundo plan.

> Documento de planeación, no contenido. Igual que `RESTART-PLAN.md`, debe
> excluirse de `check-retired-paths.py`, de `check-links.py` y del grep de la
> Fase 4 cuando se implemente la migración. Hoy **no** está excluido: el gate
> falla solo por citar el plan.

---

## 0. Método y línea base verificada

Contrastado contra el árbol real, no contra el plan anterior.

- `git status --porcelain`: **93 entradas** (39 `M`, 2 `MM`, 28 `D`, 12 `RM`,
  1 `AM`, 1 `R`, 10 `??`). `development/index.html` está en `MM`.
- `backup.tgz` existe en `/tmp/opencode/flove-taxonomy-2026-11-23/`, pero su
  `development/index.html` **no coincide** con el actual
  (`2efd1c42…` vs `81ce8ecb…`). La puerta “byte a byte contra backup.tgz” de la
  Fase 0 no puede pasar tal como está escrita.
- Registro: 29 páginas · 19 planes · 37 redirects · 42 aliases · 29 `field_map`
  · 5 `labels` · 3 `roots` · 2 `excluded_live`.
- Registro de trabajo: 326 hitos · 37 tickets · 1.559 live · 805 archived.
- Gates de hoy:
  - **OK**: `build-work-tracker --check`, `build-common --check`, `jsony`,
    `skilly` (0 errores, 47 warnings), `check-archive`, `check-content`,
    `check-plan-tray`, `check-page-status`, `check-links` (128 docs),
    `check-routing`.
  - **FAIL**: `check-taxonomy` (497 errores), `check-docs-manifest` (1 error
    base en `skills.md`), `check-retired-paths` (1: el propio plan).
- Existe un intento anterior completo y verificado en
  `tools/dev/_archive/taxonomy-migration-2026-11-23/`: `map.json`,
  `apply-taxonomy.py`, `rewrite-links.py`, `audit-taxonomy.py`,
  `recycle-content.py`, `REPORT.md`, más `main.js` y `NEW-TREE.txt` en
  `/tmp/opencode/flove-taxonomy-2026-11-23/`.

---

## 1. Veredicto

El plan **acierta en la dirección**: separa fuentes de proyecciones, identifica
el fallo real de `LinkIndex` (§3.8), ordena `milestones → pages → LinkIndex →
common → bloques`, y conserva un ledger de movimientos. Eso es sólido.

Pero **no es todavía un spec ejecutable**. Hay seis bloqueos, nueve
contradicciones internas y diez huecos de especificación. El mayor riesgo no es
un enlace roto: es que el plan se apoya en cifras y tablas escritas a mano que
el árbol ya no cumple, mientras existe un `map.json` ejecutable del intento
anterior que dice otra cosa. Si se ejecuta tal cual, se repetirá el fallo del
primer intento con más trabajo manual y sin una puerta intermedia verde.

Recomendación: **no empezar por la Fase 1**. Empezar por un slice 0 de
especificación y línea base (ver §8), y reutilizar o superar explícitamente el
`map.json` archivado.

---

## 2. Lo que está bien y conviene conservar

1. La corrección de inventario: 37 redirects y 42 aliases son reales.
2. La regla “fuente → builder dueño → `--check`”.
3. El diagnóstico de `LinkIndex`: `STANDARDS + topic + ".md"` deja 2.690
   `plan_id`/`plan_page` vacíos tras mover `standards/*.md`. Verificado en
   `tools/dev/work/register_projection.py:91-101`.
4. El orden `milestones → pages → LinkIndex → common → bloques`.
5. El ledger `origen · sha256 antes · sha256 después`.
6. Las reglas de profundidad de enlaces relativos (§3.9) y la conservación de
   anclas (§3.10).
7. La exclusión de `archive/` y de docsify como motor.

---

## 3. Bloqueos

### B1 — Línea base no reproducible

El árbol ya está sucio antes de empezar: 93 entradas, `index.html` en `MM`,
`check-counts.py` borrado, `build-chapter-decks.py` sin trackear. El plan
solo guarda `git status`; eso no permite atribuir un diff a la migración ni
restaurar el estado exacto. Además el `backup.tgz` disponible no coincide con
`index.html`.

**Corrección**: crear una línea base inmutable antes de mover nada (commit
local, bundle o `commit-tree` colgado) con `HEAD`, árbol, hashes y salida de
los 13 gates. Sin eso, el rollback de la Fase 8 es una ilusión.

### B2 — Contrato de procedencia contradictorio

`tools/README.md` y `check-retired-paths.py` dicen explícitamente que
`owner_origin`, `register-path-inventory*`, `register-path-migration.json` y
`archive/old/` **conservan rutas históricas**. El plan reescribe 1.559
`owner_origin` y regenera inventario y baseline.

Además la cifra es falsa: hay 1.559 `owner_origin` presentes, pero solo
**1.471** contienen una ruta `development/…`; los otros 88 son otra cosa.
Igual con `evidence.pointer.value`: 1.559 presentes, **1.401** con ruta. Un
rewrite de 1.559 tocaría valores que no son rutas.

**Corrección**: decidir D-09. Recomendado: procedencia inmutable y un mapa de
lectura para gates; o una procedencia v2 versionada, nunca un rewrite in situ.

### B3 — `archive/` intacto contra `check-archive` verde

`development/wiki/archive/manifest.json` tiene `"root":
"development/wiki/archive/old"`. `check-archive.py:52` compara ese root con la
ruta real. Al mover el archivo a `development/archive/`, el gate falla aunque
los bytes estén intactos. El plan exige las dos cosas a la vez.

**Corrección**: decidir D-12. Opciones: (a) permitir un `legacy_root` en el
checker sin tocar el manifiesto; (b) reescribir el manifiesto y aceptar la
excepción de bytes; (c) no mover `archive/` y dejar una ruta puente.

### B4 — Artefactos generados sin política de dueño

La Fase 4 manda reescribir a mano `pages.json`, `INDEX.md`, mapas, ledgers,
inventario y recycle, mientras el principio 1 prohíbe editar generados y D-03
dice congelar los builders. No se puede hacer las tres cosas.

Datos concretos:

- `build-wiki-skeleton.py` es un one-shot que **se niega a sobrescribir**;
  `pages.json` e `INDEX.md` ya no tienen builder activo. No se “regeneran”:
  se editan como fuentes o se les da un transformer.
- `check-content.py` lee `port-ledger.json` y exige que existan 197
  destinos bajo `development/standards/`. Congelar el ledger con rutas viejas
  rompe el gate.
- `chapter-map.json`, `field-map-review.json` y `task-recycle.json` no tienen
  consumidor vivo: solo los citan `wiki.json` (como nombre de fichero),
  `check-retired-paths` (SKIP) y el índice HTML. Reescribir 745/55/950 KB es
  trabajo muerto; lo correcto es retirarlos o archivarlos.

**Corrección**: matriz de propiedad por artefacto con tres estados:
**promover builder**, **fuente humana**, **retirar**. Ver tarea MIG-12.

### B5 — La spec de taxonomía está incompleta

`check-taxonomy.py` es el contrato ejecutable y hoy falla con 497 errores:

- espera `tabs == ["home","data","backend","frontend"]`, el generador devuelve
  los 6 antiguos;
- espera `MAX_DEPTH == 4`, el generador no tiene `MAX_DEPTH`;
- exige `item["path"]` en cada hito y ticket: **326 + 37 vacíos**;
- exige que `section` sea un id del árbol; `contracts` y `delivery` no están
  en `backend` como nodos de primer nivel.

El plan edita `TABS`, `AXES` y `parts` en la Fase 2, pero **no especifica**
`path`, `section`, `max_depth` ni `filter_order`. Sin eso, la Fase 5 no puede
poner `check-taxonomy` en verde.

**Corrección**: tratar `check-taxonomy.py` como la spec de la taxonomía y
derivar de ahí el árbol, los paths y los conteos.

### B6 — La superficie de referencias está subestimada

El plan cuenta `wiki` y `work`, pero no el reorg de mayúsculas y profundidad de
`standards/`:

- `standards/AI`: ~1.241 coincidencias en texto vivo (59 ficheros).
- `standards/Frontend`: ~1.466.
- `standards/Backend`: ~120.
- `standards/Data`, `standards/Community`, `standards/Docs`: casi cero
  (1, 1, 0), así que el coste real está en AI y Frontend.

Y faltan campos del registro:

- `pages[].supersedes`: **159** rutas de archivo.
- `pages[].detail`: 2.
- `labels`: 5.
- `roots`: 3.
- `milestones[].notes`: **147** con rutas en prosa.
- `milestones[].docs`: 8.
- `development/decision-rules.json`.
- `vocabulary.html`: 29 rutas.
- `apps/`, `whole/`, `docs/`: fuera del gate `development tools`, pero con
  enlaces que se rompen.

**Corrección**: censo por campo y por directorio, no por recuento global de
`wiki`.

---

## 4. Contradicciones internas

| # | El plan dice | El árbol dice | Corrección |
|---|---|---|---|
| C1 | D-05: cambian 3 `plan_id`; se mantienen 16 | `map.json` del intento anterior renombra **9** (`home/plan`, `home/work`, `home/*`, `data/*`) | Cerrar D-11: 3 o 9, no ambas |
| C2 | 326 hitos intactos | El árbol nuevo añade 5 hojas (`puzzy`, `wire-format`, `rules`, `contribution`, `decisions`); el intento anterior esperaba **331** hitos y **443** features | Cerrar D-10: añadir 5 hitos o marcar 5 hojas `requires_milestone:false` |
| C3 | `TABS`: “5 raíces: home, data, backend, frontend” | Son **4**; el mapa archivado también tiene 4 | Corregir a 4 |
| C4 | “Sin rediseño… solo 4 anchors, `parseHash`, `writeHash` y 2 puntos de render” | `main.js` del intento anterior tiene 1.731 líneas frente a 1.620 actuales; el diff es de ~857 líneas (`indexTree`, `chapterInfo`, `resolveTab`, `capitulo`, `qmode`, `TOPTABS`) | Reconocer el porte de runtime como tarea propia |
| C5 | “Docsify no se toca” | `wiki.md` es contenido docsify y debe cambiar; `check-docs-manifest` lo valida | Distinguir motor (intacto) de contenido (se actualiza) |
| C6 | `sw.js` y `build-aliases.mjs` “no se tocan” | La Fase 3 ejecuta `build-sw.mjs` y `build-aliases.mjs`, que los reescriben | Decir “no se editan a mano; se regeneran” |
| C7 | Fase 3 regenera; Fase 4 edita fuentes | La Fase 4 toca `AGENTS.md` (PROC), `milestones` en prosa y el registro | Mover esas ediciones a la Fase 2 o añadir una regeneración final |
| C8 | Fase 2 reescribe `pages.json` | Fase 4.1 lo vuelve a reescribir | Una sola fase para el registro |
| C9 | El plan “se excluye del gate” | `check-retired-paths` falla hoy solo por el plan | Añadirlo a `SKIP` en la Fase 0 |
| C10 | “Conservar los 37 redirects” | 26 de 37 son **self-redirects** (clave = destino); solo 11 redirigen de verdad | Separar identidades de redirects reales |

Sobre D-00: el **9** no sale de un JSON, sale de
`tools/dev/_archive/taxonomy-migration-2026-11-23/REPORT.md:30`
(“9 redirects de compatibilidad”). Es el subconjunto no-identidad del intento
anterior; hoy hay 11 no-identidad. D-00 se puede cerrar con esa evidencia.

---

## 5. Huecos de especificación

| # | Hueco | Consecuencia |
|---|---|---|
| G1 | No hay un `map.json` vigente; las tablas §2.1/§2.2/§3.8 son prosa duplicada | Deriva: ya hay cifras, rutas y decisiones distintas entre secciones |
| G2 | No hay registro único de rutas para scripts | 15+ scripts con constantes hardcodeadas; el movimiento rompe gates en cadena |
| G3 | No hay inventario por campo JSON con allowlist | Un rewrite genérico toca prosa, procedencia o `notes` |
| G4 | No hay checker de redirects/aliases | 26 self-redirects, cadenas y claves que colisionan con páginas vivas |
| G5 | No hay política de archive | `check-archive` y “bytes intactos” se excluyen |
| G6 | No hay matriz de propiedad de artefactos | Generados editados a mano o congelados que rompen gates |
| G7 | No hay spec de URLs públicas | `flove.org/development/wiki/...` no tiene motor de redirect HTTP; `404.html` no las conoce |
| G8 | `check-links` solo mira `standards/` + `wiki/`; el sidebar se valida por basename | Un enlace `plans.md` roto pasaría |
| G9 | No hay worktree ni ensayo | Se migra el árbol sucio real, sin comparación limpia |
| G10 | Los gates actuales no son la spec de aceptación | `check-taxonomy` 497 y `check-docs-manifest` 1 quedan como “baseline” sin plan de cierre |

---

## 6. Plan contra repo: cifras que hay que corregir

| Afirmación del plan | Dato real | Nota |
|---|---:|---|
| 9.423 refs `development/wiki` | ~10.257 en 72 ficheros (scope propio) | El método no está declarado |
| `index.html` 2.648 | 2.543 | Deriva |
| `common.json` 2.879 | 2.836 | Deriva |
| `milestones.json` 175 | 142 | Deriva |
| `port-ledger` 1.581 | 1.569 | Deriva |
| `wiki.json` 396 | 394 | Deriva |
| 1.559 `owner_origin` | 1.559 presentes / 1.471 con ruta | Presencia ≠ ruta |
| 1.559 pointers | 1.559 presentes / 1.401 con ruta | Presencia ≠ ruta |
| 363 `source` | 280 | Inflado |
| 326 `standards[]` | 140 | Inflado (326 es el nº de hitos) |
| 107 de 416 ficheros | 72 ficheros con refs en `development/` (scope distinto) | Declarar el censo |
| 37 redirects | 37, de los que 26 son identidad | Ver C10 |

Regla propuesta: **ninguna cifra del plan se escribe a mano**. El transformer
las emite y el gate las compara.

---

## 7. Decisiones a cerrar antes de la Fase 1

| ID | Decisión | Recomendación |
|---|---|---|
| D-00 | 9 vs 37 redirects | Cerrar con `REPORT.md`: 9 = compatibilidad real; 37 incluye 26 identidades. Conservar 9–11 reales + 26 identidades documentadas |
| D-08 | ¿Se permite un commit local de línea base? | Sí. “No commit” debe significar “no publicar”, no “no fijar el estado inicial” |
| D-09 | Procedencia (`owner_origin`, inventario, baseline) | Inmutable. Gates leen con remap; no se reescribe |
| D-10 | Árbol: 4 toptabs; ¿dónde viven community y ai? ¿326 o 331 hitos? | Adoptar el `map.json`: `home` contiene community; `data` contiene ai; decidir 331 o `requires_milestone:false` |
| D-11 | IDs de plan: 3 o 9 | Adoptar una tabla única; recomendado el `map.json` (9) si se reutiliza su runtime |
| D-12 | Archive: bytes vs `check-archive` | Mantener bytes y permitir `legacy_root` en el checker |
| D-13 | Artefactos generados | Promover / fuente humana / retirar, por fichero |
| D-14 | URLs públicas antiguas | Generar un mapa `development/wiki/* → development/*` en `404.html` o aceptar el 404 documentado |
| D-15 | Docsify | Motor intacto; `wiki.md` y enlaces de contenido se actualizan |
| D-16 | Universo de referencias | `development/` + `tools/` obligatorio; `apps/`, `whole/`, `docs/` por decisión explícita |
| D-17 | ¿Worktree para ejecutar? | Sí: worktree limpio desde la línea base; el árbol actual queda como referencia |

---

## 8. Modelo de fases propuesto: slices verdes

El plan actual mueve todo el árbol, luego edita fuentes, luego regenera: hay
dos fases sin gates posibles. Para un desarrollo guiado por spec, cada slice
debe terminar con el repo ejecutable.

| Slice | Contenido | Gate de salida |
|---|---|---|
| **S0** | Línea base + `map.json` + contrato + `paths.py` + transformer + fixtures | Los 13 gates actuales, con baseline documentado |
| **S1** | Herramientas: `tools/dev/wiki` → `checks`, `work` → `tasks`; constantes vía `paths.py` | `build-*`, `jsony`, `check-links` verdes sin tocar `development/` |
| **S2** | Registro: `wiki/` → `pages.json` + `plans/` + `tasks/`; `LinkIndex`; `INDEX.md`; redirects/aliases | `check-docs-manifest` verde (salvo deuda declarada), 19 pares de plan no vacíos |
| **S3** | Standards: subcarpetas, minúsculas y `data/ai`; frontmatter, `field_map`, `supersedes`, sidebar | `check-links` verde, `check-taxonomy` verde, `check-docs-manifest` verde |
| **S4** | Barrido: tools, skills, index.html estático, apps, URLs públicas, `AGENTS.md` | `check-retired-paths` verde con allowlist; 0 rutas vivas |
| **S5** | IA/URL: `toptab`/`capitulo`, runtime, 4 anchors, `parseHash`/`writeHash` | `check-taxonomy` + paridad Plan/Work + matriz de URLs |
| **S6** | Cierre: doble build, hashes, rollback drill, informe | Todos los gates, `git diff --check`, ledger completo |

Ventaja: S1–S4 pueden hacerse en un worktree y verificarse por separado; si un
slice falla, se revierte solo ese slice.

---

## 9. Backlog derivado (formato PROC-08)

Dueño estable de las tareas de migración hasta el cierre:
`development/archive/old/RESTART-PLAN.md`. Evidencia: comando, ancla o estado.

### S0 — Spec y línea base

| ID | Tarea | Hecho cuando | Evidencia |
|---|---|---|---|
| MIG-01 | Fijar línea base reproducible | Existe un árbol/commit local con `HEAD`, hashes y salida de los 13 gates; `backup.tgz` verificado o descartado con motivo | `migration/baseline.json` + `sha256sum` |
| MIG-02 | Escribir `migration/map.json` v2 | Una entrada por ruta, id, campo, redirect y alias; sin duplicados; destinos existentes en el árbol objetivo | `python3 tools/dev/migrate/check-map.py` |
| MIG-03 | Escribir el contrato de invariantes | 326/331 hitos, 1.559 live, 805 archived, 438/443 features, 37/42 o 9/42, bytes de archive, anclas 31→31 | `migration/contract.json` + gate |
| MIG-04 | Crear `tools/dev/paths.py` | Todos los scripts leen rutas de un solo módulo; ningún `development/wiki` hardcodeado en `.py` vivo | `python3 tools/dev/checks/check-paths.py` |
| MIG-05 | Escribir el transformer con `--check` | Reescritura por allowlist JSON + tokens de prosa; dry-run y diff estructural; no toca procedencia | `python3 tools/dev/migrate/rewrite.py --check` |
| MIG-06 | Golden fixtures y diff estructural | 1 hito, 1 ticket, 1 plan, 1 página y 1 tarea antes/después; solo cambian campos permitidos | `migration/fixtures/` + test |
| MIG-07 | Extender gates | `check-redirects`, `check-map`, `check-paths`, `check-urls`; `check-links` cubre plans/tasks/standards/root; sidebar por ruta, no basename | `bash tools/apps/v1/check-distro.sh` + 4 nuevos |
| MIG-08 | Ensayo y rollback | Migración completa en worktree limpio; restaurar un slice y repetir; tiempo medido | `migration/rehearsal.md` |

### S1 — Herramientas

| ID | Tarea | Hecho cuando | Evidencia |
|---|---|---|---|
| MIG-09 | Mover `tools/dev/wiki` → `checks` y `work` → `tasks` | 15 checkers y 10 ficheros de tasks; `py_compile`; gates verdes | `git status` + `check-distro` |
| MIG-10 | Reescribir constantes de los 15 scripts | `jsony`, `tasky`, `register_projection`, `build-*`, `check-*`, `skilly` leen `paths.py`; 0 constantes viejas | `check-paths.py` |
| MIG-11 | Mover `page-inventory`/`page-resolve` y decidir inventario | Inventario histórico inmutable o v2; baseline no regenerado | `tools/README.md#provenance` |
| MIG-12 | Política de artefactos huérfanos | `chapter-map`, `field-map-review`, `task-recycle`: retirados o promovidos; `port-ledger`: destinos remapeados; `pages.json`/`INDEX.md`: fuente humana declarada | `migration/ownership.md` |
| MIG-13 | Chapter-decks | Builder promovido o bloque congelado con allowlist; los 13 `wiki/INDEX.md` reescritos por su dueño | `build-chapter-decks.py --check` |

### S2 — Registro

| ID | Tarea | Hecho cuando | Evidencia |
|---|---|---|---|
| MIG-14 | Renombrar `wiki.json` → `pages.json` y esquema | `flove-pages-manifest/1`; 29 páginas; `check-docs-manifest` actualizado | `check-docs-manifest --check` |
| MIG-15 | Reescribir las 29 páginas y 19 planes | `path`, `detail`, `supersedes` (159), `labels`, `roots`, `plans[].sources`; ids según D-11 | diff estructural + `check-docs-manifest` |
| MIG-16 | Cerrar redirects/aliases | 9–11 reales + 26 identidades; 42 aliases; sin self, sin cadena, sin clave viva, destino existente | `check-redirects.py` |
| MIG-17 | Arreglar `LinkIndex` | 19 pares `plan_id`/`plan_page` no vacíos; 2.690/2.690/2.700 en `common.json` | `build-common --check` + test de 19 owners |
| MIG-18 | Reconstruir `INDEX.md` | Tabla de topics = manifest; 19 planes; 33 filas históricas al archivo nuevo | `check-docs-manifest` |
| MIG-19 | Regenerar proyecciones del registro | `common.json`, `WORK-DATA`, `STUBS`, `COMMUNITY`; doble build idéntico | `build-* --check` |

### S3 — Standards y referencias

| ID | Tarea | Hecho cuando | Evidencia |
|---|---|---|---|
| MIG-20 | Censo y reescritura de `standards/` | AI/Frontend/Backend/Data/Community/Docs mapeados; 0 rutas viejas en texto vivo | `grep` con allowlist |
| MIG-21 | Frontmatter y `CONTEXT` | 19 topics con `id`, `path`, `section`, `also`, `html_place`, `owns`; `supersedes` al archivo nuevo; sidebar corregido | `check-docs-manifest` |
| MIG-22 | Enlaces relativos por profundidad | 19 planes + 124 standards + 11 tasks; `../` correcto; 0 nuevos roto | `check-links --check` |
| MIG-23 | `milestones` en prosa | 147 `notes`, 8 `docs`, 140 `standards[]`, 1.559 owner, 1.401 pointers, 280 source; anclas intactas | `rewrite.py --check` |
| MIG-24 | Superficie estática de `index.html` | 13 `wiki/INDEX.md`, 21 líneas estáticas, script-folds, lista de checks; bloques generados intactos | `grep` + `build-work-tracker --check` |
| MIG-25 | Tools, skills, `AGENTS.md`, `README` | 15 scripts, 4+ SKILL.md, PROC URLs, `tools/README` lanes; `skilly` 21 skills sin `jev` | `skilly.py` + `check-retired-paths` |

### S4 — IA y URL

| ID | Tarea | Hecho cuando | Evidencia |
|---|---|---|---|
| MIG-26 | Árbol de 4 toptabs y `path` por hito/ticket | `check-taxonomy` verde; `MAX_DEPTH=4`; 326/331 paths; `filter_order` | `check-taxonomy.py` |
| MIG-27 | Runtime `toptab`/`capitulo` | Porte del diff de `main.js`; alias `docs→home`, `ai→data`; sin CSS nuevo | paridad `canonical()` |
| MIG-28 | `parseHash`/`writeHash` y compatibilidad | URL canónica `#work?toptab=…&tab=…&capitulo=…`; URLs antiguas resuelven; 4 anchors | matriz de URLs + consola limpia |
| MIG-29 | Filas y cards de subsección | Una card por subsección declarada; filas Work desde el mismo origen; 20 subsecciones | `check-taxonomy` + inspección |
| MIG-30 | URLs públicas | 198 refs reescritas; decisión D-14 aplicada (404 o breaking documentado); 5 apps D-02 | `check-urls.py` + `build-aliases.mjs` |

### S5 — Cierre

| ID | Tarea | Hecho cuando | Evidencia |
|---|---|---|---|
| MIG-31 | Matriz baseline → final | Los 13 gates: 0 fallos nuevos; los 3 fallos base resueltos o documentados; doble build idéntico | `migration/gates.csv` |
| MIG-32 | Informe y rollback drill | `REPORT.md` + `SHA256SUMS`; restaurar un slice y verificar; sin commit ni push | `migration/rollback.md` |

---

## 10. Matriz de aceptación corregida

- [ ] Línea base fijada y gates base registrados.
- [ ] `map.json` es la única fuente de rutas; ninguna tabla de prosa decide.
- [ ] `paths.py` centraliza rutas; 0 prefijos retirados en scripts vivos.
- [ ] Archive: bytes intactos **y** `check-archive` verde con `legacy_root`.
- [ ] Procedencia inmutable o v2; 0 rewrites silenciosos de `owner_origin`.
- [ ] 29 páginas y 19 planes con `path`, `detail`, `supersedes`, `sources`.
- [ ] Redirects: 9–11 reales + 26 identidades; 42 aliases; checker verde.
- [ ] `LinkIndex`: 19/19 pares; 2.690/2.690/2.700; 438/443 features.
- [ ] 326/331 hitos decidido; 0 paths vacíos; `check-taxonomy` verde.
- [ ] `standards/` sin rutas viejas; `check-links` verde (128+ docs).
- [ ] `index.html` estático y chapter-decks con dueño; bloques generados intactos.
- [ ] `toptab`/`capitulo` con compatibilidad de URL antigua.
- [ ] 13 gates + 4 nuevos; doble build idéntico; `git diff --check` limpio.
- [ ] `archive/` y `_archive/` byte a byte; sin commit ni push.

---

## 11. Rollback

El rollback por `backup.tgz` no basta: el backup disponible no coincide con
`index.html` y no cubre los 10 untracked. Propuesta:

1. Línea base en commit/bundle local (S0).
2. Un slice = un conjunto de movimientos + rewrites + gate.
3. Rollback de slice: `git restore --source=<baseline> -- <paths>` o aplicar
   el inverso del `map.json` con el transformer.
4. `move-ledger.json` generado desde `git diff -M --name-status` + hashes, no
   escrito a mano.
5. Nunca `reset --hard`; nunca restaurar `archive/`.

---

## 12. Siguiente acción recomendada

1. Aprobar o rechazar D-08…D-17 (§7).
2. Crear S0: baseline + `map.json` v2 + contrato + `paths.py`.
3. Reutilizar `map.json` del intento anterior como punto de partida; diff
   explícito contra el plan v3.2 antes de escribir una línea.
4. Ensayar S1 en un worktree; no tocar el árbol sucio actual.
5. Solo entonces abrir la Fase 1 del plan, ya convertida en slices verdes.

Si se quiere mantener el plan como está, como mínimo hay que corregir antes:
C1–C10, B1–B6 y las cifras de §6. Sin eso, el `--check` volverá a deshacer el
trabajo, que es exactamente el fallo que el plan intenta evitar.
