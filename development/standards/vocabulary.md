# flove · Canonical vocabulary — §13.7

Part of the flove standards catalogue. Index: [`README.md`](README.md) · contract:
[`contract.md`](contract.md) · catalogue: [`frontend/frontend.md`](frontend/frontend.md) ·
interactive matrix: [`vocabulary.html`](vocabulary.html).

---

## 13.7 · Canonical vocabulary (CSS classes & semantic concepts)

blogy is the **reference implementation** for the project's CSS class
vocabulary (Solo distro — local-first fallback reference; the **Central** apps are
the canonical spec, see [`apps/README.md`](apps/README.md)). The names
below are the canonical prefixes/families; other
apps should reuse them rather than invent synonyms. When a blogy file
and another app disagree on a name for the same concept, blogy wins
and the other app is migrated via §13.7.

Each row gives the prefix, what it means semantically, and the most
common derived names. Specific variants are documented in blogy's own
CSS (`apps/blogy/blogy-advanced-one.html` is the most vocabulary-rich file
— the self-contained variant — grep there first when unsure how a
prefix is used; the canonical modular `index.html` uses the same
vocabulary but is leaner).

**App frame (corporate chrome — shared across all apps):**

| Prefix | Concept | Common variants |
|--------|---------|-----------------|
| `flove-bar` | Sticky top strip: back link + mark + app name | `--auto`, `--dark` |
| `flove-mark`, `flove-sprout` | Brand glyph — the flove sprout (was the 8-point asterism) | `--still` (no spin) |
| `flove-home` | Back-to-launcher link inside the bar | — |
| `flove-app-name` | App's name shown inside the bar | — |
| `flove-card`, `flove-pill`, `flove-btn` | Family components (rounded card / pill button / family button) | — |
| `flove-toast` | Transient feedback toast | `--io` (F0 toasts) |
| `flove-footer-badge` | Floating "all apps" pill bottom-right | — |
| `flove-action-bar`, `flove-action-btn` | Legacy 4-button F0 row (older apps; new apps use the 6-button shell from §10.6) | — |

**Content units (what the user creates / manipulates):**

| Prefix | Concept | Common variants |
|--------|---------|-----------------|
| `entry-*` | The user's input unit (replaces older `love-*`, `add-*`) | `entry-field`, `entry-textarea`, `entry-row`, `entry-col`, `entry-tools`, `entry-tool`, `entry-magic`, `entry-list`, `entry-more`, `entry-del`, `entry-save` |
| `labeler-*` | A panel / perspective in the stepper — labels the user's entries from one viewpoint, will inject personalized labels via the affinity network in F3+ (was `ray-*`; before that `perspective-*`) | `labeler`, `labeler-sub`, `labeler-reset`; CSS vars `--labeler-panel-N-title`, `--labeler-panel-N-intro` |
| `wizard-*` | A content-injection wizard — suggests/injects phrases into an entry; will personalize via the affinity network in F3+ (was `bot-*`; before that `bot-choice-*`) | `wizard-arm`, `wizard-arms`, `wizard-arm-stack`, `wizard-arm--more`, `wizard-row`; the three canonical wizards are `lovely`, `joy`, `wisdom` |
| `wizardry-*` | Wizard-configuration grid (used inside `newwizard` form; was `boty-*`) | `wizardry-cell`, `wizardry-cell-icon`, `wizardry-cell-info`, `wizardry-cell-name`, `wizardry-grid` |
| `step-*` | Navigation between panels (stepper); name preserved — earlier rename to `.path-*` was retracted, do not re-attempt | `step-node` |
| `rate-*` | Rating cells inside a rater | `rate-step` |
| `rater-*` | Rater UI surround | `rater-emoji-trigger`, `rater-chip`, `rater-prep`, `rater-compact`, `rater-emos` |
| `phrase-*` | The live legible phrase block | `phrase--magic`, `phrase-heart`, `phrase-text`, `phrase-emos`, `phrase-note-lbl` |
| `clause-*` | A single clause inside the phrase | `clause-code` |

**Entry-field modifiers — 5 canonical field types (`entry-field--*`):**

The first four modifiers (`--main`, `--alternative`, `--extra`,
`--sibling`) are mutually exclusive — a given `entry-field` is exactly
one of them. `--note` is **orthogonal**: it can attach to any of the
four (a note is an annexed mini side-field, not a type of its own
axis).

| Modifier | Concept | Axis | Status in blogy |
|----------|---------|------|-----------------|
| `--main` | Primary field, top-level (one per slot) | type | ✓ |
| `--alternative` | Nested secondary alternative under main; same or a bit less featured | type | ✓ (was `--extra` until 2026-05-23) |
| `--extra` | Nested field inside an extra field-row (when the row also acts as parent of a field) | type | ✓ (was `--dup` until 2026-05-23) |
| `--sibling` | New same-thing item NOT nested; peer of main (the "add another" pattern, e.g. another Who at the same level) | type | reserved (no markup yet; declared in wizard generator GROUPS for forward compat) |
| `--note` | Mini side-note appended to a field or group — applies to any of the four above | orthogonal | ✓ (was `--mini` until 2026-05-23) |

**Important:** `entry-row--extra` is a *different axis* — an additional
textarea ROW within a field (added by `.entry-more`). The same word
`extra` appears at both axes after the swap (`entry-row--extra` AND
`entry-field--extra`), which is intentional: an extra-row can host a
nested `entry-field--extra`, so the words match the relationship.

**Topbar chrome (navigation / affordances at top):**

The topbar is the densest piece of standardised UI. Organised in four
zones: **Brand**, **Buttons**, **Menu** (the dropdown shell), and
**Menu sections** (the row types that live inside the menu). Each
button's *popover content* is documented in its feature section
(§13.1, §13.4, etc.) — this table only catalogues the topbar surface.

The topbar container itself uses three classes: `topbar` (the
`<header>`), `topbar-inner` (flex inner row), `topbar-spacer` (pushes
right-side controls). Everything below sits inside `.topbar-inner`.

### Brand — identity zone (logo + title)

| Class | Role |
|-------|------|
| `mark` | The brand glyph itself (`<span aria-hidden="true">`) |
| `mark-link` | The `<a>` that wraps the mark — `href` points to the page itself so clicking reloads |
| `title-h1` | The `<h1>` element holding the app name |
| `title-label` | The clickable `<label>` inside `title-h1` (`for="intro-open"`) — clicking opens the about/intro overlay (§13.6). Renamed from `title-btn` 2026-05-23 because it's a `<label>`, not a `<button>` |

> *Lang switcher (lang-\*) is documented under Menu sections (default)
> and Buttons (alternative).*

> **Mark propagation (2026-07-18).** An app's mark is drawn in its
> `addons/media/apps/logos/<app>/<app>-logos.html` showcase (the master — see the
> logos-folder rule below), but because a mark is **inlined per file** — no
> cross-document `<use>` on `file://`, contract.md · The person owns it — the same mark lives as
> a *copy* everywhere it is shown. When an app's mark is added or changed,
> propagate the updated inline SVG to **every** place that badges the app:
> 1. the app's own builds — every build/variant that shows a `flove-bar`;
> 2. **`apps/index.html`** — the demos-index cube for that app;
> 3. the app's **parent launcher-folder `index.html`** (the folder index that launches it);
> 4. the **appy files** — the profile builds (`miniappy` / `basicappy`,
>    §11.4) and any appy listing that badges the app.
> 5. the **Related Apps badges** — every *sibling* app whose menu lists this
>    app in its Related Apps section (§13.5) inlines this app's mark; update
>    that copy too.
> Targets 2–3 were the established pair; **appy (4) and Related-Apps badges (5)
> are now required too.**
> An app's mark must match across its own files, the demos index, the
> launcher-folder index, appy, *and* every Related-Apps badge that shows it —
> a mark change that lands in only some of these is a bug. (There is **no**
> central `flove-logos.svg`; the per-app `<app>-logos.html` is the master
> drawing.)

> **App image assets — the logos folder (2026-07-18).** App image assets
> live under **`addons/media/apps/`** (beside `addons/media/apps/captions/`, the demos-
> index screenshots). Each app's visual identity is its own folder,
> **`addons/media/apps/logos/<app>/`** — one showcase file plus category
> subfolders:
>
> ```
> addons/media/apps/logos/<app>/
>   <app>-logos.html   · the showcase — master drawing of the mark
>   imagotipo/         · ADVANCED logo: figurative / mascot / character
>                        (nety = katana · keys = pandas)
>   icons/             · nav / UI icons
>   banners/           · banner / hero imagery
> ```
>
> - **Logos come in kinds along a ladder:** the base **isotipo** (the
>   abstract glyph shown in the `flove-bar`) → **imagotipo** (the advanced,
>   figurative kind). imagotipo is *a kind of logo*, so it lives **inside**
>   the logos folder — not a separate top-level category. The ladder may
>   extend if richer kinds appear.
> - **`icons/` and `banners/` are categories inside the same logos folder**
>   (not top-level) — so an app's entire visual identity sits in one place.
> - The shipped **favicon** (`favicon.svg`, or `favicon-<sub>.svg` for a
>   cluster) stays **beside the app file** so `<link rel="icon">` resolves
>   by relative path.
> - **Showcase naming:** `<app>-logos.html` is canonical; the older
>   `logos.html` / `logos-<app>.html` / `<app>-brand.html` names are
>   superseded (fold the duplicate `apps/…/logos.html` copies in here).
> - **Master drawing:** the per-app `<app>-logos.html` is the source of
>   truth for the mark; every inlined copy (flove-bar, `apps/index` cube,
>   launcher index, appy) derives from it — see *Mark propagation* above.
> - Shared flove-level assets (the PWA icons) live under
>   **`addons/media/apps/logos/flove/icons/`** — flove's own app entry.

### Buttons — topbar trigger buttons (each opens content documented elsewhere)

Every button below carries a **shared `topbar-btn` class** in addition
to its feature-specific class. The shared class lets apps style the
button surface uniformly (size, hit area, focus ring) without
re-declaring per feature. Markup:

```html
<label class="compass-btn topbar-btn"  for="compass-open"  …></label>
<label class="magic-btn   topbar-btn"  for="magic-open"    …></label>
<label class="tier-pop-btn topbar-btn" for="tier-pop-open" …></label>
<label class="menu-btn    topbar-btn menu-btn--open"  for="d-menu" …></label>
<label class="app-toggle-btn topbar-btn" for="all-pressed" …></label>
```

The feature-specific class carries the *behavior* (which popover it
opens, which icon, which colour). The `topbar-btn` class carries the
*topbar membership* (the button surface). Both coexist.

Each button below is a `<label>` or `<button>` inside `.topbar-inner`.
The popover/menu it opens is documented in the linked section.

| Class (plus `topbar-btn`) | Triggers | Spec |
|---------------------------|----------|------|
| `compass-btn` (inside `.compass-wrap`) | Display-mode switcher popover (`compass-spark` is the click-burst FX) | §13.4 |
| `magic-btn`, `magic-btn-summary` (inside `.magic-wrap`) | Magic-mode topbar variant + the magic-rays popover | §10.6.3 |
| `tier-pop-btn` (inside `.tier-pop`) | Tier switcher (`tier-pop-rays`, `tier-pop-step`, `tier-pop-step--current`, `tier-pop-node`, `tier-pop-label`) — **demo sketches only** (tiers are not in this trunk) | §13.1 |
| `views-popup` (inside `.views-wrap`) | Layout-view picker popover | (no dedicated section yet) |
| `app-toggle-btn` | "All apps" exit (`for="all-pressed"` checkbox elsewhere) | — |
| `menu-btn`, `menu-btn--open`, `menu-btn--close` | **Legacy** ☰ toggle for the dropdown — **superseded by §13.7.13**: the menu now opens on **logo/title click** (`for="d-menu"`), and this button's slot became the ⚙ `settings-btn` (topbar collapse) | see *Menu* below |
| `lang-flag` (with `topbar-btn`) *(alternative placement)* | Language switcher — when an app surfaces it as an always-visible topbar button instead of the default menu-section placement. Markup: `<label class="lang-flag topbar-btn" for="…">…</label>` | see *Language section* under Menu sections |

### Menu — right-side dropdown shell

The menu opens on **click of the logo (`mark-link`) or title
(`title-label`)** — both `for="d-menu"` (§13.7.13; legacy builds used a
☰ `menu-btn`) — and presents a `<ul>` of rows. The
shell itself owns these classes:

| Class | Role |
|-------|------|
| `menu-list` | The `<ul>` container of items |
| `menu-divider` | A separator row (`role="separator"`) |
| `menu-plus` | The "more" affordance inside a row (toggles via `#menu-plus-open`) |
| `menu-search-row` | The search input row at the top of the menu |

### Menu sections — row types that live inside `menu-list`

Grouped by **purpose**, not by component type. Four semantic buckets
(Search · Main · Related · Core) plus a Structure block for the
orthogonal helpers (`menu-divider`, `menu-plus`).

**Bucket semantics:**

- **Search** — find stuff inside this app.
- **Main** — everything *this* app exposes: its internal sub-views and
  sub-sections AND its system settings (Mode, Sound, sound depth,
  language). The app-specific layer.
- **Related** — links to *sister apps* in the flove family (loves,
  daty, wanty, socy, etc.). Cross-links between apps within the
  family.
- **Core** — links to *flove ecosystem* sections (home `flove.org`,
  help, community, blog, the design system). Cross-cuts the whole
  family; nothing to do with the app that's displaying the menu.

A given menu may include all four buckets, in this order. Only
**Main** is mandatory (every app surfaces something about itself);
Search/Related/Core appear when the app has them.

#### Search

| Class | Role |
|-------|------|
| `menu-search-row` | Fixed-top search input row (often with a `menu-plus` to add what's being searched) |

#### Main

The biggest bucket. Includes this app's internal navigation, app-specific
quick actions, and system settings the user can toggle from any flove
app (Mode, Sound, sound depth, language).

*Quick app actions:*

| Class | Role |
|-------|------|
| `menu-minrow` | Horizontal row of small action buttons (1·2·3·4) |
| `menu-minbtn` | A single quick-action button |

*Internal sub-views (collapsibles):*

| Class | Role |
|-------|------|
| `menu-section-title` | Section header inside the menu |
| `menu-section-toggle` | The disclosure trigger for a section |
| `menu-section-plus` | "Add" affordance inside a section |

*Settings (`menu-switch-*` family):*

| Class | Role |
|-------|------|
| `menu-switch` | Container row for a setting (modifiers below) |
| `menu-switch--mode` | Modifier: a binary mode toggle (e.g. local/public) |
| `menu-switch--split` | Modifier: split row where the name links elsewhere AND a toggle sits on the right |
| `menu-switch-label`, `menu-switch-label--track-only` | The `<label>` wrapper (full or track-only) |
| `menu-switch-icon` | The leading icon (`mi`-class glyph) |
| `menu-switch-name`, `menu-switch-name-link` | The setting name; `-link` variant when the name is a link |
| `menu-switch-state` | Wrapper for the current-state visual |
| `menu-switch-left`, `menu-switch-right` | The two side labels of a binary toggle |
| `menu-switch-track`, `menu-switch-thumb` | The slider track + the moving thumb |
| `menu-switch-caret`, `menu-switch-current` | Caret + the current-value indicator (for non-binary states) |

*Sound depth (`menu-nav-*` — deprecated 2026-05-23, kept only as CSS):*

| Class | Role |
|-------|------|
| `menu-nav-bar` | Container row of sound-depth steps |
| `menu-nav-row` | A horizontal sub-row inside the bar |
| `menu-nav-step` | One sound-depth step (off/mini/normal/full) |
| `menu-nav-node` | The visual node (circle) of a step |
| `menu-nav-label` | The text label of a step |

> **Deprecated as menu items** — Marc removed the `menu-nav-bar` block
> from blogybasic / blogynormal / blogynormal-one on 2026-05-23 because
> it visually duplicated the topbar's complexity bar (§13.1). The
> orphaned `sound-level` radio inputs (`#sound-mini`, `#sound-basic`,
> `#sound-normal`, `#sound-advanced`, `#sound-super`) remain at the
> top of each file as dead state; CSS rules referencing them still
> exist but no markup toggles them.
> Sound-depth control is pending a new design — until then, the sound
> engine defaults to the `#sound-mini:checked` state.
> <!-- ↗ pendings:#T06 -->
> Tier navigation lived in the topbar tier-pop (§13.1) — demo sketches only;
> tiers are not part of this trunk.

*Language (`lang-*` — default location):*

| Class | Role |
|-------|------|
| `lang-others` | The `<ul role="menu">` listing alternative languages (visible when `#d-menu:checked` AND `#opt-lang:checked`) |
| `lang-others-more` | The "+ add a language" row inside the list (opens `blogy-newlanguage.html` via `for="new-language-modal"`) |
| `lang-flag` | The flag glyph inside any language row (also reused inside `lang-others-more` for the `＋` mark) |

**Lang placement contract.** The language switcher has two valid
placements: **default — menu section** (here, inside Main) OR
**alternative — topbar button** (Buttons zone, carrying `topbar-btn`).
Apps adopting flove standards should default to the menu placement
unless always-on visibility matters more than menu compactness.

#### Related

Links to *sister apps* in the flove family (the apps that share the
launcher: loves, daty, wanty, socy, etc.). When a user is in app
A and wants to jump to app B, that link lives here.

| Class | Role |
|-------|------|
| (no canonical class yet) | blogy's menu does not currently include sister-app links. Reserved for apps that need cross-app navigation from inside their menu. Recommendation: introduce a `menu-related-*` family (e.g. `menu-related-item`, `menu-related-link`) when first needed; mirror the `menu-design-*` shape. |

#### Core

Links to *flove ecosystem* sections — home (`flove.org`), help,
community, blog, the design system. Cross-cuts the whole family;
nothing app-specific.

| Class | Role |
|-------|------|
| `menu-design-item` | A row that links into the design system |
| `menu-design-link` | The actual `<a>` inside such a row |
| (more `menu-core-*` classes to be added when home/help/community/blog rows land in app menus) | reserved |

#### Structure — orthogonal helpers (cross-cutting)

Classes that don't belong to any single bucket — they appear anywhere
in the menu where the structural role calls for them.

| Class | Role |
|-------|------|
| `menu-divider` | Separator row (`role="separator"`) — visually splits buckets or sub-groups |
| `menu-plus` | "More" affordance — appears inside Search (add what's being searched), inside Main sub-sections (add a new sub-view), and anywhere a "+" inline trigger is needed |

### Topbar form-element ID conventions

| Pattern | Use |
|---------|-----|
| `#<feature>-open` (checkbox + `.ctl`) | Toggles a feature panel via `body:has(#<feature>-open:checked) …`. Examples: `#compass-open`, `#tier-pop-open`, `#magic-open`, `#intro-open`, `#menu-plus-open`. |
| `name="topbar-labeler"` (radio group) | Topbar-level labeler selector — all radios share this name; their IDs are `topbar-labeler-none` or `labeler-<id>`. (Was `topbar-ray` until 2026-05-23 rename.) |
| `for="all-pressed"` | The app-toggle uses an `#all-pressed` checkbox elsewhere on the page. |
| `for="intro-open"` | The title button + the menu's "about" both target the intro overlay. |

**Modal forms (sibling iframes — §13.3):**

| Prefix | Concept |
|--------|---------|
| `newlabeler-*` | New-labeler form modal (each has `-modal`, `-backdrop`, `-frame`, `-close`; was `newray-*`) |
| `newwizard-*` | New-wizard form modal (same suffixes; was `newbot-*`) |
| `newlanguage-*` | New-language form modal (same suffixes) |
| `newsound-*` | New-sound form modal (same suffixes) |

**Onboarding (§13.6):**

| Prefix | Concept | Common variants |
|--------|---------|-----------------|
| `intro-*` | First-use onboarding overlay | `intro-close`, `intro-lead`, `intro-section` |

**i18n + utility (§13.2):**

| Class/ID | Concept |
|----------|---------|
| `.t-en`, `.t-es` | Bilingual string siblings (only one shown at a time, driven by `#ui-lang-es:checked`) |
| `#ui-lang-en`, `#ui-lang-es` | Language switch radios |
| `.ctl` | Utility class on `<input type=checkbox\|radio>` that drives `:has()` from elsewhere in the document (the input itself is visually hidden) |
| `#disp-*` | Display-mode radio IDs (`disp-default`, `disp-random`, …) — see §13.4 |
| `#compass-open`, `#tier-pop-open`, `#new-X-modal` | Standard pattern: `#<feature>-open` checkbox toggled by a `<label>`, layout reacts via `body:has(#<feature>-open:checked) …` |

**Rules:**

1. **Same concept → same prefix.** If an app has the user's input
   unit, it's `entry-*` not `input-*` or `field-*`. The semantics are
   owned by the prefix.
2. **App-specific specialization uses BEM modifiers.** Don't invent a
   new prefix; extend with `--<variant>` (e.g. `wizard-arm--more`,
   `phrase--magic`).
3. **Adding a new family.** If your app introduces a concept that no
   §13.7 prefix covers, propose the new prefix here in the same turn
   — don't ship a one-off name that other apps will then duplicate
   with a different spelling.
4. **Migrating an existing app to canonical names** follows the
   §13.7 deferred-renames doc-comment pattern. Lessons from blogy:
   `bot-choice-* → bot-{lovely,joy,wisdom}` ✓, `love-* → entry-*` ✓,
   `perspective-* → ray-*` ✓, `step-* → path-*` retracted (do not
   redo).
   **The 2026-05 migration is complete:** `ray-*` → `labeler-*` and
   `bot-*` → `wizard-*` (modals, sound keys and the JS API included). The old
   prefixes are retired; the canonical names are the ones above.

   See [[project-blogy-vocabulary-renames]] for the full log including
   backup paths and verification counts.
5. **Older apps may keep the legacy 4-button `flove-action-bar`.**
   New apps adopt the v0.3 shell from §10. Don't mass-rewrite
   legacy unless asked.

#### 13.7.13 · Topbar collapse + menu via logo/title

Adopted 2026-05-28 in `apps/blogy/blogy-advanced-one.html`,
`apps/blogy/index.html`, `apps/blogy/blogy-basic-css.html`. Three
small but cumulative changes to the topbar surface (§13.7 Brand
/ Buttons / Menu rows):

- **`topbar-collapsed` checkbox + `.settings-btn`** — the ☰
  `menu-btn` is replaced by a ⚙ `settings-btn` that toggles
  `#topbar-collapsed`. While checked, every direct child of
  `.topbar-inner` except the brand (`mark-link`, `title-label`),
  the spacer and the settings button itself collapses to
  `display:none` (compass-wrap, app-toggle-btn, magic-wrap,
  tier-pop, labeler-slogan). Pure CSS, one `body:has()` rule per
  hidden child. The settings-btn re-uses the `.menu-btn` size /
  shape rules; same `topbar-btn` shared class.
- **Logo (`mark-link`) and title (`title-label`) both open the
  dropdown menu.** Both `for="d-menu"` (was: `mark-link` =
  reload link, `title-label` = `for="intro-open"`). The
  `mark-link` becomes a `<label>` instead of an `<a>` so the
  click semantics are uniform. Hover styles untouched (both
  `<a>` and `<label>` take them).
- **Certify switch in the menu** — a new `menu-switch--split`
  row sits immediately below the Sound switch, with icon `🛡`
  and bilingual name *Certify / Certificar*. Linked checkbox
  is `opt-certify`; states are *No / Sí* (vs Sound's *Off / On*).
  When `#opt-certify:checked`, a `.menu-certify-row` `<li>`
  reveals a `.cert-track` of five `.cert-node` buttons
  (`data-cert`: `trusts · mail · telf · id · bio`) on a
  `.cert-fill` progress bar, and a `.cert-intro` panel below.
  Clicking a node grows the fill to that node and swaps the
  intro copy (per-node bilingual paragraph describing how that
  proof works: vouching ring · email code · phone SMS · official
  ID · liveness bio). The reveal of the row is CSS-only (mirrors
  `body:has(#opt-sound:checked) .menu-sound-row`); the per-node
  intro swap is the one place that requires JS (a small inline
  script with a `CERT_INFO` map, reused verbatim from
  `apps/souls.html`). `blogy-basic-css.html` keeps its "100% CSS,
  no scripts" contract: the row reveals and the 5 nodes are
  visible, but the intro panel stays inert there.

**Trigger keywords** (harvest into other apps when Marc says
any of these): "settings icon collapses topbar", "logo/title
open menu", "Certify switch", "Trusts Mail Telf Id Bio",
"certify progress track", "cert-track / cert-node / cert-intro".

#### Deferred-renames doc-comment pattern (nested)

When consolidating a file's vocabulary toward §13.7 canonical names
(renaming classes, IDs, CSS variables), capture the plan in a doc
comment at the top of the file under a heading **"Deferred class
renames"** — one bullet per pending rename, with status marker
(✓ done · ✗ retracted · pending).

**Why:** mass renames "can cause conflicts" (a target name may already
exist; a CSS property may share the rename root). The doc-comment is
the plan that survives between sessions; without it, the next
consolidation turn proposes new names instead of finishing the agreed
list.

**Conflict-avoidance protocol before any rename:**
- `grep -oE` the target tokens to find pre-existing collisions.
- Note CSS properties that share the rename root (e.g. the CSS
  `perspective:` property vs `perspective-*` class names — sed on the
  bare word will break the property).
- Backup to `/tmp` before running mass sed.

The canonical destination vocabulary is the rest of this section (§13.7).

## Vocabulary data model

The interactive matrix is [`vocabulary.html`](vocabulary.html); this chapter is
the data model behind it. Consolidated from the former
`vocabulary/flove-fields.md` (removed 2026-11-19).

### Field kinds

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
- Apps whose manifest sets `"displayOnly": true` declare `fields: []` **by
  design** (content, hub and viewer pages). `check-routing.py` reports them as
  complete instead of warning about missing extraction.

### The `kind:input` contract (what questy-flove reads)

`kind:input` is the **user-data field list** — the exact slots to gather texts
about through questioning. It is a target contract for a future questy-flove
consumer, not a live dependency. The tool's export with the kind filter set to
`input` yields it directly.

### Hats & colours

**Hats belong to Questy; category colours are the standard flove palette.**
`fields-colours.json` / `fields-colours.ods` are retired; there is no separate
per-slot hat catalog.

| category | colour | Questy hat |
|----------|--------|------------|
| Inside | `#ff9b5e` | heart |
| Mating | `#ffd84d` | optimism |
| Ling / Words | `#6ed089` | creative |
| Social | `#5ea4e6` | make |
| Economy | `#6b6bd9` | facts |

Use the table only as the **hat → category-colour analogy**, and only when
influence > 0 and hats are selected. `risk` is the black counterpart of heart
and shares **Inside**. App/field data comes from `tools/routing.json`
(`apps[].fields`); do not derive a second field catalog.

### Flat field index (technical)

- Every app with a `flove-fields/1` manifest exposes **`window.floveFieldsFlat()`**:
  a read-only list of `{path, id, label, type, parent}` for cross-app lookups.
  It is added by a `data-flove-fields-flat` script; no UI, storage or network
  change.
- [`tools/routing-index.json`](../../tools/routing-index.json) is the generated
  flat index for all routed apps (currently **1,288 fields**). Rebuild with
  `python3 tools/build-routing-index.py`; verify with `--check`.
- [`tools/check-routing.py`](../../tools/check-routing.py) validates app ids,
  field trees, `fieldCount`, cross links and the colour-free rule.
- Colours are **not** in the router or the index yet; see
  [`frontend/routing-colours-db.md`](frontend/routing-colours-db.md).

### Cross-app routing — `tools/routing.json`

The app registry and cross-app graph live in
[`tools/routing.json`](../../tools/routing.json) — the canonical registry
(do not recreate a `addons/routing.json` mirror):

- `apps[]` — id, name, url, description, tags, category, optional `field`
  and `fieldPage`, a `fields` **tree** (`text`/`text[]`/`number`/`file`/`date`/`time`/`boolean`/`pick`/`multi`/`group`/
  `repeat`; fields inherit their category; optional `related[]` topic names and category/name/cross paths, never colour) and
  `fieldCount`; `status` is
  `complete` or `partial`;
- `categories{}` — each category (mating/inside/ling/social/economy) as
  **identity only**, with no palette and no colour; each consumer maps a category
  to its own colour/hat. Field relations are by category and name/cross path;
- `cross[]` — field-to-field relations (`source`, `target`, `merge`, `why`),
  e.g. PracSys system verbs → souls system verbs;
- `consumers{}` — extractive readers (questy) and what they read;
- `pending[]` — the `field-export` / `extractor` / `metadata` / `cross` gaps.
- **Field manifests** — each imported app embeds `flove-fields/1`; run
  `python3 tools/extract-fields.py --apply` to refresh `apps[].fields` from the
  apps themselves (`--check` for drift).

Questy's **Flove influence** ladder uses the app's category: all fields of all
apps in the same category share that category's hat, and `cross[]` prioritises
specific field links. The integration field list lives in `routing.json`'s
`apps[].fields` (every label inherits its category hat from `categories{}`);
this catalog remains the detailed colour/hat/vocabulary study and the two must
stay in sync.

### Labelers ↔ hats (compositional rendering)

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
- **Matrix scope.** The vocabulary matrix carries labeler variants only for
  **Blogy**; every other app exposes one `Default` text. The families above
  remain the compositional rendering model, not per-app columns.

The questy survey selects a family via its **Love · Joy · Wisdom** row; each
segment links to the matching anchor on `apps/sys/wizy/` (`#love #joy #wise
#random`), which hosts the interactive preview.