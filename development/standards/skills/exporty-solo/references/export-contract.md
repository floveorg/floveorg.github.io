# Export & share contract — the audit checklist

This is the operational, pass/fail version of **§13.12** in
`context/flove/backend_plan.md` (the source of truth — re-read it if anything here is ambiguous or
looks stale). Walk every line against the named app. `metas/souls.html` is the reference that
passes all of it; `blogy/blogyadvanced.html` passes md/json/xml/html.

## Table of contents
- A. The summary-model (single source)
- B. Axis 1 — summary parity
- C. Axis 2 — Views ↔ raters
- D. Axis 3 — the six formats (per-format criteria)
- E. Axis 4 — share readiness
- F. Cross-cutting: filenames, i18n, escaping, hostile input
- G. Tier & distro gating

---

## A. The summary-model (single source)

The app should have **one** object the phrase, the Views, and every export read from. Canonical
shape (the app may extend it, but these keys are canonical):

```js
{ app:'<app>', version:1, phrase:'<live phrase>',
  sections:[{ label, title, items:[…] }],   // recap blocks
  raters:[{ key, emoji, n, max }],           // ratings — also feed the Views
  picked:[…], stats?:{…},
  date?:'<ISO>',                             // present iff "Add date" toggle is on (§13.9)
  profile?:{ handle, … } }                   // present iff "Add profile" toggle is on — from appy(-mini)
```

- **PASS**: a single function/state builds this, and the phrase + every format derive from it.
- **FAIL (Standard-divergence, survey)**: each format re-reads the DOM independently and builds its
  own structure → that's the root cause of drift. The fix (consolidate to one model) changes
  internals → survey, don't rewrite silently.

### A.1 — Export extras: Add date / Add profile (§13.9)

Two opt-in checkboxes on the right of the summary (`#add-date`
`[data-flove-add-date]`, `#add-profile` `[data-flove-add-profile]`) inject
an extra field into the model **before** serialization, so it must ride
into **all six** formats — they are part of the export, not chrome.

- **PASS**: with **Add date** on, every format carries the `date`; with **Add profile** on, every
  format carries the `profile` (basic info — at least the username/handle, read from the
  appy(-mini) profile). Both round-trip in JSON (`date`/`profile` keys survive `JSON.parse`),
  appear in md/xml/html/csv, and show in the JPG if space allows (else the visible `…`).
- **PASS (parity on toggle)**: turning a checkbox **off** removes the field from the next export —
  no stale `date`/`profile` lingers. Off is the default; an untouched app exports neither.
- **PASS (graceful when no profile)**: if no appy(-mini) profile/username is reachable, **Add
  profile** is disabled or yields an empty/omitted field — **never** a broken or half-written
  export. Same hostile-input + escaping rules apply to profile strings (a `<` in a handle stays
  inert in HTML/XML).
- **FAIL**: a checked extra is missing from any format; or it's read independently per-format
  instead of from the one model (drift); or unchecking leaves it in the export; or an absent
  profile produces a malformed file.
- **Machine vs prose**: the `date`/`profile` **keys** stay stable English (round-trip); only their
  prose renderings localize (MD/HTML), per §13.2.

## B. Axis 1 — summary parity

- Every selected/added item appears in the live phrase. **FAIL** if a selection isn't reflected.
- No stale item lingers after deselection. **FAIL** if removing a selection leaves it in the phrase.
- Empty fields are omitted from the model (only filled items carried).
- Entirely-empty model → export controls **disabled**. **FAIL** if you can download an empty file.

## C. Axis 2 — Views ↔ raters

- The four Views (bars · vertical · axial · spider) read the **same** `raters[]`. **FAIL** if a
  View has its own private copy of the ratings that can drift.
- Each `{n,max}` maps to the visual magnitude (bar height / column / axis length / spider radius),
  normalized by `max`. **FAIL** if a rating of 3/5 doesn't visually read as 60%.
- A number shown in a View equals the rater in the JSON export. **FAIL** on any chart/number drift.

## D. Axis 3 — the six formats

For **each** format: (1) wired to a canonical hook, (2) well-formed, (3) survives parse-back to the
same item set, (4) parity with the summary, (5) hostile input survives, (6) correct filename+MIME.

| Format | Ext | MIME | Well-formed means | Parse-back check |
|--------|-----|------|-------------------|------------------|
| Markdown | `.md` | `text/markdown;charset=utf-8` | `# <app>` heading + phrase + sections; raters as a table | re-read: every item line present |
| JSON | `.json` | `application/json;charset=utf-8` | built by `JSON.stringify(model,null,2)` | `JSON.parse` → same item set; **round-trip format** |
| XML | `.xml` | `application/xml;charset=utf-8` | `<?xml…?>`, all values via `esc`/`escAttr` | `DOMParser` → no `parsererror`; same items |
| HTML | `.html` | `text/html;charset=utf-8` | standalone `<!doctype>` + inline `<style>` | sandbox/parse → phrase present, no injection |
| JPG | `.jpg` | `image/jpeg` q≥0.9 | canvas render ≥1080px wide | **visual-only** — cannot round-trip (see degradation) |
| CSV | `.csv` | `text/csv;charset=utf-8` | one row per element, RFC-4180 quoting | split → same rows; quoted fields intact |

- **Hook present** (D.1): `[data-flove-save="<fmt>"]` exists and is wired. Missing format =
  Standard-divergence → survey (it adds UI).
- **JPG degradation**: renders ≥1080px; when content overflows it truncates with a **visible `…`**,
  never silently. Everything omitted from the JPG is still complete in the other five formats.

## E. Axis 4 — share readiness

- `navigator.share` is present, behind `[data-flove-share="mobile"]`.
- The `files` variant is **guarded** by `navigator.canShare({files})` and attaches the **standalone
  HTML** export (`<app>-summary.html`). **FAIL** if it shares a JPG/JSON file, or shares a file
  without the guard (throws on unsupported devices).
- Fallback ladder intact, in order: Web Share+HTML → Web Share text-only → `clipboard.writeText` +
  toast → share-intent rows (WhatsApp/Telegram/mailto, and print). The optional in-page intent grid
  uses `[data-flove-share="apps"]`.
- PWA/manifest/service-worker are **out of scope** — their absence is not a finding.

## F. Cross-cutting

- **Filename** = `<app>-summary.<ext>`, `summary` localized to the active UI language (§13.2):
  `summary` (en) · `resumen` (es) · the translaty word otherwise. `<app>` through a `safeName`
  (lowercase, `[a-z0-9-]`).
- **i18n parity (per active language)**: human prose localizes — the MD heading, the HTML `<title>`,
  the `navigator.share` title, the section labels. Machine names do **not** — JSON keys, XML element
  names, CSV headers stay stable English. **FAIL** if an ES export carries EN labels, or if a JSON
  key got translated (breaks round-trip).
- **Escaping**: one shared `esc`/`escAttr` pair serves XML **and** HTML. **FAIL** on hand-rolled
  per-format escaping or any unescaped value.
- **Hostile input**: an item containing `< & " ' , \n` and an emoji must come out whole and inert in
  all six — no broken XML, no CSV column bleed, **no markup injection in the HTML export**. This is
  the one place a correctness slip is also a security slip.

## G. Tier & distro gating

- Export is **advanced-tier**. `mini`/`basic` → **N/A (auto-pass)**, do not flag. `normal` →
  optional. `advanced`/`super` → full contract.
- Export is **JS-distro**. CSS-pure distro → **N/A**; its surface is print + copy only. Never flag a
  CSS-pure app for "missing" JS export.
