# Fix catalog

What to check on each axis and how to repair it. Each item is tagged with its default
bucket — **[Safe]**, **[Nav-risk]**, or **[Divergence]** — but the bucket is a *default*,
not a law: the same fix can shift buckets depending on context (a heading swap is Safe
unless the heading itself is the click target; rewrapping a node is Safe unless a CSS
combinator depends on the old structure). When the context pushes a Safe item toward risk,
move it to the survey. See `navigation-and-risk.md` for how to read that context.

## Table of contents
1. HTML validity
2. Accessibility (a11y)
3. CSS validity
4. JavaScript validity
5. Mobile-friendliness
6. Internationalization (i18n)

---

## 1. HTML validity

- **[Safe] DOCTYPE casing** — `<!doctype html>` → `<!DOCTYPE html>` (html-validate's
  `doctype-style`). Pure style, zero effect.
- **[Safe] Void elements self-closing** — `<meta .../>`, `<br/>`, `<img .../>` → drop the
  `/` (`void-style`). HTML void elements don't take a closing slash. No effect.
- **[Safe] Duplicate `id`** — rename the later one *unless* an `id` is referenced by a
  `for=`, `:has(#id)`, `aria-controls`, `href="#id"`, or JS `getElementById`. If it is
  referenced, this is **[Nav-risk]** — renaming can sever the wiring.
- **[Safe→Nav-risk] Invalid nesting** — e.g. `<a>` directly inside `<ul>`, `<div>` inside
  `<p>`. Wrap or re-parent (`<a>` → `<li><a>…</a></li>`). Safe *unless* the parent is a
  CSS grid/flex container whose child styling targets the old child — then move the layout
  rule onto the new wrapper in the same edit, and if a combinator depends on the old
  structure it becomes **[Nav-risk]**.
- **[Safe] Stray/obsolete attributes** — remove `align`, `bgcolor`, etc. only when a CSS
  equivalent already exists or you add it; otherwise report.

## 2. Accessibility (a11y)

- **[Safe] `<html lang>` missing** — add it (`lang="en"` or the page's real base
  language). For translaty apps the engine already syncs this on switch; just ensure the
  static default is present.
- **[Safe] `aria-label` on an element that can't take it** — a bare `<div>`/`<span>` with
  no role can't carry `aria-label` (`aria-label-misuse`). Add an appropriate `role`
  (`role="group"`, `role="img"`, etc.) so the name is legal. Adding a role to a generic
  container doesn't change behavior.
- **[Safe] Heading inside an interactive element** — `<h2>`/`<h3>` inside a `<label>` or
  `<button>` (`element-permitted-content`). Swap the heading tag for a `<span>` (or a
  `<div role="heading" aria-level="n">` if the heading semantics matter) and move the
  heading's **class-based** styling to the new tag. **The trigger stays** (`<label for>` /
  `<button>`), so the click/keyboard behavior is identical. If the CSS targeted the bare
  tag (`.resume h3`), update the selector to a class in the same edit.
- **[Nav-risk] `aria-hidden` on a focusable element** — `aria-hidden="true"` on (or
  wrapping) something with `tabindex`, a link, or a control (`hidden-focusable`). **Do not
  just delete the attribute** — that leaves a focusable-but-invisible node in the tab
  order, a different bug. The correct fix depends on intent: if the element is hidden only
  *visually* while collapsed (max-width:0 / overflow / off-screen), drive `inert` on it
  from the state that controls visibility (a small JS handler mirroring the checkbox/menu
  state) so it leaves both the tab order and the a11y tree when closed and returns when
  open. Because this adds JS and changes focus behavior, **survey it** — and in a flove
  distro it's usually also **[Divergence]** (other apps may still use `aria-hidden`).
- **[Safe] Decorative image/SVG without alt** — `alt=""` (and `aria-hidden="true"` +
  `focusable="false"` on decorative inline SVG). For **meaningful** images with no alt,
  the text is a content judgment → **survey** the proposed alt text.
- **[Safe] Control without an accessible name** — an icon-only `<button>`/`<a>` → add
  `aria-label` (and, for translaty apps, the matching `data-aria-en/-es`). Naming a
  control doesn't change what it does.
- **[Nav-risk] `tabindex` > 0** — positive tabindex fights the natural order. Reducing to
  `0`/removing changes focus flow → survey.
- **[Safe] Form input without a label** — associate via wrapping `<label>` or
  `for`/`id`. Report if the visual design has no obvious label slot.
- **Styling for a11y fixes goes in CSS, not inline.** When adding a visually-hidden label,
  a `<legend>`, or a focus outline, attach a **class** (e.g. `.visually-hidden`) or a CSS
  rule — never an inline `style=` attribute. An inline style trips `no-inline-style` (a
  rule many flove apps enforce), so you'd swap one finding for another. Add the utility
  class definition once if it's missing, then reuse it.
- **[Report] Color contrast below WCAG AA** — can't be auto-fixed without a design call.
  Report the failing pairs with measured ratios; if the user wants it fixed, that's a
  **survey** (palette change = behavior-neutral but design-affecting and often
  **[Divergence]**).
- **[Safe] Missing `:focus-visible` styling** — if interactive elements have no visible
  focus state, add a non-intrusive `:focus-visible` outline. Additive, doesn't alter
  layout or behavior.

## 3. CSS validity

- **[Safe] Unbalanced braces / unterminated comments** — fix the structural error.
- **[Safe] Unknown/duplicate properties, invalid values** — correct or drop (stylelint).
- **[Safe] Vendor-prefix gaps** — add the standard property alongside a lone prefixed one
  (`-webkit-background-clip:text` → also `background-clip:text`). Additive.
- **[Nav-risk] Editing a selector that drives state** — anything matching
  `:has(#id:checked)`, `#id:checked ~ …`, `:target`, `details[open]`. Correctness edits
  here can change *when* UI shows. Survey unless the change is provably inert.

## 4. JavaScript validity

- **[Safe] Syntax errors / `node --check` failures** — fix the parse error.
- **[Safe] Obvious bugs with no behavior change** — a missing `?.`, an unguarded
  `querySelector` that can return null. Add the guard.
- **[Nav-risk] Changing event wiring or state logic** — if a "fix" alters which elements
  get listeners, the toggle logic, or the order of state updates, it can change
  navigation. Survey.
- Prefer **adding** small, well-commented JS (e.g. an `inert` sync) over rewriting
  existing handlers. Explain *why* in a comment so the next reader understands the a11y
  intent.

## 5. Mobile-friendliness

- **[Safe] Viewport meta missing/wrong** — ensure
  `<meta name="viewport" content="width=device-width,initial-scale=1">`.
- **[Safe] Zoom disabled** — remove `user-scalable=no` / `maximum-scale=1` from the
  viewport meta; blocking pinch-zoom is an a11y failure. Restoring zoom doesn't change
  layout.
- **[Nav-risk→Safe] Tap targets < ~44px** — interactive controls smaller than ~44×44px
  are hard to hit. Bumping `min-width/min-height`/padding is usually Safe, but if it
  reflows a tightly-packed toolbar it can shift layout → judge per case; survey if it
  visibly changes the design.
- **[Safe] Horizontal overflow** — replace fixed pixel widths that exceed the viewport
  with `max-width`/`%`/`min()`; add `overflow-x` guards where appropriate. Verify against
  a narrow width.
- **[Safe] iOS input zoom** — inputs with `font-size` < 16px trigger auto-zoom on focus;
  raise to ≥16px (or accept if intentional and documented).
- **[Report] No responsive breakpoints** — if a layout is desktop-only with no media
  queries / fluid units, report it; a responsive redesign is a survey/design task, not a
  silent fix.
- **[Safe] Hover-only affordances** — if something is reachable *only* via `:hover`, add a
  tap/focus path so touch users aren't locked out.

## 6. Internationalization (i18n)

**If the app uses translaty** (detected by `.en`/`.es` sibling spans, the worldball,
`data-ph-*`/`data-aria-*`):
- **[Safe] Unwrapped visible string** — wrap in per-language sibling spans with `lang`
  attributes, matching the existing pattern. (For a real translation pass, defer to the
  `translaty` skill — this skill flags the gap and can fill obvious ones.)
- **[Safe] Attribute text not translatable** — `placeholder`/`aria-label`/`<option>` with
  no `data-ph-*`/`data-aria-*`/`data-en` companions → add them.
- **[Safe] Span imbalance / missing `lang`** — fix so every language has a sibling and
  every span carries `lang`. Run the translaty `check.js` gate to confirm.
- **[Nav-risk] Hardcoded user-facing string inside JS** that bypasses the language maps —
  route it through the existing i18n helper instead. Touching JS string flow can affect
  output → survey if non-trivial.
- **[Divergence] Missing a language other apps have**, or a worldball missing where the
  distro standard has one — survey (is this app meant to be bilingual yet?).

**If the app does NOT use translaty** (generic i18n hygiene):
- **[Safe]** `<html lang>` present and correct; add `dir="rtl"` only if a RTL language is
  actually in use.
- **[Report]** Hardcoded user-facing strings with no externalization, dates/numbers
  formatted for one locale, text baked into images. Report; externalizing is a larger
  task to scope with the user.
