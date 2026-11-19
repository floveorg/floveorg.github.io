---
name: optimizy
description: >-
  Polish one file or page with only the stages it needs, in the order that
  avoids rework. Use for /optimizy <file|page> or /optimizy1–/optimizy5; an app
  is one run per page.
---

# optimizy

Take **one file or page** to a finished state by running only the stages it needs,
in the one order that avoids rework. Shrink first, inflate last: `/simplify`
deletes code, so later stages read less; `/translaty` multiplies every string, so
nothing reads the file after it.

For an app, run `/optimizyN` per page; `/skilly`/`/jsony` are separate; packages
are `updaty4`.

## Depth

`/optimizyN` runs levels 1 → N and stops; default `/optimizy` = 5. Levels are
cumulative and skip what the kind doesn't need.

1. **Clean** — `simplify` + `validaty` + `code-review`, plus privacy/security:
   no dead code or bugs, valid HTML/CSS/JS/JSON, a11y · mobile · i18n readiness,
   the least data, no third-party leak, clear consent. UX flags are noted.
2. **Data & Words** — `export` + `texty` + `translaty`: the portrait round-trips,
   save/share/import work, then copy, names and languages are final.
3. **Usability** — meet every minimum in the
   [usability matrix](https://flove.org/development/standards/frontend/frontend.md#1318--usability-levels--3-minimum--4-function--5-craft);
   a missing minimum fails the level. Menu, tour, metadata and transparent stats
   are the shell rows; every other section is audited the same way.
4. **Function** — the concrete level-4 features: compass, counters,
   publish/database and the deeper per-section jobs.
5. **Craft** — the level-5 features: locking/tiers, trends, migration, motion
   and the rest, plus a prioritized recommendation list (impact × effort).

Extra modules when needed, at any level: docs/help, tests/QA, PWA/install,
share/OG card, print/export, migration.

## Pick the file and its kind

Resolve the target: a path as written (`apps/metas/souls.html`), `<app> <page>`, or
an app id in `tools/routing.json`. If two files match, ask — never guess. Profile
**the file**, not the app: one app can hold a hub, a rated page and a gallery.

| Kind | Looks like | Run |
|---|---|---|
| rated JS | JS state, a model, a summary | simplify · validaty · export · code-review · texty3 · translaty |
| CSS-pure | zero JS; navigation is CSS | validaty · translaty (+ texty1) |
| hub / gallery | navigation or brand only | validaty (translaty is a call to flag) |
| form / profile | Appy-style surface | validaty · export (envelope) · code-review · translaty |
| content | prose only | validaty · code-review light · translaty |

Run only what the row lists; name every skip and why. A page with no user model
gets `export: N/A` — never scaffold a summary it never had.

## The order

| # | Stage | Why here |
|---|-------|----------|
| 1 | **simplify** | mechanical shrink: dead code, dupes, reuse. No bug-hunting. |
| 2 | **validaty** | validity (HTML · CSS · JS · JSON) + a11y · mobile · i18n *readiness*, on final single-language code. |
| 3 | **export** + **jsony** | selections lively in the summary, every save/share/import button works; when routing, `APP_ROUTING` or an envelope changed, run `/jsony` and leave it clean. |
| 4 | **code-review** | the **bug** pass on clean code; ignore its simplification findings. |
| 5 | **texty3** *(optional)* | names to match the UI, before language spans. |
| 6 | **translaty** | **always last**: wraps final strings + the worldball. Idempotent. |

Levels 3–5 are not stages: they apply the usability matrix (minimum, function,
craft).

**Backbone gate.** Stage 3 hands the JSON backbone to `/jsony` whenever the pass
touched `tools/routing.json`, Appy's `APP_ROUTING` or a `flove-fields` / portrait
envelope; the run reports jsony's result beside the stage ledgers.

Stages 1 and 4 are flove-blind: a `:has(#tab-3:checked)` selector or a `for=`/`id`
pair is a load-bearing wall. List every wall before stage 1, hand both stages a
do-not-touch/do-not-rename brief, and re-verify navigation after each. Brief
code-review with §3 too — CSS over JS is normative.

## Running the stages

- `/validaty`, `/exporty`, `/texty`, `/translaty` are flove skills. `/simplify`
  and `/code-review` are built-ins; if one is missing, shrink without changing
  behavior (dead code, duplicate helpers, reusable patterns), then find bugs
  (navigation selectors, `for=`/`id`, event wiring, export parse-back). Record
  the baseline, re-verify navigation, and never claim a missing stage ran.
- Grep the file before each stage and skip what already holds; the canonical
  signals are §13.10 title · §13.6 onboarding · §13.14 theme.
- Tell each stage it is running under `/optimizy`: it drops its own survey, report
  and commit and hands them up; the orchestrator writes the batch.
- One ledger.

**Stop-on-fail: never translate a broken file.** A failed `html-validate`, a dead
export button, a summary that never shows selections, a `node --check` error —
halt before translaty and report the gate.

## Levels 3–5 · usability

Read [§13.18](https://flove.org/development/standards/frontend/frontend.md#1318--usability-levels--3-minimum--4-function--5-craft)
and [`contract.md`](https://flove.org/development/standards/contract.md) §6 before judging. Level 3 marks every applicable row
**present / missing / N/A**; a missing minimum fails. Level 4 implements the
concrete level-4 features; level 5 the level-5 ones.

The shell rows are menu (§13.5), ten-slide tour (§13.6), metadata (§13.10 +
head / Open Graph / `flove-fields`) and transparent stats (§13.17). They are
examples: every section the app has is audited by the same matrix. Report gaps;
never silently redesign.

## Survey

Safe fixes are silent. Batch Nav-risk / Divergence findings into one inline survey
(`https://flove.org/development/standards/skills/standing.md` 3): finding, why,
recommendation, alternatives, default; ask once. Stages return findings; the
orchestrator batches. Apply the chosen rows, record refusals. Headless:
recommendation, labelled pending (rule 4).

## Definition of done

- `npx --no-install html-validate <file>` exits **0**.
- If translaty ran: its gate prints **OK** and there is no mojibake.
- No inline `style=`; each helper exists once; navigation still resolves.
- The three canonical signals hold (§13.10 · §13.6 · §13.14).
- At level 3+: no applicable row in §13.18 is missing its minimum.
- Report honestly: what ran, what was skipped, what was surveyed.

## Boundaries

- One file/page. For an app or cluster, run `/optimizyN` on each in-scope page.
  Package releases are `updaty4`; the library and backbone gates are
  `/skilly` and `/jsony`.
- It orchestrates and sequences; depth lives in each stage's own `SKILL.md`.
- It does not redesign, and does not invent stages.

Standing rules: `https://flove.org/development/standards/skills/standing.md`.
