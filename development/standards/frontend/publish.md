# flove · Publish to Appy — §13.15

Part of the flove frontend standards catalogue. Index / matrix: `../README.md` ·
contract: `../contract.md` · back to the catalogue: `../frontend.md`. Related:
the export summary-model (`export.md`, §13.12) is what gets published.

---

## 13.15 · Publish to Appy — portrait → profile

One **shared contract** so every flove app hands its result to the user's
**Appy** profile the same way. Phase 0/1, **no backend**: the app exports its
`flove-portrait/1` JSON and the user drops it on Appy, which stores it locally
(`flove:appy:plays`, one record per play, field `portrait`).

> **The app-side writer bridge is retired.** Apps no longer inline a
> `data-flove-publish` bridge; their summary section offers **Magic · Share**
> with Save JSON first, and the portrait file is the transfer. Appy still ships
> its **reader** (same API names) so older pages and the profile view keep
> working.

**The path.** Two paths, same portrait:

1. **Share → Appy (one click).** The app validates its own
   `flove-portrait/1`, writes one play (`via:'share'`) to `flove:appy:plays`,
   and shows **“Saved in your Appy profile · See profile”**. No extra confirm —
   the click is the consent. Appy re-validates on read and **renders the card
   automatically** (no raw-JSON view). If local storage is blocked, the app
   falls back to Save JSON + upload. On `file://` (per-file storage) the app
   opens Appy and hands the play over by `postMessage`, so the profile is
   actually updated there.
2. **Manual.** Download `<app>-portrait.json` (§13.12) and drop it on Appy’s
   **“Upload played app here”**. This is the durable fallback everywhere,
   including `file://` and private windows.

That file is the **portrait exported from the app's summary section** — Appy
renders portraits; the summary stays in the app and travels to the profile as
the play's `portrait`.

**WRITER contract (an app that exports).** The summary section exposes
**Magic · Share** with **Save JSON** first (§13.9), producing
`<app>-portrait.json` from `window.flovePortrait.get()` (falling back to
`window.floveSummary` only for older apps). **Send to Appy** is the second
Share item. The old inlined `data-flove-publish` trio stays retired; the
one-click write lives in the app’s Share action, not in a separate bridge.

Optional richer agent payload: `window.floveAgentBlock = (portrait) => ({
prompt, schema, context, suggestions })` — used when Appy hands a portrait to an
agent.

**Reader (Appy).** `apps/appy/appy-basic.html` renders any uploaded portrait,
stores every play in `flove:appy:plays`, and shows the profile. A play opens as
the **rendered flove card** (auto-render), not as raw JSON; the bridge API
(`window.floveAppy.read/played/publish/clear`) remains for pages that include
it, and auto-sync is a convenience over the upload — never the only path.
Downloads stay current by re-downloading; the stored profile updates on upload.

**Reference:** `apps/appy/appy-basic.html` (the reader + profile store) ·
`apps/appy/appy-mini.html` (the compact reader) · `apps/metas/goddy.html` (a
working portrait exporter).
