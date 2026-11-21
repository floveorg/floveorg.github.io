---
name: validaty
description: >-
  Check and repair a web page or single-file HTML app for basic compliance —
  HTML, CSS, JS and embedded JSON — plus accessibility, mobile and i18n
  readiness, protecting its navigation; then suggest UX improvements. Use for
  /validaty, "fix the errors", "check my a11y", "make it mobile-friendly".
category: sys
checker_of:
  - https://flove.org/development/standards/adoption.md
  - https://flove.org/development/standards/contract.md#the-floor

---

# validaty

Find and repair validity, a11y, mobile, i18n and JSON problems without changing
behaviour. A validator will happily delete an `aria-hidden`, rewrite a heading or
rewrap a node — any of those can break a navigation pattern. A fix that breaks
navigation is worse than the error it removes.

The last step is advice, not edits.

## Workflow

1. **Read and profile the target.** Map two things before touching anything:
   - **CSS-only navigation?** `label … for=`, `type="checkbox"`/`radio`,
     `:has(`, `:checked`, `:target`, `<details>`/`<summary>`, state-bound `~`/`+`.
     These are the load-bearing walls.
   - **translaty i18n?** `.en`/`.es` sibling spans, `data-ph-*`, `data-aria-*`,
     `input[name="lang"]`, `__*Relabel`. If present, apply the translaty-aware
     i18n checks; otherwise the generic ones.

2. **Detect across every axis.** Real tooling first, manual checks on top
   (linters miss mobile, i18n and JSON):
   - HTML + a11y: `npx --no-install html-validate <file>` (exit 0 = clean).
   - CSS: `npx --no-install stylelint <file>` if configured; else the sanity floor.
   - JS: `node --check` on each inline script.
   - JSON: parse every embedded block — `<script type="application/json">`,
     `flove-fields`, JSON-LD, seeded state. See **JSON compliance** below.
   - i18n: `node <translaty>/scripts/check.js <file>` when the app is translated.
   - Local artifacts: every `href`, `src`, `fetch()` path, audio base and path
     cited in a comment resolves relative to the repo; CSS selector lists end
     in a body (no trailing comma).

   The catalog axes are HTML validity, a11y, CSS, JS, mobile and i18n; each fix is
   **Safe** unless it touches the navigation map — `label for=`, a stateful `id`,
   `:checked`/`:has`/`:target`, a sibling combinator, `<details>`, or a JS string
   lookup. Any change to those is **Nav-risk**; a deviation from the §13 pattern is
   **Divergence**. Preserve the trigger and DOM adjacency; move layout rules to a
   new wrapper in the same edit.

3. **Classify every finding** into Safe / Nav-risk / Standard-divergence
   and survey the risky ones.

4. **Apply every Safe fix, every axis.** Naming one axis adds depth, not a
   filter: a `doctype-style` or missing `lang` spotted while checking mobile gets
   fixed too. Enumerate, then sweep. Keep a list.

5. **Survey the rest** — one batched inline survey, per
   `https://flove.org/development/standards/skills/standing.md` rule 3. Apply each
   per the owner's choice.

6. **Re-verify.** Re-run the validators and the translaty gate; claim success from
   a clean re-run, never from intent. Reason through every interactive path you
   touched. Never open a browser — the owner does that; see [`standing.md`](https://flove.org/development/standards/skills/standing.md).

7. **Report honestly.** Auto-fixed, surveyed + decisions, what remains and why.
   Partial coverage on a large file is stated, not implied away.

8. **Suggest UX improvements — do not apply them.** With the page clean, end
   with a short list (3–7 items) of what would make it *better*, each with the
   reason and the cost: wording, flow, empty states, focus order, tap targets,
   feedback after an action, a missing shortcut, a section that needs a way back.
   Mark the list clearly as suggestions. Apply one only when the owner says so —
   a redesign is never part of a compliance pass.

## The axes

| Axis | Basic compliance means |
|---|---|
| HTML | valid nesting, unique `id`, every `for=`/`aria-controls`/`:has(#…)` resolves, `lang`, a `title` |
| CSS | balanced braces and comments, every rule has a selector **and a body** (no trailing comma), no dead duplicate |
| JS | every inline script passes `node --check`; no unreachable handler, no selector that matches nothing |
| JSON | every embedded block parses, no duplicate keys, no unescaped `</script>`, the schema/version string is present |
| a11y | alt text, labels, heading order, focus visible, ARIA used as intended — never deleted to silence a warning |
| mobile | viewport meta, no fixed width, tap targets, content that scrolls inside its panel |
| i18n readiness | `lang` present, text extractable, no sentence built by string concatenation (translaty owns the wrapping) |

## JSON compliance

Everything that ships as JSON must parse and agree with itself:

- `JSON.parse` every `<script type="application/json">` block (a browser parses
  it lazily and silently ignores a broken one, so a syntax error can hide for
  months). The same for `flove-fields`, JSON-LD, seeded state and any
  `data-json` attribute.
- Duplicate keys are legal JSON but a real bug: keep the last and remove the
  rest, then say so.
- Escape `<` in strings that could contain `</script>`, and `&`/`<`/`>` where
  the value is interpolated into markup.
- The declared `schema`/`version` string exists and matches the rest of the
  file; ids in the JSON match ids in the markup.
- Do not "fix" JSON by deleting keys the code reads — a parse error is a repair,
  a schema change is a survey item.

This is syntax and internal agreement, not a schema audit: `exporty` and `jsony`
own the portrait and routing contracts.

## Quick CSS/JS sanity (when no linter is installed)

A floor, never a ceiling:

- CSS: braces balanced, no stray `/* */`, every rule has a selector and a body.
- JS: each inline `<script>` passes `node --check` (temp file if needed).
- HTML: tags balanced, ids unique, every `for=`, `:has(#x)`, `aria-controls`
  and `aria-labelledby` points at a real id.

## Orchestration mode

Running as the **validaty stage of `/optimizy`** (`https://flove.org/development/standards/skills/optimizy/SKILL.md`):

- The app is still single-language; translaty is last. Make the page i18n-**ready**
  (`lang` present, text extractable, no string-concatenated sentences) and stop —
  no `.es` spans, no worldball, no translation.
- `texty3` ran before you: naming is settled. Report a bad name, don't rename.
- `/code-review` runs after you: stay on validity/a11y/mobile/JSON; flag logic smells.
- The UX suggestions go in the ledger for the orchestrator's report — they do not
  become edits mid-pass.
- Return findings as text; the orchestrator surveys, reports and commits.

Standing rules: `https://flove.org/development/standards/skills/standing.md`.
