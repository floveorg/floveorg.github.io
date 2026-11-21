# Docs wiki migration — execution plan

> **Status: proposed, not executed.** Temporary planning file at `development/docs-wiki-migration-plan.md`.
> At cutover it moves to `docs/development/archive/old/` as historical record.
> Written 2026-11-21 from a read-only audit of 61 MD files, the Work JSON projection and the generators.
> Updated 2026-11-21 to carry the canonical-English five-level effort reclassification (§4.8).
> Content-migration audit finished 2026-11-21: §2 now states ownership only, §8 covers every live
> source's headings, and §12 remains the file-level inventory (gaps G1, G3, G4 and G9 closed).
> No commit or push is part of this plan.

## 0. Principles

1. **The 20 stable pages own the content.** Archived MDs are history only; every live fact is migrated into the flat `standards/<topic>.md` page whose Work domain owns it.
2. **One fact, one home.** A section page states a fact once; other pages link to it. `plans/` holds `index.md`, `conflicts.md` and topic-named child plans under owner folders; `plans/debates/` is a raw staging tray, not an owner.
3. **Copy/archive up, never cherry-pick out.** The old `debates/` tree is moved verbatim into `archive/old/` so its relative links still work and switching back is trivial.
4. **Register paths are load-bearing.** 747 task `owner` refs, 139 hito `source` refs and 55 `standards` URLs resolve today. They get rewritten by a generated resolver, never by hand.
5. **Generated stays generated.** `common.json` and the `WORK-DATA` block in `development/index.html` are rebuilt, not edited.
6. **Stable names in the wiki; dates only in frontmatter and in archive.**

## 1. Target tree

```
docs/
  index.html  paradigms.html
  papers/  tables/
  metaphysics/  psychosocial/  …/   whole-family trunks, flattened here (not created now)
  development/
    INDEX.md                     closed list + compact map; PROC Standard target
    AGENTS.md                    procedures (moved from development/AGENTS.md)
    contract.md                  values/floor (moved from standards/contract.md)

    plans/                       DYNAMIC — folder = category, file = topic keyword (sibling of the stable page)
      index.md                   thin reading map, no counts, no duplicate rows
      conflicts.md               living cross-plan tension tracker
      docs/{plan,work}.md
      backend/{scripts,systems,mynet,storage}.md
      frontend/{apps,accessibility,experience}.md
      ai/{models,skills,flows}.md
      data/{mds,index,json,schemas}.md
      community/{docs,feedback,language,channels}.md
      debates/                   RAW TRAY — drop on-the-fly plans here; promote later
        README.md                convention only, no facts, not an owner

    work/
      pendings.md                parser input; keep table syntax
      measures.md                live counts + queue policy + conflict register
      milestones.json            LIVE register — never archived
      common.json                generated projection
      work-moves.json            machine inbox (currently absent)

    wiki.json                    closed-list manifest + supersedes graph + compact context map

    archive/                     OPAQUE SNAPSHOT — no live links, excluded from wiki.json and gates
      old/                       verbatim old debates/ tree: 61 MDs + HTML + .bak + its own plans/
      old/apps/                  standards/apps/ moved verbatim here (sibling of debates inside old/)

tools/                          THE single scripts folder — all script homes collapse here
  (existing general scripts)  +  dev/  ← old development/scripts/* AND standards/scripts/*

development/                    STAYS — Work page + standards book only
  index.html                    Work page, regenerated; HTML places = tab anchors
  standards/
    README.md  _sidebar.md  vocabulary.*  index.html
    <topic>.md                  STABLE — flat, no trunk folder (20 pages)
      plan.md  work.md  scripts.md  systems.md  mynet.md  storage.md
      apps.md  accessibility.md  experience.md
      models.md  skills.md  flows.md
      mds.md  index.md  json.md  schemas.md
      docs.md  feedback.md  language.md  channels.md
    frontend/  puzzy/  risaliberada/  skills/  workflow/   stay
    AGENTS.md       MERGED into docs/development/AGENTS.md, removed
    contract.md     MOVED → docs/development/contract.md
    worldview.md    DUPLICATE → folded into INDEX.md/contract.md, removed (§10.3)
    backend.md      DUPLICATE → split into topic pages, removed (§10.3)
    adoption.md     DUPLICATE → split into topic pages, removed (§10.3)
    apps/           ported, removed (§10.4)
    debates/        emptied → archive/old/
    scripts/        moved to tools/dev/
```

Stable pages are flat: `development/standards/<topic>.md`, with no trunk folder and no compound slug. Child plans are `plans/<category>/<topic>.md` — the folder names the category, and the filename is **the same topic keyword** as the stable page it serves. `subsection` and `topic` are the same kind of keyword, so these are sibling pages across categories: `plans/backend/systems.md` sits beside `standards/systems.md`, not under a separate `<subsection>` level. `work/` files are flat too. Levels get no page: they are the core stages, already described in `contract.md`, `standards/frontend/frontend.md` §13.18 and `standards/mds.md` (data depth).

`debates/` is never a wiki peer. The only live `debates/` folder is `plans/debates/`, a raw staging tray for on-the-fly plans to be elaborated; retired debates land in `archive/old/`.

Each section page starts with a machine-readable block so a task update never loads a whole archive:

```md
<!-- CONTEXT:BEGIN -->
id: backend/mynet
trunk: backend
topic: mynet
status: active
owns: [MyNet L1–L5 ladder, flove-auth/1, BSP acceptance]
updated: 2026-11-21
read_next: [#ladder, #bridge, #acceptance]
supersedes: [archive/old/plans/2026-11-17-appy-authy-mynet.md, archive/old/browsy/spec.md]
<!-- CONTEXT:END -->
```

## 2. Content migration map — archive source → owning section page

This is the important part: **what is written where before the source is archived**.

| Archived source | Migrate live content into | What moves |
|---|---|---|
| `plans/2026-11-21-app-database-stages.md` | `standards/storage.md`, `standards/json.md`, `standards/apps.md`, `standards/mynet.md` | `seed→full` stage model, `flove-profile` model, Goddy/Realy/Appy migration, MyNet/Chatland hitos, T01–T08 |
| `plans/2026-11-17-appy-authy-mynet.md` | `standards/mynet.md`, `standards/systems.md`, `standards/schemas.md`, `standards/apps.md` | L1–L5 ladder, portable `flove-auth/1`, Browsy handoff, A0–A11 status split |
| `plans/2026-11-20-appy-dashboard-redesign.md` | `standards/apps.md`, `standards/experience.md` | Profily-as-reference dashboard, theme changes, rollout gate |
| `plans/central-backend.md` | `standards/systems.md`, `standards/storage.md`, `standards/mynet.md` | FastAPI/Turso/Railway decisions, API, identity, sync, Nety bridge; mark `implemented`, demote to optional mirror |
| `plans/puzzy.md` | `standards/apps.md` | mean+dispersion aggregation, hybrid offline compute |
| `browsy/spec.md` | `standards/mynet.md`, `standards/systems.md`, `standards/schemas.md`, `standards/apps.md`, `standards/experience.md` | BSP requirements, phases, acceptance tests, §5 old-plan reconciliation table |
| `browsy/browsy-questions.md` | `standards/mynet.md` (live A–L only), `standards/experience.md` (model labels) | live question register; **244-answer historical log stays in archive** |
| `browsy/rationale.md` | `standards/mynet.md`, `standards/docs.md` | privacy-first data mesh, P/L/S classes, threat model |
| `proposals/frontend-wizy.md` | `standards/apps.md`, `standards/flows.md` | operating areas, custom magic, key fields, influence degrees; mark draft |
| `browsy/pre-build/01-mvp.md` | `standards/mynet.md` | single-device MVP slice |
| `browsy/pre-build/02-authy-levels.md` | `standards/mynet.md` | SelfAuth vs risa/nonce+DM verified Telegram, O11=D |
| `browsy/pre-build/03-schemas.md` | `standards/schemas.md` | `flove:authy/1` key vs `flove-authy/1` schema id, migration rules |
| `browsy/pre-build/04-myfamily-profile.md` | `standards/schemas.md`, `standards/mynet.md` | 7 areas × 5 replies → 5 percentages, P-by-default |
| `browsy/pre-build/05-native-host.md` | `standards/systems.md` | Rust native messaging host, WebSocket+JSON |
| `browsy/pre-build/06-bridge-threat-model.md` | `standards/systems.md` | page/bridge boundary, API allowlist, mitigations |
| `browsy/pre-build/07-lineage-tests.md` | `standards/mynet.md` | invite-lineage metadata, fixtures |
| `browsy/pre-build/08-model-labels.md` | `standards/experience.md` | "Else" chip wording |
| `browsy/pre-build/09-consult-agreements.md` | `standards/mynet.md` | signed revocable consult agreements |
| `browsy/pre-build/11-ui-pending.md` | `standards/experience.md` | pending Browsy/Nety UI surfaces |
| `browsy/pre-build/README.md`, `open-issues.md` | README → section links; answers → their section above | closed log, no authority |
| `browsy/README.md`, `TESTING.md`, `port-nety.md` | `standards/systems.md`, `standards/mynet.md` | risk matrix, retained seams; §5 already reconciles the rest |
| `bridges/oasis.md` | `standards/mynet.md`, `standards/systems.md` | Oasis/SSB adaptation and publish mapping |
| `a11y-report.md` | `standards/accessibility.md` | current generated summary; raw file stays in archive |

### Remaining root sources

| Source | Destination / migration |
|---|---|
| `INDEX.md` | `docs/development/INDEX.md` — closed list, drop 33 Historical rows and stale counts |
| `pendings.md` | `work/pendings.md` — promote unchanged syntax (parser input) |
| `task-set-plan.md`, `hitos-audit.md` | live metrics → `work/measures.md`; originals archived |
| `roadmap-2026-06.md`, `proposals.md`, `plans/index.md` | roadmap-map + stage aliases → `standards/plan.md`; originals archived |
| `questy-proposals.md`, `standards.md` (root), `UseCase-adv.md` | decisions → `standards/skills.md` / `standards/flows.md` / `standards/mds.md`; scripts → `skills/questy/` |
| `plans/standards.md` (SD01–SD19) | fold into `work/pendings.md` `VARIOUS_Q34–50`; repoint its 46 task owners |
| `others/flove-libs-insights.md` | `standards/mds.md` + `docs/development/contract.md` (values/floor) |
| `proposals/frontend-tiers.md` | closed tier status → `standards/apps.md` |
| `research/vr_interfaces.md` | abandoned note → `standards/experience.md` |
| `reviews/2026-07-25-browsy-fastapi-libsql-performance-review.md` | architecture notes → `standards/systems.md` |
| `agents.md`, `skills-library.md`, `archive.md`, `a11y-development-index.md`, 12 old `superpowers/specs/*` | archive only; their facts are already canonical in standards chapters |

That covers all 61 MDs: 14 root + 12 old specs + 6 browsy + 12 pre-build + 11 plans + 2 proposals + 1 research + 1 review + 1 bridges + 1 others.

## 3. Reference automation — tracker → current wiki source

This replaces stale `owner`/`source` pointers with an automatically resolved canonical page.

### 3.1 `docs/development/wiki.json`

```json
{
  "schema": "flove-wiki-manifest/1",
  "roots": ["docs/development"],
  "archive": "docs/development/archive",
  "pages": [
    {
      "id": "backend/mynet",
      "path": "standards/mynet.md",
      "trunk": "backend",
      "topic": "mynet",
      "status": "active",
      "owns": ["MyNet L1–L5 ladder", "flove-auth/1", "BSP acceptance"],
      "supersedes": [
        "archive/old/plans/2026-11-17-appy-authy-mynet.md",
        "archive/old/browsy/spec.md",
        "archive/old/browsy/browsy-questions.md",
        "archive/old/browsy/pre-build/02-authy-levels.md"
      ],
      "updated": "2026-11-21",
      "heavy": false
    }
  ],
  "labels": {
    "standards": "standards/mds.md",
    "owner": "standards/work.md",
    "proposals": "standards/plan.md",
    "conflicts": "plans/conflicts.md",
    "pendings": "work/pendings.md"
  }
}
```

### 3.2 `tools/dev/wiki-resolve.py`

- `--path <old>` — resolve an old MD path (optionally `#anchor`) to the canonical section page by walking `supersedes` transitively (max depth 8; cycles are a gate error).
- `--task <id>` — return the task's canonical page and its `CONTEXT` block only.
- `--plan` — dry-run: emit the JSON diff of every `owner`, `source`, `doc` and `standards` value that would change.
- `--write` — apply the rewrite to `milestones.json`, preserving the old value as `origin` / `migrated_from`.
- `--check` — fail if any live pointer resolves into `archive/`, is unresolvable, is cyclic, or points to a page missing a `CONTEXT` block.

Resolution order: exact path → anchored path → `supersedes` chain → `labels` table → error. **Never silently fall back to archive.**

### 3.3 Integration

- `tasky.py show <id>` uses `--task`: prints PROC quick table + row + canonical page `CONTEXT` only (target ~1–1.5k tokens instead of ~15–25k). `weight`, `options`, `next`, `easy` and `procedure` keep their current output unchanged.
- `build-work-tracker.py` adds a generated `wiki` field to each Work row from the resolver — additive to `choice`, never a replacement for it.
- `jsony_check.py` gains the resolver gate; `check-docs-manifest.py` validates the closed list, frontmatter, `CONTEXT`, 20 KB `heavy` flag, generated count lines, and allowlists `work-moves.json` as an intentionally absent inbox.

## 4. File-by-file change list outside the wiki

### 4.1 Scripts (paths from current audit; verify at execution)

| File | Changes |
|---|---|
| `tools/dev/procedures_source.py:1–24,39–40` | `AGENTS.md` path → `docs/development/AGENTS.md`; parser must still find all **ten** PROC blocks including PROC-10 |
| `apply-task-set-v2.py:26` | `FILE` → `docs/development/work/milestones.json` |
| `build-common.py:4,29,30,119–120` | register/common paths; `sources.*` provenance strings; make `sources.plans` describe the hito-`source` grouping, not a phantom read |
| `build-work-tracker.py:33–34` | `PEND`, `MILESTONES_FILE` → `work/` paths |
| `build-work-tracker.py:987` | `MOVES_INBOX` → `docs/development/work/work-moves.json` |
| `build-work-tracker.py:990–991` | `COUNT_MIRRORS` → `docs/development/INDEX.md` and `work/measures.md` |
| `build-work-tracker.py:318–334` | Standard-URL validator → `https://flove.org/docs/development/INDEX.md` |
| `build-work-tracker.py:339–358` | anchor validator skips `archive/` |
| `build-work-tracker.py:953` | `snapshot` label → new pendings path |
| `check-restore.py:21`, `jsony_check.py:9,44–47`, `register_projection.py:14` | register path constants |
| `tasky.py:36,56,59–70,129–130` | register path, context tree, profile tabs; add resolver + `--context`; leave `weight`/`options` (PROC-10), the five-level `EFFORT` ladder and `easy` / `next --do` behaviour intact |
| NEW `wiki-resolve.py`, NEW `check-docs-manifest.py` | §3 |

### 4.2 `docs/development/AGENTS.md`

`:15` register link; `:25` retired-layout rule; **seven** `Standard:` URLs change — PROC-01/07/08/09/10 (`debates/INDEX.md` → `docs/development/INDEX.md`), PROC-02 (`standards/contract.md#the-floor` → `docs/development/contract.md#the-floor`), PROC-03 (`standards/backend.md` → `standards/index.md`, the JSON-backbone owner; `backend.md` is deleted); `:119` `hitos-audit.md#conflict-register`; `:142` app-database-stages §4.8.3; `:145–146` `work-moves.json`. Verify exact line numbers against the canonical file before editing.

**Merge `standards/AGENTS.md` into this file** (§10.5): its 13 work-style rules become §1, the ten PROC blocks become §3 and remain contiguous for `procedures_source.py`. Delete `standards/AGENTS.md` after repointing its 33 refs; do **not** keep a second copy. Its retired notes (`debates/archive.md`, home-directory layout) resolve into `archive/old/archive.md`.

PROC-04/05/06 Standard URLs stay (`frontend/export.md`, `frontend.md#1318…`, `skills/standing.md`); nothing in `standards/` becomes a duplicate topic page. Add a rule: *task owner/source references resolve through `wiki.json`; archived paths and raw `plans/debates/` drafts are never permanent owners.* Preserve PROC-10's `choice_weight`, `choice_override`, `choice_reason`, `tasky.py weight` / `options` and the `choice` filter unchanged — the generated `wiki` field is additive and must not alter choice classification.

### 4.3 `docs/development/contract.md`

Add `CONTEXT` block and the "one fact, one home" clause.

### 4.4 `development/index.html`

`:93981` app-database-stages link; `:94004` `pendings.md#ux01` data-source; `:94033,94041,94051,94062` four MD source cards; `:97584` `PLANS`/`DEBATE` category labels (keep as labels, note they are not paths); add generated "Wiki source" link from the resolver. The `WORK-DATA` block is regenerated wholesale. Keep the new `TASK_CATS` / `TASK_CAT_LABEL` map through regeneration: `archived` + the five canonical efforts `very easy` · `easy` · `medium` · `hard` · `very hard`, with Spanish (`Muy fácil` · `Fácil` · `Medio` · `Difícil` · `Muy difícil`) only in the `es` label half — never in the data or the `en` half. Relabel that filter from `Estado / State` to `Esfuerzo / Effort`: its group is `taskcat` and it filters effort, not task state. `level` / `degree` / `nivel` / `grado` are display synonyms of effort only (AGENTS §3.3a).

### 4.5 Standards book

`README.md:23,27,30,42,45,118,143,167`; `_sidebar.md:4,25–29` (replace chapter links with the 20 stable pages in `development/standards/`); `adoption.md:8`, `backend.md:4,51,473,478,479,520,541,542,564,565`, `worldview.md` — all three deleted, every ref repointed to the owning topic page (§10.3); `apps/README.md:15` (deleted; §10.4); `frontend/export.md:13`; `frontend/routing-colours-db.md:9`; `frontend/summary.md:35,91`; `frontend/frontend.md:44,46,52,108,440,450,535,673,897,1072`; `puzzy.md:9,502,681`; `AGENTS.md:85` (merged, then removed; §10.5). `contract.md` moves out; `apps/` and `scripts/` are removed. All 33 refs to `standards/AGENTS.md` repoint to `docs/development/AGENTS.md#how-to-work`.

### 4.6 Skills

`skills/CONFIG.md:102–105`; `jsony/SKILL.md:10,28,30,53,127`; `tasky/SKILL.md:18,90,112–113,121,126–127`; `updaty/SKILL.md:42,44`; `questy-tasky-flove/SKILL.md:35`; `questy-all/SKILL.md:19`; `questy/index.html:1276`. Questy reference MDs land in `skills/questy/`. Preserve the five English effort names in both skills and the automatic state-move rule plus very-easy batch proposal in `tasky` / `questy-tasky-flove`; the path rewrite must not reintroduce Spanish values or put state moves back among judgment calls.

### 4.7 Other repo HTML / tools

`community/index.html:74,80,86,92,104,110,116`; `apps/sys/authy/index.html:194,598,792`; `apps/sys/browsy/2026-11-18-browsy-extension-demo.html:722,724,725,730,731,732`; `apps/sys/browsy/index.html:659,663`; `apps/sys/browsy/2026-11-17-browsy-wizy-nety.html:733`; `apps/sys/wizy/index.html:1374–1376`; `development/standards/workflow/workflow.html:214,216,661`; `tools/routing.json:5`; `tools/check-a11y-axe.py:136`.

### 4.8 JSON backbone

`milestones.json`: 747 task owners, 139 hito sources, 55 standards URLs, 206 gaps, 11 new-ticket sources, 1 docs pointer — all rewritten by `wiki-resolve.py --write`, with originals preserved. `common.json` regenerated. `work-moves.json` stays absent but its path constant changes.

**Effort reclassification (carried into the migration).** The work taxonomy is now a five-level ladder with canonical **English** values in all data, code and docs; Spanish survives only as UI labels (§4.4):

| # | Canonical value | UI label (es / en) | Live before migration |
|---|---|---|---|
| 1 | `very easy` | Muy fácil / Very easy | 0 — open |
| 2 | `easy` | Fácil / Easy | 1,235 |
| 3 | `medium` | Medio / Medium | 0 — open |
| 4 | `hard` | Difícil / Hard | 315 |
| 5 | `very hard` | Muy difícil / Very hard | 9 |

This was already applied in the working tree to the current register: 2,364 `effort` values renamed in place (`fácil`→`easy` 2,038, `difícil`→`hard` 315, `muy difícil`→`very hard` 11, counting the archive). Live totals stayed 1,559; archive 805 (803 easy · 2 very hard). No task was assigned to `very easy` or `medium` — populating those two empty levels is an open owner decision (§7.8), not a side effect of the folder move.

The resolver must treat `effort` as **data, not a path**: `wiki-resolve.py --write` rewrites `owner`, `source`, `standards` and gap pointers, and leaves every `effort` value byte-identical. The regeneration then propagates the English values into `common.json`, the embedded `WORK-DATA` block and the `taskcat` groups (six filter chips: archived + five efforts). The generator constants changed with the taxonomy — `EFFORTS` in `build-work-tracker.py`, `EFFORT` / `EASY` in `tasky.py`, and the four seed literals in `apply-task-set-v2.py` — so phase 7 must verify those constants still match the register after the script paths move to `tools/`. Historical debate MDs that quote the old Spanish names are records of past decisions and are **not** rewritten; they move verbatim with `archive/old/`.

## 5. Phases

0. **Baseline.** Backup `development/`, `docs/`, `tools/` to `/tmp/opencode/docs-migration-backup-<date>/`. Green all six sync-order checks. Record 326 hitos / 1,559 live / 805 archived and current token cost of the top 10 owners. Also record the effort distribution (live 1,235 easy · 315 hard · 9 very hard · 0 very easy · 0 medium; archive 803 easy · 2 very hard) so the resolver can prove no value changed.
1. **Skeleton.** Create `docs/development/` with `work/`, `plans/` + `plans/debates/`, `wiki.json` with the full `supersedes` graph, `INDEX.md`; create the 20 flat stable pages in `development/standards/`. New files only.
2. **Content migration — all at once.** Write every topic page from §2 **and §8** in one changeset, plus the topic-named child plans (§10.1). Start with `appy-dashboard-redesign.md` (zero inbound references) as dry run, then write the rest before any source is archived. Split `browsy-questions.md` live/historical.
3. **Standards consolidation.** In the same changeset: delete the duplicate chapters `backend.md`, `adoption.md`, `worldview.md` after their content lands in topic pages (§10.3), port and delete `apps/` (§10.4), merge the two AGENTS files (§10.5), move every script home into `tools/` (§10.6). No fact gets a second home and no duplicate hub is created.
4. **PROC spine.** Move merged `AGENTS.md` + `contract.md`; repoint the seven Standard URLs (01/02/03/07/08/09/10), `procedures_source.py`, script constants. Old tree still present → dual-valid; `--check` must stay green and `tasky.py procedure` must still print all ten blocks.
5. **Resolver.** Run `wiki-resolve.py --plan` → review → `--write` → `--check`; integrate into `tasky.py` and `build-work-tracker.py`.
6. **Cutover.** `git mv` live JSONs to `work/`, then `git mv` remaining `debates/` to `archive/old/` and `standards/apps/` to `archive/old/apps/`; the 20 ported sources need no separate copy — their originals are already inside the verbatim tree.
7. **Rewrite + regenerate.** Everything in §4; then `--build`, all checks, manifest gate, token gate.
8. **Second pass later.** Archive link pruning only after a clean release; no live deletions remain by then.

## 6. Verification

```
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

Plus: zero remaining references to old `development/standards/debates/`, `standards/apps/`, `standards/AGENTS.md`, `standards/backend.md`, `standards/adoption.md`, `standards/worldview.md` or `development/scripts/` paths; all task owners resolve into the closed list; every stable page is `standards/<topic>.md` and every plan is `plans/<category>/<topic>.md` with the same topic keyword; every draft in `plans/debates/` has `status: draft` and an existing section folder; `tasky.py show` on the top 10 owners stays under the token budget; `tasky.py procedure` / `weight` / `options` output is byte-identical to the baseline except for the seven Standard URLs.

Effort-specific checks on top of the gates: `effort` is one of the five English values on every live and archived task (no `fácil` / `difícil` / `muy difícil` survives in data, script constants or PROC text); the distribution equals the phase-0 baseline exactly — the resolver changed paths, not effort; `tasky.py easy` still reports the same counts; the Work filter offers exactly six chips (archived + five) with Spanish only in `es` labels; state moves remain automatic after an evidence pointer verifies.

## 7. Confirm before execution

1. `flove.org/docs/` really serves the top-level `docs/` folder (needed for the new PROC Standard URL).
2. `docs/development/INDEX.md` may replace `development/standards/debates/INDEX.md` as the PROC target.
3. Token budget for `tasky.py show` (suggest 2k tokens).
4. Confirm stable pages are flat `standards/<topic>.md`, plans are `plans/<category>/<topic>.md` using the same topic keyword, and `work/` files are flat (§10.1); the old awkward `docs/development/docs/plan.md` disappears.
5. Confirm that `backend.md`, `adoption.md` and `worldview.md` are deleted outright, with their 600+ refs repointed to topic pages (§10.3); no hub stubs.
6. Confirm the two AGENTS files merge into one with no pointer stub (§10.5).
7. Confirm all script homes collapse into `tools/` and `tools/dev/` — no `tools/standards/` subfolder; `standards/scripts/` goes into `tools/dev/` with everything else (§10.6).
8. Decide what fills the two empty effort levels (§4.8): leave `very easy` and `medium` at 0 and let `tasky.py next --do` queue the 142 ready `directo + easy` tasks, or give an id list / rule for reclassifying a specific set. This is independent of the folder move and is **not** done by the resolver.

## 8. Chapter-level port ledger — all sources, all headings

Chapter structures were read from the actual files on 2026-11-21. **Port everything in one changeset**: write every destination section page first, then move sources to `archive/`. A partial pass duplicates facts because the same topics recur across many files (see §8.13 collisions).

`standards/work.md` and `plans/conflicts.md` are the "debates" surface — open questions, status, decision logs and conflicts go there; specifications go to the domain pages.

### 8.1 `plans/2026-11-21-app-database-stages.md` (433 lines)

| Chapter | Port to |
|---|---|
| 1 Goal and boundary | `standards/plan.md` (goal) + `standards/work.md` (boundary policy) |
| 2 The five stages | `standards/plan.md` — canonical stage ladder |
| 3 Minimal model — replicated from Appy index | `standards/json.md` |
| 4 First objective — migrate Goddy, Realy, Appy to `mature` | `standards/apps.md` |
| 5 Sys-app functionality tests — no nety required | `standards/apps.md` |
| 6 Update log | archive only |

### 8.2 `plans/2026-11-17-appy-authy-mynet.md` (520 lines)

| Chapter | Port to |
|---|---|
| 1 What activates what | `standards/mynet.md` |
| 2 Portable auth record `flove-auth/1` | `standards/schemas.md` (schema) + `standards/mynet.md` (use) |
| 3 Transport — A Web / B Browsy | `standards/systems.md` |
| 4 UI | `standards/experience.md` |
| 5 Security checklist | `standards/systems.md` |
| 6 Open questions | `standards/work.md` |
| 7 Spec-driven development map | `standards/work.md` |
| 7b Email authentication (planned) | `standards/mynet.md` |
| 7c Risa as identity provider (planned) | `standards/mynet.md` |
| 7d MyNet feature flags and Browsy identity (+ Browsy hash) | `standards/mynet.md` |
| 7e MyNet state and storage | `standards/storage.md` |
| 8 Status | `standards/plan.md` |

### 8.3 `plans/2026-11-20-appy-dashboard-redesign.md` (135 lines)

| Chapter | Port to |
|---|---|
| 1 Goal | `standards/apps.md` |
| 2 Sources and ownership | `standards/plan.md` (ownership rule) + `standards/apps.md` |
| 3 Feature lock — no regressions | `standards/apps.md` |
| 4 Layout | `standards/apps.md` |
| 5 Data contract — preserved exactly | `standards/json.md` |
| 6 Theme redo (§13.14) | `standards/experience.md` |
| 7 Dashboard customisation — planned only | `standards/apps.md` marked planned |
| 8 Verification | `standards/apps.md` |
| 9 Rollout | `standards/plan.md` |

### 8.4 `plans/central-backend.md` (338 lines)

| Chapter | Port to |
|---|---|
| Architecture Decision: Extension + Central = CORE | `standards/systems.md` |
| Decisions — CB01-CB40, D01-D23, E01-E25 | `standards/systems.md` (canonical ID index) |
| Decisions — CA01-CA44 shared code | `standards/mds.md` + `standards/systems.md` |
| Decisions — G01-G55, CB_S01-CB_S10 | `standards/mynet.md` |
| Architecture — tech stack, API, errors, data flow, server structure | `standards/systems.md` |
| Identity model (progressive) | `standards/mynet.md` |
| Browser-side persistence (SoloRich + Central) | `standards/storage.md` |
| Conflict resolution, Trust sync | `standards/systems.md` |
| Central modal, Central navigation | `standards/experience.md` |
| Nety→Central bridge | `standards/mynet.md` |
| Future: CentralRich (PostgreSQL + JSONB) | `standards/storage.md` |
| Conflicts | `plans/conflicts.md` |

### 8.5 `plans/puzzy.md` (37 lines)

| Chapter | Port to |
|---|---|
| Decisions made / Architecture — Aggregation, Compute | `standards/apps.md` |
| Tasks | `standards/work.md` |
| Conflicts | `plans/conflicts.md` |

### 8.6 `browsy/spec.md` (619 lines)

| Chapter | Port to |
|---|---|
| 1 Purpose and method | `standards/plan.md` |
| 2 Source-of-truth hierarchy | `standards/plan.md` |
| 3.1 Architecture | `standards/systems.md` |
| 3.2 Data classes and privacy invariants | `standards/schemas.md` + `standards/mynet.md` |
| 3.3 Authy | `standards/mynet.md` |
| 3.4 MyNet and MyFamily + 3.4.1 local groups | `standards/mynet.md` + `standards/schemas.md` |
| 3.5 Wizy and derivation | `standards/apps.md` + `standards/flows.md` |
| 3.6 Permissions and grants | `standards/systems.md` |
| 3.7 Interfaces and files | `standards/systems.md` |
| 3.8 Browsy extension standards (draft) | `standards/systems.md` |
| 4 Requirements | `standards/mynet.md` |
| 5 Old plans — reconciliation | `standards/plan.md` — canonical reconciliation table |
| 6 Development plan — Phases 0–8 | `standards/plan.md` |
| 7 Acceptance and test plan | `standards/work.md` (link from `standards/mynet.md`) |
| 8 Pending / out of scope | `standards/work.md` |
| 9 Changelog | archive only |

### 8.7 `browsy/browsy-questions.md` (819 lines)

| Chapter | Port to |
|---|---|
| Current Status | `standards/work.md` |
| Decisions Made + Survey / Implementation / Q205–224 / Q225–244 | historical log → archive; still-live decisions → `standards/mynet.md` |
| Next Questions to Ask (BD30, BD31) | `standards/work.md` |
| How to Use, Related Files | `standards/mds.md` |
| A · Authy and identity | `standards/mynet.md` |
| B · MyFamily and third-party data | `standards/mynet.md` + `standards/schemas.md` |
| C · Permissions and grants | `standards/systems.md` |
| D · Local network and transport | `standards/systems.md` |
| E · Wizy and derivation | `standards/flows.md` + `standards/apps.md` |
| F · Nety and the social layer | `standards/channels.md` + `standards/mynet.md` |
| G · Browsy engineering and security | `standards/systems.md` |
| H · UX and product | `standards/experience.md` |
| I · Legal, ethics and governance | `standards/docs.md` |
| J · Integration, schema and legacy | `standards/schemas.md` |
| K · Browsy extension standards | `standards/systems.md` |
| L · MyNet local groups | `standards/mynet.md` |
| Questy session 1 readout, Suggested survey order | `standards/work.md` |
| Pre-build pendings Q5…F6 | by topic: C/D/G → `standards/systems.md`; A/B/L → `standards/mynet.md`; E → `standards/flows.md`; F3/F6 → `plans/conflicts.md` |

### 8.8 `browsy/rationale.md` (875 lines)

| Chapter | Port to |
|---|---|
| 1 One-line vision | `standards/plan.md` |
| 2 Personal / Local / Social + apps in play | `standards/docs.md` + `standards/mynet.md` |
| 3 What changes against today | `standards/plan.md` |
| 4 Actors and components | `standards/systems.md` |
| 5 Data classes | `standards/schemas.md` |
| 6 What is derived? — the options | `standards/flows.md` |
| 7.1–7.4 flovePortrait envelope, extension, diagrams, API | `standards/json.md` |
| 7.5 MyFamily first local data manager | `standards/mynet.md` |
| 8 Diagram A, 9 Diagram B (three threads) | `standards/plan.md` |
| 10 Permission model | `standards/systems.md` |
| 11 Pull model — local net and Nety | `standards/mynet.md` |
| 12 Authy (+ 12.5 refined model) | `standards/mynet.md` |
| 13 Wizy inside Browsy | `standards/flows.md` + `standards/apps.md` |
| 14 JSON generation and schema | `standards/json.md` |
| 15 Threat model (v0) | `standards/systems.md` |
| 16 Milestones — specified | `standards/plan.md` |
| 17 Sources read | `standards/mds.md` (reference list) |
| 18 Ten questions Q1–Q10 | Q1/Q2 → `standards/schemas.md`; Q3/Q4/Q6/Q8/Q10 → `standards/mynet.md`; Q5 → `standards/systems.md`; Q7 → `standards/flows.md`; Q9 → `standards/json.md` |
| 19 Open decisions log | `plans/conflicts.md` |
| 20 Next action | `standards/work.md` |

### 8.9 `proposals/frontend-wizy.md` (136 lines)

| Chapter | Port to |
|---|---|
| What Wizy is / Operating areas / Custom magic contract / Relationship to summary standard | `standards/apps.md` |
| Open questions | `standards/work.md` |
| Magic button — Appy, Browsy (Nety later) | `standards/experience.md` |

### 8.10 `browsy/pre-build/*` (12 files)

| File | Chapters → destination |
|---|---|
| `01-mvp.md` | In v1 → `standards/mynet.md`; Deferred → `standards/plan.md`; Definition of done → `standards/work.md`; Build order → `standards/plan.md` |
| `02-authy-levels.md` | Short answer, Proposed ladder, State machine, What each gate unlocks, Why risa counts → `standards/mynet.md`; Storage → `standards/schemas.md`; Open → `standards/work.md` |
| `03-schemas.md` | `flove:authy/1`, `flove-identity/1`, `flove-authy/1`, `flove-group/0.1`, `flove-consult/1`, `flove-grant/1`, `flove-post/1`, `flove-invite/1`, `flove-bundle/0.1`, Rules → `standards/schemas.md`; `flove-portrait/1` → `standards/json.md` |
| `04-myfamily-profile.md` | 5 types, 7 areas, Profile shape, Percentages, What the group sees → `standards/schemas.md`; Consult agreements → `standards/mynet.md`; UI → `standards/experience.md`; Why this is better → `standards/mynet.md` |
| `05-native-host.md` | Shape, Invitations vs LAN discovery, First message set, Security, Install and update, MVP transport scope → `standards/systems.md`; Open → `standards/work.md` |
| `06-bridge-threat-model.md` | Boundary, API allowlist, Rules, Threats → `standards/systems.md`; Test cases → `standards/work.md` |
| `07-lineage-tests.md` | Lineage model, MVP UI, Fixtures → `standards/mynet.md`; Acceptance cases, E2E smoke → `standards/work.md` |
| `08-model-labels.md` | Else, Two Browsy chips, Decided, Why it matters, Proposed wording → `standards/experience.md`; Open → `standards/work.md` |
| `09-consult-agreements.md` | Actors, Agreement object `flove-consult/1` → `standards/schemas.md`; Flow, What crosses groups, No group moderation, Subject consent, UI → `standards/mynet.md`; Open → `standards/work.md` |
| `11-ui-pending.md` | Browsy UI + Nety UI (Surfaces, Languages, Constraints, Pending decisions) → `standards/experience.md`; Gate → `standards/work.md` |
| `README.md` → `index.md` | Decisions locked for v1 → `standards/plan.md`; Still open → `standards/work.md`; Artifacts → `standards/mds.md`; Build gate → `standards/work.md` |
| `open-issues.md` | closed log — archive only; live answers are already ported above |

### 8.11 `bridges/oasis.md` (195 lines)

| Chapter | Port to |
|---|---|
| 0 What Oasis is | `standards/mynet.md` |
| 1 Local deployment reality, 2 Architecture | `standards/systems.md` |
| 3 SSB data model + module anatomy + key files | `standards/schemas.md` |
| 4 Mapping flove → Oasis | `standards/mynet.md` |
| 5 Open questions / next steps | `standards/work.md` |
| Links | `standards/mds.md` |

### 8.12 `a11y-report.md` (8 lines)

Entire generated summary → `standards/accessibility.md`; raw file stays in `archive/old/a11y-report.md`.

### 8.13 Collision clusters — decide once, then link

These topics appear in 3–5 sources. The named page is the **only** writer; every other chapter becomes a link.

| Topic | Canonical page | Other sources that must link, not restate |
|---|---|---|
| Authy identity / ladder | `standards/mynet.md` | appy-authy-mynet §2/7b/7c/7d, spec §3.3, rationale §12, 02-authy-levels, questions §A |
| MyFamily / local groups | `standards/mynet.md` | spec §3.4.1, rationale §7.5, 04-myfamily-profile, questions §B/§L |
| Schemas / storage keys | `standards/schemas.md` | 03-schemas, 04-myfamily-profile, spec §3.2, rationale §5, questions §J |
| flovePortrait envelope / API | `standards/json.md` | app-database-stages §3, rationale §7.1–7.4/§14, dashboard §5 |
| Permissions / grants / bridge | `standards/systems.md` | spec §3.6, rationale §10/§15, questions §C/§G, 06-bridge-threat-model |
| Native host / transport | `standards/systems.md` | appy-authy-mynet §3, 05-native-host, questions §D, oasis §2 |
| Wizy / derivation | `standards/flows.md` | spec §3.5, rationale §6/§13, questions §E, frontend-wizy |
| Open questions / status / tests | `standards/work.md` | all `§Open`, `§Status`, `§Pending`, acceptance chapters |
| Conflicts | `plans/conflicts.md` | central-backend, puzzy, rationale §19, questions F3/F6 |

### 8.14 Anti-duplication gate

- `docs/development/PORT-LEDGER.md` is generated from §8.1–8.13 and §12: one row per source chapter → destination page + anchor, or `archive-only`. It lives outside `archive/` so the manifest gate can read it (D56); archive itself stays opaque.
- `check-docs-manifest.py` extends to assert: every source heading has a ledger row; every ledger destination anchor exists; no destination bullet is cited by two source chapters without an explicit `shared:` marker; every archived source is listed.
- The section pages are written **once**, in phase 2, in a single changeset. No follow-up edits add the same fact to a second page.

## 9. `development/standards/` — what stays and what moves

Read from disk 2026-11-21. Everything below stays physically where it is **except** `debates/`, `contract.md`, `apps/` and `AGENTS.md` (see §10).

| Area | Contents | Migration decision |
|---|---|---|
| root chapters | `AGENTS.md`, `README.md`, `_sidebar.md`, `adoption.md`, `backend.md`, `contract.md`, `index.html`, `puzzy.md`, `vocabulary.md`/`.html`, `worldview.md` | `contract.md` → `docs/development/contract.md`; PROC-02 Standard URL becomes `…/docs/development/contract.md#the-floor`. `AGENTS.md` merged into the parent (§10.5). `adoption.md`, `backend.md` and `worldview.md` are **deleted** after their facts land in topic pages (§10.3). No hubs, no new files here. |
| `apps/` | `README.md`, `onboarding-copy.md` | **Removed**; content ported per §10.4, originals survive in `archive/old/apps/` |
| `debates/` | 61 MDs + HTML + `.bak` | **The tree being ported and archived** → `archive/old/` |
| `frontend/` | `counters.md`, `export.md`, `frontend.md`, `publish.md`, `routing-colours-db.md`, `summary.md` | Stay; 10 referrals repointed (§4.5) |
| `puzzy/` | `puzzy.schema.json`, `example-water.json` | Stay |
| `risaliberada/` | `plan-v2.md`, `risaliberada.md`, `lol/`, `mermaid/` + 7 assets | Stay; no active referrals to debates |
| `scripts/` | `check-drift.py`, `check-skills.py`, 2 harnesses, 3 `publish-*.sh` | Move to `tools/dev/` with the other scripts — no `tools/standards/` duplicate (§10.6); `check-skills.py` has **no** debates references |
| `skills/` | `CONFIG.md`, `README.md`, `standing.md`, 20 skill dirs + eval workspaces | Stay; 7 SKILL/config referrals repointed (§4.6). Questy reference MDs land in `skills/questy/`. Eval workspaces untouched. |
| `workflow/` | `workflow.html` + 3 demos | Stay; 3 referrals repointed (§4.7) |

Also:

- `standards/AGENTS.md` (work-style rules) is **merged into** `docs/development/AGENTS.md`; the separate file is removed after its 33 refs are repointed.
- `_sidebar.md` docsify nav loses the three duplicate chapter links and gains the 20 flat stable page links + `docs/development/INDEX.md`.
- `standards/README.md` stable index gains one peer row for the development wiki and drops the `apps/` row.
- `standards/index.html` gains a link to `../../docs/development/INDEX.md`.
- Heavy static files (`vocabulary.html` ~1.7 MB, `frontend.md` ~69 KB, `puzzy.md` ~33 KB) are never loaded by a task update after the resolver — only the canonical `CONTEXT` block is.

## 10. Tidy — archive name, raw tray, topic folders and merges

Read from disk 2026-11-21: `AGENTS.md` 209 lines / 10 PROCs, `standards/AGENTS.md` 85 lines, `adoption.md` 6 `##` chapters, `backend.md` 16 `##` chapters, `apps/README.md` 172 lines, `apps/onboarding-copy.md` 32 `##` headings = 30 app blocks + `Shared shape` + `Catalog-only apps`.

### 10.1 `archive/old/` + `plans/debates/` + topic-only filenames

1. `archive/debates/` is renamed **`archive/old/`**. The earlier `archive/ported/` idea is dropped — those 23 source rows are already inside the verbatim old tree, so a second copy would be exactly the duplication we are removing. Ledger paths become `archive/old/…`.
2. A new live tray `docs/development/plans/debates/` holds raw on-the-fly plans. It has one `README.md` with the convention and no facts. A dropped draft uses:

   ```md
   ---
   status: draft
   section: backend/mynet
   created: 2026-11-21
   ---
   ```

3. Promotion is one operation: elaborate in the tray → `git mv` to `plans/<category>/<topic>.md`, reusing the topic keyword of the stable page it serves → port the facts to `standards/<topic>.md` → add the plan to that page's `CONTEXT`/child list → add a `supersedes` entry in `wiki.json`. The raw original stays in `archive/old/`.
4. `wiki-resolve.py --check` treats `status: draft` as a **warning** with age; a draft older than 14 days, or a draft used as a milestone `owner`, becomes an error. No live pointer ever resolves into `archive/old/`.
5. The **folder** carries the category owner (PROC-01: one section, one subsection, one owner); the **filename** is the topic keyword, identical to the stable sibling page in `standards/`. No `backend-mynet-…` compound names anywhere. Secondary sections are listed in the plan's `also:` list and link back; they never get a second copy.

| Old source | Topic-named plan (folder = owner) |
|---|---|
| `plans/2026-11-21-app-database-stages.md` | `plans/backend/storage.md` |
| `plans/2026-11-17-appy-authy-mynet.md` | `plans/backend/mynet.md` |
| `plans/2026-11-20-appy-dashboard-redesign.md` | `plans/frontend/apps.md` |
| `plans/central-backend.md` | `plans/backend/systems.md` |
| `plans/puzzy.md` | `plans/frontend/apps.md` |
| `browsy/spec.md` | `plans/docs/plan.md` |
| `browsy/browsy-questions.md` | `plans/docs/work.md` |
| `browsy/rationale.md` | `plans/docs/plan.md` |
| `proposals/frontend-wizy.md` | `plans/frontend/apps.md` |
| `browsy/pre-build/01-mvp.md` | `plans/backend/mynet.md` |
| `browsy/pre-build/02-authy-levels.md` | `plans/backend/mynet.md` |
| `browsy/pre-build/03-schemas.md` | `plans/data/schemas.md` |
| `browsy/pre-build/04-myfamily-profile.md` | `plans/data/schemas.md` |
| `browsy/pre-build/05-native-host.md` | `plans/backend/systems.md` |
| `browsy/pre-build/06-bridge-threat-model.md` | `plans/backend/systems.md` |
| `browsy/pre-build/07-lineage-tests.md` | `plans/backend/mynet.md` |
| `browsy/pre-build/08-model-labels.md` | `plans/frontend/experience.md` |
| `browsy/pre-build/09-consult-agreements.md` | `plans/data/schemas.md` |
| `browsy/pre-build/11-ui-pending.md` | `plans/frontend/experience.md` |
| `browsy/pre-build/README.md` | `plans/docs/plan.md` |
| `browsy/pre-build/open-issues.md` | archive only (closed log) |
| `bridges/oasis.md` | `plans/backend/mynet.md` |
| `a11y-report.md` | no plan — generated summary goes straight to `standards/accessibility.md` |

### 10.2 Stable pages are flat files in `standards/`

1. The 20 stable topic pages are real flat files `development/standards/<topic>.md` — no trunk folder, no thin hub, no second copy. `docs/development/` keeps only `INDEX.md`, `AGENTS.md`, `contract.md`, `wiki.json`, `plans/`, `work/` and `archive/`. Levels need no page: they are the core stages, already described in `contract.md`, `standards/frontend/frontend.md` §13.18 and `standards/mds.md`. The `#data-ux` anchor stays in the Work page as that core-stage view, but owns no separate file. Two canonical axes only — `effort` and `stage`; `level` / `degree` are display synonyms of effort, `phase` / `fase` of stage. The frontend 1–5 ladder is a view of the core stages, not a third effort scale (AGENTS §3.3a).
2. Each stable page carries a `html_place:` field in its `CONTEXT` block pointing to the real anchor in `development/index.html` (verified 2026-11-21): `#plan-maps`, `#work-tracker`, `#md-sources`, `#ai`, `#apps`, `#data`, `#data-json`, `#data-database`, `#localhost`, `#messenger`, `#p2p`, plus `#ai-note-wizy`.

| Topic page | HTML place |
|---|---|
| `standards/plan.md` | `#plan-maps` |
| `standards/work.md` | `#work-tracker` |
| `standards/scripts.md` | `#localhost` |
| `standards/systems.md` | `#p2p` |
| `standards/mynet.md` | `#p2p` / `#messenger` |
| `standards/storage.md` | `#data-database` |
| `standards/apps.md` | `#apps` |
| `standards/accessibility.md` | `#apps` |
| `standards/experience.md` | `#apps` |
| `standards/models.md` | `#ai` |
| `standards/skills.md` | `#ai` |
| `standards/flows.md` | `#ai-note-wizy` |
| `standards/mds.md` | `#data` |
| `standards/index.md` | `#data` |
| `standards/json.md` | `#data-json` |
| `standards/schemas.md` | `#data` |
| `standards/docs.md` | `#md-sources` |
| `standards/feedback.md` | `#md-sources` |
| `standards/language.md` | `#md-sources` |
| `standards/channels.md` | `#messenger` |

3. `check-docs-manifest.py` asserts each `html_place` anchor exists and each child plan `plans/<category>/<topic>.md` is referenced by exactly one stable page sharing that topic keyword. No hub files, no extra context blocks.

### 10.3 `backend.md`, `adoption.md`, `worldview.md` — split, then delete

1. These three `standards/` chapters duplicate the topic pages. `backend.md` has 504 refs and is PROC-03's `Standard:` URL; `adoption.md` has 92 refs; `worldview.md` holds the old "why + map". Port their unique content, repoint **every** ref to the owning topic page (or `INDEX.md` / `contract.md` for the map and values), then delete the files. No hub stub — a stub is the third copy rule 1.1 forbids. PROC-03 moves to `standards/index.md`.

| `backend.md` chapter | Destination |
|---|---|
| §0 Executive summary, §1 Closed decisions, §9 Roadmap | `standards/plan.md` |
| §2 Architecture overview, §4 Element life cycle | `standards/systems.md` |
| §3.1 Upper ontology, §3.2 Per-app mapping, §3.3 Vocabulary policy, §3.4 `asterism_path` | `standards/mds.md` |
| §3.5 `FloveElement` schema | `standards/schemas.md` |
| §5 Routing, §6 Publisher adapter, §7 Common traceable area | `standards/index.md` |
| §8 Puzzy engine | `standards/apps.md` |
| §10 Strategic persistence | `standards/storage.md` |
| §11 Central distro | `standards/scripts.md` |
| §12 Data depth levels | `standards/mds.md` |
| §13 MyNet subsection | `standards/mynet.md` |
| §14 Chatland cross-axis hitos | `standards/channels.md` |

| `adoption.md` chapter | Destination |
|---|---|
| Architecture | `standards/systems.md` |
| Web of Trust Persistence Budget | `standards/storage.md` |
| CSS abstraction checklist (§13.16) | `standards/experience.md` |
| Publish to Appy (§13.15) — adoption & rollout | `standards/apps.md` |
| Distro adoption (§13.11) | `standards/scripts.md` |
| Generic Webhook Exports | `standards/systems.md` |

2. Any duplicate of a fact in §8 is resolved by the §8.13 collision table: the named canonical page wins, these chapters either supply the canonical text or link to it in the same changeset.

| `worldview.md` content | Destination |
|---|---|
| Why / principles | `docs/development/contract.md` (already owns values) |
| Map of chapters and trunks | `docs/development/INDEX.md` (closed list + compact map) |
| Any chapter detail | the owning topic page from §2 / §8 |

### 10.4 Remove `standards/apps/`

1. `apps/README.md` (LocalHost distro status/index) → pipeline, zip, `sw.js`, download, TWA, `check-distro.sh`, routing count → `standards/scripts.md`; self-contained assets, entry model, four run modes and tiers → `standards/apps.md`; milestones and the "one root, no link rewriting" rule → `standards/plan.md`; the skills table → `standards/skills.md`.
2. `apps/onboarding-copy.md` → shared shape and the ten-step pattern → `standards/experience.md`; the 30 app-specific intro blocks (+ `Shared shape`, `Catalog-only apps`) stay as one table in the child plan `plans/frontend/experience.md`, linked from both `standards/experience.md` and `standards/language.md` (wording consistency). It is reference material, not a second copy of a standard.
3. Move `standards/apps/` verbatim to `archive/old/apps/` at cutover and delete the live folder. It is outside the old `debates/` tree, so this is the one extra archived subtree beyond the verbatim debates copy — still a single copy.

### 10.5 Merge the two AGENTS files

1. `standards/AGENTS.md` (work-style rules 1–13, Where things live, Editing rule, Voice, retired notes) becomes §1 **How to work** of `docs/development/AGENTS.md`; the current §1 Authority becomes §2, the ten PROC blocks become §3, and the reading notes shift down accordingly. Keep the PROC blocks contiguous and byte-identical apart from the seven Standard URLs — `procedures_source.py` parses `### PROC-nn` headings and nothing else.
2. Do **not** keep a short `standards/AGENTS.md` pointer: rule 1.1 says join or delete, never add a third copy. Repoint all 33 refs to `docs/development/AGENTS.md#how-to-work`; its retired `debates/archive.md` and home-directory-layout note resolve to `archive/old/archive.md#home-directory-layout`.
3. Preserve the Spanish rules verbatim (rule 13.1 keeps repo content English with the three named exceptions) and the continuous-number format rule 12.3. Merge only — no rewording in this changeset.
4. Update `procedures_source.py` to the new path and assert it still finds exactly ten PROC blocks; `tasky.py procedure` output must stay byte-identical to baseline except the seven URLs.

### 10.6 Collapse every script home into `tools/`

1. `development/scripts/` (register builders, gates, `tasky.py`, `procedures_source.py`, plus the new `wiki-resolve.py` and `check-docs-manifest.py`) moves to **`tools/dev/`**. Its paths are already rewritten in §4.1.
2. `standards/scripts/` (`check-drift.py`, `check-skills.py`, two harnesses, three `publish-*.sh`) moves to `tools/dev/` too — there is no `tools/standards/`; item 7 of §7 is closed on this point.
3. General scripts already in `tools/` stay at the top level. Result: one higher scripts folder, no `scripts/` under `development/` or `standards/`, and all commands in §6 change to `python3 tools/...`.
4. `check-distro.sh` and `publish-web.sh` are named in the work-style rule 10.2 as living in `development/scripts/`; that rule moves into the merged AGENTS file and its path text is updated to `tools/dev/` in the same changeset.


## 11. Decision ledger — every decision in force for this migration

All entries were taken 2026-11-21. **In force** means already applied in the working tree or fixed for the cutover; **open** means the owner has not chosen yet. No entry below is a new proposal — this section records what was decided elsewhere.

### 11.1 Governance, skills and pick flow

| ID | Decision | Status |
|---|---|---|
| D01 | Plan is proposed, not executed. No git commit or push without the owner asking. | in force |
| D02 | This temporary file moves to `docs/development/archive/old/` at cutover as historical record. | planned |
| D03 | `tasky` stays exactly one `SKILL.md`; no `PLAYBOOK.md`, `CARD.md` or third doc; no duplicate docs. | in force |
| D04 | Free work uses `tasky.py` without loading the skill. Strict run only for a cold-queue pick, a state move, a procedure edit or a red gate. | in force |
| D05 | `/tasky` both picks **and** works; a clicky intro form opens on `/tasky` and shows what it first asks. | in force |
| D06 | Ask the owner on judgment calls — task choice, unblocking, heavy-list drops, procedure edits, destructive steps. A verified state move is automatic and never asked. | in force |
| D07 | `questy` owns when/how to ask (batch, ★, answer grammar); `tasky` owns what (bundle, candidates, proof). Both default to 30-question batches. | in force |
| D08 | `/tasky <profile>` with `flove` default; context bundle = questy-all advanced Context tree + Plan/Work tab content managers. | in force |
| D09 | Survey behaviour belongs to `questy-tasky-flove`, not base `questy`; the misplaced questy edit was reverted. | in force |
| D10 | Thin `questy-tasky-flove` call created (option 2), registered as skill 21; planning chip 4 → 5. | in force |
| D11 | `--profile` is a global `tasky.py` flag; only `flove` is defined. | in force |
| D12 | Specific questy questions are suggested when the shortlist is heavy, blocked or not easy; a survey offers 30 numbered options with ★ on #1, `Ref:` / `Affects:` and answer grammar `0` = all ★, `-` = skip. | in force |

### 11.2 Register, procedures and state

| ID | Decision | Status |
|---|---|---|
| D13 | Canonical policy stays in its owner doc (`development/AGENTS.md` PROC blocks); `milestones.json` owns only hitos/tasks and has **no** `procedures` key. | in force |
| D14 | PROC-07 sort: hito-level unlock rank, then the task's own `effort`, then stable ids; advisory only, loops warn, C6 exceptions recorded, never blocks. | in force |
| D15 | PROC-08 evidence is `kind: command\|anchor\|state` plus `value`; a bare "verified" is not evidence; there is no `test` field. | in force |
| D16 | Live tasks carry `owner` only; 1,455 original live tasks were updated and 21 earlier dependency edges reverted. | in force |
| D17 | Active window stays 30 tracker IDs with `size`, `order`, `reviewed`, `reviewedBy`. | in force |
| D18 | `.3c` / `.3b` / `.3` scaffold tasks are skipped by default; `--include-bookkeeping` opts back in. | in force |
| D19 | PROC-10 `choice_weight` is orthogonal to effort: `directo` 0, `ramificado` 1, `estructurante` 3 questions; `choice_override` + `choice_reason` allowed; a dependency is hard-registered only after the answer. | in force |
| D20 | State moves are automatic once an evidence pointer verifies; no git commit unless asked. | in force |
| D21 | `skills-02.2a` and `systems-10.2a` were delivered this session but left `pendiente`; no retroactive move. | in force |
| D22 | The register drift from 1,492 → 1,559 live tasks and 317 → 326 hitos was synced by rebuilding projections, not by editing `milestones.json` by hand. | in force |

### 11.3 Effort and naming

| ID | Decision | Status |
|---|---|---|
| D23 | No `1.5` exists in the work taxonomy. The first fallback (`very easy` = 1) was superseded by the five-level scale below. | superseded |
| D24 | Five-level ladder, canonical **English** values in data/code/docs: 1 `very easy` · 2 `easy` · 3 `medium` · 4 `hard` · 5 `very hard`. Spanish is UI-label only. | in force |
| D25 | 2,364 `effort` values migrated in place (2,038 `fácil`→`easy`, 315 `difícil`→`hard`, 11 `muy difícil`→`very hard`). Live: 1,235 easy · 315 hard · 9 very hard · 0 very easy · 0 medium. Archive: 803 easy · 2 very hard. | in force |
| D26 | No task is assigned to `very easy` or `medium` without an owner-supplied id list or rule; effort stays orthogonal to PROC-10's choice class. | in force, open fill |
| D27 | `tasky.py easy` counts the very-easy pool and proposes 10-task batches; `next --do` queues `directo + very easy/easy`. | in force |
| D28 | Colour is effort, not state: `easy` green · `hard` yellow · `very hard` red; levels 1 and 3 have no chip colour until tasks carry them; `✓` means `hecha`. | in force |
| D29 | The Work `taskcat` filter is labelled `Esfuerzo / Effort`, not `Estado / State` — it filters effort, not task state. | in force |
| D30 | Two canonical axes only: `effort` and `stage`. `level` / `degree` / `nivel` / `grado` are display synonyms of effort, `phase` / `fase` of stage. Frontend 1–5 is a view of core stages, not a third effort scale. | in force |
| D31 | Historical `levels-*` ids and `#*-levels` anchors are identifiers and stay; do not mint new ones. Levels get no topic page — they are core stages already in `contract.md`, `standards/frontend/frontend.md` §13.18 and `standards/mds.md`; `#data-ux` stays as a view with no file. | in force |

### 11.4 Target tree and content ownership

| ID | Decision | Status |
|---|---|---|
| D32 | 20 stable pages are flat files `development/standards/<topic>.md` — no trunk folder, no compound slug, no hub. | in force |
| D33 | Child plans are `plans/<category>/<topic>.md` — folder names the category, filename is the **same topic keyword** as the stable page. `subsection` and `topic` are the same kind of keyword; the two are sibling pages across categories, not a parent/child pair. No `<topic>` level is nested under a subsection folder. `work/` files are flat too. | in force |
| D34 | `docs/development/` keeps only `INDEX.md`, `AGENTS.md`, `contract.md`, `wiki.json`, `plans/`, `work/` and `archive/`. | in force |
| D35 | `metaphysics/`, `psychosocial/` and the rest of the whole flatten under `docs/` as peers of `development/`; not created now. | in force |
| D36 | No `tools/standards/`; `standards/scripts/` moves into `tools/dev/` with every other script. | in force |
| D37 | `archive/old/` is an opaque verbatim snapshot — no live links, excluded from `wiki.json` and gates. The earlier `archive/ported/` copy idea is dropped. | in force |
| D38 | `plans/debates/` is a raw staging tray with `status: draft`, never a permanent owner; promotion = `git mv` to `plans/<category>/<topic>.md` + port facts + add a `supersedes` entry. | in force |
| D39 | `backend.md`, `adoption.md` and `worldview.md` are deleted outright after their facts land; every ref repointed; no hub stubs. | in force |
| D40 | The two AGENTS files merge into one with no pointer stub; the ten PROC blocks stay contiguous for `procedures_source.py`. | in force |
| D41 | `standards/frontend/`, `puzzy/`, `risaliberada/`, `skills/` and `workflow/` stay physically in place. | in force |
| D42 | `contract.md` moves to `docs/development/contract.md`; `apps/` is ported then archived verbatim in `archive/old/apps/`. | in force |

### 11.5 Automation, gates and open items

| ID | Decision | Status |
|---|---|---|
| D43 | A generated `wiki-resolve.py` rewrites 747 task owners, 139 hito sources, 55 standards URLs, 206 gaps, 11 new-ticket sources and 1 docs pointer; originals preserved as `origin` / `migrated_from`. Never hand-edit a pointer. | in force |
| D44 | `common.json` and the `WORK-DATA` block stay generated; rebuild, never hand-edit. | in force |
| D45 | Resolver order: exact path → anchored path → `supersedes` chain (max depth 8) → `labels` → error. Cycles are a gate error; never silently fall back to `archive/`. | in force |
| D46 | `tasky.py show` prints PROC quick table + row + canonical page `CONTEXT` only (target ~1–1.5k tokens); `weight`, `options`, `next`, `easy`, `procedure` output unchanged. | in force |
| D47 | The generated `wiki` field on Work rows is additive to PROC-10's `choice`, never a replacement. | in force |
| D48 | Baseline gates were green before this pass: four register gates OK, `check-skills.py` 0 errors / 2 pre-existing warnings, `tasky` skill body 992 words (cap 1000). Projections rebuilt after every AGENTS edit. | in force |
| D49 | Populate `very easy` and `medium` (D26 / §7.8): leave at 0 with `next --do` covering the 142 ready `directo + easy` tasks. | in force — G11A (owner accepted all ★, 2026-11-21) |
| D50 | Retroactive `hecha` moves for `skills-02.2a` / `systems-10.2a` would need the archive move plus one replacement patch — not done in the skill-change scope. | in force — G12A (owner accepted all ★, 2026-11-21) |

### 11.6 Additions from the coverage audit

| ID | Decision | Status |
|---|---|---|
| D51 | Unprefixed `standards/<topic>.md` in every table means `development/standards/<topic>.md`, not a path under `docs/`. | in force |
| D52 | Source filenames are the exact date-prefixed ones on disk; there is no `refs/` directory and no `browsy/wizy.md`. The verbatim archive rule forbids re-homing a source to invent such a path. | in force |
| D53 | §8's per-heading ledger wins over §2's summary when the two destination sets disagree; §12 carries the complete file-level matrix. | in force — G3A |
| D54 | Retired-note target is `archive/old/archive.md`, not `archive/old/debates/archive.md`. | in force — G5A |
| D55 | AGENTS merge: work-style rules → §1, Authority → §2, ten PROC blocks → §3 contiguous; §4.2 and §10.5 agree. | in force — G6A |
| D56 | Generated PORT-LEDGER lives outside archive so the manifest gate can read it; archive stays opaque. | in force — G7A |
| D57 | File counts corrected from disk: `AGENTS.md` 209 lines, `standards/AGENTS.md` 85, `adoption.md` 6 `##`, `backend.md` 16 `##`, `onboarding-copy.md` 32 `##` (30 app blocks + `Shared shape` + `Catalog-only apps`). | in force |
| D58 | Owner accepted **all ★ defaults** on 2026-11-21. G1–G13 are closed with option A each: port 3 plans + archive `.bak`; one plan per topic; §8 authoritative; add storage row; flat archive path; AGENTS §1/§2/§3; PORT-LEDGER outside archive; many-to-one manifest; container/range heading rows + archive exemption; 17 rows + SD crosswalk; effort tiers stay 0; two tasks stay `pendiente`; all 13 non-MD verbatim. Options B/C are rejected, not pending. | in force |
| D59 | Four D24 leftovers fixed on 2026-11-21: static `EFFORT_RANK` / `taskClass` JS in `index.html`, PROC-10 note `fácil`→`easy` in AGENTS §3.4, and the `standards/README.md` filter description. Projections rebuilt and four gates green. | in force |
| D60 | Follow-up audit found 24 action groups outside the original scope: 4 fixed under D59, 20 recorded in §14 as N1–N16 with ★ defaults. | in force |
| D61 | Owner chose N1A, N5A, N7A, N10A, N11B, N14A, N16A on 2026-11-21; all applied. `apps{}` + parked sync removed and EXP08 closed; D1 plan merged into `risaliberada/plan-v2.md` Parte C with risa-project owner line and project copy deleted; four `contract.md` refs repointed; `development/media/…` declared canonical (project risa logo copy deleted, i18n ledger repointed); four empty dirs removed; two chapter generators retired with their updaty steps. N2–N4, N6, N8–N9, N12–N13, N15 remain open. | in force |
| D62 | Closing EXP08 removes a resolved row from the Work projection: `EXPECTED_ROWS` and its three mirrors drop 76 → 75, canonical total 425 → 424. `vocabulary.html` still embeds the retired generator steps (N9 not chosen); `backend.md` line 526 still names the retired depth generator and disappears with that chapter at cutover. | in force |

## 12. Complete old → new movement matrix

This is the execution-level inventory. **Every path in this section is exact on
disk as of 2026-11-21.** Shorthand used throughout the plan:

- `standards/<topic>.md` **always means** `development/standards/<topic>.md`
  (the 20 flat stable pages, §10.2 / D32) — never `docs/development/standards/…`.
- `plans/<category>/<topic>.md` means
  `docs/development/plans/<category>/<topic>.md`, where `<topic>` is the same
  keyword as the stable sibling page (D33).
- `work/<file>.md` means `docs/development/work/<file>.md` (flat).
- `archive/old/…` means `docs/development/archive/old/…` (verbatim, opaque).
- Source paths below are relative to `development/standards/` unless they start
  with `development/` or `docs/`.

### 12.1 Coverage of the old tree

| Old area | Files | Mapped in §8 | Mapped here (§12) | Archive only |
|---|---|---|---|---|
| `debates/` root MD | 14 | 10 | 14 | 4 |
| `debates/browsy/` MD | 6 | 5 | 6 | 0 |
| `debates/browsy/pre-build/` MD | 12 | 12 | 12 | 1 (closed log) |
| `debates/plans/` MD | 11 | 7 | 11 | 1 (`conflicts.md` is a live target) |
| `debates/proposals/` MD | 2 | 1 | 2 | 0 |
| `debates/bridges/`, `others/`, `research/`, `reviews/` MD | 4 | 4 | 4 | 0 |
| `debates/archive/making-of/superpowers/specs/` MD | 12 | 0 | 12 (archive only) | 12 |
| `debates/` HTML / `.bak` / JSON | 13 | 0 | 13 | 13 |
| `apps/` MD | 2 | 2 | 2 | 2 (after port) |
| root chapters + work-style AGENTS | 5 | 5 | 5 | 5 (after port) |

Total: **61 MD in `debates/`** + 2 in `apps/` + 5 root files = 68 MD, plus 13
non-MD. §8 enumerates headings for 12 sources; §12 adds the missing file-level
rows. Where §8 and §2 disagree, §8's heading ledger is the working default
(gap G3 in §13).

### 12.2 Root chapters (ported, then deleted)

| Source | Stable page(s) / target | What moves | Plan sibling |
|---|---|---|---|
| `backend.md` (16 `##` chapters) | `standards/plan.md`, `systems.md`, `mds.md`, `schemas.md`, `index.md`, `apps.md`, `storage.md`, `scripts.md`, `mynet.md`, `channels.md` | All 15 content chapters; `## In this file` is a TOC → `docs/development/INDEX.md` | `plans/backend/{scripts,systems,mynet,storage}.md` |
| `adoption.md` (6 `##`) | `standards/systems.md`, `storage.md`, `experience.md`, `apps.md`, `scripts.md` | Adoption stages, storage trade-offs, experience tiers, app rollout, script inventory | mapped by owning topic |
| `worldview.md` (2 `##`) | `docs/development/contract.md`, `docs/development/INDEX.md`, owning topic pages | Values → contract, the "why + map" → INDEX, facts → owners | none |
| `contract.md` | `docs/development/contract.md` (whole file, one move) | Values + the floor; no chapter split, no `§2` (the file has `Values and the floor` / `The floor`) | none |
| `standards/AGENTS.md` (85 lines, rules 1–13) | merged into `docs/development/AGENTS.md` | 13 work-style rules → §1; Authority → §2; the ten PROC blocks → §3, contiguous; retired notes → `archive/old/archive.md#home-directory-layout` | none; 33 refs repointed |

### 12.3 `debates/` root MD (14 — `a11y-report.md` is in §12.6)

| Source | Destination | What moves |
|---|---|---|
| `INDEX.md` | `docs/development/INDEX.md` | closed list + compact map; drop 33 Historical rows and stale counts |
| `pendings.md` | `work/pendings.md` | unchanged parser syntax |
| `task-set-plan.md`, `hitos-audit.md` | `work/measures.md` (live metrics); `#conflict-register` → `plans/conflicts.md` | metrics + conflict register link |
| `roadmap-2026-06.md` | `standards/plan.md` | roadmap map |
| `proposals.md` | `standards/plan.md` | stage aliases |
| `questy-proposals.md` | `standards/skills.md`, `standards/flows.md`, `standards/mds.md`; scripts → `standards/skills/questy/` | decisions + reusable question shape |
| `standards.md` (root) | `standards/skills.md` / `flows.md` / `mds.md` | decisions (per-source split pending, gap G3) |
| `UseCase-adv.md` | `standards/flows.md` | use-case advice |
| `agents.md` | `archive/old/agents.md` | already canonical in AGENTS/chapters |
| `skills-library.md` | `archive/old/skills-library.md` | already canonical in `standards/skills/` |
| `archive.md` | `archive/old/archive.md` | retired note |
| `a11y-development-index.md` | `archive/old/a11y-development-index.md` | superseded by generated report |

### 12.4 `debates/browsy/` (6) and `browsy/pre-build/` (12)

| Source | Destination | What moves |
|---|---|---|
| `browsy/spec.md` | `standards/mynet.md`, `systems.md`, `schemas.md`, `apps.md`, `experience.md`, `plan.md`, `flows.md`, `work.md` | BSP requirements, phases 0–8, acceptance tests, §5 old-plan reconciliation |
| `browsy/browsy-questions.md` | `standards/mynet.md` (live questions A–L under `## Live questions — 2026-11-17 …`), `experience.md` (model labels), `work.md`, `mds.md`, `systems.md`, `flows.md`, `channels.md`, `docs.md`, `schemas.md`; conflicts → `plans/conflicts.md` | 244-answer historical log stays in archive |
| `browsy/rationale.md` | `standards/mynet.md`, `docs.md`, `plan.md`, `systems.md`, `schemas.md`, `flows.md`, `json.md`, `mds.md`, `work.md`; conflicts → `plans/conflicts.md` | privacy-first mesh, P/L/S classes, threat model |
| `browsy/README.md`, `TESTING.md`, `port-nety.md` | `standards/systems.md`, `mynet.md` | risk matrix, retained seams |
| `browsy/pre-build/01-mvp.md` | `standards/mynet.md` | single-device MVP |
| `browsy/pre-build/02-authy-levels.md` | `standards/mynet.md` | SelfAuth vs risa/nonce+DM verified Telegram, O11=D |
| `browsy/pre-build/03-schemas.md` | `standards/schemas.md` | `flove:authy/1` key vs `flove-authy/1` id, migration |
| `browsy/pre-build/04-myfamily-profile.md` | `standards/schemas.md`, `mynet.md` | 7 areas × 5 replies → 5 percentages, P-by-default |
| `browsy/pre-build/05-native-host.md` | `standards/systems.md` | Rust host, WebSocket+JSON |
| `browsy/pre-build/06-bridge-threat-model.md` | `standards/systems.md` | page/bridge boundary, allowlist, mitigations |
| `browsy/pre-build/07-lineage-tests.md` | `standards/mynet.md` | invite lineage, fixtures |
| `browsy/pre-build/08-model-labels.md` | `standards/experience.md` | "Else" chip wording |
| `browsy/pre-build/09-consult-agreements.md` | `standards/mynet.md` | signed revocable consult agreements |
| `browsy/pre-build/11-ui-pending.md` | `standards/experience.md` | pending UI surfaces |
| `browsy/pre-build/README.md` | `standards/plan.md`, `work.md`, `mds.md` | index and section links |
| `browsy/pre-build/open-issues.md` | `archive/old/…/open-issues.md` | closed log, no authority |

### 12.5 `debates/plans/` (11) — all date-prefixed names are exact

| Source | Stable page(s) / target | Child plan sibling |
|---|---|---|
| `plans/2026-11-21-app-database-stages.md` | `standards/plan.md`, `work.md`, `json.md`, `apps.md`, `storage.md`, `mynet.md` | `plans/backend/storage.md` |
| `plans/2026-11-17-appy-authy-mynet.md` | `standards/mynet.md`, `systems.md`, `schemas.md`, `apps.md`, `experience.md`, `storage.md`, `work.md`, `plan.md` | `plans/backend/mynet.md` |
| `plans/2026-11-20-appy-dashboard-redesign.md` | `standards/apps.md`, `experience.md`, `plan.md`, `json.md` | `plans/frontend/apps.md` |
| `plans/central-backend.md` | `standards/systems.md`, `storage.md`, `mynet.md`, `mds.md`, `experience.md`; conflicts → `plans/conflicts.md` | `plans/backend/systems.md` |
| `plans/puzzy.md` | `standards/apps.md`, `work.md`; conflicts → `plans/conflicts.md` | `plans/frontend/apps.md` |
| `plans/2026-06-18-nety-frontend-build.md` **(newly mapped)** | `standards/apps.md` (built UI), `experience.md` (tabs, vocabulary), `scripts.md` (deferred backend wiring), `plan.md` (phase status) | `plans/frontend/apps.md` |
| `plans/2026-06-18-nety-frontend-build.md.bak-orig` **(newly mapped)** | archive verbatim; if ported, same four pages (11-task build order, deferred/out-of-scope) | same as parent |
| `plans/2026-11-14-app-tier-planned.md` **(newly mapped)** | `standards/apps.md` (closed tier status, same rule as `frontend-tiers.md`); conflicts → `plans/conflicts.md` | `plans/frontend/apps.md` |
| `plans/2026-11-19-authy-open-questions.md` **(newly mapped)** | `standards/work.md` (open questions), link from `standards/mynet.md`; no new plan unless promoted | none |
| `plans/conflicts.md` | **live target** → `docs/development/plans/conflicts.md` | is itself the target |
| `plans/index.md` | `standards/plan.md` | none |
| `plans/standards.md` (SD01–SD19) | `work/pendings.md` `VARIOUS_Q34–50`; 46 task owners repointed | 19 decisions into 17 existing rows (gap G10) |

### 12.6 Other `debates/` folders

| Source | Destination | What moves |
|---|---|---|
| `proposals/frontend-tiers.md` | `standards/apps.md` | closed tier status |
| `proposals/frontend-wizy.md` (136 lines) | `standards/apps.md`, `flows.md`, `work.md`, `experience.md` | operating areas, custom magic, key fields, influence degrees; mark draft. **There is no `browsy/wizy.md` on disk** — the old plan's claim was wrong, and the verbatim-archive rule forbids re-homing it |
| `bridges/oasis.md` | `standards/mynet.md`, `systems.md`, `schemas.md`, `work.md`, `mds.md` | Oasis/SSB adaptation, publish mapping |
| `a11y-report.md` | `standards/accessibility.md` | current generated summary; raw file stays in archive; no child plan |
| `others/flove-libs-insights.md` | `standards/mds.md` + `docs/development/contract.md` (values/floor) | library insights |
| `research/vr_interfaces.md` | `standards/experience.md` | abandoned note |
| `reviews/2026-07-25-browsy-fastapi-libsql-performance-review.md` | `standards/systems.md` | architecture notes |

### 12.7 Archive-only MD (16 files, no live port)

`agents.md`, `skills-library.md`, `archive.md`, `a11y-development-index.md`
(§12.3) and the 12 files in `archive/making-of/superpowers/specs/`:

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

All land at `archive/old/…` with their relative paths intact. Their facts are
already canonical in the standards chapters; no second copy, no hub stub.

### 12.8 Non-MD (13 files)

| Source | Destination |
|---|---|
| `flove-decisions-interview.html` | `archive/old/flove-decisions-interview.html` |
| `ephemerall/ephemeral-glider.html`, `ephemerall.html`, `ephemerall-logos.html`, `glider-balls-set.html`, `strategicpersistence.html` | `archive/old/ephemerall/…` verbatim |
| `archive/making-of/making-of.html`, `skills-applied.html` | `archive/old/archive/making-of/…` verbatim |
| `milestones.json.bak-2026-11-20`, `milestones.json.bak-2026-11-20-prequeue` | `archive/old/…` verbatim; not imported into the register |
| `common.json`, `milestones.json` | **not archived** — canonical register + generated projection; stay live |

### 12.9 `standards/apps/` (2 MD)

| Source | Destination |
|---|---|
| `apps/README.md` (172 lines) | `standards/scripts.md`, `apps.md`, `plan.md`, `skills.md`; then the whole file at `archive/old/apps/README.md` |
| `apps/onboarding-copy.md` (32 `##` = 30 app blocks + `Shared shape` + `Catalog-only apps`) | shared shape + ten-step pattern → `standards/experience.md`; 30 app blocks as one table in `plans/frontend/experience.md`, linked from `experience.md` and `language.md`; then `archive/old/apps/onboarding-copy.md` |

### 12.10 Target inventory after the move

**20 flat stable pages** in `development/standards/`: `plan`, `work`, `scripts`,
`systems`, `mynet`, `storage`, `apps`, `accessibility`, `experience`, `models`,
`skills`, `flows`, `mds`, `index`, `json`, `schemas`, `docs`, `feedback`,
`language`, `channels`.

**Plan siblings** (`plans/<category>/<topic>.md`, same keyword):
`docs/{plan,work}.md` · `backend/{scripts,systems,mynet,storage}.md` ·
`frontend/{apps,accessibility,experience}.md` · `ai/{models,skills,flows}.md` ·
`data/{mds,index,json,schemas}.md` · `community/{docs,feedback,language,channels}.md`
plus `plans/index.md`, `plans/conflicts.md`, `plans/debates/README.md`.

**Flat `work/` files:** `pendings.md`, `measures.md`, plus any generated summaries.
**Root of `docs/development/`:** `INDEX.md`, `AGENTS.md`, `contract.md`,
`wiki.json`, and `archive/old/`.

## 13. Gap solutions — choose one per gap

Each gap has A/B/C options. ★ marked the recommended default; every ★ states
its reason and its con on the same line. **Owner chose all ★ (option A) on
2026-11-21** — G1–G13 are closed and recorded as D58 in the decision ledger.
Nothing is executed by this choice: the cutover still needs its own go-ahead.

**G1 — Three unmapped plans + one `.bak-orig`.** Sources: `plans/2026-06-18-nety-frontend-build.md`, `2026-11-14-app-tier-planned.md`, `2026-11-19-authy-open-questions.md`, `2026-06-18-nety-frontend-build.md.bak-orig`.
- ★ **A: Port the three MDs as mapped in §12.5; `.bak-orig` archive only.** Reason: matches the existing rule that built UI → `apps.md`, closed tiers → `apps.md`, open questions → `work.md`; con: adds one more source to 30 app-block and open-question ledgers.
- **B: Archive all four with no port.** Reason: they are dated build logs; con: loses the vocabulary-drift and closed-tier facts the plan already ports from similar files.
- **C: Port only `2026-06-18-nety-frontend-build.md`.** Reason: it is the only one with a full chapter list; con: leaves two silent gaps.

**G2 — Six child-plan collisions under D33** (`frontend/apps`, `docs/plan`, `backend/mynet`, `backend/systems`, `data/schemas`, `frontend/experience` each have 3–5 old sources).
- ★ **A: One `<category>/<topic>.md` per topic; each old source becomes a dated `##` section inside it.** Reason: preserves D33's sibling-page rule and one-owner policy; con: those six plan files get long.
- **B: Allow qualifiers in the filename** (`plans/backend/mynet-authy.md`). Reason: keeps files small; con: breaks "topic keyword = stable sibling" and reintroduces compound slugs.
- **C: Keep only one source as the plan; the others port facts directly to the stable page.** Reason: fewest files; con: loses the raw plan lineage that `supersedes` records.

**G3 — §2 vs §8 destination drift on 8 sources** (e.g. `storage` in §2 but no storage chapter in §8.1; `experience`/`plan`/`flows` in §8 only).
- ★ **A: §8 heading ledger is authoritative; §2 is a summary and gets a pointer.** Reason: §8 is per-heading and checked; con: §2 needs a rewrite to stop contradicting it.
- **B: Use the union of both destination sets.** Reason: nothing is lost; con: facts get written in two pages, breaking one-fact-one-home.
- **C: §2 is authoritative.** Reason: shorter; con: §8's 100+ heading rows become advisory dead weight.

**G4 — `standards/storage.md` has no §8.1 chapter row** although §2 and §10.1 give it a child plan.
- ★ **A: Add a `storage` chapter row to §8.1 from `2026-11-21-app-database-stages.md` §4.8.3 (the two cap increases).** Reason: gives the page its own fact; con: needs a fresh read of that section at execution.
- **B: Drop `storage` from §2 and delete `plans/backend/storage.md`.** Reason: fewer empty files; con: stage-model facts then sit in `plan.md`/`json.md` only.
- **C: Keep the page as a link-only redirect to `plan.md`.** Reason: no content duplication; con: a stable page with no content is a hub stub, which D32 forbids.

**G5 — Old `archive/old/debates/archive.md` path.** Audit found the retired note pointed one folder too deep; I have applied `archive/old/archive.md`.
- ★ **A: Keep the applied fix.** Reason: the old tree is copied verbatim with `archive/` at its root, so `debates/archive.md` lands flat; con: any existing link using the deeper path must be repointed (already in §4.2/§10.5).
- **B: Preserve the deep path** by nesting the old tree one level under `archive/old/debates/`. Reason: no link edits; con: contradicts the agreed target tree and every other `archive/old/…` row.

**G6 — AGENTS merge numbering.** Plan currently says work-style → §1, Authority → §2, PROCs → §3 (§4.2 now agrees).
- ★ **A: Keep that.** Reason: the work-style rules read first and the contiguous PROC block is still machine-parsed by heading text; con: all `AGENTS.md#§…` deep links and the `Standard:` URLs need a numbering sweep.
- **B: Append the 13 rules as a new §8 and keep Authority §1 / PROCs §2.** Reason: zero link churn; con: execution policy is no longer the first thing an agent reads.

**G7 — Generated PORT-LEDGER inside `archive/` but §8.14 says `check-docs-manifest.py` checks it, while D37 excludes archive from gates.**
- ★ **A: Write the generated ledger to `docs/development/PORT-LEDGER.md` (outside archive) and check that.** Reason: gates only read live paths; con: one extra generated file at the wiki root.
- **B: Keep it in archive and add a single explicit gate exception.** Reason: no new root file; con: weakens the "archive is opaque" rule.
- **C: Drop the generated ledger; §12 of this plan is the record.** Reason: simplest; con: no machine check that every source was ported.

**G8 — `check-docs-manifest.py` "one stable page per child plan" vs six collision clusters (G2).**
- ★ **A: Allow one stable page to reference several child plans, but each child plan names exactly one stable page.** Reason: matches real lineage; con: the manifest must count many-to-one.
- **B: Force one child plan per stable page** (with G2 option A). Reason: exists already in D33; con: needs the six merged files.
- **C: Drop the manifest assertion.** Reason: no gate work; con: orphan plans become invisible.

**G9 — Heading-level omissions in §8** (`backend.md` `## In this file`, `browsy-questions.md` live-questions container, spec Phases 0–8 folded, 17 pre-build pendings folded, 16 archive-only files with no heading ledger).
- ★ **A: Add container rows and range rows; archive-only files explicitly exempt with a one-line reason each.** Reason: keeps "all headings" honest without 200 new rows; con: ranges are less precise than individual headings.
- **B: Full heading ledger for all 61 MDs.** Reason: maximum specificity; con: plan grows by several hundred rows.
- **C: Change the §8 claim to "all live headings" and drop archive-only detail.** Reason: smallest edit; con: archive-only files lose their audit trail.

**G10 — `plans/standards.md` SD01–SD19 → `VARIOUS_Q34–50` mismatch** (19 decisions into 17 rows, no `SD01` string in `pendings.md`).
- ★ **A: Keep the 17 rows as destinations and add an `SD → VARIOUS` crosswalk table in `work/pendings.md`.** Reason: the parser input stays unchanged; con: one small generated-looking table to maintain by hand.
- **B: Expand to 19 rows.** Reason: 1:1 mapping; con: changes parser input and may collide with existing IDs.
- **C: Add the 19 `SD` decisions as new `VARIOUS` entries.** Reason: no crosswalk; con: `VARIOUS_Q34–50` is no longer 17 rows and 46 task owners need new targets.

**G11 — Empty `very easy` and `medium` effort tiers (D49).**
- ★ **A: Leave both at 0; `next --do` covers the 142 ready `directo + easy` tasks.** Reason: no invented classification; con: two filter chips stay empty.
- **B: You supply an id list for each tier.** Reason: real data, no guesswork; con: needs your input before cutover.
- **C: Apply a rule** (e.g. `directo` + one-step + no dependencies → `very easy`; `ramificado` + 3–9 fan-out → `medium`). Reason: fills both tiers automatically; con: reclassifies tasks without a per-task judgement.

**G12 — Retroactive `hecha` moves for `skills-02.2a` / `systems-10.2a` (D50).**
- ★ **A: Leave `pendiente`; no retroactive move.** Reason: the done-flow needs archive move + replacement patch; con: two delivered items still read as open.
- **B: Do the full move now** (archive + one replacement patch per task). Reason: register matches reality; con: touches canonical data and requires a gate rerun.
- **C: Add only an evidence pointer, keep state `pendiente`.** Reason: documents delivery without a state move; con: state remains misleading.

**G13 — Three `.bak` files and 8 HTML files.**
- ★ **A: Copy all 13 verbatim to `archive/old/…`, no live links.** Reason: D37 says opaque snapshot; con: ~small archive size cost.
- **B: Drop the `.bak` files, keep only HTML.** Reason: backups are redundant with git history; con: loses the pre-queue register snapshots.
- **C: Import the `.bak` register snapshots into `archive/old/` and index them.** Reason: searchable history; con: creates a third copy of register data.

## 14. Follow-up audit — pending migrations outside the original scope

The read-only audit of 2026-11-21 found **24 action groups** beyond the tree
mapped in §12. Four were unfinished applications of D24 (canonical English
effort) and are **already fixed** (§14.1). Of the twenty recorded here, the
owner chose and I applied **N1A, N5A, N7A, N10A, N11B, N14A and N16A** on
2026-11-21; those are marked in §14.3 and in D61. The other nine remain open.

### 14.1 Applied immediately under D24 (no new decision needed)

| Exact path | Fix applied |
|---|---|
| `development/index.html:97986` | `EFFORT_RANK` keys → `very easy` · `easy` · `medium` · `hard` · `very hard` (0–4); unknown default rank 5 |
| `development/index.html:97999` | `taskClass()` → `vdhard` / `hard` / `easy` / `''` for levels 5/4/2 and the two unpopulated levels 1/3 |
| `development/AGENTS.md:147` | PROC-10 reading note `fácil` → `easy` (§3.4, not a PROC block, so byte-identical PROC text is preserved) |
| `development/standards/README.md:36–39` | filter documented as `Esfuerzo / Effort` with six chips `archived · very easy · easy · medium · hard · very hard` |

Projections rebuilt; four register gates green; `check-skills.py` 0 errors /
2 pre-existing warnings. Recorded as D59.

### 14.2 The twenty open groups

| # | Exact path(s) | Pending action | Scope |
|---|---|---|---|
| N1 | `tools/pending/sync-puzzy.py:5`, `debates/pendings.md:201` | Parked puzzy registry sync / EXP08: decide whether `tools/puzzy.json apps{}` is generated, live from routing, or dropped; wire or delete the script | outside |
| N2 | `debates/pendings.md:107` | `QUESTYDEMO01` clean `questy-html-flove` demo — not started; schedule or close separately from the already-done thin caller | outside |
| N3 | `debates/pendings.md:182,184`, `standards/frontend/routing-colours-db.md` | `RC01` extra colours + `RDB01` future DB: keep as Work items or retire explicitly; repoint after cutover | outside |
| N4 | `development/scripts/jsony_check.py:732`, `standards/skills/jsony/SKILL.md:148` | `TODO` category placeholders: convert to a tracked decision or document as intentional | outside |
| N5 | `projects/liberada/risa/plans/PLAN-V2-D1.md:22,139` | Project-local v2-D1 follow-ups need an owner; not docs-migration work | outside |
| N6 | `development/blog/build-blog.sh:47`, `scripts/build-puzzy-demo.py:9–11,63`, `scripts/check-distro.sh:6–8,237`, `scripts/check-portrait-protocol.py:8`, `scripts/inject-conformance.py:9–10`, `scripts/narrate.sh:5–7`, `standards/scripts/check-skills.py:513` | Repoint script examples and warning text to `tools/dev/…` when §10.6 lands | cutover follow-up |
| N7 | `standards/contract.md:59,71,74,87` | Repoint refs to `adoption.md`, `worldview.md`, `apps/README.md` before moving the file to `docs/development/contract.md` | cutover blocker |
| N8 | `tools/puzzy.json:938,1046` vs `tools/routing.json:8377,8495` | `apps{}` snapshot stale (`vizy.url`, `vizy2.url` drift); `--check` reports stale | outside |
| N9 | `standards/vocabulary.html:279,285–289` | Generated index embeds old `development/scripts/…` paths and the deleted `worldview.md` / `backend.md` chapters; regenerate after N6 | cutover follow-up |
| N10 | `media/apps/logos/ephemerall/` ↔ `debates/ephemerall/` (3 files), `media/apps/logos/risa/risa-logos.html` ↔ `projects/liberada/risa/media/logos/risa-logos.html` | Exact duplicate assets (md5 verified); declare one canonical home for each pair | outside |
| N11 | `standards/risaliberada/plan-v2.md` ↔ `projects/liberada/risa/plans/PLAN-V2-D1.md` | Two active risa-v2 plans; add explicit status/cross-link and decide which owns Work pointers | outside |
| N12 | Skills `backy:9,31–36,62–63`, `validaty:10`, `narraty:40,71,84`, `skilly:57,67`, `translaty:99` + `audit.md:11,14–20,36–37`, `texty:10,59`, `updaty:40–51,72` + `heavy.md:20–24,56`, `questy-tasky-flove:34,37,38` | Stale script/chapter/pendings refs in skill bodies; rewrite queue for `tools/dev/…`, topic pages, `work/pendings.md` | cutover follow-up |
| N13 | `skills/brandy/SKILL.md` (1156 words), `skills/optimizy/SKILL.md` (1095 words) | Two pre-existing word-cap warnings; move detail to sidecars or formally accept | outside |
| N14 | `apps/sys/browsy/app/entrypoints/popup`, `app/tests/e2e`, `app/tests/unit`, `skills/questy/packs` | Four empty first-party directories; delete or add intentional placeholders | outside |
| N15 | `development/addons/legacy/nety.html`, `sety.html`, `projects/liberada/_nav-demo/old-index.html` | Legacy/orphan HTML with almost no live refs; archive/delete or mark intentional, regenerate `tools/i18n-ledger.json` | outside |
| N16 | `scripts/build-depth-md.py:5,8–9,20,65`, `scripts/build-whole-md.py:2,5,8–9,20,156` | Both write to `backend.md` / `worldview.md`, which §10.3 deletes; retire or repoint to `mds.md` / `index.md` + `contract.md` | cutover blocker |

Clean subchecks (no action): canonical effort data in `milestones.json` and
`common.json`; `tools/jsony-pending.md` critical 0 / advisory 0;
`build-routing-index.py --check` ok (1288 fields); all 21 skills have matching
frontmatter and registry entries; all `Standard:` URLs resolve locally; no
retired skill names in current skill docs. `perfil fácil` in
`build-work-tracker.py:95–98` is a bilingual task title, not an effort value —
left as a proper name.

### 14.3 Choose one per follow-up

**N1 puzzy sync / EXP08**
- `N1A` **[CHOSEN + APPLIED 2026-11-21]** ★ Drop `apps{}` from `puzzy.json` and delete `sync-puzzy.py`; close EXP08 as superseded by routing.
- `N1B` Wire the parked sync into the JSON gates and keep `apps{}`.
- `N1C` Leave parked and carry EXP08 into `work/pendings.md` unchanged.

**N2 questy-html demo**
- `N2A` ★ Keep `QUESTYDEMO01` as a Work item; it is unrelated to the thin caller.
- `N2B` Schedule it now as its own task.
- `N2C` Close it as not needed.

**N3 colours / DB pendings**
- `N3A` ★ Keep `RC01` / `RDB01` as Work items; repoint their owner refs after cutover.
- `N3B` Retire both and delete the pending note.
- `N3C` Port the note into the new `plans/frontend/…` file as-is.

**N4 TODO categories**
- `N4A` ★ Keep the placeholders but add a one-line comment saying the category is an intentional decision slot.
- `N4B` Convert to a real tracked Work decision now.
- `N4C` Replace with a concrete category name guessed from context.

**N5 risa v2-D1 follow-ups**
- `N5A` **[CHOSEN + APPLIED with N11merge (owner line in merged plan)]** ★ Leave in the project plan; add an owner line.
- `N5B` Promote into Work.
- `N5C` Close as obsolete.

**N6 script-path examples**
- `N6A` ★ Repoint all seven files to `tools/dev/…` inside the §10.6 move.
- `N6B` Leave examples pointing at the old path and add a compatibility shim.
- `N6C` Ignore; examples are illustrative only.

**N7 contract.md refs**
- `N7A` **[CHOSEN + APPLIED 2026-11-21]** ★ Repoint the four refs to owning topic pages before the move (cutover blocker).
- `N7B` Move the file first and fix refs after.
- `N7C` Keep redirect stubs for the three deleted chapters.

**N8 puzzy.json drift**
- `N8A` ★ Regenerate `apps{}` from `routing.json` and add a `--check` to the gate.
- `N8B` Delete `apps{}` (ties to N1A).
- `N8C` Leave stale and document as a snapshot.

**N9 vocabulary.html**
- `N9A` ★ Regenerate after N6 and N12, and add it to the cutover checklist.
- `N9B` Delete the generated file and link to the standards index instead.
- `N9C` Leave stale until a later release.

**N10 duplicate assets**
- `N10A` **[CHOSEN + APPLIED 2026-11-21]** ★ Keep `development/media/…` as the single live home; leave the `debates/` copies only inside `archive/old/`.
- `N10B` Keep the `projects/liberada/risa/media/` copy as canonical instead.
- `N10C` Leave both copies and add a sync script.

**N11 two risa-v2 plans**
- `N11A` ★ Keep both, add a cross-link: `plan-v2.md` = design, `PLAN-V2-D1.md` = active branch; Work points to D1.
- `N11B` **[CHOSEN + APPLIED 2026-11-21]** Merge D1 into `plan-v2.md` and delete the project copy.
- `N11C` Keep only the project plan.

**N12 skill-body refs**
- `N12A` ★ Add the ten listed files to the skill rewrite queue, repointing to `tools/dev/…`, topic pages and `work/pendings.md`.
- `N12B` Fix only the broken chapter links; leave script examples.
- `N12C` Defer to a separate skills-only pass.

**N13 word-cap warnings**
- `N13A` ★ Keep the two warnings formally accepted in D48; no change now.
- `N13B` Move detail into sidecars and reach 0 warnings.
- `N13C` Trim the bodies in place.

**N14 empty directories**
- `N14A` **[CHOSEN + APPLIED 2026-11-21]** ★ Delete all four if git does not track them; otherwise add a short `README.md` placeholder.
- `N14B` Keep them as intentional scaffolding with placeholders.
- `N14C` Leave as-is (git ignores empty dirs anyway).

**N15 legacy HTML**
- `N15A` ★ Mark the three files as intentional offline references and regenerate `i18n-ledger.json`.
- `N15B` Delete all three and regenerate the ledger.
- `N15C` Move them into `archive/old/` and keep the ledger entry.

**N16 chapter-writing scripts**
- `N16A` **[CHOSEN + APPLIED 2026-11-21]** ★ Retire both scripts; their output chapters are deleted in §10.3 (cutover blocker).
- `N16B` Repoint them to `mds.md` and `index.md` + `contract.md`.
- `N16C` Move to `tools/dev/` unchanged and mark deprecated.
