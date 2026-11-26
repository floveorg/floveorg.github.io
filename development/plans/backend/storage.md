---
status: stable
section: backend/storage
created: 2026-11-21
also: []
---

# backend/storage plan

> **Child plan.** The stable page owns the facts; this file records the dated
> source history and open plan decisions. Updated 2026-11-21.

## Source index

### plans/2026-11-17-appy-authy-mynet.md — 2026-11-17

- Archive: `development/archive/old/plans/2026-11-17-appy-authy-mynet.md`
- Stable home: `development/standards/backend/storage/storage.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/2026-11-21-app-database-stages.md — 2026-11-21

- Archive: `development/archive/old/plans/2026-11-21-app-database-stages.md`
- Stable home: `development/standards/backend/storage/storage.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/central-backend.md — 2026-08-01

- Archive: `development/archive/old/plans/central-backend.md`
- Stable home: `development/standards/backend/storage/storage.md`
- Status: summarised in the stable page; no open decision is recorded here.

### root/adoption.md — 2026-08-01

- Archive: `development/archive/old/root/adoption.md`
- Stable home: `development/standards/backend/storage/storage.md`
- Status: summarised in the stable page; no open decision is recorded here.

### root/backend.md — 2026-08-01

- Archive: `development/archive/old/root/backend.md`
- Stable home: `development/standards/backend/storage/storage.md`
- Status: summarised in the stable page; no open decision is recorded here.

<a id="storage-v2-01"></a>

## storage-v2-01 — V2 storage contract and migration boundary

- Status: seed / todo
- Section: `backend/storage/v2-solo`
- Depends on: `storage-03`
- Standard: `development/standards/backend/storage/storage.md`
- Deliverable: V2 storage contract and V1->V2 migration boundary as the single authority at `development/standards/backend/storage/storage.md`.
- Done when: the V2 record envelope, migration rules, and backup/export/import contract are named and one V1 fixture path is verified.
- Decision: who owns the V2 migration boundary and compatibility window.

Core tasks:
1. Define V2 storage contract/migration boundary from V1.
2. Register V2 entry points in Plans/Work and storage presentation.
