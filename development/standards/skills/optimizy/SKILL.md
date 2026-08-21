---
name: optimizy
description: >-
  Run the full flove polish pipeline on an app — code simplification, validation
  (validity/a11y/mobile/i18n), export & share check, a correctness code-review,
  optional vocabulary normalization, and translation — in the one order that avoids rework
  and burns the fewest tokens. Use this
  whenever the user wants to "polish", "pulir", "optimize", "clean up", "finish", or "do
  the full pass" on an app or a whole cluster/family of apps, types /optimizy, or asks to
  apply several of the polish skills together ("validate + translate this", "get worthing
  production-ready", "run the whole polish on the trusty cluster"). It is the orchestrator
  for /simplify, /validaty, /exporty, /code-review, /vocaby and /translaty — reach for it even when
  the user only names two of those but clearly wants the app brought to a finished state.
  flove-first by default (single-file HTML/CSS/JS apps, the §13 standards, CSS-only
  navigation); override via the personal config (see CONFIG.md). It inherits every standing
  rule of the skills it drives: inline surveys only, never a browser, no commit unless the
  user's workflow says so.
---

# optimizy

Bring a flove app (or a whole cluster of them) to a *finished* state by running the polish
skills in the right order. The skills themselves already know how to do their jobs — this
skill's only value is **sequence and economy**: doing them in an order where no step undoes
a previous one, and where the file is at its smallest single-language size for every step
that has to read it.

## Personal config

This skill ships with flove-first defaults. To fork/reuse it for another
project, create a personal config that overrides the defaults instead of
editing the skill (see `development/standards/skills/CONFIG.md`): a shared
`~/.config/flove/skills-config.yml`, a per-skill `settings.yml`, a hidden
`.settings`, or a `config.yml` in the skill folder. Only the keys you set
change; everything else falls back to these defaults.

## The two anchors

Almost the whole design collapses to one sentence:

> **Shrink first, inflate last.**

- `/simplify` (or the `code-simplifier` agent) deletes dead and duplicated code, so every
  later step reads a *smaller* file — fewer tokens, every time.
- `/translaty` multiplies every visible string into one span per language, so it roughly
  **doubles or triples the file**. Nothing must read the file after it. Run it once, at the
  very end.

Everything between those two anchors is low-coupling, but the order below still matters
because it stops a later skill from invalidating an earlier one (renaming after you've
translated, reviewing bugs in code you're about to simplify away). `/vocaby` sits between
code-review and translaty for exactly this reason: renaming a load-bearing name is a
nomenclature pass, and it must happen *before* the file inflates with language spans —
after that, every renamed selector would need re-translating too.

## The order

| # | Stage | Why it sits here |
|---|-------|------------------|
| 1 | **simplify** (`/simplify` or `code-simplifier`) | Mechanical shrink: dead code, dupes, reuse. Smallest possible file for everyone downstream. No bug-hunting. |
| 2 | **validaty** (`/validaty`) | Validity + a11y + mobile + leave i18n *ready*, on the structurally-final, single-language file. The `aria-label`s it adds get translated once, in stage 6. |
| 3 | **export** (`/exporty`) | Make sure selections are **lively shown** in the summary — live, or via an update button if the design allows it in the HTML — and that every button for **saving, sharing, or importing** content actually works. A behavior check on the single-language file, before translation. |
| 4 | **code-review** (`/code-review`) | The **bug** pass, on clean, final, single-language code — smaller read, fewer false positives. The last correctness gate before the file inflates. Briefed with the §3 rule (CSS-over-JS normative). |
| 5 | **vocaby** (`/vocaby`, optional) | Normalize the §13.7 nomenclature — align the internal names (classes, ids, i18n keys) with the words the UI shows, on the clean single-language file, *before* translaty inflates it. Skipped when the vocabulary is already canonical. |
| 6 | **translaty** (`/translaty`) | **Always last.** Wraps every now-final visible string (including whatever validaty/exporty/vocaby added) + the worldball. Idempotent, so it sweeps the lot in one go. After this, nothing reads the file. |

**On the simplify/code-review overlap:** both touch the reuse/efficiency dimension.
That's deliberate — use stage 1 to *shrink* and stage 4 to find *bugs*. In stage 4 you can
ignore code-review's "simplification" findings; stage 1 already did them. Don't pay for the
same cleanup twice.

## Guard the flove-blind stages (simplify, code-review)

Stages 1 and 4 are Anthropic built-ins. They're excellent at general code — and **blind to
flove**: they don't know that a `:has(#tab-3:checked)` selector, a `for=`/`id` pair, or a
state-bound `~`/`+` combinator is a *load-bearing wall* of a CSS-only navigation. Left
unbriefed, `/simplify` will happily merge two "duplicate" classes or collapse a selector and
silently kill a menu; `/code-review` will recommend the same. They're the riskiest stages
precisely because they look the safest.

So before stage 1, **profile the load-bearing walls once** (the same grep validaty
runs): every `label … for=`, `type="radio"`/`checkbox`, `:checked`, `:has(`,
`:target`, state-bound `~`/`+`, `<details>`/`<summary>`, and any class/id a selector keys on.
Hand that list to simplify and to code-review as an explicit **do-not-touch / do-not-rename**
constraint, and tell them the app is a self-contained single-file flove app whose navigation
is pure CSS. After each of those two stages, **re-verify navigation** — reason through every
interactive path that touched a wall, and re-run `html-validate` + the translaty gate if any
id/selector moved. A simplification that breaks nav is worse than the duplication it removed.

**Brief code-review with §3 too.** The load-bearing walls are *structural* blind spots; §3
(CSS-over-JS, contract.md) is the *behavioral* one. Unbriefed, code-review is flove-blind in
the other direction and will happily bless a `matchMedia` JS theme switcher, a click listener
that reinvents `:has()`, or JS-driven show/hide that CSS could do for free. Tell it **CSS-over-JS
is normative** — reveal/hover/expand via `:hover`/`:focus-visible`/`:has()`/`details`, theming
via custom properties + `prefers-color-scheme` + a `flove:theme` override, never JS measuring
or listeners where CSS answers. A JS pattern §3 forbids is a finding, not a "improvement."

## Preflight: detect what's already done (skip, don't redo)

The biggest waste in a re-run is re-doing a stage that already landed. Before running any
stage on an app, **detect its current state from cheap signals** and skip what's already
satisfied — say so in the report rather than silently redoing it. Grep the file; cross-check
with `git diff` against a pre-work baseline when one exists:

| Stage | "Already done" signal |
|-------|-----------------------|
| translaty | a worldball (`🌐` / `input[name="lang"]` / `.lang-opts`) **and** `.es`+`lang="es"` sibling spans, gate clean → skip (or only fill a missing language) |
| validaty | `html-validate <file>` exits 0 **and** `<!DOCTYPE html>` + `<html lang=` present → validity done (still scan a11y/mobile if never run) |
| export | the selected/added content shows in the summary **lively** (live or via an update button), and the save/share/import buttons each do their job → skip (still probe if never checked) |
| vocaby | class/id/label names match the words the UI shows (spot-grep a couple against `flove-vocaby.html` slots) → skip (or only rename the drift) |
| simplify / code-review | no file marker — use `git log`/diff: if the app was simplified/reviewed since its last substantive change, don't repeat |

**Canonical signals (all one-grep, none exists today — add them to every intake and to the
Definition of done below).** These are the family-wide standards that *no* stage owns, so they
fall to the orchestrator:

| Signal | §13 | One-grep check | Done when |
|--------|-----|----------------|-----------|
| Nav-tab title | §13.10 | `grep -o '<title>[^<]*</title>' <file>` | `<App> · FLOVE` — app name first (display case), ` · ` separator, `FLOVE` last; favicon = the app's own SVG mark; **no sprout glyph** in the title |
| Onboarding | §13.6 | `grep -cE 'onboarding|intro-open|seen-intro|welcome|step' <file>` | present and "loud first time, ignorable after" — it's the **only mandatory family-wide** standard, and no stage checks it |
| Theme switcher | §13.14 | `grep -cE "flove:theme|data-theme|prefers-color-scheme" <file>` | `flove:theme` key in `localStorage` + a ◐ control, CSS palettes (`prefers-color-scheme` + `[data-theme]`) — the JS only does click + persistence (§3) |

If a canonical signal is missing, fix it in this pass (they're cheap greps and small fixes);
report each as its own line so the matrix knows it landed.

Run this once per app at intake, decide the stage set, then execute only the gaps. It's the
same detection that seeds the progress board below.

## Driving the pipeline (per app)

For a single app, run the six stages in order, each as its own skill invocation, on the
same file. Between stages, keep a short running ledger of what changed — you'll fold it into
one final report rather than narrating six times.

Two judgment calls keep it efficient:

- **Skip what doesn't apply to the tier.** A `mini` app is pure CSS, 0 JS — stages 1 and 4
  (simplify, code-review) are near-empty there; don't spend a pass on them. A `logos.html`
  gallery or a hub (`trusty.html`, `dealy/index.html`) is brand/navigation, not a rated
  app — usually only validaty applies. State which stages you skipped and why.
- **Inherit, don't re-ask.** Each sub-skill has a standing rule to surface risky/divergent
  changes as **one inline survey** (never an HTML form unless the user invokes `/questy-html`).
  When running the full pipeline, **batch all the surveys you can foresee into one** at the
  point you first read the app, so the user answers a coherent set once instead of being
  interrupted six times. Where a sub-skill would block on a survey and you're running
  headless (a subagent, a batch), follow its headless rule: write the survey as text, apply
  the recommended option, label it "pending confirmation."

### Tell each stage you're driving (the orchestration-mode contract)

The four flove sub-skills (`validaty`, `exporty`, `vocaby`, `translaty`) each have an
**"Orchestration mode — when /optimizy is driving"** section. When you invoke a stage, say so
explicitly — e.g. *"Running as the validaty stage of /optimizy — orchestration mode"* — so it
drops the work you (or a neighbour) own and hands the rest back instead of acting alone. In
that mode the stages stop doing three things, and **you take them over**:

1. **The survey.** Stages return their Nav-risk / Standard-divergence findings (and big calls
   like "scaffold the whole export surface", the translaty proper-noun call) as text. You
   collect them across stages and run **one** batched inline survey.
2. **The report.** Stages return a compact ledger; you write the **single** end-of-run report.
3. **The commit.** Stages leave the tree dirty; you handle commit/push per the user's
   workflow once the pipeline (or cluster) is done.

`simplify` and `code-review` are Anthropic built-ins without this mode, so you manage their
overlap from here: run `simplify` as the pure shrink pass, and in `code-review` **focus on
bugs and ignore its reuse/simplification findings** — stage 1 already did those.

### Which stages apply by tier

Don't guess per app — the tier (and distro) decides the stage set. Skipping an N/A stage is a
token win, not a gap; just name it in the report.

| Tier / kind | simplify | validaty | export | code-review | vocaby | translaty |
|-------------|:--:|:--:|:--:|:--:|:--:|:--:|
| mini (CSS-pure, 0 JS) | – | ✓ | N/A | – | ~ | ✓ |
| basic | ~ | ✓ | N/A | ~ | ~ | ✓ |
| normal | ✓ | ✓ | opt | ✓ | opt | ✓ |
| advanced / super | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| logos / hub / index | – | ✓ | N/A | – | – | flag* |

✓ applies · ~ light (little JS / few names to rename) · – near-empty, skip · N/A not applicable · opt optional.
*hubs/logos are brand or nav, so translaty is a *flag the call* (proper names often stay English).
When in doubt, run the listed set and say what you skipped.

### Stop-on-fail (never translate a broken app)

The stages run in order because a later one assumes the earlier succeeded. If a stage **fails
its own gate** — validate can't reach `html-validate` 0, export finds a save/share/import
button that does nothing or a summary that never shows the selections, vocaby hits a
nomenclature dead-end, a `node --check` errors — **halt that app before translaty** and report
it. Translating an app
that isn't valid yet is the worst outcome: translaty inflates the file ×languages, so you'd
multiply a broken state and make the fix far costlier. Halting one app never blocks the others
in a cluster — set it aside, finish the rest, and list the casualty with the exact failing
gate so it's an easy pickup.

## The big token lever: clusters and fan-out

The single largest cost in this work is reading the same large file many times. Two tactics
cut it hard:

1. **Cluster by family, not app-by-app.** blogy mini/basic/normal/advanced are near-clones;
   the trusty apps share a shell. Polish a whole family in one session so the shared
   patterns and the survey decisions stay in context and aren't re-derived per app.

2. **Fan the per-app work out to subagents; keep only the conclusions.** When polishing a
   cluster, dispatch each app's pipeline to its own subagent. The heavy file reads then live
   in *that* subagent's context; only the diffs and the report come back to you. This is the
   biggest multi-app saving. Caveats the orchestrator must own:
   - Subagents **can't run `npx`/`node`** in the sandbox, so their validity and translaty
      passes are *blind*. You (the orchestrator) re-run `npx --no-install html-validate` and
      the translaty gate (`<translaty>/scripts/check.js`) and finish validity by hand,
      **per app**, after the subagents return. The export, vocaby, and canonical-signal
      checks are plain greps subagents can run, but their verdicts come back as text — confirm
      the parity/parse-back and the canonical signals yourself before marking the row done.

2. **Commit between stages / between apps.** Small diffs let you detect state with
   `git diff` instead of re-reading whole files to learn what's left to do.

## The progress board (state & resume)

A cluster pass is long and gets interrupted. Keep the state **on disk**, not in your head, so
a re-run resumes instead of restarting. The board is the `docs/` skills-applied table — the
one that tracks app × {simplify, validaty, export, code-review, vocaby, translaty}, plus a
row for the three canonical signals (§13.10 title · §13.6 onboarding · §13.14 theme).
Treat it as the pipeline's source of truth:

- **At intake**, seed/refresh each app's row from the preflight detection above — so the board
  reflects reality, not what was merely *intended*.
- **After each stage**, mark the cell (✓ done · ~ partial · blank todo) with the date and
  commit it alongside the app's diff. A killed session then resumes by reading the board: any
  app with an unfinished row is the next pickup, at its first blank stage.
- **One writer.** Like the matrix table, the board is shared state — only the orchestrator
  writes it, never a fan-out subagent. Update it in the same step you fold in each app's ledger.

This closes the loop: the audit table isn't a one-off snapshot, it's the live to-do list the
skill drives from and keeps current for free.

## Standing rules it inherits (don't relearn them the hard way)

- **No browser, ever.** flove's owner opens the page himself to look; never drive a browser
  to "verify visually." Verify with the tooling and by reasoning through each interactive
  path you touched.
- **No commit/deploy unless the user's workflow says so.** This skill repairs the working
  tree. (flove's own rule is commit+push each change to its Gitea — follow that if it's
  active, otherwise leave the tree clean and say so.)
- **§13 is the standard.** A fix that's correct but would make this app diverge from the
  shared flove pattern is a distro-level decision — survey it, don't apply it silently.
- **translaty encoding gotcha.** Translation edits via perl must use **byte mode**
  (`open '<',$f` — *not* `:encoding(UTF-8)` with UTF-8 literals, which yields mojibake like
  `EscrÃ­belo`). After each translate pass, confirm `grep -c 'Ã\|Â'` is 0.
- **The `/.htmlvalidate.json` at the repo root is intentional** (`form-dup-name` lets radio/
  checkbox groups share a `name` inside a form). Don't delete or "fix" it.
- **Exclusions still hold.** Whatever the active polish program excludes — hubs, `logos.html`
  galleries, `keysbasic`/`keysmini`, `economy/dealy/inventary.html` (categories not yet
  frozen → don't translate) — stays excluded here too. Check the program memory before a
  cluster run.

## Definition of done (the acceptance gate)

Each sub-skill verifies its own slice, but "optimized" needs **one bar** the whole app clears
before you mark its board row complete. For the stages that apply to its tier, an app is done
when:

- `npx --no-install html-validate <file>` exits **0** (validity + the a11y the linter sees).
- The translaty gate (`node <translaty>/scripts/check.js <file>`) prints **OK**, and
  `grep -c 'Ã\|Â' <file>` is **0** (no mojibake).
- **No inline `style=`** was introduced, and each helper added (`esc`, `downloadBlob`, the
  i18n engine) exists once, not duplicated.
- For advanced/super: the summary **lively shows** the selected/added content (live or via an
  update button, per the design), every save/share/import button does its job, and each export
  format **parses back** to the same item set as the summary (parity); `navigator.share` is
  wired with the `canShare({files})` guard where the tier has it.
- Navigation **still resolves** — you've reasoned through each interactive path whose selector,
  id or class any stage moved (no browser, by inspection).
- **Nomenclature matches the UI** (when vocaby applied): class/id/label names align with the
  words the screen shows — no legacy `ray-*`/`bot-*` aliases where `labeler-*`/`wizard-*`
  belong (§13.7).
- **The three canonical signals are green** (all one-grep, the family-wide standards no stage
  owns):
  - §13.10 title reads `<App> · FLOVE` (app name first, display case · FLOVE last), the
    favicon is the app's own SVG mark, no sprout glyph in the tab title.
  - §13.6 onboarding exists and is "loud first time, ignorable after" — the one mandatory
    family-wide standard.
  - §13.14 theme: `flove:theme` key + a ◐ control, palettes in CSS
    (`prefers-color-scheme` + `[data-theme]`), JS only for click + persistence.

If any line fails, the app isn't done — it's a stop-on-fail casualty. Report the bar honestly
per app; a half-cleared gate stated plainly beats a green checkmark that lies.

## Reporting

One report at the end, not six. For each app: which stages ran, which were skipped and why,
what was auto-fixed per stage, what was surveyed and how the user decided, the final
`html-validate` count and translaty gate result, the state of the three canonical signals,
and anything still open. Coverage honesty
over false completeness — a truthful "4 of 6 stages, validity at 3 errors remaining" beats a
confident "all optimized" that isn't.

## Scope & non-goals

- It **orchestrates**; it does not reimplement the sub-skills. If a stage needs depth, that
  lives in the stage's own SKILL.md — defer to it.
- It does **not redesign**. If finishing an app truly needs a redesign (no accessible
  contrast anywhere, a broken layout), report it as a finding; don't restyle silently.
- It does not invent stages. Six stages, that order (vocaby optional — it's the one stage
  that can be dropped when the vocabulary is already canonical). If the user wants only a
  subset ("just validaty + translaty"), run that subset *in this relative order* and say so.
