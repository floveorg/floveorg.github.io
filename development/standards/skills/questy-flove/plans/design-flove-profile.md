# Questy FLOVE — flove-app questions → profile JSON (design)

**Date:** 2026-09-12 · **Status:** implemented — `index.html` drives the loop;
this file records the schema and the data-flow notes.

## What this adds

The core questy skill interviews *your project* generically (thinking hats,
pendings, batches). **Questy FLOVE** narrows that to the flove ecosystem itself:

1. It only asks questions **about flove apps** — each flove app is a survey
   topic, so a session interviews one (or several) of the **43 catalogued
   apps**.
2. Each answered question lands on an **app profile field**; the session
   exports a **`flove-profile` JSON** that can be imported into the appy-basic
   profile and fills the fields the user answered.

## The loop

```
pick app(s) → set Flove influence (1–5) → answer the app's own questions (typed batches)
→ answers map to profile slots → export JSON → import into the appy-basic profile
```

## Sources (full URLs)

- **Catalog (inputs + hats):**
  `https://flove.org/development/standards/vocabulary/fields-colours.json`
  (schema `flove-hats/1`, generated 2026-09-12) — `apps[].slots` lists each
  app's user-data fields. The page's embedded snapshot is emitted by
  `https://flove.org/development/standards/vocabulary/scripts/build-questy-flove-data.py`
  and can be live-synced (Catalog card → `localStorage`).
- **Apps full view (categories & colours):**
  `https://flove.org/central/apps/apps-full.html`
- **Appy profile model (import target):**
  `https://flove.org/solo/apps/appy/appy-basic.html`
- **Human spec of the field kinds & hat ladder:**
  `https://flove.org/development/standards/vocabulary/index.html` and
  `https://flove.org/development/standards/vocabulary/flove-fields.md`

## The questions — the app's own reflections

The session interviews the owner as a **user of the app, never as a developer**,
with the app's own reflective questions:

- **Authored sets (`APP_QUESTIONS` on the page).** Each entry is one reflection
  the app invites — e.g. Goddy asks "Do you think there is a goddess?", "Do you
  think she sees us?", "How fully do we see — a glimpse, a fuller look, or the
  whole?" — answered from candidate positions (`Yes / No / Not sure / It
  depends`). Each entry carries a `key` (the profile slot it lands on), the
  `text`, and the `opts`.
- **Fallback until authored.** One reflection per `input` slot ("What do you
  think about {field} in {app}?"). Apps with zero input slots (cathy, fity, loly,
  wizy, questy, nety, browsy, dealy, lowy) get no questions until their set is
  authored.
- **Hats and colours.** Each question carries its blended colour — the slot's
  hat (~40%) mixed into the app's category colour (~60%, the parent wins). A slot
  without its own hat inherits its app's signature hat, an app without one its
  category's.

## JSON schema (export — `flove-profile`)

```json
{
  "kind": "flove-profile",
  "version": 1,
  "exported": "...",
  "handle": "@you",
  "presence": "LIVE",
  "stage": { "name": "newbie", "index": 0, "stars": 0 },
  "facets": { "personal": 0, "local": 0, "social": 0, "global": 0 },
  "appsPlayed": [
    { "app": "Daty", "colour": "#ffd84d",
      "answered": { "Gender": "Woman · Man", "Children": "Yes" } }
  ],
  "influence": 3,
  "visibility": { "content": "mynet", "resources": "mynet", "profile": "private", "scores": "private" }
}
```

- `appsPlayed` holds one entry per interviewed app, keyed by the app's own
  question keys (authored reflective keys like "Goddess sees us", or the
  vocabulary `input` slots), plus the app's full-view colour; apps with no
  answered slot are omitted.
- `influence` carries the Flove influence degree that shaped the session.
- `stage`, `facets`, `visibility`, `handle` and `presence` are appy-profile
  plumbing — the import reads them and the appy-basic editor owns them.
- Import merges into the profile without overwriting fields the user did not
  answer in this session.

## Files

- `flove-influence.md` — the 1–5 scale spec (shared reference).
- `index.html` — the questy-flove page: app picker → influence gauge → question
  batches → JSON export (download / copy / preview), schema above.
- `questy-flove.md` — loop + siblings doc (updated).