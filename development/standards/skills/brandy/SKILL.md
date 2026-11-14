---
name: brandy
description: >-
  Two-stage logo design for a flove app. Stage 1 (sketch) builds ONE lightweight
  sheet of 5–10 simple logo candidates — monoline marks at 16/80 px, no full
  gamut, no formats and no per-logo animations — then stops for the owner's
  pick. Stage 2 (full) builds the real `<app>-logos.html` study for the chosen
  mark: the full size gamut, a motion gamut (the mark animated at 16/24/44/80),
  an extended set of 5–7 distinct animations, the lockup + slogan, theme toggle
  and all formats (SVG/PNG/favicon/apple); optionally applies the favicon to the
  app tab and registers the app in the catalogs. Use for "brandy", "/brandy",
  "explore logos", "logo sketches", "give me 5–10 logos", "make the logos page",
  "build the logo study", "full gamma", "the svg png favicon". Do NOT generate a
  full study for every candidate. Companion to /rebrandy: brandy creates the
  identity study, rebrandy propagates a chosen mark across every surface.
---

# Brandy — two-stage logo design for a flove app

## Personal config

See `development/standards/skills/CONFIG.md` for the override routes and keys.

## The two stages

Brandy deliberately separates **exploring** from **producing**. Never build a
full size gamut, formats and animation set for every idea: that is slow, noisy
and makes the choice harder.

| Stage | Output | What it contains | What it does NOT contain |
|---|---|---|---|
| **1 · Sketch** | `<app>-logo-sketches.html` (temporary) | 5–10 numbered candidate marks, each at 16 + 80 px with a one-line idea | full gama, formats, per-logo animations; **not committed** |
| **2 · Full study** | `<app>-logos.html` | lockup, size gama, **motion gama**, extended animation set, formats | other candidates' full studies |

**Flow:** gather the brief → sketch sheet (5–10) → **STOP for the owner's pick**
→ build the full study for the chosen mark(s) only.

If the owner asks for "logos" without a chosen direction, start at stage 1. If
they already have a chosen mark, skip to stage 2.

## Shared inputs to gather first

- **App name**, its **wordmark** (which glyph the title accent sits on, e.g.
  `net<em>y</em>`) and its **slogan/tagline** in EN + ES (the one-line promise;
  e.g. `archetype & matrix` / `arquetipo y matriz`). The slogan is part of the
  identity and travels with the mark.
- **The idea** — what the app is, its mood, and any fixed metaphor or geometry.
- **The mark** — if one already exists, do NOT redraw it: go straight to the
  full study (or a redraw only if asked).
- **Accent + signal colours** — the app's own two-colour pair (family style,
  e.g. nety `#8d89ff` + `#00f7a7`). Take them from the app's page, don't
  invent. For the sketch stage a monochrome version is enough; apply the pair in
  the full study (or show both in the sketch if colour is part of the idea).
- **Constraints** — must it read at 16 px? avoid text? keep a circle? existing
  family language to respect?
- **Is it an app?** If yes, note its app id, category(s), app page and slogan
  now; catalog registration happens after the pick (see
  `development/standards/skills/app-registration.md`).

## Stage 1 — the sketch sheet

**File:** `central/shared/media/images/apps/logos/<app>/<app>-logo-sketches.html`
(create the app folder if it does not exist yet). It is a **temporary review
artifact**: write it, render it, and do **not** commit it. It is deleted once the
chosen mark's full study is committed (unless the owner explicitly asks to keep
it as an alternates archive).

One self-contained, lightweight HTML page:

- Header: app name, the brief in one line, and a small **theme toggle**
  (dark studio / light day) — see the theme rule below.
- A grid of **5–10 numbered candidates**. Each cell has:
  - the candidate at **80 px** (the main read),
  - the same candidate at **16 px** (the favicon read),
  - a short name + one-line idea (e.g. `01 · rubbed string, two tensions`).
- Simple monoline geometry at the mark's own viewBox (usually 64×64). Strokes
  2–2.8 px so the 16 px cell is honest. Two colours maximum.
- **No full size gamut, no formats, no download buttons, no animation set.**
  A hover lift on a cell is fine; do not animate each candidate.
- Use one `<symbol id="sk-01">`… per candidate and `<use>` for the 16/80
  repeats. This keeps the sheet small and makes a later redraw easy.

Verify by rendering (see below), especially the 16 px read and both themes. Then
**STOP** and ask the owner which number(s) to take forward. Do not build the
full study before the answer. If they want more options, replace or extend the
sheet with another 5–10 — still no full studies.

## Stage 2 — the full study for the chosen mark

**File:** `central/shared/media/images/apps/logos/<app>/<app>-logos.html`.
This is the **source of truth** for the app's mark, and the surface `/rebrandy`
propagates from.

If more than one candidate is chosen for the same app, ask which is the
**primary**; the full study uses that one. Keep the others in the sketch sheet
as alternates — do not create several full studies unless explicitly asked. If
several apps are chosen, build one full study per app.

### Page anatomy (the spec)

Single file, `<!DOCTYPE html>`, `lang`, `charset`, `viewport`, meta `author`
Marc (marcflove), a one-line `description` carrying the slogan,
`<title>🌱 <App> · <short tagline></title>` (sprout prefix per the flove
identity), a data-URI SVG favicon of the mark, and the wordmark font (Fredoka
for the lockup unless the app has its own face).

**Night–day theme switcher.** A logo study must prove the mark reads on both
backgrounds — the dark studio (`#0d0d13`-ish) and a light day surface
(`#f6f5f2`-ish). A small `☀️/🌙` toggle flips the page via a single
`.theme--light` class on the root; the mark's fills stay identical so real
clarity problems show. Keep the dark studio as the default. When verifying,
render both; if a colour disappears on one, flag it — do not silently shift the
brand palette.

Sections, top to bottom:

1. **Hero lockup** — the living mark beside the wordmark:
   `<svg class="hero-mk live">` + `<span class="wm">app<em>x</em></span>`, with
   the bilingual **slogan** underneath as the page's one-line promise.
2. **Size gama** (label it `gama`) — the static mark at **16, 24, 44, 80 px**
   and one **live** cell at 80 px. Static cells reuse the mark `<symbol>` via
   `<use>`; the live cell inlines the mark so animation classes can reach its
   parts. Label each size.
3. **Motion gama** — the same mark at **16, 24, 44 and 80 px**, all running the
   **primary animation**. This is the gamut extended with motion: it proves the
   mark stays legible while it moves, at favicon size too. Four labelled cells.
4. **Animation set** — **5–7 distinct variants**, each labelled and shown at
   **44 and 80 px**. Name the behaviour (e.g. `breathe`, `trace`, `orbit`,
   `glow`, `drift`, `pulse`, `flip`). Vary the *kind* of motion, not just the
   speed. All rules inside
   `@media (prefers-reduced-motion:no-preference){ … }`.
5. **Formats** — the identity's full artifact set (SVG, PNG, favicon, apple,
   caption reference). See below.
6. **Reduced-motion fallback** —
   `@media (prefers-reduced-motion:reduce){ *{ animation:none !important; } }`.
   The static mark and both gamas remain visible.

### Motion rules that don't break

- A mark may comma-list two animations, but **two animations must not both
  drive `transform`** on the same element — pair a transform motion
  (rotate/scale/translate) with a filter or opacity one (glow, twinkle).
- Use `transform-box:fill-box; transform-origin:center` (or `view-box` at the
  mark's own origin) so parts rotate/scale around themselves.
- Five distinct variants read better than five speeds of the same thing. The
  motion must remain readable at 16 px; if a variant turns to mud there, choose
  a simpler one.
- The primary animation is the one used in the hero/live cell and motion gama.
  Pick it as the clearest, most legible behaviour.

### Formats — the identity's artifact set

- **SVG (main)** — the canonical master. Define it once as
  `<symbol id="mark-<app>">`; provide a copyable/downloadable standalone
  `<app>.svg` — self-contained (fills/strokes inline, no `<use>`, no external
  refs) at its own viewBox (usually 64×64), plus a "download .svg" button.
- **PNG** — raster exports at **16, 32, 48, 64, 128, 256, 512 px** via
  `<canvas>` at 2× device ratio, transparent background, one download per size
  (`download="<app>-<size>.png"`). Show the PNG cells next to the SVG gama so
  they visibly match.
- **Favicon** — the `<link rel="icon" href="data:image/svg+xml,…">` line from
  the head, copyable; the mark at 16/32 reads there. Note the legacy `.ico`
  (32×32) and `apple-touch-icon` (180×180, opaque background) as raster
  siblings.
- **Family extras** — the caption PNG at
  `central/shared/media/images/apps/captions/<app>.png` and the fact that the
  app's own page uses this mark as its favicon. Do not regenerate the caption
  here — that is `/rebrandy` — but reference it.

## Applying the chosen mark (optional)

When the owner wants the chosen mark **applied**, not just studied:

- **Logos page tab** — the study's own head already carries the chosen mark as
  its data-URI favicon.
- **App index page tab** — replace the `<link rel="icon" …>` in the app page's
  head with the same data-URI (URL-encoded mark). The app page is
  `apps/<cat>/<app>.html` or `whole/<field>/<app>/index.html`. Keep the
  `<title>` unless the app name changed (that is rebrandy).
- **Is this an app? — ask.** If yes, register/update it in the catalogs via
  `development/standards/skills/app-registration.md`: the full card + cube
  caption in `apps/apps-full.html`, its category and background classes, the
  `development/index.html` app tree entry, and the slogan propagation. If the
  app already exists, this becomes a rebrandy sweep.
- **Slogan** — visible text where the surface has room, `title`/`aria-label` on
  icon-only surfaces (the registration reference lists the exact places).

## Mark hygiene

- Define the mark once as `<symbol id="mark-<app>">`; every static `<use>` pulls
  from it so a redraw updates the whole study.
- Strokes at **2–2.8 px** on a 64 viewBox so the mark still reads at **16 px**.
- Keep the two-colour rule (accent + signal); don't add a third hue without the
  user asking.
- The sketch sheet's chosen candidate must be the same geometry used in the full
  study — no silent redraw between stages. If the mark changes, update the
  sketch sheet too.

## Verify by rendering — never ship a blind logo page

A logo study is visual; a wrong path or broken data-URI is invisible until
rendered. Rasterise and look:

```bash
google-chrome --headless=new --no-sandbox --disable-gpu \
  --password-store=basic --use-mock-keychain --no-first-run \
  --disable-features=Crashpad --user-data-dir=/tmp/cprof \
  --hide-scrollbars --force-device-scale-factor=2 --window-size=1280,2000 \
  --screenshot=/tmp/brandy-out.png "file:///abs/path/<app>-logos.html"
```

- Pages pulling Google Fonts hang headless without network — render a copy with
  the font `<link>` stripped.
- **Render both themes** — add `?theme=light` (or a query flag the page reads)
  to force the day surface; check the mark and its accent/signal read on both
  dark and light grounds.
- Check the **static gama** (16 px reads, each size identical), the **motion
  gama** (the mark stays legible at 16/24/44/80) and the **animation set** (all
  5–7 variants visibly differ, none collide with another transform).
- Check the sketch sheet in both themes too; the 16 px minis are the point.
- Re-open the PNG and read it.

## Close out

Stage 1: keep the sketch sheet **uncommitted**. Show it, get the pick, and move
straight to stage 2. Do not commit it.

Stage 2: commit only the full study, with a prompt such as
`add: <app> logo study — gama + motion gama + 6 animations`. After the full study
is committed, **delete the temporary sketch sheet** (and its folder if empty);
stage only the full study — never `git add -A` — and push `origin main` to
`localhost:3000/marc/flove` per the flove Gitea workflow. One commit per page.
If the owner wants the chosen mark live in the app and on every surface, continue
with `/rebrandy` after the study is committed. Before closing, ask the
application question: app page favicon, catalog registration and slogan
propagation (see “Applying the chosen mark”).

## When to stop and ask

- The mark doesn't exist and must be **drawn** — confirm the shape/meaning
  before inventing geometry. The sketch stage is the place to explore it.
- The app has no established accent/signal pair — confirm colours rather than
  guessing.
- The owner picks more than one candidate for the same app — ask which is
  primary; do not build several full studies silently.
- The user names the folder explicitly (`central/shared/media/images/apps/<app>/`
  without `logos/`) — follow their word; the `logos/` level is the convention,
  not the law.
