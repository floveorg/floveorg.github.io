# Manual code-review pass

Use this when `/code-review` is unavailable. This is the **bug pass** on clean,
final, single-language code — not a simplification or style pass.

## Read for

- **Navigation:** CSS-only tabs/menus, radio/checkbox state, `label for=`,
  `:checked`, `:has(`, `:target`, `~`/`+` combinators, `<details>/<summary>`,
  dialogs. A rename or collapse here can silently kill nav.
- **JS:** event listeners, null guards, async/audio errors, theme persistence,
  language switch, export/share/import paths.
- **CSS-over-JS:** flag JS that reinvents `:has()`, `details`, or
  `prefers-color-scheme` where CSS answers (§3 normative).
- **Mobile/a11y:** focus order, labels, touch targets, reduced motion, contrast.

## Verify

- `html-validate` is clean.
- Render at 390 px and 1280 px.
- Exercise every interactive path: tabs, menus, dialogs, audio, language, theme,
  export/share.
- Test export → save → re-import/load where the app supports it.

## Report

- Findings with severity (blocker / bug / regression risk), file and line.
- Do not fix in this pass — optimizy fixes after the review, before translaty.
- Say explicitly what you did **not** review.
