# Routing colours, optimisation and future databases

> Status: **routing optimisation done; colours and future DB pending**
> (2026-11-18). `tools/routing.json` remains the canonical app/field router.
> Flat index: `tools/routing-index.json`; validator: `tools/check-routing.py`.
> Every app now exposes `window.floveFieldsFlat()` for technical combination.

**Tracked work:** RC01 (consumer colour map) and RDB01 (future DB) are rows in
[`../debates/pendings.md` §Browsy pre-build](../../wiki/archive/old/pendings.md); Work filter:
[data · json](https://flove.org/development/index.html#work?tab=docs&view=r2&subtab=work&category=data&section=json).

## Current state

- `tools/routing.json` (`flove-routing/3`) has **no colour** by design: categories
  are identity only; consumers map category → colour/hat.
- `development/standards/vocabulary.md` holds the current
  category palette:

| Category | Colour | Questy hat |
|---|---|---|
| Inside | `#ff9b5e` | heart |
| Mating | `#ffd84d` | optimism |
| Ling / Words | `#6ed089` | creative |
| Social | `#5ea4e6` | make |
| Economy | `#6b6bd9` | facts |

- Fields currently inherit their **category** colour; there is no per-field
  colour, tone or state.

## Done

- `tools/check-routing.py` — app/field/cross/fieldCount validation, colour-free rule.
- `tools/build-routing-index.py` — flat `tools/routing-index.json` (1,288 fields).
- `window.floveFieldsFlat()` in every app with a manifest — read-only, no UI change.
- `routing.json` metadata points at the index; palette pending entry added.

## Goal

1. Specify **additional colours** for routing fields without turning
   `routing.json` into a palette.
2. Keep the router **identity-only**; colours live in a separate consumer map.
3. Optimise `routing.json` (size, duplication, schema, consumers, pending list).
4. Specify the **future database** for routing and colours.

## Proposed colour model

Keep **category** as the base. Add a small, finite **field tone** layer:

| Tone | Meaning | Use |
|---|---|---|
| `input` | a field the user fills | forms, question slots |
| `output` | a derived/read field | summaries, results |
| `meta` | identity, tags, descriptions | headers, metadata |
| `relation` | cross/related fields | graph edges, cross links |
| `repeat` | repeatable groups | lists, rows |
| `action` | buttons/commands | verbs, actions |

A field colour is a function of **category base + tone**, not an arbitrary
colour per field. Optional per-field overrides are allowed only by path, with a
reason.

### Consumer map

Do **not** add `color` to `routing.json` fields. Add a separate map, e.g.:

```json
{
  "schema": "flove-routing-colours/1",
  "base": "category",
  "categories": {
    "inside": { "light": "#ff9b5e", "dark": "#ffb27d" },
    "mating": { "light": "#ffd84d", "dark": "#ffe27a" },
    "ling":   { "light": "#6ed089", "dark": "#8fe0a5" },
    "social": { "light": "#5ea4e6", "dark": "#8cc3f2" },
    "economy":{ "light": "#6b6bd9", "dark": "#9696ef" }
  },
  "tones": {
    "input":  { "mix": 0.0,  "label": "input" },
    "output": { "mix": 0.18, "label": "output" },
    "meta":   { "mix": -0.12, "label": "meta" },
    "relation": { "mix": 0.28, "label": "relation" },
    "repeat": { "mix": 0.08, "label": "repeat" },
    "action": { "mix": 0.35, "label": "action" }
  },
  "overrides": []
}
```

- `mix` is a tint/shade relative to the category base, not a new hue.
- `light`/`dark` are required for both themes.
- Contrast is checked, not hand-waved: each pair must meet the project’s
  contrast bar.
- Consumers (Questy, Browsy, Appy, charts) can render the same field
  consistently.

## Optimisation of `routing.json`

Proposed pass, no schema break in v1:

1. **Validate** against a JSON Schema; add `tools/check-routing.py`.
2. **Dedupe** field IDs and repeated labels; keep the tree parent/order.
3. **Normalise** `field` / `fieldPage` / `fields` semantics; one source for the
   field tree.
4. **Check** `fieldCount` against the actual tree; fix drift.
5. **Trim** `cross[]` duplicates and dead `pending[]` items.
6. **Document** `consumers{}` and what each reads.
7. **Size budget**: set a target and measure before/after; do not split the
   canonical file without a migration plan.
8. **Exporter**: keep a generated read-only view for consumers, with a version
   and hash.

## Future database

The JSON stays the authored source; a database is a read model/mirror.

Proposed tables:

| Table | Key fields |
|---|---|
| `routing_version` | `id`, `schema`, `version`, `hash`, `created_at` |
| `categories` | `id`, `name`, `slug` |
| `apps` | `id`, `name`, `url`, `category`, `status`, `description` |
| `fields` | `id`, `app_id`, `parent_id`, `order`, `label`, `type`, `tone` |
| `cross_relations` | `id`, `source_field`, `target_field`, `merge`, `why` |
| `consumers` | `id`, `name`, `reads[]` |
| `pending` | `id`, `kind`, `reason`, `status` |
| `palettes` | `id`, `name`, `schema`, `version` |
| `category_colours` | `palette_id`, `category_id`, `light`, `dark`, `contrast` |
| `field_colours` | `palette_id`, `field_path`, `tone`, `light`, `dark`, `contrast` |

- **SQLite/Turso** is the likely mirror (Central), not the authority.
- JSON → DB migration is versioned; a hash identifies the source.
- The colour tables are separate from `routing` tables: the router remains
  colour-free.
- If a DB is not needed yet, keep the JSON + consumer map; do not add a server
  dependency.

## Open questions

1. Category-only colours, or category + tone? (proposed: category + tone)
2. Who owns the palette: vocabulary, frontend, or a shared design token file?
3. Is a per-field override ever allowed, or only tone?
4. Which contrast target: WCAG AA, AAA, or a custom flove bar?
5. When does the DB arrive: before or after the routing optimisation?
6. Does `routing.json` stay the only authored source? (proposed: yes)
7. Is the colour map shipped in `tools/` or `development/standards/`?
