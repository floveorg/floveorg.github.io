<!-- CONTEXT:BEGIN
schema: flove-page/1
id: community/channels
path: development/standards/channels.md
trunk: community
topic: channels
kind: topic
status: stable
html_place: ["#messenger"]
owns: ["Chatland", "messenger"]
updated: 2026-11-21
read_next: ["#chatland-cross-axis-hitos","#audience-map","#risa-lovy","#proposal-channel","#contribution-model","#chatland-muc","#community-decision-map","#chatland-3d"]
supersedes:
  - development/wiki/archive/old/browsy/browsy-questions.md
  - development/wiki/archive/old/plans/2026-11-21-app-database-stages.md
  - development/wiki/archive/old/root/backend.md
  - development/wiki/archive/old/standards.md
heavy: false
CONTEXT:END -->

# Channels

> **Migrated 2026-11-21.** This page imports the archived `root/backend.md` §14.

## Chatland cross-axis hitos

> Source: `development/wiki/archive/old/root/backend.md#14--chatland-cross-axis-hitos` (archived 2026-11-21).

The `mature` database enables Chatland; later stages add MUC, the 3D room and
federation. The canonical map and its owner live in the archived
`plans/2026-11-21-app-database-stages.md` §4.8; the rows live in
`milestones.json`.

| Hito | Stage | Axis · domain | Deliverable |
|---|---|---|---|
| `mynet-06` | mature | Backend · mynet | profiles/claims row as the single source Chatland reads; enables 1:1 chat |
| `schemas-11` | mature | Data · schemas | canonical schema for messages and chat_ephemeral with one owner doc |
| `storage-08` | mature | Backend · storage | persistent messages table backing Chatland 1:1 chat |
| `shell-13` | mature | Frontend · shell | thin opt-in XMPP adapter in Appy chat over WebSocket/BOSH |
| `work-25` | mature | Docs · work | one canonical map of the Chatland enablement chain and its owner |
| `channels-09` | grown | Community · channels | MUC zones with group visibility driven by M08 |
| `systems-25` | grown | Backend · systems | thin Prosody bridge for presence and MUC |
| `channels-10` | full | Community · channels | short-lived JWT room for Colyseus + Filament |
| `systems-26` | full | Backend · systems | portable profile and edges carrying Chatland identity between nodes |

Enablement chain: `mynet-06` + `schemas-11` → `storage-08` → `shell-13` →
`channels-09` / `systems-25` → `channels-10` / `systems-26` + `mynet-05`.
Docs → Work (`work-25`) owns the map. AI has no new model, skill, flow or depth
level and therefore no hito.

## Work

10 hitos · 53 tasks · 7 open · 3 closed. This page owns the
`community/channels` chapter.

<a id="audience-map"></a>
## Audience map

> Owner: channels. One table of audiences, channels and decision owner; every
> proposal has a destination and one authoritative channel.

<a id="risa-lovy"></a>
## risa ↔ lovy shared identity

> Owner: channels. One Authy identity signs into both apps without duplicating
> the profile; one app owns identity.

<a id="proposal-channel"></a>
## Proposal channel

> Owner: channels. Template with owner, status and linked decision; an open
> conflict is visible before implementation.

<a id="contribution-model"></a>
## Contribution-channel model

> Owner: channels. ACCESS/COM/IDEA and their destinations; Questy project
> standards fix paths, rules and presets.

<a id="chatland-muc"></a>
## Chatland MUC and presence

> Owner: channels. One zone maps to one MUC room; presence comes from claims; a
> private zone hides members while the row keeps them.

<a id="community-decision-map"></a>
## Community decision map

> Owner: channels. Every community tension lists its resolution and destination.

<a id="chatland-3d"></a>
## Chatland 3D room

> Owner: channels. A member with a verified claim gets an expiring JWT, enters
> the room, and leaves no persisted messages row for the session.

## Sources

- `development/wiki/archive/old/root/backend.md` §14.
- `development/wiki/archive/old/plans/2026-11-21-app-database-stages.md` §4.8.

## Source map

| Archived source | Date | Stable home |
|---|---|---|
| `archive/old/browsy/browsy-questions.md` | 2026-08-01 | development/standards/channels.md |
| `archive/old/plans/2026-11-21-app-database-stages.md` | 2026-11-21 | development/standards/channels.md |
| `archive/old/root/backend.md` | 2026-08-01 | development/standards/channels.md |
| `archive/old/standards.md` | 2026-08-01 | development/standards/channels.md |

Chapters without a separate source row are `milestone-only`: they are
specified from the register (hitos and tasks) and remain owned here.
