---
name: texty
description: >-
  Polish a flove app's copy and align its internal names with what the UI shows,
  at five data-depth levels. Use for /texty, /texty1–/texty5, "fix the copy",
  "smooth the prose", "make the names match the labels".
category: sys
checker_of:
  - https://flove.org/development/standards/vocabulary.html
  - https://flove.org/development/standards/experience.md#onboarding-copy

---

# texty — copy and names at five depths

One skill for the text layer, from the words the reader sees to the names the code
keys on. Depth is a stop point: `/textyN` runs levels 1 → N and stops. Default
`/texty` = 1.

| Level | Name | Covers |
|---|---|---|
| 1 | **Surface** | headings, prose, buttons, hints, empty and error states |
| 2 | **Labels** | title, description, aria-label, title, placeholder, field labels |
| 3 | **Names** | classes, ids, JS identifiers, data and i18n keys |
| 4 | **Data** | display values in manifests and export envelopes |
| 5 | **Contracts** | routing, `flove-fields`, export schema (read-only) |

The shared ladder with examples:
`https://flove.org/development/index.html#levels`.

**Stop rule.** `textyN` edits only levels 1–N. At level 1, metadata, `aria-*`
and names are read-only; at 2, names are read-only; at 3, keys and contracts are
read-only. Never widen the edit because the form makes it easy.

## Levels 1–2 · copy

Polish the presentational layer — everything the reader sees as *copy*. The line:
a label is load-bearing, a paragraph is not. Rewording "Press here to continue" is
free; renaming the `id` a `for=` anchors to is level 3.

- **Level 1** — titles, prose, hints, tooltips, empty states, quotes, slogans,
  footer blurbs; button/link labels only when nothing looks them up by string.
- **Level 2** — add `<title>`, `description`, `aria-label`, `title`,
  `placeholder`, field labels and the values of `data-aria-*` / `data-ph-*`.

At both levels the machine names stay: classes, ids, `name=`, `data-*` keys,
i18n keys, `tKey(`. Their display values are level 2; their keys are level 3.

## Level 3 · names

Make the internal names agree with the words on screen, then sync the vocabulary
matrix. A name lives in HTML *and* CSS *and* JS: rename every site in one move,
or surface it for review.

1. **Profile the walls.** CSS-only navigation (`label … for=`, `:checked`,
   `:has(`, `:target`), `tKey(` / i18n tables, `querySelector` by string, a
   "VOCABULARY — locked terms" contract. Anything a selector keys on is a wall.
2. **Extract with the scanner.**
   `python tools/dev/extract_vocab.py <file> --out inv.json`
   (`--labeled`, `--deep-json`, `--no-display`). It returns the machine layer
   (classes/ids/names/data/i18n keys + `load_bearing` sites) and the display layer
   (visible text and `data-aria-*`/`placeholder`/`title`). A term can sit at
   machine, semantic-key and display depth; line them up. The scanner cannot judge
   `maybe_legacy` or nesting deeper than deck→items.
3. **Review by number.** Build `<app>-texty-review.html` with one numbered row per
   term: current name, proposed label, an Apply/Keep toggle. Never edit before the
   payload returns.
4. **Rename atomically and sync.** Apply the approved set everywhere, keep
   load-bearing selectors working, and mirror the result into
   `development/standards/vocabulary.html` — the matrix is this level's
   output.

## Level 4 · data values

Inside `flove-fields`, routing descriptions and tags, `flove-portrait` and i18n
tables, rewrite display values only. Keys, enum values and schema names are not
copy. No manifest change without approval.

## Level 5 · contracts

`routing.json`, `flove-fields` and the export schema are canonical and read-only.
At level 5, audit labels against them and report drift; hand structural changes to
`/jsony`.

## Workflow

1. **Profile the file.** Grep the coupling tells: `label … for=`, `type="radio"`,
   `:checked`, `:has(`, `:target`, `tKey(`, `data-*`, `querySelector` by string.
   Anything on that map is a wall — reword around it, or take it to level 3.
2. **Extract the strings** for the chosen depth; note what reads off (stiff,
   inconsistent, wrong voice, untranslated leftovers, legacy terms).
3. **Build the review form — then stop.** `<app>-texty-review.html`: one numbered
   row per item — current value, why it is off, an editable proposal, Apply/Keep
   and Copy. The payload starts `texty-review\t<app>\t<timestamp>`, then
   `<id>\tapply|keep\t<proposed>`. **Never edit before the payload returns**;
   apply only the `apply` rows, keep numbers stable, and surface coupled names to
   level 3.
4. **Apply and re-verify.** Apply marked rows only, in place; preserve markup,
   `lang=`, spans and untouched `data-*`. Check that nothing keys on a rewritten
   value.
5. **Report** what changed, what was surveyed, what stayed untouched and why.

## Fog around the line

- **Safe** — display-only copy, no coupling. Apply on approval.
- **Coupled** — looks like copy but something keys on it (i18n table, JS match,
  `for=`/`:checked` chain). Surface it; at level 3 rename the coupling too.
- **Voice call** — wording is fine, tone isn't. Apply once approved.

When unsure, treat it as Coupled. The survey protocol is shared:
`https://flove.org/development/standards/skills/standing.md` rule 3.

## Non-goals

Does not translate (`/translaty`), fix validity (`/validaty`), or commit. The only
file written before approval is the review form; the edited file and the report
complete the output.

Standing rules: `https://flove.org/development/standards/skills/standing.md`.
