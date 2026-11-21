# Debates · canonical index

> **Scope / Ámbito:** EN: Canonical navigation index of the other 64 files under `development/standards/debates/` (55 Markdown, 8 HTML, 1 `.bak-orig`), for Docs · Plan. · ES: Índice de navegación canónico de los otros 64 archivos de `development/standards/debates/` (55 Markdown, 8 HTML, 1 `.bak-orig`), para Docs · Plan.

**Authority — one home per fact.** [`development/index.html`](https://flove.org/development/index.html) **Plan + Work** are the canonical surface: they own milestone/task rows, section order and plan status. Markdown files are fallback referrals — they carry detail, never a duplicate register. [`plans/index.md`](https://flove.org/development/standards/debates/plans/index.md) is a reading map of plans; this file is the navigation index. [`../README.md`](https://flove.org/development/standards/README.md) and the standards chapters own **standards detail**; [`browsy/spec.md`](https://flove.org/development/standards/debates/browsy/spec.md) is the active **Browsy specification**. [`milestones.json`](https://flove.org/development/standards/debates/milestones.json) is the tracker source: **312 milestones** and **37 debate tickets** across 6 sections × 5 stages; `development/scripts/build-work-tracker.py` generates the page JSON block. [`common.json`](https://flove.org/development/standards/debates/common.json) is the generated page join (`flove-common/1`): **1,455 live tasks + 805 archived**; `jsony_check.py` and `build-common.py --check` fail when it lags the register. Run `python3 development/scripts/build-work-tracker.py --check` before and after any tracker edit — it is the fast gate for counts, section order, URLs, checker ownership, dependency cycles and Skills chip parity. The canonical roadmap execution policy is [`development/AGENTS.md`](https://flove.org/development/AGENTS.md), parsed by `development/scripts/procedures_source.py`, indexed in [`../README.md#procedures`](https://flove.org/development/standards/README.md#procedures), mirrored into `common.json` and rendered in **Work · AI → Skills**. The register owns only hitos and tasks. PROC-09 is the queue-replenishment loop: the **Archive · done + closed-hito tasks** drawer below the Work register collects moved tasks, `Export moves` writes a reviewable `work-moves.json` patch, and below 1,200 live tasks new ones are specified toward the 1,400 target (1,455 hard cap, 55 reserved), keeping ~30 active-window tasks ready; `check-restore.py` drills the reopen path read-only. The archived static a11y sweep of that page is [`a11y-development-index.md`](a11y-development-index.md). A milestone `source` may be a live MD **or** `build-work-tracker.py` (seed traceability); historical MDs are never sources. The builder enforces canonical section order and exact counts; MDs mirror the page and never reorder it.

**Hito shape (Q091–Q120):** each of the 312 hitos has an opaque id (`<section>-<n>`), a `stage` (`seed · infant · mature · grown · full`) — see [`hitos-audit.md`](hitos-audit.md) — and a task shape set by state: **0 tasks when closed (`on`)**, **7 when open** (1 seed + 3 infant + 3 mature), **8 on open `grown`/`full`** (plus one generalist). State and evidence live on the task, and the 99 once-flagged rows were split into concrete stage tasks (Q105/Q119 follow-up). Filtering and listing use subsections; the `section` field holds that subsection id and is treated as the section filter value (Q115). The 37 debate tickets carry a `stage` alias of `phase`. The group-label
`ticket` was retired from hitos in Q145 (the id is the only key); `keep`
stays load-bearing for Work row classification (127 `true` → `feature`,
185 `false` → `question`) and `state_mirror` must equal `state` (Q149).
Task execution order lives in
[`../README.md#task-order-proc-07`](../README.md#task-order-proc-07).
See [`questy-proposals.md#q091q120--hitos-tasks-y-stage`](questy-proposals.md).

**Live** = current source of record; **Historical** = kept for history, no authority. The canonical register is **425 items** — **312 milestones** across the 30 section × stage boxes, **37 debate tickets** plus **76 pendings rows** — across **6 sections** (docs · backend · frontend · ai · data · community) × **5 stages** (`seed · infant · mature · grown · full`, aliases **F1–F5**). Section, part and subsection order is fixed by `build-work-tracker.py` and mirrored in [`../README.md`](../README.md); no index may reorder it.

**Work filter route:** `https://flove.org/development/index.html#work?tab=docs&view=r2&subtab=work&category=<section>&section=<subsection>` — use `tab=docs` for the docs section; `section=work` for issue rows, `section=plan|levels|index` for degree milestones.

## Root

| File | What it is | Status |
|------|------------|--------|
| [a11y-report.md](https://flove.org/development/standards/debates/a11y-report.md) | Generated axe-core + keyboard audit report (49 apps, 0 nodes) | Live (generated) |
| [agents.md](https://flove.org/development/standards/debates/agents.md) | Questy tuning config for the old "flove central" sessions | Historical |
| [archive.md](https://flove.org/development/standards/debates/archive.md) | Retired home-directory layout note | Historical |
| [flove-decisions-interview.html](https://flove.org/development/standards/debates/flove-decisions-interview.html) | Standalone HTML interview used to collect design decisions | Historical |
| [pendings.md](https://flove.org/development/standards/debates/pendings.md) | Live issue register; mirrored as 76 canonical Work rows | **Live (tracker source)** |
| [proposals.md](https://flove.org/development/standards/debates/proposals.md) | Snapshot of questy central proposals P01–P17 | Historical |
| [questy-proposals.md](https://flove.org/development/standards/debates/questy-proposals.md) | Resolved questy proposals P001–P009 | Historical |
| [roadmap-2026-06.md](https://flove.org/development/standards/debates/roadmap-2026-06.md) | Archived June 2026 phased roadmap (legacy F0–F5); Work uses F1–F5 | Historical |
| [skills-library.md](https://flove.org/development/standards/debates/skills-library.md) | Prose moved out of the skills README | Historical |
| [standards.md](https://flove.org/development/standards/debates/standards.md) | Questy project standards (paths, rules, presets) | Live (questy reference) |
| [UseCase-adv.md](https://flove.org/development/standards/debates/UseCase-adv.md) | Questy advanced use case: step-by-step script | Live (questy reference) |

## browsy/

| File | What it is | Status |
|------|------------|--------|
| [browsy/README.md](https://flove.org/development/standards/debates/browsy/README.md) | Architecture, decisions and file map | Live (reference) |
| [browsy/spec.md](https://flove.org/development/standards/debates/browsy/spec.md) | Active Browsy/Authy/Wizy/MyNet spec (BSP requirements, phases) | **Live (active spec)** |
| [browsy/rationale.md](https://flove.org/development/standards/debates/browsy/rationale.md) | Privacy-first data-mesh vision behind the spec | Live (reference) |
| [browsy/browsy-questions.md](https://flove.org/development/standards/debates/browsy/browsy-questions.md) | Only register for the live A–L questions (§A Authy); historical decision log above | **Live (questions)** |
| [browsy/TESTING.md](https://flove.org/development/standards/debates/browsy/TESTING.md) | Risk analysis, test matrices, crypto comparison | Live (reference) |
| [browsy/port-nety.md](https://flove.org/development/standards/debates/browsy/port-nety.md) | Crypto/storage seams for the Nety port | Live (reference) |

## browsy/pre-build/

| File | What it is | Status |
|------|------------|--------|
| [browsy/pre-build/README.md](https://flove.org/development/standards/debates/browsy/pre-build/README.md) | Index of pre-build contracts | Live |
| [browsy/pre-build/01-mvp.md](https://flove.org/development/standards/debates/browsy/pre-build/01-mvp.md) | MVP scope and first slice | Live |
| [browsy/pre-build/02-authy-levels.md](https://flove.org/development/standards/debates/browsy/pre-build/02-authy-levels.md) | SelfAuth vs verified Telegram | Live |
| [browsy/pre-build/03-schemas.md](https://flove.org/development/standards/debates/browsy/pre-build/03-schemas.md) | Schema ids and storage keys | Live |
| [browsy/pre-build/04-myfamily-profile.md](https://flove.org/development/standards/debates/browsy/pre-build/04-myfamily-profile.md) | MyFamily 7-areas × 5-replies projection | Live |
| [browsy/pre-build/05-native-host.md](https://flove.org/development/standards/debates/browsy/pre-build/05-native-host.md) | Native messaging host transport | Live |
| [browsy/pre-build/06-bridge-threat-model.md](https://flove.org/development/standards/debates/browsy/pre-build/06-bridge-threat-model.md) | Bridge boundary and threat model | Live |
| [browsy/pre-build/07-lineage-tests.md](https://flove.org/development/standards/debates/browsy/pre-build/07-lineage-tests.md) | Invite lineage and test fixtures | Live |
| [browsy/pre-build/08-model-labels.md](https://flove.org/development/standards/debates/browsy/pre-build/08-model-labels.md) | "Else" and the two Browsy chips | Live |
| [browsy/pre-build/09-consult-agreements.md](https://flove.org/development/standards/debates/browsy/pre-build/09-consult-agreements.md) | Signed, revocable Wizy consult agreements | Live |
| [browsy/pre-build/11-ui-pending.md](https://flove.org/development/standards/debates/browsy/pre-build/11-ui-pending.md) | Pending Browsy/Nety UI model (design only) | Live (pending) |
| [browsy/pre-build/open-issues.md](https://flove.org/development/standards/debates/browsy/pre-build/open-issues.md) | Closed pre-build answers log | Live (reference) |

## plans/

| File | What it is | Status |
|------|------------|--------|
| [plans/index.md](https://flove.org/development/standards/debates/plans/index.md) | Plan map, roadmap phases and conflicts pointer | **Live (plan map)** |
| [plans/central-backend.md](https://flove.org/development/standards/debates/plans/central-backend.md) | Central FastAPI/Turso design (superseded in part by Browsy spec) | Live (design) |
| [plans/puzzy.md](https://flove.org/development/standards/debates/plans/puzzy.md) | Puzzy aggregation and compute decisions | Live |
| [plans/standards.md](https://flove.org/development/standards/debates/plans/standards.md) | Standards/distro decisions SD01–SD19 — historical referral; live status is in Docs · Plan/Work | Historical |
| [plans/conflicts.md](https://flove.org/development/standards/debates/plans/conflicts.md) | Cross-plan tensions tracker | Live (living doc) |
| [plans/2026-11-17-appy-authy-mynet.md](https://flove.org/development/standards/debates/plans/2026-11-17-appy-authy-mynet.md) | Authy → Appy → MyNet activation spec draft | Live (draft) |
| [plans/2026-11-19-authy-open-questions.md](https://flove.org/development/standards/debates/plans/2026-11-19-authy-open-questions.md) | Compact pointer only — Authy A01–A13 live in `browsy-questions.md` §A | Live (pointer) |
| [plans/2026-06-18-nety-frontend-build.md](https://flove.org/development/standards/debates/plans/2026-06-18-nety-frontend-build.md) | Old nety/appy frontend build plan, rewritten to match the build | Live (build record) |
| [plans/2026-06-18-nety-frontend-build.md.bak-orig](https://flove.org/development/standards/debates/plans/2026-06-18-nety-frontend-build.md.bak-orig) | Original section-by-section build plan backup | Historical |
| [plans/2026-11-14-app-tier-planned.md](https://flove.org/development/standards/debates/plans/2026-11-14-app-tier-planned.md) | Tiers closed for this trunk; demos only | Historical |

## proposals/

| File | What it is | Status |
|------|------------|--------|
| [proposals/frontend-tiers.md](https://flove.org/development/standards/debates/proposals/frontend-tiers.md) | §13.1 tier model design sketch (not in trunk) | Historical |
| [proposals/frontend-wizy.md](https://flove.org/development/standards/debates/proposals/frontend-wizy.md) | Wizy operating-areas draft | Live (draft) |

## reviews/

| File | What it is | Status |
|------|------------|--------|
| [reviews/2026-07-25-browsy-fastapi-libsql-performance-review.md](https://flove.org/development/standards/debates/reviews/2026-07-25-browsy-fastapi-libsql-performance-review.md) | Browsy/FastAPI/libSQL standards and build-readiness review | Historical |

## archive/

| File | What it is | Status |
|------|------------|--------|
| [archive/making-of/making-of.html](https://flove.org/development/standards/debates/archive/making-of/making-of.html) | Full design-decision interview record | Historical |
| [archive/making-of/skills-applied.html](https://flove.org/development/standards/debates/archive/making-of/skills-applied.html) | Per-app `/optimizy` pipeline board | Historical |
| [archive/making-of/superpowers/specs/2026-06-12-frontend-standards-upgrade-design.md](https://flove.org/development/standards/debates/archive/making-of/superpowers/specs/2026-06-12-frontend-standards-upgrade-design.md) | Frontend standards upgrade design | Historical |
| [archive/making-of/superpowers/specs/2026-06-15-keys-intro-summary-design.md](https://flove.org/development/standards/debates/archive/making-of/superpowers/specs/2026-06-15-keys-intro-summary-design.md) | Keys intro carousel and summary design | Historical |
| [archive/making-of/superpowers/specs/2026-06-17-keysmini-design.md](https://flove.org/development/standards/debates/archive/making-of/superpowers/specs/2026-06-17-keysmini-design.md) | Keys mini design | Historical |
| [archive/making-of/superpowers/specs/2026-06-18-nety-access-ecosystem-design.md](https://flove.org/development/standards/debates/archive/making-of/superpowers/specs/2026-06-18-nety-access-ecosystem-design.md) | Nety access and identity ecosystem design | Historical |
| [archive/making-of/superpowers/specs/2026-06-18-nety-spec-vs-flovenet-oasis-comparison.md](https://flove.org/development/standards/debates/archive/making-of/superpowers/specs/2026-06-18-nety-spec-vs-flovenet-oasis-comparison.md) | Nety spec vs flovenet/oasis comparison | Historical |
| [archive/making-of/superpowers/specs/2026-06-19-apps-index-redesign-design.md](https://flove.org/development/standards/debates/archive/making-of/superpowers/specs/2026-06-19-apps-index-redesign-design.md) | Apps index redesign round | Historical |
| [archive/making-of/superpowers/specs/2026-06-19-appy-five-apps-tier-ladders-design.md](https://flove.org/development/standards/debates/archive/making-of/superpowers/specs/2026-06-19-appy-five-apps-tier-ladders-design.md) | Five Appy variants tier-ladder design | Historical |
| [archive/making-of/superpowers/specs/2026-06-24-appy-intros-rainbow-roadmap-design.md](https://flove.org/development/standards/debates/archive/making-of/superpowers/specs/2026-06-24-appy-intros-rainbow-roadmap-design.md) | Appy first-run intros and rainbow roadmap | Historical |
| [archive/making-of/superpowers/specs/2026-06-25-flove-private-addon-login-encryption-design.md](https://flove.org/development/standards/debates/archive/making-of/superpowers/specs/2026-06-25-flove-private-addon-login-encryption-design.md) | Locking/encryption add-on design (DS02) | Historical |
| [archive/making-of/superpowers/specs/2026-07-04-launch-language-chooser-design.md](https://flove.org/development/standards/debates/archive/making-of/superpowers/specs/2026-07-04-launch-language-chooser-design.md) | Launch language chooser design | Historical |
| [archive/making-of/superpowers/specs/2026-07-05-flove-pwa-installable-design.md](https://flove.org/development/standards/debates/archive/making-of/superpowers/specs/2026-07-05-flove-pwa-installable-design.md) | Installable PWA design (DS01) | Historical |
| [archive/making-of/superpowers/specs/2026-07-20-context-standards-tidy-design.md](https://flove.org/development/standards/debates/archive/making-of/superpowers/specs/2026-07-20-context-standards-tidy-design.md) | Executed `context` standards tidy | Historical |

## ephemerall/

| File | What it is | Status |
|------|------------|--------|
| [ephemerall/ephemerall.html](https://flove.org/development/standards/debates/ephemerall/ephemerall.html) | "All must go" ephemeral installation | Historical (demo) |
| [ephemerall/ephemeral-glider.html](https://flove.org/development/standards/debates/ephemerall/ephemeral-glider.html) | Glider assembling mark study | Historical (demo) |
| [ephemerall/ephemerall-logos.html](https://flove.org/development/standards/debates/ephemerall/ephemerall-logos.html) | Ten vanishing logo marks | Historical (demo) |
| [ephemerall/glider-balls-set.html](https://flove.org/development/standards/debates/ephemerall/glider-balls-set.html) | Glider ball-mark motion set | Historical (demo) |
| [ephemerall/strategicpersistence.html](https://flove.org/development/standards/debates/ephemerall/strategicpersistence.html) | Strategic persistence planner demo | Historical (demo) |

## others/

| File | What it is | Status |
|------|------------|--------|
| [others/flove-libs-insights.md](https://flove.org/development/standards/debates/others/flove-libs-insights.md) | Historical questy→`flove.css` notes; recommendations absorbed into `contract.md` §2 / `frontend.md` §13.16 | Historical (reference) |

## research/

| File | What it is | Status |
|------|------------|--------|
| [research/vr_interfaces.md](https://flove.org/development/standards/debates/research/vr_interfaces.md) | Free-software Godot/VR research (VR direction abandoned) | Historical |

## bridges/

| File | What it is | Status |
|------|------------|--------|
| [bridges/oasis.md](https://flove.org/development/standards/debates/bridges/oasis.md) | Oasis/0asis reference map and flove adaptation | Live (reference) |
