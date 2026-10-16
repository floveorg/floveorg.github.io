# proposals.md

Active proposals awaiting resolution.

## P001 [resolved] Archive resolved items instead of deleting

**Source:** questy skill enhancement
**Status:** resolved
**Description:** When a user selects the "archive" option in the questy HTML survey, resolved items should be moved to an archive file instead of being deleted. This preserves history while keeping the main file clean.

**Resolution:** Implemented in SKILL.md — archive mode moves resolved items to archived-questions.md instead of deleting them. HTML toggle exists in Addons → Agents.md → archive.

**Date resolved:** 2026-07-27

## P002 [resolved] Addon row layout and Continue config

**Source:** questy HTML redesign
**Status:** resolved
**Description:** Restructure addons layout with Archive/Pro on left and Scripts on right. Move .github before HTML. Workflows only shown when Git is selected. Add Continue Addons Config button to show additional settings.

**Resolution:** Implemented — layout restructured, workflows conditional on Git, Continue button added with per-addon config fields.

**Date resolved:** 2026-07-27

## P003 [resolved] Info texts for Archive, Pro, Scripts

**Source:** questy UX enhancement
**Status:** resolved
**Description:** Show info texts when Archive, Pro, or Scripts are checked. One row per addon with X to hide. Info stays visible when collapsed.

**Resolution:** Implemented — addon-info-row elements with close button, shown on check, hidden on uncheck or X click.

**Date resolved:** 2026-07-27

## P004 [resolved] Human icon and use case button

**Source:** questy UX enhancement
**Status:** resolved
**Description:** Add human icon floating top right that shows humanized descriptions. Move Scripts to Continue config section. Add info button at bottom that generates use case narrative.

**Resolution:** Implemented — 👤 icon toggles human descriptions, Scripts in Continue config, ℹ button generates use case text based on selections.

**Date resolved:** 2026-07-27

## P005 [resolved] Scripts row layout and Demonstrative Use Cases

**Source:** questy UX enhancement
**Status:** resolved
**Description:** Rename Continue Addons Config to Scripts. Show scripts one per row with tech description on click. Convert ℹ button to option style, rename to Demonstrative Use Cases, request use case generation in prompt.

**Resolution:** Implemented — Scripts button shows script rows with expandable descriptions, Demonstrative Use Cases option triggers use case generation request in prompt.

**Date resolved:** 2026-07-27

---

> Consolidated 2026-08-01 from the older `debates/PROPOSALS.md` snapshot
> (deleted — this file is the single home for questy proposals).

## P006 [resolved] Move questy out of .agents/skills

**Source:** project structure cleanup
**Status:** resolved
**Description:** All questy files should live in visible project dirs, not hidden `~/.agents/skills/`.
**Resolution:** Moved out of `~/.agents/skills` into the visible flove tree. Final location (2026-08-01): `development/standards/skills/questy/` — skill (SKILL.md), web app (index.html, crowd-questy.html, tour.html), and shared assets (presets/, templates/) together as one real copy, loaded via the `~/.agents/skills` symlink. `~/.agents/skills/questy/` removed.
**Date resolved:** 2026-07-28

## P007 [resolved] Consolidate questy-html

**Source:** project structure cleanup
**Status:** resolved
**Description:** Two questy-html files existed separately. Consolidate into tools/questy-html/ folder.
**Resolution:** Consolidated at `development/standards/skills/questy-html/` with SKILL.md, README.md, questy-html-flove.md, DESIGN-questy-html.md, gen-feeds.js, template.html, template123.html. Old pointer SKILL.md and `central/questy/tools/questy-html/` removed (2026-08-01).
**Date resolved:** 2026-07-28

## P008 [active] standards.md for questy

**Description:** Create questy's own development standards (official routes, rules, error handling, version format, preset authoring guide).
**Resolution:** Created at `development/standards/debates/standards.md`. Expanded with error handling, version/changelog, preset authoring, commands reference, proposals format.

## P009 [active] Tour HTML

**Description:** Create professional 5-slide graphical tour explaining why/what/how questy works.
**Resolution:** Created at `development/standards/skills/questy/tour.html`. 5 slides (problem, solution, system, workflow, get started), keyboard nav, dark theme.

## Conflict resolution — skill standard vs HTML form

### Naming (resolved)

| # | Area | Decision |
|---|------|----------|
| 1 | Types | **Words only** — vision, arch, trust, data, integration (no colors) |
| 2 | Hats yellow | **optimism** (not vision) |
| 3 | Hats blue | **make** (not process) |
| 4 | Lens type | **Removed** — not in KISS |
| 5 | Agents.md naming | **Current technical names** (shortcuts, constraints, etc.) |

### Structure (resolved)

| # | Area | Decision |
|---|------|----------|
| 6 | File count question | **Not needed** — routes field covers it |
| 7 | Resume flow | **Not needed** — will add later if needed |
| 8 | Addons naming | **Keep both** — skill uses folders, form uses addons |
| 9 | Workflows | **Added to skill** — full section |
| 10 | PR standards | **Added to skill** — full section |

### Agents.md (resolved)

| # | Area | Decision |
|---|------|----------|
| 11-14 | Existing sections | **Keep** — shortcuts, constraints, pending-resolutions, decision-log |
| 15-21 | New sections | **Added** — batch-overrides, export-prefs, territory, aliases, danger zone, archive |

## Deferred

| # | Area | Decision |
|---|------|----------|
| 1 | questy-html progress indicator | Defer — implement when questy-html is active |
| 2 | questy-html save/load state | Defer — localStorage already handles this |
| 3 | Multi-user scenarios | Defer — not needed yet |
| 4 | Error recovery for malformed config | Deferred — fallback to defaults works for now |