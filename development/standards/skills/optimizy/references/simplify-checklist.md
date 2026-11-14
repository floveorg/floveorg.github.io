# Manual simplify pass

Use this when `/simplify` (or the `code-simplifier` agent) is unavailable.
Goal: **shrink the file without changing behaviour.** This is not a bug hunt —
that is the code-review stage.

## Before

- Record the baseline: file size, `html-validate` result, and the navigation
  paths you will re-check.
- Profile the load-bearing walls (see optimizy): `label for=`, radio/checkbox,
  `:checked`, `:has(`, `:target`, state-bound `~`/`+`, `<details>`/`<summary>`,
  and every class/id a selector or lookup keys on.

## Pass

- Remove dead CSS selectors, unused JS functions/variables, commented-out
  blocks, duplicated helpers and stale assets.
- Merge duplicate rules only when the cascade is provably identical. Never
  collapse or rename a selector that drives navigation, theme, i18n or state.
- Reuse an existing utility/class instead of adding a new abstraction.
- Keep behaviour identical: theme, language switch, audio, dialogs, export and
  share.
- Do not touch source text or names; this is a structural shrink only.

## After

- `html-validate` is clean.
- Re-check every interactive path that touched a load-bearing wall.
- Render at 390 px and 1280 px.
- Report what was removed, the size delta, and anything intentionally kept.
