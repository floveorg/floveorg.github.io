# Queue policy and task-set plan

> Source: `development/wiki/archive/old/task-set-plan.md` (archived 2026-11-21).

Status: **proposal v2 — third view applied** (register reshaped; gate green)
Source: `archive/old/task-set-plan.md` + `archive/old/hitos-audit.md` · register: `wiki/work/milestones.json` · page join: `wiki/work/common.json` · mirror: `standards/README.md` · gate: `tools/dev/build-work-tracker.py`
Date: 2026-11-20

> **Historical target.** §4 records the 2026-11-20 reshape to 1,455 live
tasks. The current register is 1,559 live after the 2026-11-21 increase; use
`common.json` / Work for current counts, not this historical target.

## 1. Inputs and constraints

Three things set the shape of this plan:

1. **The project is ambitious.** 312 hitos across 6 sections × 5 subsections × 5 stages, 86 apps, 89 types, 26,000+ vocabulary rows. A queue of 1,455 live tasks is still large; it is the open work, not the whole register.
2. **The working profile.** About 30 concrete tasks fit in simultaneous attention; the file is the external memory beyond that. Quality is limited by **specification density per task**, not by the total count. A task that can be executed well has: a concrete title, a verifiable done-criterion, an owner path, and a test and dependency position when it enters the active window.
3. **Owner rules.** Closed hitos (`on`) keep their hito row and carry **0 live tasks**; their tasks move to `tasks_archive`. Every subsection keeps at least one open hito. New hitos must archive or merge achieved ones rather than grow the live queue past the cap.

## 2. Full area study

Before the note fix: 136 hitos had **no** spec markers at all (126 empty + 10 prose-only), 76 had partial markers, 100 were fully specified. The 196 generic `.2b` criteria were exactly the hitos with no `Done when` line (136 + 60).

| Section | Subsections | Hitos | Open | Closed | Blank notes before |
|---|---:|---:|---:|---:|---:|
| docs | 5 | 42 | 24 | 18 | 19 |
| backend | 5 | 67 | 44 | 23 | 24 |
| frontend | 5 | 78 | 43 | 35 | 36 |
| ai | 5 | 52 | 40 | 12 | 16 |
| data | 5 | 33 | 20 | 13 | 14 |
| community | 5 | 40 | 26 | 14 | 17 |
| **Total** | **30** | **312** | **197** | **115** | **126** |

The blank notes were concentrated in degrees 0–2 (Raw/Basic/Normal); Advanced and Super already carried generated specs. The "done" half of the project was the *least* specified: of 115 `on` hitos, only 1 had all three markers.

### Criteria audit after the fixes

- **312/312 hitos** resolve to exactly one `Deliverable:` + `Done when` + `Decision:` triple.
- **1,455/1,455 live tasks** carry a non-empty done-criterion.
- The 60 Advanced/Super notes that used `Done (generated from <URL>):` were normalized to `Done when … · Source: <URL>` without losing the source.
- `.2c` keeps one shared invariant — *"the case points back to its local owner · no stage 3/4 work"* — and is documented as an invariant, not counted as 312 distinct criteria.
- The 388 mature/generalist rows that previously had `gaps: []` now carry a criterion derived from their own hito's Done line.

## 3. Fixes applied

- **212 hitos** given a full `Deliverable / Done when / Decision` note, preserving any existing fragment. Section-specific done-criteria (map → one entry per item with a source link; work → no orphaned or archive row; contracts → same rule in every tier; schemas → unique id and validating payload).
- **1,872 generated task criteria** regenerated from those notes for the seed and infant bands.
- **388 mature/generalist criteria** filled and **60 legacy markers** normalized.
- Result: **0 blank notes, 0 empty live criteria**, 312 fully structured hitos.
- **Task reshape applied** with a backup (`milestones.json.bak-2026-11-20`): open hitos now carry 1 seed + 3 infant + 3 mature (+1 generalist); closed hitos keep their row and their 805 tasks move to `tasks_archive`.
- No hito was added, removed, reopened or closed. Hito states, ids, stages and the 124 hito edges are unchanged.

## 4. Target — 1,455 live + 805 archived

| Layer | Tasks | Rule |
|---|---:|---|
| Seed | 197 | **1 per open hito** — local definition + decision |
| Infant | 591 | **3 per open hito** — the main execution band |
| Mature | 591 | **3 per open hito** — publish · verify · decision |
| Generalist | 76 | **1 per open grown/full hito** — preserves C2 |
| Closed hitos (`on`) | 0 live | 805 tasks in `tasks_archive` |
| **Live total** | **1,455** | `197 × 7 + 76` |
| **Archived total** | **805** | 690 `pendiente` + 115 `hecha` |

**1,182 of 1,455 live tasks (81%) sit in the execution and mature bands.** That is the deliberate concentration; seed is a single local-definition step and grown/full keep their one generalist.

The arithmetic is explicit: `197 × 7 + 76 = 1,455`, which is exactly the number of tasks that were already attached to open hitos. **Closure alone produces the live target.** The 1/3/3 shape is a zero-sum rotation — seed `591 → 197` (−394), mature `197 → 591` (+394) — kept because the mature band now carries the three-line spec, not because the number requires it.

### By section

| Section | Open hitos | Generalists | Live tasks | Archived | Total |
|---|---:|---:|---:|---:|---:|
| docs | 24 | 15 | 183 | 126 | 309 |
| backend | 44 | 15 | 323 | 161 | 484 |
| frontend | 43 | 19 | 320 | 245 | 565 |
| ai | 40 | 8 | 288 | 84 | 372 |
| data | 20 | 9 | 149 | 91 | 240 |
| community | 26 | 10 | 192 | 98 | 290 |
| **Total** | **197** | **76** | **1,455** | **805** | **2,260** |

### By degree (subsection ladder)

| Degree | Ladder | Live | Archived | Total |
|---:|---|---:|---:|---:|
| 0 | Raw | 224 | 322 | 546 |
| 1 | Basic | 217 | 266 | 483 |
| 2 | Normal | 406 | 217 | 623 |
| 3 | Advanced | 296 | 0 | 296 |
| 4 | Super | 312 | 0 | 312 |

## 5. Minimums and anchors

- **30 subsections**, minimum **2 open hitos** each (max 17). The "at least one open hito with 3 tasks" floor is satisfied in every subsection without reopening a closed one.
- Closed hitos keep their hito row, stage, `state_mirror`, dependencies and title — only their tasks move to `tasks_archive`.
- Every open hito keeps a seed task (local definition + decision), 3 infant tasks and 3 mature tasks; grown/full keep their generalist. No section loses its stage-4/5 representation.
- **Mature band:** `.3` publish keeps its ID and the valuation anchor; `.3b` verifies against the hito's `Done when` line; `.3c` records the `Decision:` and its owner. The live `.3` anchors keep 107 of the original 123 incoming edges; the 15 that pointed at archived `.3` tasks are covered by the matching hito edges, so PROC-07 ordering and C6 exceptions stay intact.
- **Task edges:** 124 → 108 live. The 15 live edges that pointed from open `.3`/`.4` tasks at `.3` tasks of closed hitos were dropped; all 15 have a matching hito-level edge, so unlock counts are preserved by `HITO_UNLOCK` and `--check` no longer sees dangling task references. One further edge (`channels-05.3 → levels-21.3`) moved with its closed source into `tasks_archive` and stays recorded there.

## 6. Quality policy

| Tier | Count | Fields carried |
|---|---:|---|
| Active window | ~30 | title + criterion + owner + **test + dependency position** |
| Specified backlog | ~1,425 | title + criterion + owner; test/dep added on activation |
| Archived | 805 | original row + `closed_reason` + `closed_on` |

Full test/dependency detail is added **when a task enters the window**, not up-front for all 1,455. A task is never marked `hecha`/`parcial` without a verifiable pointer (PROC-08/09). The gate now rejects an empty criterion, so the dense backlog is also a specified backlog.

## 7. Cap, churn and replenishment (PROC-09)

- Cap: **1,455 live tasks / 197 open hitos / 312 hitos total**; 805 archived rows are preserved.
- A new hito arrives ⇒ close (0 live tasks) or merge an achieved hito first. The 115 closed hitos are the merge pool.
- The cap changes only by owner decision, never by accumulation.
- `taskSet.queuePolicy` in the register holds the loop: `hardCap` 1,455, `recommendedMax` 1,400, `headroom` 55, `replenishBelow` 1,200, `activeWindow` 30, `activeWindowFloor` 20. The same object is embedded in the Work block and checked against the register. The gate now requires `replenishBelow < recommendedMax <= hardCap` and `headroom == hardCap - recommendedMax`; live is currently at the hard cap, so the first replenishment cycle *reduces* it to 1,400 instead of refilling to 1,455.
- **Done moves a task out of the queue.** Work has an **Archive · done + closed-hito tasks** drawer below the register; the `Done` button on a live task moves it there, lowers the live count by one, and can be undone individually or wholesale. The 805 canonical archived rows are always listed there; local moves are a browser overlay until the register is edited. The list is lazy, searchable and patched in place, and each row shows a `reason_code` (`closed_hito`, `done`, `superseded`).
- **Replenish, don't just trim.** When live tasks descend below 1,200, specify new tasks in the 1 seed + 3 infant + 3 mature shape until the queue is near the 1,400 target again, before taking more work. Keep ~30 active-window tasks fully specified with tests and dependency positions (floor 20) so there is always a next task. This is PROC-09, with `jsony` as its checker; the drawer turns the threshold and the 55 reserved slots into visible counts instead of abstract rules.
- **Local → canonical is reviewed, never silent.** `Export moves` writes `flove-work-moves/1`; once committed to `debates/work-moves.json`, jsony treats it as critical until applied. `--apply-moves` requires one fully specified replacement per move (same hito) because the 7/8-task shape gate forbids simply deleting a task; it then updates the register, both projections and the mirrored counts.

## 8. Gate changes (applied)

- `EXPECTED_TASKS`: `2260 → 1455`; new `EXPECTED_ARCHIVED = 805`; `EXPECTED_TICKETS`: `33 → 37` for the four follow-up tickets in §13.
- Checker rule `len(tasks) < 2` becomes: `0` required when hito `state == "on"`, `7` (or `8` with generalist) required when open.
- New checks: every live task has a non-empty criterion; every hito has exactly one `Deliverable:` / `Done when` / `Decision:`; live and archived IDs are unique and disjoint; closed features may carry 0 tasks; the embedded Work `archive` IDs match `tasks_archive`; the embedded `queuePolicy` matches `taskSet.queuePolicy` and its thresholds stay ordered; `taskSet.live`/`archived` and every `reason_code` match the register; jsony blocks an unapplied `work-moves.json`; the summary prints live + archived counts.
- `README.md`'s stage description, count and PROC-09 section now match the new shape; `hitos-audit.md` and `questy-proposals.md` carry pre-reshape banners; `INDEX.md` and `pendings.md` use 37 tickets / 425 items.
- `--build` resyncs the embedded Work block (now with `archive` and `queuePolicy`); `--check` runs green before and after. `jsony_check.py` also fails if the embedded archive or queue policy drifts from the register.
- `apply_moves()` validates an export (dry run by default), then with `--commit` folds it into the register, rebuilds `common.json` and the embedded block, consumes the patch and mirrors the archive count. `check-restore.py` drills a closed-hito reopen in memory; both share `register_projection.py` with the two generators.

## 9. Rollout

1. ✅ Fill the 212 notes and regenerate the 1,872 criteria.
2. ✅ Fill the 388 mature/generalist criteria and normalize the 60 legacy markers.
3. ✅ Build `common.json` — the page-facing join of hito info boxes and tasks.
4. ✅ Apply the reshape on all 312 hitos with a backup; run `--check`, `--build`, `--check`.
5. ✅ Verify 1,455 unique live task IDs, 805 archived, and 30 subsections with an open hito.
6. ✅ Add the Work archive drawer, the per-task `Done` action and the four follow-up tickets; add PROC-09 and `queuePolicy`; teach the gate and jsony about the embedded archive and the new ticket count.
7. ✅ Close the local → canonical loop: `Export moves`, reviewed `work-moves.json`, one replacement per move, `--apply-moves --commit`; add headroom 1,400 / 1,455, archive reason codes and a read-only restore drill.
8. ✅ Execute the §13 tickets as verification runs (§14): archive round trip, join drift, restore drill and the replenishment pilot. All four gates are green.
9. ✅ Reviewed the five-hito mature band (`map-05`, `systems-04`, `contracts-03`, `tree-05`, `channels-02`): all seven-task shapes read correctly, and started the active window. The first 30 tasks by PROC-07 (6 × unlock 4, 21 × unlock 3, 3 × unlock 2) are listed in `taskSet.activeWindow`; every live task now carries an `owner` path (its hito's canonical source). **Next:** bring the live count from 1,455 down to the 1,400 target as the queue churns.

## 10. Risks and tradeoffs

- **Archive, not deletion.** The 805 closed-hito tasks — 690 `pendiente`, 115 `hecha` — stay in `tasks_archive` with `closed_reason` and `closed_on`. Reopening a hito restores its tasks; the pending rows remain auditable. To roll back the whole reshape: `cp milestones.json.bak-2026-11-20 milestones.json`, then `--build` and `--check`.
- **The dropped edges.** Fifteen live edges pointed at archived `.3` tasks and all had a matching hito edge; a sixteenth (`channels-05.3 → levels-21.3`) moved with its closed source into `tasks_archive`. The fix is documented in §5 and logged by the migration script.
- **Depth vs breadth.** Concentrating in infant/mature leaves seed thin by design; a hito whose real work is local definition can still be promoted by the owner.
- **Stage names.** `mature` remains the publish band, matching `plans/index.md` (F3 = nety identity + Publish). Verification and decision recording sit around publish, not instead of it.
- **Quality ceiling.** Do not replenish past 1,400 while the active-window tasks lack tests and dependency positions; 1,455 is a hard cap, not a target. Below 1,200, replenishment is a duty, not an option; ambition argues for density, not row count.
- **Local vs canonical archive.** A `Done` click is browser-local so the static page stays honest: it shows the move immediately but cannot edit `milestones.json`. Until the register is edited, Work reports both the 805 canonical rows and the local moves, and the drawer can undo them. The export is the review boundary; no static page writes the register on its own.
- **Replacement, not subtraction.** Because an open hito must keep 7/8 tasks, applying a move without a new fully specified task would break the shape gate. That is why `--apply-moves` insists on a replacement: the live count is refilled while the archive grows, and the 55-slot headroom is created by *not* replenishing above 1,400.
- **Stale mirrors.** `hitos-audit.md` is a pre-reshape snapshot; `README.md` and `--check` are the current counts. Regenerate the audit from `milestones.json` when its per-field table is next used.

## 11. Plan description and the page join

A hito's definition does not have to fit inside `notes`. It can be **extended through a plan description** — the long-form prose in `debates/plans/index.md` or a per-plan MD — while the definition information itself stays standardized.

- **One owner, one shape.** `milestones.json` stays the canonical register; a plan description is the fallback detail (PROC-01), never a second authority.
- **Three markers everywhere.** Whether the definition lives in `notes` or in a plan section, it carries `Deliverable:` / `Done when` / `Decision:`. The gate verifies exactly one of each.
- **Pointer in the register.** `notes` keeps the short three-line spec plus `Ref: <plan path>#<anchor>` when a plan description exists.
- **`common.json` is the page-facing join.** Generated by `tools/dev/build-common.py`, it projects every hito's info box (`spec`), owner page, plan page, live task ids and archive summary into one `flove-common/1` file. The page exposes `loadFloveCommon()`, `floveHito(id)` and `floveTask(id)`; the embedded Work block stays the offline fallback and now carries its own compact `archive` (805 rows) plus `queuePolicy`, so the drawer works without a fetch. Every task row carries the PROC-08 standard — `title`, `criterion`, `owner`, `evidence` — plus `plan_id` / `plan_page` (its `development/wiki/plans/` page) and `standard` (the owner-page section that proves it done). `counts` carries the 438 split — 326 hitos + 37 tickets + 75 pendings rows — and `documents` groups hitos by their source doc. `common.json --check` and `jsony_check.py` fail when either projection drifts.
- **Canonical rule.** `milestones.json` → (generator) → `common.json` → page. Never hand-edit `common.json`; edit the register and rebuild.

## 12. Decision map

| ID | View | Status |
|---|---|---|
| D1 | Third view: archive-first, publish/verify/decision mature band, criteria gate | **Chosen and applied** |
| D2 | Proposal as written: 1/3/3 rotation with `.3b`/`.3c` left unspecified | Retired — the rotation without criteria put 394 rows in the emptiest band |
| D3 | Closure only: archive 805, keep 3/3/1 | Superseded — archive is in place; the mature band now earns its three rows |
| D4 | Gate first: add criteria/marker checks before any reshape | Implemented, then folded into D1 |
| D5 | Pilot first: five hitos before the full apply | Kept as a review sample after the full apply |

## 13. Related tickets added

Four `new_tickets` rows were added to the canonical register for this change
(33 → 37 debate tickets; 422 → 426 items). They are follow-up verifications, not
replacements for the code already applied:

| Ticket | Area | What it checks |
|---|---|---|
| `NEW-WORK-ARCHIVE-UI` | frontend / quality | `Done` → leaves live list → appears in archive → survives reload → undo; mobile and keyboard. |
| `NEW-WORK-REPLENISH` | docs / plan | Pilot PROC-09: cross 1,200, specify back toward 1,400 (cap 1,455), keep the ~30-task window full. |
| `NEW-WORK-JOIN-CHECK` | backend / contracts | `jsony check_common` plus `build-common.py --check` fail on any live/archive drift. |
| `NEW-WORK-RESTORE-DRILL` | docs / work | Reopen one closed hito on a copy and confirm its tasks return from `tasks_archive` intact. |

No hito was added, removed, reopened or closed. The reshape is reversible from `milestones.json.bak-2026-11-20`; the pre-queue snapshot is `milestones.json.bak-2026-11-20-prequeue`; `common.json` is generated.

## 14. Verification run (2026-11-20)

The four tickets were executed as read-only drills; no ticket was promoted into
the live task index, so the 1,455 / 805 counts are unchanged. The active window
(§9.9) was then specified without moving a task: the 30-task window was listed
and an `owner` path (hito source, verified on disk) was added to all 1,455 live
tasks; no tests, ranks or new dependency edges — all gates green.

| Ticket | Drill | Result |
|---|---|---|
| `NEW-WORK-ARCHIVE-UI` | Stubbed-DOM run of the Work IIFE: first-open build (805 rows), `Done` → 806/1454 + 1 local row + `localStorage`, `Restore` → 805/1455, `Reset` → 805/1455, `Export moves` → `flove-work-moves/1` with 1 move, search/toggle handlers wired. | Pass |
| `NEW-WORK-REPLENISH` | Same run with 256 preset moves: live 1,199, archive 1,061, PROC-09 prompt “specify new tasks up to 1400”, headroom 201 to target and `cap +55`. | Pass |
| `NEW-WORK-JOIN-CHECK` | Temporary drift in `queuePolicy` → `jsony: critical=1`; restored → `critical=0`. `build-common.py --check` green. A committed export with no replacement → `jsony: critical=1` until applied. | Pass |
| `NEW-WORK-RESTORE-DRILL` | `python3 tools/dev/check-restore.py`: `map-01` — 7 tasks restore cleanly, live 1,455, archive 805 → 798 on the copy. | Pass |

End-to-end apply test on a full snapshot: a patch with one `Done` move and one
replacement dry-ran, then committed; the register moved to 806 archived with
1,455 live, `common.json` and the embedded block regenerated, the patch consumed
and all gates green. The snapshot was restored afterwards — the delivered state
is still 805 archived.

## 15. Related work suggested (not yet registered)

These are candidates, **not** new tickets: adding them would change the register
count again, so they wait for an owner decision.

| Candidate | Why now | Done when |
|---|---|---|
| `NEW-WORK-HEADROOM-TRIM` | Live is still at the 1,455 hard cap; the 55 reserved slots do not exist yet. | Live ≤ 1,400, active window full, no open hito below 7/8 tasks, all gates green. |
| `NEW-WORK-MOVE-PATCH-E2E` | The export → review → apply path was tested once by hand on a snapshot. | A CI drill creates a patch, dry-runs, commits on a copy, asserts consumed patch + mirrored counts, then restores. |
| `NEW-WORK-ARCHIVE-VIRTUAL` | The drawer builds 805 `<li>` rows on first open; it will grow. | First-open and filter repaint stay under a stated budget with 2,000 archive rows. |
| `NEW-WORK-TOAST-UNDO` | Undo currently requires opening the drawer and finding the row. | A keyboard-accessible undo toast reverts the last `Done` without leaving the matrix. |
| `NEW-WORK-REASON-TAXONOMY` | 805 rows share one free-text `closed_reason`; the drawer derives a code at render time. | Canonical rows carry a coded reason plus the old text, and the gate rejects unknown codes. |
| `NEW-WORK-PROC09-AUDIT` | The threshold is visible in the page but not reported over time. | A scheduled report shows live count, headroom, active-window fill and the below-floor alert. |

---

# Historical hitos audit

> Source: `development/wiki/archive/old/hitos-audit.md` (archived 2026-11-21).

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

Result: `needs_split: false` on all 312 hitos. Q133 reopened the `grown`/`full` question: 76 generalist tasks were added, so Q106/Q111 now stand at 1012 tasks. Re-run `python3 tools/dev/build-work-tracker.py --build && --check` after any tracker edit — item 13 (`--audit`) was explicitly not done.

## Conflict register

One table, one home (Q128). Three columns only (Q138); every listed conflict
carries its decision in the third column. The task order is described in
[`../README.md#task-order-proc-07`](../../AGENTS.md#proc-07-order-tasks-by-unblocking-then-ease).

| ID | Conflicto | Decisión |
|----|-----------|----------|
| C1 | `work-15`, `work-16`, `work-18` shared the title "Should docs include code examples?" (Q122/Q134) | Merged into `work-15`; the other two ids are gone and the count is 312. |
| C2 | No tasks existed for `grown` (37) or `full` hitos (Q106/Q111 vs Q133) | 76 generalist tasks added, one per hito, state `pendiente`, effort `difícil`/`muy difícil`; total 1012. |
| C3 | 124 hito edges but no task `depends_on`; "unlocks" had no data (Q126/Q139) | Effort valued by hito dependientes; all 124 hito edges mirrored as task→task edges on each hito's valuation task (`.3`/`.4`), no cycles. |
| C4 | Dependency order cuts across `stage` (Q127/Q141) | Unblocking first, then ease, independent of `stage`; the Work detail list follows that order. |
| C5 | PROC-01…06 had no sequencing rule (Q132) | PROC-07 added with the eight fields; the human section is README "Task order". |
| C6 | 7 edges have a dependiente more advanced than its prerequisite (Q130): `shell-07`←`shell-05`, `shell-09`←`shell-06`, `skills-05`←`skills-03`, `skills-08`←`skills-03`, `schemas-06`←`schemas-05`, `docs-06`←`docs-05`, `channels-05`←`levels-21` | Registered exception; PROC-07 is advisory, not a hard gate. |
| C7 | `contracts-04` and `quality-02` were the same checker in backend and frontend (Q131/Q135) | Merged into `contracts-04`; frontend coverage recorded as evidence in the title/notes. |
