# App tiers in `routing.json` — not in this trunk

**Status (2026-11-15): closed for this trunk.** `tier` is **not** part of
`tools/routing.json`, no app carries tier markup, CSS or fields, and the concept
was stripped from the apps this session (see the decision section at the end).
The mini → super variants survive only as demo sketches under `apps/blogy/`,
`apps/economy/dealy/`, `apps/puzzy/keys/` and `apps/appy/`.

## What a tier is

The app complexity/size class used by the distro and the offline package:

`nano · mini · basic · normal · advanced · super · mega`

It is a **routing/distribution** attribute, not a field-vocabulary attribute. It
does not affect `apps[].fields`, the category colour/hat, or the influence
ladder.

## Intended source

Per app, from its own meta tags:

```html
<meta name="tier" content="basic">
```

The future build scan would read it, validate it against the valid values, and
write it into `apps[].tier`.

## Why it is not live yet

- The first apps imported into `routing.json` (Goddy, Souls, Willy, Astry,
  DieSafe, Fivy, Hacky, PracSys, MyFamily, Inventary, Realy, Keys) do not all
  declare the meta tag.
- Without a declared tier, guessing produces false metadata. `status: "partial"`
  was being used only for this missing metadata, which obscured whether the
  **fields** were complete.
- The field tree is the current priority; tier can be added without changing it.

## When adopted

1. Add the `<meta name="tier" content="…">` tag to each self-contained app.
2. Scan and validate on the `routing.json` build.
3. Add `apps[].tier` and include it in the merge-not-replace key list.
4. Only then may an app with complete fields be blocked from `status:
   "complete"` by a missing tier.

Until then, `status` means **field completeness only**:
`complete` = full field tree extracted; `partial` = curated subset still to
extract.

## Decision — 2026-11-15 · removed from the trunk

Tiers are **not going into this trunk repo**. The owner will not implement them
here, so the concept was stripped out of the app code:

- **Puzzy launcher** — the `mini · basic · normal · advanced · super` stepper,
  its `data-tier` attributes, `tier-locked` bubbles, `TIERS`/`tierSel`/`applyTier`
  logic and the matching CSS are gone. Every app shows at every layout. The
  `tier` field and the per-app `tier` sub-field left the field manifest and
  `routing.json` too, so the portrait adapter no longer emits `tier` rows.
- **Souls** — the ladder vocabulary was renamed (`is-prev-pick`,
  `ladder-preview` / `ladder-label` / `ladder-chip`,
  `renderLadderPreview`, `refreshLadderPreviews`); it was a species → matter →
  particle ladder, never an app tier.
- **Fivy** — the gated `tier-pop` unlock module (`UNLOCK`, `checkUnlocks`,
  `openTierIframe`, `closeTierIframe`, the `.dl-btn` level message) was removed
  from its inlined `flove.js`; none of its hooks existed in Fivy.
- **Shared code** — `addons/code/js/flove.js` lost the same module, and
  `flove-loader.js` describes its browsy gift gate without tier language.
- **Catalog** — `apps/apps-full.html` and `central/apps/apps-full.html`: the
  Blogy tile is a normal app tile pointing at `blogy/index.html`; the
  seven-variant child list, the "Blogy · Launcher" cube, the "by tier"
  explainer and the "the flove tiers" tags are gone.
- **Distro pages** — `central/apps/{sety,wizy,gody}/index.html` lost their
  `flove:tier` meta and `tier` config/card entries.
- **Maty** — its unrelated "colour tiers / motion tiers" are now
  `colorStep` / `motionStep`.
- **Links & comments** — the catalog's Blogy tile points at the app, not the
  launcher, and `apps/puzzy/{wisy,linky}.html` comments no longer mention tiers.

Kept on purpose: `apps/blogy/`, `apps/economy/dealy/`, `apps/puzzy/keys/` and
`apps/appy/` still carry their mini → super variants as **demo sketches** for a
future release; they are the reference for how the idea would look, not a
feature of this trunk.

Left alone: `apps/sys/nety/index.html` says "hybrid local tiers" about storage
replication — a different meaning.
