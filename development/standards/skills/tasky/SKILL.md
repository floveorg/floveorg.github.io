---
name: tasky
description: >-
  Strict, procedure-bound execution of ongoing tasks from the milestones.json
  procedures chapter (PROC-07 pick, PROC-08 spec/evidence, PROC-09 queue). Use
  for /tasky, "strictly by procedure", "apply PROC-08" or a red register gate.
  Free work needs no skill load: `python3 development/scripts/tasky.py next`.
category: utility
---

# tasky

One skill, one file. The canonical policy is the nine `### PROC-nn` blocks in
[`development/AGENTS.md`](https://flove.org/development/AGENTS.md), parsed by
`development/scripts/procedures_source.py`; `milestones.json` owns only hitos and
tasks. `standards/README.md#procedures` is the index. Read the source, never copy
its rules here. Work one ongoing task at a time.

## 1 · Two ways in

- **Free work — no skill load.** `python3 development/scripts/tasky.py next`
  (PROC-07 order), `... show <task-id>` (hito, criterion, owner, PROCs),
  `... procedure [PROC-ID]` (live chapter), `... check` (four gates),
  `... card` (printable short prompt). Ordinary development uses only these.
- **Strict run.** Load this skill for a cold-queue pick, a state move, a
  procedure edit, or a red gate; follow §3–§5.

## 2 · PROC map — ids and owners only

| PROC | Bites when | Checker |
|---|---|---|
| 01 | a deliverable has no single owner doc | jsony |
| 02 | a page is new or edited, before depth work | validaty |
| 03 | envelopes or routing change | jsony |
| 04 | portrait JSON + HTML card must round-trip | exporty |
| 05 | a Frontend level is closed by section | optimizy |
| 06 | a skill was edited | skilly |
| 07 | picking the next task | jsony |
| 08 | writing a spec or moving state | jsony |
| 09 | a task is done, or live count < 1,200 | jsony |

Exact `advice`, `inputs`, `outputs`, `gates` and `definition_of_done` live in the
chapter. PROC-07 is advisory: unlock rank is hito-level, effort is the task's own
field; loops warn and continue, C6 exceptions get recorded, never block.

## 3 · Pick → specify → deliver → verify

1. Pick one queued task by PROC-07: open hito, unlock rank (open hitos that
   depend on it), then effort `fácil → difícil → muy difícil`, then stable ids.
   Check hito and task `depends_on` first; never flip a stage/state to pick.
2. Read `... show <id>`: hito `Deliverable:` / `Done when` / `Decision:`, the
   task's done-criterion, and its `owner` path (hito source, verified on disk).
3. Specify before doing (PROC-08) when the title is a template/stage-label
   suffix or the criterion is vague. A concrete title names the deliverable;
   criterion and evidence pointer exist before any state move.
4. Deliver into that one owner doc — no parallel copy (PROC-01). Run the owning
   checker from §2 before calling it done.
5. Verify with a pointer a second agent can follow: a checker command + result,
   a `file#anchor`, or a rendered state. `parcial` names what remains. Record
   the `Decision:` with its owner.

## 4 · State, moves and the queue (PROC-09)

- States: `pendiente` → `parcial` → `hecha`. Never mark one without evidence;
  never mark one to make a count look better.
- Work `Done` → archive drawer → `Export moves` → `flove-work-moves/1`. Only a
  reviewed, committed patch is canonical:
  `python3 development/scripts/build-work-tracker.py --apply-moves --commit`.
- Then `python3 development/scripts/build-work-tracker.py --build` and
  `python3 development/scripts/build-common.py --build`, then `... check`.
- Thresholds: replenish 1,200 · target 1,400 · cap 1,455 · headroom 55 ·
  window ~30 (floor 20). Below 1,200, add tasks in the 1 seed + 3 infant +
  3 mature (+1 generalist) shape, one fully specified replacement per move.
  The cap never grows. `check-restore.py` drills a closed-hito reopen.

## 5 · Free-work card

```text
Work ONE ongoing task from milestones.json by the canonical procedure.
1. python3 development/scripts/tasky.py next
2. Pick one; check hito and task depends_on. Never change stage/state to pick.
3. python3 development/scripts/tasky.py show <chosen-id>
   → Deliverable / Done when / Decision, done-criterion, owner path.
4. Deliver in the owner doc; run its checker (PROC 01–06 in tasky SKILL.md §2).
5. Attach a followable evidence pointer; parcial names what remains (08).
6. python3 development/scripts/tasky.py check
7. Work Done → Export moves → reviewed work-moves.json → --apply-moves --commit;
   regenerate common.json and the Work block; keep ~30 window tasks (09).
8. Report changes, checkers, dirty files, next task. No commit unless asked.
Full policy: python3 development/scripts/tasky.py procedure
```

## 6 · Suggestions — applied and open

**Applied to the canonical chapter and `development/AGENTS.md`:** a
`definition_of_done` on every PROC; machine-readable evidence
(`kind: command|anchor|state`, value); the PROC-07 tie-break fixed to unlock
rank (hito-level) then the task's own effort, with `next` printing the key; a
weekly window review with `reviewed` and `reviewedBy`; the PROC map mirrored in
`common.json`; PROC-06's gate made satisfiable and PROC-08's "tests" requirement
removed.

**Still open:** add a read-only `tasky.py audit` reporting stale criteria,
missing owners and `depends_on` edges that point at a closed hito. A second idea
is to have `jsony` verify an evidence pointer's `kind` against the owner file
rather than only checking that the field exists.

## 7 · Guardrails and sync

- `milestones.json` owns hitos/tasks; `development/AGENTS.md` owns the PROC
  policy. `common.json` and the Work block are generated projections — never
  hand-edit one.
- This file mirrors PROC **ids**, never PROC **text**, so a procedure update
  cannot go stale here. If the chapter changes, update §2 here and the table in
  `development/AGENTS.md`, then the index in `standards/README.md#procedures`.
- After any skill edit: `python3 development/standards/scripts/check-skills.py`,
  then rebuild the Work skills table. No commit, push or deploy unless asked.
