# flove · Frontend contract (mandatory)

The **non-negotiable** rules every flove app follows — identity, tokens, file pattern, the a11y floor, anti-patterns. This is the stable
core; the *opt-in* patterns catalogue lives in `frontend/frontend.md`, and the
at-a-glance index in `README.md` (this folder's matrix). Philosophy:
`worldview.md`. Architecture: `backend.md`. Plans & conflicts:
`debates/plans/index.md`. Live token source of
truth: `flove.css` — these notes summarize and constrain it.

## 0. Stance

**Slow it · flow it · love it.** Low-tech, relational.
Calm motion, breathable layouts, generous whitespace. 


## 2. Token discipline

### Effects

| Token | Purpose | Light | Dark |
|-------|---------|-------|------|
| `--glow-a` | accent glow | `rgba(108,92,231,.20)` | `rgba(141,137,255,.18)` |
| `--glow-s` | signal glow | `rgba(3,168,119,.16)` | `rgba(3,168,119,.14)` |
| `--glass` | glassmorphism bg | `rgba(255,255,255,.82)` | `rgba(17,19,26,.85)` |
| `--glass-border` | glassmorphism border | `rgba(108,92,231,.16)` | `rgba(141,137,255,.18)` |

### Layout

| Token | Purpose | Value |
|-------|---------|-------|
| `--nav-h` | bottom nav height | `56px` |
| `--safe-b` | safe area bottom | `env(safe-area-inset-bottom,0px)` |
| `--safe-t` | safe area top | `env(safe-area-inset-top,0px)` |
| `--transition` | default transition | `.3s ease` |

### Per-app accent tokens (Solo distro)

| Token | Purpose |
|-------|---------|
| `--app-accent` | app's accent color |
| `--app-accent-soft` | soft variant |
| `--app-ink-on-accent` | text color on accent bg |

### Geometry tokens (Solo distro)

| Token | Value |
|-------|-------|
| `--flove-radius-sm` | `12px` |
| `--flove-radius` | `20px` |
| `--flove-radius-lg` | `28px` |
| `--flove-radius-pill` | `999px` |

### Motion tokens (Solo distro)

| Token | Value |
|-------|-------|
| `--flove-ease` | `cubic-bezier(.2,.8,.2,1)` |
| `--flove-fast` | `.15s var(--flove-ease)` |
| `--flove-medium` | `.25s var(--flove-ease)` |
| `--flove-slow` | `.4s var(--flove-ease)` |

### Font tokens (Solo distro)

| Token | Value |
|-------|-------|
| `--flove-font-ui` | `'Inter', system-ui, sans-serif` |
| `--flove-font-display` | `'Georgia', serif` |



## 4. File pattern

A flove demo is a **single self-contained HTML file**:

```
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />
  <title>{App} · FLOVE</title> <!-- app name · FLOVE; app favicon; no sprout glyph in the title — frontend.md §13.10 -->
  <link rel="stylesheet" href="flove.css" />
  <style>
    :root { --app-accent: …; --app-accent-soft: …; --app-ink-on-accent: …; }
    /* app-local styles */
  </style>
</head>
<body>
  <nav class="flove-bar"> … </nav>
  <main> … </main>
</body>
</html>
```

Use `_template.html` as the starting point. Do not introduce a build
step, framework, or bundler. Vanilla HTML + CSS + small JS only.



## 6. Accessibility floor

- Every interactive element has a visible `:focus-visible` state.
- Color contrast ≥ 4.5:1 for body text against its background.
- Hit targets ≥ 40×40 px on touch.
- Animations respect `@media (prefers-reduced-motion: reduce)`.
- Decorative sprout glyphs are `aria-hidden="true"`.
- **Collapsed-but-rendered panels stay out of the a11y tree.** A panel
  hidden via `max-width:0` / `opacity:0` / `transform` (not `display:none`)
  still keeps its focusable controls in the tab order + screen-reader tree
  while invisible. Remove them when closed: **JS builds** mirror the toggle
  with `el.inert = !open` (CSS can't toggle `inert`; reference:
  `worthing.html` `.magic-arms` ↔ `#magic-open`); **`-0` / CSS-pure builds**
  add `visibility:hidden` to the closed state (+ `visibility 0s linear <dur>`
  on the close transition so the animation isn't cut). Panels already
  `display:none` when closed need nothing.

## 7. Anti-patterns (do not do)

- Inventing a new accent / radius / easing instead of using the token.
- Overriding `.flove-bar` styles per-app — extend with a modifier class.
- Modal-stacked, dense, dashboard-like layouts. Flove breathes.


## 9. Versioning

Flove uses **adoption-driven versioning**: versions are tagged when standard
completions are adopted, not by arbitrary dates.

| Element | Format | Example |
|---------|--------|---------|
| Version number | `YY-M` (year-month) | `26-6` |
| Intra-month releases | `YY-M.N` | `26-6.1`, `26-6.2` |
| Changelog button | Footer of every page | `<button id="changelog-btn">` |

**Rules:**
1. Version bumps on **standard adoption completions** (§14 checklist items).
2. The version number is the **adoption date**: `26-6` = June 2026.
3. If multiple adoptions happen in one month, append `.1`, `.2`, etc.
4. Every page carries a **changelog button** in the footer linking to the
   version history (see `frontend.md §13.x` for implementation).
5. **Android APK** (`updaty-apk`) version aligns with milestones — recompile
   and publish to GitHub Releases when adoption milestones are reached.

## 10. The harvested catalogue → `frontend/frontend.md`

The opt-in patterns (tier model, i18n, compass, topbar, onboarding, canonical
vocabulary, counters, summary, surfaces, export, locking, theme —
**§13.1–§13.14**) live in **`frontend/frontend.md`**; the per-app **adoption checklist
(§14)** in **`adoption.md`**; the at-a-glance index in **`README.md`**.

When Marc names a pattern ("tier model", "compass", "topbar", "surfaces",
"forms-iframe", "i18n t-en", "export", "locking"…), look it up in
`frontend.md §13.x` before doing anything. `ray-*`/`bot-*` are the **old**
vocabulary — use `labeler-*`/`wizard-*` (§13.7).
