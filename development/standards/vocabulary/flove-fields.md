# flove fields — vocabulary data model (temporary plan)

> **Status:** working plan. The real spec *is* `index.html` in this folder (the
> vocabulary tool) — this file will become a dump of its final model once the
> tool settles. For now it records the contract so questy-flove can consume it.

## Field kinds

Every slot in the vocabulary matrix wears exactly one **kind**:

| kind | meaning | example |
|------|---------|---------|
| **input** | user data a person fills in | Gender, Children, About-me, Relationships, Projects |
| **display** | descriptive copy | App title, Tagline, Entry label, About (body) |
| **action** | buttons / controls | Save, Share, Insights, Resume actions |
| **nav** | navigation chrome | Menu, Steps, Views, Stage nav |

- Tagged in `slotKinds` (hand-curated, human-owned — never auto-inferred).
- Unlisted slots default to `display`.
- The tool filters by kind (All / input / display / action / nav); exports honour
  the active filter.

## The `kind:input` contract (what questy-flove reads)

`kind:input` is the **user-data field list** — the exact slots to gather texts
about through questioning. It is a target contract for a future questy-flove
consumer, not a live dependency. The tool's export with the kind filter set to
`input` yields it directly.

## Hats & colours (flove-hats/1)

The questy-flove question-colour association. **Canonical data lives in
`fields-colours.json`** (schema `flove-hats/1`) — categories, apps and slots all
wear a hat; the sheet is a generated view, never hand-edited.

- **Six hats** (from /questy1): facts ⚪ · heart ❤ · risk ⬛ · optimism 🟡 ·
  creative 🟢 · make 🔵.
- **Five categories**, each with a colour and the hat it wears as session
  framing (its analogy is the session intro line):

  | category | colour | hat |
  |----------|--------|-----|
  | Mating | `#ffd84d` | optimism |
  | Inside | `#ff9b5e` | heart |
  | Ling / Words | `#6ed089` | creative |
  | Social | `#5ea4e6` | make |
  | Economy | `#6b6bd9` | facts |

- **The ladder** (hat resolution — the **parent colour is weighed 50% more**
  than a lower one): an un-set slot fully inherits its app's hat, an un-set app
  its category's; when a slot has its own hat, the **effective colour** is a
  blend of the slot's hat and the nearest parent hat, weighted 50% heavier
  toward the parent (≈ 60/40):
  1. category hat = session framing default (always set)
  2. app `hat` = the signature badge on the app's row
  3. slot `hat` (one per `kind:input` slot) = the per-question colour refinement —
     a field may differ from its category, e.g. white/red fields inside yellow apps
- **Inputs first, hats secondary — this file is questy-flove's source.** The
  `apps[].slots` maps are the user-data catalog: every `kind:input` slot must be
  present (the load-bearing part). Hats are cosmetic metadata and may be inherited
  rather than explicit; a missing hat never excuses a missing input.
- **Apps without input slots** still carry category + signature hat
  (signature-only rows, e.g. blogy, nety, cathy, wizy, dealy, lowy).
- **Derived artifact:** `fields-colours.ods` — identical row shape to this
  spec (colour-chip banner, hat analogies, header, then one signature row per
  app + one row per input slot with ● in its hat column). Regenerate with
  `scripts/build-fields-colours.py`; the script writes the ODS natively and
  needs no LibreOffice.
- **Consumers:** questy-flove colours each question by the slot's hat;
  vocabulary matrix exports may carry the hat alongside `kind`.

## Labelers ↔ hats (compositional rendering)

Pick a hat → a slot is worded in that hat's labeler family. One family, or the
wild card:

| family | labelers | hats |
|--------|----------|------|
| Love ❤ | Lovely · Hotter | heart 🟥 (green 🟩 hot) |
| Joy 😂 | Lucky | optimism 🟨 |
| Wisdom 🫠 | Formal · Casual · Fatal | facts ⚪ · risk ⬛ · make 🟦 |
| Random 🎲 | any family, or a new voice | creative 🟩 |

- **Default** = any hat (the slot adopts the active hat's voice).
- **Random** = wild card — any family, or a brand-new labeler.

The questy survey selects a family via its **Love · Joy · Wisdom** row; each
segment links to the matching anchor on `central/apps/wizy/` (`#love #joy #wise
#random`), which hosts the interactive preview.