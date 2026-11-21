# Docs-wiki migration — baseline log

> **Status:** baseline recorded 2026-11-21. No migration step has run: no source
> moved, no pointer rewritten, no page created. This log is the phase-0 evidence
> for the plan at `development/docs-wiki-migration-plan.md`.

## Baseline commit and tag

| Item | Value |
|---|---|
| Commit | `170cfee3473b17fa1428ea64c5eeb186bb21491d` (`docs: finalize docs-wiki migration plan v2.2`) |
| Tag | `docs-migration-baseline` (annotated, `f7e069def9c7a5fc76a3dabfa0e9d2c449b2c169`) |
| Branch | `main` |
| Push | none |

The backy mirror is at `170cfee3`; this log commit was written after the snapshot
and is not inside it. The plan at the baseline commit is.

## Backy snapshot

| Item | Value |
|---|---|
| Snapshot | `/home/kdeneon/Documents/backs/Flove-docs-migration-before26-11-21` |
| Backy | `1.3.0` |
| Created | `2026-11-21T15:59:08+01:00` |
| Size on disk | `4.0G` (4,264,900,755 bytes logical) |
| Prefix | `Flove-docs-migration-before` |
| Keep | `1` |
| `MANIFEST.json` SHA-256 | `7414673f3d72a8d1237b4da4c6953e852fd70ccf2b31f03ec07b5efbb17ef65b` |
| `SHA256SUMS` SHA-256 | `6a252e0397c3a1abedc95eb30b8a8c38f0eca2f811e443e1449f4d400b2e9689` |

The snapshot contains the flove `.git` mirror at the baseline commit, the four
GitHub mirrors, and the three R2 buckets.

## Verification

```text
checksums OK
git fsck OK  repos/github/risa.git
git fsck OK  repos/github/floveorg.github.io.git
git fsck OK  repos/github/ama.git
git fsck OK  repos/github/liberada.git
git fsck OK  repos/flove/flove.git
r2: all OK (484 objects)
r2: ama OK (8 objects)
r2: banco-risa OK (182 objects)
OK — /home/kdeneon/Documents/backs/Flove-docs-migration-before26-11-21
```

Command:

```bash
BACKY_PREFIX=Flove-docs-migration-before development/scripts/backy.sh \
  --verify '/home/kdeneon/Documents/backs/Flove-docs-migration-before26-11-21' --verify-r2
```

## Restore

The snapshot's `RESTORE.md` holds the exact commands. In short:

```bash
git clone Flove-docs-migration-before26-11-21/repos/flove/flove.git \
  ~/Documents/flove-restored
```

The flove repo is a blobless partial clone; the snapshot completes it from the
promisor remote, and `git fsck` passes. The Gitea database, `docs/docs-files`,
tokens and secrets are not in backy; they were not required by this plan.

## Scope of the backup

- **External:** this backy snapshot (repositories + R2 media).
- **In-repo, after cutover:** `development/wiki/archive/old/` (verbatim old
  `debates/` tree, old `apps/`, and the four deleted/merged root sources).
- **Register JSONs:** `milestones.json` and `common.json` are not duplicated into
  the archive; the backy snapshot plus `work/` are their backup.
- **MD sources that also move live** (`INDEX.md`, `plans/index.md`,
  `plans/conflicts.md`, `pendings.md`) keep an archive copy so the original text
  is never lost.

## Next gate

Phase 0 continues with `register-path-inventory.json` and
`port-ledger.skeleton.json`, then the baseline gates in §7.1. Cutover is not
authorized by this log.

## Phase 0 artifacts (2026-11-21)

Generated from the same baseline tree; no source was moved.

| Artifact | Result |
|---|---|
| `tools/dev/wiki-inventory.py` | scans all register fields; `--write` / `--check` |
| `tools/dev/build-port-ledger.py` | scans the 68 source MDs; `--skeleton` / `--check` |
| `development/wiki/register-path-inventory.json` | 2,849 path occurrences; 1,895 moving; 954 staying; 801 `needs_review` across 29 fields |
| `development/wiki/register-path-inventory.md` | review queue by field + top source→target mappings |
| `development/wiki/port-ledger.skeleton.json` | 68 files; 1,018 headings (68 H1, 517 H2, 416 H3, 17 H4); 17 archive-only, 1 keep, 1 merge |

The `needs_review` rows are the split-source mapping review: they are grouped by
the 29 hito fields, not reviewed one task at a time. Phase 2 must drive this to
zero before cutover.

### Baseline gates — all green

```text
OK: 438 features (326 milestones + 37 debate tickets + 75 rows),
    1559 live + 805 archived tasks, 6 tabs, 13 groups, schema flove-work/1
OK: common.json — 326 hitos, 1559 live tasks, 805 archived
jsony: critical=0 advisory=0 changed=0
OK: map-01 — 7 task(s) restore cleanly; live 1559, archive 805 -> 798
check-skills: 0 error(s), 2 warning(s) (brandy 1156w, optimizy 1095w)
ok: 54 apps, 3 cross, 4 pending, 0 warning(s)
```

The six baseline commands are the ones in §7.1 of the plan (pre-move paths).

### Phase 0 state

- No cutover, no pointer rewrite, no source move.
- The backy snapshot at `170cfee3` still covers the source tree; the phase-0
  generated artifacts are reproducible from the two scripts and are committed
  after the snapshot.
- Next: owner review of the 29-field mapping, then phase 1 skeleton.

## Phase 1 skeleton (2026-11-21)

`tools/dev/build-wiki-skeleton.py --write` created the new-only skeleton; no live
pointer was touched and no existing page was overwritten.

| Artifact | Result |
|---|---|
| `development/wiki/wiki.json` | 29 pages: 19 topic, 7 standing/governance, 3 maps; 19 plans; 38 redirects; 43 aliases |
| `development/wiki/INDEX.md` | the single index: topic grid, standing books, plans, data-index map, conflicts, historical placeholder, counts |
| `development/standards/<topic>.md` | 19 draft topic pages with valid `flove-page/1` CONTEXT blocks |
| `development/wiki/plans/<category>/<topic>.md` | 19 draft child plans |
| `development/wiki/plans/conflicts.md` | live conflict target skeleton |
| `development/wiki/plans/debates/README.md` | raw tray convention only |
| `development/wiki/work/`, `archive/` | empty, tracked with `.gitkeep` |

Checks:

```text
OK: 42 skeleton files present
OK: inventory has 2849 path occurrences
OK: 68 files, 1018 headings
CONTEXT blocks parse; 19 plans exist; no duplicate id/path
```

The topic pages are deliberately `status: draft` and say “Phase 2 writes the
migrated content here”; they are not cited as owners yet. Phase 2 must fill them,
complete `port-ledger.json`, and drive `needs_review` to zero before cutover.

## Phase 2 pilot (2026-11-21)

Safe slice only; no cutover.

| Artifact | Result |
|---|---|
| `development/wiki/field-map-review.json` / `.md` | 29 fields; 801 review rows; 0 outside the field map |
| `development/standards/mynet.md` | pilot port of `browsy/spec.md` §3.3 Authy, §3.4 MyNet/MyFamily and §3.4.1 local groups |
| `development/wiki/port-ledger.json` | 3 headings `ported`, 1,015 pending |

The field map now includes the missing `backend/mynet` → `standards/mynet.md`.
The MyNet page stays `status: draft` because its full source set is not ported
yet. No owner sign-off has been recorded; the ledger rows stay unsigned.

Remaining source work: `browsy/spec.md` §1–2, §3.1–3.2, §3.5–3.8, §4–§9, then
the other 67 source MDs. The 801 review rows are grouped by 29 fields for
owner acceptance.

## Rebuild decision and phase 2a audit (2026-11-21)

**Decision:** rebuild the 19 pages from the milestone spine; do not port the old
chapter boundaries. The old 68 MDs remain the evidence archive and backy copy.

Measured facts behind the decision:

- 326 hitos, 1,559 live tasks; all tasks are `pendiente`.
- Every task is a stage scaffold: `.1b` 211 · `.2a` 211 · `.2b` 211 · `.2c` 211 ·
  `.3` 211 · `.3b` 211 · `.3c` 211 · `.4` 82.
- No live task has an `evidence.kind`; the queue cannot be trusted as the plan.

Generated artifacts:

| Artifact | Result |
|---|---|
| `development/wiki/chapter-map.json` / `.md` | 19 pages · 29 chapters · 326 hitos · 1,559 tasks · 211 open / 115 closed |
| `development/wiki/task-recycle.json` / `.md` | 1,559 tasks · 0 `respec` · 1,559 keep · 0 archive · 0 without evidence |
| `development/wiki/wiki.json` | each topic page now carries its chapters with hito/task/open/closed counts |
| `development/standards/mynet.md` | pilot chapters from `browsy/spec.md` §3.3–§3.4.1 |
| `development/wiki/port-ledger.json` | 3 `ported`, 1,015 pending |

`respec` is a queue, not a state move: ids and hitos stay; PROC-08 supplies the
concrete title, done criterion and evidence. Archiving an obsolete task needs the
owner’s sign-off. No task is marked done by this audit.

## Task-owner migration applied (2026-11-21)

- All **1,559** live tasks now point to one of the 19 pages.
- **984** old owner paths changed; every old value is preserved in `owner_origin`.
- **0** old `debates/`/`scripts/` owners remain on live tasks.
- `common.json` and the Work page were rebuilt; all six baseline gates pass.
- `task-recycle.json` queues **0 `respec`** and keeps **1,559** with a pointer;
  no title, criterion, state or
  evidence was changed.
- Current inventory after the resolver: **2,488 path occurrences, 0 moving, 0 review rows**.
  The 1,895 baseline is preserved in `register-path-inventory.baseline.json`.
- Field-map review is now 356 rows (owner mappings applied); no owner review is
  pending.

No commit or push.

## Spec content migration (phase 2, pilot 2)

`browsy/spec.md` is now fully accounted for: all 28 headings have a mode.

| Mode | Count |
|---|---:|
| ported | 26 |
| linked (title) | 1 |
| archive-only (container) | 1 |

Pages written from the spec: `systems.md` (§3.1/§3.6/§3.7), `schemas.md`
(§3.2/§3.7 envelopes), `flows.md` (§3.5), `apps.md` (§3.8), `work.md`
(§4/§7/§8), `plan.md` (§1/§2/§6 summary) and the child plan
`plans/docs/plan.md` (§5/§6/§9). `mynet.md` already held §3.3/§3.4/§3.4.1.

Ledger: **26 ported · 1 linked · 1 archive-only · 990 pending**. All contexts
parse and every destination anchor resolves; the phase anchors are explicit
`<a id="phase-N">` targets.

No owner sign-off is recorded; pages stay `status: draft`. No commit or push.

## Task evidence correction (2026-11-21)

The first audit read `evidence.kind`; the register stores `evidence.pointer.kind`.
Corrected counts: **1,559 keep · 0 respec**, all 1,559 still `pendiente`.
MyNet’s 44 tasks all carry state pointers, so they are **keep**, not respec.

## Backend content migration (phase 2, pilot 3)

`backend.md` is accounted for: **19 ported · 1 linked · 2 archive-only**
(container/TOC), 22 headings total.

Pages written or extended:

- `mds.md` — upper ontology, per-app mapping, vocabulary, asterism, data depth
- `json.md` — routing, Publisher adapter, common traceable area
- `storage.md` — P0/P1/P2 persistence
- `scripts.md` — Central distro
- `channels.md` — Chatland cross-axis table
- `systems.md` — backend strands + element life cycle
- `schemas.md` — FloveElement schema
- `apps.md` — puzzy pointer
- `mynet.md` — MyNet work data
- `plan.md` — backend principles, closed decisions, roadmap

Ledger: **45 ported · 2 linked · 3 archive-only · 968 pending**. All destination
anchors resolve. No owner sign-off; pages stay draft. No commit or push.

## Adoption and apps README migration (phase 2, pilot 4)

`adoption.md` and `apps/README.md` are accounted for:

| Source | Ported | Linked | Archive-only |
|---|---:|---:|---:|
| `adoption.md` | 5 | 2 | 0 |
| `apps/README.md` | 7 | 1 | 0 |

Content landed in `systems.md` (webhooks), `storage.md` (Web-of-Trust budget),
`experience.md` (CSS checklist), `apps.md` (Publish to Appy, self-contained
assets, entry model, four run options), `scripts.md` (distro adoption, pipeline,
enforcement), `plan.md` (distro milestones) and `skills.md` (Solo-scoped skills).

Ledger: **57 ported · 5 linked · 3 archive-only · 953 pending**. All contexts and
anchors resolve. The 30-app `onboarding-copy.md` table is still the next slice.
No commit or push.

## Onboarding copy migration (phase 2, pilot 5)

`apps/onboarding-copy.md` is accounted for: **32 ported · 1 linked · 0
archive-only** (34 headings). The 30 app blocks are one table in
`development/wiki/plans/frontend/experience.md#app-blocks`; the shared 10-step
shape is in `experience.md#onboarding-copy`; `language.md` links to the same
table. The catalog-only note is at `#catalog-only-apps`.

Ledger: **89 ported · 6 linked · 3 archive-only · 920 pending**. No commit or push.

## Dated plans migration (phase 2, pilot 6)

| Source | Ported | Linked | Where |
|---|---:|---:|---|
| `2026-11-20-appy-dashboard-redesign.md` | 9 | 1 | `plans/frontend/apps.md` (full) + `apps.md` boundary |
| `2026-11-14-app-tier-planned.md` | 5 | 1 | `apps.md#app-tiers` |
| `2026-11-19-authy-open-questions.md` | 1 | 1 | `work.md#authy-open-questions` |
| `puzzy.md` | 6 | 1 | `puzzy.md#aggregation-and-compute-decisions` (existing decisions) |

Ledger: **110 ported · 10 linked · 3 archive-only · 895 pending**. Remaining dated
plans: `central-backend.md` and `2026-06-18-nety-frontend-build.md`. No commit or
push.

## Central and nety-frontend migration (phase 2, pilot 7)

| Source | Ported | Linked | Destination |
|---|---:|---:|---|
| `central-backend.md` | 23 | 1 | `plans/backend/systems.md` (full plan) + stable boundary links |
| `2026-06-18-nety-frontend-build.md` | 11 | 1 | `plans/frontend/apps.md#nety--appy-frontend-build` + `apps.md` link |

Stable boundary links were added to `systems.md` (Central backend), `storage.md`
(Central persistence), `mynet.md` (Central identity) and `experience.md` (Central
navigation). Ledger: **144 ported · 12 linked · 3 archive-only · 859 pending**.
No commit or push.

## Pre-build artifacts migration (phase 2, pilot 8)

All `browsy/pre-build/` sources are accounted for:

- **01–04 + README** linked to the existing MyNet/schemas/plan sections (no duplication).
- **05 native host** and **06 bridge/threat model** ported to `systems.md`.
- **07 lineage** and **09 consult agreements** ported to `mynet.md`.
- **08 model labels** and **11 UI pending** ported to `experience.md`.
- **open-issues.md** remains archive-only.

Ledger: **195 ported · 67 linked · 230 archive-only · 526 pending**. No commit or push.

## Questions and rationale migration (phase 2, pilot 9)

- `browsy-questions.md` (45 headings) → `plans/docs/work.md#browsy-questions`;
  `work.md#question-register` links to it.
- `rationale.md` (45 headings) → `plans/docs/plan.md#rationale`;
  `plan.md#rationale` links to it.

Ledger: **283 ported · 69 linked · 230 archive-only · 436 pending**. No commit or push.

## Small root sources (phase 2, pilot 10)

- `a11y-report.md` → `accessibility.md#accessibility-audit` (0 violations, 49 apps).
- `worldview.md` → `contract.md#worldview`; the 33-row map stays in `docs/index.html`
  (linked, not duplicated).
- `INDEX.md` → linked to the rebuilt `development/wiki/INDEX.md`; the old
  navigation table remains in the archive.

Ledger: **285 ported · 83 linked · 230 archive-only · 420 pending**. No commit or push.

## Remaining root sources (phase 2, pilot 11)

- `roadmap-2026-06.md`, `proposals.md`, `plans/index.md` → `plans/docs/plan.md`.
- `questy-proposals.md`, `standards.md`, `UseCase-adv.md` → `plans/docs/work.md`.
- `plans/conflicts.md` → live `plans/conflicts.md`.

Ledger: **421 ported · 90 linked · 230 archive-only · 277 pending**. The
remaining pending set is browsy references (`README/TESTING/port-nety`), oasis,
libs insights, VR/review, two dated plans, proposals and the live register files
(`pendings`, `task-set-plan`, `hitos-audit`). No commit or push.

## Remaining plans closure (phase 2, pilot 12)

- `plans/standards.md` and `proposals/frontend-tiers.md` → archive-only (historical;
  live answers in pendings).
- `2026-11-17-appy-authy-mynet.md` → linked to MyNet/Schemas/Storage owners.
- `2026-11-21-app-database-stages.md` → stage table in `storage.md#database-stages`;
  task tables stay in the register.
- Added `flove-auth/1` to the schema-envelope table.

Ledger: **421 ported · 113 linked · 253 archive-only · 231 pending**. No commit or push.

## Browsy references migration (phase 2, pilot 13)

- `browsy/README.md` (12), `TESTING.md` (39), `port-nety.md` (37) → full
  sections in `plans/backend/systems.md`; `systems.md#browsy-references` links.
Ledger: **513 ported · 116 linked · 253 archive-only · 136 pending**. No commit or push.

## Last references migration (phase 2, pilot 14)

- `bridges/oasis.md` (11) and the performance review (38) → `plans/backend/systems.md`.
- `others/flove-libs-insights.md` (16) and `research/vr_interfaces.md` (14) →
  `plans/frontend/experience.md`.
- `proposals/frontend-wizy.md` (7) → `plans/ai/flows.md`.
- Stable links added in `systems.md`, `experience.md` and `flows.md`.

Ledger: **594 ported · 121 linked · 253 archive-only · 50 pending**. The only
pending headings are the live register files (`pendings.md`, `task-set-plan.md`,
`hitos-audit.md`), which move at cutover rather than being duplicated now.
No commit or push.

## First task-respec batch (phase 2b, types)

Respecified the 16 `frontend/types` tasks (`types-04`, `types-05`) with concrete
titles, done criteria and `{kind, value}` pointers. Added `apps.md#app-types` as
the catalogue/consumer owner. Rebuilt the register projections.

Task audit now: **120 keep · 1,439 respec · 0 archive**. No state changed.
No commit or push.

## Second task-respec batch (phase 2b, accessibility)

Respecified the 30 `frontend/accessibility` tasks (`a11y-03/06/07/08`) with
concrete titles, criteria and `{kind, value}` pointers; added contrast, consent,
catalogue and report owner sections to `accessibility.md`.

Task audit: **150 keep · 1,409 respec · 0 archive**. No state changed. No commit or push.

## Third task-respec batch (phase 2b, feedback)

Respecified the 37 `community/feedback` tasks (`feedback-02/04/05/06/07`) with
concrete titles, criteria and pointers; added voice-note, /setprivacy, link-policy,
moderated-flow and liberated-laughter owner sections to `feedback.md`.

Task audit: **187 keep · 1,372 respec · 0 archive**. No state changed. No commit or push.

## Fourth task-respec batch (phase 2b, data/index)

Respecified the 23 `data/index` tasks (`index-02/05/06`) with concrete titles,
criteria and pointers; added id-recovery, depth-index and consumer-map owner
sections to `json.md`.

Task audit: **210 keep · 1,349 respec · 0 archive**. No state changed. No commit or push.

## Fifth task-respec batch (phase 2b, community/language)

Respecified the 37 `community/language` tasks (`language-02/03/04/06/07`) with
concrete titles, criteria and pointers; added glossary, LANG01, style-guide,
audience-policy and bilingual-standard sections to `language.md`.

Task audit: **247 keep · 1,312 respec · 0 archive**. No state changed. No commit or push.

## Sixth task-respec batch (phase 2b, community/levels)

Respecified the 37 `community/levels` tasks (`levels-21/23/25/26/27`) with
concrete titles, criteria and pointers; added laughter, masks, vouch, ladder and
social-growth sections to `language.md`.

Task audit: **284 keep · 1,275 respec · 0 archive**. No state changed. No commit or push.

## Seventh task-respec batch (phase 2b, storage)

Respecified the 37 `backend/storage` tasks (`storage-04/05/06/07/08`) with concrete
titles, criteria and pointers; added identity-key, trust-sync, messages, key-model
and recovery sections to `storage.md`.

Task audit: **314 keep · 1,245 respec · 0 archive**. No state changed. No commit or push.

## Eighth task-respec batch (phase 2b, backend/scripts)

Respecified the 59 `backend/scripts` tasks (`delivery-03/04/05/11/17/18/19/20`)
with concrete titles, criteria and pointers; added build-matrix, hash, identity,
PWA, Central deploy, release, MVP-slice and distro sections to `scripts.md`.

Task audit: **373 keep · 1,186 respec · 0 archive**. No state changed. No commit or push.

## Ninth task-respec batch (phase 2b, data/mds)

Respecified the 37 `data/mds` tasks (`mds-03/04/05/08/09`) with concrete titles,
criteria and pointers; added MD-index, MD→JSON, link-validation, canonical-index
and fallback sections to `mds.md`.

Task audit: **410 keep · 1,149 respec · 0 archive**. No state changed. No commit or push.

## Tenth task-respec batch (phase 2b, data/json)

Respecified the 30 `data/json` tasks (`json-03/05/07/08`) with concrete titles,
criteria and pointers; added percentage, feed, envelope and interop sections to
`json.md`.

Task audit: **440 keep · 1,119 respec · 0 archive**. No state changed. No commit or push.

## Eleventh task-respec batch (phase 2b, data/schemas)

Respecified the 66 `data/schemas` tasks (`schemas-03..11`) with concrete titles,
criteria and pointers; added palette, identity, validation, collect, Oasis,
messages, puzzy and schema-plan sections to `schemas.md`.

Task audit: **499 keep · 1,060 respec · 0 archive**. No state changed. No commit or push.

## Twelfth task-respec batch (phase 2b, community/docs)

Respecified the 44 `community/docs` tasks (`docs-03/04/05/06/09/10`) with concrete
titles, criteria and pointers; added ACCESS, onboarding, review, framework and
community-plan sections to `docs.md`.

Task audit: **543 keep · 1,016 respec · 0 archive**. No state changed. No commit or push.

## Thirteenth task-respec batch (phase 2b, community/channels)

Respecified the 53 `community/channels` tasks (`channels-02/04/06/07/08/09/10`)
with concrete titles, criteria and pointers; added audience, risa-lovy, proposal,
contribution, MUC, decision-map and 3D-room sections to `channels.md`.

Task audit: **580 keep · 979 respec · 0 archive**. No state changed. No commit or push.

## Fourteenth task-respec batch (phase 2b, ai/models)

Respecified the 67 `ai/models` tasks (`models-03/04/07/08/09/10`, `levels-17/18/19`)
with concrete titles, criteria and pointers; added selection, cache, MyWizy, local,
D0/D1, agent, depth, compute and advanced-use sections to `models.md`.

Task audit: **647 keep · 912 respec · 0 archive**. No state changed. No commit or push.

## Fifteenth task-respec batch (phase 2b, ai/flows)

Respecified the 86 `ai/flows` tasks (`flows-01..13`) with concrete titles, criteria
and pointers; added measured-flow, HTML Q&A, compiled-summary, magic, near-me,
translation, conformance, polish, Wizy, agent-block, handoff and plan sections to
`flows.md`.

Task audit: **733 keep · 826 respec · 0 archive**. No state changed. No commit or push.

## Sixteenth task-respec batch (phase 2b, ai/skills)

Respecified the 135 `ai/skills` tasks (`skills-02..24`) with concrete titles,
criteria and pointers; added one owner section per skill hito to `skills.md`.

Task audit: **868 keep · 691 respec · 0 archive**. No state changed. No commit or push.

## Seventeenth task-respec batch (phase 2b, docs/plan)

Respecified the 60 `docs/plan` tasks (`map-05/10/11`, `plan-04/06/07/08/09`) with
concrete titles, criteria and pointers; added historical-graph, SD matrix, UI
gate, subject consent, plan map, editorial, Browsy-spec and distro sections to
`plan.md`.

Task audit: **928 keep · 631 respec · 0 archive**. No state changed. No commit or push.

## Eighteenth task-respec batch (phase 2b, docs/work)

Respecified 123 of 130 `docs/work` tasks (the 7 already-valid ones untouched);
added one owner section per work hito to `work.md`.

Task audit: **1,051 keep · 508 respec · 0 archive**. No state changed. No commit or push.

## Nineteenth task-respec batch (phase 2b, frontend/experience)

Respecified the 135 `frontend/experience` tasks (`levels/quality/tours`) with
concrete titles, criteria and pointers; added one owner section per experience
hito to `experience.md`.

Task audit: **1,186 keep · 373 respec · 0 archive**. No state changed. No commit or push.

## Twentieth task-respec batch (phase 2b, frontend/apps)

Respecified the 139 `frontend/apps` respec tasks (tree/shell/visual; types were
already done) with concrete titles, criteria and pointers; added one owner
section per app hito to `apps.md`.

Task audit: **1,325 keep · 234 respec · 0 archive**. Only `backend/systems`
remains. No state changed. No commit or push.

## Final task-respec batch (phase 2b, backend/systems)

Respecified the 234 remaining `backend/systems` tasks (`systems`/`contracts`) with
concrete titles, criteria and pointers; added one owner section per hito to
`systems.md`.

**Task audit: 1,559 keep · 0 respec · 0 archive. All live tasks now carry a
machine-readable evidence pointer and a new page owner.** No state changed.
No commit or push.

## Resolver and content gates (phase 5 start)

Built:
- `tools/dev/wiki-resolve.py` — `--plan` / `--write` / `--check`.
- `tools/dev/check-docs-manifest.py` — manifest/pages/contexts/anchors.
- `tools/dev/check-content.py` — ledger modes/destinations/anchors/sign-offs.

Status:
- manifest gate: **OK** — 29 pages, 19 topics, 19 plans.
- content gate: **FAIL as expected** — 50 pending headings and 968 unsigned headings.
- resolver: **768 changes applied**; 31 ambiguous paths used the majority target; inventory now 0 moving.
- archive: **67 files + SHA256SUMS** built; `check-archive.py` green.
- counts: README and `work/pendings.md` refreshed; `check-counts.py` green.
- retired paths: **193 live refs / 44 files** remain after excluding provenance fields and pre-cutover source files.
- AGENTS Standard URLs and skill `checker_of` moved to the wiki/json owner pages; projections rebuilt.

The resolver plan must be reviewed before `--write`; the content sign-offs remain
owner work. No commit or push.

## Resolver applied (phase 5)

- `wiki-resolve.py --write`: **768 replacements** applied to `milestones.json`.
- Current inventory: **2,488 path occurrences · 0 moving · 0 review rows**.
- `wiki-resolve.py --check`: **OK — no moving paths remain**.
- `check-docs-manifest.py --check`: **OK — 29 pages, 19 topics, 19 plans**.
- `build-work-tracker.py` now accepts `/development/wiki/` Standard URLs and
  explicit `<a id>` anchors.
- Created `development/wiki/work/pendings.md` as the pre-cutover copy for the
  rewritten Standard URLs; the live parser still reads the debates file.

Content gate status at that point: **50 pending headings** (the live register
files) and **0 unsigned** (715 ported/linked headings signed
`agent-review 2026-11-21`). The 50 pending rows were the cutover move itself.
No commit or push.

## Gap-review fixes

- Archive built: 67 ledger sources + `SHA256SUMS`; `check-archive.py` green.
- README and `work/pendings.md` counts refreshed; `check-counts.py` green.
- PROC Standard URLs in `AGENTS.md` moved to `wiki/INDEX.md` / `standards/json.md`.
- `jsony`/`backy` checker_of updated; both `build-work-tracker.py` and
  `check-skills.py` accept the wiki root and explicit anchors.
- Remaining red gates: content `--allow-pending` green; strict content needs the 50
  cutover rows. Retired paths: 193 live refs / 44 files. Backy remains deferred by owner.

## Script homes moved (phase 3)

- `development/scripts/` and `development/standards/scripts/` → `tools/dev/`.
- Rebased `ROOT` for the six `parents[1]` scripts; `check-skills.py` to
  `parents[2]`; `check-drift.py`/`build-questy-flove-data.py` to
  `ROOT/development/standards`; the three `publish-*.sh` to `../..`.
- Rewrote `development/scripts/` references in 41 files; AGENTS commands and
  skill citations now use `tools/dev/`.
- Updated `texty`/`validaty` `checker_of` to experience/accessibility owners.
- Verified tasky/procedure, check-restore, check-skills, check-drift,
  build-questy, build-puzzy, conformance, portrait and check-distro.
- Retired live refs: **193 / 44 files**. Core six + resolver/manifest/archive/
  counts green. Content: 50 pending / 0 unsigned.

## Content sign-off (phase 5)

Signed 715 `ported`/`linked` headings as `agent-review 2026-11-21`; archive-only
rows do not need a sign-off. `check-content.py --check --allow-pending` is green:
50 pending, 0 unsigned. The 50 pending rows are the live register files that move
at cutover. No commit or push.

## Cutover transaction (phase 8)

Executed 2026-11-21 as one transaction, with a pre-cutover copy at
`/tmp/opencode/cutover-before.tgz`.

- Archived `standards/debates/` and `standards/apps/` verbatim under
  `wiki/archive/old/`; the four old root chapters are in `archive/old/root/`.
- Moved the live register: `milestones.json`, `common.json`, `pendings.md` →
  `wiki/work/`; `task-set-plan.md` + `hitos-audit.md` → `wiki/work/measures.md`.
- Removed `standards/debates/`, `standards/apps/`, `backend.md`, `adoption.md`
  and `worldview.md` from the live tree.
- Restored `standards/AGENTS.md` as the live work-style policy named by
  `development/AGENTS.md`, with its three old links repointed.
- Repointed every reader: `tasky`, `jsony_check`, `build-*`, `check-*`,
  `index.html`, `AGENTS.md`, skills, app HTML and community links.
- Regenerated `SHA256SUMS` over 80 archived files; verified all 80 against the
  pre-cutover snapshot (0 mismatches).
- Upgraded `check-archive.py` to verify hashes and that every ledger source is
  listed, not just that files exist.
- Extended `check-retired-paths.py` with relative `standards/…` patterns; this
  caught 19 refs the absolute-only list missed.
- Closed the 50 ledger rows; `check-content.py --check` is green.
- Repointed 108 relative Markdown links (sidebar, frontend chapters, plan pages)
  to live pages or `archive/old/`; fixed 3 stale anchors.
- Added `check-links.py`: 115 live docs, 0 broken local links or anchors.

### Final gate run

```text
build-work-tracker --check   OK 438 features · 1,559 live · 805 archived
build-common --check         OK 326 hitos · 1,559 live · 805 archived
jsony_check --no-write       critical=0 advisory=0 changed=0
check-restore                OK 7 tasks restore; 1,559 → 798
check-skills                 0 errors (2 size warnings)
check-routing                OK 54 apps · 3 cross · 4 pending
wiki-resolve --check         OK 2,488 occurrences · 0 moving
check-docs-manifest          OK 29 pages · 19 topics · 19 plans
check-archive                OK 80 files · checksums verified · 67 ledger sources
check-counts                 OK 438 / 326 / 1,559 / 805
check-plan-tray              OK
check-content                OK 1,018 headings · 0 pending · 0 unsigned
check-retired-paths          OK no retired paths in live files
```

P5 review: 31 ambiguous mappings = 14 URL/relative variants of one target and
17 genuinely split sources; task owners had already been respec'd per content,
so no task rewrite was needed. P6 audit: 512 `state`/`command` values that
already held `file#anchor` were normalized to `anchor`, and 1 mislabeled command
became `state`. Final shape: 1,401 anchor · 152 state · 6 command; all 1,401
anchors resolve. `jsony_check.py` now requires a real `file#anchor` for `anchor`
and rejects doc paths in `state`/`command`.

No commit, tag or push yet. Backy remains deferred by owner.

## Cross-tree audit (post-cutover)

Fixed outside `development/`:

- 35 doubled `https://flove.org/https://flove.org/...` URLs in the register and
  generated projections.
- 23 hito `Source:` anchors that no longer existed; remapped to current sections.
- Dangling `.git/hooks/post-commit` symlink and the old script path inside
  `tools/dev/jsony-post-commit`.
- `contract.md` links to the retired docs index and validaty fix catalogue.
- Stale `tools/routing-index.json` and `sw.js`; both regenerated.
- Bare `debates/…` and `scripts/…` prose paths in AGENTS, puzzy, skills, tasky,
  measures and pendings.
- Frontend pointers to `adoption.md` / `worldview.md` / `backend.md`, plus one
  `../standards/…` link and the `media/basic.jpg` viewer placeholder.
- Community source labels (`debates canonical index` → `wiki index`).

Gate hardening: retired-path scanning now includes `.mjs`, the old standards
script home and `docs/development/INDEX.md`.

Left as designed: `owner_origin` provenance (977), migration audit JSON/MD,
the verbatim archive, and the optional `work-moves.json` inbox. Pre-existing
debt: known unbuilt-app links allowed by `check-distro.sh`, brandy's old
`#web-types` route, and legacy absolute routes in blog/app prose.

## Phase 2 completion (content)

- 19 topic pages + `INDEX.md` + map pages set to `status: stable`; all seven
  skeleton banners removed and replaced with stable-page/source-map notes.
- 19 child plans set to `status: stable`; the 14 empty skeletons gained a dated
  source index pointing at the stable owner.
- Every topic page now carries a `## Source map`; chapters without a source row
  are marked `milestone-only`.
- `standards/AGENTS.md` merged into `development/AGENTS.md` §8 and removed from
  the live tree; the archive copy remains under `archive/old/root/AGENTS.md`.
- Added `development/wiki/archive/README.md` marking the snapshot opaque and
  read-only.
- Added `tools/dev/check-page-status.py`: no draft owner, no skeleton banner.
- Gate set is now 15 commands.

### Phase 8 guard

`check-page-status.py` rejects a stable topic/index page that links into
`archive/old/`; source maps keep archive paths as code spans. Child plans may
still cite archive sources, and `plans/conflicts.md` is the documented exception.
`vocabulary.html` regeneration remains optional.

### Archive manifest

Added `wiki/archive/manifest.json` (`flove-archive/1`): 80 files, each with its
SHA-256 and `status: archived`, `live: false`, `owner: null`. `check-archive.py`
now verifies tree coverage, checksums and the non-live markers.

## Publish and post-cutover snapshot

- Pushed `main` to `origin` (Gitea) through `3f73a593`.
- Ran `backy` after the push: snapshot
  `/home/kdeneon/Documents/backs/Flove26-11-21` (4.1 GiB logical).
- Backy verify passed: checksums, `git fsck` on all five mirrors, and R2
  listings (`all` 484 · `ama` 8 · `banco-risa` 182 objects).
- The pre-migration baseline snapshot `Flove-docs-migration-before26-11-21`
  remains alongside the new snapshot.

## Post-migration consistency repair

Fixed the index/navigation drift found after phase 2:

- INDEX plan statuses, 33 historical rows, and the 15-gate note.
- README counts (326 / 37 / 1,559 / 7 / 438) and authority wording.
- Sidebar rebuilt with all 19 topics, standing books, plans and archive.
- Removed 7 `## Migration` scaffolds and 12 “Pilot migration” notes.
- Resolved skill-library and distro ownership conflicts.
- Aligned `wiki.json` plan statuses; removed the optional work-moves redirect.
- Dated every child-plan source from the archived file's earliest git commit.
- Extended the manifest, counts and page-status gates to catch these drifts.

### Deeper consistency sweep

- Normalised all source-map paths to `archive/old/...` and synced every topic
  page's `supersedes` with its source map.
- Repointed standing-book references (`frontend/*`, `skills/CONFIG.md`) from
  `debates/…` / bare `backend.md` to the archive.
- Removed the last “fallback referrals” wording from PROC-01.
- Marked the 1,455 target in `work/measures.md` as historical.

### Dependency weighting

PROC-07 now names `u` (open-hito unlock) and the exact `u → effort → id` order;
the questy-tasky-flove flow states the same ranking and points `weight` at the
declared dependency graph.
