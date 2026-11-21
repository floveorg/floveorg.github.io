# flove development — agent execution context

**Scope:** the register, its scripts, standards and the Work page under
`development/`. This file owns **how tasks are executed** and the work-style rules (§8); it is
the canonical source of that policy.

## 1. Authority

1.1 The ten `### PROC-nn` blocks in §2 are the canonical execution policy. Each
carries `Checker`, `Standard`, `Definition of done`, `Advice`, `Inputs`, `Outputs`
and `Gates`. `tools/dev/procedures_source.py` parses them; `tasky`,
`common.json`, the embedded Work block and every gate read that parser.

1.2 [`wiki/work/milestones.json`](wiki/work/milestones.json) owns
**only hitos and tasks** — it has no `procedures` block.
[`standards/README.md#procedures`](standards/README.md#procedures) is the
standards index; `common.json` and the Work block are generated projections,
never a second source.

1.3 The [`tasky` skill](standards/skills/tasky/SKILL.md) references this file.
`python3 tools/dev/tasky.py procedure [PROC-ID]` prints §2 from the
parser, so the source and the helper never disagree.

## 2. Procedures

The blocks below are the source. Edit here first, then rebuild the projections;
an indented line continues the field above it.

### PROC-01 — Route each plan to one owner
- Checker: jsony
- Standard: https://flove.org/development/wiki/INDEX.md
- Definition of done: Every plan row has one section and one subsection, and each deliverable names one owner doc; jsony reports no parallel copy.
- Advice: One section and one subsection per row; MDs stay fallback referrals. Each deliverable names one owner doc or section; other docs refer to it instead of restating it.
- Inputs: a plan or debate row without an owner, or a deliverable without one owner doc
- Outputs: one owner per plan in wiki/INDEX.md and one owner doc per deliverable
- Gates: jsony: one section and one subsection per row; task and index point to the same owner; no parallel copy

### PROC-02 — Hold the floor before polish
- Checker: validaty
- Standard: https://flove.org/development/standards/contract.md#the-floor
- Definition of done: validaty floor checks pass on the page before any depth work begins.
- Advice: Validate a11y, privacy and structure before any depth work.
- Inputs: a new or edited page before depth work
- Outputs: a page validated for a11y, privacy and structure
- Gates: validaty: the floor checks pass before polish

### PROC-03 — Check the JSON backbone
- Checker: jsony
- Standard: https://flove.org/development/standards/json.md
- Definition of done: jsony validates envelopes and routing; no envelope lacks an owner.
- Advice: Validate envelopes and routing before a checkout is shared.
- Inputs: routing.json and flove-fields envelopes
- Outputs: validated envelopes ready for a checkout
- Gates: jsony: envelopes and routing validate

### PROC-04 — Round-trip the export
- Checker: exporty
- Standard: https://flove.org/development/standards/frontend/export.md
- Definition of done: exporty round-trip returns identical rows from JSON to HTML card to import.
- Advice: Save, share and import must return the same portrait.
- Inputs: flove-portrait/1 JSON and the HTML card
- Outputs: the same portrait after save, share and import
- Gates: exporty: round-trip returns identical rows

### PROC-05 — Close Frontend levels by section
- Checker: optimizy
- Standard: https://flove.org/development/standards/frontend/frontend.md#1318-usability-levels-3-minimum-4-function-5-craft
- Definition of done: optimizy advice for the page and its section is recorded; no new standard detail was added.
- Advice: Run optimizy per page; it advises execution, not new standard detail.
- Inputs: a Frontend page and its section
- Outputs: per-page optimizy advice applied
- Gates: optimizy: advice recorded without new standard detail

### PROC-06 — Keep the library healthy
- Checker: skilly
- Standard: https://flove.org/development/standards/skills/standing.md
- Definition of done: check-skills.py exits 0, warnings are resolved or explained, and the skills map is synced in standards/README.md.
- Advice: After editing a skill, run skilly once and sync the map in standards/README.md.
- Inputs: an edited skill and its SKILL.md
- Outputs: skilly result and the synced skills map
- Gates: skilly: 0 errors; warnings resolved or explained in the report; map synced in standards/README.md

### PROC-07 — Order tasks by unblocking, then ease
- Checker: jsony
- Standard: https://flove.org/development/wiki/INDEX.md
- Definition of done: A recommended order exists for every stage, changes no stage or state, records loops and C6 exceptions, and never blocks the queue.
- Advice: Advisory only: rank open hitos by how many open hitos depend on them, then sort tasks by their OWN effort very easy (1) → easy (2) → medium (3) → hard (4) → very hard (5), then stable ids, within stages 1–5 (seed · infant · mature · grown · full). Loops warn and continue; record C6 exceptions; never block.
- Inputs: the task queue with stage, effort, hito- and task-level depends_on graph, and the open-hito set
- Outputs: a recommended order for every stage that changes no stage and no state, printing the exact sort key
- Gates: recommendation only: check prerequisites before starting, record C6 exceptions and any loop, never block the queue

### PROC-08 — Specify tasks from milestones
- Checker: jsony
- Standard: https://flove.org/development/wiki/INDEX.md
- Definition of done: Each task has a concrete title, a done-criterion, an owner path and an evidence pointer with kind and value before any state move; parcial names remaining work.
- Advice: Specify each task from its milestone: concrete title naming the deliverable (no template or stage-label suffix), a done-criterion, the owner path, and an evidence pointer with kind (command|anchor|state) and value. Require evidence before a state move; a parcial task names what remains; sweep template debt back through this procedure.
- Inputs: a milestone (hito), its stage, section and dependency context, and pendiente or parcial tasks
- Outputs: spec-driven tasks with a concrete title, done-criterion, owner path and machine-readable evidence pointer
- Gates: jsony: no template title on hecha/parcial; done-criterion and evidence {kind, value} before a state move; parcial names remaining work; sweep findings fixed through this procedure

### PROC-09 — Replenish the live queue as tasks are done
- Checker: jsony
- Standard: https://flove.org/development/wiki/INDEX.md
- Definition of done: common.json matches milestones.json, Work --check is green, live count is between 1,200 and 1,559, and the window review has a date and reviewer.
- Advice: When live tasks descend below replenishBelow (1,200), specify new tasks in the 1 seed + 3 infant + 3 mature shape until the queue approaches recommendedMax (1,504); never exceed hardCap (1,559) with 55 slots reserved. Keep about 30 active-window tasks fully specified with owner and evidence, re-ranked weekly with a date in activeWindow.reviewed and the reviewer in activeWindow.reviewedBy. Marking a task done moves it to the Work archive section; the cap never grows by accumulation — a new hito needs an achieved hito archived or merged first.
- Inputs: the live and archived counts in Work / common.json, taskSet.queuePolicy and the Work archive section
- Outputs: new specified tasks up to recommendedMax, a reviewed window with date and reviewer, and updated live/archive counts
- Gates: jsony: common.json matches milestones.json; build-work-tracker.py --check green; live count between replenishBelow and hardCap after replenishment; window review recorded

### PROC-10 — Weigh decision consequence before asking
- Checker: jsony
- Standard: https://flove.org/development/wiki/INDEX.md
- Definition of done: Every live task has an advisory choice_weight class (`directo` · `ramificado` · `estructurante`) with a score and a question depth; the class is orthogonal to effort, changes no stage or state, and is filterable in Work and mirrored in common.json.
- Advice: Classify from the declared graph: `estructurante` when u ≥ 3, or fan-out ≥ 10, or the owner is a canonical schema/envelope/route/index, or g ≥ 2 declared dependencies; `ramificado` when u = 2, or fan-out 3–9, or the `Decision:` clause contains vs / or / which / who; `directo` otherwise. Offer A/B/C solutions with ★ on the owner default; ask 0, 1 or 3 questions, the last as a questy-all batch. A task may tune its class with `choice_override` + `choice_reason`; the gate keeps the override and shows the reason. Hard-register a new dependency only after the answer, in `depends_on` with `choice_reason`; no new envelope and no flag outside the row.
- Inputs: hito and task `depends_on` graph, the open-hito set, owner paths, the `Decision:` clause and any `choice_override` on the task
- Outputs: a class and score per task in tasky and common.json, a `choice` filter in Work, and an A/B/C solution batch for the tasks that need a decision
- Gates: jsony: `choice` is one of the three canonical classes in Work and common.json; `tasky.py weight` / `options` read the same projection; no stage or state changed by the classification
  Every ★ recommendation states its reason and its con in the same line (questy ★ rule); `options` prints both, and the survey never offers a bare default.

## 3. PROC-07 — reading notes

3.1 `stage` says where a hito sits; it does not decide what to execute first
(Q127). The unlock rank is hito-level; effort is the task's own field — never
inferred from the dependiente count.

3.2 A loop warns, is recorded and the queue continues (Q137/Q140). The seven
state inversions of C6 are explicit exceptions (Q129). The conflict register is
[`wiki/work/measures.md#conflict-register`](wiki/work/measures.md#conflict-register).

3.3 Effort is a five-level ladder with canonical English values (1–5):
`very easy` · `easy` · `medium` · `hard` · `very hard`. Spanish names belong to
the UI labels only, never to the data; there is no fractional tier. Colour is
effort, not state (Q123/Q124): `easy` green · `hard` yellow · `very hard` red;
levels 1 and 3 have no chip colour until tasks carry them. A `✓` means `hecha`.
`tasky.py easy` counts the very easy pool and proposes batches; `next --do`
queues it with directo + easy.

3.3a Two canonical axes only: `effort` (task difficulty) and `stage` (hito
maturity: seed · infant · mature · grown · full). `level`, `degree`, `nivel`
and `grado` are display synonyms for `effort` — never field names; `phase` /
`fase` is the display synonym for `stage`. The frontend 1–5 ladder is a view of
those core stages (§13.18 of `standards/frontend/frontend.md`), not a third
effort scale. Historical `levels-*` ids and `#*-levels` anchors stay as
identifiers; do not mint new ones.

3.4 `choice_weight` is not effort (PROC-10): an `easy` task can be `estructurante`
when its owner is a canonical index. It only sets question depth — `directo` 0,
`ramificado` one A/B/C question, `estructurante` the three-question questy-all
batch — and `tasky.py next --do` queues the `directo + very easy/easy` tasks
for work without asking. `tasky.py weight <id>` shows the signals and any user
override.

## 4. PROC-08 — reading notes

4.1 `kind` is `command`, `anchor` or `state`; `value` is the command plus its
result, a `file#anchor`, or a rendered state. A bare "verified" is not evidence.
`jsony_check.py` rejects a `hecha`/`parcial` task without `{kind, value}`.

4.2 Every live task already carries `owner`; verify it resolves on disk. There
is no `test` field — do not reintroduce one. One owner doc per deliverable;
other docs link to it rather than restating it (PROC-01).

## 5. PROC-09 — reading notes

5.1 `taskSet.queuePolicy` is the numbers source: `replenishBelow` 1,200 ·
`recommendedMax` 1,504 · `hardCap` 1,559 · `headroom` 55 · `activeWindow` 30
(floor 20). The register sits at the cap after the reshape, so the first cycle
brings it down to 1,504 rather than back up to 1,559.

The 2026-11-21 owner decision recorded the two increases
(1,455 → 1,492 → 1,559) in `wiki/archive/old/plans/2026-11-21-app-database-stages.md` §4.8.3.

5.2 A Work `Done` moves a task to the **Archive · done + closed-hito tasks**
drawer. `Export moves` writes a `flove-work-moves/1` patch. Save it as
`wiki/work/work-moves.json` with one
fully specified replacement per move (same hito, canonical stage/effort, a done
criterion, valid `depends_on`), then run
`python3 tools/dev/build-work-tracker.py --apply-moves --commit`.

5.3 `python3 tools/dev/check-restore.py` drills a closed-hito reopen
read-only. Archive rows carry `closed_hito`, `done` or `superseded` as
`reason_code`.

## 6. Free work without a loaded skill

Routine task work needs no skill in context:

```bash
python3 tools/dev/tasky.py next          # PROC-07 order
python3 tools/dev/tasky.py easy          # very easy count + batches
python3 tools/dev/tasky.py show <id>     # hito, criterion, owner
python3 tools/dev/tasky.py procedure     # §2 from the parser
python3 tools/dev/tasky.py check         # four register gates
```

Load `tasky` only for a cold-queue pick, a state move, a procedure edit or a red
gate. `tasky.py card` prints the same loop as a short prompt.

## 7. Sync

7.1 Edit the PROC blocks in §2 first; then rebuild `common.json` and the
embedded Work block. Never hand-edit a generated projection. A `procedures` key
in `milestones.json` is a gate error.

7.2 After any change here run `python3 tools/dev/build-work-tracker.py --build`,
then `--check`, `build-common.py --check`, `jsony_check.py`, `check-restore.py`
`tools/dev/check-skills.py`, `tools/dev/check-page-status.py` and
`tools/dev/check-links.py`. No commit or push unless asked.

## 8. Work-style rules (merged from the old standards policy, 2026-11-21)

**How to work with me**


1. Duplicados
   1.1 Unir o borrar; no añadir un tercero
   1.2 Si no hay solución práctica, preguntar
   1.3 Si un cambio duplica o añade bloat, revertir y decirlo
2. Propiedad
   2.1 Buscar el dueño del hecho antes de crear un doc o sección
3. Estándares y skills
   3.1 El estándar lleva el detalle
   3.2 La skill lo referencia
   3.3 Nombres canónicos: Data Depth, Apps, Tree/Types, whole/; no sinónimos
4. Niveles
   4.1 `<skill>N` = 1 → N, acumulativos, para en N
   4.2 Sin número → el default documentado de cada skill; N corre 1→N
   4.3 Separar mínimo / función / craft
5. Tablas
   5.1 Una tabla vive en su fuente
   5.2 Si otra doc la necesita, exportarla; no reescribirla
   5.3 Retirado → `wiki/archive/old/archive.md`
   5.4 Datos reales: leer la fuente (docs/index, development/index, routing.json); si falta, N/A o missing; no inventar filas, apps ni paradigmas
6. Rutas
   6.1 Tras un traslado, actualizar todas las referencias
   6.2 Una corrección se aplica en todos los sitios, no solo en el archivo actual
7. Mapas
   7.1 AGENTS = cómo trabajo
   7.2 README = qué hay
   7.3 worldview = porqué + mapa
   7.4 contract = reglas
   7.5 No repetir el mismo mapa
8. Interacción
   8.1 Responder en el idioma del último mensaje
   8.2 Ejecutar; preguntar solo si es destructivo o ambiguo
9. Seguridad
   9.1 No tocar `~/agents` (credenciales)
   9.2 `sw.js` solo en `updaty4`
   9.3 No commit/push sin pedirlo
10. Scripts
   10.1 `tools/` = generalistas
   10.2 `tools/dev/` = específicos + el procedimiento de release (`check-distro.sh`, `publish-web.sh`)
11. Cambios
   11.1 Editar solo lo pedido; no reformatear el resto
   11.2 Si el encargo es amplio, hacer la parte segura y listar lo que queda
   11.3 En tareas grandes, si aparece un conflicto o riesgo en la edición, avisar antes de tocar nada y mostrar las opciones (formato 12.3)
12. Formato
   12.1 Tablas para matrices y comparaciones
   12.2 En documentos, numerar con IDs únicos y jerárquicos: 1, 1.1, 1.2 — no listas planas
   12.3 Numbered suggestions and questions (terminal): when you ask for ideas, I offer concrete actions (next steps, options, alternatives), or I present questions for you to answer, use one numbered batch with this format:
        12.3.1 Continuous sequence per batch (1–N): assign a unique number to every numbered element in the batch in one continuous sequence. Never restart numbering per section or category.
        12.3.2 Titles included: each titled block (section, question, or group) is a numbered element in that same sequence — include its number in the heading (e.g. `### 1. Title`) so titles are addressable, not outside the count.
        12.3.3 Items continue the sequence: list every suggestion, next step, or selectable option as a numbered item that continues the same sequence (one per line, concise). This applies to both direct action suggestions and questions with reply options.
        12.3.4 Replies (for questions/options): make each answer option uniquely numbered within the batch and state the reply format (e.g. "reply with one option number per question, in order" or "reply with the numbers you choose"), so answers map unambiguously to numbers.
        12.3.5 Layout: separate blocks with a blank line; keep blocks scannable. When useful, also offer a multiselect prompt as an additional way to choose. For multi-batch sessions, keep numbering continuous across batches when practical and label the range (e.g. Q001–Q030) so references stay unique.
13. Idioma
   13.1 Todo el contenido de `flove/` (apps, webs, docs y código) va en inglés
   13.2 Excepciones en español: `liberada`, `futbolia` y `dinámicas electrónicas`

**Where things live**

- Standards index: [`standards/README.md`](standards/README.md) — what exists and where it is specified.
- Vocabulary: [`standards/vocabulary.html`](standards/vocabulary.html) — canonical names, the field data model and the interactive matrix.
- Task procedure: this file, §2 — the ten PROCs; [`wiki/work/milestones.json`](wiki/work/milestones.json) owns only hitos and tasks.
- Archive: [`wiki/archive/README.md`](wiki/archive/README.md) — opaque pre-cutover snapshot, never an owner.

**Editing rule.** Integrate new content into the section that already owns the fact — do not add a new file (or a new section) for every change; a new file only when the fact has no existing home.

**Voice.** Write affirmatively — name what holds and the test that proves it; keep prohibitions for safety edges.

**Home-directory layout.** Retired note: [`wiki/archive/old/archive.md`](wiki/archive/old/archive.md#home-directory-layout).
