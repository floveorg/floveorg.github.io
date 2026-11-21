---
name: brandy
description: >-
  One logo pipeline for an app: sketch 5–10 candidates, build the full study,
  place the mark in the product, present it, then add section icons,
  mini-diagrams and the tour. Use for "brandy", logo ideas, rebranding, or
  `/brandyN` to run stages 1–N.
category: authoring
---

# brandy — from sketch to shipped identity

One skill, five stages. **Ask first: new mark or existing one?** A new mark runs
1 → 5. An existing mark skips stage 1 and runs 2 → 5 in reverse — that is a
rebrand, not a different skill. Invoked as **`/brandyN`** (e.g. `brandy4`), run
stages 1 → N and stop; otherwise ask, **multiselect, which stages to run**
(default 1–3), and stop after the last one chosen. Either way, state what remains:
at the end of each stage, name the next one and ask to continue; never jump to the
study before the pick.

| Stage | Output |
|---|---|
| **1 · Sketch** | 5–10 numbered candidates in `<app>-logos.html` |
| **2 · Study** | the same file becomes the full study |
| **3 · Placement** | card, tree, Types row, launcher tile, app tab |
| **4 · Presentation** | long copy, values, slides, downloads (planned) |
| **5 · Sections & tour** | SVG icon set, click-to-open minidiagrams, the 10-slide tour |

**One file per app:** `development/addons/media/apps/logos/<app>/<app>-logos.html`. Stage 1
fills its sketch section; stage 2 replaces that section in place. Never create a
second logo or sketch file.

## 1 · Sketch

Gather the brief: name and wordmark (which glyph carries the accent), slogan in
EN + ES, what the app is, its accent/signal pair (taken from its page, never
invented), and any fixed geometry or 16 px constraint. A mark that already exists
is not redrawn: go to stage 2 and extend its study.

The sketch section:

- header with app name, the brief in one line, a small theme toggle;
- **5–10 numbered candidates**, each at **80 px and 16 px**, with a name and a
  one-line idea (`01 · rubbed string, two tensions`);
- monoline geometry in a 64×64 viewBox, strokes 2–2.8, two colours maximum;
- one `<symbol id="sk-01">` per candidate, `<use>` for the repeats;
- no gamut, formats or animation set; a hover lift is fine.

Rasterise at 2× (see **Render check**), check both themes, then **STOP** for the
pick.

## 2 · Study

The chosen mark becomes the study; alternates stay in a compact row. Use the reference page
`https://flove.org/development/addons/media/apps/logos/central/central-logos.html` — copy its
anatomy:

- **hero lockup** — living mark + wordmark + bilingual slogan;
- **novelty mini-diagram** — one inline SVG (~120×52) of the app's essential
  novelty, monoline, label-free, both themes; no diagram, no slogan;
- **size gamut** — 16/24/44/80 px plus one live cell;
- **motion gamut** — the same sizes running the primary animation;
- optional **weight scale** — ten steps of the signature stroke;
- **animation set** — 5–7 distinct behaviours at 44 and 80 px, not one speed
  repeated; all inside `prefers-reduced-motion:no-preference`;
- **formats** — SVG master (`<symbol id="mark-<app>">` plus a standalone
  download), PNG 16–512 via `<canvas>` at 2×, favicon data-URI;
- **theme toggle** — dark studio and light day surface, mark fills identical;
- **metadata** — slogan, one-line about for `routing.json`, the tour outline.

Motion rules: two animations never both drive `transform` on one element; use
`transform-box:fill-box; transform-origin:center`; keep strokes at 2–2.8 on a 64
viewBox; the chosen sketch geometry is the study geometry — no silent redraw.

Verify both themes at 2×. Commit the study alone; placement is a separate commit.

## 3 · Placement

**Ask the type; never infer it from the path.** It sets the Types row, the tree
treatment, whether it counts in `N apps`, and whether it needs a launcher tile.
Offer that choice as a **clicky interface**: one picker whose options are the
types below as buttons/chips, using the host's question or quick-reply tool when
one exists. Fall back to a numbered terminal batch only when no clicky surface
is available.

| Type | `data-type` | Tree row | Counted | Launcher tile |
|---|---|---|---|---|
| standard | `standard` | `tnode file` | yes | yes |
| launcher | `launcher` | `tnode file launcher` | no | it *is* one |
| demo / page | `demo` / `page` | `tnode file` | yes | optional |
| project / skill | `project` / `skill` | `tnode file` | yes | no |
| other | owner's string | ask | ask | ask |

**Card** — minimal in `apps/apps-full.html`: mark, name, slogan in `cube-tag`,
category pill, one line, `▶ Open`. Long copy is stage 4.

**Tree** — one `<li>` in `development/index.html` under its category:
`<li><a class="tnode file" href="../../<path>"><svg class="ic appic"><use href="#i-file"/></svg><code class="tname">App</code><em class="tpath"><folder>/</em></a></li>`
Launchers get `tnode file launcher`. Recount `N apps` from the `tnode file` rows
(launchers excluded) — a lazy count is the commonest defect.

**Types** — a row in [Web → Types](https://flove.org/development/index.html#web-types)
with the matching `data-type`; bump `Launcher · N` and `All · N`.

**Launcher** — a tile in the category launcher (`apps/language`, `psychosocial`,
`economy`, `metas`/`bio`). Inline the mark in the symbol's own viewBox; gradients
don't travel (use a solid accent); never anchor the insert on the first
`</defs>` — it belongs to the favicon data-URI.

**App tab** — replace `<link rel="icon">` with the mark's data-URI. Appy pages
(`apps/appy/`) and `apps/bubbles.html` keep their own `#mark-<app>`; swap that
body too, same `id`.

The caption PNG (`development/addons/media/apps/captions/<app>.png`) is regenerated on
request, not here.

Render the four surfaces: card, tree row, Types row, launcher tile.

## 4 · Presentation

Long description, values cloud, slides and downloads — planned, not built. Until
then the card stays deliberately minimal; never fill it with placeholder prose.

## 5 · Sections and tour

Everything lives on the app's **logo study page** (`<app>-logos.html`); no second
gallery file and no separate diagram folder.

1. **SVG set (default view)** — one monoline icon per section of the app's
   index, drawn like the mark: same 64×64 grid, 2–2.8 stroke, accent + signal
   taken from the page. Show the whole set as the default, labelled, with no
   build step and no external source file.
2. **Minidiagram on second click** — clicking a section icon opens one simple
   inline SVG minidiagram for that section, in the same page: one frame, one
   happy path, a few nodes and arcs in the mark's two colours. Each section gets
   its own composition, not the same boxes-and-arrows template. Clicking the
   icon again (or ×) closes it; only one panel is open at a time; Escape closes.
   **No Excalidraw, no Mermaid, no ×3 threading, no `diagramy` dependency.**
3. **The tour** — the 10-slide outline: logo, what it is, how it starts, core
   interaction, what you keep, privacy, share, tiers, limits, docs. Keep it in
   the study's metadata and link to it; never duplicate it.

## Rebrand

Existing mark: skip stage 1, then run stages 2–5 in reverse. Grep first, swap the
`#mark-<app>` symbol body everywhere (keep the `id`), and let each `<use>` follow.
Slogan, accent and favicon count too.

Config: `https://flove.org/development/standards/skills/CONFIG.md`.

## Render check
Headless Chrome at 2×; strip Google Fonts first (offline headless hangs). Both
themes and 80/16 px; re-open the PNG. Command:
[`diagramy` · Verify](https://flove.org/development/standards/skills/diagramy/SKILL.md#verify).

Standing rules: `https://flove.org/development/standards/skills/standing.md`.
