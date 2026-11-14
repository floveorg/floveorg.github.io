# Registering an app in the flove catalogs

Shared checklist for **brandy** (new app/identity) and **rebrandy** (changed
identity). Use it only when the target **is an app** — ask first if that is not
obvious. It covers the full card, the cube caption, the category/background
classes, the development tree and the slogan propagation.

## 1. Confirm before writing

Ask/collect:

- **App id / name** and its **page**:
  - `apps/<cat>/<app>.html`, or
  - `whole/<field>/<app>/index.html` for a whole-hosted app.
- **Category(s)** — Inside, Mating, Linguistics, Social, Economy (one or more).
- **Emotional level** (`cat-emo1`…`cat-emo5`) — match the app's siblings.
- **Slogan/tagline** in **EN + ES** (the one-line promise, e.g.
  `archetype & matrix` / `arquetipo y matriz`).
- **Caption PNG** — `central/shared/media/images/apps/captions/<app>.png`.
- **Play URL** (app page), optional **docs** URL and **download** zip.
- Whether it belongs in the **bubbles** icon layout too.

## 2. `apps/apps-full.html` — full card + cube

### a. Mark symbol

Ensure the page head defines `<symbol id="mark-<app>">…</symbol>` once and the
card/cube reference it with `<use href="#mark-<app>">`. Do not duplicate paths.

### b. Grid tile (the “full card”)

Add a tile in `<section class="grid">`, in the right category group:

```html
<a class="tile tile-rb-o cat-inside cat-emo5" href="#app-<app>"
   style="--ord-rb:<n>; --ord-rd:<n>;">
  <div class="icon"><svg class="flove-mark" aria-hidden="true"><use href="#mark-<app>"/></svg></div>
  <div class="meta">
    <div class="name"><App></div>
    <div class="tag"><span class="en" lang="en"><slogan EN></span><span class="es" lang="es"><slogan ES></span></div>
  </div>
</a>
```

- **Background/category classes** (the colour comes from these):

  | Category | Tile/cube palette | Category class |
  |---|---|---|
  | Inside | `tile-rb-o` / `cube-rb-o` (orange) | `cat-inside` |
  | Mating | `tile-rb-y` / `cube-rb-y` (yellow) | `cat-mating` |
  | Linguistics | `tile-rb-g` / `cube-rb-g` (green) | `cat-ling` |
  | Social | `tile-rb-b` / `cube-rb-b` (blue) | `cat-social` |
  | Economy | `tile-rb-i` / `cube-rb-i` (indigo) | `cat-economy` |

  Multi-category cards keep all their `cat-*` classes (the page blends the
  accents); use the primary category's palette class. The grid tile uses
  `cat-*`; the cube uses the matching `cube-cat-*` (e.g. `cube-cat-inside`).
- Append `--ord-rb` / `--ord-rd` after the current maximum, or ask which slot.
- If the category chips show a `.cat-count`, increment the matching count.

### c. Cube (the detail panel + captions)

Add the matching `<div class="cube cube-rb-o cube-cat-inside" id="app-<app>">`
with:

- `.cube-head` — mark, `<h2>`, `.cube-tag` (the slogan, bilingual) and
  `.cube-cat-pill` (the category name).
- `.cube-desc` — one short description + optional `.cube-cloud` values.
- `.cube-slides`:
  - logo slide — the mark + caption `<App> · <slogan>`;
  - screenshot slide — `<img src="../central/shared/media/images/apps/captions/<app>.png">`
    + its caption;
  - video slide only when a clip exists.
- `.cube-actions` — See docs, Download (only if a zip exists), Play.

The caption PNG lives once under `central/shared/media/images/apps/captions/`.
Create/regenerate it only when asked (that is a rebrandy surface); otherwise
reference the existing file.

### d. Bubbles (optional)

If the app belongs in the bubbles layout, add it to the matching category group:

```html
<a class="ib-app ia1" href="#app-<app>"><svg class="flove-mark" aria-hidden="true"><use href="#mark-<app>"/></svg><span class="ib-app-n"><App></span></a>
```

## 3. `development/index.html` — app tree

Find the right category `<li class="reveal cat-<cat>">` → `<ul class="subtree sun">`
and add:

```html
<li><a class="tnode file" href="../../apps/<cat>/<app>.html" title="<slogan EN>">
  <svg class="ic appic"><use href="#i-file"/></svg><code class="tname"><App></code><em class="tpath"><cat>/</em></a></li>
```

- Whole-hosted apps: `href="../../whole/<field>/<app>/index.html"` and a
  matching `tpath` (`whole/`).
- Keep the sibling ordering; use `title` for the hover slogan (this surface has
  no text slot).

## 4. Slogan propagation

The app's slogan is part of the identity, not just the card copy.

- **Visible text where there is room:**
  - apps-full tile `.tag` (bilingual).
  - cube `.cube-tag` and the logo-slide caption.
  - the app's own page (hero/lede or meta).
  - the logo-study hero/lockup.
- **Hover on icon-only surfaces** (native `title`, plus `aria-label`/`data-aria-*`
  where the page supports them):
  - appy `.appbtn` buttons: `title="<App> — <slogan>"`.
  - development tree `.tnode` links: `title="<slogan>"`.
  - launchers/category icons with no text.
- Keep EN/ES in sync; never leave an old slogan on one surface.

## 5. Favicon / tab

The chosen mark's data-URI must be the `<link rel="icon">` in:

- the logo study's own head, and
- the app page's head (`apps/<cat>/<app>.html` or
  `whole/<field>/<app>/index.html`).

The **title** stays the app name/slogan unless the name itself changed (that is
rebrandy). Verify the tab shows the mark.

## 6. Verify

- `apps/apps-full.html`: tile and cube render in both themes; the category
  filter includes it; colours match the siblings; caption image loads.
- `development/index.html`: the tree link resolves and the `title` hover shows
  the slogan.
- The app page favicon is the new mark.
- Search for the old mark/name/slogan across `apps`, `whole`, `central` and the
  skill pages; no stale copy.
