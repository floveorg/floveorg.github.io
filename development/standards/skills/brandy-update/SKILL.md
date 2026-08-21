---
name: rebrandy
description: >-
  Roll a flove app's changed identity — its logo/mark, favicon, wordmark, name, or
  accent palette — out to EVERY surface it appears on, consistently and following the
  flove standards. Use this whenever a mark or logo is redrawn or replaced and needs to
  propagate: "make this the sensy logo everywhere", "apply the new mark across all
  surfaces", "the app's icon changed — update it everywhere", "roll out the pentad", "the
  bio and apps index(s) too", "and in the appy ones too", "propagate the rebrand", "new
  wordmark for X", "rename this app everywhere", "update the palette across the app's
  pages", or `/rebrandy`. Trigger it even when the user only names one more surface ("…in
  appy too") — that is a rebrand-propagation request. It knows the full map of places a
  flove app's identity lives (its own file, its logo study, the category launcher, the
  demos index symbol, the appy surfaces, favicons), replaces the mark at each while
  matching that surface's own treatment (gradient / monochrome / grayscale-until-hover),
  applies motion per the standard (mark animates where it lives, hover interacts,
  reduced-motion honoured), and verifies every surface by rendering before committing.
  flove-first by default; override via the personal config (see CONFIG.md). Anything that
  would diverge from the shared standard is surfaced,
  not changed silently.
---

# Rebrand — propagate an app's identity across every surface

## Personal config
This skill ships with flove-first defaults. To fork/reuse it for another
project, create a personal config that overrides the defaults instead of
editing the skill (see `development/standards/skills/CONFIG.md`): a shared
`~/.config/flove/skills-config.yml`, a per-skill `settings.yml`, a hidden
`.settings`, or a `config.yml` in the skill folder. Only the keys you set
change; everything else falls back to these defaults.

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
- **Favicon** — the `<link rel="icon">` data-URI SVG (can't animate; update the shape/colour).
- **Wordmark / name** — the app's text label changes, or gets a treatment (a shimmer, a split accent).
- **Palette** — the app's accent colour(s) change and must ripple through its own file and swatches.

Most requests are the mark. The rest follow the same fan-out discipline.

## The surface map — where a flove app's identity lives

Sweep these for the app being rebranded. Not every app touches every row; grep first
(`grep -rl "mark-<app>\|<app>.html\|<App>" apps images` , minus `.git`/worktrees) to find
the real set, then work the list.

| Surface | Where | What to change |
|---|---|---|
| **The app itself** | `apps/<cat>/<app>.html` | header mark(s) (often 2: topbar + About), favicon, wordmark |
| **Logo study** | `images/apps/logos/<app>/<app>-logos.html` | the source of truth for the mark + its size ramp + motion |
| **Category launcher** | `apps/<cat>/index.html` | the app's node/tile glyph |
| **Apps index** | `apps/apps-full.html` | the `#mark-<app>` **symbol** (drives app-bar, grid tile, cube icon, logo slide) |
| **Appy surfaces** | `apps/appy/appy-basic.html`, `appy-mini-full.html`, `profily.html` | each holds its own `#mark-<app>` symbol |
| **Bubbles** | `apps/bubbles.html` | the app's `#cloud` symbol + wordmark/favicon if rebranded |
| **Captions / preview** | `images/apps/captions/<app>.png`, preview modal in `apps/index.html` | screenshot (regenerate only if asked) |

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

## Motion — as the standard says (`docs/standards.html` §Principles, §Frontend)

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
