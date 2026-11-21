<!-- CONTEXT:BEGIN
schema: flove-page/1
id: docs/plan
path: development/standards/plan.md
trunk: docs
topic: plan
kind: topic
status: stable
html_place: ["#plan-maps"]
owns: ["Plan map", "roadmap", "stage aliases"]
updated: 2026-11-21
read_next: ["#purpose-and-method","#source-of-truth-hierarchy","#development-plan","#backend-context","#distro-milestones","#rationale","#historical-graph","#sd-matrix","#browsy-nety-gate","#subject-consent","#plan-map","#editorial-plan","#browsy-spec","#distro-strategy"]
supersedes:
  - development/wiki/archive/old/apps/README.md
  - development/wiki/archive/old/browsy/pre-build/README.md
  - development/wiki/archive/old/browsy/rationale.md
  - development/wiki/archive/old/browsy/spec.md
  - development/wiki/archive/old/plans/2026-06-18-nety-frontend-build.md
  - development/wiki/archive/old/plans/2026-11-17-appy-authy-mynet.md
  - development/wiki/archive/old/plans/2026-11-20-appy-dashboard-redesign.md
  - development/wiki/archive/old/plans/2026-11-21-app-database-stages.md
  - development/wiki/archive/old/plans/index.md
  - development/wiki/archive/old/proposals.md
  - development/wiki/archive/old/roadmap-2026-06.md
  - development/wiki/archive/old/root/backend.md
  - development/wiki/archive/old/root/worldview.md
heavy: false
CONTEXT:END -->

# Plan

> **Pilot migration (phase 2).** This page imports `browsy/spec.md` §1, §2 and
> the §6 phase summary. Reconciliation detail, full phases and changelog live in
> the child plan `plans/docs/plan.md`.

## Purpose and method

> Source: `development/wiki/archive/old/browsy/spec.md#1-purpose-and-method` (archived 2026-11-21).

The project accumulated several browsy/nety plans written at different times,
with different assumptions about Central, trust, permissions and Wizy. This
document is the **spec-first source of truth**: requirements are named,
implementation work references those names, and acceptance is tested against
them.

Rules:

1. A behaviour is not “implemented” until its requirement ID has an acceptance
   check in §7.
2. Old plans are not deleted; they are marked historical or partially
   superseded, with the exact sections that still apply.
3. A task without a requirement ID is either a chore or a new requirement; add
   it to the table first.
4. UI copy and diagrams must use the same vocabulary as this spec
   (Browsy, Authy, Wizy, MyNet, MyFamily, Nety, Personal, Local, Social).
5. Unresolved work goes to `browsy-questions.md`, not into silent assumptions.

## Source-of-truth hierarchy

> Source: `development/wiki/archive/old/browsy/spec.md#2-source-of-truth-hierarchy` (archived 2026-11-21).

| Level | Artifact | Owns |
|---|---|---|
| 1 | This plan | behaviour, boundaries, acceptance |
| 2 | `rationale.md` | rationale, sketches, alternatives |
| 3 | `apps/sys/authy/index.html` | Authy levels, claim demo, persistence/keepers |
| 4 | `apps/sys/browsy/index.html` | Browsy use cases and model diagrams |
| 5 | `development/addons/media/apps/logos/{authy,browsy,central}/*` | canonical visual masters + rendered threads |
| 6 | `browsy-questions.md` | unresolved questions for the next questy survey |

Anything below level 2 that contradicts levels 1–2 is a documentation bug.

## Development plan

> Source: `development/wiki/archive/old/browsy/spec.md#6-development-plan` (archived 2026-11-21).

| Phase | Spec | Gate | Status |
|---|---|---|---|
| 0 Spec consolidation | all | every old plan points here; no contradictory “current spec” | done (this migration) |
| 1 Authy foundation | BSP-I01–I04, A01 | reload survives; L3 publishes; tamper rejected | mostly built; schema/risa/ladder pending |
| 2 Wizy inside Browsy | BSP-A01, W01–02 | offline derive; no separate keys | shell |
| 3 MyFamily + flat groups | BSP-M02–M08, M12, M16, D01–02 | 7×5 + 5 percentages; flat groups; reload | bridge/class built; list/group pending |
| 4 Grants + projections | BSP-P01–02, M09, D01–02 | grant mismatch/expiry/rotation; consult scope | spec |
| 5 Local net transport | BSP-A02, P02, M08–09 | two instances; non-member rejected; no Nety | native host chosen |
| 6 Nety Social | BSP-N01, A02–03, M10–11 | S-only; toggle off; Public requires L3 | postponed |
| 7 Documents + map | BSP-U01–02 | vocabulary; links; render | pending |
| 8 Hardening + release | BSP-T01 + all | check-distro clean; Chrome+Firefox pass | pending |

Full phase tasks, gates and status text: `plans/docs/plan.md#development-plan`.

## Reconciliation and changelog

The old-plan reconciliation table and the changelog are owned by
`plans/docs/plan.md#old-plans-reconciliation` and `#changelog`.

## Work

20 hitos · 60 tasks · 8 open · 12 closed. This page owns the `docs/plan`
chapter; `docs/map` has no hitos/tasks and 13 evidence sources.

## Backend context

> Source: `development/wiki/archive/old/root/backend.md#0--executive-summary`,
> `#1--decisions-already-closed`, `#9--roadmap` (archived 2026-11-21).

**flove** is a local-first constellation of small client-side apps expressing a
relational worldview (“flow + love”). The plan turns it into a backed-by-the-
network experience **without breaking its local-first nature**.

Two principles drive every decision:

1. **Local-first.** Nothing leaves the user’s device unless they explicitly
   publish. Each app persists what you add; the summary is the source of truth
   you export “as you see it”; an **Update** button reconciles edits — no
   background polling.
2. **A corporate backend, plus portability.** flove’s corporate backend is
   **nety**; flove stays a portable semantic layer. A `Publisher` adapter also
   integrates external backends — **0asis** first, then ActivityPub / Matrix /
   Solid. 0asis is an add-on, not the corporate backend.

Closed decisions:

| # | Topic | Decision |
|---|---|---|
| 1.1 | Accounts | No registration to use; an account appears only when publishing |
| 1.2 | Puzzy protocol | Multi-dimensional, relational, polysemic annotation system on user-defined objects |
| 1.3 | Corporate backend | **nety** — flove’s own backend on the flovenet stack (Ed25519, trust graph, resources, GraphQL) |
| 1.7 | External integration | **0asis.net** (and later AP/Matrix/Solid) is an optional add-on via `Publisher`; not a runtime dependency |
| 4.1 | Element | A **puzzy object** OR a **person/bond** |
| 4.2 | Cross-app sharing | Common pool PLUS direct field-to-field cross-links |
| 4.3 | Common area priority | Semantic AI search → whole-matrix → graph → feed |
| 4.4 | Traceability | Only over **published** elements; local data never leaves the browser |
| 5.1 | Forms quick-win | Persist, export/import, cross-link, publish |
| 5.3 | Local persistence (F0) | Added items survive close/reopen; Reload/Reset start fresh; summary re-derives + Update; export what you see |
| 5.4 | Cross-link example | A `loves` act of type gift surfaces in a Market view; 0asis-Market is the demo |
| 6.1 | nety | Corporate backend: Ed25519 identity + keystore, reputation facets, trust graph, resources, GraphQL gateway |
| 6.1b | 0asis add-on | Identity, ssb-blobs storage, gossip federation, 40+ modules, public PUBs; opted in |
| 6.2 | AI strategy | nety ships **wizy** for search + suggestions; 0asis module 42 optional; local **MyWizy** is separate |
| 6.3 | Visibility | Private-first on nety; local until the user publishes |
| 6.4 | Thematic views | Messages (DM) and Forum (circles/tribes); 0asis can bridge SSB tribes/DM |
| 7 | Scope | flove is the portable semantic layer; nety is its corporate backend; 0asis/AP/Matrix/Solid are interchangeable demos |

Roadmap:

- **Shipped:** F0 JS distro (local persistence, Update, export); Appy profile;
  portrait JSON + Save HTML + shared renderer; routing backbone.
- **Active:** Central (FastAPI + Turso); Browsy spec; Authy → MyNet.
- **Deferred:** nety backend (F2–F4) and external-platform integration (0asis).

## Distro milestones

> Source: `development/wiki/archive/old/apps/README.md#milestones` (archived 2026-11-21).

- **2026-11-09 — `apps/` + `tools/`:** the old `solo/` folder mixed apps and
  machinery and carried a nested forwarder. Now `apps/` holds every app, `tools/`
  the machinery, shared artwork lives in `development/addons/media/`, and
  `sw.js`, `.well-known/assetlinks.json` and `404.html` sit at the root. The
  package was renamed `flove-localhost.zip`. No folder is called `solo`.
- **2026-11-08 — one root, no link rewriting:** before this, the site had three
  roots and `sed`-rewrote links. Now there is one canonical root in every run
  mode; a link is written once, relative, and never rewritten at build time.

## Rationale

The full privacy-first rationale, diagrams, threat model and open decisions are
owned by [`plans/docs/plan.md#rationale`](../wiki/plans/docs/plan.md#rationale).
The stable pages carry the accepted facts; this link is the evidence trail.

<a id="historical-graph"></a>
## Historical decision graph

> Owner: plan. Every historical decision points to its current authority; the
> graph is navigable and no decision is orphaned.

<a id="sd-matrix"></a>
## SD01–SD19 decision matrix

> Owner: plan. The standards decisions have one current state; historical rows
> point to the live answer.

<a id="browsy-nety-gate"></a>
## Browsy/Nety UI gate

> Owner: plan. No Browsy/Nety UI is implemented until the local slice is defined
> and the bridge is signed off.

<a id="subject-consent"></a>
## Subject consent (O30)

> Owner: plan. Sharing a third person’s record requires the subject-consent
> decision; no silent L/S share.

<a id="plan-map"></a>
## Plan map and roadmap

> Owner: plan. One reading map of plans and phases; no duplicate rows.

<a id="editorial-plan"></a>
## Editorial plan

> Owner: plan. One editorial sequence for the wiki; exceptions recorded.

<a id="browsy-spec"></a>
## Browsy specification

> Owner: plan. The Browsy spec phases and acceptance are the canonical plan.

<a id="distro-strategy"></a>
## Distro and release strategy

> Owner: plan. SD18 branches and release gates are named and reachable.

## Sources

- `development/wiki/archive/old/browsy/spec.md` §1, §2, §6.
- `development/wiki/archive/old/plans/index.md`, `roadmap-2026-06.md`,
  `proposals.md`.
- `development/wiki/archive/old/root/backend.md`, `worldview.md`.

## Source map

| Archived source | Date | Stable home |
|---|---|---|
| `apps/README.md` | undated | development/standards/plan.md |
| `browsy/pre-build/README.md` | undated | development/standards/plan.md |
| `browsy/rationale.md` | undated | development/standards/plan.md |
| `browsy/spec.md` | undated | development/standards/plan.md |
| `plans/2026-06-18-nety-frontend-build.md` | 2026-06-18 | development/standards/plan.md |
| `plans/2026-11-17-appy-authy-mynet.md` | 2026-11-17 | development/standards/plan.md |
| `plans/2026-11-20-appy-dashboard-redesign.md` | 2026-11-20 | development/standards/plan.md |
| `plans/2026-11-21-app-database-stages.md` | 2026-11-21 | development/standards/plan.md |
| `plans/index.md` | undated | development/standards/plan.md |
| `proposals.md` | undated | development/standards/plan.md |
| `roadmap-2026-06.md` | undated | development/standards/plan.md |
| `root/backend.md` | undated | development/standards/plan.md |
| `root/worldview.md` | undated | development/standards/plan.md |

Chapters without a separate source row are `milestone-only`: they are
specified from the register (hitos and tasks) and remain owned here.
