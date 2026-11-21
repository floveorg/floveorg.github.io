# Level detail

## Extra modules (any level)

docs/help, tests/QA, PWA/install, share/OG card, print/export, migration.

## Bug probes (levels 1–3)

These are technical checks on the file, not flove-standard rows.

### Level 1 — artifact and selector

Delegated to `validaty` step 2, so run them inside the Clean stage:

- **Artifact probe** — extract local paths from `href`, `src`, `fetch()`, audio
  bases and cited comment paths; check each exists relative to the repo. A
  missing asset, generated-only JSON or renamed route is a bug, not a note.
- **Selector probe** — confirm balanced CSS braces and that every selector list
  ends in a block (no trailing comma); verify language-specific width and
  animation overrides survived the parse. No selector may be load-bearing and
  silently dropped.

### Level 3 — improving probes

- **Motion/state** — reduced-motion must keep the same semantic state as the
  animated one (the right actor, staged reveals), and hidden rails must stay
  keyboard reachable.
- **Timing** — one owner for navigation timers; `requestAnimationFrame` fades
  must reach their end state when the tab is backgrounded; failure paths must
  clear blocking veils.
- **Feedback** — clipboard success only after the promise resolves; late async
  data must repaint every derived UI (URL text, QR), not only its state.

## Flove standards sweep (level 4 only)

`code-review` checks the file; this sweep checks the **single source** of the
flove standards behind it. Read the canonical degree matrix in
`development/index.html` (`degStats` / `degGroups`) — never a copied table — and
enumerate every card (six axes) × degree 1–5 and every milestone group by
subsection. Score each group with the flove rule
`round(100 * (done + 0.5 * part) / total)`: **closed means 100 %**; otherwise
report `done / part / total`, the exact percentage and the failing IDs with
their Done-when and owner evidence.

- **Claim probe** — for each card/group, confirm the file actually implements
  the state the milestone claims; prose alone never closes a row.

Report the sweep as a ledger beside the stage ledgers: per card and per group
`pct`, `closed` or `gap`, with the IDs. This adds no ladder and changes no
canonical row — it only measures and reports.

## Usability (levels 3–5)

Read [§13.18](https://flove.org/development/standards/frontend/frontend.md#1318--usability-levels--3-minimum--4-function--5-craft)
and [`contract.md#the-floor`](https://flove.org/development/standards/contract.md#the-floor)
before judging. Level 3 marks every applicable row **present / missing / N/A**;
a missing minimum fails. Level 4 implements the concrete level-4 features;
level 5 the level-5 ones.

Shell rows: menu (§13.5), tour (§13.6), metadata (§13.10 + head / Open Graph /
`flove-fields`) and stats (§13.17). Audit every section the same way; report
gaps, never redesign.
