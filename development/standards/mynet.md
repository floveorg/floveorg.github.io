<!-- CONTEXT:BEGIN
schema: flove-page/1
id: backend/mynet
path: development/standards/mynet.md
trunk: backend
topic: mynet
kind: topic
status: stable
html_place: ["#p2p", "#messenger"]
owns: ["MyNet L1–L5", "flove-auth/1", "BSP acceptance"]
updated: 2026-11-21
read_next: ["#authy-identity","#mynet-and-myfamily","#local-groups","#mynet-work-data","#central-identity","#invite-lineage","#consult-agreements"]
supersedes:
  - development/wiki/archive/old/bridges/oasis.md
  - development/wiki/archive/old/browsy/README.md
  - development/wiki/archive/old/browsy/TESTING.md
  - development/wiki/archive/old/browsy/browsy-questions.md
  - development/wiki/archive/old/browsy/port-nety.md
  - development/wiki/archive/old/browsy/pre-build/01-mvp.md
  - development/wiki/archive/old/browsy/pre-build/02-authy-levels.md
  - development/wiki/archive/old/browsy/pre-build/04-myfamily-profile.md
  - development/wiki/archive/old/browsy/pre-build/07-lineage-tests.md
  - development/wiki/archive/old/browsy/pre-build/09-consult-agreements.md
  - development/wiki/archive/old/browsy/rationale.md
  - development/wiki/archive/old/browsy/spec.md
  - development/wiki/archive/old/plans/2026-11-17-appy-authy-mynet.md
  - development/wiki/archive/old/plans/2026-11-21-app-database-stages.md
  - development/wiki/archive/old/plans/central-backend.md
  - development/wiki/archive/old/root/backend.md
heavy: false
CONTEXT:END -->

# MyNet

> **Migrated 2026-11-21.** The Authy, MyNet/MyFamily and local-group
> sections below are imported from `browsy/spec.md` §3.3–§3.4.1. The rest of
> MyNet’s source set is still pending.

## Authy identity

> Source: `development/wiki/archive/old/browsy/spec.md#33-authy` (archived 2026-11-21).

**Levels:** **L1 Self** (SelfAuth internally) · **L2 verified email** (optional) ·
**L3 Telegram verified** · **L4 verified phone** · **L5 bio**. L3 owns the
ladder (CR26, 2026-11-20); a bare Telegram link stays L1.

- **Self (L1):** anything self-asserted — self, bio, a bare Telegram link. A bare
  link is a channel state; it does not raise the level and does not open MyNet.
- **Telegram verified (L3):** either a **risa signed presence claim** or the
  **Authy nonce + DM** flow. Both prove control; the handle is not published. L3
  is the MyNet local gate and the Social/Public publishing gate in v1.
- **Email/phone/bio:** L2/L4 are optional verified channels and L5 is profile
  completeness; none is a different identity or a new content surface.
- **Invites as authentication:** an invite code can travel as a Telegram deep
  link; clicking it can start Authy authentication for the invitee. The invitee
  gets an identity hash and can join MyFamily/Invitees. **risa is a redirect to
  the Authy ID**, not a separate root; accept both risa-signed and
  Authy-signed proofs.
- **Persistence:** canonical key **`flove:authy/1`** in `localStorage` (localhost
  and `file://`). `flove:authy` is the legacy key: read it once, migrate to
  `/1`, and keep a `legacy` flag. Appy-basic and the Authy index share
  `flove:authy/1`.
- **Keepers:** the signed summary goes to a **local** keeper first and, only at
  L3, to a **social** keeper. Bridge hooks: `floveBrowsy.saveAuthy` /
  `floveNety.publishAuthy`, with local fallback.
- **Recovery:** self-backup rotation, social quorum fallback, probation after
  social recovery; never a central reset.

## MyNet and MyFamily

> Source: `development/wiki/archive/old/browsy/spec.md#34-mynet-and-myfamily` (archived 2026-11-21).

- **Social ships inside MyNet, not as a standalone app.** The archived choice
  (`VARIOUS_Q07`, “Profily-integrated MyNet”) makes Social the MyNet tab of the
  tabbed Nety app — prominent at tab 3 of 5 — with social features as its
  headline content. There is no standalone Social entry point or duplicate card;
  Social publishing remains the L3 surface and is not a second MyNet tier. See
  BSP-M16.
- **Telegram verified enables MyNet.** A bare presence link does not. Once L3 is
  verified, MyNet exposes people, favourites, flat local groups, feed, invites +
  lineage and local sharing.
- **MyNet uses the MyFamily profile, not a simplified copy.** The profile is the
  **7 MyFamily areas × 5 replies**, summarised as **5 type percentages**
  (Cousin, Sibling, Grandparent, Parent, Partner). There are no separate
  relation/traits/affinity fields.
- **MyFamily is the full record manager.** A new person defaults to **P**
  (Personal/private); **Wizy may read P locally on the owner’s device**.
  Sharing requires an **L** projection or an **S** card. **L** is
  Local/shareable with named peers or groups; **S** is Social = Public. The app
  stays the editor; Browsy is the record manager.
- **Fallback:** `window.floveMyFamily` exposes `toRecord`, `save`, `setClass`,
  `list` and `groups`. When Browsy is absent, the app downloads the portrait and
  links to the Browsy info page; no hard dependency and no network call.

## Local groups

> Source: `development/wiki/archive/old/browsy/spec.md#341-mynet-local-groups-built-on-the-myfamily-profile` (archived 2026-11-21).

The Appy MyNet panel demonstrates the local surface: invites and lineage,
favourites, groups, a two-column feed (People · Groups), post visibility and a
moderation flow. In v1 Browsy ships the **local surface only**: **Public/Nety
and moderation are deferred**.

| MyNet feature (Appy) | Browsy v1 object |
|---|---|
| Invites + lineage | Invite (M/L), local; lineage tree visible |
| Favourites | f2f peers (L) |
| Groups | Flat local group (M/L), from MyFamily `personId`s |
| Feed: People · Groups | Signed posts; L only |
| Visibility: Private · MyNet · Group | P · L (favourites) · L (members); **Public deferred** |
| Moderation: pending → curator → live | **Deferred** with Public |
| People to follow / groups to support | **Deferred** (S discovery) |

**MyFamily profile.** A person is not reduced to “relation + 2–3 traits + one
affinity”. The profile is the MyFamily **7 × 5 matrix**:

- **7 areas:** Attention · Contact · Influence · Feedback · Gifting · Sharing ·
  Money.
- **5 replies per area**, mapped to the 5 types, least → most: Cousin, Sibling,
  Grandparent, Parent, Partner.
- **5 percentages** = selected replies per type ÷ total selections, rounded to
  one decimal and summing to 100 (e.g. Cousin 18.2% · Sibling 27.3% ·
  Grandparent 18.2% · Parent 18.2% · Partner 18.1%).

The 7 × 5 answers stay in the person record. The group projection is
`displayName` + the **5 type percentages**; sharing the raw area answers is an
explicit opt-in, never the default.

A **local group**:

| Field | Meaning |
|---|---|
| `id`, `name`, `kind` | stable id; **free display name**; `family` / `friends` / `work` / `custom`. |
| `labels[]` | free labels; `Invitees` marks an invite-only group. |
| `invitePolicy` | `single` (one invitee per invite, self-join) or `multi`. |
| `memberIds[]` | MyFamily `personId`s; a person can belong to several flat groups. |
| `roles{}` | `owner` / `member`; v1 is owner/member only. |
| `defaultClass` | `L` in v1. |
| `visibility` | `local` (MyNet/favourites) or `group` (members). No nesting. |
| `projection` | `myfamily-profile/1`: display name + 5 type percentages (raw 7×5 opt-in). |
| `card` | `public` S stats (invitee count, activity) + `local` L details (members, roles, posts, lineage). |
| `keyId`, `version` | per-group content key and monotonic version. |
| `signature` | signed by Authy; travels with every group bundle. |

**One list, free names, optional labels.** Groups live in a single owner list
and can be named freely. A group may carry labels (free text); **Invitees** is
special: an invite-only group where each invite admits one person, who joins
themselves. The owner can publish an **S card** with invitee count/activity
stats and keep the **L details** (members, roles, posts, lineage) for permitted
peers.

Rules:

1. **MyFamily remains the person editor; MyNet is the group editor.** One
   `personId`, no copied person store.
2. **Projection = display name + 5 percentages.** No relation/traits/affinity
   fields; the raw 7×5 answers are P/L unless explicitly shared.
3. **Groups are flat.** No nesting, no aliases, no parent group.
4. **No public group join in v1.** Visibility is Private / MyNet / Group. An
   owner may publish an **S stats card** (invitee count/activity); the group
   itself stays L.
5. **Creating or joining a group is Local.** No Nety call; no Public card.
6. **Every group has its own key.** Add member → L grant; remove member →
   version++ and key rotation. Removal writes a tombstone and requests deletion;
   copies cannot be recalled. Revocation is forward-only.
7. **Posts and invites are signed.** Groups are owner-managed; there is **no
   group moderation** in v1.
8. **Invite lineage is included.** The invite code, parent, uses, expiry and
   status are M/L; the tree is visible locally.
9. **A person can be in several groups** without merging or reclassifying the
   person.
10. **Consult agreements.** An owner can sign a scoped, revocable
    `flove-consult/1` agreement that lets a selected member’s **Wizy** consult
    selected MyFamily data across groups. It returns derived answers, never a
    raw P copy.
11. **Invitees label.** A group labelled `Invitees` is invite-only; each code
    admits one person and the invitee joins themselves. The owner sees the
    invitee count; that count can be the S stats card.
12. **Stats vs details.** Invitee count and activity are **S** only when the
    owner opts in; members, roles, posts and lineage are **L** details.

Group objects:

| Object | Key fields | Class |
|---|---|---|
| Person (MyFamily) | `personId`, display name, 7 areas × 5 replies, 5 type percentages, class | P/L/S |
| Local group | `id`, name, kind, `labels[]`, `invitePolicy`, `memberIds`, roles, `defaultClass: L`, visibility `local`/`group`, card stats S/L, projection `myfamily-profile/1`, `keyId`, version, **no `parentId`** | M/L (+S stats card) |
| Group grant | `groupId`, `memberId`, paths, capabilities, expiry, content key, version, signature | M |
| Post | `id`, author, `groupId?`, visibility, body, `class: L`, createdAt, signature | L |
| Invite | code, inviter, parent, lineage, uses, expires, status | M/L |

**Flow — MyNet → Groups → New group:**

1. Name the group freely; choose kind (`family`/`friends`/`work`/`custom`),
   optional labels (including `Invitees`) and visibility (`MyNet` or `Group`).
2. Pick people from the **MyFamily** list; each pick shows the 5 type bars.
3. Roles owner/member; projection is display name + 5 percentages. Raw 7×5
   stays out unless the owner opts in.
4. Create: Authy signs the group; Browsy creates the per-group key and member
   grants.
5. The group card shows member count, the 5 mini bars, class **L**, key
   version, last post and an “Open MyFamily record” action. An owner can opt in
   to an **S stats card** with invitee count/activity; full details stay **L**.
6. Settings: add/remove member, rotate key, invite + lineage, invite policy
   (`single`/`multi`), S stats toggle, archive.

**Shared list.** MyFamily shows each person’s groups and a “New group” action;
MyNet is the default group workspace. Both read the same group store — no
second group list and no duplicate membership.

## MyNet work data

> Source: `development/wiki/archive/old/root/backend.md#13--mynet-subsection` (archived 2026-11-21).

MyNet is the Appy feature set that opens over `claims` and the `profiles` row.
Its hitos and tasks are owned by the register under `backend/mynet`; the Work
page renders the Backend → MyNet tab. This page does not restate the table.

| Hito | Stage | Deliverable |
|---|---|---|
| `mynet-01` | seed | read-only MyNet preview and MyFamily JSON export owned by Appy |
| `mynet-02` | infant | claim rows from the Authy and Browsy handoffs |
| `mynet-03` | infant | `mynetFlags()`, `socialEnabled()` and `publishUnlocked` derived from claims |
| `mynet-06` | mature | profiles/claims row as the single source Chatland reads; enables 1:1 chat |
| `mynet-04` | grown | row-backed people, circles, feed, follow and local sharing |
| `mynet-05` | full | signed portable MyNet profile and its edges |

All **44** tasks carry a concrete title, a done-criterion, one owner path and a
machine-readable evidence pointer. The preview reads the existing
`flove-profile` envelope; no new envelope, feature-flags envelope or third
control surface is added.

## Central identity

> Source: `development/wiki/archive/old/plans/central-backend.md#identity-model-progressive` (archived 2026-11-21).

Central’s identity is progressive: a device UUID first, an email claim later,
and more methods deferred. The canonical Authy identity remains the Browsy/Authy
ladder; Central is a mirror, not a second root. Full model:
[`plans/backend/systems.md#identity-model-progressive`](../wiki/plans/backend/systems.md#identity-model-progressive).

## Invite lineage

> Source: `development/wiki/archive/old/browsy/pre-build/07-lineage-tests.md` (archived 2026-11-21).

Lineage is in v1: local metadata plus a visible tree, not a public/Nety feature.

```json
{
  "code": "FLOVE-7K2M",
  "inviter": "bafk…",
  "parent": "FLOVE-3A9Q" | null,
  "uses": 1,
  "expiresAt": "2026-12-17T00:00:00Z",
  "status": "active" | "revoked" | "used",
  "signature": "ed25519:hex"
}
```

`parent` is the code that invited the inviter; `null` for a root. The tree is
`parent → inviter → invitee`. Lineage is M/L and never goes to Nety in v1.
Revoke marks `status: "revoked"`; it does not erase the tree. “Disown” is
deferred until its meaning is defined.

MVP UI: generate/copy/validate/revoke one code; a simple lineage tree; a used
code shows the invitee if accepted locally; no public group join or discovery.

Fixtures: people `ana` (28.6/28.6/14.3/14.3/14.2), `bob` (20 each), `charlie`
(0/0/0/0/100); groups `family`, `friends`, `work`, `invitees`; bundles valid,
tampered, expired, revoked and P-leak. Acceptance: identity lock/unlock; P
default; percentages sum 100; flat groups; post survives reload; remove member
rotates key; invite lineage; consult scope/revoke; page writes L-only; no Nety
call; `file://` + localhost.

## Consult agreements

> Source: `development/wiki/archive/old/browsy/pre-build/09-consult-agreements.md` (archived 2026-11-21).

An owner can let selected members’ **Wizy** consult selected MyFamily data
through an explicit, signed, revocable agreement. No group moderation.

Actors: **owner** (record/group creator), **subject** (person the record is
about), **member** (peer in a shared group), **Wizy** (member’s local runtime).
The member’s Wizy never receives the raw P record; it receives a scoped
capability and returns derived answers.

`flove-consult/1` fields: `id`, `owner`, `member`, `wizy`, `scope{personIds,
groupIds, paths, capabilities}`, `purpose`, `expiresAt`, `version`, `signature`.
Capabilities are `view`, `derive`, `aggregate`; **no `copy`**. Scope is the
intersection of person/group/paths; the most specific wins. Revocation bumps
`version`; the next pull refuses the old agreement.

Flow: member asks or owner offers → owner picks scope/purpose/expiry → Authy
signs → member Wizy pulls and derives locally → Wizy explains what it used →
owner revokes/shortens → old results are labelled old; copies cannot be
recalled.

No group moderation. Subject-consent options remain open: owner-only; owner +
subject consent for L/S (recommended); subject consent for S only; no
third-person sharing. UI: MyFamily person → “Allow a Wizy to consult…”; choose
member/scope/purpose/expiry; group card shows “consulted by N Wizys” with
revoke; member sees the agreement, not the raw record.

## Sources

- `development/wiki/archive/old/browsy/spec.md` §3.3–§3.4.1 (verbatim archive).
- `development/wiki/archive/old/browsy/pre-build/02-authy-levels.md`,
  `04-myfamily-profile.md`, `09-consult-agreements.md`.
- `development/wiki/archive/old/plans/2026-11-17-appy-authy-mynet.md`.

## Source map

| Archived source | Date | Stable home |
|---|---|---|
| `archive/old/bridges/oasis.md` | 2026-08-01 | development/standards/mynet.md |
| `archive/old/browsy/README.md` | 2026-08-01 | development/standards/mynet.md |
| `archive/old/browsy/TESTING.md` | 2026-08-01 | development/standards/mynet.md |
| `archive/old/browsy/browsy-questions.md` | 2026-08-01 | development/standards/mynet.md |
| `archive/old/browsy/port-nety.md` | 2026-08-01 | development/standards/mynet.md |
| `archive/old/browsy/pre-build/01-mvp.md` | 2026-11-17 | development/standards/mynet.md |
| `archive/old/browsy/pre-build/02-authy-levels.md` | 2026-11-17 | development/standards/mynet.md |
| `archive/old/browsy/pre-build/04-myfamily-profile.md` | 2026-11-17 | development/standards/mynet.md |
| `archive/old/browsy/pre-build/07-lineage-tests.md` | 2026-11-17 | development/standards/mynet.md |
| `archive/old/browsy/pre-build/09-consult-agreements.md` | 2026-11-18 | development/standards/mynet.md |
| `archive/old/browsy/rationale.md` | 2026-11-17 | development/standards/mynet.md |
| `archive/old/browsy/spec.md` | 2026-11-17 | development/standards/mynet.md |
| `archive/old/plans/2026-11-17-appy-authy-mynet.md` | 2026-11-17 | development/standards/mynet.md |
| `archive/old/plans/2026-11-21-app-database-stages.md` | 2026-11-21 | development/standards/mynet.md |
| `archive/old/plans/central-backend.md` | 2026-08-01 | development/standards/mynet.md |
| `archive/old/root/backend.md` | 2026-08-01 | development/standards/mynet.md |

Chapters without a separate source row are `milestone-only`: they are
specified from the register (hitos and tasks) and remain owned here.
