# 11 · Browsy and Nety UI — pending model

> Status: **pending; design only, no code** (2026-11-18). Use only what is
> already standardised and safe: flove tokens, the existing EN/ES copy pattern,
> accessibility rules and the current extension boundaries. Do not invent a new
> UI framework or a second component library.

**Tracked work:** BUI01 (Browsy UI) and NUI01 (Nety UI) are rows in
[`../../pendings.md` §Browsy pre-build](../../pendings.md); Work filter:
[ux · visual](https://flove.org/development/index.html#work?tab=docs&view=r2&subtab=work&category=ux&section=visual).

## Browsy UI

### Surfaces

| Surface | Purpose | Notes |
|---|---|---|
| **Entry popup** | Lock/unlock, identity level, quick links | “Browsy entry” chip in the model |
| **Host workspace** | Vault, MyFamily records, MyNet groups/feed, Wizy | “Browsy host” chip |
| **Authy ladder** | L1 Self → L3 Telegram verified → L4 phone → L5 bio | Bare Telegram link shown as unverified/hidden |
| **MyFamily editor** | 7 areas × 5 replies, 5 percentages, P/L/S | P default; Wizy local read |
| **MyNet local** | People, favourites, groups, feed, invites, lineage | Flat groups; `Invitees` label; S stats card vs L details |
| **Wizy panel** | D0/D1, explanation | No network by default |
| **Settings/security** | Lock, host status, permissions, export/import | No secrets in logs |

### Languages

- **EN + ES** first, using the existing `.en` / `.es` span pattern.
- No third language until the owner asks.
- Copy follows the spec vocabulary: **Self**, **verified Telegram**, **personal/local/social**, **Browsy entry/host**, **Browsy host**.
- Keep the existing bilingual pattern; do not add a runtime i18n dependency.

### Constraints

- Use the standard flove tokens and the existing component patterns.
- No remote fonts, CDN or remote code.
- No private key or P record in the UI layer.
- Every screen must have a locked, empty, error and offline state.
- Mobile: popup/panel must fit a narrow screen; tables scroll, not overflow.

### Pending decisions

- Popup vs side panel vs full workspace (H06).
- First-run onboarding: privacy classes, peers, empty vault (H01).
- Lock screen and panic/lock visibility (G07).
- Where the host status and permissions live.
- Which settings are per-device vs synced (sync is later).

## Nety UI

### Surfaces

| Surface | Purpose | Notes |
|---|---|---|
| **Social feed** | Public/S cards and reads | S only; no Local |
| **Public card** | Author, class S, provenance | No P fields |
| **Moderation** | pending → curator → live | Nety curators, not Browsy |
| **Public group card** | Join/read public groups | Deferred with Public |
| **Network status** | Toggle, gateway, zero-traffic state | Toggle off = no calls |

### Languages

- **EN + ES** first, same `.en` / `.es` pattern.
- Vocabulary: **Social = Public**, never “local” for Nety.
- Nety is a **client** in Browsy; do not present it as a local node.

### Constraints

- No P/L data in Nety UI.
- No moderation UI before the gateway/curator contract exists.
- Public/Nety is deferred; the UI is a sketch, not a build target.

### Pending decisions

- Is Nety a Browsy tab, a separate page, or the Nety app?
- What does the zero-traffic/toggle state look like?
- How are S cards and public groups joined?
- Which moderation actions exist for curators?

## Gate

Do not implement either UI until:

1. The local Browsy slice is defined (MVP).
2. The copy uses the settled vocabulary.
3. The screen inventory and states are accepted.
4. The bridge/security boundary is signed off.
