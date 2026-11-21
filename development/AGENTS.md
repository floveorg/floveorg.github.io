# flove development — agent execution context

**Scope:** the register, its scripts, standards and the Work page under
`development/`. The standards work-style rules live in
[`standards/AGENTS.md`](standards/AGENTS.md); this file owns **how tasks are
executed** and is the canonical source of that policy.

## 1. Authority

1.1 The nine `### PROC-nn` blocks in §2 are the canonical execution policy. Each
carries `Checker`, `Standard`, `Definition of done`, `Advice`, `Inputs`, `Outputs`
and `Gates`. `development/scripts/procedures_source.py` parses them; `tasky`,
`common.json`, the embedded Work block and every gate read that parser.

1.2 [`standards/debates/milestones.json`](standards/debates/milestones.json) owns
**only hitos and tasks** — it has no `procedures` block.
[`standards/README.md#procedures`](standards/README.md#procedures) is the
standards index; `common.json` and the Work block are generated projections,
never a second source.

1.3 The [`tasky` skill](standards/skills/tasky/SKILL.md) references this file.
`python3 development/scripts/tasky.py procedure [PROC-ID]` prints §2 from the
parser, so the source and the helper never disagree.

## 2. Procedures

The blocks below are the source. Edit here first, then rebuild the projections;
an indented line continues the field above it.

### PROC-01 — Route each plan to one owner
- Checker: jsony
- Standard: https://flove.org/development/standards/debates/INDEX.md
- Definition of done: Every plan row has one section and one subsection, and each deliverable names one owner doc; jsony reports no parallel copy.
- Advice: One section and one subsection per row; MDs stay fallback referrals. Each deliverable names one owner doc or section; other docs refer to it instead of restating it.
- Inputs: a plan or debate row without an owner, or a deliverable without one owner doc
- Outputs: one owner per plan in debates/INDEX.md and one owner doc per deliverable
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
- Standard: https://flove.org/development/standards/backend.md
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
- Standard: https://flove.org/development/standards/debates/INDEX.md
- Definition of done: A recommended order exists for every stage, changes no stage or state, records loops and C6 exceptions, and never blocks the queue.
- Advice: Advisory only: rank open hitos by how many open hitos depend on them, then sort tasks by their OWN effort fácil → difícil → muy difícil, then stable ids, within stages 1–5 (seed · infant · mature · grown · full). Loops warn and continue; record C6 exceptions; never block.
- Inputs: the task queue with stage, effort, hito- and task-level depends_on graph, and the open-hito set
- Outputs: a recommended order for every stage that changes no stage and no state, printing the exact sort key
- Gates: recommendation only: check prerequisites before starting, record C6 exceptions and any loop, never block the queue

### PROC-08 — Specify tasks from milestones
- Checker: jsony
- Standard: https://flove.org/development/standards/debates/INDEX.md
- Definition of done: Each task has a concrete title, a done-criterion, an owner path and an evidence pointer with kind and value before any state move; parcial names remaining work.
- Advice: Specify each task from its milestone: concrete title naming the deliverable (no template or stage-label suffix), a done-criterion, the owner path, and an evidence pointer with kind (command|anchor|state) and value. Require evidence before a state move; a parcial task names what remains; sweep template debt back through this procedure.
- Inputs: a milestone (hito), its stage, section and dependency context, and pendiente or parcial tasks
- Outputs: spec-driven tasks with a concrete title, done-criterion, owner path and machine-readable evidence pointer
- Gates: jsony: no template title on hecha/parcial; done-criterion and evidence {kind, value} before a state move; parcial names remaining work; sweep findings fixed through this procedure

### PROC-09 — Replenish the live queue as tasks are done
- Checker: jsony
- Standard: https://flove.org/development/standards/debates/INDEX.md
- Definition of done: common.json matches milestones.json, Work --check is green, live count is between 1,200 and 1,455, and the window review has a date and reviewer.
- Advice: When live tasks descend below replenishBelow (1,200), specify new tasks in the 1 seed + 3 infant + 3 mature shape until the queue approaches recommendedMax (1,400); never exceed hardCap (1,455) with 55 slots reserved. Keep about 30 active-window tasks fully specified with owner and evidence, re-ranked weekly with a date in activeWindow.reviewed and the reviewer in activeWindow.reviewedBy. Marking a task done moves it to the Work archive section; the cap never grows by accumulation — a new hito needs an achieved hito archived or merged first.
- Inputs: the live and archived counts in Work / common.json, taskSet.queuePolicy and the Work archive section
- Outputs: new specified tasks up to recommendedMax, a reviewed window with date and reviewer, and updated live/archive counts
- Gates: jsony: common.json matches milestones.json; build-work-tracker.py --check green; live count between replenishBelow and hardCap after replenishment; window review recorded

## 3. PROC-07 — reading notes

3.1 `stage` says where a hito sits; it does not decide what to execute first
(Q127). The unlock rank is hito-level; effort is the task's own field — never
inferred from the dependiente count.

3.2 A loop warns, is recorded and the queue continues (Q137/Q140). The seven
state inversions of C6 are explicit exceptions (Q129). The conflict register is
[`standards/debates/hitos-audit.md#conflict-register`](standards/debates/hitos-audit.md#conflict-register).

3.3 Colour is effort, not state (Q123/Q124): `fácil` green · `difícil` yellow ·
`muy difícil` red; a `✓` in a task row means `hecha`, whatever its colour.

## 4. PROC-08 — reading notes

4.1 `kind` is `command`, `anchor` or `state`; `value` is the command plus its
result, a `file#anchor`, or a rendered state. A bare "verified" is not evidence.
`jsony_check.py` rejects a `hecha`/`parcial` task without `{kind, value}`.

4.2 Every live task already carries `owner`; verify it resolves on disk. There
is no `test` field — do not reintroduce one. One owner doc per deliverable;
other docs link to it rather than restating it (PROC-01).

## 5. PROC-09 — reading notes

5.1 `taskSet.queuePolicy` is the numbers source: `replenishBelow` 1,200 ·
`recommendedMax` 1,400 · `hardCap` 1,455 · `headroom` 55 · `activeWindow` 30
(floor 20). The register sits at the cap after the reshape, so the first cycle
brings it down to 1,400 rather than back up to 1,455.

5.2 A Work `Done` moves a task to the **Archive · done + closed-hito tasks**
drawer. `Export moves` writes a `flove-work-moves/1` patch. Save it as
[`standards/debates/work-moves.json`](standards/debates/work-moves.json) with one
fully specified replacement per move (same hito, canonical stage/effort, a done
criterion, valid `depends_on`), then run
`python3 development/scripts/build-work-tracker.py --apply-moves --commit`.

5.3 `python3 development/scripts/check-restore.py` drills a closed-hito reopen
read-only. Archive rows carry `closed_hito`, `done` or `superseded` as
`reason_code`.

## 6. Free work without a loaded skill

Routine task work needs no skill in context:

```bash
python3 development/scripts/tasky.py next          # PROC-07 order
python3 development/scripts/tasky.py show <id>     # hito, criterion, owner
python3 development/scripts/tasky.py procedure     # §2 from the parser
python3 development/scripts/tasky.py check         # four register gates
```

Load `tasky` only for a cold-queue pick, a state move, a procedure edit or a red
gate. `tasky.py card` prints the same loop as a short prompt.

## 7. Sync

7.1 Edit the PROC blocks in §2 first; then rebuild `common.json` and the
embedded Work block. Never hand-edit a generated projection. A `procedures` key
in `milestones.json` is a gate error.

7.2 After any change here run `python3 development/scripts/build-work-tracker.py --build`,
then `--check`, `build-common.py --check`, `jsony_check.py`, `check-restore.py`
and `development/standards/scripts/check-skills.py`. No commit or push unless
asked.
