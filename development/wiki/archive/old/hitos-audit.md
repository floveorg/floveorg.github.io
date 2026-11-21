# Hitos · coherence audit (2026-11-20)

> **Reshape notice:** the tables below are the pre-reshape 1,012-task
> snapshot (345 `hecha`). The current register is **1,455 live tasks + 805
> archived** (`milestones.json`, projected by `common.json`). Regenerate the
> per-field counts before reusing this report as a source.

> **Scope / Ámbito:** EN: Result of the Q119 audit — every hito has an id, a stage and associated tasks. · ES: Resultado de la auditoría Q119 — todo hito tiene id, stage y tasks asociadas.

| Section | Hitos | Tasks | New generalist | needs_split (before) | needs_split (now) |
|---|---:|---:|---:|---:|---:|
| docs | 42 | 141 | 15 | 18 | 0 |
| backend | 67 | 216 | 15 | 22 | 0 |
| frontend | 78 | 253 | 19 | 20 | 0 |
| ai | 52 | 164 | 8 | 14 | 0 |
| data | 33 | 108 | 9 | 12 | 0 |
| community | 40 | 130 | 10 | 13 | 0 |
| **Total** | **312** | **1012** | **76** | **99** | **0** |

Stage values: `seed · infant · mature · grown · full` (Q109/Q114).
All 312 hitos have a unique `<section>-<n>` id (Q116), 124 dependencies point at ids (Q091), the 99 rows flagged by Q105/Q107/Q119 were split and cleared, and 76 generalist tasks were added to the `grown`/`full` hitos (Q133/Q136). Counts supersede the 315/945 of Q091–Q120.
Regenerate this report from `milestones.json` after any tracker edit.

## Fields and their tasks

Each section owns **different** fields — the `section` value on each hito, which
is the same name the Work `Sections` filter shows under its parent axis. Tasks
belong to their hito's field: the counts below are read from `milestones.json`,
not copied from another section. `f / d / x` = `fácil / difícil / muy difícil`;
`h / p / n` = `hecha / parcial / pendiente`.

| Section | Field | Hitos | Tasks | f | d | x | h | p | n | First id |
|---------|-------|------:|------:|--:|--:|--:|--:|--:|--:|----------|
| docs | map | 11 | 35 | 32 | 3 | 0 | 24 | 0 | 11 | map-01 |
| docs | plan | 9 | 29 | 26 | 3 | 0 | 12 | 0 | 17 | plan-01 |
| docs | work | 22 | 77 | 65 | 12 | 0 | 18 | 2 | 57 | work-01 |
| backend | contracts | 16 | 52 | 43 | 7 | 2 | 12 | 0 | 40 | contracts-01 |
| backend | delivery | 20 | 63 | 60 | 3 | 0 | 36 | 0 | 27 | delivery-01 |
| backend | storage | 7 | 23 | 19 | 4 | 0 | 9 | 0 | 14 | storage-01 |
| backend | systems | 24 | 78 | 66 | 9 | 3 | 12 | 0 | 66 | systems-01 |
| frontend | a11y | 8 | 26 | 24 | 2 | 0 | 12 | 0 | 14 | a11y-01 |
| frontend | levels | 14 | 46 | 41 | 5 | 0 | 21 | 1 | 24 | levels-01 |
| frontend | quality | 12 | 39 | 36 | 3 | 0 | 12 | 2 | 25 | quality-01 |
| frontend | shell | 12 | 38 | 35 | 2 | 1 | 12 | 3 | 23 | shell-01 |
| frontend | tours | 6 | 20 | 18 | 2 | 0 | 9 | 0 | 11 | tours-01 |
| frontend | tree | 14 | 44 | 41 | 2 | 1 | 18 | 0 | 26 | tree-01 |
| frontend | types | 5 | 17 | 15 | 2 | 0 | 9 | 0 | 8 | types-01 |
| frontend | visual | 7 | 23 | 21 | 2 | 0 | 12 | 0 | 11 | visual-01 |
| ai | flows | 13 | 41 | 37 | 3 | 1 | 3 | 3 | 35 | flows-01 |
| ai | levels | 5 | 17 | 15 | 2 | 0 | 6 | 0 | 11 | levels-15 |
| ai | models | 10 | 32 | 28 | 4 | 0 | 12 | 0 | 20 | models-01 |
| ai | skills | 24 | 74 | 69 | 3 | 2 | 15 | 4 | 55 | skills-01 |
| data | index | 6 | 20 | 18 | 2 | 0 | 9 | 0 | 11 | index-01 |
| data | json | 8 | 26 | 24 | 2 | 0 | 12 | 0 | 14 | json-01 |
| data | mds | 9 | 29 | 26 | 3 | 0 | 12 | 0 | 17 | mds-01 |
| data | schemas | 10 | 33 | 29 | 3 | 1 | 6 | 2 | 25 | schemas-01 |
| community | channels | 8 | 26 | 22 | 4 | 0 | 9 | 0 | 17 | channels-01 |
| community | docs | 10 | 32 | 29 | 3 | 0 | 12 | 2 | 18 | docs-01 |
| community | feedback | 7 | 23 | 20 | 3 | 0 | 6 | 0 | 17 | feedback-01 |
| community | language | 7 | 23 | 21 | 2 | 0 | 6 | 0 | 17 | language-01 |
| community | levels | 8 | 26 | 23 | 3 | 0 | 9 | 0 | 17 | levels-20 |
| **Total** | **28 fields** | **312** | **1012** | **903** | **98** | **11** | **345** | **19** | **648** | — |

Note: `levels` is a real field in three sections (frontend, ai, community) with
different ids — `levels-01`, `levels-15`, `levels-20` — not a shared bucket.
`docs` is likewise a field of `community`, not of the `docs` section.

## Refinement (Q105 / Q107 / Q119 — executed 2026-11-20)

The 99 flagged rows are now split. Each keeps its hito id and its original stage tasks,
but the placeholders (`<title> — <stage>`) became concrete stage actions: `define locally`, `apply in the basic flow`, `publish in the canonical index`. The mature task of each hito is now valued by its number of dependientes (Q126): `fácil` 0–1, `difícil` 2, `muy difícil` ≥3. The 315/945 counts were later superseded by the Q131–Q139 merges and generalist tasks.

Result: `needs_split: false` on all 312 hitos. Q133 reopened the `grown`/`full` question: 76 generalist tasks were added, so Q106/Q111 now stand at 1012 tasks. Re-run `python3 development/scripts/build-work-tracker.py --build && --check` after any tracker edit — item 13 (`--audit`) was explicitly not done.

## Conflict register

One table, one home (Q128). Three columns only (Q138); every listed conflict
carries its decision in the third column. The task order is described in
[`../README.md#task-order-proc-07`](../README.md#task-order-proc-07).

| ID | Conflicto | Decisión |
|----|-----------|----------|
| C1 | `work-15`, `work-16`, `work-18` shared the title "Should docs include code examples?" (Q122/Q134) | Merged into `work-15`; the other two ids are gone and the count is 312. |
| C2 | No tasks existed for `grown` (37) or `full` hitos (Q106/Q111 vs Q133) | 76 generalist tasks added, one per hito, state `pendiente`, effort `difícil`/`muy difícil`; total 1012. |
| C3 | 124 hito edges but no task `depends_on`; "unlocks" had no data (Q126/Q139) | Effort valued by hito dependientes; all 124 hito edges mirrored as task→task edges on each hito's valuation task (`.3`/`.4`), no cycles. |
| C4 | Dependency order cuts across `stage` (Q127/Q141) | Unblocking first, then ease, independent of `stage`; the Work detail list follows that order. |
| C5 | PROC-01…06 had no sequencing rule (Q132) | PROC-07 added with the eight fields; the human section is README "Task order". |
| C6 | 7 edges have a dependiente more advanced than its prerequisite (Q130): `shell-07`←`shell-05`, `shell-09`←`shell-06`, `skills-05`←`skills-03`, `skills-08`←`skills-03`, `schemas-06`←`schemas-05`, `docs-06`←`docs-05`, `channels-05`←`levels-21` | Registered exception; PROC-07 is advisory, not a hard gate. |
| C7 | `contracts-04` and `quality-02` were the same checker in backend and frontend (Q131/Q135) | Merged into `contracts-04`; frontend coverage recorded as evidence in the title/notes. |
