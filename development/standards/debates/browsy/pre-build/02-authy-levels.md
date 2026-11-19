# 02 · Authy levels: SelfAuth vs verified Telegram

> Question: what is the difference between “Telegram presence” and “verified by
> Telegram”? The answer decides the MyNet gate.

## Short answer

- **Presence** = you linked a Telegram account. It is **self-asserted**: Authy
  records that a handle is associated, but no peer can verify that you control
  it. It is **SelfAuth (L1)** and enables nothing.
- **Verified** = you proved control of the account:
  - a **risa signed presence claim**, or
  - the **Authy nonce → deep link → DM** flow.
  Both produce a signed proof that a peer can check. That is **L3**, and it is
  the MyNet/publish gate.
- **No presence level.** A bare Telegram link is a channel state, not a rung.
  This matches the decision: “count it as SelfAuth unless it is risa/verified”.

## Proposed ladder

| Level | Name | What it proves | How it is obtained | Gate |
|---|---|---|---|---|
| **L1** | **Self** (internal SelfAuth) | Nothing beyond self-assertion | Self, bio, a bare Telegram link | Default; no MyNet |
| **L2** | **Verified email** (optional) | Control of an email address | Email challenge | Extra assurance; not required for MyNet |
| **L3** | **Telegram verified** | Control of the Telegram account | **risa signed claim** or **Authy nonce+DM** | **MyNet local + Public/S + social keeper** |
| **L4** | **Verified phone** (optional) | Control of a phone number | SMS/voice challenge | Extra assurance; later |

**Bio** is profile completeness, not a level. **L5/L6 are retired** from the
ladder.

## State machine

```
L1 SelfAuth
  ├─ bare Telegram link ......... stays L1 (channel state)
  ├─ risa signed claim .......... L3
  ├─ Authy nonce + DM ........... L3
  ├─ verified email ............. L2 (optional)
  └─ verified phone ............. L4 (optional)
```

A later verification can raise the level; nothing lowers it automatically.
Revoking a channel returns the channel state, not the whole identity.

## What each gate unlocks

| Gate | Requirement | Unlocks |
|---|---|---|
| MyNet local | L3 | people, favourites, flat groups, local feed, invites/lineage |
| Social/Public | L3 | S bundles/posts; **deferred in v1** |
| Social keeper | L3 | send the signed Authy summary to the social keeper |
| Local keeper | L1 | send the signed summary to the local keeper |

## Why risa counts

risa is a **redirect to the Authy ID**, not a second identity root. It signs a
claim that points at the Authy identity; Browsy accepts **risa-signed** and
**Authy-signed** proofs. The Authy nonce+DM flow is the fallback. A bare link
has neither signature nor DM proof, so it stays Self (L1).

Decision: **pin risa and keep the Authy nonce+DM fallback** (O11=D). risa
redirects to the Authy ID; it does not create a new root.
A bare Telegram link is hidden until verified (O13=B); the L1 UI word is
**Self** (O12=B).

## Storage

- Canonical key: **`flove:authy/1`**.
- Legacy: `flove:authy` is read once, migrated, and marked `legacy: true`.
- Schema id: `flove-authy/1` inside the object.
- The extension stores the same state in the encrypted vault; the web demo
  uses `localStorage`.

## Open

- **Decided:** L1 + L3 only in the first build; L2 email/L4 phone later (O10=A).
- Which key signs the risa claim, and how is that key pinned?
- **Decided:** the UI word is **Self**.
