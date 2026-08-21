---
name: validaty
description: >-
  Check and repair a web page or single-file HTML app across five axes — HTML/CSS/JS
  validity, accessibility (a11y), mobile-friendliness, and internationalization (i18n) —
  fixing everything safe automatically while protecting the app's existing navigation.
  Use this whenever the user wants to validate, audit, lint, or "fix the errors" on a
  page, asks to make something accessible / WCAG-compliant / screen-reader friendly,
  mobile-friendly / responsive, or i18n-ready, or types /validaty. Trigger it even when
  they don't say "validaty" — phrasings like "is this page broken?", "clean up the
  warnings", "make this work on phones", "check my a11y", "why does html-validate
  complain", "audit this app", or "make sure I didn't break anything" all count. flove-first
  by default (deep knowledge of CSS-only navigation); override via the personal config (see
  CONFIG.md). Works on any HTML/CSS/JS.
  Anything that could change behavior or diverge from the shared flove standard is never
  silently changed — it is raised as an inline survey for the user to decide.
---

# validaty

Find and repair correctness, accessibility, mobile, and i18n problems in a web page —
**without breaking how it works.** The defining tension of this skill: a validator will
happily tell you to delete an `aria-hidden`, rewrite a heading, or rewrap a node, and any
of those can quietly kill a navigation pattern that relies on it. So the job is not "make
the linter happy at all costs" — it's "make the page correct while the page keeps doing
exactly what it did." A fix that breaks navigation is worse than the original error.

## Personal config

This skill ships with flove-first defaults. To fork/reuse it for another
project, create a personal config that overrides the defaults instead of
editing the skill (see `development/standards/skills/CONFIG.md`): a shared
`~/.config/flove/skills-config.yml`, a per-skill `settings.yml`, a hidden
`.settings`, or a `config.yml` in the skill folder. Only the keys you set
change; everything else falls back to these defaults.

## The core idea: three buckets

Every finding gets sorted into one of three buckets. This sorting *is* the skill — the
checks themselves are routine; the judgment is knowing which bucket a fix belongs in.

1. **Safe** — the fix cannot change behavior or layout. Apply it silently and report it
   afterward. (doctype casing, a missing `lang`, `role` so an `aria-label` becomes legal,
   a heading→`span` swap *inside* a preserved trigger, adding the viewport meta…)
2. **Nav-risk** — the fix touches something the app's interaction depends on, so it
   *might* change behavior. Never apply blind. Surface it in an inline survey.
3. **Standard-divergence** — the fix is correct, but applying it would make this app
   differ from the shared flove pattern (the §13 standards). Even if it's safe in
   isolation, it's a distro-level decision. Surface it in the same survey.

When unsure whether something is Safe or Nav-risk, treat it as Nav-risk. The cost of
asking is one question; the cost of a wrong silent edit is a broken app the user has to
debug later.

**House rule — don't fix one lint by tripping another.** When a Safe fix needs styling
(a visually-hidden label, a `<legend>`, a focus outline), put the styling in a **class or
a CSS rule, never an inline `style=` attribute.** Many codebases — flove apps in
particular — enforce a no-inline-style rule, so an inline style is itself a validation
error: you'd be trading one finding for another. If a utility class like
`.visually-hidden` doesn't exist yet, add the class definition to the stylesheet once and
reuse it. The same spirit applies generally: a repair shouldn't introduce a new violation
of the project's own conventions.

## Orchestration mode — when /optimizy is driving

If your invocation says you're running as the **validaty stage of `/optimizy`** (the
orchestrator tells you so), fix validity, a11y and mobile in full — but stay off the ground
the neighbouring stages own:

- **The app is still single-language; translaty is the *last* stage, not yet run.** So make
  the page i18n-**ready** (no string-concatenated sentences, text extractable, `lang`
  present) and **stop there** — do **not** translate, add `.es` spans or the worldball, or
  run the translaty-aware i18n-correctness checks. Doing any of that now is premature work
  translaty will redo.
- **`/vocaby` ran just before you** — naming is settled. If a name still looks wrong,
  *report* it; don't rename (that's not your axis and would fight an earlier stage).
- **`/code-review` runs after you** and owns behavioural **bugs**. Stay on validity/a11y/
  mobile; flag a logic smell for the orchestrator rather than chasing it here.
- **Don't open your own survey, don't write a final report, don't commit.** Apply the whole
  Safe bucket as always, then hand the Nav-risk / Standard-divergence findings to the
  orchestrator as text; it batches one survey for the pipeline and writes the single report.

Everything else below still applies in full — you're doing *less overlap*, not less care.

## Workflow

1. **Read and profile the target.** Read the file(s). Before touching anything, map two
   things, because they decide your buckets:
   - **Does it use a CSS-only navigation pattern?** Grep for the tells: `label ... for=`,
     `<input type="checkbox"`/`type="radio"`, `:has(`, `:checked`, `:target`,
     `<details>`/`<summary>`, sibling combinators (`~`, `+`) tied to state. These are the
     load-bearing walls. See `references/navigation-and-risk.md`.
   - **Does it use translaty i18n?** Grep for `.en`/`.es` sibling spans, `data-ph-*`,
     `data-aria-*`, an `input[name="lang"]` worldball, `__*Relabel` hooks. If present,
     apply the translaty-aware i18n checks; otherwise fall back to generic i18n.

2. **Detect across all five axes.** Run whatever real tooling is installed, then layer
   the manual checks on top (tools miss a lot, especially mobile and i18n). The full
   catalog of what to check and how to repair each item lives in
   `references/fix-catalog.md` — read it. Tooling, with graceful fallback:
   - HTML + a11y: `npx --no-install html-validate <file>` (exit 0 = clean).
   - CSS: `npx --no-install stylelint <file>` if configured; else the brace/comment
     balance check below.
   - JS: `node --check` on each inline script (extract or use the translaty gate).
   - i18n (translaty apps): `node <translaty>/scripts/check.js <file>` if available —
     it validates span balance, `lang` attrs, escaped `data-*`, and compiles inline JS.

3. **Classify every finding** into Safe / Nav-risk / Standard-divergence using
   `references/navigation-and-risk.md`. This is the step that earns the skill its keep.

4. **Apply the Safe fixes — all of them, every axis.** Edit them in. Crucially: a prompt
   that names one axis ("is this mobile-friendly?", "ready to translate?") tells you where
   to spend *extra depth and judgment* — it is **not** a filter that lets you skip the
   cheap Safe fixes on the other axes. If you enumerated a `doctype-style`, a self-closing
   void element, an unnamed control, or a missing `lang` while looking at mobile, fix it
   too. Leaving a one-character DOCTYPE fix unmade because "they only asked about mobile"
   is the most common way this skill underdelivers. Enumerate every finding first, then
   sweep the whole Safe bucket. Keep a running list of what you changed and why.

5. **Survey the rest.** Batch all Nav-risk and Standard-divergence findings into **one
   inline survey** (see "The survey" below) rather than interrogating the user item by
   item. Apply each according to their choice.

6. **Re-verify.** Re-run the validators and the translaty gate. Do not claim success
   from intent — claim it from a clean re-run. If anything still fails, loop back. Confirm
   the navigation still works by reasoning through each interactive path you touched (and,
   for flove, never open a browser yourself — the user does that; see their preferences).

7. **Report honestly.** What was auto-fixed, what was surveyed and how the user decided,
   what remains and why. If you only covered part of a large file, say so.

## The survey — how and when to ask

Trigger an inline survey when there is **at least one** Nav-risk or Standard-divergence
finding. Ask using the environment's inline question mechanism (in Claude Code, the
`AskUserQuestion` tool). **Never render an HTML form for this** unless the user explicitly
invokes `/questy-html` — answer and ask inline by default (this is a standing user
preference).

Make each question carry enough for a real decision: the issue, the *concrete* fix you'd
apply, **why** it's risky or divergent, and clear options. Good option sets usually look
like: *Apply the fix* / *Apply a safer alternative (describe it)* / *Leave as-is* / (for
divergence) *Apply here and flag it as a new §13 standard to propagate*. Recommend the
option you'd pick and say why — the user is deciding, not guessing in the dark.

Batch related decisions so the user answers a short, coherent set once, not a drip of
pop-ups. If there are zero risky findings, **don't ask anything** — just fix, verify, and
report.

### Headless / non-interactive mode

If you can't reach a human to answer (running as a subagent, a batch job, CI, or any
context with no interactive channel), **never block on the survey.** Instead, write the
survey out *as text* in your report — for each risky finding: the issue, the concrete fix,
why it's risky/divergent, the options, and your recommendation. Then **apply the
recommended option** for each, and clearly label those edits as *"applied on
recommendation — pending user confirmation"* so the human can review and revert. A
recommended fix that preserves navigation (e.g. `inert` over deleting `aria-hidden`) is
the right default; never fall back to the behavior-breaking fix just because no one
answered. The point is to keep moving while leaving a clear paper trail of every judgment
call.

## Quick CSS/JS sanity (when no linter is installed)

A minimum floor when tooling is absent — never the ceiling:
- CSS: braces `{}` balanced, no stray `/* */`, every rule has a selector and a body.
- JS: each inline `<script>` passes `node --check` (write it to a temp file if needed).
- HTML: tags balanced, ids unique, every `for=` points at a real id, every `:has(#x)` /
  `aria-controls`/`aria-labelledby` references a real id.

## What "done right" looked like once (worked example)

When this skill's patterns were first applied by hand to a flove app (`worthing.html`),
html-validate reported 11 errors. They sorted cleanly into the three buckets, which is the
canonical illustration — `references/fix-catalog.md` and `references/navigation-and-risk.md`
walk through each. The headline: the cosmetic and heading-swap fixes went in silently; the
`aria-hidden`-on-focusable arms (fixed with `inert` toggled by JS, not by deleting the
attribute) and the `<a>`-inside-`<ul>` rewrap were surveyed because they touched the magic
menu's navigation and diverged from the other apps' pattern.

## Scope honesty & non-goals

- This skill **does not commit or deploy.** It validates and repairs the working tree;
  any commit/push follows the user's own workflow.
- It does not redesign. If correctness truly requires a redesign (e.g., a color system
  with no accessible contrast anywhere), report it as a finding for the user — don't
  silently restyle the app.
- Coverage honesty over false completeness: a partial, truthful pass beats a confident
  "all fixed" that isn't.
