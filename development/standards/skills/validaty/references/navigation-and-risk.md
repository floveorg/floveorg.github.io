# Navigation & risk classification

This is the heart of the skill. A validator sees markup; it doesn't see *what makes the
page work*. Your job is to see both, so that a "fix" never silently severs an interaction.
This file explains how to recognize the load-bearing structures and how to decide which
bucket a fix belongs in.

## Why this matters

Many single-file apps — and essentially every flove app — drive their UI with **no
JavaScript for navigation**. State lives in hidden form controls, and CSS reacts to it.
That means ordinary-looking markup is secretly load-bearing: a `<label>` is a button, an
`<input>` you can't see is the app's memory, and the *position* of a node in the DOM can
be the thing that makes a panel open. Delete or rewrap the wrong one and the lights go
out — but the linter will have called it an improvement.

So before editing, find the wiring. After that, classifying fixes is mostly mechanical.

## Recognizing CSS-only navigation

Grep for these and trace what each one controls:

| Tell | What it usually means |
|------|------------------------|
| `<label … for="x">` | A clickable trigger for the control with `id="x"`. The label *is* the button. |
| `<input type="checkbox" id="x">` / `type="radio"` | The state store. Often visually hidden (`opacity:0;position:absolute`) but **functionally essential** and frequently focusable. |
| `body:has(#x:checked) …` | The page reacts to that control's state. The `#x` id and the `:checked` state are load-bearing. |
| `#x:checked ~ .panel` / `+ .label` | Sibling-combinator reaction — depends on **DOM order and adjacency**. Rewrapping or reordering siblings can break it. |
| `:target` + `href="#x"` | Anchor-driven state; the `id` and the link target are wired. |
| `<details>`/`<summary>` | Native disclosure; the `<summary>` is the trigger. |
| `.tier-pop-step` / `.level-pop-step` (flove) | Tier navigation between mini/basic/normal/advanced variants. |

Build a quick mental (or written) map: *control id → what reacts to it → what triggers
it*. Every fix that touches a node in that map is at least Nav-risk until proven Safe.

## The decision procedure

For each finding, ask in order:

1. **Does the fix change, move, rename, or rewrap a node in the navigation map?**
   (a `for=` target, a stateful `id`, a `:checked`/`:has`/`:target` selector, a control,
   or a sibling whose adjacency a combinator relies on)
   → **Nav-risk.** Survey it.

2. **Does the fix add or alter JavaScript that affects focus, events, or state?**
   (e.g. introducing an `inert` sync, rewiring a listener)
   → **Nav-risk.** Survey it — even when it's the *correct* a11y fix.

3. **Is the fix correct and behavior-neutral, but would it make this app differ from the
   shared flove pattern** used by sibling apps / the §13 standards?
   → **Standard-divergence.** Survey it as a distro decision (apply here only, or adopt as
   a new standard and propagate).

4. **Otherwise** — the fix cannot change behavior or layout, and doesn't touch the map.
   → **Safe.** Apply it silently and report afterward.

When two answers conflict (e.g. a fix is both behavior-neutral *and* divergent), the more
cautious bucket wins — surface it.

## Preserving navigation while still fixing the error

The skill exists because you usually **can** satisfy the validator *and* keep behavior.
Patterns that thread the needle:

- **Heading inside a trigger** → swap only the *tag* (`<h2 class="brand">` → `<span
  class="brand">`), keep the `<label for>`/`<button>` wrapper. Behavior identical; move
  tag-based CSS to the class. This is Safe.
- **`aria-hidden` on a visually-collapsed, focusable menu** → don't delete the attribute.
  Add a tiny JS handler that sets `.inert` on the collapsed container, mirroring the
  checkbox that controls its visibility. `inert` removes it from the tab order **and** the
  a11y tree when closed, and restores it when open — the real fix, not the linter-silencing
  one. Nav-risk (adds JS, changes focus) → survey, and usually Divergence too.
- **`<a>` directly inside `<ul>`** → wrap in `<li>` and **move the grid/flex placement**
  (e.g. `grid-column:1/-1`) from the `<a>` onto the new `<li>` in the same edit, so the
  layout is preserved. Safe *if* no combinator depended on the `<a>` being a direct child;
  Nav-risk if one did.
- **`aria-label` on a bare container** → add `role="group"` rather than removing the
  label. Safe.

The common thread: **keep the trigger, keep the DOM relationships the selectors rely on,
and move styling rather than dropping it.** If you can't do the fix without disturbing one
of those, that's your signal to survey instead of edit.

## A note specific to flove

- The whole distro shares this CSS-only pattern, so a fix that's locally correct can still
  be a *standard* decision. The principle: don't let one app silently drift from the
  others. When you'd improve one app in a way the siblings don't yet have, raise it as
  Divergence so the user can choose to propagate it to the §13 standard instead of leaving
  an inconsistency.
- Don't open a browser to "verify" visually — the user does that themselves. Verify by
  re-running the validators and by reasoning through each interaction path you touched.
