---
name: tasky
description: >-
  Decide the next flove task fast by the canonical procedure in
  development/AGENTS.md (PROC-07 window pick, PROC-08 evidence, PROC-09 queue,
  PROC-10 choice weight). Use for /tasky, "what next", "pick a task" or a red
  gate. Clicky intro, asks the user on ambiguity or a heavy list (questy).
  Free work: tasky.py pick.
category: utility
---

# tasky

One skill, one file, public. A **profile** maps an advanced context bundle to
real paths; `flove` is the default, `/tasky <profile>` overrides. The core picks
→ proves → delivers; the adapter owns paths. Policy is the ten `### PROC-nn`
blocks in [`development/AGENTS.md`](https://flove.org/development/AGENTS.md),
parsed by `procedures_source.py`; `milestones.json` owns hitos/tasks. Read the
source, never copy its rules. Work one task at a time.

## 1 · Two ways in

- **Free work — no skill load (default).** `python3 tools/dev/tasky.py
  pick` gives one ready task and its rationale; `... show <id>` proves it,
  `... next` lists the window (`--all` ranks, `--ready` hides blocked/vague),
  `... context [profile]` loads the bundle, `... rewindow --survey` prints 30
  questy candidates, `... questy` asks a heavy list, `... audit` hygiene,
  `... easy` very-easy batches, `... check` four gates, `... procedure
  [PROC-ID]` the chapter, `... card` the prompt. `questy-tasky-flove` runs
  survey → `weight` → `options` → `show <id>` and the two close blocks.
- **Strict run.** Load this skill for a cold-queue pick, a state move, a
  procedure edit, or a red gate; follow §3–§5.

On `/tasky`, open a **clicky intro form** (host question tool, else AGENTS §12.3
numbered batch): `pick + work` (★ reason: fastest ready task with proof; con:
skips comparing a heavy shortlist) / `show one id` / `audit` / `procedure`.

**Ask the user, never infer, on judgment calls:** which ready task to take,
whether to unblock, what a heavy list drops, a procedure edit, anything
destructive. A verified state move is automatic — never ask. Same clicky tool,
else one numbered batch. Otherwise execute without confirming (AGENTS §8.2).

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
| 10 | choice | jsony |

Chapter owns the five PROC fields. PROC-07 is advisory: hito-level unlock,
task-level effort; loops warn, C6 exceptions recorded, never block.

## 3 · Pick → prove → deliver → verify

1. `python3 tools/dev/tasky.py pick` starts from reviewed
   `activeWindow.order`, skips unsatisfied `depends_on`, generic criteria and
   `.3*` scaffolds, and prints its rank rationale; `--all` covers the queue.
   `next` shows `w`, `u` and `READY`/`BLOCKED`/`SPEC`. Never flip a stage or
   state for eligibility. On a **heavy** shortlist (most window
   `BLOCKED`/`SPEC`, or ready `hard`/`very hard`), run
   `python3 tools/dev/tasky.py questy` (read-only) and put its
   options to the clicky form — never take the first silently.
2. Read `python3 tools/dev/tasky.py show <id>`: the hito's
   `Deliverable:` / `Done when:` / `Decision:`, the done-criterion, owner path and
   three proofs — `owner exists`, `depends satisfied`, `pointer kind=value`. A
   `NO`, `BLOCKED` or `missing` means specify or unblock first (PROC-08).
3. Specify before doing when the title is a template/stage-label suffix or the
   criterion is vague. A concrete title names the deliverable; the criterion and
   evidence pointer exist before any state move.
4. Deliver into that one owner doc — no parallel copy (PROC-01). Run the owning
   checker from §2 before calling it done.
5. Verify with a followable pointer: a checker command + result, a `file#anchor`,
   or a rendered state. Move the task to `hecha` automatically once the pointer
   verifies (PROC-08); `parcial` names what remains. Record the `Decision:`.

## 4 · State, moves and the queue (PROC-09)

- States: `pendiente` → `parcial` → `hecha`. Evidence first, then move without
  asking; never mark one to make a count look better. `tasky.py easy` counts the
  very easy pool and proposes batches; `next --do` queues those with directo.
- Work `Done` → archive drawer → `Export moves` → `flove-work-moves/1`. Only a
  reviewed, committed patch is canonical:
  `python3 tools/dev/build-work-tracker.py --apply-moves --commit`.
- Then `python3 tools/dev/build-work-tracker.py --build` and
  `python3 tools/dev/build-common.py --build`, then `... check`.
- Thresholds: replenish 1,200 · target 1,504 · cap 1,559 · headroom 55 ·
  window ~30 (floor 20). Below 1,200 add 1 seed + 3 infant + 3 mature
  (+1 generalist), one specified replacement per move; cap never grows.
  `check-restore.py` drills a reopen.
- `tasky.py audit` reports stale criteria, missing owners and closed-hito
  dependencies before the weekly window re-rank.

## 5 · Free-work card

```text
Work ONE ready task by the canonical procedure in development/AGENTS.md.
1. python3 tools/dev/tasky.py pick          # one decision, window first
2. python3 tools/dev/tasky.py show <id>     # criterion, owner, proof
3. Check the proof lines: owner exists, depends satisfied, pointer present (08).
4. Deliver in the owner doc; run its checker (PROC 01–06 in §2).
5. Verify the pointer, then move state automatically; parcial names remains.
6. python3 tools/dev/tasky.py check         # four register gates
7. Work Done → Export moves → reviewed work-moves.json → --apply-moves --commit;
   regenerate common.json and the Work block; keep ~30 window tasks (09).
8. Report changes, checkers, dirty files, next task. No commit unless asked.
Full policy: python3 tools/dev/tasky.py procedure
```

## 6 · Suggestions — applied

Applied: evidence, tie-break, review, `common.json` mirror, no `test`
field, `audit`, clicky intro, `questy`, profiles, `context`, very-easy tier,
PROC-10 pick/weight/options/next --do, five-level effort, caps, ★ reason +
con, questy-tasky-flove close blocks. Open: `jsony` pointer `kind`.

## 7 · Guardrails and sync

- `milestones.json` owns hitos/tasks; `development/AGENTS.md` owns the PROC
  policy. `common.json` and the Work block are generated projections — never
  hand-edit one.
- This file mirrors PROC **ids**, never PROC **text**, so edits cannot stale it.
  On change update §2, the ten PROC blocks and
  `standards/README.md#procedures`.
- After any skill edit: `python3 tools/dev/check-skills.py`,
  then rebuild the Work skills table. No commit, push or deploy unless asked.
