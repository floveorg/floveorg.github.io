---
name: brandy
description: >-
  Generate a flove app's logo-study page — the single-file `appname-logos.html` that shows the
  app's mark across its FULL SIZE GAMUT (16·24·44·80 px + a live cell) and FORMATS (SVG master,
  PNG, favicon), with THREE animation variants of the logo and the mark + site-title lockup —
  and place it in the app's folder under images/apps (`images/apps/logos/<app>/<app>-logos.html`).
  Use whenever the brand page needs building: "brandy", "/brandy sensy", "make the logos page",
  "build the logo study", "generate <app>-logos.html", "the size gamut page", "three animations
  of the logo", "logo and site title", "sizes and formats", "the svg png favicon". Trigger it when
  a new app — or a freshly-redrawn mark — needs its logo study from scratch. Companion to /rebrandy: brandy CREATES the study, rebrandy PROPAGATES a change across
  every surface. Built flove-first (single-file HTML/CSS/JS, the §13 standards, the family's
  dark-studio look, prefers-reduced-motion honoured); anything that would diverge from the shared
  standard is surfaced, not generated silently.
---

# Brandy — generate a flove app's logo study (`<app>-logos.html`)

## What brandy makes

One self-contained HTML page that is the **source of truth** for an app's brand mark:
the mark next to its **site title** (the lockup), the same mark across its **full size
gamut** and in every **format** the identity ships as (SVG master, PNG, favicon), and
**three animation variants** of it. It is the surface that `/rebrandy`
pushes to when an identity changes — so build it to the family standard the first time
and nothing downstream drifts.

**File:** `images/apps/logos/<app>/<app>-logos.html`
(that is the app's folder under `images/apps`; the family keeps logo studies at
`images/apps/logos/<app>/`). The image lives once, at the repo root, and ships into the
solo download from there — there is no `solo/images` copy.

Live templates to mirror (read before generating): `images/apps/logos/nety/nety-logos.html`
(dark studio, lockup + gama), `images/apps/logos/sensy/sensy-logos.html` (multi-animation),
`images/apps/logos/flove/flove-logos.html` (labelled gamut cells).

## Inputs to gather first

- **App name** and its **wordmark** (which glyph the title accent sits on, e.g. `net<em>y</em>`).
- **The mark** — prefer pulling the existing `<symbol>` / paths from the app's own page or the
  demos index (`#mark-<app>` in `apps/index.html`). Do NOT redraw a mark that already exists.
- **Accent + signal colours** — the app's own two-colour pair (family style, e.g. nety `#8d89ff` +
  `#00f7a7`). Take them from the app's page, don't invent.
- **Three animations** — name them for what the mark does (e.g. a network: orbit/pulse/glow; a
  sprout: sway/breathe/drift). Pick behaviours that fit the mark's geometry.
- **Formats to show** — the master SVG is the single source; PNG and favicon are derived from it
  (no extra drawing needed). Confirm the app's caption PNG path (`images/apps/captions/<app>.png`)
  only if you mention it.

## Page anatomy (the spec)

Single file, `<!doctype html>`, `lang`, `charset`, `viewport`, meta `author` Marc (marcflove),
a one-line `description`, `<title>🌱 <App> · <short tagline></title>` (sprout prefix per the flove
identity), a data-URI SVG favicon of the mark, and the wordmark font (family: Fredoka for the
lockup unless the app has its own face).

Dark studio background; the app's accent + signal on the mark. Sections, top to bottom:

1. **Hero lockup** — the living mark beside the wordmark:
   `<svg class="hero-mk live">` + `<span class="wm">app<em>x</em></span>` (accent on the em).
2. **Size gamut** (label it `gama`) — the same mark at **16, 24, 44, 80 px** and one **live** cell
   at 80 px. Static cells reuse a `<symbol id="mark-<app>">` via `<use href="#mark-<app>">`;
   the live cell inlines the mark so animation classes can reach its parts. Label each size.
3. **Three animation variants** — three labelled cells, each running ONE distinct infinite
   animation. Wrap the rules in `@media (prefers-reduced-motion:no-preference){ … }`; the static
   mark remains under `reduce`.
4. **Formats** — the identity's full artifact set: **SVG (main)**, **PNG**, **favicon** and the
   family extras (caption, apple-touch-icon). See the "Formats" section below.
5. **Reduced motion fallback** — `@media (prefers-reduced-motion:reduce){ *{ animation:none !important; } }`.

### Formats — the identity's artifact set

Every flove app identity ships as more than the inline SVG. The study must carry and show them:

- **SVG (main)** — the canonical master. Define it once as `<symbol id="mark-<app>">` (the
  study's own head has it inline); provide a copyable/downloadable standalone `<app>.svg` — the
  mark at its own viewBox (usually 64×64), self-contained (fills/strokes inline, no `<use>`, no
  external refs), plus a "download .svg" button that serialises it.
- **PNG** — the raster exports at standard sizes: **16, 32, 48, 64, 128, 256, 512 px**. In-page
  script: draw the mark onto `<canvas>` (at 2× device ratio for crispness), transparent
  background, and offer a download per size (`download="<app>-<size>.png"`). Show the PNG cells
  next to the SVG gamut so the two visibly match.
- **Favicon** — the `<link rel="icon" href="data:image/svg+xml,…">` line from the head, shown
  copyable; the mark at 16/32 reads there. Note the legacy `.ico` (32×32) and the
  `apple-touch-icon` (180×180, opaque background) as the raster siblings where a favicon can't be SVG.
- **Family extras** — the caption PNG at `images/apps/captions/<app>.png` (the preview/demo
  thumbnail) and the fact that the app's own page uses this same mark as its favicon. Don't
  regenerate the caption here — that's the `/rebrandy` surface — but reference it as part of the
  identity artifact set (per the App identity artifacts standard).

### Animation rules that don't break

- A mark may comma-list two animations, but **two animations must not both drive `transform`**
  on the same element — pair a transform motion (rotate/scale/translate) with a filter or opacity
  one (glow, twinkle). Otherwise fold both motions into a single keyframe.
- Use `transform-box:fill-box; transform-origin:center` (or `view-box` at the mark's own origin)
  so parts rotate/scale around themselves, not the page.
- Three distinct variants read better than three variations of the same thing — vary the *kind*
  of motion (breathe ≠ drift ≠ glow), not just the speed.

## Mark hygiene

- Define the mark once as `<symbol id="mark-<app>">`; every static `<use>` pulls from it so a
  redraw updates the whole gamut.
- Strokes at **2–2.8 px** on a 64 viewBox so the mark still reads at **16 px**. Verify it.
- Keep the two-colour rule (accent + signal); don't add a third hue without the user asking.

## Verify by rendering — never ship a blind logo page

A logo study is visual; a wrong path or broken data-URI is invisible until rendered. Rasterise
and look:

```bash
google-chrome --headless=new --no-sandbox --disable-gpu \
  --password-store=basic --use-mock-keychain --no-first-run \
  --disable-features=Crashpad --user-data-dir=/tmp/cprof \
  --hide-scrollbars --force-device-scale-factor=2 --window-size=1280,2000 \
  --screenshot=/tmp/brandy-out.png "file:///abs/path/<app>-logos.html"
```

- Pages pulling Google Fonts hang headless without network — render a copy with the font
  `<link>` stripped.
- Check the gamut: the 16 px cell reads, each size's mark looks identical, and the live/animation
  cells visibly differ. Re-open the PNG and read it.

## Close out

Stage **only** the generated file(s) — never `git add -A` (the tree may have parallel edits) —
commit with the prompt + a short explanation (e.g. `add: <app> logo study — gama + 3 mark
animations`), and push `origin main` to `localhost:3000/marc/flove` per the flove Gitea workflow.
One commit per page.

## When to stop and ask

- The mark doesn't exist anywhere yet and must be **drawn** — confirm the shape/meaning before
  inventing geometry.
- The app has no established accent/signal pair — confirm colours rather than guessing.
- The user names the folder explicitly (`images/apps/<app>/` without `logos/`) — follow their
  word; the `logos/` level is the convention, not the law.
