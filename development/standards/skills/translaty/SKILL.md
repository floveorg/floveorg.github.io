---
name: translaty
description: >-
  Make a self-contained HTML app (a flove app or any single-file page)
  multilingual: translate its visible UI text into Spanish (and any other
  requested languages) by wrapping each string in per-language spans, and add a
  🌐 "worldball" language switcher that flips the whole page on click. Use this
  whenever the user asks to translate a page/app, make it bilingual or
  multilingual, add a language switcher / the worldball / a 🌐, add Spanish (or
  another language), or invokes /translaty — even phrasings like "make this
  work in Spanish too" or "add a globe to switch languages". Target languages
  are given as a comma-separated list when invoking (e.g. `/translaty fr, pt,
  de`); English is always the base and Spanish is the default if none are named.
  Translates inline (no external service) and is idempotent: re-running fills
  gaps rather than double-wrapping.
---

# translaty

Turn a single-file HTML app into a multilingual one with a pure-CSS language
switch. Two parts: an **engine** (bundled, you inline it) and a **translation
pass** (you do it, string by string, using your own translation).

## Invoking it

`/translaty <lang>, <lang>, …` on a file — the **comma-separated list** is the
set of target languages to translate that file into. Accept either codes (`fr`,
`pt-BR`) or names (`French`, `Portuguese`); normalise to a BCP-47 code for the
`lang` attribute and a span class. **English is always the base** (the page's
existing text = `en`). If no languages are given, default to **Spanish (`es`)**.

So `/translaty fr, pt` → produce `en` (existing) + `fr` + `pt`; `/translaty`
alone → `en` + `es`.

Translate **correctly**: idiomatic, locale-appropriate UI wording for each
language (not literal/word-for-word), respecting that the same source string may
differ by locale. Use the right plurals/diacritics/punctuation per language.

### Language code + native name (for the worldball option labels)

Label each option in the language's **own name** (autonym), and use the code for
the class / id / `lang` / `data-*` suffix:

| code | autonym (label) | code | autonym (label) |
|------|-----------------|------|-----------------|
| en   | English         | de   | Deutsch         |
| es   | Español         | it   | Italiano        |
| fr   | Français        | pt   | Português       |
| ca   | Català          | gl   | Galego          |
| eu   | Euskara         | nl   | Nederlands      |

For a code not in the table, use the standard ISO 639-1 code and its autonym.
Keep `data-*` suffixes lowercase-of-the-code (`data-fr`, `data-pt`); for a region
code like `pt-BR`, use a class-safe form (`pt-br`) and apply `lang="pt-BR"`.

## How the engine works

- Each translatable string becomes sibling spans, one per language, with a
  language class **and** a `lang` attribute:
  `<span class="en" lang="en">Save</span><span class="es" lang="es">Guardar</span>`
- CSS shows only the active language's spans; the worldball's radios drive it via
  `:has()`. No JS needed for the visible-text swap.
- Things CSS can't toggle (`<option>` text, `placeholder`, `aria-label`) carry
  their translations on `data-en` / `data-es` / `data-ph-en` / `data-aria-en` …
  attributes, and `engine.js`'s `applyLang()` applies them on switch. It also
  remembers the choice (localStorage) and syncs `<html lang>`.

### Family-wide default (§13.2 — pick once, applies everywhere)

The choice persists under **one shared, app-agnostic key — `flove:lang`** (NOT
a per-app key), so a language picked in any flove app is the default across the
whole family. `engine.js` already does this:

- Writes only `flove:lang`; **reads** `flove:lang` then the legacy
  `translaty-lang` (migration — apps that still hold the old key keep working).
- Honors a **`?lang=<code>` URL handoff** so the default carries between apps on
  `file://` too (where per-file storage is isolated). **Precedence: URL param >
  stored `flove:lang` > `en`.**
- When you translate an app, ensure these are present (they are, if you inlined
  the current `engine.js`). If the app had a hand-rolled engine on the old key,
  migrate it to `flove:lang` + the `?lang=` read rather than stacking a second.

The **entrance picker** itself (a first-run "Choose your language 🌐" step) is a
**launcher / §13.6 onboarding** concern, not this skill's per-file job — but it
writes the same `flove:lang`, and every app you translate must honor it on load
(via the read above). Inter-app links should pass `?lang=` so the default
survives `file://` navigation.

## Bundled files (`assets/`)

- `engine.css` — the i18n toggle + the worldball styling (light + dark). Inline it.
- `worldball.html` — the `<details>` 🌐 switcher markup. Place near the top.
- `engine.js` — `applyLang` + persistence + `<html lang>` sync + auto-close. Inline it.
- `scripts/check.js` — the validity gate (`node scripts/check.js <file>`); run it
  before finishing. HTML/CSS/JS sanity for the hazards this skill can introduce.

Inline these (don't link them as external files) — flove apps are self-contained.

## Orchestration mode — when /optimizy is driving

If your invocation says you're running as the **translaty stage of `/optimizy`** (the
orchestrator tells you so), you are the **last** stage — five stages of polish already
landed, so trust the file and translate it; don't reopen their work:

- **Assume the app is already simplified, renamed, validated and export-audited.** Don't fix
  unrelated validity, naming or logic you notice in passing — that's earlier stages' ground,
  and editing it now risks undoing a settled decision. *Report* anything out of scope to the
  orchestrator instead of touching it.
- **You still own the validity of your *own* changes.** Run the bundled gate
  (`node scripts/check.js <file>`) and the encoding check (`grep -c 'Ã\|Â'` must be 0) before
  finishing — nothing runs after you to catch a broken span.
- **The nav/menu "proper-noun" call** (tier lists, app-name menus you'd normally leave
  untranslated and flag) → surface it to the orchestrator's batched survey rather than
  deciding silently.
- **Don't write a final report or commit** — return a compact ledger of what you wrapped and
  what's left; the orchestrator writes the one report and follows the commit workflow.

Everything else below still applies in full — you're doing *less overlap*, not less care.

## Procedure

1. **Settle the language set.** Parse the comma-separated languages from the
   invocation (see "Invoking it"): `en` is always the base, those are the
   targets, `es` is the default if none given. Normalise each to a code + autonym
   from the table. If a requested language is genuinely ambiguous (e.g. just
   "Chinese" — simplified vs traditional), ask; otherwise proceed.

2. **Install the engine** (once per app):
   - Inline `engine.css` into the app's main `<style>`. For each language beyond
     es, append its 3-line toggle block (the comment in the file shows the
     shape) — e.g. for `fr`: `.fr{display:none}` + the two
     `body:has(#lang-fr:checked) …` rules.
   - Add the `worldball.html` markup near the top — inside the header if there is
     one, otherwise right after `<body>`. Add one `<input>+<label>` option per
     language (ids `lang-<code>`, first one `checked`, each input immediately
     followed by its label).
   - Inline `engine.js`. If the page has **no script**, add a brand-new
     `<script>` before `</body>`; if it has its own IIFE you may merge the body
     in. Prefer making this generic engine the *only* `curLang`/`applyLang` in
     the app.
   - **If the app already has a language switcher or `.en/.es` engine** — even a
     hand-rolled, EN/ES-hardcoded one — don't stack a second. Keep the worldball
     and upgrade the engine to the generic multi-language form (see "Extending an
     already-multilingual app" below).

3. **Translate the page** — wrap every user-facing string:
   - Visible text → `<span class="en" lang="en">…</span><span class="es" lang="es">…</span>`
     (plus a span per extra language). Translate faithfully and idiomatically for
     UI — short, natural, not literal. You produce the translation; there is no
     external translator.
   - Attributes can't hold spans. For translatable `placeholder`, `aria-label`,
     `title`, and `<option>` text, keep the element and add data attributes the
     engine reads: `<option data-en="Friends" data-es="Amigos">Friends</option>`,
     `placeholder="search" data-ph-en="search" data-ph-es="buscar"`,
     `aria-label="Close" data-aria-en="Close" data-aria-es="Cerrar"`. Prefer
     `aria-label` over `title` for tooltips that need translating (the engine
     toggles aria, not title).
   - Add the `lang` attribute to every span (so screen readers pronounce each
     language correctly).
   - **Escape to keep the markup valid:** in span text escape `&` `<` `>`; in
     `data-*` and other attribute values escape `&` `<` `"`. Translated strings
     often carry `&`, quotes, or `«» —` — accented letters are fine as UTF-8, but
     these specials must be entities or they break the element. The validity gate
     (step 5) will catch misses, but get them right as you write.

4. **What to skip** — don't wrap or translate: `<script>`/`<style>` contents,
   code/`<pre>`/`<kbd>` samples, URLs, numbers, brand/proper names, and the
   language option labels themselves (`English`, `Español` are names — leave
   them). Also skip `<title>` and `<meta>` content — they can't hold spans and
   the engine doesn't toggle them (if the user wants the tab title localized,
   add `data-title-en/es` to a sentinel and have `applyLang` set
   `document.title`). For **nav/menu labels that double as product names** (a
   tier list like Mini/Basic/Normal/Advanced, an app-name menu), treat them as
   proper names and leave them unless the user says otherwise — flag the call so
   it's explicit, not silent. Leave already-wrapped strings alone; only **fill
   missing languages** (e.g. add `.fr` spans to an app that already has
   `.en/.es`). That idempotency is what makes re-running safe.

5. **Verify — valid HTML, CSS and JS is non-negotiable.** The output must always
   parse cleanly; a translation that breaks the page is worse than no translation.
   - Run the bundled gate: `node scripts/check.js <file>` (from the skill dir).
     It checks span balance & legal placement, `lang` attrs, unique ids, escaped
     `data-*`, CSS brace/comment balance, and compiles every inline `<script>`.
     Fix everything it flags, then re-run until it prints OK.
   - If `html-validate` / `stylelint` are installed, run them too — they catch
     more than the gate. (None? the gate is the floor, not the ceiling.)
   - Then sanity-check behaviour: toggling the worldball flips every visible
     string (no language showing through another), and `<option>`s / placeholders
     / aria-labels change on switch.
   - Let the user view it in their browser (don't screenshot it yourself).

## Extending an already-multilingual app

Adding a language to an app that's already bilingual is mostly *not* a markup
job — most flove apps bake the two languages into their **JS**, and that's where
the work is. Before editing, scan for these and generalize them to a language
list rather than a hard-wired pair:

- **CSS pattern.** A hand-rolled engine often uses `body:not(:has(#lang-es:checked))
  .es{display:none}`. Normalise to the additive form so a 3rd+ language slots in
  cleanly: `.es,.fr{display:none}` as the default, then per non-default language
  `body:has(#lang-X:checked) .en{display:none}` + `…{.X{display:inline}}`. Also
  switch any `#lang-X:checked ~ label` highlight to the generic
  `.lang input:checked + label`, and make sure `.lang-opts` has `flex-wrap:wrap`
  once there are more than two options.
- **`curLang`/`applyLang`.** If the app ships its own EN/ES-hardcoded copy
  (`curLang` only checks `#lang-es`; placeholder/aria via `li==='es' ? … : …`),
  replace it with the bundled `engine.js` form (`dataset[li]`, `'ph'+cap(li)`,
  `'aria'+cap(li)`) so no further language ever needs a JS edit.
- **Bilingual helpers & data.** Look for `(en, es)` helper signatures
  (`bx(en,es)`, `T(en,es)`), `[en, es]` data tuples (decks, pools, word lists),
  and binary "show the other language" logic (a `vis()` that removes the single
  non-active span). These must each become list-aware: `bx(...langs)`,
  `[en, es, fr]`, and "remove every non-active language". This is usually the
  bulk of the diff.
- **Generated markup.** Anything the JS builds (rows, options, toasts, export
  labels) must emit the new language's span / `data-*` too — translating only the
  static HTML leaves the dynamic UI half-translated.

**Extend self-check** (no browser): every `.es` has a sibling `.<newlang>`; every
`data-es` / `data-ph-es` / `data-aria-es` has a matching `*-<newlang>`; one
worldball with the new option; `curLang`/`applyLang` are list-generic; tags
balanced.

## Notes & limits

- **Big pages**: wrapping every string is the bulk of the work and is done by
  hand (your judgment). Go section by section; don't miss buttons, headings,
  small print, empty-state messages, and dynamically-generated strings inside
  the app's JS template literals (those need spans too).
- **JS-built UI**: if the app generates markup in JS (e.g. a `bx(en,es)` helper),
  translate there as well — wrap generated text the same way and add `data-*`
  for generated options/placeholders/aria.
- **Coverage honesty**: if you translate only part of a large app in one pass,
  say what you did and what's left rather than implying it's fully done.
