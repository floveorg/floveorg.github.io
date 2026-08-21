# Extracting a flove app's vocabulary

How to pull the term inventory out of a single-file app, tie each internal name to the word
the UI shows, and keep the nesting. Read this when running step 2 of the skill.

## Run the scanner first

`scripts/extract_vocab.py` does the mechanical discovery so you don't grep by hand:

```bash
python scripts/extract_vocab.py <file> --labeled       # terms with a label or legacy flag
python scripts/extract_vocab.py <file> --summary       # just the counts
python scripts/extract_vocab.py <file> --out inv.json   # full inventory to a file
python scripts/extract_vocab.py <file> --deep-json out.json  # translatable display layer only
python scripts/extract_vocab.py <file> --no-display    # machine terms only (drop display)
```

It works on **two layers** deliberately:

1. **Machine names** — class / id / input-name / data-attr / i18n-key, every `sites` line (the
   basis for an atomic rename), a `load_bearing` flag set only when a state selector (`:checked`,
   `:has(`, `:target`, `:focus-within`) or a `for=`/`:has(#id)`/`aria-*` reference keys on it —
   plain styling selectors are *not* flagged — the resolved `label`, a `maybe_legacy` flag, the
   `data_blocks` (deck→items, now with `title_en`/`title_es`), and `legacy_markers`.
2. **Display strings** — everything visible and translatable, `kind: "display"` (en/es dual
   translaty spans, control/heading/option/summary text) or `kind: "attr"` (`data-aria-*`,
   `data-ph-*`, `aria-label`, `placeholder`, `title`). These are the "translate me" set;
   they're presentational and Safe. A tKey/`I18N.strings` dictionary is also rebuilt into
   `i18n_dict` (`key -> {en, es}`) and each `i18n-key` term is tied to its translation.

`--deep-json` emits just the display+i18n inventory (plus `machine_count` / `load_bearing` as
context) — the exact shape the **Deep-labels** view in `flove-vocaby.html` renders.
- **Can't (do these by hand):** map a *semantic key* (`stats.main_triads`) or a `tKey`
  namespace to its label when there's no dictionary to rebuild from; judge whether a
  `maybe_legacy` hit is truly dead; and catch nesting deeper than deck→items (e.g. RAY → its
  10 labels, slot→labeler). The scanner is the strong default; you supply the judgment.

The sections below are the patterns it keys on, plus the ones it leaves to you.

## The three naming layers

Every flove term tends to exist at up to three depths. The skill's job is to line them up.

| Layer | Examples | Where it lives |
|-------|----------|----------------|
| Machine name | `t1`, `x3`, `.labeler-formal`, `state.perStep`, `data-deck-id` | ids, classes, JS vars, data attrs |
| Semantic key | `stats.main_triads`, `wizard-choice-2-joy`, `rate-h` | i18n keys, namespaced lookups |
| Display label | "Main triads", "Philosophy", "Formal Hall" | inline text, i18n `.en/.es`, data objects |

A *mismatch* is when the machine/semantic layer still carries an older word than the display
layer (the canonical one). A *dead term* is a machine name with no live display label at all
(legacy/commented-out).

## Grep tells

Run these against the target file to surface candidates fast:

- **Selectors that key on a name (load-bearing):** `:checked`, `:has(`, `for="`, `id="`,
  `:target`, sibling combinators near state. A name caught here is **Nav-risk** by default.
- **Author-declared contracts (gold):**
  - `VOCABULARY` / `locked terms` — e.g. blogyadvanced.html ~lines 53–77 documents RAY /
    BOT / RATER with their exact class + input-name contracts.
  - `renamed from` / `Deferred class renames` / `legacy` / `deprecated` / `alias` — e.g.
    keys.html `// renamed from Main decks/Main Keys`. These name the *intended* target and
    the *old* word in one line.
  - `dead code` / `legacy` notes in comments or the user's memory (e.g. keys' péntadas
    `p1–p5` / "fivys" are flagged dead — favoritables are triads + extras only).
- **Data objects that hold the nesting:** `const DECKS`, `EXTRA_DECKS`, `EXTRA_PAIR`,
  `TREE`, `WANTS`, `vocab`, `SLOTS`, `LABELERS`. These are the structured vocabulary.
- **i18n tables:** `tKey('...')`, `titleI18n`, `itemsI18n`, `.en`/`.es` spans, `data-aria-*`,
  `data-ph-*`. When present, the canonical label is in the i18n entry, not the raw markup —
  resolve the label there before judging a mismatch.

## Nesting shapes you'll meet

Preserve these exactly — they are the meaning, and the export must round-trip them.

- **Deck → items** (keys.html): `{ id:'t1', title:'Philosophy', items:['Joy','Love','Wisdom'],
  titleI18n:{...}, itemsI18n:{...} }`. The id (`t1`) is machine; `title` is display.
- **Paired decks** (keys `EXTRA_PAIR`): a triad maps to an extra (`t1↔x2`, `t2↔x3`). The
  pairing is a relationship to keep, not a term to rename.
- **Parent → children** (profily `TREE`): `{ 'Like':['Favorite','Cheer',...], 'Wish':[...] }`
  — one level deep; parents and leaves are both display labels with no separate machine id.
- **Slot → labeler** (matrix-tier `vocab[app][slot][labeler]`): two levels — a slot row
  ("Tagline") with 8 tone columns (Default, Formal, Casual, Hotter, Lovely, Fatal, Lucky,
  Random). This is also the *destination* shape (see `matrix-tier-sync.md`).
- **CSS-variable contracts** (blogy RAY/RATER): an input id (`#labeler-formal`) drives a
  block of CSS vars and a display title ("Formal Hall"), logo, slogan. Renaming the id means
  moving the input, every `--labeler-*` var, the `.ray`/`.labeler-sub` classes, *and* the
  `:checked` selectors in lockstep — textbook Nav-risk.

## Building the inventory

For each term, record: a unique number, machine name(s), semantic key(s), display label,
nesting parent, the set of file locations (so the rename can be atomic), and a bucket
(Safe / Nav-risk / Standard-divergence). That record is what the numbered review form
renders, what the renames consume, and what the `vocaby-<app>.md` export serializes (one
item per row). One term, one number, all its sites — that traceability is what lets the
rename be atomic and the export be clean.

## Vocabulary-dense apps (good first targets)

- **keys.html** (`apps/puzzy/`) — highest density: 10 triad decks, 5 péntadas (dead), 5
  extras, paired map, `stats.*` timing keys, heavy i18n. The stress test.
- **blogyadvanced.html** (`apps/blogy/`) — RAY/BOT/RATER contracts, dual-span i18n.
- **profily.html** — the `TREE` parent→children hierarchy with seeded leaf examples.
