<!-- CONTEXT:BEGIN
schema: flove-page/1
id: backend/storage
path: development/standards/storage.md
trunk: backend
topic: storage
kind: topic
status: stable
html_place: ["#data-database"]
owns: ["Storage", "Web-of-Trust budget", "persistence"]
updated: 2026-11-21
read_next: ["#strategic-persistence","#web-of-trust-persistence-budget","#central-persistence","#database-stages","#identity-keys","#trust-sync","#messages-table","#storage-key-model","#mirrors-recovery"]
supersedes:
  - development/wiki/archive/old/plans/2026-11-17-appy-authy-mynet.md
  - development/wiki/archive/old/plans/2026-11-21-app-database-stages.md
  - development/wiki/archive/old/plans/central-backend.md
  - development/wiki/archive/old/root/adoption.md
  - development/wiki/archive/old/root/backend.md
heavy: false
CONTEXT:END -->

# Storage

> **Pilot migration (phase 2).** This page imports `backend.md` §10.

## Strategic persistence

> Source: `development/wiki/archive/old/root/backend.md#10--strategic-persistence` (archived 2026-11-21).

The Ephemerall rule: **survive close, reload resets**. Data divides into three
tiers; the enforceable minimum is `frontend/frontend.md` §13.18.

| Tier | Survives | Resets on | Holds |
|---|---|---|---|
| **P0 permanent** | everything | manual delete | identity, settings, trust scores |
| **P1 session** | tab close | browser restart | active tab, current mask |
| **P2 ephemeral** | — | reload | selections, drafts, UI state |

Storage: `localStorage` for P0 and small data (5–10 MB), IndexedDB for larger
records and offline queues, `chrome.storage` in Browsy, Turso in Central.

Rules: one explicit key per record; version the payload; reset clears P2 and
leaves P0; export before a migration; a failed write falls back to memory and
says so.

## Work

8 hitos · 37 tasks · 5 open · 3 closed. This page owns the `backend/storage`
chapter.

## Web of Trust persistence budget

> Source: `development/wiki/archive/old/root/adoption.md#web-of-trust-persistence-budget` (archived 2026-11-21).

| Parameter | Value | Notes |
|---|---|---|
| **Hop depth** | 3 hops | Full network (~1 MB) |
| **Max users** | 100 | ~20 KB storage |
| **Compression** | JSON | ~70% reduction with gzip |
| **Eviction** | LRU | Least recently used |

Trust visibility: first circle, second circle, social groups, public.

## Central persistence

> Source: `development/wiki/archive/old/plans/central-backend.md#architecture` (archived 2026-11-21).

Central stores the full `window.flove.collect()` JSON in `app_data` indexed by
`(app, user)`, with cursor-based list pagination and an IndexedDB pending-sync
queue on the client. Non-trust data is last-write-wins; trust data merges with
vector clocks. Full schema, endpoints and migration path:
[`plans/backend/systems.md#architecture`](../wiki/plans/backend/systems.md#architecture).

## Database stages

> Source: `development/wiki/archive/old/plans/2026-11-21-app-database-stages.md#2--the-five-stages` (archived 2026-11-21).

The app-data ladder uses the canonical stage words; it does not move Work hitos.

| Stage | Name | What holds | Writer |
|---|---|---|---|
| `seed` | Local | `localStorage` + JSON in git + SW precache | the app itself |
| `infant` | Bridge | optional `flove.json` enrichment + hosted SQLite replica | hosted replica |
| `mature` | Local backend | `rusqlite` + FTS5, derived slices, SHA gate, event log | local node |
| `grown` | Local sys services | typed local services, no cloud; `rusqlite` writer | local gateway |
| `full` | Federated mesh | several nodes, no central authority | each node |

Boundary: the database holds app data and the sys apps that serve apps; it holds
no development hitos/tasks, `milestones.json`, `common.json`, `development/**`,
`whole/` or `docs/**`. The living plan and its task tables are in the archived
`2026-11-21-app-database-stages.md`; the register owns the tasks.

<a id="identity-keys"></a>
## Identity keys and migration

> Owner: storage. Ed25519 → CIDv1 PeerId; an old vault upgrades without losing
> the peer id and carries a `legacy:true` marker.

<a id="trust-sync"></a>
## Trust sync and offline queue

> Owner: storage. Delta-only sync with replay order; an offline write merges
> without overwriting newer trust data.

<a id="messages-table"></a>
## Messages table

> Owner: storage. One stanza → one `messages` row; survives reload with the node
> off through the seed fallback; matches `schemas-11` with no new envelope.

<a id="storage-key-model"></a>
## Storage and key model

> Owner: storage. Schemas, vault and key namespaces use the `flove-authy/1`
> namespace without collision.

<a id="mirrors-recovery"></a>
## Mirrors and recovery

> Owner: storage. Backup mirrors, checksums and the restore drill; the standards
> index names the homes for storage and schema detail.

## Sources

- `development/wiki/archive/old/root/backend.md` §10.
- `development/wiki/archive/old/root/adoption.md` Web-of-Trust budget.
- `development/wiki/archive/old/plans/2026-11-21-app-database-stages.md`.

## Source map

| Archived source | Date | Stable home |
|---|---|---|
| `plans/2026-11-17-appy-authy-mynet.md` | 2026-11-17 | development/standards/storage.md |
| `plans/2026-11-21-app-database-stages.md` | 2026-11-21 | development/standards/storage.md |
| `plans/central-backend.md` | undated | development/standards/storage.md |
| `root/adoption.md` | undated | development/standards/storage.md |
| `root/backend.md` | undated | development/standards/storage.md |

Chapters without a separate source row are `milestone-only`: they are
specified from the register (hitos and tasks) and remain owned here.
