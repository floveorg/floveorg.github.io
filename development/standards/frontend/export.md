# flove · Export & share — §13.12

Part of the flove frontend standards catalogue. Index / matrix: `../README.md` · contract: `../contract.md` · back to the catalogue: `../frontend.md`.

---

## 13.12 · Export & share contract — summary-model → portrait JSON

Part of the flove frontend standards catalogue. The `/exporty` and `/jsony`
skills audit an app against this contract; Goddy is the reference.

**The current model is JSON-only.** Every app exports **one file**,
`<app>-portrait.json`, a `flove-portrait/1` envelope built from its summary
section. Appy renders that portrait into the human HTML view. The former
six-format contract survives only in the documented **exceptions** below.

**Summary section ≠ portrait file.**

| | What it is | Where it lives | Names |
|---|---|---|---|
| **Summary section** | the live panel an app builds from the filled fields: phrase, raters, views | inside the app; `window.floveSummary` exposes its model; Appy stores a published copy as the record field `portrait` | “summary”, `floveSummary`, `rec.portrait` |
| **Portrait file** | the JSON exported *from* that section: `flove-portrait/1` with phrase + rows | a downloaded file, `<app>-portrait.json`, re-importable and renderable by Appy | “portrait”, `flovePortrait`, `<app>-portrait.json` |

Appy is the renderer of **portraits**; a profile record stores the portrait
(`rec.portrait`). The apps own
the summary section; the file it emits is the portrait.

**How the file leaves the app.** The summary row shows two buttons — **Magic**
then **Share**. **Save** is Share's first menu item, never a sibling: it emits
`<app>-portrait.json`. On a touch device Share calls the native share sheet with
the JSON file attached, so saving is one of the sheet's own options; on desktop
it opens the small menu (Save JSON · Email, plus whatever share targets the app
offers).

**The envelope.** Built once per export from the summary model:

```js
{
  schema: 'flove-portrait/1',
  app: '<slug>', version: 1,
  generatedAt: '<ISO>',
  lang: '<en|es|…>',
  phrase: '<one italic line>',          // the summary's live (or edited first) line
  rows: [ { key, kind, title, items[] } ],  // the extractive core
  summary: { text, edited: true },       // optional: the editable summary box
  words: [ … ],                          // flattened items (optional)
  completeness: { layers, total },
  stats: { … },                          // app-specific counters (optional)
  consent: { share, purposes: ['self-reflection','export'] },
  source: { url }
}
```

`rows[]` is the only required payload beyond the identity fields; `phrase` and
`words` feed Appy's renderer. API: `window.flovePortrait.get / validate /
consult / selfTest`; `window.floveSummary` remains the older model fallback.
JSON keys stay stable English; only prose follows the active language.

**Parity.** The portrait mirrors the filled fields: one row per filled item (or
per app-defined group), no invented data, no dropped items. Empty fields are
omitted rather than exported as blanks. A portrait that was exported and
re-imported must produce the same phrase and rows.

**Hostile input.** `JSON.stringify` handles escaping; no manual string building
for the portrait. HTML/XML escaping rules apply only to the exceptions that still
emit those formats.

**Filename.** `<app>-portrait.json`. Appy accepts that name (and legacy
`<app>-summary.json` uploads, matched by app slug). There is no localized
filename suffix — the extension and app slug are stable.

**Share to mobile.** Default share carries the JSON file:
`navigator.canShare({files})` → `share({files:[portrait]})`; text-only share and
clipboard are the fallbacks. The share sheet can save the file, which is why
Save lives inside Share.

**DOM hooks (canonical).** `#floveSummaryMagic`, `#floveSummaryShare`,
`#floveSummaryShareMenu`, `[data-action="save"]`, `[data-action="download"]`,
`data-flove-save="json"` — every audited app uses one of these patterns, and
`jsony --summary` reads them (Magic + Share, Save inside Share).

**Share → Appy rollout (2026-11-17).** The standard-tier apps from
`development/index.html` carry the inline `flove-appy-standard` action. It
inserts an **Appy** item after Save JSON (or a fixed fallback control when the
app's share UI predates the standard), validates `flovePortrait.get()`, writes
one `via:'share'` record to `flove:appy:plays`, and shows **“Saved in your Appy
profile · See profile”**. Goddy and Keys were the first; Appy is the receiver.
The action never uploads: the click is the consent and Appy re-validates on read.

**Exceptions — they keep their own exports.** `blogy` and `fivy` are the two
apps still in `EXPORT_EXCEPTIONS`:

| App | Export surface | Difference from the standard |
|---|---|---|
| `blogy` | Save bundle (md · json · csv · xml · html · jpg) + generic card/ZIP exporter | JSON is first and carries `phrase` + `rows`; the bundle still ships |
| `fivy` | Standard Magic · Share (JSON first) + its generic card/ZIP exporter | summary surface is standard; the card exporter is separate |

`keys` and `souls` are **standard targets** since 2026-11-17. Their Share offers
**Save JSON** and **Save HTML**: the JSON is the `flove-portrait/1` envelope, the
HTML is a self-contained card generated from the same `rows` in the same pass —
one model, two files. The retired multi-format serializers (CSV, XML, JPG,
`buildSummaryDocHTML`) stay retired; the HTML card is not one of them and needs
no exception. `worthing` follows the same two buttons and its saved HTML is its
**axial view**, cloned from the live SVG. `fivy` has the same Save JSON/HTML
pair inside Share; its separate card/ZIP exporter is what keeps it in the
exception set. The live view is `addons/rendery/index.html`.
`jsony --app` is clean for all of them.

In every exception the **JSON envelope is the same `flove-portrait/1`** as
everywhere else, and JSON is the first Save item. Legacy serializers may remain
only to serve those multi-format exports; `jsony --app` reports them as
documented exceptions.

These are variants of **one** set: `jsony_check.py` keeps a single
`EXPORT_EXCEPTIONS` and no second list. The pages outside the contract below
belong to the same set; each page's type is in the development index's app
table — `development/index.html` → **Web → Apps** (`#web-apps`).

**Distro.** The portrait is generated client-side from inlined code; no runtime
dependency and no build step. Apps remain single self-contained files, and the
export works offline and from `file://` (download path).

### Runtime conformance (dev)

Every routing app with a real portrait bridge (manifest or not — `keys` has no
`flove-fields`) carries an inline `window.flovePortrait.conformance()`
(`data-flove-conformance`, generated by `development/scripts/inject-conformance.py`). It
returns `{ok, checks[], errors[], advisories[], coverage}`:

| Check | Level |
|---|---|
| `get()` returns an envelope · schema · app slug · `rows[]` | critical |
| `validate()` accepts it · row keys unique · no blank items · filled rows titled | critical |
| `consult()` returns `flove-consult/1` and a subset of `get().rows` | critical |
| filename `<app>-portrait.json` · blob MIME `application/json;charset=utf-8` | advisory |
| field-id coverage vs `floveFields()` (parity is advisory: rows are semantic layers, not a field dump) | advisory |
| `merge()` accepts a probe row (`__conformance__`) without applying it | advisory |

**Summary box.** The summary exposes one editable box (all selections) with one
global Copy at its bottom-right. Edits are an overlay: the first line becomes
`phrase`, the whole text travels as `summary: {text, edited}`; the form fields
stay the source of truth for the data. Goddy is the reference.

**Rendery — the flove JSON converter.** `addons/rendery/index.html` (published) turns any `flove-portrait/1`, `flove-consult/1` or `flove-profile` into **Card · Editorial · Compact**, a **data** view (bars + completeness ring), **JSON-LD / Turtle** linked data, and raw **JSON / XML**. Appy carries a single link to it in Export — it is a separate tool, not Appy's renderer. The card view is also what souls and keys open with **◫ HTML view**.

**One live profile.** Appy’s **Profile** tab is the single live profile: it
already carries Authy data, played apps, Play apps, Upload played app and the
topbar. There is no second in-Appy “See” page; Share → Appy and Authy →
Telegram land on `appy-basic.html#profile`, with the unlock tour. **View &
Export** (next to Upload, 33%) generates a self-contained HTML snapshot of the
whole profile with a **Share** button (`navigator.share` files) and Save HTML;
**Export JSON** lives in **Privacy → Export**. Appy play cards use its own
internal card renderer, not Rendery.

`development/tools/conformance.html` loads the apps from `tools/routing.json` in
an iframe and runs it; `?app=<id>&auto=1` tests one, `?expand=1` opens the
checks, `?skip=lowy,...` omits a page that blocks the run. Serve it over HTTP
(`file://` iframes are opaque origins; Chrome needs
`--allow-file-access-from-files`). An app that blocks its own thread can freeze
the harness — reload and run the rest with `?skip=` or one at a time with
`?app=`. An empty app passes the envelope checks — green does **not** prove
filled-data parity. It is a smoke test; the renderer and the Appy round-trip
remain `exporty`'s.

### Pages outside the export contract

`tools/routing.json` also lists pages that are **not apps with a summary
surface** — launchers, skill pages, project sites and dev prototypes. They carry
no `flovePortrait`, so `jsony --app <id>` reports them as exempt instead of
failing. This is a documentation list, not a wish list: when one of these pages
grows a real summary, remove it here.

| Page (routing id) | File | Why it is exempt |
|---|---|---|
| `puzzy` | `apps/puzzy/index.html` | Puzzy launcher — the folder's own home, no summary |
| `questy` | `development/standards/skills/questy/index.html` | skill page opened as a web app |
| `loly` | `projects/liberada/risa/index.html` | risa project site |
| `wizy` | `apps/sys/wizy/index.html` | sys-cluster engine, not a flove summary app |
| `browsy` | `apps/sys/browsy/index.html` | sys-cluster extension and bridge |
| `chacrikun` | `chacrikun/index.html` | project-folder app |
| `electrorchestra` | `electrorchestra/index.html` | project-folder app |
| `frotis` | `frotis/index.html` | project-folder app |
| `sety` | `apps/sys/sety/index.html` | settings surface, no summary |
| `vizy`, `vizy2` | `apps/puzzy/dev/*.html` | dev prototypes, not shipped apps |
| `nety` | `apps/sys/nety/index.html` | social-network surface, no summary |
| `profily` | `apps/appy/profily.html` | profile surface, no summary |
| `rewardy` | `apps/economy/dealy/rewardy.html` | rating playground, no summary export |

`fity` is expected to gain its summary soon and is **not** on this list.
