# whole — the flove wiki

`whole/` is the wiki of **fields**, their **paradigms**, and the **apps** that make each field playable.

- `index.html` — the wiki home, showing only the five top-level field cards. Apps live inside their field pages, not on a separate page.
- `metaphysics/`, `science/`, `biology/`, `linguistics/`, `economy/`, `psychosocial/` — the field pages. Metaphysics, Science, Biology, Language and Psychosocial share the same rhythm: each subject has its description, a **field title with the substance as a chip on its left**, its **paradigms as columns (2 per row) with a video slot and the paradigm intro below**, and its **app cards**. The content mirrors the paradigms/apps table in `docs/index.html`. They remain hand-authored HTML: edit them directly, keep any design you like.
- A fixed **common header** on every page: the **Whole** tab (highlighted on the hub) + the five field tabs, each page highlighting its own tab; the animated sprout logo + **whole** title open the shared menu — **About**, **Download**, **Updates**, **Last updated**, and a **Flove** subsection with **Docs · Development · News · Home**. **Language** and **Psychosocial** are normal page links; on their pages (and on Music/Economy) their child menu — Music / Economy — is loaded and visible. No settings icon. Edit it once in `whole/build-header.mjs` and run `node whole/build-header.mjs` to re-inject it into every page.
- `whole.css` / `whole.js` — a shared, `whole-`prefixed skin with **light/dark palettes (§13.14, `flove:theme`, ◐ toggle next to the page title)**, the deep-link opener and the **animated app preview modal** (any `.whole-appcard` opens it; it shows the caption, tagline, a longer description and value chips when `apps-full.html` has them, and its own **Play in →** button goes to the app). Field pages opt in with `<link rel="stylesheet" href="../whole.css">`; their own CSS stays in charge of everything else.
- `linguistics/music/` — the Music index, nested under Language and linked as its subitem in the header.

## Authoring rules

1. **Section header:** the **field is the `h2` title**; when the taxonomy has a substance, it sits on the left as `.whole-substance` inside that `h2` (e.g. `Cytoplasm` + `(Evo) Microbiology`). Keep the field anchor on the `h2` and the substance anchor on the chip, so `docs/index.html` links to both keep working.
2. **A new app:** add an app card to the right subsection of its field page: `<a class="whole-appcard" id="app-<id>" href="…" data-context="<subsection>">` with the caption at `../../central/shared/media/images/apps/captions/<id>.png` when it exists. Cards open the shared preview modal and keep their deep link. Optional `data-tag`, `data-cat`, `data-long` and `data-vals` (piped) enrich that modal; the field pages already carry them for every app listed in `apps-full.html`.
3. **A new field:** copy one of the field folders, rename it, change the accent (`--whole-field-accent` on the hub card) and add a card to `whole/index.html` and an entry in `whole/build-header.mjs`. Add the slug to `tools/build-aliases.mjs` so `/yourfield` redirects to `/whole/yourfield/`.
4. **Deep links:** apps-full's “See docs” and the logo slides point to `/whole/<field>/#app-<id>`. Keep those anchors stable.
5. **App cards:** each app card in a field subsection carries `id="app-<id>"`; apps-full deep links (`whole/<field>/#app-<id>`) scroll straight to it. The old bottom collapsed app lists were removed from the five structured field pages.
6. **Interaction:** a normal click on a card opens the preview modal; Ctrl/Cmd/middle-click still opens the app directly. A deep link to `#app-<id>` scrolls to the card and pulses it.
7. **Cross-feeds / gamification:** every app card carries `data-context` (its subsection) and keeps the app link in `href`; add XP/streak attributes or related-app rails without changing the markup model.
8. **Design:** the shared CSS only styles `whole-*` classes, so a field page is free to look like `metaphysics/index.html` or something entirely different.
9. **Paradigm videos:** each paradigm column reserves a 16:9 video slot. Metaphysics already has its intro clips; the other fields show the styled **Video** placeholder until their clips exist — drop the media in and link it there.

## Source & download

The header menu links to the **whole/ folder in the GitHub repository** (`github.com/floveorg/floveorg.github.io/tree/main/whole`) instead of a generated zip — there is nothing to rebuild when the wiki changes. **Updates** opens the folder commit history, and **Last updated** is read from the latest GitHub commit touching `whole/` (cached per session; falls back to “recently”). The full offline site package still carries `whole/` (see `tools/build-flove-zip.sh`).

## Notes

- **Psychosocial** is a top-level field and holds **Economy** as its child page; **Organism** was folded into Psychosocial (its content/apps now live there).
- **Old field URLs** (`/Metaphysics`, `/metaphysics`, …) are resolved by `404.html` to the new `/whole/<slug>/` pages (see `tools/build-aliases.mjs`). `/frotis`, `/chacrikun` and `/electrorchestra` (and the old `/linguistics/music/<slug>/` paths) resolve the same way to `/whole/linguistics/music/<slug>/` — there are **no root stubs or duplicate app copies**.
- **Source:** the GitHub repository is the download/source path; the full offline site package (`tools/build-flove-zip.sh`) carries both `whole/` and the apps.
