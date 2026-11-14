---
name: rebrandy
description: >-
  Propagate a flove app's chosen identity — mark/logo, favicon, wordmark, name,
  slogan or accent palette — to every surface it lives on, matching each page's
  own treatment and motion. Use for "make this the new logo everywhere", "apply
  the new mark across all surfaces", "roll out the pentad", "the bio and apps
  indexes too", "and in the appy ones", "propagate the rebrand", "rename this
  app everywhere", or /rebrandy — even when only one extra surface is named.
  Covers the app, logo study, catalog card + cube caption, launchers, demos
  index, appy grids, development tree and favicons; the slogan travels as
  visible text or a hover title. Verifies by rendering. If the mark isn't chosen
  yet, use /brandy stage 1 first. Divergence from the shared standard is
  surfaced, not changed silently.
---

# Rebrand — propagate an app's identity across every surface

## Personal config

See `development/standards/skills/CONFIG.md` for the override routes and keys.

## Before you start — is there a chosen mark?

Rebrandy propagates an identity that already exists. If the owner is still
choosing between logo directions, do **not** sweep the surfaces yet: use
`brandy` stage 1 (5–10 sketches) and wait for the pick. Come back here once one
mark is chosen (or when an existing mark is being replaced).

## The core idea

A flove app's identity is not in one file. Its mark, wordmark, favicon and accent
colour are copied into a dozen places — the app itself, its logo study, the launcher
that lists it, the big demos index, the appy profile grids. So a "small" logo change is
really a **fan-out**: the redraw is the easy 10%; the job is landing it on every surface
without leaving a stale mark behind and without breaking each page's own look.

Two failure modes to avoid, equally:

- **A missed surface** — the new mark ships in the app but the demos index still shows
  the old one. Incomplete rebrands look like bugs. Sweep the whole map (below) every time.
- **A tone-deaf paste** — dropping the app's brand-coloured mark into a gallery that
  renders every mark muted-grey, or a neon spin into a page whose marks are all static.
  Consistency means matching *each surface's* treatment, not stamping one style everywhere.

The guiding question at each surface is: *how does THIS page already treat app marks?*
Then make the new identity behave the same way — only the shape (or word, or colour)
changes.

## What counts as a rebrand

- **Mark / logo** — the app's glyph is redrawn or replaced (e.g. sensy's heart → the Pentad).
- **Favicon** — the `<link rel="icon">` data-URI SVG in the app page's tab and the logo study (can't animate; update the shape/colour).
- **Wordmark / name** — the app's text label changes, or gets a treatment (a shimmer, a split accent).
- **Slogan / tagline** — the one-line promise changes or must reach every surface (visible text where there is room, hover `title` on icon-only surfaces).
- **Palette** — the app's accent colour(s) change and must ripple through its own file and swatches.

Most requests are the mark. The rest follow the same fan-out discipline.

## The surface map — where a flove app's identity lives

Sweep these for the app being rebranded. Not every app touches every row; grep first
(`grep -rl "mark-<app>\|<app>.html\|<App>" apps whole central/shared/media/images` , minus `.git`/worktrees) to find
the real set, then work the list.

| Surface | Where | What to change |
|---|---|---|
| **The app itself** | `apps/<cat>/<app>.html`; for whole-hosted apps, `whole/<field>/<app>/index.html` (e.g. the music projects live in `whole/linguistics/music/<app>/`) | header mark(s) (often 2: topbar + About), favicon, wordmark |
| **Logo study** | `central/shared/media/images/apps/logos/<app>/<app>-logos.html` | the source of truth for the mark + its size ramp + motion |
| **Category / hub launcher** | `apps/<cat>/index.html`; for whole-hosted apps, `whole/<field>/index.html` or `whole/linguistics/music/index.html` | the app's node/tile glyph |
| **Apps index** | `apps/apps-full.html` | the `#mark-<app>` **symbol**, the grid **full card** (category + background classes, name, slogan `.tag`), the **cube** (`#app-<app>`: head, `.cube-tag`, category pill, slides/captions), and the bubbles icon group when relevant |
| **Development tree** | `development/index.html` | the app's `li` under its category `<li class="reveal cat-*">` (link, name, path, hover slogan) |
| **Appy surfaces** | `apps/appy/appy-basic.html`, `appy-mini-full.html`, `profily.html` | each holds its own `#mark-<app>` symbol and the `.appbtn` title/aria (hover slogan) |
| **Bubbles** | `apps/bubbles.html` | the app's `#cloud` symbol + wordmark/favicon if rebranded |
| **Captions / preview** | `central/shared/media/images/apps/captions/<app>.png`, preview modal in `apps/index.html`, cube slides | screenshot + caption (regenerate only if asked) |

### Is this an app?

If the target is an app — it has an app page (`apps/<cat>/<app>.html` or
`whole/<field>/<app>/index.html`), an `apps/apps-full.html` card, or a catalog
entry — **ask** whether to register/update it in the catalogs. Do not skip the
question just because the mark also appears elsewhere.

When yes, follow `development/standards/skills/app-registration.md`:

- the full card + cube caption in `apps/apps-full.html`,
- its category classes and **background/palette class**,
- the `development/index.html` app tree entry under its category,
- the caption PNG and the slogan propagation.

### The one-symbol lever

Index and appy pages define the mark **once** as `<symbol id="mark-<app>">` and reference
it with `<use href="#mark-<app>">` in several spots (app-bar dot, grid tile, cube icon,
logo slide). **Replace the symbol body and every usage updates at once** — you rarely edit
the `<use>` sites. Keep the `id` identical so the references keep resolving; the `viewBox`
may change freely (the family already mixes 24/64/100 viewBoxes).

## Match each surface's treatment — don't fight the page

Read how the target page colours and animates its marks before pasting:

- **Colour**: a gallery mark usually inherits a **category gradient** (`url(#grad-…)`) or a
  **monochrome fill** (`#fff` tiles), and is often shown **grayscale-until-hover**
  (`filter: grayscale(1)`). Give the new mark the *same* fill mechanism the old one used so
  it grayscales and colourises exactly like its siblings. Carry a small brand accent (e.g. a
  magenta core) only where the surface is already colourful; drop it where marks are strictly
  monochrome and it would read as an error.
- **The app's own file is the exception** — there the mark *is* the brand: full brand colour,
  and it animates (see below). The galleries are where it's one of many.

## The slogan travels with the mark

The app's **slogan/tagline** (EN + ES) is part of the identity. Propagate it:

- **Visible text where there is room** — the apps-full tile `.tag`, the cube
  `.cube-tag` and logo-slide caption, the app page's hero/lede or meta, and the
  logo-study hero/lockup.
- **Hover on icon-only surfaces** — native `title` (plus `aria-label` /
  `data-aria-en`/`data-aria-es` where the page supports it): appy `.appbtn`
  (`title="<App> — <slogan>"`), the development tree `.tnode`, launchers and
  category icons with no text slot.
- Keep EN/ES in sync and remove the old slogan everywhere; a stale tagline is
  as visible as a stale mark.

## Motion — as the standard says (`development/standards/index.html` §Principles, §Frontend)

The standard: the brand mark **animates wherever it lives**, **hover interacts** with it,
and **all motion is gated by `prefers-reduced-motion`** — "calm shouldn't mean careless".
Apply that in the app's own file and its logo study:

- Wrap animation rules in `@media (prefers-reduced-motion: no-preference){ … }` so reduce
  turns everything off and the static mark remains.
- A mark can carry more than one animation by comma-listing them, but **two animations
  cannot both drive `transform` on the same element** — combine rotate+scale into one
  keyframe, or split motion (transform) from glow (filter) across the list.
- Hover: pause the spin, or lift/scale — a small affordance, not a second show.
- **Do NOT invent a bespoke spin for a dense gallery** (demos index, launcher) whose app
  marks are all static — that breaks the page's internal consistency. There, static-but-
  correct-logo is the standard-aligned choice. If the user wants motion there too, offer
  hover-spin rather than a resting spin.

## Verify by rendering — never rebrand blind

A rebrand is visual; a wrong path or a broken data-URI is invisible until rendered. After
each surface, **rasterise and look** (this is a firm flove practice):

```bash
# headless Chrome, with the kwallet workaround that keeps it from hanging
google-chrome --headless=new --no-sandbox --disable-gpu \
  --password-store=basic --use-mock-keychain --no-first-run \
  --disable-features=Crashpad --user-data-dir=/tmp/cprof \
  --hide-scrollbars --force-device-scale-factor=2 --window-size=W,H \
  --screenshot=out.png "file:///abs/path/page.html"
```

- Pages that pull Google Fonts hang headless with no network — render a copy with the
  `<link ...fonts...>` stripped.
- To confirm a mark inside a huge file, extract just its `<symbol>` + its gradient `<defs>`
  into a tiny test page and render it at a few sizes (16/24/64) plus grayscale — quicker and
  surer than hunting it in the grid. Then read the PNG.
- Check the mark holds at **16 px** and reads under the page's grayscale filter.

## Close out — scoped commit, then push

Follow the flove Gitea workflow: stage **only the files you touched** (never `git add -A`;
the tree may have parallel edits), commit with the prompt + a short explanation, and push
`origin main` to `localhost:3000/marc/flove`. One commit per coherent surface-set is fine
(e.g. "app + logo study", then "indexes", then "appy") — mirror how the request arrived.

## When to stop and ask

Rename the shape freely; but **surface, don't silently apply**, anything that changes an
app's relationship to the family: dropping a whole surface's treatment (e.g. making one
gallery mark brand-coloured when all others are muted), adding resting motion to a static
gallery, or a name change that ripples into class names / ids / file names (that's a
`/vocaby`-shaped job — hand it off or flag it). A one-line question is cheaper than an
inconsistent rebrand the user finds later.
