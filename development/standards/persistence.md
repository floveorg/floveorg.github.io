# flove · Strategic Persistence Plan

> Ephemerall standard meets real-world persistence needs.
> Flove as case study for persistence parameters.

## Ephemerall Standard (SD09)

**Core rule:** Survive close, reload resets.

But "reload resets" needs nuance — some data MUST persist (identity, settings), some SHOULD be ephemeral (session state), some CAN go either way (app data).

## Persistence Tiers

| Tier | Survives | Resets on | Example |
|------|----------|-----------|---------|
| **P0: Permanent** | Everything | Manual delete only | Identity, settings, trust scores |
| **P1: Session** | Tab close | Browser restart | Current mask, active tab |
| **P2: Ephemeral** | Nothing | Reload | Selections, drafts, UI state |

## Flove Case Study: App Persistence Matrix

| App | P0 (Permanent) | P1 (Session) | P2 (Ephemeral) |
|-----|----------------|--------------|----------------|
| **blogy** | Read list, ratings | Current article | Scroll position |
| **souls** | Soul profile, connections | Active soul | Selection state |
| **goddy** | Published items, drafts | Current draft | Form inputs |
| **inventary** | Inventory items | Current item | Filter state |
| **myfamily** | Family tree, members | Active member | View mode |
| **keys** | Key pairs, vault | Current key | Search query |
| **browsy** | Trust scores, web of trust (3 hops, 100 users LRU) | Active mask | Panel state |
| **nety** | Profile, circles, trust | Active circle | Feed position |

## Storage Mechanisms

| Mechanism | Limit | Use for | Flove apps |
|-----------|-------|---------|------------|
| **localStorage** | 5-10MB | P0 settings, simple data | All apps |
| **sessionStorage** | 5-10MB | P1 session state | blogy only (not browsy) |
| **IndexedDB** | 50-200MB | P0 complex data, P1 large state | nety (circles) only |
| **Cache API** | Varies | Offline app copies | browsy (fallback) |
| **Extension storage** | 10MB (MV3) | All browsy data (unified) | browsy only |

## Persistence Parameters

### Size Budgets

| Data Type | Max Size | Eviction | Storage |
|-----------|----------|----------|---------|
| **User profile** | 10KB | Never | Extension storage |
| **Trust scores** | 100KB | LRU | Extension storage |
| **Web of trust** | 1.5MB | LRU (3 hops, 100 users + CRDT overhead) | Extension storage |
| **App data** | 10MB | App-defined | localStorage/IndexedDB |
| **Offline apps** | 50MB | LRU | Cache API |
| **Extension core** | 10MB (MV3) | User-managed | Extension storage |

### Eviction Policies

| Policy | When to use | Flove apps |
|--------|-------------|------------|
| **LRU** | Trust data, web of trust | browsy |
| **Time-based** | Session state | blogy |
| **Size-based** | Offline cache | browsy |
| **Never** | Identity, settings, trust scores | All apps |
| **User-managed** | Large data | browsy (10MB extension quota) |

### Compression

| Type | Method | Reduction | Use for |
|------|--------|-----------|---------|
| **JSON** | gzip | ~70% | Trust data, profiles |
| **Delta** | Only changes | Significant | Frequent updates (trust sync) |
| **CRDT metadata** | Vector clocks | ~20% overhead | Trust vouch entries |
| **Binary** | Array buffers | ~50% | Media, large blobs |

## Central Persistence

| Layer | Storage | Persistence | Notes |
|-------|---------|-------------|-------|
| **User data** | Turso (libSQL) | Permanent | `app_data` table |
| **User config** | Turso (libSQL) | Permanent | `user_config` table |
| **Trust data** | Turso (libSQL) | Permanent | CRDT-merged vouches, delta-synced |
| **Pending sync** | IndexedDB | Session | Ordered log of pending operations |
| **Cache** | localStorage | Session | `central=available` flag |

### Conflict Resolution Model
- **Trust data:** CRDT-style merge (vector clocks, client-side in browsy). Server stores merged result.
- **Profile/app data:** Last-write-wins by client timestamp.
- **Schema validation:** Server rejects malformed data against `collect-schemas.json` (per-app, required fields + types).

## Browsy Persistence

All browsy data uses Extension storage (`chrome.storage.local`) — unified, persistent, synchronous API, 10MB quota in MV3.

| Layer | Storage | Persistence | Notes |
|-------|---------|-------------|-------|
| **Trust scores** | Extension storage | Permanent | LRU, 100 users max |
| **Web of trust** | Extension storage | Permanent | 3 hops, LRU, ~1.2MB working set |
| **Profiles** | Extension storage | Permanent | JSON-LD generated locally |
| **Webhook configs** | Extension storage | Permanent | User-configurable |
| **Export history** | Extension storage | Session | Last 10 exports |
| **Panel state** | Extension storage | Session | Current view |

### Migration from IndexedDB (one-time)
On first update after unified storage lands:
1. Read all keys from IndexedDB (trust, profiles)
2. Write to Extension storage
3. Remove old IndexedDB entries
4. Set `flove:storage-migrated=v1` flag
5. If migration fails: keep IndexedDB, log error, retry next load

## Implementation Rules

### Rule 1: P0 data must have export/import
Every P0 data type must support export (JSON download) and import (file upload or webhook).

### Rule 2: P1 data must have defaults
Every P1 data must have sensible defaults if missing (no "undefined" states).

### Rule 3: P2 data must be optional
P2 data is nice-to-have, never required for core functionality.

### Rule 4: Size limits must be enforced
Check before writing. Show warning at 80%. Evict at 100%.

### Rule 5: Compression for large data
Any data >10KB should be compressed before storage.

## Migration Strategy

When persistence format changes (CC05: version-check on load):

1. Check `flove:version` in localStorage
2. If version mismatch, run migration script
3. Migration scripts are pure functions: `(oldData) => newData`
4. Store new version after successful migration
5. Never delete old data until migration confirmed

## Flove-Specific Patterns

### The `flove:` namespace
All flove localStorage keys use `flove:` prefix:
- `flove:lang` — language setting (app-agnostic)
- `flove:theme` — theme setting (app-agnostic)
- `flove:pending-sync` — Central sync flag
- `flove:<app>:*` — app-specific data
- `flove:version` — schema version

### The `collect()` contract
Apps define `window.flove.collect()` to specify what data to sync to Central. This is the boundary between P0 (synced) and P2 (local only).

### The ephemerall reset
On "reload resets", apps should:
1. Clear P2 data
2. Reset P1 data to defaults
3. Preserve P0 data
4. Show onboarding if first visit
