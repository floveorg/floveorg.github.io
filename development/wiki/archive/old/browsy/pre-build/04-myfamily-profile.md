# 04 · MyFamily profile — 7 areas × 5 replies → 5 percentages

> Replaces the old “name + relation + 2–3 traits + one affinity” projection.
> The person is the MyFamily profile; the group sees a summary.
>
> A new person defaults to **P** (private). **Wizy may read P locally** on the
owner’s device; sharing to a group/peer requires an L projection. S is explicit.

## The 5 types

Ordered least → most, matching the app’s `col1`…`col5`:

| # | Type (EN) | Type (ES) | Key |
|---|---|---|---|
| 1 | Cousin | Prima/o | `cousin` |
| 2 | Sibling | Hermana/o | `sibling` |
| 3 | Grandparent | Abuela/o | `grandparent` |
| 4 | Parent | Madre/padre | `parent` |
| 5 | Partner | Pareja | `partner` |

The UI may keep “Couple” as a local alias, but the canonical model word is
**Partner**.

## The 7 areas

Each area is a section with 5 possible replies (`col1`…`col5`), using the
MyFamily labels already in `apps/trusty/myfamily.html`:

| Key | Area (EN) | Área (ES) |
|---|---|---|
| `attention` | Attention | Atención |
| `contact` | Contact | Contacto |
| `influence` | Influence | Influencia |
| `feedback` | Feedback | Devoluciones |
| `gifting` | Gifting | Regalos |
| `sharing` | Sharing | Compartir |
| `money` | Money | Dinero |

The 35 reply labels stay in the MyFamily app; Browsy treats them as the
canonical vocabulary. Do not invent a second trait list.

## Profile shape

```json
{
  "personId": "p_ana",
  "displayName": "Ana",
  "areas": {
    "attention": [1,0,0,0,0],
    "contact":   [0,1,0,0,0],
    "influence": [0,0,1,0,0],
    "feedback":  [0,0,0,1,0],
    "gifting":   [0,1,0,0,0],
    "sharing":   [0,0,0,0,1],
    "money":     [1,0,0,0,0]
  }
}
```

- Each vector has exactly 5 slots, one per type.
- A slot is `1` when that reply is selected, otherwise `0`.
- More than one reply per area is allowed by the app; the vector supports it.

## Percentages

For each type `t`:

```
pct(t) = round( count(t) * 1000 / totalSelections ) / 10
```

- `count(t)` = number of `1`s in slot `t` across the 7 areas.
- `totalSelections` = total `1`s across all areas.
- Round to one decimal; adjust one bucket by ±0.1 if the sum is not exactly
  100.0.

Example: 2 Cousin + 2 Sibling + 1 Grandparent + 1 Parent + 1 Partner = 7
selections → 28.6 / 28.6 / 14.3 / 14.3 / 14.2.

## What the group sees

Default projection (`myfamily-profile/1`):

```json
{
  "displayName": "Ana",
  "percentages": {
    "cousin": 28.6,
    "sibling": 28.6,
    "grandparent": 14.3,
    "parent": 14.3,
    "partner": 14.2
  }
}
```

- The **5 percentages** are the group projection.
- The raw 7×5 answers stay in the person record as P/L.
- Sharing the raw answers is an explicit per-group opt-in; the group bundle
  then adds `areas` and a `rawAreas: true` flag.
- No `relation`, `traits` or `affinity` fields exist.

## Consult agreements

An owner can sign `flove-consult/1` to let a selected member’s Wizy consult
selected person/group/paths. The Wizy gets derived answers, not raw P. See
[`09-consult-agreements.md`](09-consult-agreements.md).

## UI

- Person page: the 7 MyFamily sections, unchanged.
- Group card: a compact 5-bar chart with the type labels and percentages.
- Group settings: “Share the 7 areas with this group” checkbox (off by
  default).
- A person can be in several groups with different raw-area choices; the 5
  percentages are the same because they derive from the same person record.

## Why this is better

- It keeps the MyFamily vocabulary the user already knows.
- It is a real projection, not a second taxonomy.
- It is comparable across people: every profile has the same 5 buckets.
- It gives the group a privacy-safe summary by default.
