# Browsy · MyNet — pre-build artifacts

> Status: **refinement** (2026-11-17). These are the contracts to close before
> writing the first vertical slice. They refine
> [`../spec.md`](../spec.md); they do not replace it.

## Decisions locked for v1

| Decision | Value |
|---|---|
| Authy ladder | **L1 Self (SelfAuth internally) · L2 verified email (optional) · L3 Telegram verified · L4 verified phone**. Bio is profile completeness, not a level. |
| Telegram | A bare link is SelfAuth L1. A **risa signed presence claim** or **Authy nonce + DM** reaches L3. Presence alone enables nothing. |
| MyNet gate | **L3 verified Telegram** opens MyNet local. Public/S is deferred. |
| MyFamily profile | **7 areas × 5 replies** → **5 type percentages** (Cousin · Sibling · Grandparent · Parent · Partner). No relation/traits/affinity fields. |
| New person | **P** (private) by default; **Wizy reads P locally**; L/S only when shared. |
| Groups | **Flat**, owner/member, no nesting, **no public groups**, **no moderation**. |
| Groups | One owner list, free names, optional labels; **Invitees** = invite-only, one code per person, self-join. |
| Group card | Owner may publish an **S stats card** (invitee count/activity); members/details stay **L**. |
| Consult | `flove-consult/1`: owner lets a member’s Wizy consult selected data; revocable. |
| Invite discovery | Invite code + Telegram deep link + Authy authentication; risa is a redirect to Authy ID. |
| Projection | Display name + 5 percentages. The raw 7×5 answers stay P/L unless the owner opts in. |
| Transport | **Native messaging host** (not browser WebRTC). |
| Nety / Public | **Postponed** for v1. MyNet local only. |
| Authy key | **`flove:authy/1`** canonical; `flove:authy` is migrated once. |
| Social/Public | **Synonyms**. `S` is the class; “Public” is its visibility. |
| Local | **Shareable** with named peers/groups; not public. |
| Personal | **Private**, owner only. |

## Still open

- F3: O05/O06/O07 defaults.
- F6: owner agreement vs subject consent.
- Remaining Qs: Q5–Q7, Q9, Q14, Q19–Q23, Q27–Q29, Q31–Q32 — see `browsy-questions.md` §Pre-build pendings.

The lettered answer sheet is [`open-issues.md`](open-issues.md).

## Artifacts

| # | File | What it closes |
|---|---|---|
| 01 | [`01-mvp.md`](01-mvp.md) | In/out scope and first-slice definition of done |
| 02 | [`02-authy-levels.md`](02-authy-levels.md) | SelfAuth vs verified Telegram, gates, keepers |
| 03 | [`03-schemas.md`](03-schemas.md) | `flove:authy/1`, identity, profile, group, bundle, grant, post, invite |
| 04 | [`04-myfamily-profile.md`](04-myfamily-profile.md) | 7 areas × 5 replies, 5 types, percentages, projection |
| 05 | [`05-native-host.md`](05-native-host.md) | Native messaging protocol and security |
| 06 | [`06-bridge-threat-model.md`](06-bridge-threat-model.md) | Page↔extension API, XSS, keys |
| 07 | [`07-lineage-tests.md`](07-lineage-tests.md) | Invite lineage + fixtures/acceptance |
| 08 | [`08-model-labels.md`](08-model-labels.md) | “Else” and the two Browsy chips |
| 09 | [`09-consult-agreements.md`](09-consult-agreements.md) | Owner→member Wizy consultation across local groups |
| 10 | [`open-issues.md`](open-issues.md) | Closed answer log; open items are in `../browsy-questions.md` §Pre-build pendings |
| 11 | [`11-ui-pending.md`](11-ui-pending.md) | Browsy/Nety UI models, EN/ES, no code |

## Build gate

Do not start the first slice until:

1. The MVP table is accepted.
2. The Authy ladder and gates are accepted.
3. The profile and group projection schema is frozen.
4. The bridge API allowlist and threat model are signed off.
5. The native-host protocol has a first message set.
6. Fixtures exist for a valid, tampered and revoked bundle.

The first slice is **single-device**: Authy + vault + MyFamily profile + flat
groups + local feed. No host transport, no Nety, no public groups.
