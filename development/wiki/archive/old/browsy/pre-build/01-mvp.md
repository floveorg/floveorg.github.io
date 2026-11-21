# 01 · MVP scope and first slice

> Goal: a single-device Browsy + MyNet that proves the data model before the
> network. The first slice is not a social network; it is a private/local
> record manager with groups.

## In v1

| Area | In |
|---|---|
| Authy | Create/unlock/lock; Ed25519; identity hash; L1 SelfAuth; L3 verified Telegram via risa or nonce+DM; optional L2 email/L4 phone |
| Vault | Encrypted local store; no P plaintext at rest |
| MyFamily | Person list; `personId`; 7 areas × 5 replies; 5 type percentages; **P by default**; Wizy reads locally |
| Groups | One free-named list; optional `Invitees` label (single-use, self-join); owner/member; add/remove; per-group key; version; projection = display name + 5 percentages; **no moderation** |
| Group card | Optional **S stats card** (invitee count/activity); members/details stay **L** |
| MyNet | People; favourites; groups; local feed; invites + **lineage**; visibility Private/MyNet/Group |
| Wizy | D0/D1 over local records; explanation of classes/paths |
| Bridge | Page status, save/list records, list groups, save/list local posts; no keys |
| Tests | Unit + Playwright smoke + two-profile fixtures |

## Deferred

| Area | Why |
|---|---|
| Public/S and Nety | Gateway contract and moderation not ready |
| Public groups / discovery | Requires Nety; no public group in v1 |
| Chat / audio / video | Different retention and consent model |
| Native host transport | Phase 5; v1 is single-device |
| Recovery quorum / masks / cross-device sync | Identity hardening after the local slice |
| Activity rings / trust facets | Not needed for local groups |
| Notifications | Needs transport |

## Definition of done — first slice

1. Fresh install → create identity → unlock → lock → unlock again.
2. Add two people; each defaults to P, has 7×5 answers and 5 percentages summing to 100; Wizy reads P locally.
3. Create a flat group with both people; projection shows the 5 bars, no raw
   areas.
4. Post to the group; reload; the post survives.
5. A second group shares one person; no duplicate `personId`.
6. A consult agreement lets a member’s Wizy see only the agreed scope; revoke stops it.
6. P fields never appear in the group projection or export.
7. Invite code + lineage tree visible locally.
8. No network call to Nety; no Public control.
9. `file://` and localhost both work.
10. Unit tests + Playwright popup smoke pass.

## Build order

1. Schemas + fixtures + threat model.
2. Authy vault + L1/L3.
3. MyFamily person + 7×5 profile.
4. Flat groups + projection + keys.
5. MyNet local UI (people/favourites/groups/feed/invites/lineage).
6. Native host + two-instance pull (Phase 5).
7. Nety Public (deferred).
