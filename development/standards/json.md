<!-- CONTEXT:BEGIN
schema: flove-page/1
id: data/json
path: development/standards/json.md
trunk: data
topic: json
kind: topic
status: stable
html_place: ["#data-json"]
owns: ["flovePortrait/1", "routing index", "data index"]
updated: 2026-11-21
read_next: ["#routing","#publisher-adapter","#common-traceable-area","#id-recovery","#index-rules","#flat-index-consumer-map","#profile-percentages","#feed-provenance","#envelopes","#interop"]
supersedes:
  - development/wiki/archive/old/bridges/oasis.md
  - development/wiki/archive/old/browsy/pre-build/03-schemas.md
  - development/wiki/archive/old/browsy/rationale.md
  - development/wiki/archive/old/plans/2026-11-20-appy-dashboard-redesign.md
  - development/wiki/archive/old/plans/2026-11-21-app-database-stages.md
  - development/wiki/archive/old/proposals/frontend-wizy.md
  - development/wiki/archive/old/root/backend.md
heavy: false
CONTEXT:END -->

# JSON

> **Migrated 2026-11-21.** This page imports the archived `root/backend.md` §5, §6 and §7.

## Routing

> Source: `development/wiki/archive/old/root/backend.md#5--routing-apps--backend-modules` (archived 2026-11-21).

The module map lives as a **declarative `routing.json`** file, never as
hard-coded logic inside each app. The map below is the 0asis demo mapping; the
same elements route to nety’s own modules natively.

| App · element | 0asis demo module |
|---|---|
| loves · act:gift | Market |
| thingy · offer/need | Market |
| socy | Parliament |
| MyFamily | Tribes (forum) |
| MyFamily · private | DM |
| daty | Tribes (forum) |
| daty · private | DM |
| wanty · essence | Feeds |
| diesafe · legacy | DM |
| hackboth | Parliament |
| realy | Media |
| openastro | Feeds |

## Publisher adapter

> Source: `development/wiki/archive/old/root/backend.md#6--publisher-adapter-portability` (archived 2026-11-21).

One interface, several implementations:

| Implementation | Target |
|---|---|
| `NetyPublisher` | nety GraphQL gateway; **corporate backend default** |
| `OasisPublisher` | 0asis module; integration demo |
| `ActivityPubPublisher` | ActivityPub outbox; future |
| `LocalOnlyPublisher` | IndexedDB; tests |

`Publisher` exposes `publish(element)`, `fetch(ref)`, `search(query, filters)`,
`subscribe(channel, handler)` and `identity()`. The app never knows which
implementation is running.

## Common traceable area

> Source: `development/wiki/archive/old/root/backend.md#7--common-traceable-area` (archived 2026-11-21).

Served by the **nety** corporate backend. The 0asis add-on can mirror it as an
integration demo, but the authoritative common area lives on nety.

| Priority | View |
|---|---|
| 1 | Semantic AI search (wizy fine-tuned with whole + puzzy) |
| 2 | whole-matrix (elements placed on their cell) |
| 3 | Graph (which element appears in which apps) |
| 4 | Feed (chronological) |

All four read the unified index: published elements + `asterism_path` +
`puzzy_annotations`.

## Work

14 hitos · 53 tasks · 7 open · 7 closed. This page owns the `data/index` and
`data/json` chapters.

<a id="id-recovery"></a>
## Id recovery and app feeds

> Owner: json. The canonical id source is the record’s own id; an app recovers it
> without a central listing. Feed shape is `{items, next_cursor}`.

<a id="index-rules"></a>
## Index rules for the depth levels

> Owner: json. The five data-depth levels are defined in `mds.md#data-depth-levels`;
> this page owns their index rules and forbids overlapping definitions.

<a id="flat-index-consumer-map"></a>
## Flat index and consumer map

> Owner: json. `routing.json` and `floveFieldsFlat()` provide one flat entry per
> item; this section maps each consumer to one source field.

<a id="profile-percentages"></a>
## 7 × 5 → five percentages

> Owner: json. The projection rule is selected replies per type ÷ total, rounded
> to one decimal and summing to 100; only percentages leave the device.

<a id="feed-provenance"></a>
## Feed shape and provenance

> Owner: json. Each feed row carries its provenance; a feed rebuilds from local
> data alone. Public-by-default is an explicit decision, not an assumption.

<a id="envelopes"></a>
## JSON envelopes

> Owner: json. Portrait, work, auth, group, consult and puzzy envelopes each have
> one schema id and round-trip through export/import.

<a id="interop"></a>
## Data interoperability

> Owner: json. Oasis types and graph shape map to flove envelopes with one
> conversion note per type.

## Sources

- `development/wiki/archive/old/root/backend.md` §5–§7.
- `development/wiki/archive/old/plans/2026-11-21-app-database-stages.md`.
- `tools/routing.json`.

## Source map

| Archived source | Date | Stable home |
|---|---|---|
| `archive/old/bridges/oasis.md` | 2026-08-01 | development/standards/json.md |
| `archive/old/browsy/pre-build/03-schemas.md` | 2026-11-17 | development/standards/json.md |
| `archive/old/browsy/rationale.md` | 2026-11-17 | development/standards/json.md |
| `archive/old/plans/2026-11-20-appy-dashboard-redesign.md` | 2026-11-20 | development/standards/json.md |
| `archive/old/plans/2026-11-21-app-database-stages.md` | 2026-11-21 | development/standards/json.md |
| `archive/old/proposals/frontend-wizy.md` | 2026-11-19 | development/standards/json.md |
| `archive/old/root/backend.md` | 2026-08-01 | development/standards/json.md |

Chapters without a separate source row are `milestone-only`: they are
specified from the register (hitos and tasks) and remain owned here.
