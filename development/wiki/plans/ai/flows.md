---
status: stable
section: ai/flows
created: 2026-11-21
also: []
---

# ai/flows plan

> **Child plan.** The stable page owns the facts; this file records the dated
> source history and open plan decisions. Updated 2026-11-21.

<a id="wizy-operating-areas"></a>
## Wizy operating areas (draft)

> Source: `development/wiki/archive/old/proposals/frontend-wizy.md` (archived 2026-11-21).

> 2026-11-17. Draft, pending the Wizy standardization pass. Wizy is not yet a
> fixed standard; this file records the agreed **areas** so apps (and the
> summary’s Custom magic) have a home to point at.

### What Wizy is

The contextual influence layer: it reads an app’s portrait and proposes what
could be said, asked or explored next. Pure client-side, no backend; each app
keeps a local fallback because apps are single-file and offline.

### Operating areas

| Area | Where it lives | Status |
|---|---|---|
| **Custom magic insights** | Reads your flove and other portraits you want to add, offering lovely suggestions and rewards | Pending |
| **Key fields** | Apps' key fields, exported prompts, the interview flow's influence degree / question suggestions; questy colours related to the full flove ontology at degrees 1–5 | Pending |
| **Exported prompts** | Shapes the prompt handed to the user’s agent (`floveAgentBlock` / Wizy agent block) | Partly live |
| **External embeds** | Embedded in external apps / pages | Pending |
| **(G)Local Browsy** | Its own data-sharing network: local pulls and local derivation, social only with consent | Pending |
| **Appy Magic** | The Magic button below Upload played app here: Myself / With others (three wizards) | Live |
| **Wizy Labelers** | Advanced space: re-voices an app’s labels in a chosen perspective — blogy is the demo (8 labelers) | Live demo |
| **Wizy Raty** | The wide wizard list from Raty’s 28 rater scales + the add-a-wizard form | Live demo |
| **Wizy Helpers** | A help page as a Wizy space — dealy’s help / new-bot pages are the demo | Live demo |

“Operating area” is deliberately broader than a page section: the same engine
appears as a floating layer, as field hints, as agent context, as an embed, and
as a network participant.

**Index surface.** The Wizy page mirrors this table at
`apps/sys/wizy/index.html#areas`; update both when an area changes status.
Questy-flove is described inside Key fields rather than as a separate row.
The Browsy field test (`apps/sys/browsy/2026-11-18-browsy-extension-demo.html`)
shows the (G)Local Browsy area in context. P2P permissions are tracked in
`debates/plans/`, not listed as a Wizy area.

### Custom magic contract (proposal)

```js
wizy.custom(portrait) -> {
  text: 'a personal reflection',
  area: 'custom',
  weight: 1..3
} | [{ text, area:'custom', weight }]
```

- Input: the `flove-portrait/1` envelope (same as `wizy.suggest`).
- Output: one or a few gentle reflections, never instructions.
- No backend; no network. If Wizy is absent, the app shows a neutral prompt, not
  an empty button.
- The summary renders the chosen text; it is **not** part of `rows` unless the
  app already exports it.
- The floating bottom layer is the canonical UI for Custom magic; an app may
  also expose the same content inline while the layer is being built.

### Relationship to the summary standard

[`../../frontend/summary.md` §13.9](../../../standards/frontend/summary.md) (revision
2026-11-17; summary plan consolidated): **Magic → General** is the app’s own
insight/reflection text; **Magic → Custom** is this contract. The separate
Insight button retires.

### Open questions

1. Canonical home for the engine: `apps/appy/wizy.js` (current) vs a new
   `wizy/` module — and how the floating layer ships with a single-file app.
2. Is Custom magic generated on demand, cached per play, or both?
3. How do the Browsy federation and NetyBrowsy permissions share the same
   consent model?
4. What is the Wizy standard’s owner file — this draft, or a section in
   `frontend/frontend.md`?

Not yet in the issue register; flagged here for the owner (Work filter:
[ai · models](https://flove.org/development/index.html#work?tab=docs&view=r2&subtab=work&category=ai&section=models)):

- [debate] Wizy engine canonical home — Work: https://flove.org/development/index.html#work?tab=docs&view=r2&subtab=work&category=ai&section=models
- [debate] Custom magic on demand vs cached per play — Work: https://flove.org/development/index.html#work?tab=docs&view=r2&subtab=work&category=ai&section=models
- [debate] Shared consent model for Browsy and NetyBrowsy permissions — Work: https://flove.org/development/index.html#work?tab=docs&view=r2&subtab=work&category=ai&section=models
- [debate] Wizy standard owner file — Work: https://flove.org/development/index.html#work?tab=docs&view=r2&subtab=work&category=ai&section=models

### Magic button — Appy, Browsy (Nety later)

**Placement.** Appy: inside the upload section, directly below the
**Upload played app here** row (above the played icons and submitted posts).
Browsy: directly below the hero. Nety: same component later; not part of this
pass.

**Status (2026-11-18).** Implemented in [`apps/appy/index.html`](../../../../apps/appy/index.html)
and [`apps/sys/browsy/index.html`](../../../../apps/sys/browsy/index.html).
Nety is pending.

**Shape.** One `✨ Magic` button toggles one panel. No introduction, no footer.

1. **Three wizards** — `Love`, `Joy`, `Wisdom`, as three icon+label buttons.
   The selected wizard is `aria-pressed="true"`.
2. **Two modes** — `Myself` and `With others`.
3. **Myself** — shows three suggestions. Each suggestion links **two content
   items from different uploaded plays**, joined by a **different preposition**
   per suggestion. The link text is the play's `phrase`, `summary.text` or first
   filled row; the app name goes in `title`. A `3 more` button below appends the
   next three.
4. **With others** — reads `flove:myfamily:state`, takes the named person
   (`friend`) and their strongest category, and renders **one readable
   sentence** that combines two of my play links with that person and category.
   With no person, show one minimal line, not an intro.
5. **Empty / short data** — fewer than two distinct apps: one minimal line.
   No backend, no network; links open the source app page from
   `#play-apps .appbtn[data-app]` (fallback `#`).

**Data sources.**

| Input | Key | Notes |
|---|---|---|
| Uploaded plays | `flove:appy:plays` (`window.flovePlays()` in Appy) | `app`, `portrait`, `id` |
| MyFamily person | `flove:myfamily:state` | `friend` + checked `category:col` keys |
| App link | `#play-apps .appbtn[data-app="<app>"]` | Appy; Browsy reads `tools/routing.json` and falls back to the Appy profile |

**Wizard prepositions.**

| Wizard | Prepositions |
|---|---|
| Love | with · for · beside · near · toward |
| Joy | after · into · around · beyond · against |
| Wisdom | through · within · from · before · across |

**Acceptance.**

- Appy: Magic sits below the upload button; Browsy: same interaction; Nety:
  documented, pending.
- Myself: exactly three links, two different apps each, three different
  prepositions; `3 more` appends three without duplicates.
- With others: one sentence with two play links + MyFamily name + category;
  fewer than two apps shows one minimal line.
- No intro/footer; keyboard focus and `aria-live` on results.

## Source index

### UseCase-adv.md — 2026-08-01

- Archive: `development/wiki/archive/old/UseCase-adv.md`
- Stable home: `development/standards/flows.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/browsy-questions.md — 2026-08-01

- Archive: `development/wiki/archive/old/browsy/browsy-questions.md`
- Stable home: `development/standards/flows.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/rationale.md — 2026-11-17

- Archive: `development/wiki/archive/old/browsy/rationale.md`
- Stable home: `development/standards/flows.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/spec.md — 2026-11-17

- Archive: `development/wiki/archive/old/browsy/spec.md`
- Stable home: `development/standards/flows.md`
- Status: summarised in the stable page; no open decision is recorded here.

### proposals/frontend-wizy.md — 2026-11-19

- Archive: `development/wiki/archive/old/proposals/frontend-wizy.md`
- Stable home: `development/standards/flows.md`
- Status: summarised in the stable page; no open decision is recorded here.

### questy-proposals.md — 2026-11-15

- Archive: `development/wiki/archive/old/questy-proposals.md`
- Stable home: `development/standards/flows.md`
- Status: summarised in the stable page; no open decision is recorded here.

### standards.md — 2026-08-01

- Archive: `development/wiki/archive/old/standards.md`
- Stable home: `development/standards/flows.md`
- Status: summarised in the stable page; no open decision is recorded here.
