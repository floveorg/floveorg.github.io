# flove · Frontend contract (mandatory)

The **non-negotiable** rules every flove app follows — identity, tokens,
CSS-over-JS, file pattern, the a11y floor, anti-patterns. This is the stable
core; the *opt-in* patterns catalogue lives in `frontend.md`, and the
at-a-glance index in `README.md` (this folder's matrix). Philosophy:
`../worldview.md`. Architecture: `../backend.md`. Plans & conflicts:
`../plans/index.md`. Live token source of
truth: `flove.css` — these notes summarize and constrain it.

## 0. Stance

**Slow it · flow it · love it.** Low-tech, relational, no flashy AI.
Calm motion, breathable layouts, generous whitespace. If a feature
*feels* hypey or "AI-cool", it does not belong in flove.

## 1. Identity primitives (mandatory in every app)

Every demo HTML file MUST keep:

1. **The flove sprout mark** — an inline `<svg class="flove-mark">` inside the
   flove-bar. The sprout is the non-negotiable flove identity: two warm leaves
   and a stem (viewBox `0 0 100 100`, stroke `stroke-width="5"
   stroke-linecap="round" stroke-linejoin="round"`, warm gradient
   `#ff3344→#ff8a3a→#ffd633`). The canonical master is
   `images/apps/logos/flove/flove-logos.html`; the gradient + paths are
   **inlined** into the flove-bar per file — do NOT use external `<use>`
   (Chrome blocks `file://` cross-document SVG references). Where the mark
   appears in a text-only context (prose bullets, exports, canvas `fillText`,
   titles, JS icon arrays), use the **🌱 seedling glyph** as the sprout
   equivalent. The old asterism `✺` is retired — it is never the identity.
   (See `frontend.md §13.7` · *Mark propagation* + *App image assets — the
   logos folder*.)
2. **The flove-bar** — sticky strip at the very top with the back link
   to `index.html`, the flove sprout mark (point 1), and the app name.
   Use `.flove-bar` / `.flove-bar--auto` (auto dark) / `.flove-bar--dark`.
3. A **single accent palette** declared in the page's local `:root`
   via the `--app-accent*` tokens. Never hard-code accent colors mid
   stylesheet. The mark's gradient stops come from the app's category
   palette (the 7 canonical category colors; see the app's
   `images/apps/logos/<app>/<app>-logos.html`).

## 2. Token discipline

Always prefer tokens from `flove.css` (or `flove-base.css`) over ad-hoc values.
The complete canonical token table — apps may override these in their local
`:root` but must not invent new surface or semantic tokens:

### Surface palette

| Token | Purpose | Light | Dark |
|-------|---------|-------|------|
| `--bg` | page background | `#f3f4fb` | `#0b0b0f` |
| `--ink` | primary text | `#16141f` | `#e9eaf2` |
| `--muted` | secondary text | `#4a4e5a` | `#a3a7b4` |
| `--line` | borders, dividers | `#e3e5f0` | `#1e2133` |
| `--card` | card/panel backgrounds | `#ffffff` | `#11131a` |
| `--panel` | elevated surfaces | `#edeef7` | `#11131a` |

### Semantic palette

| Token | Purpose | Light | Dark |
|-------|---------|-------|------|
| `--accent` | brand / interactive | `#6c5ce7` | (inherited) |
| `--accent-soft` | soft accent variant | `#5347c4` | (inherited) |
| `--signal` | success / positive | `#02855c` | (inherited) |
| `--warn` | caution | `#b9820a` | (inherited) |
| `--danger` | error / destructive | `#dd3b3b` | (inherited) |

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

**Rules:**
1. Apps must use these token names — inventing `--text` instead of `--ink`,
   `--surface` instead of `--card`, or `--border` instead of `--line` is
   forbidden in new code.
2. Backward-compatible aliases (`--text: var(--ink)`) are acceptable during
   migration but must be removed once all references are updated.
3. Each app declares its own background/ink palette in its local `:root`,
   but must keep the family geometry and motion tokens.
4. The canonical token source of truth is `flove.css` (full) or
   `flove-base.css` (foundation only).

## 3. CSS over JS (firm)

Implement with CSS first. Reach for JS only when CSS literally cannot
express it (state machines, data, persistence). Examples:

- Reveal/hover/focus/expand → `:hover`, `:focus-visible`, `:has()`,
  `details/summary`, `popover`, anchor positioning. Not JS.
- Theming → CSS custom properties + `@media (prefers-color-scheme)`.
  Not a JS theme switcher.
- Layout reflow → container queries / grid. Not JS measuring.

If you find yourself writing a `useEffect`-style listener for layout,
stop and look for a CSS answer.

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

## 5. Visual verification

No browser-automation MCP is available in this environment — verifying
visually is Marc's job, not Claude's. After any visual change:

1. Describe in plain text **what you changed and where to look** — the
   selectors, the layout zone, the breakpoint that matters.
2. Flag explicitly which states need attention (mobile ~390px, dark
   mode if the app supports it, focus rings, reduced motion).
3. State explicitly that you have not verified visually; never claim a
   UI works without it having been opened.

Marc loads the page in his own browser to confirm. If something looks
off, he reports back and you iterate. Don't try to launch a browser,
take screenshots, or call playwright/chrome-devtools — they're not
wired and the attempts only add noise.

**One exception — vector artwork.** For a *self-contained SVG* (a logo mark,
icon, or symbol) you may rasterize it to PNG (`convert`, or headless chromium
when filters/clips are involved) and read the image to check the shape before
committing — that's inspecting a static asset, not driving a page, and it beats
iterating blind. Whole-page layout, motion, and responsive states still need
Marc's browser.

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
- Adding a JS dependency to do what CSS can do (see §3).
- Overriding `.flove-bar` styles per-app — extend with a modifier class.
- Heavy gradients, neon glows, or "AI-shimmer" effects.
- Modal-stacked, dense, dashboard-like layouts. Flove breathes.
- Removing the flove sprout or the back-to-launcher link.

## 8. When in doubt

Re-read `flove.css` and `index.html` (the launcher) — they are the
canonical reference for the family look. Match their restraint.

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

## 10. The harvested catalogue → `frontend.md`

The opt-in patterns (tier model, i18n, compass, topbar, onboarding, canonical
vocabulary, counters, summary, surfaces, export, locking, theme —
**§13.1–§13.14**) live in **`frontend.md`**; the per-app **adoption checklist
(§14)** in **`adoption.md`**; the at-a-glance index in **`README.md`**.

When Marc names a pattern ("tier model", "compass", "topbar", "surfaces",
"forms-iframe", "i18n t-en", "export", "locking"…), look it up in
`frontend.md §13.x` before doing anything. `ray-*`/`bot-*` are the **old**
vocabulary — use `labeler-*`/`wizard-*` (§13.7).
