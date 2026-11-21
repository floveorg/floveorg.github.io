<!-- CONTEXT:BEGIN
schema: flove-page/1
id: ai/models
path: development/standards/models.md
trunk: ai
topic: models
kind: topic
status: stable
html_place: ["#ai"]
owns: ["Models", "AI levels"]
updated: 2026-11-21
read_next: ["#model-selection","#inference-cache","#mywizy","#local-model","#d0d1","#agent-plan","#depth-ladder","#compute-plan","#advanced-use"]
supersedes:
  - development/wiki/archive/old/UseCase-adv.md
  - development/wiki/archive/old/browsy/spec.md
  - development/wiki/archive/old/proposals/frontend-wizy.md
  - development/wiki/archive/old/root/adoption.md
  - development/wiki/archive/old/root/backend.md
  - development/wiki/archive/old/roadmap-2026-06.md
heavy: false
CONTEXT:END -->

# Models

> **Stable page.** Migrated from the pre-cutover sources on 2026-11-21.
> The chapters below are the only owners; the child plan records source history.


<a id="model-selection"></a>
## Model selection

> Owner: models. One model per task class with cost and latency noted; no model
> is chosen twice for the same task.

<a id="inference-cache"></a>
## Inference cache

> Owner: models. Cached outputs carry an expiry and invalidation rule; a cache
> hit is distinguishable from a fresh inference.

<a id="mywizy"></a>
## MyWizy

> Owner: models. Local AI over own and imported summaries; no network by default.

<a id="local-model"></a>
## Local model

> Owner: models. A local model runs without a backend; the fallback path is
> explicit.

<a id="d0d1"></a>
## D0/D1 local defaults

> Owner: models. D0 none and D1 deterministic rules are local; D3 needs
> per-request consent.

<a id="agent-plan"></a>
## Agent prompts and model plan

> Owner: models. One prompt/model row per agent with owner and fallback.

<a id="depth-ladder"></a>
## Data-depth ladder

> Owner: models. The five depth levels apply to AI outputs with no overlapping
> definition.

<a id="compute-plan"></a>
## AI compute plan

> Owner: models. Compute location and cost per task class; no hidden remote
> call.

<a id="advanced-use"></a>
## Advanced-use standard

> Owner: models. Advanced use names its inputs, depth and consent; no new model
> is implied.

## Three distinct AIs

> Source: `development/wiki/archive/old/roadmap-2026-06.md` (archived 2026-11-21).

- **`MyWizy`** (F1) — the local, per-user finetuner over your own and imported
  summary JSONs. It never fetches a corpus without an explicit action.
- **`wizy`** (F4) — Athenea's global AI over the community corpus, trained with
  `whole` and puzzy seeds.
- **module 42** — 0asis's AI, usable only as an optional engine for `wizy` when
  the 0asis add-on is installed.

Do not conflate the three: local enrichment (`MyWizy`), corporate community AI
(`wizy`) and the optional 0asis engine (module 42) have different data scopes.

## Compute tiers

| Tier | Where it runs | What it does |
|---|---|---|
| `archive/old/roadmap-2026-06.md` | 2026-11-19 | development/standards/models.md |
| F0 · `mini` / `minifull` | JS distro, fully offline | local persistence, summary, Update and export |
| F1 · `basic` + `MyWizy` | JS distro, opt-in network | local AI insights, on-demand reference pulls |
| F4 · `wizy` | nety (corporate) | global AI over the community corpus |
| F5 · puzzy engine | nety (corporate) | multi-axis ratings, consensus and trajectories |

## Source map

| Archived source | Date | Stable home |
|---|---|---|
| `archive/old/UseCase-adv.md` | 2026-08-01 | development/standards/models.md |
| `archive/old/browsy/spec.md` | 2026-11-17 | development/standards/models.md |
| `archive/old/proposals/frontend-wizy.md` | 2026-11-19 | development/standards/models.md |
| `archive/old/root/adoption.md` | 2026-08-01 | development/standards/models.md |
| `archive/old/root/backend.md` | 2026-08-01 | development/standards/models.md |

Chapters without a separate source row are `milestone-only`: they are
specified from the register (hitos and tasks) and remain owned here.
