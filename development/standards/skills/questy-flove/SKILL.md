---
name: questy-flove
description: >-
  The flove edition of the questy skill — structured Q&A that interviews the
  OWNER as a user of the flove apps, never as the developer. It drives the
  questy-flove page: pick app(s) → set the Flove influence degree (1–5) →
  answer typed batches of the app's own reflective questions — what you think
  and feel inside it, e.g. Goddy asks "Do you think there is a goddess?", "Do
  you think she sees us?" — → export a JSON you can import into your appy-basic
  profile, formatted to flove's profile standard. Questions, colours and hats
  follow the vocabulary catalog (`fields-colours.json`, schema `flove-hats/1`),
  which the page embeds and can sync from flove.org.
  Use when the owner types /questy-flove or wants to "digitalise an app's
  profile", "interview the apps", "record what I think about an app's
  questions", "fill the appy profile for an app", or run a structured
  flove-app review. Override via the personal config (see CONFIG.md).
---

# questy-flove — structured Q&A about the flove apps

The flove edition of **questy**: the same structured interview — read the source,
detect gaps and conflicts, ask the right questions in typed batches — narrowed to
the **flove apps themselves**.

The app is the `questy-flove/index.html` page: pick app(s), set the influence,
answer, and export — see [`index.html`](index.html), [`plans/flove-influence.md`](plans/flove-influence.md)
and [`plans/design-flove-profile.md`](plans/design-flove-profile.md).

## The objective — interview the user, not the developer

Questy-flove does NOT brief the app's maker. It interviews the owner as a **user
of the app**, and the questions are the app's own — the reflections the app
itself invites. The maker is never asked how to build, develop or set something
up.

For **Goddy** (a "Goddess · God · Us" matrix — who sees whom, and how fully), the
questions are exactly what the app asks its user:

- "Do you think there is a goddess?" · "Do you think there is a god?"
- "Do you think the goddess sees us?" · "Do you think we can see the goddess?"
- "Do you think god sees us?" · "Do you think we can see god?"
- "Do the goddess and god see each other?" · "Do you think we truly see ourselves?"
- "How fully do we see — a glimpse, a fuller look, or the whole?"

The owner's answers are their positions; they ride in the exported profile under
the app's name. Every flove app authors its own reflective set (the page's
`APP_QUESTIONS` block). Until a set is authored, the page falls back to one
reflection per input field (e.g. "What do you think about Children in Daty?").

## The loop

```
pick app(s) → set Flove influence degree → answer app questions (typed batches)
→ answers map to profile slots → export JSON → import into the appy-basic profile
```

## App-scoped, coloured by the apps full view

A session interviews the **apps you pick, not a generic project**. Each flove app
is its own mini-survey. The picker groups the **43 catalogued apps** in the same
five rainbow categories as the **apps full view**
(`https://flove.org/central/apps/apps-full.html`) — the canonical launcher's
"apps/index" full view:

| category | colour | apps in the picker |
|----------|--------|--------------------|
| **Inside** (`cat-inside`) | orange `#ff9b5e` | Goddy, Astry, Hacky, DieSafe, Souls, Profily, Sensy, Pracsys, Willy, MoralY, Lovy |
| **Mating** (`cat-mating`) | yellow `#ffd84d` | Daty, MyFamily, Maty, Varyy, Evily, Trusty, Crumbly, Parenty |
| **Ling / Words** (`cat-ling`) | green `#6ed089` | Fity, Keys, Fivy, Puzzy, Loly, Wisy |
| **Social** (`cat-social`) | blue `#5ea4e6` | Questy, Realy, Nety, Socy, Blogy, Wizy, Browsy |
| **Economy** (`cat-economy`) | indigo `#6b6bd9` | Crafty, Worthing, Lowy, Dealy, Freed, Inventary, Minioffer, Offer, Rewardy, Shareful, Wanty |

The grouping, colours and app order are **generated from the catalog**, not
hand-copied: `build-questy-flove-data.py` reads the catalog and emits the picker
chips (shareful pinned → Economy; lovy home → Inside), so every chip matches both
the catalog and the full view the owner navigates.

## Each answer references the vocabulary catalog (input fields)

The questions are the app's own reflective set (`APP_QUESTIONS` on the page) and
they land on the app's profile slots. The words, colours and hats those questions
carry come from the vocabulary **catalog** — inputs first, hats as secondary
metadata:

- **Machine catalog (inputs + hats):** `https://flove.org/development/standards/vocabulary/fields-colours.json`
  — schema `flove-hats/1` (generated 2026-09-12 · 43 apps). Every `kind:input`
  slot lives under its app in `apps[].slots`; the page reads it directly. Nine
  apps (cathy, fity, loly, wizy, questy, nety, browsy, dealy, lowy) carry zero
  input slots by design — they get no questions until their reflective set is
  authored.
- **Human spec (kinds + slots):** `https://flove.org/development/standards/vocabulary/index.html`
  — the vocabulary matrix, `slotKinds` object, kind `input` (the kind filter
  "input" yields the exact field list). /vocaby keeps both in lockstep; drift is
  gated by `https://flove.org/development/standards/vocabulary/scripts/check-drift.py`.
- **Contract doc:** `https://flove.org/development/standards/vocabulary/flove-fields.md`
  — the field-kind model (`input`/`display`/`action`/`nav`) and the hat ladder
  spec this section summarises.
- **Hats are secondary; the parent colour weighs 50% more (~60/40).** An un-set
  slot inherits its app's signature hat, an app without one its category's; when
  a slot has its own hat, the effective question colour blends slot + parent with
  the parent weighed 50% more (~60/40) — never 100% the slot's own.
- **Page is regenerated, not hand-edited:** the embedded snapshot
  (`CATEGORIES`/`INPUT_FIELDS`/`CAT_COLOURS`) is emitted from the catalog by
  `https://flove.org/development/standards/vocabulary/scripts/build-questy-flove-data.py`
  (`--apply` patches the page; `--dry-run` shows the diff). The sibling
  `fields-colours.ods` is the spreadsheet view, built by
  `https://flove.org/development/standards/vocabulary/scripts/build-fields-colours.py`
  (never hand-edit either).
- **Local/offline mode:** the Catalog card offers `⟳ sync from flove.org` —
  fetched once online, the catalog is cached in `localStorage`
  (`questy-flove-catalog` + `questy-flove-catalog-at`); later offline sessions
  interrogate the cached copy, staying in sync without a re-deploy.

Input slots are user data (e.g. daty → Gender, Children, About-me; sensy →
HELLO!, Incentives, Annex…); display/action/nav are copy and controls and are not
questioned.

## The output is profile JSON for appy-basic

The session does NOT produce a standalone HTML survey. Its output is a **JSON you
add to your appy-basic profile**, formatted to fit the appy profile standard
(`https://flove.org/solo/apps/appy/appy-basic.html` — the `flove-profile`
model). Shape:

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

- `appsPlayed` holds one entry per interviewed app, carrying the answers keyed by
  the app's own question keys — its authored reflective keys (like "Goddess
  sees us") or the vocabulary `input` slots — plus the app's full-view colour.
- `influence` carries the Flove influence degree (1–5) that shaped the session.
- The appy-basic import merges into the profile without clobbering fields you did
  not answer (see `plans/design-flove-profile.md` schema notes).

## Questy Flove Degrees

### The Flove influence degree (1–5)

Every session starts with the **Flove influence** gauge — a single self-assessed
pick (1–5) of *how deep this pass should go into the flove way of working*. Full
spec in [`plans/flove-influence.md`](plans/flove-influence.md).

| # | name  | effect on the interview |
|---|-------|-------------------------|
| 1 | **None**  | purely your project, no flove vocabulary or conventions |
| 2 | **Touch** | light flove flavour, no ceremony |
| 3 | **Blend** | flove conventions where they help (default sweet spot) |
| 4 | **Soak**  | flove standards throughout |
| 5 | **All-in**| the full flove workflow, every hat, every addon |

Rule of thumb: pick the lowest number that still gives the project what it needs.
3 is the recommended default; 4–5 for apps living in the flove circuit; 1–2 for
standalone things that merely borrow a look.

### All the questions are the app's own

Every question is one the app itself asks its user; the owner answers as a
**user**, never as a developer. There is no flove/owner split in the wording:
the app's reflective questions are the interview.

The **Flove influence** still shapes the session — how deeply the app's hat
vocabulary and conventions colour the questioning (see the table above) — but it
never switches the interview onto a maker's brief, and it never changes the
questions, only how the profile slots the answers land on are weighted.
The `influence` value rides in the export.

## Personal config

Fork/reuse this for another project by creating a personal config that overrides
the defaults instead of editing the skill (see
`https://flove.org/development/standards/skills/CONFIG.md`): a shared
`~/.config/flove/skills-config.yml`, a per-skill `settings.yml`, a hidden
`.settings`, or a `config.yml` in the skill folder. Only the keys you set change;
everything else falls back to these defaults.

## Siblings

- **Questy** — the core skill
  (`https://flove.org/development/standards/skills/questy/SKILL.md`)
- **Questy1** — the recommended bundle
  (`https://flove.org/development/standards/skills/questy1/SKILL.md`)
- **Questy FLOVE** — this edition (the flove-app profile interview)
- **Questy DEV** — `https://flove.org/development/standards/skills/questy-html/index.html`,
  the build/dev view of the same engine (surveys, thinking-hat filters, pending,
  import/export)
- **Flove influence** — the 1–5 scale spec (`plans/flove-influence.md`)
- **Vocabulary matrix** — `https://flove.org/development/standards/vocabulary/index.html`
  (the source of each app's `input` fields)
- **Catalog (flove-hats/1)** — `https://flove.org/development/standards/vocabulary/fields-colours.json`
  (the machine source of this page's data)
