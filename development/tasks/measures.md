# Queue policy and task-set plan

The 2026-11-20/21 plan, historical targets, gate changes and verification runs are
preserved in `development/archive/2026-11-23/work/measures.md`. Current counts
live in `tasks/common.json` and Work; use those, not the historical target.

## Conflict register

One table, one home (Q128). Three columns only (Q138); every listed conflict
carries its decision in the third column. The task order is described in
[PROC-07 in AGENTS.md](../AGENTS.md#proc-07-order)
and summarized under [Task order in the standards README](../standards/README.md#task-order-proc-07).

| ID | Conflicto | Decisión |
|----|-----------|----------|
| C1 | `work-15`, `work-16`, `work-18` shared the title "Should docs include code examples?" (Q122/Q134) | Merged into `work-15`; the other two ids are gone and the count is 312. |
| C2 | No tasks existed for `grown` (37) or `full` hitos (Q106/Q111 vs Q133) | 76 generalist tasks added, one per hito, state `pendiente`, effort `difícil`/`muy difícil`; total 1012. |
| C3 | 124 hito edges but no task `depends_on`; "unlocks" had no data (Q126/Q139) | Effort valued by hito dependientes; all 124 hito edges mirrored as task→task edges on each hito's valuation task (`.3`/`.4`), no cycles. |
| C4 | Dependency order cuts across `stage` (Q127/Q141) | Unblocking first, then ease, independent of `stage`; the Work detail list follows that order. |
| C5 | PROC-01…06 had no sequencing rule (Q132) | PROC-07 added with the eight fields; the human section is README "Task order". |
| C6 | 7 edges have a dependiente more advanced than its prerequisite (Q130): `shell-07`←`shell-05`, `shell-09`←`shell-06`, `skills-05`←`skills-03`, `skills-08`←`skills-03`, `schemas-06`←`schemas-05`, `docs-06`←`docs-05`, `channels-05`←`levels-21` | Registered exception; PROC-07 is advisory, not a hard gate or a routine warning. `tasky.py audit` reports it on request. |
| C7 | `contracts-04` and `quality-02` were the same checker in backend and frontend (Q131/Q135) | Merged into `contracts-04`; frontend coverage recorded as evidence in the title/notes. |
