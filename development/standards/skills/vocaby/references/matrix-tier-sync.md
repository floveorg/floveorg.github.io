# Syncing the matrix-tier table

The matrix-tier table is the **shown mirror** of every app's vocabulary. After you clean a
file's vocabulary (steps 2–5), its copy here goes stale and must be updated (step 6). Read
this then.

## Where it is

`development/standards/flove-vocaby.html` — renamed 2026-08-03 from the old
`flove-tiers-matrix.html`; its `<title>` is "flove · standards matrix". It is **not** one
HTML `<table>` — it's a JS data model rendered into editable tables. The piece this skill
touches is the **vocabulary** model (`const vocab`, `SLOTS`, `LABELERS`, `appSlots`).

## The data model

Read the arrays at the top of the file — they are the source of truth, and they change:

```js
const APPS      = [ /* 36 app keys */ ];
const SLOTS     = ["App title","Tagline","Entry label","About (body)"];   // 4 global slots
const LABELERS  = ["Default","Formal","Casual","Hotter","Lovely","Fatal","Lucky","Random"]; // 8 tone columns
const appSlots  = { blogy:[...custom slot names...], ... };               // per-app extra slots
const vocab     = {
  blogy: {
    "App title": { Default:"blogy", Casual:"blogy", Hotter:"blogy, baby", Lovely:"dear blogy ♥", ... },
    "Tagline":   { Default:"Compose and label your entries.", Casual:"jot stuff...", ... },
    // one entry per slot (global + appSlots[blogy]); each is slot → {labeler: text}
  },
  daty: {...}, // one entry per app in APPS
};
```

Rendering: `appSection(app)` concatenates `SLOTS` + `appSlots[app]`, builds one row per slot
from `vocab[app][slot]` and one column per `LABELERS` into `#appList`; the chip bar
(`pickApp`) filters to one app or "All". So the shape you edit is
**`vocab[app][slot][labeler] = "text"`**, with `appSlots[app]` declaring any slot beyond the
global 4.

**The reference prompt for the update task**: the file's own export — `updateExport()` →
`vocabLines(app)` emits, for each non-empty cell, one Markdown row under
`# {app} — vocabulary`: `{app}.V{n}: [{slot} · {labeler}] {value}` (the `V{n}` numbering
matches the cell numbers shown in the UI). That is the "Prompt for Claude" you must match
when reporting/updating the vocabulary. Line numbers drift — re-grep `const vocab`,
`const SLOTS`, `const appSlots`, `appSection`, `vocabLines` before editing rather than
trusting the ranges above.

## Resolving file → app key

The relationship is **1:1**: each app's HTML file has its vocabulary copied into one
`vocab[<key>]` entry. The key is the app name, which is usually *not* the filename:
`apps/puzzy/keys.html` is the "keys" app, but the matrix key could be `keys` or `puzzy`.
Resolve it, don't guess:

1. Look at the existing keys of `vocab` and `appSlots` — match by the app's own title/slug.
2. Cross-check the `APPS` list in the same file.
3. If still ambiguous (or the app has no entry yet), **ask inline** which key to use — this
   is a one-line question and a wrong guess corrupts a different app's row.

## Editing surgically

- Touch **only** that app's `vocab[<key>]` object (and `appSlots[<key>]` if slot names
  changed). The other apps in `APPS` must diff as untouched.
- A **rename** of a term in the source file → rename the matching slot key here and/or update
  the `Default` value; keep the other labeler columns unless they referenced the old word.
- A **removed** legacy term (e.g. a dead péntada) → delete its slot row and its `appSlots`
  entry if present.
- An **added** term → add the slot row with at least a `Default`; leave other labelers blank
  or carry sensible tone variants if obvious.
- **Preserve nesting and columns:** every slot keeps its full `{labeler: text}` map; don't
  collapse a slot to a bare string. If the source nesting is deeper than slot→labeler (decks
  → items), the matrix only models slot→labeler — represent the deck as a slot and note in
  the report that the finer nesting lives in the report, not the matrix.
- Keep formatting consistent with the surrounding entries (the file uses compact one-line
  slot objects); match it so the diff stays readable.

## After syncing

The matrix file and the source file now agree. Finish the workflow's step 7: the default
Markdown export `vocaby-<app>.md` (one item per row) plus the optional `vocaby-<app>.html`
are the app deliverables on disk; the fine vocabulary (systems, platforms, ids, renames
applied) that the slot × labeler grid can't hold lives in the **export**, with the
**report** explaining the decisions. No `vocab-*.json` is written — the scanner's
`inv.json` is internal tooling. When the update task needs a prompt, mirror the matrix
file's own "Prompt for Claude" export format (`app.V#: [slot · labeler] value`).
