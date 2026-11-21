<!-- CONTEXT:BEGIN
schema: flove-page/1
id: data/mds
path: development/standards/mds.md
trunk: data
topic: mds
kind: topic
status: stable
html_place: ["#data"]
owns: ["MD sources", "library insights"]
updated: 2026-11-21
read_next: ["#upper-ontology","#per-app-mapping","#vocabulary-policy","#asterism-path","#data-depth-levels","#md-index","#md-json","#link-validation","#canonical-md-index","#fallback-docs"]
supersedes:
  - development/wiki/archive/old/bridges/oasis.md
  - development/wiki/archive/old/browsy/browsy-questions.md
  - development/wiki/archive/old/browsy/pre-build/README.md
  - development/wiki/archive/old/browsy/rationale.md
  - development/wiki/archive/old/others/flove-libs-insights.md
  - development/wiki/archive/old/plans/central-backend.md
  - development/wiki/archive/old/questy-proposals.md
  - development/wiki/archive/old/root/adoption.md
  - development/wiki/archive/old/root/backend.md
  - development/wiki/archive/old/standards.md
heavy: false
CONTEXT:END -->

# MD sources

> **Pilot migration (phase 2).** This page imports `backend.md` §3.1–§3.4 and
> §12.

## Upper ontology

> Source: `development/wiki/archive/old/root/backend.md#31--upper-ontology--universal-classes` (archived 2026-11-21).

Every concrete app field maps to one of a small set of universal classes. Apps
may add their own subclasses, but the upper classes are the only thing the
common-area views, the cross-link graph and module 42 are required to
understand.

| Class | What it represents | Example emitting apps |
|---|---|---|
| `Act` | An action performed by a person on/with something | loves (gift), thingy (offer) |
| `Wish` | A desire / pending act | thingy (need/want), wanty (essence) |
| `Bond` | A relationship between two persons | MyFamily, daty |
| `Place` | A spatial location (point or region) | openastro, MyFamily, daty |
| `Person` | A human (self or other), pseudonymous OK | MyFamily, daty, avatar |
| `Time` | A point or interval in time | daty, openastro, realy |
| `Object` | A thing/concept being rated or referenced | rate, realy |
| `Freedom` | A declared right or boundary | socy, hackboth, diesafe |
| `Rating` | A puzzy annotation | rate, any other app via attach |

Mapping rule: every leaf field of every app declares which universal class it
carries. This is what lets the common area treat fields from different apps as
queryable peers.

## Per-app mapping

> Source: `development/wiki/archive/old/root/backend.md#32--per-app-mapping` (archived 2026-11-21).

Each app ships a small `mapping.json` next to its HTML that declares, for every
field name, which upper class the field carries:

```json
{
  "app": "loves",
  "type": "act",
  "subtype": "gift",
  "fields": {
    "from":    { "class": "Person", "vocab": "person",  "free_tags": false },
    "to":      { "class": "Person", "vocab": "person",  "free_tags": false },
    "thing":   { "class": "Object", "vocab": "object",  "free_tags": true  },
    "context": { "class": "Place",  "vocab": "place",   "free_tags": false },
    "motive":  { "class": "Wish",   "vocab": "essence", "free_tags": false }
  }
}
```

This file is the bridge between the app’s free-form HTML and the upper
ontology; the F0 persistence layer reads it to populate `FloveElement.fields`
correctly.

## Vocabulary policy

> Source: `development/wiki/archive/old/root/backend.md#33--vocabulary-policy` (archived 2026-11-21).

| Mode | Meaning | Updateable by |
|---|---|---|
| `closed` | Versioned canonical list; only project releases add terms | flove release |
| `closed + IA-sug` | Same as closed but **wizy** may **suggest** new terms inline | flove release (after curation) |
| `free` | User-typed tags, no validation, indexed as-is | every user |

`free_tags: true` on a field opts that field into the `free` mode in addition to
its declared closed vocabulary. Module 42 suggestions are always proposals — a
release cycle decides whether they enter the canonical list.

## Asterism path

> Source: `development/wiki/archive/old/root/backend.md#34--asterism_path-per-sub-field` (archived 2026-11-21).

Every field carries its **own** coordinate inside the **Whole** taxonomy
(`docs/index.html`), not just the element as a whole. This lets a single element
appear simultaneously in several cells of the whole-matrix view (one per field)
and lets cross-link search hit the right granularity.

```json
{
  "asterism_path": "puzzy/relate/rate",
  "fields": {
    "subject": { "class": "Object", "value": "TRUE",
                 "asterism_path": "puzzy/relate/rate/subject" },
    "anchor":  { "class": "Object", "value": "LOVE",
                 "asterism_path": "puzzy/relate/rate/anchor" }
  }
}
```

## Data depth levels

> Source: `development/wiki/archive/old/root/backend.md#12--data-depth-levels` (archived 2026-11-21).

| Level | Name | What it covers | Commands |
|---|---|---|---|
| 1 | Surface | Every string the reader sees: headings, prose, buttons, hints, empty and error states, text read aloud. | texty1 · translaty1 |
| 2 | Labels | Metadata and field labels: `<title>`, description, aria-label, title, placeholder, field labels, data-aria-*/data-ph-*, i18n display values. | texty2 · translaty2 |
| 3 | Names | Internal names: classes, ids, JS identifiers, data and i18n keys. Rename or translate display values; never the keys. | texty3 · translaty3 |
| 4 | Data | Display values inside manifests and envelopes: flove-fields, routing descriptions and tags, flove-portrait values, i18n tables. Keys stay untouched. | texty4 · translaty4 |
| 5 | Contracts | Canonical identifiers and contracts: routing.json, flove-fields, the export schema, routes and enum names. Read-only for text and translation. | texty5 · translaty5 |

## Work

9 hitos · 37 tasks · 5 open · 4 closed. This page owns the `data/mds` chapter.

<a id="md-index"></a>
## MD index

> Owner: mds. One index maps every live MD to an axis and degree; no live MD is
> orphaned.

<a id="md-json"></a>
## MD → JSON

> Owner: mds. Envelope and field rules derived from the MDs; a changed doc is
> detected by a check. Prose stays prose.

<a id="link-validation"></a>
## Relative-link validation

> Owner: mds. Broken relative links fail before publish; external URLs are
> explicitly skipped or checked.

<a id="canonical-md-index"></a>
## Canonical MD index

> Owner: mds. The canonical index lists each live document once with its
> authority.

<a id="fallback-docs"></a>
## Fallback documents

> Owner: mds. Every fallback MD points back to one canonical page fact.

## Sources

- `development/wiki/archive/old/root/backend.md` §3.1–§3.4, §12.
- `development/wiki/archive/old/others/flove-libs-insights.md`.

## Source map

| Archived source | Date | Stable home |
|---|---|---|
| `bridges/oasis.md` | undated | development/standards/mds.md |
| `browsy/browsy-questions.md` | undated | development/standards/mds.md |
| `browsy/pre-build/README.md` | undated | development/standards/mds.md |
| `browsy/rationale.md` | undated | development/standards/mds.md |
| `others/flove-libs-insights.md` | undated | development/standards/mds.md |
| `plans/central-backend.md` | undated | development/standards/mds.md |
| `questy-proposals.md` | undated | development/standards/mds.md |
| `root/adoption.md` | undated | development/standards/mds.md |
| `root/backend.md` | undated | development/standards/mds.md |
| `standards.md` | undated | development/standards/mds.md |

Chapters without a separate source row are `milestone-only`: they are
specified from the register (hitos and tasks) and remain owned here.
