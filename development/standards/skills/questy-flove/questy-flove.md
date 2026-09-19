# Questy FLOVE

**Questy FLOVE** is the flove edition of the questy skill: the same structured
Q&A — read the project docs, detect the gaps and conflicts, ask the right
questions in typed batches — narrowed to the **flove apps themselves**.

It interviews the owner as a **user of the apps, never as the developer**. The
questions are the app's own reflections ("Do you think there is a goddess?" /
"Do you think she sees us?" for Goddy), not a maker's brief.

## What makes it FLOVE

- **App-scoped.** Each flove app is its own mini-survey. A session interviews
  the **43 catalogued apps** you pick, following the same five rainbow
  categories as the **apps full view**
  (`https://flove.org/central/apps/apps-full.html`): Inside · Mating ·
  Ling/Words · Social · Economy, each with its colour (orange · yellow · green ·
  blue · indigo). The grouping and colours are generated from the catalog, not
  hand-copied.
- **Catalog-driven colours & slots.** Each app's question carries the colour,
  hat and slot vocabulary from the machine catalog (schema
  `flove-hats/1`):
  **https://flove.org/development/standards/vocabulary/fields-colours.json** —
  the page embeds a generated snapshot (emitted by `build-questy-flove-data.py`)
  and can `⟳ sync` it from flove.org, caching it in `localStorage` so offline
  sessions stay current. The human spec is the vocabulary matrix
  (`https://flove.org/development/standards/vocabulary/index.html`); the field
  kinds and the hat ladder live in
  `https://flove.org/development/standards/vocabulary/flove-fields.md`.
- **The gauge.** A Flove influence scale (1–5) rides along — see
  [`plans/flove-influence.md`](plans/flove-influence.md) — so every session starts with a
  self-assessed intensity of how deeply the app's hat vocabulary and conventions
  colour the session.
- **Profile JSON for appy-basic.** The session's output is a **JSON you add to
  your appy-basic profile**, formatted to fit the appy profile standard
  (`https://flove.org/solo/apps/appy/appy-basic.html`, the `flove-profile`
  model). Answered questions land under `appsPlayed` keyed by the app's own
  question keys (authored reflections or input slots); the appy-basic import
  merges them without clobbering unanswered fields (schema
  in [`plans/design-flove-profile.md`](plans/design-flove-profile.md)). It is not a
  standalone HTML survey.

## The loop

pick app(s) → set the Flove influence degree → answer the app's own questions →
answers map to profile slots → export JSON → import into the appy-basic profile.

## Questy Flove Degrees

- **Flove influence (1–5).** How deep this pass goes into the flove way of
  working — None · Touch · Blend · Soak · All-in (spec in
  [`plans/flove-influence.md`](plans/flove-influence.md)). Picking the lowest number that
  still gives the app what it needs; 3 is the default.
- **All the questions are the app's own.** Every question is one the app itself
  asks its user; the owner answers as a user, never as a developer. There is no
  flove/owner split in the wording. The influence degree colours how deeply the
  app's hats and conventions weigh in, but never switches the interview onto a
  maker's brief. Until an app authors its reflective set, the page falls back to
  one reflection per input field.

## Siblings

- **Questy** — the core skill
  (`https://flove.org/development/standards/skills/questy/SKILL.md`)
- **Questy1** — the recommended bundle
  (`https://flove.org/development/standards/skills/questy1/SKILL.md`)
- **Questy FLOVE** — this edition
- **Questy DEV** — `https://flove.org/development/standards/skills/questy-html/index.html`,
  the build/dev view of the same engine (surveys, thinking-hat filters, pending,
  import/export)
- **Flove influence** — the 1–5 scale spec (`plans/flove-influence.md`)
- **Vocabulary catalog** —
  `https://flove.org/development/standards/vocabulary/fields-colours.json` (the
  machine source of each app's `input` fields)