<!-- CONTEXT:BEGIN
schema: flove-page/1
id: backend/systems
path: development/standards/systems.md
trunk: backend
topic: systems
kind: topic
status: stable
html_place: ["#p2p"]
owns: ["Architecture", "bridge", "permissions"]
updated: 2026-11-21
read_next: ["#sys-systems-04", "#sys-systems-05", "#sys-systems-06", "#sys-systems-07", "#sys-systems-08", "#sys-systems-10", "#sys-systems-11", "#sys-contracts-03", "#sys-systems-12", "#sys-systems-13", "#sys-contracts-05", "#sys-systems-14", "#sys-systems-15", "#sys-contracts-07", "#sys-contracts-08", "#sys-systems-16", "#sys-contracts-09", "#sys-contracts-10", "#sys-contracts-11", "#sys-systems-17", "#sys-systems-18", "#sys-contracts-12", "#sys-systems-19", "#sys-contracts-13", "#sys-systems-20", "#sys-systems-21", "#sys-contracts-14", "#sys-systems-22", "#sys-contracts-15", "#sys-systems-25", "#sys-systems-23", "#sys-contracts-16", "#sys-systems-24", "#sys-systems-26"]
supersedes:
  - development/wiki/archive/old/apps/README.md
  - development/wiki/archive/old/bridges/oasis.md
  - development/wiki/archive/old/browsy/README.md
  - development/wiki/archive/old/browsy/TESTING.md
  - development/wiki/archive/old/browsy/browsy-questions.md
  - development/wiki/archive/old/browsy/port-nety.md
  - development/wiki/archive/old/browsy/pre-build/05-native-host.md
  - development/wiki/archive/old/browsy/pre-build/06-bridge-threat-model.md
  - development/wiki/archive/old/browsy/rationale.md
  - development/wiki/archive/old/browsy/spec.md
  - development/wiki/archive/old/plans/2026-11-17-appy-authy-mynet.md
  - development/wiki/archive/old/plans/2026-11-21-app-database-stages.md
  - development/wiki/archive/old/plans/central-backend.md
  - development/wiki/archive/old/reviews/2026-07-25-browsy-fastapi-libsql-performance-review.md
  - development/wiki/archive/old/root/adoption.md
  - development/wiki/archive/old/root/backend.md
  - development/wiki/archive/old/root/worldview.md
heavy: false
CONTEXT:END -->

# Systems

> **Pilot migration (phase 2).** This page imports `browsy/spec.md` §3.1, §3.6
> and §3.7. The rest of the systems source set is still pending.

## Architecture

> Source: `development/wiki/archive/old/browsy/spec.md#31-architecture` (archived 2026-11-21).

- **Browsy is the host.** It runs as a browser extension (MV3 + Firefox
  polyfill) and contains Authy and Wizy. Wizy is not a separate network client
  and does not own a key store.
- **Authy is the identity module inside Browsy.** It owns the root identity,
  channel proofs, levels, sessions, recovery, and the signing of bundles and
  grants.
- **Wizy is the JSON manager inside Browsy.** It reads the vault, merges
  Personal + Local + Social data, derives D, builds projections, and explains
  its results. It reaches the local net and Nety social only through Browsy’s
  two explicit toggles.
- **Nety carries the Social layer only.** It stores/distributes public or
  group-visible bundles and supplies reputation/WoT for ranking. It is not the
  permission authority and never receives Local or Personal plaintext.
- **Localhost and the web author bundles.** Both use the same schema and sign
  through Authy; neither is a second runtime identity.
- **Central is optional.** It may mirror public bundles; it is not required for
  the mesh and is not the authority for Local grants.
- **Browsy is a Nety client, not a Nety node.** The extension reaches Nety
  through the gateway/daemon over HTTPS/WebSocket; it never opens raw sockets
  or runs a DHT. Local transport is a separate lane (WebRTC or a native host)
  and never passes through Nety.

## Permissions and grants

> Source: `development/wiki/archive/old/browsy/spec.md#36-permissions-and-grants` (archived 2026-11-21).

- A grant is signed by Authy and travels with the bundle.
- Fields: grantor, grantee (key/circle/group), bundle, paths, capabilities
  (`view`, `derive`, `aggregate`; no implicit `copy`), expiry, content key,
  version, signature.
- Unit for v1: JSON path with array ranges. Field-level is a later refinement.
- Enforcement: Browsy on send/receive; Wizy on projection; apps never read the
  vault directly.
- P2P permission enforcement is a separate trunk; the current scope is local
  federation between Browsy instances.

## Interfaces

> Source: `development/wiki/archive/old/browsy/spec.md#37-interfaces-and-files` (archived 2026-11-21).

| Interface | Contract |
|---|---|
| `flove.authy.*` (proposed) | status, unlock, session, link, sign, rotate, recover |
| `floveMyFamily.*` | toRecord, save, setClass, list, groups, info |
| `floveBrowsy.saveRecord(payload)` | store a MyFamily L record |
| `floveBrowsy.listGroups()` / `createGroup(payload)` | read/create a local group and its projection |
| `floveBrowsy.addGroupMember(groupId, personId, role)` / `removeGroupMember(...)` | change membership; removal rotates the key |
| `floveBrowsy.listFeed({groupId?})` / `savePost(payload)` | signed L/S feed reads and writes |
| `floveBrowsy.createInvite(payload)` / `revokeInvite(code)` | local invite code and lineage |
| `floveBrowsy.createConsultAgreement(payload)` / `revokeConsult(id)` | owner→member Wizy consultation over selected data |
| `floveBrowsy.saveAuthy(payload)` | hand the signed Authy summary to the local keeper |
| `floveNety.publishAuthy(payload)` / `publishPost(payload)` | publish only S summaries/posts |

Schema envelopes (`flove:authy/1`, `flove-bundle/0.1`, `flove-group/0.1`,
`flove-consult/1`, `flove-identity/1`) are owned by
[`schemas.md#schema-envelopes`](schemas.md#schema-envelopes).

## Work

42 hitos · 250 tasks · 34 open · 8 closed. This page owns the `backend/contracts`
and `backend/systems` chapters.

## Backend strands (2026-08)

> Source: `development/wiki/archive/old/root/backend.md#2--architecture-overview` (archived 2026-11-21).

The current Browsy architecture is owned by [Architecture](#architecture). This
section records the three backend strands from the earlier overview:

| Backend | Layer | Role |
|---|---|---|
| **Central** (FastAPI + Turso) | network home | canonical data bank + frontend home; serverless on Railway, served through the GitHub Pages proxy |
| **Decentral (nety)** | P2P network | SQLite per peer; community side; separate repo |
| **Browsy** | navigation + identity | browser extension; fetches HTML from Central or solo fallback; identity/trust bridge |

Publishing is always a deliberate user act; local data is never auto-uploaded.
The corporate backend is nety; the Publisher adapter and 0asis are an
integration demo, not a runtime dependency.

## Element life cycle

> Source: `development/wiki/archive/old/root/backend.md#4--element-life-cycle` (archived 2026-11-21).

1. The user adds an item in an app (e.g. loves · gift).
2. The app persists it immediately to `localStorage` / IndexedDB.
3. The summary reflects it; on reload the summary re-derives from the store.
4. Editing an added item marks the summary stale; no polling.
5. **Update** re-derives from the store and clears stale.
6. **Export/Share** emits “what you see”.
7. Optional: publish to Appy, and opt-in publish to nety or a demo bridge.

No step uploads local data without an explicit publish.

## Generic webhook exports

> Source: `development/wiki/archive/old/root/adoption.md#generic-webhook-exports` (archived 2026-11-21).

Browsy and Central can export profile data to external services via generic webhooks.

| Parameter | Decision |
|---|---|
| **Storage** | Both (Browsy local + Central synced copy) |
| **Trigger** | Manual only (user clicks export) |
| **Auth** | User-configurable (supports all methods) |
| **Proxy** | Both (Browsy direct OR via Central) |

Export targets: GitHub repo, GitHub Pages, Gitea, custom URL, local file.

## Central backend plan

> Source: `development/wiki/archive/old/plans/central-backend.md` (archived 2026-11-21).

Central is the optional data bank and frontend host: FastAPI + Turso on Railway,
served through the GitHub Pages proxy at `flove.org/api/*`. The full decision
set (CB/D/E/G/CB_S), architecture, API, identity, trust sync, navigation and
conflicts is owned by
[`plans/backend/systems.md`](../wiki/plans/backend/systems.md#central-backend-plan).
This page keeps only the boundary: Central is optional, not the permission
authority; nety remains the corporate backend.

## Native host transport

> Source: `development/wiki/archive/old/browsy/pre-build/05-native-host.md` (archived 2026-11-21).

Decision: **native messaging host**, not browser WebRTC. MV3 cannot open raw
sockets or run mDNS; the host owns the local network. **Rust** host,
**WebSocket + JSON** for v1, signed release + version check.

The host does **not** own the vault. Authy keys and P data stay in the
extension; the host moves signed L bundles and group posts.

- **LAN discovery** (host): mDNS + manual `host:port`; no Telegram.
- **Invitation discovery** (Browsy UI): invite code + QR sent as a Telegram deep
  link; clicking can start Authy authentication. risa is a redirect to the Authy
  ID, not a separate root. Telegram is an invite/auth channel, not the LAN
  transport.

First message set: `hello`, `ready`, `pair.start`, `pair.accept`, `peers.list`,
`pull`, `push`, `revoke`, `status`; request/response uses an `id`; the host
executes no arbitrary commands.

Security: native-messaging manifest allows only the Browsy extension; pairing
uses one-time code + fingerprint; L frames are Authy-signed and verified;
the host never receives P plaintext or the root key; listener binds explicitly
(no `0.0.0.0` by default); nonce + timestamp + version replay protection; no
shell/exec surface; signed updates + version check.

MVP: pair, list peers, pull/push group posts and membership grants, revoke.
Open: signing key, relay queue for offline peers, deep-link replay protection.

## Bridge and threat model

> Source: `development/wiki/archive/old/browsy/pre-build/06-bridge-threat-model.md` (archived 2026-11-21).

The page is untrusted. The bridge exposes a small API; it never exposes the
vault, root key, P data or signing.

`window.flove.browsy` (MAIN world) → `postMessage` (origin-checked) → isolated
content script (allowlist + schema) → background service worker (vault +
policy) → IndexedDB / native host.

| Method | Returns | Page can write? |
|---|---|---|
| `status()` | `{hasIdentity, level, locked, identityHash?}` | no |
| `info()` | version + status | no |
| `saveRecord(record)` | `{id, class}` | **forces L** |
| `listRecords()` | only L/S records | no |
| `listGroups()` | group cards (name, member count, 5 bars) | no |
| `listFeed({groupId?})` | L posts | no |
| `savePost({groupId, body})` | L post | yes (L only) |
| `createInvite()` | `{code}` | yes (local) |

**Never exposed:** `sign`, `unlock`, `exportRoot`, `getKeypair`, raw P, vault,
keepers or arbitrary storage.

Rules: origin allowlist; check `event.source`/`event.origin`; schema validation;
page records forced L; P filtered from reads; rate limit + size cap; no `eval`
or remote code; logs redact bodies/hashes/keys.

Threats and mitigations: XSS/malicious localhost (L-only, origin, CSP, rate
limit), compromised content script (allowlist, schema, no secrets), forged/
replayed bundles (signature, grant, version, nonce), stolen device
(passphrase/Argon2id, lock, panic wipe), supply chain (signed builds, pinned
deps).

## Browsy references

The full Browsy README (architecture, decisions, file map), TESTING (risk
matrix, test plan) and port-nety (crypto/storage seams) are owned by
[`plans/backend/systems.md#browsy-readme`](../wiki/plans/backend/systems.md#browsy-readme).
They remain reference material for the Browsy/Authy/MyNet implementation.

The Oasis/0asis bridge and the Browsy + FastAPI + libSQL review are owned by
[`plans/backend/systems.md#oasis-bridge`](../wiki/plans/backend/systems.md#oasis-bridge)
and [`.md#performance-review`](../wiki/plans/backend/systems.md#performance-review).

<a id="sys-systems-04"></a>
## Inventory of app↔bridge contracts: producer, consumer and version

> Owner: systems. Canonical backend/contract item for `systems-04`; evidence lives in the register.

<a id="sys-systems-05"></a>
## Local service registry: name, version and health check

> Owner: systems. Canonical backend/contract item for `systems-05`; evidence lives in the register.

<a id="sys-systems-06"></a>
## Per-app isolation: process boundaries and communication channel

> Owner: systems. Canonical backend/contract item for `systems-06`; evidence lives in the register.

<a id="sys-systems-07"></a>
## Versioned Browsy bridge: envelopes, errors and negotiation

> Owner: systems. Canonical backend/contract item for `systems-07`; evidence lives in the register.

<a id="sys-systems-08"></a>
## End-to-end traces LocalHost↔cloud: correlation id and minimal fields

> Owner: systems. Canonical backend/contract item for `systems-08`; evidence lives in the register.

<a id="sys-systems-10"></a>
## Browsy host MV3: least privilege and exposed surface

> Owner: systems. Canonical backend/contract item for `systems-10`; evidence lives in the register.

<a id="sys-systems-11"></a>
## Browsy

> Owner: systems. Canonical backend/contract item for `systems-11`; evidence lives in the register.

<a id="sys-contracts-03"></a>
## FloveElement with universal classes: required fields and class rules

> Owner: systems. Canonical backend/contract item for `contracts-03`; evidence lives in the register.

<a id="sys-systems-12"></a>
## Nety Social only: Local/Nety boundary and what never crosses the gateway

> Owner: systems. Canonical backend/contract item for `systems-12`; evidence lives in the register.

<a id="sys-systems-13"></a>
## Nety

> Owner: systems. Canonical backend/contract item for `systems-13`; evidence lives in the register.

<a id="sys-contracts-05"></a>
## Per-app mapping.json to the Upper Ontology: rules and validation

> Owner: systems. Canonical backend/contract item for `contracts-05`; evidence lives in the register.

<a id="sys-systems-14"></a>
## F3 · common area with GraphQL: query contract and limits

> Owner: systems. Canonical backend/contract item for `systems-14`; evidence lives in the register.

<a id="sys-systems-15"></a>
## Class P/L/S: containment of P, public S and shareable L

> Owner: systems. Canonical backend/contract item for `systems-15`; evidence lives in the register.

<a id="sys-contracts-07"></a>
## Delete for everyone: tombstone, remote deletion and labelled copies

> Owner: systems. Canonical backend/contract item for `contracts-07`; evidence lives in the register.

<a id="sys-contracts-08"></a>
## Extraction from Browsy: DOM redaction and origin allowlist

> Owner: systems. Canonical backend/contract item for `contracts-08`; evidence lives in the register.

<a id="sys-systems-16"></a>
## lib/crypto.js, lib/store.js and lib/handler.js ports: seam contracts

> Owner: systems. Canonical backend/contract item for `systems-16`; evidence lives in the register.

<a id="sys-contracts-09"></a>
## Capability object and XSS boundary: scopes, TTL and user gesture

> Owner: systems. Canonical backend/contract item for `contracts-09`; evidence lives in the register.

<a id="sys-contracts-10"></a>
## Central CRUD API: HTTP contract, pagination and errors

> Owner: systems. Canonical backend/contract item for `contracts-10`; evidence lives in the register.

<a id="sys-contracts-11"></a>
## Versioned ping: version, features and bridge cache

> Owner: systems. Canonical backend/contract item for `contracts-11`; evidence lives in the register.

<a id="sys-systems-17"></a>
## Publishers: common interface and routed destinations

> Owner: systems. Canonical backend/contract item for `systems-17`; evidence lives in the register.

<a id="sys-systems-18"></a>
## Reputation: four facets and the trust graph

> Owner: systems. Canonical backend/contract item for `systems-18`; evidence lives in the register.

<a id="sys-contracts-12"></a>
## A01–A13: open questions live in browsy-questions §A

> Owner: systems. Canonical backend/contract item for `contracts-12`; evidence lives in the register.

<a id="sys-systems-19"></a>
## Implement Browsy specification in System apps

> Owner: systems. Canonical backend/contract item for `systems-19`; evidence lives in the register.

<a id="sys-contracts-13"></a>
## Implement the backend integration contract in Contracts

> Owner: systems. Canonical backend/contract item for `contracts-13`; evidence lives in the register.

<a id="sys-systems-20"></a>
## Implement the backend level ladder in System apps

> Owner: systems. Canonical backend/contract item for `systems-20`; evidence lives in the register.

<a id="sys-systems-21"></a>
## Contrast the historical Browsy map with the active spec

> Owner: systems. Canonical backend/contract item for `systems-21`; evidence lives in the register.

<a id="sys-contracts-14"></a>
## Pre-build contract index as the entry to all eleven pieces

> Owner: systems. Canonical backend/contract item for `contracts-14`; evidence lives in the register.

<a id="sys-systems-22"></a>
## Native messaging transport: boundary, format and fallback

> Owner: systems. Canonical backend/contract item for `systems-22`; evidence lives in the register.

<a id="sys-contracts-15"></a>
## Bridge threat model: assets, boundaries and mitigations

> Owner: systems. Canonical backend/contract item for `contracts-15`; evidence lives in the register.

<a id="sys-systems-25"></a>
## XMPP/Prosody :5222 bridge

> Owner: systems. Canonical backend/contract item for `systems-25`; evidence lives in the register.

<a id="sys-systems-23"></a>
## Execute backend roadmap in System apps

> Owner: systems. Canonical backend/contract item for `systems-23`; evidence lives in the register.

<a id="sys-contracts-16"></a>
## Execute puzzy standard in Contracts

> Owner: systems. Canonical backend/contract item for `contracts-16`; evidence lives in the register.

<a id="sys-systems-24"></a>
## Execute the architecture decision map in System apps

> Owner: systems. Canonical backend/contract item for `systems-24`; evidence lives in the register.

<a id="sys-systems-26"></a>
## Nety + Chatland federated over the portable profile

> Owner: systems. Canonical backend/contract item for `systems-26`; evidence lives in the register.

## Sources

- `development/wiki/archive/old/browsy/spec.md` §3.1, §3.6, §3.7.
- `development/wiki/archive/old/root/backend.md`, `adoption.md`, `worldview.md`.
- `development/wiki/archive/old/plans/central-backend.md`.

## Source map

| Archived source | Date | Stable home |
|---|---|---|
| `apps/README.md` | undated | development/standards/systems.md |
| `bridges/oasis.md` | undated | development/standards/systems.md |
| `browsy/README.md` | undated | development/standards/systems.md |
| `browsy/TESTING.md` | undated | development/standards/systems.md |
| `browsy/browsy-questions.md` | undated | development/standards/systems.md |
| `browsy/port-nety.md` | undated | development/standards/systems.md |
| `browsy/pre-build/05-native-host.md` | undated | development/standards/systems.md |
| `browsy/pre-build/06-bridge-threat-model.md` | undated | development/standards/systems.md |
| `browsy/rationale.md` | undated | development/standards/systems.md |
| `browsy/spec.md` | undated | development/standards/systems.md |
| `plans/2026-11-17-appy-authy-mynet.md` | 2026-11-17 | development/standards/systems.md |
| `plans/2026-11-21-app-database-stages.md` | 2026-11-21 | development/standards/systems.md |
| `plans/central-backend.md` | undated | development/standards/systems.md |
| `reviews/2026-07-25-browsy-fastapi-libsql-performance-review.md` | 2026-07-25 | development/standards/systems.md |
| `root/adoption.md` | undated | development/standards/systems.md |
| `root/backend.md` | undated | development/standards/systems.md |
| `root/worldview.md` | undated | development/standards/systems.md |

Chapters without a separate source row are `milestone-only`: they are
specified from the register (hitos and tasks) and remain owned here.
