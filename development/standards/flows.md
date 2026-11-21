<!-- CONTEXT:BEGIN
schema: flove-page/1
id: ai/flows
path: development/standards/flows.md
trunk: ai
topic: flows
kind: topic
status: stable
html_place: ["#ai-note-wizy"]
owns: ["Wizy derivation", "use cases"]
updated: 2026-11-21
read_next: ["#wizy-and-derivation","#wizy-operating-areas","#measured-flow","#html-qa","#compiled-summary","#general-magic","#near-me","#translation-audit","#web-conformance","#stage-polish","#basic-wizy","#agent-block","#wizy-browsy","#wizy-browsy-plan"]
supersedes:
  - development/wiki/archive/old/UseCase-adv.md
  - development/wiki/archive/old/browsy/browsy-questions.md
  - development/wiki/archive/old/browsy/rationale.md
  - development/wiki/archive/old/browsy/spec.md
  - development/wiki/archive/old/proposals/frontend-wizy.md
  - development/wiki/archive/old/questy-proposals.md
  - development/wiki/archive/old/standards.md
heavy: false
CONTEXT:END -->

# Flows

> **Migrated 2026-11-21.** This page imports `browsy/spec.md` §3.5.

## Wizy and derivation

> Source: `development/wiki/archive/old/browsy/spec.md#35-wizy-and-derivation` (archived 2026-11-21).

Wizy supports the D options already tabled: D0 none, D1 deterministic rules,
D2 on-device model, D3 remote de-identified, D4 remote encrypted (future),
D5 peer-assisted. Others-view options: O0 signed projection (default), O1
recomputation under grant (opt-in), O2 social comparison (S only, later).

Defaults: D0/D1 local; D2 optional; D3 per-request consent; D4/D5 later; O0.

## Work

13 hitos · 86 tasks · 12 open · 1 closed. This page owns the `ai/flows`
chapter.

## Wizy operating areas

The Wizy operating-areas draft, custom-magic contract and open questions are
owned by [`plans/ai/flows.md#wizy-operating-areas`](../wiki/plans/ai/flows.md#wizy-operating-areas).

<a id="measured-flow"></a>
## Measured private ↔ public flow

> Owner: flows. One measured path from private input to public output; the
> boundary is explicit.

<a id="html-qa"></a>
## HTML Q&A form

> Owner: flows. Question batches, live preview and export from one self-contained
> page.

<a id="compiled-summary"></a>
## Compiled-summary convention

> Owner: flows. The form compiles to one summary shape with a fixed order.

<a id="general-magic"></a>
## General Magic vs Custom

> Owner: flows. The default magic action and the custom action are distinguished;
> no third path.

<a id="near-me"></a>
## Near me / unlike me

> Owner: flows. Comparisons show proximity without numeric scores.

<a id="translation-audit"></a>
## Base and strip audit

> Owner: flows. A translated page keeps its base and strips only the language
> layer.

<a id="web-conformance"></a>
## Web conformance gate

> Owner: flows. A page passes the conformance gate before publishing.

<a id="stage-polish"></a>
## Stage-based polish

> Owner: flows. One file is polished by the stages it needs, without rework.

<a id="basic-wizy"></a>
## Basic Wizy

> Owner: flows. Wizy reads local data, derives and explains; no network by default.

<a id="agent-block"></a>
## Exported prompts / floveAgentBlock

> Owner: flows. An exported prompt carries one `floveAgentBlock` with owner and
> scope.

<a id="wizy-browsy"></a>
## Wizy and Browsy flows

> Owner: flows. The Wizy/Browsy handoff is one flow with explicit consent.

<a id="wizy-browsy-plan"></a>
## Wizy–Browsy plan

> Owner: flows. The plan names the phases, owner and acceptance for the
> Wizy/Browsy integration.

## Sources

- `development/wiki/archive/old/browsy/spec.md` §3.5.
- `development/wiki/archive/old/browsy/rationale.md`.
- `development/wiki/archive/old/proposals/frontend-wizy.md`.

## Source map

| Archived source | Date | Stable home |
|---|---|---|
| `archive/old/UseCase-adv.md` | 2026-08-01 | development/standards/flows.md |
| `archive/old/browsy/browsy-questions.md` | 2026-08-01 | development/standards/flows.md |
| `archive/old/browsy/rationale.md` | 2026-11-17 | development/standards/flows.md |
| `archive/old/browsy/spec.md` | 2026-11-17 | development/standards/flows.md |
| `archive/old/proposals/frontend-wizy.md` | 2026-11-19 | development/standards/flows.md |
| `archive/old/questy-proposals.md` | 2026-11-15 | development/standards/flows.md |
| `archive/old/standards.md` | 2026-08-01 | development/standards/flows.md |

Chapters without a separate source row are `milestone-only`: they are
specified from the register (hitos and tasks) and remain owned here.
