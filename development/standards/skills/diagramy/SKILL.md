---
name: diagramy
description: >-
  Build a compact Excalidraw mini-diagram that expands on click into a
  ×3-detailed threaded Mermaid diagram, as one self-contained page. Use for
  /diagramy, "mini diagram", "excalidraw + mermaid", "zoomable diagram".
---

# diagramy — one story, two zoom levels

A small hand-drawn **Excalidraw** mini-diagram is the invitation. Clicking it
opens a **Mermaid thread** with exactly ×3 the detail: the same story, every
actor and step spelled out. The mini sells the shape; the thread proves the
order. Not a logo study (`brandy`) and not a code sketch — diagrams only.

## Brief

- **slug** + one sentence: what changes between the first actor and the last.
- **actors** in order, with the one thing each does.
- **novelty** — the single move the mini must show.
- **accent + signal** colours, taken from the app/page; two maximum.
- **host** — standalone page (default) or a section of an existing page.
- **order** — a sequence (`sequenceDiagram`) or a structure (`flowchart`);
  prefer a sequence when the story has a before/after.

Budget: mini **5–7 nodes**; thread **15–21 messages/notes** (≈3×).

## Files

Diagrams live with the app page they explain, inside that app's addons logos
folder — never in `development/diagrams/`:

- `addons/media/apps/logos/<app>/minidiagrams/` — masters and rendered artifacts
- `addons/media/apps/logos/<app>/<app>-minidiagrams.html` — the gallery page,
  one card per move. A **brandy stage-5 gallery** (`/brandy` → `/diagramy`)
  uses this same pattern.

| File | Role |
|---|---|
| `minidiagrams/<slug>.mini.excalidraw` | editable master (Excalidraw JSON) |
| `minidiagrams/<slug>.mini.svg` | exported/inline mini used by the page |
| `minidiagrams/<slug>.thread.mmd` | canonical Mermaid source |
| `minidiagrams/<slug>.thread.svg` | pre-rendered thread for the click panel (dark ground) |
| `minidiagrams/<slug>.thread-light.svg` | light-ground render, when the host has a day theme |
| `<app>-minidiagrams.html` | self-contained page, both states |

The `.excalidraw` and `.mmd` are the masters; the SVGs are artifacts. Keep the
page in sync with both. `development/diagrams/` is not a diagram home — do not
write new diagram sets there.

## Mini — one frame, no branches

- Author the scene in Excalidraw at `roughness: 1`, strokes **2–2.8** on a
  ~`320×180` viewBox, two colours max (accent + signal). Export the SVG with no
  external fonts or refs.
- One happy path. No failure branch, no notes, no legend. Labels of three words
  at most; the caption outside the drawing carries the rest.
- Working size 160×90; it must still read at 80×45.
- Make the whole frame a `<button>`: the drawing is the hit area, not a link
  hidden beside it.

## Thread — exactly ×3

- `sequenceDiagram` when the story is ordered; `flowchart LR` when it is not.
- Every mini node becomes a participant or step. Add the return path, one
  `Note over` per phase, and the single failure that changes the outcome. That
  is the ×3.
- 15–21 messages/notes for a 5–7-node mini. More is a different diagram; fewer
  is still a mini.
- Same names, order and colours as the mini. The mini is a zoom-out of the
  thread, not a second story.
- Render the `.mmd` to SVG and **inline it**. No runtime CDN: the page must work
  offline. Link the `.mmd` as "source". Render with
  `npx --yes @mermaid-js/mermaid-cli -i <slug>.thread.mmd -o <slug>.thread.svg -t dark -b transparent`
  (`-t neutral` for the light copy). If rendering is not
  possible, show the `.mmd` in a `<pre>` labelled "source — render before
  publishing"; never fake a Mermaid drawing.
- Render for each ground the host has (`-t dark` and `-t neutral`) and show the
  matching SVG; one fixed-theme render on the wrong background is a bug.

## Click contract

- Closed: mini, one-line caption, "unfold the thread" cue.
- Open: dialog or inline panel with the thread SVG; close button, Escape,
  backdrop click; focus moves in and returns to the trigger.
- Trigger: `<button aria-expanded aria-controls>`; panel: `hidden`; no layout
  shift on open. Panel may be wider than the mini; on mobile it scrolls inside,
  never the page.
- Both themes and `prefers-reduced-motion` must keep both states usable.

## Verify

Headless Chrome at 2×; strip the Google Fonts link first (offline headless hangs).
Render closed, open, the 80×45 mini and both themes; re-open the PNG and check the
thread labels do not overlap. The owner opens the page, not the agent.

```bash
google-chrome --headless=new --no-sandbox --disable-gpu \
  --password-store=basic --use-mock-keychain --no-first-run \
  --disable-features=Crashpad --user-data-dir=/tmp/cprof \
  --hide-scrollbars --force-device-scale-factor=2 --window-size=1280,2000 \
  --screenshot=/tmp/render-out.png "file:///abs/path/<page>.html"
```

No commit unless asked.

## Build notes

The mini is `.mini.excalidraw`: 5–7 elements (frame, 2–4 nodes, 1–2 arrows), one
accent, `roughness: 1`; export SVG with scene/background off and no second frame.
The thread is `.thread.mmd` (`sequenceDiagram`/`flowchart LR`), 15–21 messages/notes
for a 5–7-node mini, same names/order/colours; render → inline SVG with
`npx --yes @mermaid-js/mermaid-cli -i <slug>.thread.mmd -o <slug>.thread.svg -t dark
-b transparent` (and `-t neutral`). The page: closed mini + one-line caption; open
dialog/inline panel with the SVG, `<button aria-expanded aria-controls>`, `hidden`,
focus in/out, Escape/backdrop, no layout shift; both themes.

Standing rules: https://flove.org/development/standards/skills/standing.md.
