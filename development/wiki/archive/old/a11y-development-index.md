# Accessibility — `development/index.html` (static gate)

> **Scope / Ámbito:** EN: Archived result of the static accessibility gate on the canonical Docs · Plan/Work page. · ES: Resultado archivado de la comprobación estática de accesibilidad de la página canónica Docs · Plan/Work.

**Date:** 2026-11-20
**Tool:** `tools/check-a11y.py` (`check()` applied to `development/index.html`; the script's CLI only walks `tools/routing.json`, so the same function is called directly for this page)
**Result:** 0 issues (re-checked 2026-11-20 after the `<h1>` fix).

| Check | Outcome |
|---|---|
| `main` landmark | ok |
| `<h1>` | ok · one sr-only bilingual `<h1>` at the top of `<main>` |
| `prefers-reduced-motion` | ok |
| bilingual spans with `lang` | ok |
| positive `tabindex` | ok |
| `role=button/menuitem` focusable | ok |
| placeholder links `href="#"` | ok |
| `<img>` with `alt` | ok |
| named form controls | ok |
| `outline:none` with `:focus` | ok |

**Finding (resolved):** the page used to open with `<div class="work-tracker">` and `<h2>` headings. A single visually hidden bilingual `<h1>` now sits at the top of `<main>`. `tools.check(Path("development/index.html"))` returns `[]`; the i18n/structure gate (`node development/scripts/check.js development/index.html`) is clean: balanced spans, unique ids, escaped `data-*`, balanced CSS and compiling inline JS.
