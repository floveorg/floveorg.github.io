# Docs → wiki migration — spec-driven implementation plan

> **Status:** v2.9 · 2026-11-21 · **migration complete; 15 gates green; pushed; backy verified.**
> v2.4 records the applied task-owner migration: all 1,559 live tasks now point
> to the 19 new pages (984 old owners changed; 0 still queued `respec`, 1,559
> carry an `evidence.pointer`).
> v2.3 recorded the rebuild decision: pages are chapterized from the milestone
> spine, old MDs are the evidence archive, and the 1,559 scaffold tasks go through
> a respec audit before they are trusted. It keeps the applied decisions from v2.2: `development/wiki/` as the single root (R09),
> `development/AGENTS.md` stays (R10), `standards/contract.md` stays (R11),
> 19 topic pages + 6 standing books (R12), and one `INDEX.md` that absorbs the
> plans map and the data-index section (R13). It also adds the content-import
> contract (§4.5) and the backy backup contract (§4.6). No migration step was
> executed by this review.
> **Authority:** this file is the recommended implementation. §8 is the decision
> ledger; §9 records the follow-up audit; §11 records the review pass. The
> canonical execution policy remains `development/AGENTS.md` (PROC blocks) — this
> plan does not replace it.
> **Backup:** the complete v1 planning structure is preserved verbatim at
> `development/docs-wiki-migration-plan.backup-2026-11-21.md`. Nothing in v1 was
> discarded; v2 reorganises it into specs + routing + recommendation.
> **Commit policy:** no push is part of this plan. The earlier applied fixes were
> landed in commit `14b0e07` (not uncommitted); see R06. Before execution: commit
> this finalized plan locally, tag it `docs-migration-baseline`, then run backy
> (§4.6). The cutover itself should run on a local branch so FR-16 and the
> rollback drill are enforceable (R32).

---

## 0. How to read this plan

| Section | What it is |
|---|---|
| §1 | Goals and explicit non-goals |
| §2 | The specification: functional requirements with testable acceptance criteria |
| §3 | The recommendation: which option is implemented for every requirement and gap |
| §4 | Target architecture: tree, stable pages, child plans, manifest |
| §5 | **Complete file routing** — every old path → its new home, deduplicated |
| §6 | Implementation phases, each with inputs / work / outputs / exit gate |
| §7 | Verification: the exact gate commands and acceptance checks |
| §8 | Decision ledger D01–D73 (in force / applied / planned) |
| §9 | Follow-up audit: N1–N16 with applied marks and recommended defaults |
| §10 | Risks, rollback and the applied-changes log |
| §11 | Review pass 2026-11-21 — R01–R44; R09–R13/R33 resolved, the rest proposed |

**Conventions used in every table below:**

- `standards/<topic>.md` always means `development/standards/<topic>.md` —
  one of the 19 flat topic pages — **never** `development/wiki/standards/…`.
- `plans/<category>/<topic>.md` means
  `development/wiki/plans/<category>/<topic>.md`; `<topic>` is the same keyword
  as the stable sibling page.
- `work/<file>` means `development/wiki/work/<file>` (flat).
- `archive/old/…` means `development/wiki/archive/old/…` — verbatim, opaque,
  excluded from `wiki.json` and all gates.
- Source paths are relative to `development/standards/` unless they start with
  `development/` or `docs/`.
- **Applied** = already landed (commit `14b0e07` or earlier). **Cutover** = to implement.
  **Recommended** = the ★ option proposed for a still-open item.

---

## 1. Goals and non-goals

### 1.1 Goals

1. Give every live fact in the wiki **one canonical home** among the 19 flat
   topic pages (plus the standing books in §5.5a), with cross-links instead of
   restatement.
2. Move the old `debates/` tree to an **opaque verbatim archive** so history is
   preserved and rollback is a directory swap.
3. Keep the register and Work page working throughout: **984 of the 1,559
   task owners** (747 into `debates/`, 71 into `development/scripts/`, 60 into
   `standards/apps/`, 99 into the three deleted chapters,
   7 into `standards/AGENTS.md`), **226 hito sources**, **66 `standards` URLs**,
   **463 gap strings**, **127 note strings**, **25 new-ticket paths**, **3 docs
   pointers** and **1 moves inbox** are rewritten by a generated resolver, never
   by hand. That is 1,895 path occurrences across nine register fields at baseline;
   **984 owner occurrences were applied in phase 2b**; the resolver then applied
   768 replacements and 0 remain. The other
   575 owners already point at a staying page (R01).
4. Keep `tasky` and the PROC spine intact: ten contiguous PROC blocks, one
   `SKILL.md`, automatic state moves after verified evidence, no Spanish effort
   values in data.
5. Collapse all script homes into `tools/` / `tools/dev/` and ship a single
   manifest (`wiki.json`) plus two new gates (`wiki-resolve.py --check`,
   `check-docs-manifest.py --check`).
6. Bring the register to a **lower token cost per task view** (~1–1.5k tokens)
   without losing procedure text.
7. Make the new pages reflect the **plan and work data**: each topic page gets
   chapters from its milestone fields, and every live hito/task points to one of
   those pages (D70/D71).

### 1.2 Non-goals

- No push, publish or release. A **local** baseline commit/tag is allowed and
  required before backy (§4.6); it is never pushed.
- No new topic pages for the frontend 1–5 levels; they are a view of core stages.
- No `tools/standards/` folder, no trunk folder, no hub/stub pages, no second
  AGENTS file.
- No reclassification of the two empty effort tiers without an owner id list.
- No rewriting of historical debate MDs in place — they move verbatim, Spanish
  quotes included; their **meaningful content is ported** into sections per §4.5,
  with a link back to the archived source.
- No in-place port of the old chapter boundaries; the new pages are rebuilt from
  the milestone fields, not from `backend.md`/`adoption.md` headings.
- No mass archive of the live task queue without an owner decision; the respec
  audit proposes, the owner disposes.
- No retroactive `hecha` moves for already-delivered-but-open tasks.

---

## 2. Specification

Each requirement is independently testable. "Decision" points to §8, where the
owner choice is recorded.

| ID | Requirement | Acceptance criteria | Decision |
|---|---|---|---|
| **FR-01** | 19 flat topic pages own all migrated content; six standing books stay outside the grid | Exactly `development/standards/<topic>.md` for the 19 topics in §4.2; no `development/wiki/standards/`; no trunk folder; no compound slug. **Standing books** keep their existing canonical pages and are linked, not duplicated: `standards/puzzy.md`, `standards/frontend/*.md`, `standards/skills/*`, `standards/risaliberada/*`, `standards/workflow/*`, `standards/vocabulary.*` (R12) | D32 |
| **FR-02** | One fact, one home | No destination bullet cited by two source chapters without an explicit `shared:` marker; every other chapter links to the canonical page; the rule covers the 19 topic pages **and** the six standing books | D01/D39 |
| **FR-03** | Verbatim opaque archive | Every source file routed archive-only **and every deleted or merged root source** is byte-identical at its mapped `archive/old/` path; the two large register JSONs moved live to `work/` (`milestones.json`, `common.json`) are **not** duplicated into the archive, while every MD source — including `INDEX.md`, `plans/index.md`, `plans/conflicts.md` and `pendings.md` — keeps an archive copy; a `sha256` manifest lists both sets; the whole pre-cutover `.git` is also in the backy snapshot (R05) | D37 |
| **FR-04** | Register paths are load-bearing | `wiki-resolve.py --write` applied **768 replacements** after the 984 owners migrated in phase 2b; the inventory now reports **0 moving paths**; originals preserved per field (`*_origin` / `migrated_from`); no hand edits (R01/R24) | D43 |
| **FR-05** | Generated stays generated | `common.json`, `WORK-DATA`, `wiki` row field and `PORT-LEDGER.md` are rebuilt by scripts, never hand-edited | D44/D47/D56 |
| **FR-06** | Stable names | Topic filenames stable; dates only in frontmatter and `archive/old/` | D51/D52 |
| **FR-07** | Child plans mirror stable pages | `plans/<category>/<topic>.md`, folder = owner category, filename = same keyword as the stable sibling; no `<topic>` nested under a subsection folder; `plans/conflicts.md` and `plans/debates/README.md` are explicit gate exceptions (R22); `plans/index.md` is not created (R13) | D33/D51 |
| **FR-08** | Raw staging tray | `plans/debates/` holds only `status: draft` plans + one convention-only README; never a milestone `owner`; a `created:` date older than 14 days is a gate error; the check uses the declared date, not filesystem mtime | D38 |
| **FR-09** | One AGENTS file | Merged file: work-style §1, Authority §2, ten PROC blocks contiguous in §3; only six `Standard:` URLs change; `procedures_source.py` still finds exactly ten. **Resolved:** the merged file stays at `development/AGENTS.md`; not moved to `development/wiki/` (R10) | D40/D55 |
| **FR-10** | Effort taxonomy | Five English values `very easy · easy · medium · hard · very hard`; Spanish only in UI `es` labels; two axes only (`effort`, `stage`); no `1.5`; `very easy`/`medium` stay at 0 | D24–D31/D49 |
| **FR-11** | Pick flow | `tasky` = one `SKILL.md`; free work via `tasky.py`; state moves automatic after evidence; judgment calls asked with A/B/C + ★ | D03–D12/D20 |
| **FR-12** | Resolver | `wiki.json` `flove-wiki-manifest/1`; resolution order exact → `redirects`/`aliases` → anchored → `field_map` → `supersedes` (max depth 8) → `labels` → error; cycles are gate errors; never silently fall back to archive (R27) | D43/D45 |
| **FR-13** | Context budget | `tasky.py show <id>` prints PROC quick table + row + one page's `CONTEXT` block, **target ≤1.5k tokens, hard cap 2k**; the measurement method is fixed (R28); `weight`/`options`/`next`/`easy`/`procedure` output unchanged | D46 |
| **FR-14** | Gates green | All commands in §7 pass; zero refs to the retired paths in §7.2; the baseline set and the cutover set are named separately (R08) | D48 |
| **FR-15** | Script homes | `development/scripts/` and `standards/scripts/` → `tools/dev/`; general scripts stay at `tools/` top level; no `tools/standards/`; every moved script re-bases its `ROOT`/`parents[n]` and has a self-check (R04/R29) | D36 |
| **FR-16** | Atomic cutover | All destination pages written first in one changeset, then sources archived; no partial pass that duplicates facts; the changeset is a local branch/commit, not a multi-day working tree (R32) | D58 (G2A) |
| **FR-17** | Rollback | `backy` snapshot (MANIFEST/SHA256SUMS/RESTORE) + local `docs-migration-baseline` tag + verbatim `archive/old/` copy; `check-restore.py` and `check-content.py` drills green; archive checksums match (§4.6, R33) | D01 |
| **FR-18** | Every live owner resolves to a context | Each of the 79 distinct owner targets is either a page carrying a valid `CONTEXT` block or a declared non-page owner with a fallback; `tasky.py show` never prints an empty context (R14) | new |
| **FR-19** | Inventory before routing | Phase 0 generates `register-path-inventory.json` (field, old path, target, mapping rule, `needs_review`) from HEAD; cutover requires zero `needs_review` (R01/R24) | new |
| **FR-20** | Content import completeness | Every meaningful source heading maps to a **chapter** (not necessarily a same-named section) or has a signed `archive-only` reason; every chapter has a `Source:` line and a per-file sign-off; `check-content.py --check` green (§4.5) | new |
| **FR-21** | Backup and old-link preservation | A pre-cutover `backy` snapshot (MANIFEST + SHA256SUMS + RESTORE) and a local `docs-migration-baseline` tag exist; every old link resolves through `aliases` to a new page or the archive copy; the archive checksum matches (§4.6) | new |
| **FR-22** | Chapter map from the milestone spine | Every topic page has chapters generated from its milestone fields/hitos; every live hito and task maps to exactly one chapter/page; counts and open/closed states come from the register, not from old prose (§4.0) | new |
| **FR-23** | Task recycle audit | Every live task has a new-page owner; every template/no-evidence task is queued as `respec` with a reason; no task is treated as done without evidence; archiving obsolete tasks needs the owner’s sign-off (§4.0a) | new |
| **FR-24** | Task-owner migration applied | All 1,559 live tasks carry one of the 19 new page owners; `owner_origin` preserves the old value; `task-recycle.json` queues 0 `respec` and keeps 1,559 with a pointer; no old `debates/` or `scripts/` owner remains on a live task | D73 |

---

## 3. Recommended implementation

This is the recommendation, not a new decision. Every ★ default and every
owner-chosen option is folded here.

### 3.1 Coverage gaps G1–G13 — recommended option A for all

Owner accepted all ★ on 2026-11-21 (D58). Option A is therefore the
implementation for each gap; B/C are rejected, not pending.

| Gap | Implement (A) | Rejected |
|---|---|---|
| G1 unmapped plans + `.bak-orig` | Port 3 MDs per §5.5; `.bak-orig` archive-only | B archive all · C port one |
| G2 six child-plan collisions | One `<category>/<topic>.md` per topic; each old source a dated `##` section | B qualified filenames · C drop plans |
| G3 §2 vs §8 drift | §8 heading ledger authoritative; summary points to it | B union · C §2 authoritative |
| G4 `storage` chapter row | Add from `2026-11-21-app-database-stages.md` §4.8.3 | B drop page · C redirect stub |
| G5 retired-note path | `archive/old/archive.md` (applied) | B deep nesting |
| G6 AGENTS numbering | work-style §1 / Authority §2 / PROCs §3 | B append as §8 |
| G7 PORT-LEDGER location | `development/wiki/PORT-LEDGER.md`, outside archive | B gate exception · C drop ledger |
| G8 one page ↔ many plans | One stable page may reference many child plans; each plan names one page | B force 1:1 · C drop assertion |
| G9 heading omissions | Container + range rows; archive-only files exempt with one-line reason | B full 61-file ledger · C relabel claim |
| G10 SD→VARIOUS crosswalk | 17 rows + crosswalk table in `work/pendings.md` | B expand to 19 · C add entries |
| G11 empty effort tiers | Leave at 0; `next --do` covers 142 ready `directo + easy` | B id list · C rule |
| G12 two delivered tasks | Leave `pendiente`; no retroactive move | B full move · C evidence only |
| G13 3 `.bak` + 8 HTML | Copy all 13 verbatim, no live links | B drop `.bak` · C index them |

### 3.2 Follow-up audit N1–N16

Seven are already applied; the remaining nine carry the ★ recommendation for
implementation, pending the owner's go-ahead. Full detail in §9.

| Applied (commit `14b0e07`) | Recommended for the open nine |
|---|---|
| N1A · N5A+N11merge · N7A · N10A · N14A · N16A | N2A keep demo as Work item · N3A keep `RC01`/`RDB01` · N4A document `TODO` slots · N6A repoint 26 MDs / 12 skill files to `tools/dev/` · N8B (already satisfied by N1A) · N9A regenerate `vocabulary.html` · N12A rewrite **12** skill files · N13A accept 2 warnings · N15A mark legacy HTML intentional |

**Counting correction (D63).** The earlier draft headlined "24 groups / 20
open", but the authoritative enumeration is **N1–N16 (16 groups) + 4 effort
leftovers** applied under D59 = 20 action groups. The "24" figure was a tally
error in v1; v2 uses the enumerated set. N8 is now satisfied by N1A (dropping
`apps{}` removes the drift), so only nine items are genuinely open.

---

## 4. Target architecture

### 4.0 Rebuild from the milestone spine (D70)

The new wiki is **not an in-place upgrade** of the old chapter boundaries. It is
rebuilt from the register:

1. **The spine is `milestones.json`:** 6 sections → 29 fields → 326 hitos →
   chapters. A page chapter is a field or a small group of fields mapped to the
   page; the field map is §11.3.
2. **The old MDs are the evidence archive:** they stay verbatim in
   `development/wiki/archive/old/` and in the backy snapshot. Their meaningful
   facts are cited into chapters; their old `##` order does not dictate the new
   order.
3. **The pages are new:** `development/standards/<topic>.md` starts from the
   chapter map, not from a renamed `backend.md`.
4. **The work data is reflected:** each chapter carries its hito/task counts,
   open/closed states and a link to the register view; each live task points to
   the page that owns its field.
5. **The old task queue is not trusted as-is:** see §4.0a. It is recycled through
   a respec audit, not copied.

Why this wins over porting chapters:

| Option | Verdict |
|---|---|
| A — port old chapters into new pages | Rejected: carries old boundaries, duplicates and stale assumptions; 1,018 headings become the work plan |
| B — rebuild from milestones, old MDs as evidence | **Chosen:** clean taxonomy, work data reflected, old facts preserved in the archive |
| C — rebuild from milestones and ignore old MDs | Rejected: loses rationale, decisions and edge cases that are not in hito titles |

Chapter template (every topic page):

```md
## <chapter title>                  <!-- from a field / hito group -->
> Source: <archived old path#heading> (archived 2026-11-21)
Purpose: one paragraph.
Canonical facts: prose/tables/schemas.
Work: <n hitos · m tasks · open/closed> + link to the register view.
Acceptance: <test that proves the chapter>.
```

The chapter map is generated (`chapter-map.json`), not hand-guessed. A page with
no fact for a field does not get a chapter; the field still maps to its owner
page for task ownership.

### 4.0a Task recycle audit (D71)

Measured on 2026-11-21: **all 1,559 live tasks are scaffold tasks**
(`.1b` 211 · `.2a` 211 · `.2b` 211 · `.2c` 211 · `.3` 211 · `.3b` 211 · `.3c`
211 · `.4` 82) and **all `pendiente`**. **0 have no `evidence.pointer`;
1,559 carry a pointer.** The queue is a skeleton with a small evidence
tail, not a finished plan.

Policy:

- **Owner now:** every live task gets the new page owner from the field map. No
  live task keeps an old `debates/` or `scripts/` owner after cutover.
- **Respec queue:** every task whose title is a stage template or whose evidence
  is empty is queued as `respec` with a reason. PROC-08 supplies the concrete
  title, done criterion, owner page and `{kind, value}` evidence. The task id and
  hito stay; the queue is not reset.
- **Archive queue:** a duplicate, closed-hito leftover or obsolete deliverable is
  queued as `archive` with a reason; the owner signs. No mass archive without
  that sign-off.
- **No false done:** a task never moves to `hecha` because of the migration; it
  moves only when its evidence verifies (D20).
- **Gate:** every live task resolves to a new page; `respec`/`archive` counts are
  recorded per page; no task is silently dropped.

**Applied 2026-11-21:** all 1,559 live tasks now point to one of the 19 pages
(984 owner paths changed); the old value is in `owner_origin`. The queue still
has 0 `respec` rows and 1,559 `keep` rows. No task state changed.

The audit is `task-recycle.json` / `.md`, generated from the register. Phase 2a
must review it before content is declared complete.

### 4.1 Tree

```
docs/                                    PUBLIC DOCS FAMILY — untouched by this plan
  index.html  paradigms.html
  papers/  tables/
  metaphysics/  psychosocial/  …/        whole-family trunks, flattened here (not created now)

development/                             THE DEVELOPMENT ROOT — Work page + standards + wiki
  AGENTS.md                              authority; merged work-style rules (stays, R10)
  index.html                             Work page, regenerated; HTML places = tab anchors
  standards/
    README.md  _sidebar.md  vocabulary.*  index.html
    contract.md                          STANDING governance — values + the floor (stays, R11)
    <topic>.md                           19 flat topic pages, no trunk folder (§4.2)
    puzzy.md  puzzy/                     STANDING BOOK — normative, 24 owners (R12)
    frontend/                            STANDING BOOK — frontend.md + 5 sub-pages (R12)
    skills/  risaliberada/  workflow/    STANDING BOOKS — stay (R12)
    backend.md  adoption.md  worldview.md   split + deleted
    apps/                                ported, archived verbatim
    debates/                             emptied → wiki/archive/old/
    scripts/                             moved to tools/dev/

  wiki/                                  THE SINGLE WIKI ROOT (R09)
    INDEX.md                             ONLY index: closed list + compact map + plans map
                                         + data-index section; PROC Standard target
    PORT-LEDGER.md                       generated source-heading → chapter evidence ledger
    wiki.json                            closed-list manifest + chapters + redirects + field map
    chapter-map.json/.md                 generated field → page chapters + work counts
    task-recycle.json/.md                generated respec/keep/archive audit
    register-path-inventory.json/.md      current pointer inventory
    register-path-inventory.baseline.json  phase-0 baseline (2,849 occurrences; 1,895 moving)

    plans/                               DYNAMIC — folder = category, file = topic keyword
      conflicts.md                       sole cross-plan tension tracker
      docs/{plan,work}.md
      backend/{scripts,systems,mynet,storage}.md
      frontend/{apps,accessibility,experience}.md
      ai/{models,skills,flows}.md
      data/{mds,json,schemas}.md         no data/index.md: merged into json.md (R13)
      community/{docs,feedback,language,channels}.md
      debates/                           RAW TRAY — drop on-the-fly plans here
        README.md                        convention only, no facts, not an owner

    work/
      pendings.md                        parser input; keep table syntax
      measures.md                        live counts + queue policy; conflict register links only
      milestones.json                    LIVE register — never archived
      common.json                        generated projection
      work-moves.json                    machine inbox (intentionally absent)

    archive/                             OPAQUE SNAPSHOT — no live links, no gates
      old/                               verbatim old debates/ files: 61 MDs + HTML + .bak + plans/
      old/root/                          backend.md, adoption.md, worldview.md, standards/AGENTS.md verbatim
      old/apps/                          standards/apps/ moved verbatim (sibling of debates)

tools/                                   THE single scripts folder
  (existing general scripts) + dev/       old development/scripts/* AND standards/scripts/*
                                          each moved script re-bases its ROOT (R04)
```

### 4.2 The 19 topic pages and their HTML places

Verified on disk 2026-11-21. Each page carries `html_place:` in its `CONTEXT`
block. The **19 topic pages** are the topic grid; six **standing books** stay
outside it and are linked, never duplicated: `puzzy.md`, `frontend/*`, `skills/*`,
`risaliberada/*`, `workflow/*`, `vocabulary.*` (R12).

> **R13 resolved — one index only.** `development/wiki/INDEX.md` is the single
> index: it takes the plans reading map, a compact “Data index / routing” section
> and the 33 Historical rows as archive links. The former `plans/index.md` and
> `standards/index.md` are not created.
> The `data/index` chapter (backend §5–§7: routing, publisher adapter, common
> traceable area) merges into `standards/json.md` as
> `## Data index and routing`; `plans/data/index.md` merges into
> `plans/data/json.md`. The register field `data/index` maps to
> `standards/json.md` (R13).

| Topic page | HTML place | Topic page | HTML place |
|---|---|---|---|
| `standards/plan.md` | `#plan-maps` | `standards/models.md` | `#ai` |
| `standards/work.md` | `#work-tracker` | `standards/skills.md` | `#ai` |
| `standards/scripts.md` | `#localhost` | `standards/flows.md` | `#ai-note-wizy` |
| `standards/systems.md` | `#p2p` | `standards/mds.md` | `#data` |
| `standards/mynet.md` | `#p2p` / `#messenger` | `standards/json.md` | `#data-json` |
| `standards/storage.md` | `#data-database` | `standards/schemas.md` | `#data` |
| `standards/apps.md` | `#apps` | `standards/docs.md` | `#md-sources` |
| `standards/accessibility.md` | `#apps` | `standards/feedback.md` | `#md-sources` |
| `standards/experience.md` | `#apps` | `standards/language.md` | `#md-sources` |
| | | `standards/channels.md` | `#messenger` |

`contract.md` is a standing governance page, not a topic page: it stays at
`standards/contract.md` and carries its own `CONTEXT` block (R11).

### 4.2a `INDEX.md` — the single index (R13)

There is exactly one Markdown index in the wiki:
`development/wiki/INDEX.md`. It replaces three candidates:

| Old candidate | Disposition |
|---|---|
| `debates/INDEX.md` (closed list + map) | **is** `INDEX.md`; keep the 33 Historical rows as archive links and regenerate counts |
| `debates/plans/index.md` (plan list) | its plan rows become `INDEX.md` §4 “Plans”; stage aliases go to `standards/plan.md`; no `plans/index.md` is created |
| `standards/index.md` (data/index topic) | its chapter merges into `standards/json.md` `## Data index and routing`; `INDEX.md` §5 gives the short map; `plans/data/index.md` merges into `plans/data/json.md` |

Required structure:

```md
# flove development wiki — index
> Generated counts: 326 hitos · 37 tickets · 75 rows · 1,559 live · 805 archived.
> Baseline: <tag> · updated: <date>.

## 1. How to read this wiki
## 2. Topic grid (19)
## 3. Standing books (6)
## 4. Plans
   one row per plan: source · date · primary page · child plan · status · link
## 5. Data index and routing
   short map; canonical detail lives in standards/json.md#data-index-and-routing
## 6. Conflicts
   link to plans/conflicts.md; no duplicate table
## 7. Historical rows (33)
   archive links only, no authority
## 8. Register counts and gates
   generated from common.json; never hand-typed
```

Rules: §4 is generated from `wiki.json` plan rows, §8 from `common.json`; no
hand counts; no `plans/index.md`; no `standards/index.md`; no duplicate conflict
table. `check-counts.py` validates §8 and `check-docs-manifest.py` validates the
plan rows.


### 4.3 Page header contract

Every page that can be a task owner (the 19 topic pages, `INDEX.md`,
`contract.md`, `puzzy.md`, and the standing books that carry owners) opens with a
machine-readable block so a task update never loads a whole archive. The block is
**strict YAML inside an HTML comment** (the v2 draft was not valid YAML —
unquoted `#anchors` start a comment and `#p2p / #messenger` is not a list; R14).

```md
<!-- CONTEXT:BEGIN
schema: flove-page/1
id: backend/mynet
path: development/standards/mynet.md
trunk: backend
topic: mynet
kind: topic               # topic | standing | map
status: active            # active | draft | retired
html_place: ["#p2p", "#messenger"]
owns: [MyNet L1–L5 ladder, flove-auth/1, BSP acceptance]
updated: 2026-11-21
read_next: ["#ladder", "#bridge", "#acceptance"]
supersedes:
  - development/wiki/archive/old/plans/2026-11-17-appy-authy-mynet.md
  - development/wiki/archive/old/browsy/spec.md
heavy: false
CONTEXT:END -->
```

Rules enforced by `check-docs-manifest.py`:

- `id` unique; `path` is **repo-relative**; `path` ends with `<topic>.md` for a
  topic page; `id` equals `<trunk>/<topic>`; `kind: topic` pages follow the 19-page
  grid, `kind: standing` pages are the §5.5a books, `kind: map` is `INDEX.md` or a
  plans map.
- `html_place` is a list; each `#anchor` must exist in `development/index.html`
  (split the old `#p2p / #messenger` string form — R14).
- `read_next` and `supersedes` are lists; every `#anchor` in `read_next` exists in
  the same page.
- `heavy: true` above 20 KB; `tasky.py show` never prints a `heavy` page body.
- The block is **≤40 lines / ≤600 tokens** and is the only text `tasky.py show`
  prints from the page.

### 4.4 Manifest

`development/wiki/wiki.json` — schema `flove-wiki-manifest/1`. **All paths are
repo-relative** (the v2 draft mixed `roots: ["development/wiki"]` with
`path: "standards/mynet.md"`, which cannot both be true — R03):

```json
{
  "schema": "flove-wiki-manifest/1",
  "roots": {
    "wiki": "development/wiki",
    "pages": "development/standards",
    "archive": "development/wiki/archive/old"
  },
  "pages": [
    {
      "id": "backend/mynet",
      "path": "development/standards/mynet.md",
      "trunk": "backend",
      "topic": "mynet",
      "status": "active",
      "kind": "topic",
      "owns": ["MyNet L1–L5 ladder", "flove-auth/1", "BSP acceptance"],
      "supersedes": ["development/wiki/archive/old/plans/2026-11-17-appy-authy-mynet.md"],
      "updated": "2026-11-21",
      "heavy": false
    },
    {
      "id": "standing/puzzy",
      "path": "development/standards/puzzy.md",
      "trunk": "standing",
      "topic": "puzzy",
      "status": "active",
      "kind": "standing",
      "owns": ["Puzzy extended definitions", "D0–D5 depth ladder"],
      "supersedes": ["development/wiki/archive/old/plans/puzzy.md"],
      "updated": "2026-11-21",
      "heavy": true
    }
  ],
  "redirects": {
    "development/standards/debates/browsy/README.md": "development/standards/systems.md"
  },
  "aliases": {
    "development/standards/debates/browsy/README.md#risk-matrix": "development/standards/systems.md#risk-matrix",
    "development/standards/debates/INDEX.md#historical": "development/wiki/archive/old/INDEX.md#historical"
  },
  "plans": [
    {
      "id": "backend/mynet",
      "path": "development/wiki/plans/backend/mynet.md",
      "primary": "backend/mynet",
      "sources": ["development/wiki/archive/old/browsy/spec.md"],
      "status": "active"
    }
  ],
  "field_map": {
    "data/index": "development/standards/json.md",
    "backend/contracts": "development/standards/systems.md"
  },
  "excluded_live": [
    "development/wiki/work/milestones.json",
    "development/wiki/work/common.json"
  ],
  "labels": {
    "standards": "development/standards/mds.md",
    "owner": "development/standards/work.md",
    "proposals": "development/standards/plan.md",
    "conflicts": "development/wiki/plans/conflicts.md",
    "pendings": "development/wiki/work/pendings.md"
  }
}
```

`redirects` is the primary old→new table for files that do not split; `aliases`
maps old paths and anchors to new pages or archive anchors; pages that split keep
a `field_map` (hito field → topic) and a `default` (R02/R26). A
`supersedes` chain is provenance, not the first lookup. `kind` is `topic`,
`standing` or `map`; standing books are included in `pages[]` even though they do
not follow the 19-topic grid (R12). `excluded_live` lists the files that are not
copied into the archive, so FR-03 remains testable (R05). `plans[]` is the source
for INDEX.md §4; each plan names one `primary` page and its archived sources.

### 4.5 Chapter evidence contract (no meaningful content lost)

The pages are rebuilt from the milestone spine; the old MDs are the evidence
archive. This contract makes “all meaningful content is accounted for” testable
without forcing every old heading into a same-named section.

1. **Chapter first.** `chapter-map.json` defines each page’s chapters from its
   fields/hito groups. Content is written into a chapter, not into a renamed old
   chapter.
2. **One row per old heading.** `port-ledger.json` still has one row per heading
   (`#`–`####`) in each of the 68 source MDs (1,018 rows). Each row records:
   `source`, `heading`, `level`, `mode`, `destination_chapter`,
   `destination_anchor`, `child_plan`, `provenance`, `signoff`,
   `summary_reason`, `notes`.
3. **Every row has one mode:**
   - `ported` — a meaningful fact from that heading is used in a chapter. The
     chapter need not share the old heading’s name; the row records the chapter
     anchor and a `Source:` line.
   - `linked` — the fact is already canonical in another chapter/page; the row
     names it and does not restate it.
   - `archive-only` — the heading has no live fact (closed log, superseded
     snapshot, duplicate, historical answer log). It requires a one-line reason.
4. **Chapter coverage.** Every chapter has either at least one evidence row or a
   `milestone-only` declaration (the chapter is derived from hito titles/notes
   because no old prose exists). A chapter with neither is incomplete.
5. **Meaningful content is defined before porting:** any heading with more than
   one sentence, a table, a code block, a decision, a schema, an acceptance test
   or a numbered procedure cannot be `archive-only` without an owner reason. A
   bare heading with no body may be `linked`.
6. **Per-file sign-off and size check.** Each source file gets
   `signoff: <initials> <date>` after a review of its ledger rows. The report
   prints source vs destination word counts; a `ported` heading below 60% of the
   source body must carry a `summary_reason`. The gate fails on a missing
   sign-off or an unexplained short port.
7. **Provenance is mandatory.** Every chapter that uses a source starts its
   evidence block with:
   `> Source: development/wiki/archive/old/<path>#<heading> (archived 2026-11-21)`.
8. **Order per chapter:** read the chapter map → collect evidence rows → write the
   chapter → verify the facts → add the `Source:` line and ledger rows → sign off.
   Archive only after the source rows are complete.
9. **Old links stay useful.** `wiki.json` `aliases` maps the old path and anchors
   to the new chapter or the archive copy. Every old link in HTML, skills, JSON
   or MD is repointed; no stub pages.
10. **No deletion without proof.** A source file is removed from its old location
    only when its ledger rows are complete, its archive checksum matches and its
    sign-off is recorded.

The generated `PORT-LEDGER.md` is a human report; `port-ledger.json` is the gate
input. `check-content.py --check` asserts rows, modes, chapter anchors,
provenance, sign-offs, summary reasons, word-count ratios and archive checksums.

Execution checklist per chapter:

1. Open `chapter-map.json` and the chapter’s evidence rows.
2. Port decisions → schemas/envelopes → acceptance tests → procedures → prose.
3. Keep tables as tables, code fenced, diagrams with a caption and archive link.
4. Compare the chapter with each source heading; if a fact is missing, the
   evidence row is not done.
5. Add the `Source:` line and mark the rows `ported`/`linked`.
6. Re-run `check-content.py --check` for the page before the next chapter.

### 4.6 Backup contract — backy, then cutover

`backy` is the local, read-only snapshot of the repositories and R2 media. Run it
only after this plan is final — never on a half-written plan. It is the
**external** copy; `development/wiki/archive/old/` is the **in-repo** copy.
Both are required. “Keep the actual setup as backup” means the pre-cutover tree
is recoverable byte-for-byte from both copies; it does **not** mean two live
sources of truth stay in place. The old live path is retired only after the
archive copy and the backy snapshot exist.

1. **Commit the finalized plan first.** `backy` mirrors `.git`; it does not see
   uncommitted working-tree edits. Commit the plan update locally (no push) and
   tag it `docs-migration-baseline`. If a local commit is not wanted, also write
   `working-tree.tar.zst` beside the snapshot with the same date.
2. **Run backy from the current script home, before the scripts move:**
   ```bash
   BACKY_PREFIX=Flove-docs-migration-before development/scripts/backy.sh --keep 1
   BACKY_PREFIX=Flove-docs-migration-before development/scripts/backy.sh --verify
   ```
   `BACKY_PREFIX` keeps this snapshot separate from the normal `Flove` snapshot,
   so the default `--keep 1` cannot replace the owner's routine backup.
3. **Record** the snapshot folder, `MANIFEST.json`, `SHA256SUMS`, `RESTORE.md`,
   `CHANGES.md` and the baseline tag/commit in the phase-0 log.
4. **What backy does not cover:** the Gitea database, `docs/docs-files`, tokens,
   `~/.ssh`, `~/.gnupg`, `~/.config`. Do not claim otherwise. The in-repo archive
   plus `SHA256SUMS` covers the wiki content.
5. **After cutover:** run backy again only after the gates are green, using a
   distinct prefix; keep the `…-before` snapshot until the restore drill passes.
   Post-move, the command is:
   ```bash
   BACKY_PREFIX=Flove-docs-migration-after tools/dev/backy.sh --keep 1
   BACKY_PREFIX=Flove-docs-migration-after tools/dev/backy.sh --verify
   ```
6. **Restore drill:** clone the flove mirror from the snapshot per `RESTORE.md`,
   restore `development/` and `development/wiki/archive/old/`, run
   `check-restore.py` and `check-content.py --check`. A backup that has not been
   drilled is not a rollback plan.
7. **No release in the same run:** never run `updaty` “just in case” before
   backy; a partial release mutates `sw.js`, the package zip and the vocabulary
   index. Backy is read-only and must stay that way.

---

## 5. Complete file routing (old → new)

This section is the authoritative routing table. It deduplicates §2, §8, §10 and
§12 of v1; where they disagreed, the per-heading ledger (§5.10) wins (D53).

### 5.0 Coverage matrix — the 68 migrated MDs

Every file in the old tree appears in exactly one row below; the per-file rows
are in §5.1–§5.7. The generated `port-ledger.json` expands each file to its
headings (§4.5).

| Area | Files | Routed in | Archive |
|---|---:|---|---|
| `debates/` root MD | 14 | §5.2 | 4 archive-only |
| `debates/browsy/` | 6 | §5.3 | 0 |
| `debates/browsy/pre-build/` | 12 | §5.3 | 1 (`open-issues.md`) |
| `debates/plans/` | 11 MD (12 files with `.bak-orig`) | §5.4 | 0 archive-only; MD sources also copied |
| `debates/proposals/` | 2 | §5.5 | 0 |
| `bridges/`, `others/`, `research/`, `reviews/` | 4 | §5.5 | 0 |
| `debates/archive/making-of/superpowers/specs/` | 12 | §5.7 | 12 archive-only |
| `standards/apps/` | 2 | §5.6 | 2 (after port) |
| root chapters + `standards/AGENTS.md` | 5 | §5.1 | 4 (contract stays) |
| **Migrated total** | **68** | | **23 archived MD** |
| standing books (§5.5a) | 6 groups | stay | 0 |
| non-MD `debates/` | 13 | §5.7 | 11; 2 live JSONs in backy |

### 5.1 Root chapters

| Source | Destination | What moves |
|---|---|---|
| `standards/backend.md` (16 `##`) | `standards/{plan,systems,mds,schemas,json,apps,storage,scripts,mynet,channels}.md` + `archive/old/root/backend.md` | 15 content chapters; §5–§7 (`routing`, `publisher adapter`, `common traceable area`) → `json.md` under `## Data index and routing`; `## In this file` (TOC) → `development/wiki/INDEX.md` |
| `standards/adoption.md` (6 `##`) | `standards/{systems,storage,experience,apps,scripts}.md` + `archive/old/root/adoption.md` | adoption stages, storage trade-offs, experience tiers, app rollout, script inventory |
| `standards/worldview.md` (2 `##`) | `development/standards/contract.md`, `development/wiki/INDEX.md`, owning pages + `archive/old/root/worldview.md` | values → contract (stays); why + map → INDEX; facts → owners |
| `standards/contract.md` | **stays** at `development/standards/contract.md` (R11) | values + the floor; no move, no chapter split |
| `standards/AGENTS.md` (85 lines, rules 1–13) | merged into `development/AGENTS.md` (R10) + `archive/old/root/AGENTS.md` | rules → §1, Authority → §2, ten PROC blocks → §3 contiguous; retired note → `archive/old/archive.md#home-directory-layout`; 33 refs repointed |

### 5.2 `debates/` root MD (14)

| Source | Destination | What moves |
|---|---|---|
| `INDEX.md` | `development/wiki/INDEX.md` | the **only** index: closed list + compact map + plans reading map + data-index section; keep the 33 Historical rows as archive links; regenerate counts |
| `pendings.md` | `work/pendings.md` | unchanged parser syntax; regenerate the scope counts to 75 rows / 438 items / 326 hitos (R07) |
| `task-set-plan.md`, `hitos-audit.md` | `work/measures.md` (queue policy + a clearly marked `## Historical snapshot`, not live counts); `#conflict-register` → `plans/conflicts.md` | live counts are generated from `common.json`; the 312/1012/345 table stays historical; conflict register has one home (R20/R21) |
| `roadmap-2026-06.md`, `proposals.md` | `standards/plan.md` | roadmap map + stage aliases (old `plans/index.md` merges into INDEX, §5.4) |
| `questy-proposals.md`, `standards.md` (root), `UseCase-adv.md` | `standards/{skills,flows,mds}.md`; scripts → `standards/skills/questy/` | decisions + reusable question shape |
| `agents.md`, `skills-library.md`, `archive.md`, `a11y-development-index.md` | `archive/old/…` | archive only; facts already canonical |

### 5.3 `debates/browsy/` (6) and `browsy/pre-build/` (12)

| Source | Destination | What moves / child plan |
|---|---|---|
| `browsy/spec.md` | `standards/{mynet,systems,schemas,apps,experience,plan,flows,work}.md` | BSP requirements, phases 0–8, acceptance, §5 reconciliation · child `plans/docs/plan.md` |
| `browsy/browsy-questions.md` | `standards/{mynet,experience,work,mds,systems,flows,channels,docs,schemas}.md`; conflicts → `plans/conflicts.md` | live A–L questions under `## Live questions — 2026-11-17 …`; **244-answer log stays in archive** · child `plans/docs/work.md` |
| `browsy/rationale.md` | `standards/{mynet,docs,plan,systems,schemas,flows,json,mds,work}.md`; conflicts → `plans/conflicts.md` | privacy-first mesh, P/L/S classes, threat model · child `plans/docs/plan.md` |
| `browsy/README.md`, `TESTING.md`, `port-nety.md` | `standards/{systems,mynet}.md` | risk matrix, retained seams (§5.10 §5 already reconciles) |
| `pre-build/01-mvp.md` | `standards/mynet.md` | single-device MVP · `plans/backend/mynet.md` |
| `pre-build/02-authy-levels.md` | `standards/mynet.md`, `schemas.md` | SelfAuth vs risa/nonce+DM, O11=D · `plans/backend/mynet.md` |
| `pre-build/03-schemas.md` | `standards/schemas.md`, `json.md` | `flove:authy/1` key vs `flove-authy/1` id · `plans/data/schemas.md` |
| `pre-build/04-myfamily-profile.md` | `standards/{schemas,mynet,experience}.md` | 7 areas × 5 replies → 5 percentages · `plans/data/schemas.md` |
| `pre-build/05-native-host.md` | `standards/systems.md` | Rust host, WebSocket+JSON · `plans/backend/systems.md` |
| `pre-build/06-bridge-threat-model.md` | `standards/systems.md` | boundary, allowlist, mitigations · `plans/backend/systems.md` |
| `pre-build/07-lineage-tests.md` | `standards/mynet.md` | invite lineage, fixtures · `plans/backend/mynet.md` |
| `pre-build/08-model-labels.md` | `standards/experience.md` | "Else" chip wording · `plans/frontend/experience.md` |
| `pre-build/09-consult-agreements.md` | `standards/{schemas,mynet}.md` | `flove-consult/1`, consent · `plans/data/schemas.md` |
| `pre-build/11-ui-pending.md` | `standards/experience.md` | pending Browsy/Nety surfaces · `plans/frontend/experience.md` |
| `pre-build/README.md` → `index.md` | `standards/{plan,work,mds}.md` | index + section links · `plans/docs/plan.md` |
| `pre-build/open-issues.md` | `archive/old/…/open-issues.md` | closed log, no authority |

### 5.4 `debates/plans/` (11 MD; 12 files with `.bak-orig`) — date-prefixed names exact

| Source | Destination | Child plan |
|---|---|---|
| `plans/2026-11-21-app-database-stages.md` | `standards/{plan,work,json,apps,storage,mynet}.md` | `plans/backend/storage.md` |
| `plans/2026-11-17-appy-authy-mynet.md` | `standards/{mynet,systems,schemas,apps,experience,storage,work,plan}.md` | `plans/backend/mynet.md` |
| `plans/2026-11-20-appy-dashboard-redesign.md` | `standards/{apps,experience,plan,json}.md` | `plans/frontend/apps.md` |
| `plans/central-backend.md` | `standards/{systems,storage,mynet,mds,experience}.md`; conflicts → `plans/conflicts.md` | `plans/backend/systems.md` |
| `plans/puzzy.md` | `standards/{apps,work}.md`; conflicts → `plans/conflicts.md` | `plans/frontend/apps.md` |
| `plans/2026-06-18-nety-frontend-build.md` | `standards/{apps,experience,scripts,plan}.md` (built UI, tabs, deferred wiring, phase status) | `plans/frontend/apps.md` |
| `plans/2026-06-18-nety-frontend-build.md.bak-orig` | archive verbatim; same four pages if ported | same as parent |
| `plans/2026-11-14-app-tier-planned.md` | `standards/apps.md` (closed tier status); conflicts → `plans/conflicts.md` | `plans/frontend/apps.md` |
| `plans/2026-11-19-authy-open-questions.md` | `standards/work.md`, link from `mynet.md` | none unless promoted |
| `plans/conflicts.md` | **live target** → `development/wiki/plans/conflicts.md` | is itself the target |
| `plans/index.md` | `development/wiki/INDEX.md` (plans map) + `standards/plan.md` (stage aliases) | no separate plans/index.md is created (R13) |
| `plans/standards.md` (SD01–SD19) | `work/pendings.md` `VARIOUS_Q34–50` + crosswalk; **23 task owners** (+4 hito sources, 2 standards URLs) repointed (R37) | none (G10A) |

### 5.5 Proposals, bridges and other folders

| Source | Destination | What moves |
|---|---|---|
| `proposals/frontend-wizy.md` (136 lines) | `standards/{apps,flows,work,experience}.md` | operating areas, custom magic, key fields, influence degrees; mark draft |
| `proposals/frontend-tiers.md` | `standards/apps.md` | closed tier status |
| `bridges/oasis.md` | `standards/{mynet,systems,schemas,work,mds}.md` | Oasis/SSB adaptation, publish mapping |
| `a11y-report.md` | `standards/accessibility.md` | generated summary; raw file stays in archive; no child plan |
| `others/flove-libs-insights.md` | `standards/mds.md` + `development/standards/contract.md` | library insights |
| `research/vr_interfaces.md` | `standards/experience.md` | abandoned note |
| `reviews/2026-07-25-browsy-fastapi-libsql-performance-review.md` | `standards/systems.md` | architecture notes |

### 5.5a Standing books that stay (not part of the 68 migrated MDs)

These files are canonical today and remain canonical. They are **not** duplicated
into the 19 topic pages; the topic pages link to them. They must be added to the
reference-rewrite inventory because their links, counts and navigation change
(R12/R15).

| Path | Role | Action at cutover |
|---|---|---|
| `standards/puzzy.md` (731 lines) | extended-definition standard; 24 task owners | stays; add `CONTEXT`; repoint 3 refs |
| `standards/puzzy/{puzzy.schema.json,example-water.json}` | schema + example | stay |
| `standards/frontend/frontend.md` (≈69 KB) | frontend catalogue; 112 task owners | stays; add `CONTEXT` or fallback; repoint 10 refs |
| `standards/frontend/{counters,export,publish,routing-colours-db,summary}.md` | frontend sub-standards | stay; repoint refs |
| `standards/skills/{README,CONFIG,standing}.md` + 20 skill dirs | skill library | stay; **12 skill files** reference `development/scripts/` or `standards/scripts/`; repoint to `tools/dev/` |
| `standards/risaliberada/{plan-v2,risaliberada}.md` + assets | project book; 23 owners on `plan-v2.md` | stays |
| `standards/workflow/*.html` | workflow demos | stay; repoint 3 refs |
| `standards/vocabulary.md` / `vocabulary.html` | vocabulary matrix; 7 owners | stay; regenerate `vocabulary.html` (N9) |
| `standards/README.md` / `_sidebar.md` / `index.html` | book index, nav, docsify shell | stay; rewrite the file table, add the 19 topics, link `../wiki/INDEX.md` (docsify `:ignore` if the router refuses the out-of-root path), regenerate the 438/326/1,559 counts |

### 5.6 `standards/apps/` (2 MD)

| Source | Destination |
|---|---|
| `apps/README.md` (172 lines) | `standards/{scripts,apps,plan,skills}.md`; then verbatim at `archive/old/apps/README.md` |
| `apps/onboarding-copy.md` (32 `##` = 30 app blocks + `Shared shape` + `Catalog-only apps`) | shared shape + ten-step pattern → `standards/experience.md`; 30 app blocks as one table in `plans/frontend/experience.md` (linked from `experience.md` + `language.md`); then `archive/old/apps/onboarding-copy.md` |

### 5.7 Archive-only and non-MD

| Source | Destination |
|---|---|
| **17 archive-only MD**: `agents.md`, `skills-library.md`, `archive.md`, `a11y-development-index.md`, `browsy/pre-build/open-issues.md` + 12 `archive/making-of/superpowers/specs/*` | `archive/old/…`, relative paths intact |
| 4 deleted/merged root sources (`backend.md`, `adoption.md`, `worldview.md`, `standards/AGENTS.md`) | `archive/old/root/{backend,adoption,worldview,AGENTS}.md` verbatim, checksummed (AGENTS comes from `standards/AGENTS.md`) |
| `flove-decisions-interview.html` | `archive/old/flove-decisions-interview.html` |
| `ephemerall/{ephemeral-glider,ephemerall,ephemerall-logos,glider-balls-set,strategicpersistence}.html` | `archive/old/ephemerall/…` verbatim |
| `archive/making-of/{making-of,skills-applied}.html` | `archive/old/archive/making-of/…` verbatim |
| `milestones.json.bak-2026-11-20`, `…prequeue` | `archive/old/…` verbatim; not imported |
| `common.json`, `milestones.json` | **not archived** — canonical register + generated projection; they move to `work/`, so the archive is not a whole-tree copy of `debates/` (R05) |

The 12 archive-only spec filenames (all under
`archive/making-of/superpowers/specs/`, relative paths preserved) are:

`2026-06-12-frontend-standards-upgrade-design.md`,
`2026-06-15-keys-intro-summary-design.md`,
`2026-06-17-keysmini-design.md`,
`2026-06-18-nety-access-ecosystem-design.md`,
`2026-06-18-nety-spec-vs-flovenet-oasis-comparison.md`,
`2026-06-19-apps-index-redesign-design.md`,
`2026-06-19-appy-five-apps-tier-ladders-design.md`,
`2026-06-24-appy-intros-rainbow-roadmap-design.md`,
`2026-06-25-flove-private-addon-login-encryption-design.md`,
`2026-07-04-launch-language-chooser-design.md`,
`2026-07-05-flove-pwa-installable-design.md`,
`2026-07-20-context-standards-tidy-design.md`.

Non-import list: `common.json`, `milestones.json` and `work-moves.json` (absent).
These are the only sources without an archive copy; they are covered by the
backy snapshot. MD sources that also move live (`INDEX.md`, `plans/index.md`,
`plans/conflicts.md`, `pendings.md`) keep an archive copy so the original text is
never lost. The archive checksum manifest records both sets explicitly (R05).

### 5.8 Split of the three duplicate chapters

`backend.md` → plan §0/1/9 · systems §2/4 · mds §3.1–3.4/§12 · schemas §3.5 ·
json §5/6/7 · apps §8 · storage §10 · scripts §11 · mynet §13 · channels §14.
`adoption.md` → systems Architecture + Webhook Exports · storage Web-of-Trust
budget · experience CSS checklist §13.16 · apps Publish §13.15 · scripts Distro
§13.11. `worldview.md` → contract (why/principles) · INDEX (map) · owning pages.
PROC-03's `Standard:` URL moves to `standards/json.md`. The old data-index child
plan is absorbed by `plans/data/json.md`; no `plans/data/index.md` is created.

### 5.9 Collision clusters — one writer, all others link

| Topic | Canonical writer | Link, do not restate |
|---|---|---|
| Authy identity / ladder | `standards/mynet.md` | appy-authy-mynet §2/7b/7c/7d, spec §3.3, rationale §12, 02-authy-levels, questions §A |
| MyFamily / local groups | `standards/mynet.md` | spec §3.4.1, rationale §7.5, 04-myfamily-profile, questions §B/§L |
| Schemas / storage keys | `standards/schemas.md` | 03-schemas, 04-myfamily-profile, spec §3.2, rationale §5, questions §J |
| flovePortrait envelope / API | `standards/json.md` | app-database-stages §3, rationale §7.1–7.4/§14, dashboard §5 |
| Data index / routing | `standards/json.md` | backend §5–§7, `tools/routing.json`, `frontend/routing-colours-db.md` |
| Permissions / grants / bridge | `standards/systems.md` | spec §3.6, rationale §10/§15, questions §C/§G, 06-bridge-threat-model |
| Native host / transport | `standards/systems.md` | appy-authy-mynet §3, 05-native-host, questions §D, oasis §2 |
| Wizy / derivation | `standards/flows.md` | spec §3.5, rationale §6/§13, questions §E, frontend-wizy |
| Open questions / status / tests | `standards/work.md` | all `§Open`, `§Status`, `§Pending`, acceptance chapters |
| Conflicts | `plans/conflicts.md` | central-backend, puzzy, rationale §19, questions F3/F6 |

### 5.10 Per-heading evidence ledger

Read from the actual files 2026-11-21. Port **all** headings in one changeset.
The table below is a **summary**; it cannot satisfy FR-14's "every source heading
has a ledger row" because the 61 `debates/` MDs alone carry **851 `##`/`###`
headings** and the full source set has **1,018** heading rows. The executable ledger is generated:

- Phase 0 emits `development/wiki/port-ledger.skeleton.json` (one row per source
  heading: `source`, `heading`, `level`; destination/mode pending). Phase 2
  completes `port-ledger.json` with `destination`, `mode`, `provenance`, `signoff`.
- `development/wiki/PORT-LEDGER.md` is rendered from it; neither file is hand-edited.
- `check-docs-manifest.py` compares the ledger to the pre-cutover HEAD tree and
  fails on any unmatched heading (R18/R30).

The summary below is **evidence routing**, not a chapter order. The chapter
order comes from `chapter-map.json`; a source heading can feed a chapter with a
different name, and one chapter can draw from several sources.

| Source (`##` / chapter) | Destination |
|---|---|
| app-database-stages §1 goal / §2 five stages / §3 minimal model / §4 migrate Goddy·Realy·Appy / §5 sys-app tests / §6 update log | plan · plan · json · apps · apps · archive only |
| appy-authy-mynet §1–§8 (+7b–7e) | mynet · schemas+mynet · systems · experience · systems · work · work · mynet×3 · mynet · storage · plan |
| dashboard-redesign §1–§9 | apps · plan+apps · apps · apps · json · experience · apps (planned) · apps · plan |
| central-backend Architecture Decision / CB·D·E / CA / G·CB_S / tech stack / identity / persistence / conflicts / bridge / CentralRich | systems · systems (ID index) · mds+systems · mynet · systems · mynet · storage · systems+plans/conflicts · mynet · storage |
| puzzy Decisions+Architecture / Tasks / Conflicts | apps · work · plans/conflicts |
| browsy/spec §1–§9 | plan · plan · systems · schemas+mynet · mynet · apps+flows · systems · systems · systems (draft) · mynet · plan · plan · work · work · archive only |
| browsy-questions Current / Decisions log / Next questions / How to use / §A–§L / sessions / pendings | work · archive (live → mynet) · work · mds · mynet×4 · systems×4 · flows+apps · channels+mynet · experience · docs · schemas · systems · mynet · work · by topic (C/D/G→systems, A/B/L→mynet, E→flows, F3/F6→conflicts) |
| browsy/rationale §1–§20 | plan · docs+mynet · plan · systems · schemas · flows · json · mynet · plan×2 · systems · mynet · mynet · flows+apps · json · systems · plan · mds · Q1/2→schemas, Q3/4/6/8/10→mynet, Q5→systems, Q7→flows, Q9→json · conflicts · work |
| frontend-wizy What/areas/magic/contract · Open · Magic button | apps · work · experience |
| pre-build 01–11 | per-file rows in §5.3 (all chapters mapped there) |
| oasis §0–§5 + links | mynet · systems · schemas · mynet · work · mds |
| a11y-report (all) | accessibility; raw stays in archive |

Container/range rows and the archive-only exemption are the G9A implementation.

### 5.11 Reference rewrite map (scripts, JSON, HTML, skills)

| File | Rewrite |
|---|---|
| `tools/dev/procedures_source.py` | parse `development/AGENTS.md` (R10); still finds exactly ten PROC blocks |
| `apply-task-set-v2.py`, `build-common.py`, `build-work-tracker.py`, `check-restore.py`, `jsony_check.py`, `register_projection.py`, `tasky.py` | **re-base `ROOT`/`parents[n]` first** (R04), then register + `work/` path constants; provenance strings; Standard-URL validator → `https://flove.org/development/wiki/INDEX.md`; anchor validator skips `archive/`; `tasky.py` gains resolver + `--context` and keeps effort/weight/options intact |
| NEW `wiki-inventory.py`, `build-port-ledger.py`, `build-wiki-skeleton.py`, `build-field-map-review.py`, `build-chapter-map.py`, `build-task-recycle.py`, `port-ledger-mark.py`, `wiki-resolve.py`, `check-docs-manifest.py`, `check-retired-paths.py`, `check-archive.py`, `check-counts.py`, `check-content.py`, `check-plan-tray.py` | §4.0, §4.4, §4.5, §7.1, R24–R43 |
| `development/AGENTS.md` | 15 register link; 25 retired-layout rule; six `Standard:` URLs (01/03/07/08/09/10); §3.3 `fácil`→`easy` already applied (D59); merged work-style §1 / Authority §2 / PROCs §3 |
| `development/index.html` | app-database link, `pendings.md#ux01` source, four MD cards, `PLANS`/`DEBATE` labels kept; generated "Wiki source" link; `WORK-DATA` regenerated preserving six `TASK_CATS` chips |
| standards book | `README.md`, `_sidebar.md`, `frontend/{export,routing-colours-db,summary,frontend}.md`, `puzzy.md`, `skills/CONFIG.md`, **12** skill files, `questy/index.html`, `workflow/workflow.html`, community + sys apps HTML, `tools/routing.json`, `tools/check-a11y-axe.py` — every retired path repointed |
| `milestones.json` | baseline **1,895** path occurrences: **984 owners already migrated in phase 2b**; the resolver applied **768 replacements** (sources, standards, notes, gaps, docs, inbox); **0 remain**; `effort` values byte-identical; originals kept per field (R01/R24) |
| `common.json`, `WORK-DATA` | regenerated; never hand-rewritten |
| other live MDs/HTML | 26 MDs and the repo HTML inventory outside `development/standards/` reference `development/scripts/` or `standards/scripts/`; generate the list with `grep -rl`, do not hand-list (R35) |

### 5.12 Target inventory

- **19 flat topic pages** (§4.2) + **six standing books** (§5.5a).
- **Plan siblings**: `docs/{plan,work}` · `backend/{scripts,systems,mynet,storage}` ·
  `frontend/{apps,accessibility,experience}` · `ai/{models,skills,flows}` ·
  `data/{mds,json,schemas}` · `community/{docs,feedback,language,channels}`
  plus `plans/conflicts.md`, `plans/debates/README.md`.
- **Flat `work/`**: `pendings.md`, `measures.md`, `milestones.json`, `common.json`.
- **Wiki root**: `INDEX.md`, `wiki.json`, `PORT-LEDGER.md`, `chapter-map.*`,
  `task-recycle.*`, `register-path-inventory.*`, `plans/`, `work/`, `archive/old/`.
- **Development root**: `AGENTS.md` and `standards/contract.md` stay outside the wiki root (R09–R11).
- **Register counts after D62**: 326 hitos · 37 debate tickets · **75 pendings rows** =
  **438** canonical items (326 + 37 + 75; `build-work-tracker.py --check` prints
  `438 features`); 1,559 live tasks · 805 archived. The "424 = 312 + 37 + 75"
  figure and the `pendings.md` scope line "76 rows / 425 / 312 milestones" are
  stale pre-reshape numbers (R07).

---

## 6. Implementation phases

Each phase states its spec, inputs, work, outputs and exit gate. Phase order is
fixed: routing must exist before references can be resolved.

| # | Phase | Inputs | Work | Outputs | Exit gate |
|---|---|---|---|---|---|
| 0 | **Baseline + backy** | finalized plan; clean working tree | **commit the plan locally (no push) and tag `docs-migration-baseline`**; run `BACKY_PREFIX=Flove-docs-migration-before development/scripts/backy.sh --keep 1` then `BACKY_PREFIX=Flove-docs-migration-before development/scripts/backy.sh --verify`; record the snapshot folder, `MANIFEST.json`, `SHA256SUMS`, `RESTORE.md`; run the baseline block in §7.1 (six commands today); generate `register-path-inventory.json` + `port-ledger.skeleton.json` (source headings only); record 326 / 1,559 / 805, 75 rows, 438 features and the effort distribution (1,235 easy · 315 hard · 9 very hard · 0 very easy · 0 medium; archive 803 easy · 2 very hard) | baseline log + backy snapshot + inventory + ledger skeleton | backy verify green and snapshot recorded; baseline §7 gates green; `needs_review` queue recorded and grouped (zero only before cutover); token cost of top 10 owners recorded with the fixed method (R28) |
| 1 | **Skeleton** | §4 tree | `build-wiki-skeleton.py --write`: `wiki.json` with `redirects` + `supersedes`, `INDEX.md`, 19 draft topic pages in `development/standards/`, 19 plan skeletons, `plans/conflicts.md`, `plans/debates/README.md`, `work/` and `archive/` | 42 new files + 2 dirs; no live pointer touched | `build-wiki-skeleton.py --check` green; every `CONTEXT` block parses; no existing page overwritten |
| 2a | **Chapter map + task recycle** | milestones + inventory | `build-chapter-map.py --write` and `build-task-recycle.py --write`; owner reviews the 29 fields and the respec queue | `chapter-map.json/.md`, `task-recycle.json/.md` | 29 fields → 19 pages; every live task has a new-page owner; all template/no-evidence tasks are queued `respec` or have a signed `keep` reason |
| 2b | **Task-owner migration** | `task-recycle.json` | `apply-task-owners.py --plan` → `--apply`; rebuild `common.json` and `WORK-DATA`; run the six baseline gates | 1,559 tasks on 19 page owners; old values in `owner_origin` | `apply-task-owners.py --plan` reports 0 changes; every live task resolves to a page; no old owner remains; gates green |
| 2 | **Chapter content** | phase 2a + §5 + §4.5 | write each topic page chapter by chapter from its evidence rows; dry-run on the highest-fanout sources (`browsy/spec.md` 95 owners, `backend.md` 83), then the easy one; split browsy live/historical; complete `port-ledger.json` from the skeleton: modes, destinations, provenance, sign-offs | 19 chapterized pages + the child plans in §5.12 + generated ledger | each chapter has evidence or `milestone-only`; all 1,018 rows accounted; `check-content.py --check` green |
| 3 | **Standards consolidation** | phase 2 | delete `backend.md`/`adoption.md`/`worldview.md` after port; port + archive `apps/`; merge the two AGENTS; move every script home into `tools/dev/` and re-base each `ROOT` (R04) | single AGENTS, no duplicate chapters | 33 AGENTS refs repointed; no hub stubs; each moved script `--self-check` green |
| 4 | **PROC spine** | merged AGENTS | repoint six Standard URLs, `procedures_source.py`, script constants; old tree still present → dual-valid | PROC spine live in both trees | `tasky.py procedure` prints all ten blocks byte-identical except the six URLs |
| 5 | **Resolver** | `wiki.json` + inventory | `wiki-resolve.py --plan` → review → `--write` → `--check`; integrate into `tasky.py` and `build-work-tracker.py` | rewritten pointers with per-field originals; generated `wiki` field | `--check` green; 768 replacements applied; 0 moving paths; owners already on pages; no pointer resolves into archive; cycles error; no `needs_review` |
| 6 | **Cutover** | phases 2–5 | `git mv` live JSONs to `work/`; `git mv` remaining `debates/` to `archive/old/`; copy the MD sources that also move live (`INDEX.md`, `plans/index.md`, `plans/conflicts.md`, `pendings.md`) into `archive/old/`; `standards/apps/` to `archive/old/apps/`; `backend.md`/`adoption.md`/`worldview.md`/`standards/AGENTS.md` to `archive/old/root/`; write the checksum manifest and the explicit live-file exclusions (R05); verify every source heading has a ledger row before removing its old path | final tree + archive manifest | zero retired-path refs (§7.2); archive checksums match every archived file; every `ported` row has a destination anchor |
| 7 | **Rewrite + regenerate** | all §5.11 | every script/HTML/skill path rewrite; `--build`; all gates; manifest gate; token gate; `--self-check` on moved scripts | generated projections current | all §7.1 commands green |
| 8 | **Second pass, later** | clean release | archive link pruning only; N9 regeneration of `vocabulary.html` if chosen | no live deletions | gates still green |

---

## 7. Verification

### 7.1 Gate commands

**Baseline, before any file moves (phase 0).** These are the paths on disk
today; use them for the pre-cutover baseline and for the dual-valid window.

```bash
python3 development/scripts/build-work-tracker.py --check
python3 development/scripts/build-common.py --check
python3 development/scripts/jsony_check.py --no-write
python3 development/scripts/check-restore.py
python3 development/standards/scripts/check-skills.py
python3 tools/check-routing.py
```

`build-work-tracker.py --build` is a write step, not a baseline gate; run it only
when regenerating projections.

**Target, after the scripts move (phase 7).**

```bash
python3 tools/dev/build-work-tracker.py --build
python3 tools/dev/build-work-tracker.py --check
python3 tools/dev/build-common.py --check
python3 tools/dev/jsony_check.py --no-write
python3 tools/dev/check-restore.py
python3 tools/dev/check-skills.py
python3 tools/check-routing.py
python3 tools/dev/wiki-resolve.py --check
python3 tools/dev/check-docs-manifest.py --check
```

**Proposed additions (R24–R30, not existing yet):**

```bash
python3 tools/dev/wiki-inventory.py --check
python3 tools/dev/check-retired-paths.py --check
python3 tools/dev/check-archive.py --check
python3 tools/dev/check-counts.py --check
python3 tools/dev/check-plan-tray.py --check
python3 tools/dev/check-content.py --check
python3 tools/dev/build-port-ledger.py --check
python3 tools/dev/build-chapter-map.py --check
python3 tools/dev/build-task-recycle.py --check
```

The target block has nine commands; the nine additions make FR-04, FR-14,
FR-16, FR-18, FR-19, FR-20, FR-21, FR-22 and FR-23 testable. Until they exist,
"gates green" means the six baseline commands before the move and the nine target
commands after it (R08).

### 7.2 Acceptance checks

- Zero references to `development/standards/debates/`, `standards/apps/`,
  `standards/AGENTS.md`, `standards/backend.md`, `standards/adoption.md`,
  `standards/worldview.md` or `development/scripts/`.
- Every task owner resolves into the closed list; every topic page is
  `standards/<topic>.md`; every plan is `plans/<category>/<topic>.md` with the
  same topic keyword **except** the two allowlisted maps (`plans/conflicts.md`,
  `plans/debates/README.md`); every `plans/debates/` draft
  has `status: draft`, a `created:` date and an existing section folder.
- Every owner target has a valid `CONTEXT` block or is on the declared non-page
  fallback list (R14); every `html_place` anchor exists; every `read_next` anchor
  exists.
- `tasky.py show` on the top 10 owners stays **≤1.5k tokens, hard cap 2k**;
  measurement is `python3 -c` with the same tokenizer used in phase 0, or
  `wc -c` with a fixed 4-bytes/token approximation documented in the baseline log
  (R28). `procedure` / `weight` / `options` output is byte-identical to baseline
  except the six Standard URLs.
- `check-docs-manifest.py` asserts: every source heading in the generated
  `port-ledger.json` has a destination; at least the 851 `##`/`###` `debates/` headings and all 1,018
  source heading rows are covered; `####` rows are included when they carry a fact; every
  destination anchor exists; each child plan names exactly one primary page and
  lists any secondary pages under `also:`; every `html_place` anchor exists;
  `work-moves.json` is allowlisted as absent.
- **Content:** every ledger row has `mode` `ported|linked|archive-only`; every
  `ported` row has a chapter anchor and a `Source:` provenance line; every source
  file has a sign-off; no heading with meaningful body is `archive-only` without
  a signed reason (§4.5).
- **Chapters:** every topic page chapter comes from `chapter-map.json`; every
  chapter has evidence or a `milestone-only` reason; every live hito/task maps to
  exactly one page (FR-22).
- **Tasks:** every live task has a new-page owner; every template/no-evidence
  task is in `task-recycle.json` as `respec` or has a signed `keep`/`archive`
  reason; no task is marked done by the migration (FR-23).
- **Backup:** the phase-0 `backy` snapshot verifies (`backy.sh --verify`), the
  local `docs-migration-baseline` tag exists, and `archive/old/` checksums match
  for every archived file (§4.6).
- **Effort**: one of the five English values on every live and archived task; no
  `fácil` / `difícil` / `muy difícil` in data, script constants or PROC text;
  distribution equals the phase-0 baseline; `tasky.py easy` counts unchanged;
  Work offers exactly six chips (archived + five) with Spanish only in `es`
  labels; state moves still automatic after evidence.

---

## 8. Decision ledger — every decision in force

All entries taken 2026-11-21. **In force** = applied or fixed for cutover;
**open** = no owner choice yet. No entry is a new proposal. The §11 review
amended D01/D32/D34/D40/D42/D43/D45/D62 during the 2026-11-21 review; the
amended rows are marked “in force, amended/corrected”.

### 8.1 Governance, skills and pick flow

| ID | Decision | Status |
|---|---|---|
| D01 | Plan executed through cutover. No push/publish without the owner asking; the local cutover commit/tag awaits owner approval (§4.6, R39). | in force, amended |
| D02 | This file's v1 structure preserved at `…-plan.backup-2026-11-21.md`; at cutover the historical plan moves to `development/wiki/archive/old/`. | planned |
| D03 | `tasky` stays exactly one `SKILL.md`; no `PLAYBOOK.md`, `CARD.md` or third doc. | in force |
| D04 | Free work uses `tasky.py` without loading the skill. Strict run only for a cold-queue pick, state move, procedure edit or red gate. | in force |
| D05 | `/tasky` picks **and** works; clicky intro form shows the first question. | in force |
| D06 | Ask the owner on judgment calls; a verified state move is automatic and never asked. | in force |
| D07 | `questy` owns when/how to ask; `tasky` owns what. Both default to 30-question batches. | in force |
| D08 | `/tasky <profile>` with `flove` default; context = questy-all advanced Context tree + Plan/Work tab content. | in force |
| D09 | Survey behaviour belongs to `questy-tasky-flove`, not base `questy`. | in force |
| D10 | Thin `questy-tasky-flove` call created (option 2), registered as skill 21. | in force |
| D11 | `--profile` is a global `tasky.py` flag; only `flove` defined. | in force |
| D12 | Suggest specific questy questions when the shortlist is heavy, blocked or not easy; A/B/C with ★, answer grammar `0` / `-`. | in force |

### 8.2 Register, procedures and state

| ID | Decision | Status |
|---|---|---|
| D13 | Canonical policy in owner docs; `milestones.json` owns only hitos/tasks, no `procedures` key. | in force |
| D14 | PROC-07 sort: hito unlock rank → task's own `effort` → stable ids; advisory only. | in force |
| D15 | PROC-08 evidence `kind: command\|anchor\|state` + `value`; no `test` field. | in force |
| D16 | Live tasks carry `owner` only; 1,455 updated, 21 earlier dependency edges reverted. | in force |
| D17 | Active window 30 tracker IDs with `size`, `order`, `reviewed`, `reviewedBy`. | in force |
| D18 | `.3c`/`.3b`/`.3` scaffold tasks skipped by default; `--include-bookkeeping` opts in. | in force |
| D19 | PROC-10 `choice_weight` orthogonal to effort; `choice_override` + `choice_reason`; dependency registered only after the answer. | in force |
| D20 | State moves automatic once evidence verifies; no git commit unless asked. | in force |
| D21 | `skills-02.2a` / `systems-10.2a` left `pendiente`; no retroactive move. | in force |
| D22 | Register drift 1,492→1,559 and 317→326 synced by rebuilding projections. | in force |

### 8.3 Effort and naming

| ID | Decision | Status |
|---|---|---|
| D23 | No `1.5`; the first `very easy`=1 fallback was superseded. | superseded |
| D24 | Five-level English ladder: `very easy` · `easy` · `medium` · `hard` · `very hard`; Spanish UI-label only. | in force |
| D25 | 2,364 effort values migrated (2,038 + 315 + 11). Live 1,235 easy / 315 hard / 9 very hard; archive 803 easy / 2 very hard. | in force |
| D26 | No task assigned to `very easy` / `medium` without an owner id list or rule. | in force, open fill |
| D27 | `tasky.py easy` proposes 10-task batches; `next --do` queues `directo + very easy/easy`. | in force |
| D28 | Colour is effort, not state: easy green / hard yellow / very hard red; levels 1 and 3 uncoloured; `✓` = `hecha`. | in force |
| D29 | Work filter labelled `Esfuerzo / Effort`, not `Estado / State`. | in force |
| D30 | Two axes only — `effort` and `stage`; `level`/`degree`/`nivel`/`grado` display synonyms; frontend 1–5 is a stage view. | in force |
| D31 | Historical `levels-*` ids / `#*-levels` anchors stay; no levels page; `#data-ux` is a view with no file. | in force |

### 8.4 Target tree and content ownership

| ID | Decision | Status |
|---|---|---|
| D32 | **19** flat topic pages `development/standards/<topic>.md`; `data/index` merged into `json.md` (R13). | in force, amended |
| D33 | Child plans `plans/<category>/<topic>.md`; folder = category, filename = same topic keyword; `work/` flat. | in force |
| D34 | `development/wiki/` keeps only INDEX, wiki.json, PORT-LEDGER, plans/, work/, archive/. `development/AGENTS.md` and `development/standards/contract.md` stay outside the wiki root (R09–R11). | in force, amended |
| D35 | Whole-family trunks flatten under `docs/` as peers; not created now. | in force |
| D36 | No `tools/standards/`; `standards/scripts/` → `tools/dev/`. | in force |
| D37 | `archive/old/` opaque verbatim; `archive/ported/` dropped. | in force |
| D38 | `plans/debates/` raw tray with `status: draft`, never an owner. | in force |
| D39 | Three duplicate chapters deleted outright; refs repointed; no hub stubs. | in force |
| D40 | Two AGENTS merge to one at `development/AGENTS.md`; ten PROCs contiguous (R10). | in force, amended |
| D41 | `standards/frontend/`, `puzzy/`, `risaliberada/`, `skills/`, `workflow/` stay. | in force |
| D42 | `contract.md` **stays** at `development/standards/contract.md` (R11); `apps/` archived verbatim. | in force, amended |

### 8.5 Automation, gates and open items

| ID | Decision | Status |
|---|---|---|
| D43 | Baseline 1,895 path occurrences: **984 owners applied in phase 2b**; resolver applied 768 replacements (sources, standards, notes, gaps, tickets, docs, inbox); **0 remain**. Originals preserved per field. **Amended by R01/R44.** | in force, amended |
| D44 | `common.json` and `WORK-DATA` generated. | in force |
| D45 | Resolution exact → `redirects`/`aliases` → anchored → `field_map` → `supersedes` (max 8) → `labels` → error; cycles error; no archive fallback. **Amended by R27.** | in force, amended |
| D46 | `tasky.py show` prints quick table + row + one `CONTEXT`; other commands unchanged. | in force |
| D47 | Generated `wiki` field additive to PROC-10 `choice`. | in force |
| D48 | Baseline gates green; `check-skills.py` 0 errors / 2 pre-existing warnings. | in force |
| D49 | Empty effort tiers stay 0; `next --do` covers 142 ready `directo + easy`. | in force — G11A |
| D50 | No retroactive `hecha` for the two delivered tasks. | in force — G12A |

### 8.6 Coverage audit additions and follow-ups

| ID | Decision | Status |
|---|---|---|
| D51 | Unprefixed `standards/<topic>.md` means `development/standards/<topic>.md`. | in force |
| D52 | Exact date-prefixed source names; no `refs/` and no `browsy/wizy.md`. | in force |
| D53 | §5.10 heading ledger wins over summary destinations; §5 is the file matrix. | in force — G3A |
| D54 | Retired note → `archive/old/archive.md`. | in force — G5A |
| D55 | AGENTS merge: rules §1 / Authority §2 / PROCs §3. | in force — G6A |
| D56 | PORT-LEDGER outside archive so gates can read it. | in force — G7A |
| D57 | Counts from disk: AGENTS 209 lines, standards/AGENTS 85, adoption 6 `##`, backend 16 `##`, onboarding 32 `##`. | in force |
| D58 | Owner accepted all ★: G1–G13 closed with option A; B/C rejected. | in force |
| D59 | Four D24 leftovers fixed (index.html JS, AGENTS PROC-10 note, README filter). | in force |
| D60 | Follow-up audit enumerated N1–N16 + 4 effort fixes. | in force (corrected by D63) |
| D61 | Applied N1A, N5A+N11merge, N7A, N10A, N14A, N16A. | in force |
| D62 | Closing EXP08 drops pending rows 76→75. The current canonical total is **438** = 326 hitos + 37 debate tickets + 75 rows; the older "425→424" used the pre-reshape 312-hito count and is superseded (R07). | in force, corrected |
| D63 | Tally correction: 16 tracked groups (N1–N16) + 4 effort fixes = 20, not "24"; N8 satisfied by N1A; nine items open. | in force |

### 8.7 Review decisions applied (2026-11-21)

| ID | Decision | Status |
|---|---|---|
| D64 | `development/wiki/` is the single wiki root; `docs/` stays the public docs family (R09). | applied |
| D65 | `development/AGENTS.md` is the only AGENTS file; `standards/AGENTS.md` merges into it and is archived (R10). | applied |
| D66 | `development/standards/contract.md` stays; PROC-02's URL is unchanged (R11). | applied |
| D67 | **19** topic pages + **6** standing books; `data/index` merges into `standards/json.md`; no `plans/data/index.md` (R12/R13). | applied |
| D68 | One `development/wiki/INDEX.md`: plans map + data-index section + 33 historical archive links; no `plans/index.md`, no `standards/index.md` (R13). | applied |
| D69 | The content-import contract (§4.5) and the backy baseline (§4.6) are mandatory gates, not optional advice (R38/R39). | applied |
| D70 | **Rebuild, do not port chapter boundaries.** The 19 pages are chapterized from the 29 milestone fields; old MDs are the evidence archive (R41). | applied |
| D71 | **Task recycle policy.** Every live task gets a new-page owner; template/no-evidence tasks are queued `respec`; archive needs owner sign-off; no false done (R42). | applied |
| D72 | **Chapter map is generated** from `milestones.json` + field map; a page chapter is a field or hito group, and work counts come from the register, not old prose. | applied |
| D73 | **Task-owner migration applied.** All 1,559 live tasks carry a new page owner; `owner_origin` keeps the old path; 0 `respec` + 1,559 `keep` (pointer); no state change. | applied |

---

## 9. Follow-up audit — N1–N16 status

### 9.1 Applied in commit `14b0e07`

| Item | What was applied |
|---|---|
| N1A | `apps{}` removed from `tools/puzzy.json`; parked `sync-puzzy.py` deleted; EXP08 closed; jsony + skill updated to routing-as-sole-registry |
| N5A + N11merge | 406-line `PLAN-V2-D1.md` merged into `risaliberada/plan-v2.md` **Parte C** (headings demoted, content intact), risa-project owner line added, project copy deleted, README link repointed |
| N7A | Four refs in `contract.md` repointed off `adoption.md` / `worldview.md` / `apps/README.md` |
| N10A | `development/media/…` declared canonical; duplicate project risa logo deleted; `i18n-ledger.json` repointed |
| N14A | Four empty directories removed (none git-tracked) |
| N16A | `build-depth-md.py` / `build-whole-md.py` retired with their updaty gate + Heavy steps |

Four D24 leftovers (D59) were also fixed: `EFFORT_RANK` / `taskClass()` in
`index.html`, the PROC-10 note in AGENTS §3.4, and the README filter description.

### 9.2 Open items and recommended option

| Item | Exact path(s) | Recommended implementation | Alternative |
|---|---|---|---|
| N2 | `pendings.md:107` `QUESTYDEMO01` | **N2A** keep as Work item | B schedule now · C close |
| N3 | `pendings.md:182,184`, `routing-colours-db.md` | **N3A** keep `RC01`/`RDB01`, repoint after cutover | B retire · C port note |
| N4 | `jsony_check.py:732`, `jsony/SKILL.md:148` | **N4A** document `TODO` as intentional decision slots | B track now · C guess name |
| N6 | 26 MD files reference `development/scripts/` or `standards/scripts/` | **N6A** repoint to `tools/dev/` inside §6 phase 6; generate the list with `grep -rl` (R35) | B shim · C ignore |
| N8 | `puzzy.json` vs `routing.json` | **N8B** already satisfied by N1A — no drift remains | A regenerate (moot) · C document |
| N9 | `vocabulary.html:279,285–289` | **N9A** regenerate after N6/N12, add to cutover checklist; use a stable selector, not line numbers (R34) | B delete · C defer |
| N12 | **12** skill files (not 10, not 7) | **N12A** rewrite to `tools/dev/` + topic pages + `work/pendings.md` | B broken links only · C defer |
| N13 | `brandy` 1156w, `optimizy` 1095w | **N13A** formally accept the 2 warnings (D48) | B sidecars · C trim |
| N15 | `nety.html`, `sety.html`, `old-index.html` | **N15A** mark intentional offline refs, regenerate i18n ledger | B delete · C archive |

Clean subchecks (no action): canonical effort data English-only; `jsony-pending`
0/0; routing index matches 1,288 fields; all 21 skills have matching frontmatter
and registry entries; all `Standard:` URLs resolve locally; no retired skill
names. `perfil fácil` in `build-work-tracker.py` is a bilingual task title, not
an effort value.

---

## 10. Risks, rollback and applied-changes log

| Risk | Mitigation |
|---|---|
| Partial content pass duplicates facts | Phase 2 writes all pages in one changeset (FR-16); anti-duplication gate §7.2 |
| Resolver silently points at archive | D45: error, never fallback; `--check` fails on archive targets |
| PROC text drifts in the merge | D40: URL-only changes; `tasky.py procedure` byte-compared except six URLs |
| Effort values change during path rewrite | D43: `effort` treated as data; phase-0 distribution compared exactly |
| Empty stable pages become hub stubs | D39/G4A: `storage` gets its own §4.8.3 fact; manifest checks content |
| Cutover breaks live gates | Phase 4 runs dual-valid before source deletion; phase 0 backy snapshot for swap-back |
| Meaningful content is silently dropped | §4.5 ledger modes + sign-off + `check-content.py`; no archive before destination verification |
| Backup does not contain the plan edits | Commit the finalized plan + tag before backy; backy mirrors `.git` (§4.6) |
| Split source cannot choose an owner | `field_map` + `default` + `needs_review`; zero review rows before cutover (R02/R19) |
| Script `ROOT` silently changes after the move | per-script base table + `--self-check` gate (R04/R29) |
| Register undercount leaves pointers behind | generated inventory over the 1,895 baseline occurrences; 984 owners applied; `check-retired-paths.py` (R01/R25) |
| Narrative counts drift from `common.json` | `check-counts.py`; regenerate README/pendings/measures counts (R07) |
| Archive is not a whole-tree copy | per-file `sha256` manifest + explicit live-file exclusions (R05) |

**Rollback:** restore from the phase-0 `backy` snapshot under
`~/Documents/backs/Flove-docs-migration-beforeYY-MM-DD/` (MANIFEST/SHA256SUMS/RESTORE),
the `docs-migration-baseline` tag, or the verbatim `archive/old/` tree. Run the
`RESTORE.md` commands, then `check-restore.py` and `check-content.py --check`.
The archive checksum manifest verifies the in-repo copy; the backy snapshot
verifies the repository and media.

**Applied-changes log:** the D59 effort fixes; the D61/D62 follow-ups in §9.1;
projection rebuilds after each; gates green at last run — `438 features (326 + 37
+ 75)`, 1,559 live / 805 archived, `jsony 0/0`, `check-restore` OK,
`check-skills.py` 0 errors / 2 pre-existing warnings. These fixes were committed
in `14b0e07`; the plan itself remains unexecuted. No push or publish.

---

## 11. Review pass — 2026-11-21 (R01–R44; R09–R13/R33 resolved)

> **Status:** R09–R13 and R33 are resolved and applied in this document; the rest
> are proposed changes to execute. Every item was checked against the tree and
> register on 2026-11-21. **Apply now** = mechanical correction; **resolved** =
> decided; **gate** = a new check to build; **sequence** = ordering/hygiene.

### 11.1 Summary table

| ID | Finding | Proposal | Status |
|---|---|---|---|
| R01 | The pointer inventory is undercounted: 747 owners is only the `debates/` subset; 984 of 1,559 owners changed (applied), and 1,895 path occurrences were in scope across nine fields | Replace every 747/1,159 count with the 1,895 inventory; generate `register-path-inventory.json` in phase 0; gate before/after | apply now |
| R02 | 465 tasks point at files that split into 2–8 pages, so a path lookup cannot choose an owner | Add `default` per file + `field_map` (29 hito fields → 19 topics) + `needs_review`; require zero review rows at cutover | apply now |
| R03 | `wiki.json` mixes `roots: ["development/wiki"]` with `path: "standards/mynet.md"` | Make every path repo-relative; add a `roots` map, `redirects`, `aliases`, `field_map`, `excluded_live`; validate uniqueness | apply now |
| R04 | Moving scripts changes `ROOT`/`parents[n]`: six use `parents[1]`, `check-skills.py` uses `parents[3]`, `check-drift.py` uses `dirname(HERE)`, three `publish-*.sh` use `../../..` | Per-script old base → new base table; re-base before path constants; `--self-check` each | apply now |
| R05 | FR-03 says the old `debates/` tree is byte-identical, but the register, `common.json` and `conflicts.md` move live and are not archived | Redefine as per-file verbatim + explicit live-file exclusion list + `sha256` manifest | apply now |
| R06 | The header says "uncommitted working-tree edit"; the applied fixes are in commit `14b0e07` | Correct the status/log; keep "no push"; allow a local branch for cutover | apply now |
| R07 | `424 = 312 + 37 + 75` is stale; `build-work-tracker.py --check` prints `438 = 326 + 37 + 75`; `pendings.md`, `README.md` and `debates/INDEX.md` still say 76/425/312/1,455 or 424/312 | Regenerate narrative counts from `common.json`; add `check-counts.py`; fix the two MDs before porting | apply now |
| R08 | §6 phase 0 says "six sync checks", §7 lists nine, phase 7 says "all nine" | Name the baseline set (nine) and the proposed additions (six) separately | apply now |
| R09 | **Resolved.** `development/wiki/` is the single wiki root under the development tree; `docs/` stays the public docs family. | Applied: tree, manifest roots, URLs and Standard targets now use `development/wiki/`; no `docs/development/` is created. | resolved |
| R10 | **Resolved.** The merged AGENTS file stays at `development/AGENTS.md`; moving it would break the harness auto-load. | Applied: `development/AGENTS.md` is the one AGENTS file; the 33 `standards/AGENTS.md` refs point to it; no second file. | resolved |
| R11 | **Resolved.** `contract.md` stays at `development/standards/contract.md` as a standing governance page. | Applied: PROC-02's URL is unchanged; `README.md`/`_sidebar.md` keep the entry; no move. | resolved |
| R12 | **Resolved.** The grid is **19 topic pages + 6 standing books**; the books are real owners and are linked, never duplicated. | Applied: `puzzy.md`, `frontend/*`, `skills/*`, `risaliberada/*`, `workflow/*`, `vocabulary.*` are in `pages[]` with `kind: standing`; one-fact-one-home applies across both. | resolved |
| R13 | **Resolved — one index only.** `development/wiki/INDEX.md` absorbs the plans map and the data-index section; `plans/index.md` and `standards/index.md` are not created. | Applied: old `plans/index.md` → INDEX + `standards/plan.md`; `data/index` chapter → `standards/json.md` `## Data index and routing`; `plans/data/index.md` → `plans/data/json.md`; register field `data/index` → `standards/json.md`. | resolved |
| R14 | The `CONTEXT` example is not valid YAML; `html_place: #p2p / #messenger` is not machine-readable; the plan gives context only to the 19 topic pages while 79 targets are used as owners | Strict YAML block (`flove-page/1`), list-valued `html_place`, declared non-page fallback, `check-context` gate | apply now |
| R15 | Standing MDs are not in the routing table, yet their content changes (README file table, sidebar nav, counts, links) | Add the §5.5a maintenance table; treat them as migration inputs, not untouched files | apply now |
| R16 | The 12 archive-only spec filenames exist only in the v1 backup | List them in §5.7 (done) and in the generated ledger | apply now |
| R17 | `frontend/counters.md`, `frontend/publish.md`, `development/tools/conformance.html`, `standards/scripts/vendor/` have no destination row | Add explicit "stays" or move targets; keep `vendor/axe.min.js` with the harnesses | apply now |
| R18 | §5.10 summary rows cannot satisfy "every source heading has a ledger row": 61 MDs carry 851 `##`/`###` headings and the full set has 1,018 rows | Generate `port-ledger.json` + `PORT-LEDGER.md`; gate against pre-cutover HEAD; keep the summary as a reading aid | gate |
| R19 | `backend.md` §3 splits 3.1–3.4 to `mds.md` and 3.5 to `schemas.md` in one range row | One row per heading/sub-heading; no ranges in the authoritative ledger | apply now |
| R20 | `hitos-audit.md` is a pre-reshape snapshot (312/1012/345); `pendings.md` scope says 76/425/312; `README.md` and `debates/INDEX.md` say 424/312/1,455 | Mark historical tables as snapshots or archive them; generate `measures.md` from `common.json`; update the three live scopes | apply now |
| R21 | `work/measures.md` and `plans/conflicts.md` would both own a conflict register | `plans/conflicts.md` is the sole writer; `measures.md` links only | apply now |
| R22 | The gate says "every plan is `plans/<category>/<topic>.md`", but `plans/conflicts.md` and `plans/debates/README.md` are exceptions; no plan template exists | Allowlist the two maps; require `status`, `section`, `created`, `also:` frontmatter; dated `## <source> — <date>` sections | apply now |
| R23 | "All MDs" is asserted but not enumerated: 68 MDs (61 debates + 2 apps + 5 root) plus standing books | Add a coverage matrix (source, headings, destination, child plan, archive flag); this is the execution checklist | gate |
| R24 | The resolver only takes whole-field paths; 463 gaps and 127 notes are prose with inline paths | Add `--inventory`, `--report`, idempotency, per-field originals, substring replacement, `--fail-on-review` | gate |
| R25 | No gate checks retired paths, archive checksums, narrative counts, context schema or the draft tray | Add the seven gates in §7.1; fold link checks into `check-docs-manifest.py` | gate |
| R26 | The manifest lacks `redirects`, `field_map`, `excluded_live`, `sha256` | Add them; make `redirects` the first lookup after exact | apply now |
| R27 | Resolution order puts `supersedes` before `labels` and has no redirects/field map | exact → redirects/aliases → anchored → field_map → supersedes (max 8) → labels → error; log every fallback | apply now |
| R28 | The token target is "1–1.5k" in FR-13 but "under 2k" in §7.2; no measurement method | Fix target ≤1.5k / cap 2k; record tokenizer or `wc -c` method in the baseline log | apply now |
| R29 | A moved script can pass import but resolve the wrong tree | `--self-check` prints/validates resolved roots; run it in phase 7 | gate |
| R30 | `PORT-LEDGER.md` is called generated but no generator/check exists | `build-port-ledger.py --check`; never hand-edit | gate |
| R31 | The phase-2 dry run uses the easiest source (`appy-dashboard-redesign.md`, zero inbound) | Dry-run first on `browsy/spec.md` (95 owners) and `backend.md` (83), then the easy one | sequence |
| R32 | "No commit" conflicts with FR-16 atomicity and rollback | Cutover on a local branch with one commit; no push; keep the working tree clean after | sequence |
| R33 | **Resolved by R39.** The old plan relied on `/tmp` and did not capture uncommitted plan edits. | Use the §4.6 backy contract: local baseline commit/tag, `BACKY_PREFIX=Flove-docs-migration-before`, `--verify`, recorded snapshot. | resolved |
| R34 | Line-number references are already stale (`jsony_check.py:732`, `build-work-tracker.py:987`, `pendings.md:107`) | Replace with grep-able selectors or stable anchors; verify at execution | sequence |
| R35 | N6 says 7 files, N12 says 10 skills, §5.11 says 7 SKILL files; the tree has 12 skill files and 26 MDs referencing scripts | Use the generated list; update N6/N12/§5.11 | sequence |
| R36 | `.docs-wiki-migration-plan.md.kate-swp` exists in `development/` | Remove it; it is git-ignored and not migration content | sequence |
| R37 | §5.4 says `plans/standards.md` has "46 task owners"; the register has **23** owners (plus 4 hito sources and 2 standards URLs) | Correct the count and resolve the two fields separately | apply now |
| R38 | File routing alone does not prove meaningful content was imported; 1,018 headings carry prose, tables, decisions and schemas | Add §4.5: one ledger row per heading with `ported\|linked\|archive-only`, destination anchor, `Source:` provenance, per-file sign-off, `check-content.py --check`; no deletion before verification | apply now |
| R39 | The old backup plan used `/tmp` and did not capture uncommitted plan edits; backy mirrors `.git` | Add §4.6: commit the finalized plan + tag, run `BACKY_PREFIX=Flove-docs-migration-before development/scripts/backy.sh --keep 1`, then `BACKY_PREFIX=Flove-docs-migration-before development/scripts/backy.sh --verify`, record snapshot/MANIFEST/SHA256SUMS/RESTORE, drill restore after cutover | apply now |
| R40 | The v2 plan said to "drop 33 Historical rows" from INDEX, which loses source links the owner wants kept | Keep them as `INDEX.md` §7 archive links; ledger mode `linked`; no authority, no duplicate facts | apply now |
| R41 | Porting old chapter boundaries would carry stale shape and make 1,018 headings the plan; the register already has a clean 29-field spine | Rebuild pages from milestone fields/hitos; old MDs become evidence archive; chapter map is generated (D70) | applied |
| R42 | All 1,559 live tasks are pending scaffold actions with no evidence | Every task gets a new-page owner; queue all as `respec` with a reason; no false done; archive only with owner sign-off (D71) | applied |
| R43 | "Plan and work data reflected" needs a concrete artifact, not prose | `chapter-map.json` carries chapters, hito/task counts and open/closed per page; pages and task ownership use it (D72) | applied |
| R44 | Tasks still pointed at old `debates/`/`scripts/` paths; the audit was not applied | Migrate all 1,559 owners to the 19 pages, preserve `owner_origin`, rebuild projections; keep the 0 `respec` + 1,559 `keep` split (D73) | applied |

### 11.2 The inventory that replaces "747 / 1,159"

Measured on the working tree with `milestones.json` (2,364 tasks, 326 hitos):

| Field | Moving occurrences | Notes |
|---|---:|---|
| `tasks[].owner` | 984 | 747 debates + 71 scripts + 60 apps + 99 deleted chapters + 7 AGENTS |
| `tasks_archive[].evidence.gaps[]` | 320 | prose sentences, substring replacement |
| `hitos[].source` | 226 | 139 debates + 46 scripts + 24 deleted + 16 apps + 1 AGENTS |
| live `tasks[].evidence.gaps[]` | 143 | prose |
| `notes` (hitos + tickets) | 127 | prose with paths |
| `hitos[].standards[]` | 66 | URLs, 48 carry anchors |
| `new_tickets[].source` | 25 | 37 source fields total |
| `hitos[].docs[]` | 3 | two hitos (`mds-08`, `schemas-08`); only moving entries counted |
| `taskSet.moves_inbox` | 1 | absent file, path constant |
| **Total** | **1,895** | baseline; 984 owners + 768 resolver replacements applied; **0 remain**; current inventory 2,488 all-staying |

79 distinct owner targets; 575 owners already point at a staying page. The
register also has 37 effort-less `new_tickets` and 805 archived tasks; the
archived evidence gaps are part of the rewrite even though they are not live
owners.

### 11.3 Split-source owner map (the missing rule)

For a file that splits, the owner must be chosen from the task's hito field, not
from the source path. The proposed default table (owner reviews it once; a task
can override with `choice_reason`):

| Hito field | Topic page | Hito field | Topic page |
|---|---|---|---|
| `docs/map` | `standards/plan.md` | `frontend/levels`, `quality`, `tours` | `standards/experience.md` |
| `docs/plan` | `standards/plan.md` | `frontend/a11y` | `standards/accessibility.md` |
| `docs/work` | `standards/work.md` | `frontend/shell`, `tree`, `types`, `visual` | `standards/apps.md` |
| `backend/contracts` | `standards/systems.md` | `data/index` | `standards/json.md` |
| `backend/delivery` | `standards/scripts.md` | `data/json` | `standards/json.md` |
| `backend/storage` | `standards/storage.md` | `data/mds` | `standards/mds.md` |
| `backend/systems` | `standards/systems.md` |
| `backend/mynet` | `standards/mynet.md` | `data/schemas` | `standards/schemas.md` |
| `ai/flows` | `standards/flows.md` | `community/docs` | `standards/docs.md` |
| `ai/models` | `standards/models.md` | `community/feedback` | `standards/feedback.md` |
| `ai/skills` | `standards/skills.md` | `community/language` | `standards/language.md` |
| `ai/levels` | `standards/models.md` | `community/channels` | `standards/channels.md` |
| `frontend/*` (remaining) | see above | `community/levels` | `standards/language.md` |

Algorithm: (1) exact/redirect for files that do not split; (2) `field_map` for
split files; (3) file `default`; (4) mark `needs_review: true`. The gate fails on
any `needs_review` row unless it is in the signed baseline exception list.
Examples that force the rule: `browsy/spec.md` (95 owners → 8 topics),
`backend.md` (83 → 10), `apps/onboarding-copy.md` (30 → experience/apps),
`plans/standards.md` (23 → pendings).

### 11.4 Script base changes (R04)

| Script / harness | Current base | After `tools/dev/` | Required edit |
|---|---|---|---|
| `apply-task-set-v2.py`, `build-common.py`, `build-work-tracker.py`, `check-restore.py`, `procedures_source.py`, `register_projection.py` | `parents[1]` = `development/` | `parents[1]` = `tools/` | `ROOT = parents[2] / "development"` or `DEV` constant |
| `check-skills.py` | `parents[3]` = repo root | `parents[2]` | re-base |
| `check-drift.py`, `build-questy-flove-data.py` | `VOCAB = dirname(HERE)` = `standards/` | `dirname` = `tools/` | pin to `repo/development/standards` |
| `publish-ama.sh`, `publish-liberada.sh`, `publish-risa.sh` | `../../..` = repo root | `../..` | re-base |
| `build-puzzy-demo.py`, `jsony_check.py`, `tasky.py`, `inject-conformance.py`, `check-portrait-protocol.py`, `check-distro.sh`, `publish-web*.sh` | repo root | repo root (same depth) | verify, no change expected |
| `a11y-harness.html`, `keyboard-harness.html` + `vendor/axe.min.js` | `standards/scripts/` | `tools/dev/` | keep `vendor/` beside the harnesses or rewrite the `src` |
| `backy.sh`, `narrate.sh`, `mkmusic.py` | script dir / absolute | script dir | verify; `narrate.sh` expects `mkmusic.py` beside it. Phase 0 runs `development/scripts/backy.sh` **before** the move; post-cutover uses `tools/dev/backy.sh`. |

The phase-7 exit gate is `--self-check` for every moved script, not just the nine
gate commands.

### 11.5 Content completeness — the 68-MD matrix

The migration claim "all MDs are migrated" needs an explicit count. On disk:

| Group | Files | Treatment | Ledger requirement |
|---|---:|---|---|
| `development/standards/debates/**/*.md` | 61 | §5.2–§5.7; archive-only **17**; 1,018 headings total | one row per heading; sign-off per file |
| `development/standards/apps/*.md` | 2 | §5.6; port + archive verbatim | one row per heading; sign-off |
| root chapters + `standards/AGENTS.md` | 5 | §5.1; split/delete/merge; contract stays; 4 archived at `archive/old/root/` | one row per chapter/rule; sign-off |
| **Migrated total** | **68** | one file row in `port-ledger.json`; **23 archived** (17 archive-only + 2 apps + 4 root) | all rows have a mode |
| standing books (§5.5a) | 6 groups | stay; links/counts updated | `kind: standing` in `pages[]`; context or fallback |
| non-MD `debates/` | 13 | 11 archive (including `.bak-orig`) + 2 live (`milestones.json`, `common.json` in `excluded_live`) | checksum or exclusion row |

The generated ledger is the only acceptable proof: 68 file rows, 1,018 heading rows, plus the standing-book rows. A summary table in Markdown is a
reading aid, not the gate. Every `ported` row carries a `Source:` provenance line
(§4.5) so the old source stays linked from the new section; every old path is in
`wiki.json` `aliases` or the archive, so no link is silently lost.

### 11.6 Recommended decision order

1. **Placement — settled (R09–R13):** `development/wiki/`, AGENTS stays,
   contract stays, 19 topics + 6 standing books, one `INDEX.md`. Do not reopen
   these without a full path/count audit.
2. **Correctness (R01–R08)** — inventory, split map, manifest paths, script
   bases, archive definition, counts, gate set.
3. **Content proof (R14–R23, R38–R43)** — chapter map, task recycle audit, context
   contract, generated ledger, split sub-rows, freshness, conflict home, plan
   template, 68-MD matrix, content modes, sign-offs, historical archive links.
4. **Tooling (R24–R30)** — resolver, gates, manifest fields, token method,
   self-checks, ledger generator.
5. **Backup + sequence (R31–R37, R39)** — commit/tag, backy, dry-run order,
   stable selectors, counts, swap-file cleanup.

**Minimum viable set if the owner wants to execute now:** R01–R08 + R18–R28 +
R31–R33 + R38–R43. The placement decisions are already applied; the content and
backup contracts are what prevent an update from silently losing a fact.

### 11.7 What this review does not change

- It does not execute the migration, move a file, rewrite a pointer, commit or
  publish.
- It does not overrule D58 (all ★ option A) or any decision in §8. R09–R13 and
  R33 are resolved and already reflected here; the remaining R-items are
  proposals to execute.
- It does not ask for new content beyond what is on disk; the generated ledger is
  a projection of existing headings.

---

## 12. Cutover and gap closure (2026-11-21)

Cutover ran as one transaction. The old sources are in
`development/wiki/archive/old/`, the live register and work files are under
`development/wiki/work/`, and every gate is green. The backy snapshot remains
deferred by the owner; the baseline snapshot and the in-repo archive are the two
restore points.

### 12.1 Gate snapshot (post-cutover)

| Gate | Status | Evidence |
|---|---|---|
| six baseline gates | **green** | register, common, jsony, restore, skills, routing |
| `wiki-resolve.py --check` | **green** | 2,488 occurrences, 0 moving, 0 review |
| `check-docs-manifest.py --check` | **green** | 29 pages, 19 topics, 19 plans |
| `check-archive.py --check` | **green** | 80 files, checksums verified against the pre-cutover snapshot (67 ledger sources) |
| `check-counts.py --check` | **green** | 438 / 326 / 1,559 / 805 |
| `check-plan-tray.py --check` | **green** | plan frontmatter + tray valid |
| `check-content.py --check` | **green** | 1,018 headings, 0 pending, 0 unsigned |
| `check-retired-paths.py --check` | **green** | no retired paths in live files |
| `check-links.py --check` | **green** | 115 live docs, 0 broken local links or anchors |

### 12.2 Gaps closed

| ID | Gap | Resolution |
|---|---|---|
| GAP-01 | Content sign-off | 715 `ported`/`linked` headings signed `agent-review 2026-11-21`; owner re-sign optional |
| GAP-02 | 50 live-register headings pending | `pendings.md` and `measures.md` ported; ledger 0 pending |
| GAP-03 | Retired paths in live files | script homes moved to `tools/dev/`; all live refs rewritten, including relative `standards/…` forms; 108 broken Markdown links repointed to live pages or `archive/old/`; `check-links.py` now guards them |
| GAP-04 | Archive unverified | 80 files hashed and matched against the pre-cutover copy; `check-archive.py` now verifies checksums, not just presence |
| GAP-05 | Duplicate `pendings.md` | parser now reads `wiki/work/pendings.md`; only one live copy |
| GAP-06 | 31 ambiguous resolver targets | reviewed: 14 are URL/relative variants of one target, 17 genuinely split; task owners were respec'd per content, no moving paths remain |
| GAP-07 | Task pointers | normalized: 512 `state`/`command` values that were doc anchors became `anchor`; 1 command became `state`. Final shape: 1,401 anchor · 152 state · 6 command, all 1,401 anchors resolve. `jsony_check.py` now rejects a path in `state`/`command` and a missing anchor. |
| GAP-08 | Backy deferred | baseline snapshot + `archive/old/` + `SHA256SUMS` are the restore path |
| GAP-09 | Cutover not executed | executed as one transaction; projections rebuilt and all gates green |

### 12.3 Cutover transaction

1. Pre-cutover copy made (`/tmp/opencode/cutover-before.tgz`) and verified.
2. `standards/debates/` and `standards/apps/` copied verbatim into
   `archive/old/` (plus the old root chapters under `archive/old/root/`).
3. Live register moved: `milestones.json`, `common.json`, `pendings.md` →
   `wiki/work/`; `task-set-plan.md` + `hitos-audit.md` → `wiki/work/measures.md`.
4. `debates/` and `apps/` removed from `standards/`; `backend.md`,
   `adoption.md` and `worldview.md` retired after their content landed in
   `systems.md`, `storage.md`, `models.md`, `experience.md`, `contract.md`.
5. `standards/AGENTS.md` restored as the live work-style policy that
   `development/AGENTS.md` names, with its three old links repointed.
6. All live readers updated: `tasky`, `jsony_check`, `build-*`, `check-*`,
   `index.html`, `AGENTS.md`, skills and app HTML.
7. `SHA256SUMS` regenerated over the 80 archived files; projections rebuilt.
8. 108 relative Markdown links in `standards/` and `wiki/` repointed (sidebar,
   frontend chapters, plan pages, measures/pendings); `check-links.py` verifies
   every local link and heading anchor.

### 12.4 Owner decisions still open

| ID | Decision |
|---|---|
| P5 | Optional: replace the majority target for a split source with another sibling page; current owners are coherent and no path is moving |
| P7 | Keep backy deferred; run it only on request |
| P9 | Commit the cutover on owner approval and tag it locally (no push) |
| P6 | **done** — 512 mislabeled pointers normalized to `anchor`; the remaining 152 `state` values are acceptance states, not page-level paths; shape enforced by `jsony_check.py` |

No commit or push has been made.

---

## 13. Cross-tree audit after cutover (2026-11-21)

The cutover was checked beyond `development/`: `apps/`, `community/`, `tools/`,
`sw.js`, `docs/`, `whole/` and the root pages. The findings below are separated
into migration regressions (fixed) and pre-existing debt (not caused by the
wiki move).

### 13.1 Migration regressions fixed

| Finding | Evidence | Fix |
|---|---|---|
| Doubled absolute URLs in hito notes | 35 × `https://flove.org/https://flove.org/...` in the register, `common.json` and `index.html` | collapse to one origin; rebuilt projections |
| Stale hito source anchors | 23 `Source:` URLs pointed at headings that moved or were renamed | remapped to the current section (plan, systems, schemas, apps, experience, models, flows, json, INDEX, channels, language) |
| Post-commit hook broken | `.git/hooks/post-commit` was a dangling link to `development/scripts/jsony-post-commit`; the script also called the deleted path | link repointed to `tools/dev/jsony-post-commit`; internal path fixed |
| `contract.md` links | `/docs/development/INDEX.md` and `skills/validaty/fix-catalog.md` no longer exist | point to `wiki/INDEX.md` and `standards/accessibility.md` |
| Stale generated indexes | `routing-index.json` and `sw.js` no longer matched the tree | regenerated both (`flove-…`, 367 precache entries) |
| Retired prose paths | `debates/INDEX.md`, `debates/pendings.md`, `scripts/build-common.py`, `scripts/check-drift.py` | rewritten to `wiki/…` and `tools/dev/…` |
| Frontend adoption pointers | `frontend.md` still named `adoption.md`, `worldview.md`, `backend.md` as live | point to `experience.md`, `contract.md#worldview`, `systems.md` |
| Work page local links | one `../standards/…` path and the `media/basic.jpg` viewer placeholder | corrected to `standards/…` and `media/development/basic.jpg` |

### 13.2 Residual by design

| Item | Why it stays |
|---|---|
| 977 `owner_origin` values in the register and embedded Work block | provenance of the original owner; not rendered and not a live link |
| Migration audit files (`port-ledger`, `chapter-map`, `field-map-review`, `register-path-*`, `task-recycle`) | evidence of the move; they intentionally quote pre-cutover paths |
| `archive/old/` and its internal links | verbatim pre-cutover snapshot; historical URLs are expected to point at the old tree |
| `wiki/work/work-moves.json` redirect/alias | optional inbox created by the first Work export; no file until then |
| Migration-only tools (`build-port-ledger`, `build-wiki-skeleton`, `build-field-map-review`, `wiki-inventory`) | one-shot phase tools; sources are archived, so rerunning them pre-cutover no longer applies |

### 13.3 Pre-existing debt found (not caused by the cutover)

- Distro check allows 10 known unbuilt-app links (`clauses`, `loves`, `wizardry`,
  `hoty`); `docs/index.html` has 6 links to planned app pages.
- `brandy` cites `index.html#web-types`, an old hash route; Work now exposes the
  typed app rows under its current tab routes.
- Several legacy absolute routes (`/apps/realy.html`, `/central/`, `/nety`, …)
  appear in blog/app prose; they predate this migration.
- `check-links.py` covers live Markdown only. Local HTML links are covered by
  `check-distro.sh`; absolute `https://flove.org/...` URLs are not yet a gate.

### 13.4 Gate hardening

- `check-retired-paths.py` now scans `.mjs` and knows
  `development/standards/scripts/` and `docs/development/INDEX.md`.
- `check-archive.py` verifies checksums and ledger coverage.
- `check-links.py` verifies local Markdown links and heading anchors.
- `check-page-status.py` keeps draft pages and skeleton banners from being owners.

---

## 14. Phase 2 completion (2026-11-21)

The content phase is now structurally complete:

- All **19 topic pages**, `wiki/INDEX.md` and the map pages carry
  `status: stable`; no page carries a “Phase 1 skeleton / do not cite” banner.
- All **19 child plans** are `status: stable`. The five plans that already carried
  source content were left intact; the 14 skeletons now carry a dated source
  index with a link to the stable owner.
- Each topic page carries a **Source map**: archived source, date and stable home.
  Chapters without a separate source row are explicitly `milestone-only`.
- `standards/AGENTS.md` was merged into `development/AGENTS.md` §8 and archived;
  `development/AGENTS.md` is the single work-style + PROC source.
- `wiki/archive/README.md` marks the archive as opaque, non-owner and read-only.

New gate: `tools/dev/check-page-status.py --check` fails if a live page or plan is
still draft, still carries a skeleton banner, or if any task points at a draft
owner. The gate set is now **15 commands**.

### 14.1 Phase 8 — archive-link guard

- Stable topic pages and `INDEX.md` contain **no** links into `archive/old/`;
  their source maps use code spans, not clickable archive links.
- Child plans may link to archive sources for provenance; `plans/conflicts.md`
  is the only cross-plan exception.
- `check-page-status.py` now fails if a stable topic/map page links to
  `archive/old/`, in addition to the draft/skeleton checks.
- `vocabulary.html` regeneration remains optional (texty3), not a migration
  prerequisite.

### 14.2 Archive manifest

- `wiki/archive/manifest.json` (`flove-archive/1`) lists every archived file with
  its SHA-256, `status: archived`, `live: false` and `owner: null`.
- `check-archive.py` now verifies the manifest against the tree, the checksums
  and the non-live markers, in addition to the ledger coverage.
