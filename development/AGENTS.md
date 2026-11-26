# flove development — agent execution context

<a id="work-style-rules"></a>

**Scope:** the register, its scripts, standards and the Work page under
`development/`. The root [`AGENTS.md`](../AGENTS.md) is a router only;
[`standards/AGENTS.md`](standards/AGENTS.md) owns work-style; this file owns
**how tasks are executed** and is the canonical source.

## 1. Authority

1.1 §2 is canonical. `tools/dev/tasks/procedures_source.py` parses it; `tasky`,
`common.json`, the embedded Work block and every gate consume that parser.

1.2 [`tasks/milestones.json`](tasks/milestones.json) owns only hitos and tasks —
it has no `procedures` block.
[`standards/README.md#procedures`](standards/README.md#procedures) is the
standards index; `common.json` and the Work block are generated projections,
never a second source.

1.3 The [`tasky` skill](standards/data/ai/skills/tasky/SKILL.md) references this
file. `python3 tools/dev/tasks/tasky.py procedure [PROC-ID]` prints §2 from the
parser, so source and helper never disagree.

<a id="local-first-url-resolution"></a>

1.4 A `https://flove.org/...` pointer resolves **locally first**: derive the
repo path from the URL, open the file, and jump to the explicit id or heading
slug; if the file or anchor is missing, follow the URL. `AGENTS.md` has two
local sources: `development/AGENTS.md` (PROCs) and
`development/standards/AGENTS.md` (work style). In skill pages and task
pointers the URL is the only written link, so it also serves a downloaded skill
outside the repo. This rule applies to task execution, skills and checks;
`skilly` validates anchors and `skilly.py` derives the local candidates.
The root [`AGENTS.md`](../AGENTS.md) is a router, not a third rule source; it
points here and to the work-style file.

## 2. Procedures

The blocks below are the source. Edit here first, then rebuild the projections;
an indented line continues the field above it.

### PROC-01 — Ownership
- Checker: jsony
- Standard: https://flove.org/development/INDEX.md
- Definition of done: Every plan row has one section and one subsection, and each deliverable names one owner doc; jsony reports no parallel copy.
- Advice: One section and one subsection per row; the stable topic pages own the detail. Each deliverable names one owner doc or section; other docs refer to it instead of restating it.
- Inputs: a plan or debate row without an owner, or a deliverable without one owner doc
- Outputs: one owner per plan in INDEX.md and one owner doc per deliverable
- Gates: jsony: one section and one subsection per row; task and index point to the same owner; no parallel copy

### PROC-02 — Floor
- Checker: validaty
- Standard: https://flove.org/development/standards/contract.md#the-floor
- Definition of done: validaty floor checks pass on the page before any depth work begins.
- Advice: Validate a11y, privacy and structure before any depth work.
- Inputs: a new or edited page before depth work
- Outputs: a page validated for a11y, privacy and structure
- Gates: validaty: the floor checks pass before polish

### PROC-03 — Backbone
- Checker: jsony
- Standard: https://flove.org/development/standards/data/content/json.md
- Definition of done: jsony validates envelopes and routing; no envelope lacks an owner.
- Advice: Validate envelopes and routing before a checkout is shared.
- Inputs: routing.json and flove-fields envelopes
- Outputs: validated envelopes ready for a checkout
- Gates: jsony: envelopes and routing validate

### PROC-04 — Export
- Checker: jsony
- Standard: https://flove.org/development/standards/frontend/frontend.md#1312-export-share-contract-summary-model-portrait-json
- Definition of done: jsony round-trip returns identical rows from JSON to HTML card to import.
- Advice: Save, share and import must return the same portrait.
- Inputs: flove-portrait/1 JSON and the HTML card
- Outputs: the same portrait after save, share and import
- Gates: jsony: round-trip returns identical rows

### PROC-05 — Levels
- Checker: optimizy
- Standard: https://flove.org/development/standards/frontend/frontend.md#1318-stages-3-minimum-4-function-5-craft
- Definition of done: optimizy advice for the page and its section is recorded; no new standard detail was added.
- Advice: Run optimizy per page; it advises execution, not new standard detail.
- Inputs: a Frontend page and its section
- Outputs: per-page optimizy advice applied
- Gates: optimizy: advice recorded without new standard detail

### PROC-06 — Library
- Checker: skilly
- Standard: https://flove.org/development/standards/data/ai/skills/skills.md#skill-skills-01
- Definition of done: skilly.py exits 0, warnings are resolved or explained, and the skills map is synced in standards/README.md.
- Advice: After editing skilly, run it once and sync the map in standards/README.md.
- Inputs: an edited skill and its SKILL.md
- Outputs: skilly result and the synced skills map
- Gates: skilly: 0 errors; warnings resolved or explained in the report; map synced in standards/README.md

### PROC-07 — Order
- Checker: jsony
- Standard: https://flove.org/development/INDEX.md
- Definition of done: A recommended order exists for every stage, every candidate shows its `u` unlock count, changes no stage or state, records loops and C6 exceptions, and never blocks the queue.
- Advice: Advisory only. Let `u` be the number of **open hitos that depend on this hito** (open-hito unlock); rank by `u` descending, then sort tasks by their OWN effort easiest (1) → easy (2) → medium (3) → hard (4) → hardest (5), then stable ids, within stages 1–5 (seed · infant · mature · grown · full). `tasky.py next`, `easy`, `rewindow` and `show` print `u=`; the task-level `depends_on` graph supplies the blockers. Loops warn and continue; record C6 exceptions; never block.
- Inputs: the task queue with stage, effort, hito- and task-level depends_on graph, and the open-hito set
- Outputs: a recommended order for every stage that changes no stage and no state, printing the exact sort key
- Gates: recommendation only: check prerequisites before starting, record C6 exceptions and any loop, never block the queue

### PROC-08 — Specify
- Checker: jsony
- Standard: https://flove.org/development/INDEX.md
- Definition of done: Each task has a concrete title, a done-criterion, an owner path and an evidence pointer with kind and value before any state move; parcial names remaining work.
- Advice: Specify each task from its milestone: concrete title naming the deliverable (no template or stage-label suffix), a done-criterion, the owner path, and an evidence pointer with kind (command|anchor|state) and value. Require evidence before a state move; a parcial task names what remains; sweep template debt back through this procedure.
- Inputs: a milestone (hito), its stage, section and dependency context, and pendiente or parcial tasks
- Outputs: spec-driven tasks with a concrete title, done-criterion, owner path and machine-readable evidence pointer
- Gates: jsony: no template title on hecha/parcial; done-criterion and evidence {kind, value} before a state move; parcial names remaining work; sweep findings fixed through this procedure

### PROC-09 — Replenish
- Checker: jsony
- Standard: https://flove.org/development/INDEX.md
- Definition of done: common.json matches milestones.json, Work --check is green, live count is between 1,200 and 2,000, and the window review has a date and reviewer.
- Advice: When live tasks descend below replenishBelow (1,200), specify new tasks in the 1 seed + 3 infant + 3 mature shape until the queue approaches recommendedMax (1,400); never exceed hardCap (2,000) with 600 slots reserved. Keep about 30 active-window tasks fully specified with owner and evidence, re-ranked weekly with a date in activeWindow.reviewed and the reviewer in activeWindow.reviewedBy. Marking a task done moves it to the Work archive section; the cap never grows by accumulation — a new hito needs an achieved hito archived or merged first. The 2026-11-26 owner decision raised the ceiling to 2,000 while keeping the historical 1,400 target; `work-25.3d` owns trimming the live queue back to it.
- Inputs: the live and archived counts in Work / common.json, taskSet.queuePolicy and the Work archive section
- Outputs: new specified tasks up to recommendedMax, a reviewed window with date and reviewer, and updated live/archive counts
- Gates: jsony: common.json matches milestones.json; build-work-tracker.py --check green; live count between replenishBelow and hardCap after replenishment; window review recorded

### PROC-10 — Decide
- Checker: jsony
- Standard: https://flove.org/development/INDEX.md
- Definition of done: Every live task has an advisory impact class (`direct` · `simple` · `branched` · `complex` · `structuring`) with a score and a question depth; the class is orthogonal to effort, changes no stage or state, and is filterable in Work and mirrored in common.json.
- Advice: Classify from the declared graph: `structuring` when the owner is a canonical schema/envelope/route/index; otherwise keyed by the open-hito unlock `u` — `complex` when u ≥ 3, `branched` when u = 2, `simple` when u = 1, `direct` when u = 0. Offer A/B/C solutions with ★ on the owner default; ask 0, 1 or 3 questions, the last as a questy-all batch. A task may tune its class with `impact_override` + `impact_reason`; the gate keeps the override and shows the reason. Hard-register a new dependency only after the answer, in `depends_on` with `impact_reason`; no new envelope and no flag outside the row.
- Inputs: hito and task `depends_on` graph, the open-hito set, owner paths, the `Decision:` clause and any `impact_override` on the task
- Outputs: a class and score per task in tasky and common.json, the `Dependencias / Dependencies` filter in Work (keyed `impact`), and an A/B/C solution batch for the tasks that need a decision
- Gates: jsony: `impact` is one of the five canonical classes in Work and common.json; `tasky.py weight` / `options` read the same projection; no stage or state changed by the classification
  Every ★ recommendation states its reason and its con in the same line (questy ★ rule); `options` prints both, and the survey never offers a bare default.

<a id="5-proc-09-reading-notes"></a>

## 3–5. Reading notes (PROC-07 / 08 / 09 — not parsed)

| Topic | Rule | Gate / tool |
|---|---|---|
| Order | `stage` says where a hito sits; it does not decide what executes first (Q127). Rank is hito-level `u`; effort is the task's own field — never inferred from the dependiente count. | Q127 · `tasky.py next` |
| Loops & C6 | A loop warns, is recorded and the queue continues (Q137/Q140). The seven C6 state inversions are explicit exceptions (Q129): advisory only, silent in routine checks, never a tasky failure. `tasky.py audit` lists them on request. Conflict register: [`tasks/measures.md#conflict-register`](tasks/measures.md#conflict-register). | Q137/Q140/Q129 |
| Effort ladder | Five canonical English values (1–5): `easiest` · `easy` · `medium` · `hard` · `hardest`. Spanish names belong to UI labels only, never to data; no fractional tier. Colour is effort, not state (Q123/Q124): `easy` green · `hard` yellow · `hardest` red; levels 1 and 3 have no chip colour until tasks carry them. `✓` means `hecha`. | `tasky.py easy` counts the easiest pool; `next --do` queues direct + easy |
| Axes | Two canonical axes only: `effort` (task difficulty) and `stage` (hito maturity: seed · infant · mature · grown · full). `level`, `degree`, `nivel`, `grado` are display synonyms for `effort`, never field names; `phase` / `fase` for `stage`. The frontend 1–5 ladder is a view of those stages (§13.18 of `standards/frontend/frontend.md`), not a third effort scale. Historical `levels-*` ids and `#*-levels` anchors stay as identifiers. | — |
| Impact | `impact` is not effort (PROC-10): an `easy` task can be `structuring` when its owner is a canonical index. It only sets question depth — `direct` 0 questions, `simple`/`branched` one A/B/C, `complex`/`structuring` the three-question questy-all batch — and `tasky.py next --do` queues the `direct + easiest/easy` tasks. | `tasky.py weight <id>` shows signals and any override |
| Evidence | `kind` is `command`, `anchor` or `state`; `value` is the command plus its result, a `file#anchor`, or a rendered state. A bare "verified" is not evidence. | `jsony.py` rejects `hecha`/`parcial` without `{kind, value}` (PROC-08) |
| Owner | Every live task already carries `owner`; verify it resolves on disk. There is no `test` field — do not reintroduce one. One owner doc per deliverable; other docs link instead of restating it. | PROC-01 |
| Queue policy | `taskSet.queuePolicy` is the numbers source: `replenishBelow` 1,200 · `recommendedMax` 1,400 · `hardCap` 2,000 · `headroom` 600 · `activeWindow` 30 (floor 20). The 2,000 ceiling is not a target; the queue works toward 1,400. | `taskSet.queuePolicy` |
| History | The 2026-11-21 owner decision recorded two increases (1,455 → 1,492 → 1,559) in `archive/old/plans/2026-11-21-app-database-stages.md` §4.8.3; the 2026-11-26 decision raised `hardCap` to 2,000, kept the original 1,400 target, and `work-25.3d` owns trimming live back to it. | — |
| Moves | A Work `Done` moves a task to the **Archive · done + closed-hito tasks** drawer. `Export moves` writes a `flove-tasks-moves/1` patch: save it as `development/tasks/tasks-moves.json` with one fully specified replacement per move (same hito, canonical stage/effort, done criterion, valid `depends_on`), then run `python3 tools/dev/tasks/build-work-tracker.py --apply-moves --commit`. | builder |
| Reopen drill | `python3 tools/dev/tasks/check-restore.py` drills a closed-hito reopen read-only. Archive rows carry `closed_hito`, `done` or `superseded` as `reason_code`. | `check-restore.py` |

## 6. Free work without a loaded skill

Routine task work needs no skill in context:

```bash
python3 tools/dev/tasks/tasky.py next          # PROC-07 order
python3 tools/dev/tasks/tasky.py easy          # easiest count + batches
python3 tools/dev/tasks/tasky.py show <id>     # hito, criterion, owner
python3 tools/dev/tasks/tasky.py procedure     # §2 from the parser
python3 tools/dev/tasks/tasky.py check         # four register gates
```

Load `tasky` only for a cold-queue pick, a state move, a procedure edit or a red
gate. `tasky.py card` prints the same loop as a short prompt.

## 7. Sync

7.1 Edit the PROC blocks in §2 first; then rebuild `common.json` and the
embedded Work block. Never hand-edit a generated projection. A `procedures` key
in `milestones.json` is a gate error.

7.2 After any change here run `python3 tools/dev/tasks/build-work-tracker.py --build`,
then the full gate set:

```sh
python3 tools/dev/tasks/build-work-tracker.py --check
python3 tools/dev/tasks/build-common.py --check   # register + narrative counts
python3 tools/dev/checks/jsony.py --no-write
python3 tools/dev/tasks/check-restore.py
python3 tools/dev/checks/check-routing.py
python3 tools/dev/checks/page-resolve.py --check
python3 tools/dev/checks/check-docs-manifest.py --check
python3 tools/dev/checks/check-archive.py --check
python3 tools/dev/checks/check-plan-tray.py --check
python3 tools/dev/checks/check-content.py --check
python3 tools/dev/checks/check-archived-paths.py --check
python3 tools/dev/checks/check-links.py --check
python3 tools/dev/checks/check-page-status.py --check
```

No commit or push unless asked.

**Pending gate (not blocking yet):** `check-types-sync.py` — verifies the app-type
mirror contract owned by
[`apps.md#app-types`](standards/frontend/apps/apps.md#app-types). Tracked as
`GATE01` in [`tasks/pendings.md`](tasks/pendings.md); add it to the command list
above only when the checker exists.
