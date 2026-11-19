---
name: translaty
description: >-
  Make a single-file HTML app multilingual: per-language spans plus the 🌐
  worldball switcher. English is the base, Spanish the default target. Use for
  "translate this page", "add Spanish", or `/translatyN` for depth levels 1–N.
---

# translaty

Turn a single-file HTML app multilingual with a pure-CSS language switch. Two
parts: an **engine** (bundled in `assets/`, you inline it) and a **translation pass** (you
do it, string by string).

## Invoking it

`/translaty <lang>, <lang>, …` on a file — the comma-separated list is the target
set. Codes (`fr`, `pt-BR`) or names (`French`) are both accepted; normalise to a
BCP-47 code for `lang` and a span class. **English is the base** (exceptions:
three Spanish projects); no languages → **Spanish (`es`)**.

So `/translaty fr, pt` → `en` + `fr` + `pt`; `/translaty` alone → `en` + `es`.
If a language is genuinely ambiguous ("Chinese"), ask; otherwise proceed.

Translate **correctly**: idiomatic, locale-appropriate UI wording, right
plurals/diacritics/punctuation for each language — never word-for-word.

Label each option in the language's **own name**; the code is the
class/id/`lang`/`data-*` suffix. `en` English · `es` Español · `fr` Français ·
`de` Deutsch · `it` Italiano · `pt` Português · `nl` Nederlands · `ca` Català ·
`gl` Galego · `eu` Euskara. An unlisted code: ISO 639-1 + its autonym; a region uses
`pt-br` for the class and `lang="pt-BR"`.

## Depth

`/translatyN` runs levels 1–N of the shared
[Data Depth ladder](https://flove.org/development/index.html#levels) and stops;
languages follow the usual list. Default `/translaty` = 2 (surface + labels).

0. **Audit** — read-only coverage report and ledger; see [`audit.md`](audit.md).
1. **Surface** — visible copy.
2. **Labels** — add `<title>`, `description`, `aria-label`, `title`, `placeholder` and field labels.
3. **Names** — add i18n keys and internal names: translate their values, never the keys.
4. **Data** — add display values inside i18n tables, `flove-fields` and export envelopes; values only, never keys or enum values.
5. **Contracts** — routing, `flove-fields` and the export schema are never translated; audit and report.

**Stop rule.** `translatyN` translates only levels 1–N. At 1, metadata stays; at
2, i18n keys and names stay; at 3, data values stay; at 4, contracts stay; level
5 audits and never translates a contract.

## Procedure

1. **Settle the language set.** Parse the invocation: `en` is the base, the list
   is the targets, `es` the default. Normalise each to code + autonym.

2. **Install the engine** (once per app).
   - Inline `assets/engine.css` into the app's `<style>`; for each language beyond
     `es` append its 3-line toggle block (`.fr{display:none}` + the two
     `body:has(#lang-fr:checked) …` rules).
   - Add `assets/worldball.html` near the top — inside the header if there is one,
     else right after `<body>` — with one `<input>+<label>` per language (ids
     `lang-<code>`, first `checked`, input immediately followed by its label).
   - Inline `assets/engine.js` (new `<script>` before `</body>`, or merge into the
     existing IIFE). Prefer it as the *only* `curLang`/`applyLang` in the app.
   - **Already has a switcher or `.en/.es` engine?** Don't stack a second: keep the
     worldball and upgrade the engine to the generic multi-language form (see the
     standards note below).

3. **Translate the page** — wrap every user-facing string:
   - Visible text → `<span class="en" lang="en">…</span><span class="es" lang="es">…</span>`
     plus a span per extra language. Short, natural UI wording; you produce the
     translation, there is no external translator.
   - Attributes can't hold spans. For `placeholder`, `aria-label`, `title` and
     `<option>` text keep the element and add what the engine reads:
     `<option data-en="Friends" data-es="Amigos">Friends</option>`,
     `placeholder="search" data-ph-en="search" data-ph-es="buscar"`,
     `aria-label="Close" data-aria-en="Close" data-aria-es="Cerrar"`. Prefer
     `aria-label` over `title` — the engine toggles aria, not title.
   - `lang` on every span, so screen readers pronounce each language correctly.
   - **Escape to keep the markup valid**: in span text escape `&` `<` `>`; in
     attribute values also `"`. Accented UTF-8 needs no entity; `&`, quotes and
     `«» —` do.

4. **What to skip** — `<script>`/`<style>` contents, code/`<pre>`/`<kbd>` samples,
   URLs, numbers, brand/proper names, the language option labels themselves,
   `<title>` and `<meta>` (they can't hold spans; for a localized tab title add
   `data-title-en/es` to a sentinel and let `applyLang` set `document.title`).
   **Nav/menu labels that double as product names** are proper names: leave them
   unless the owner says otherwise, and flag the call so it's explicit.
   Already-wrapped strings stay alone — only **fill missing languages**. That
   idempotency is what makes re-running safe.

5. **Verify — valid HTML, CSS and JS is non-negotiable.** A translation that breaks
   the page is worse than none.
   - `node development/scripts/check.js <file>`: span balance and legal
     placement, `lang` attrs, unique ids, escaped `data-*`, CSS brace/comment
     balance, every inline `<script>` compiles. Fix and re-run until it prints OK.
   - If `html-validate`/`stylelint` are installed, run them too — they catch more.
   - Sanity-check behaviour: toggling the worldball flips every visible string (no
     language showing through), and options/placeholders/aria-labels change.
   - Let the owner view it in their browser; don't screenshot it yourself.

## Orchestration mode

Running as the **translaty stage of `/optimizy`**
(`https://flove.org/development/standards/skills/optimizy/SKILL.md`) — you are **last**, five stages
already landed. Trust the file; don't reopen their work.

- Assume it is simplified, renamed, validated and export-audited. Report anything
  out of scope instead of fixing it in passing.
- You still own the validity of your **own** changes: run the gate and check
  `grep -c 'Ã\|Â'` is 0 before finishing — nothing runs after you.
- The nav/menu proper-noun call goes to the orchestrator's batched survey.
- Return a compact ledger of what you wrapped and what's left.

## Notes

- **Big pages**: wrapping every string is the bulk of the work and is judgement.
  Go section by section; don't miss buttons, headings, small print, empty states,
  or strings inside JS template literals.
- **JS-built UI**: wrap generated text the same way and add `data-*` for generated
  options/placeholders/aria.
- **Coverage honesty**: a partial pass says what it did and what's left.

## Standards & extending

The family contract is
[`frontend.md` §13.2](https://flove.org/development/standards/frontend/frontend.md)
— the `flove:lang` key, `?lang=` precedence (URL > stored > `en`), and the pure-CSS
switch. Inline the three files in `assets/`; `engine.js` handles `applyLang`,
persistence and `<html lang>`.

An app already bilingual? Don't stack a second engine. Normalise its CSS to the
additive form (`.es,.fr{display:none}`, then per language
`body:has(#lang-X:checked)…`), switch the highlight to
`.lang input:checked + label`, and replace a hard-wired EN/ES `applyLang` with
the dataset form (`dataset[li]`, `'ph'+cap`, `'aria'+cap`).

Standing rules: `https://flove.org/development/standards/skills/standing.md`.
