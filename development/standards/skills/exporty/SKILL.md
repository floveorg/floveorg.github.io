---
name: exporty
description: >-
  Audit an app's export: one `flove-portrait/1` JSON download, the HTML card saved
  from the same rows, and the shared Appy renderer that turns any such JSON into
  the flove card. Covers parity and share. Use for /exporty, "is the JSON
  complete?", "does the export render?".
category: sys
checker_of:
  - https://flove.org/development/standards/frontend/export.md

---

# exporty

Audit an app's export: `flove-portrait/1` JSON, the HTML card built from the same
rows, and Appy's shared renderer.

## Profile

- **JS app** — the JSON export and the renderer are in scope.
- **CSS-pure app** — export is inherently N/A; its send surface is print/copy.
  Say so and stop; never flag it.
- **Save HTML is adopted, not universal** — souls, keys, fivy and worthing ship
  the card today (worthing's is its axial view). An app without it is **advisory**,
  not a FAIL: report it as a candidate, never as a defect.

## Workflow

0. **Resolve the target from `tools/routing.json`.** Match the app by `id` or
   `name`, take its `url` (the file to audit) and its `fields` (the expected
   vocabulary). Never guess a path.
1. **Read the export path — and the app.** Find `flovePortrait.get()` /
   `portraitModel()` and the download handler. While tracing the model, audit
   the rest of the file too: dead code, duplicate helpers, selector/event bugs,
   keyboard/a11y gaps and stale legacy paths. Fix Safe ones in the same pass;
   survey anything that changes behavior. Do not stop at the summary area.
2. **Audit the JSON.** `flove-portrait/1`; `app` matches routing; `rows` carry
   filled `title`/`items`; filename `<app>-portrait.json`; correct MIME; empty
   state disabled; the Save HTML card comes from the same rows and carries no
   data the JSON does not.
3. **Render it.** Load the downloaded JSON into Appy's ◫ Render — switch
   **HTML / XML**, and confirm every row, title and item survives, hostile text
   is inert, and the source footer is right. Save the view only when the user
   asks.
4. **Share.** Web Share attaches the JSON, guarded by `canShare({files})`, with a
   text fallback; no HTML file.
5. **Fix Safe issues** — filename, MIME, dead formats, escaping. Survey anything
   that changes the envelope or removes a feature.
6. **Round-trip.** Upload to Appy, export the profile, reload, consult/merge:
   envelope intact, fill-empty only.
7. **Report** — JSON state, renderer state, share, what was removed, exceptions.

## Orchestration mode

Running as the **export stage of `/optimizy`**
(`https://flove.org/development/standards/skills/optimizy/SKILL.md`):
this is a **functional check**, not the full audit — JSON exists, the renderer
shows it, share works; Safe fixes only.

- translaty hasn't run: any UI or text you add stays in base English and
  translaty-ready.
- `/validaty` ran just before you: keep additions valid and §13-conformant.
- Remaining a per-app extra format is a survey item — hand it up, never decide
  alone.
- Return Safe-applied + risky findings as text; no own survey, report or commit.

## Handoff to jsony

`/jsony` owns the backbone (routing, Appy's `APP_ROUTING`, envelopes); `/exporty`
owns the app's surface. Cross both ways:

- repair changed `flove-fields`, the `flove-profile` / `flove-portrait/1` envelope
  or `floveStore` keys → run `/jsony` (`jsony_check.py --strict`);
- routing or `APP_ROUTING` changed first → re-run `/exporty` on that app.

**Runtime smoke.** `development/tools/conformance.html` calls each app's
`flovePortrait.conformance()` (validate · row integrity · blob name/MIME ·
probe-row merge) in an iframe. Use it before this audit to catch a broken API
cheaply; it does not render the card and does not replace the round-trip below.

## The contract

Share offers **Save JSON** from one model: `<app>-portrait.json`
(`application/json;charset=utf-8`). Where the app ships **Save HTML**, the card is
built from the same rows — `<app>-portrait.html`; a chart app's card is its chart
(worthing: the axial view). Adoption is per app (see Profile).

```js
{ schema:'flove-portrait/1', app, version, generatedAt, lang,
  rows:[{ stage?, key, kind, title, items:[] }],
  words?, completeness?, stats?,
  consent?:{ share, purposes }, source?:{ url } }
```

- One model function feeds `rows`, the phrase and the renderer; no format reads
  the DOM.
- API: `get/validate/consult/merge/toSummary/toAgent/selfTest`, plus
  `flovePort`, `floveImport`, `floveFields()`, `floveStore`. Fallbacks return
  valid empty envelopes; `import()` returns `{ok:false, errors}`.
- Parity: every filled item once, nothing stale, empty model disables export.
- Share the JSON with `canShare({files})`; text fallback; never an HTML file.

**Renderer.** Appy → **Export → ◫ Render** takes any portrait (or `sections[]`)
JSON, toggles **HTML/XML**, and **Save** writes `<app>-portrait.html|xml`. Design:
gradient `#f5b463 → #ed8aa6`, dark mat, two columns of `kind`/`title`/`items`,
optional phrase/raters/completeness/source. Escape everything; sanitize source
URLs to `http(s)`. It is a view, not a format.

**Two buttons.** A summary row has Magic then Share; Save is Share's first item
and emits the JSON portrait. On mobile, Share opens the native share sheet with
the JSON attached. Flag any app that still shows a separate Save button.

**Non-app pages.** Launchers, skill pages, project sites and dev prototypes carry
no portrait and are skipped — the documented list is [`frontend/export.md`](https://flove.org/development/standards/frontend/export.md) § Pages
outside the export contract.

**Exceptions.** Fivy is the only app still shipping its own card/ZIP exporter;
its JSON shape stays identical. Blogy, Souls and Keys are **standard targets**:
a single `flove-portrait/1` JSON download — Souls and Keys also ship a Save HTML
card from the same rows, Blogy is JSON-only — no exception and no "advanced"
category. Worthing saves its
axial view as the HTML card — a display choice, not an exception. The live view
is the shared renderer at `development/addons/rendery/index.html`. The exception
set is single (`EXPORT_EXCEPTIONS` in `jsony_check.py`); its variants — these
apps, the summary notes, the pages outside the contract — live in
[`frontend/export.md`](https://flove.org/development/standards/frontend/export.md) and [`frontend/summary.md`](https://flove.org/development/standards/frontend/summary.md), with each page's type in
`development/index.html` → **Web → Apps** (`#web-apps`).

**Round-trip.** App → file → Appy upload (stored whole, `appId`/`category` from
`tools/routing.json`) → `flove-profile` export (`flove-routing/3`) → reload →
`consult()` fresh slices / `merge()` fill-empty only.

**Repair patterns.** One model; fields from `floveFields()`; `floveStore`;
debounced saves; one picker sync; fresh consult; fill-empty merge; no DOM reads
in exports; no raw events/attachments/secrets; valid empty fallbacks.

**PASS.** JSON download, renderer shows every row, envelope intact; if a Save HTML
card exists, it comes from the same rows.
**FAIL.** A per-app MD/CSV/XML/JPG serializer, an HTML card that diverges from
the rows, ad-hoc model, per-format DOM reads, category guessed from the name,
envelope stripped on upload, unescaped input, `localStorage.clear()`.

Standing rules: `https://flove.org/development/standards/skills/standing.md`.
