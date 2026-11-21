# Browsy — spec-driven development plan

> Status: **active specification** (2026-11-17). This plan collects the actual
> Browsy/Authy/Wizy/MyFamily/Nety decisions made today and turns them into
> traceable requirements, phases and acceptance tests. It supersedes the old
> plans only where the reconciliation table says so; it does not pretend the
> old documents never existed.
>
> Canonical companion docs:
> [`rationale.md`](rationale.md)
> (design rationale) · [`browsy-questions.md`](browsy-questions.md) (open questions) ·
> [`../../../../apps/sys/authy/index.html`](../../../../apps/sys/authy/index.html) (Authy index) ·
> [`index.html`](../../../../apps/sys/browsy/index.html) (Browsy use cases and diagrams) ·
> [`../../../diagrams/`](../../../diagrams/) (diagram masters).

---

## 1. Purpose and method

The project has accumulated several browsy/nety plans written at different
times, with different assumptions about Central, trust, permissions and Wizy.
This document is the **spec-first source of truth**: requirements are named,
implementation work references those names, and acceptance is tested against
them.

Rules:

1. A behaviour is not “implemented” until its requirement ID has an acceptance
   check in §7.
2. Old plans are not deleted; they are marked as historical or partially
   superseded in §5, with the exact sections that still apply.
3. A task without a requirement ID is either a chore or a new requirement; add
   it to the table first.
4. UI copy and diagrams must use the same vocabulary as this spec
   (Browsy, Authy, Wizy, MyNet, MyFamily, Nety, Personal, Local, Social).
5. Unresolved work goes to [`browsy-questions.md`](browsy-questions.md), not into silent
   assumptions.

---

## 2. Source-of-truth hierarchy

| Level | Artifact | Owns |
|---|---|---|
| 1 | This plan | behaviour, boundaries, acceptance |
| 2 | `rationale.md` | rationale, sketches, alternatives |
| 3 | `apps/sys/authy/index.html` | Authy levels, claim demo, persistence/keepers |
| 4 | `apps/sys/browsy/index.html` | Browsy use cases and model diagrams |
| 5 | `development/addons/media/apps/logos/{authy,browsy,central}/*` | canonical visual masters + rendered threads |
| 6 | `browsy-questions.md` | unresolved questions for the next questy survey |

Anything below level 2 that contradicts levels 1–2 is a documentation bug.

---

## 3. Actual specifications (as of 2026-11-17)

### 3.1 Architecture

- **Browsy is the host.** It runs as a browser extension (MV3 + Firefox
  polyfill) and contains Authy and Wizy. Wizy is not a separate network client
  and does not own a key store.
- **Authy is the identity module inside Browsy.** It owns the root identity,
  channel proofs, levels, sessions, recovery, and the signing of bundles and
  grants.
- **Wizy is the JSON manager inside Browsy.** It reads the vault, merges
  Personal + Local + Social data, derives D, builds projections, and explains
  its results. It reaches the local net and Nety social only through Browsy's
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

### 3.2 Data classes and privacy invariants

| Class | Meaning | Movement |
|---|---|---|
| **P — Personal** | private data and keys; **Private** visibility | encrypted vault; never leaves unencrypted |
| **L — Local** | records **shareable** with named peers or groups | direct, encrypted per recipient, session by session |
| **S — Social = Public** | published data; **Social** and **Public** are synonyms | Nety (and optional Central mirror) |
| **D — Derived** | Wizy outputs | local by default; shared only by explicit export |
| **M — Metadata** | grants, peer list, audit | encrypted vault; minimal disclosure |

Invariants:

1. P is never present in an S bundle.
2. L is a projection under a signed grant; no “share whole vault” path.
3. Revocation is forward-only; copies cannot be recalled. TTL + key rotation
   are the mitigations.
4. Every received bundle is signature-checked before merge.
5. Defaults are private; widening is an explicit user act.
6. Nety never learns who pulls from whom locally.
7. Linking a channel never re-derives the identity root.
8. Promotion is explicit: P → L or S, and L → S, only by the owner. L never
   becomes Public automatically; S is the only class that reaches Nety.

### 3.3 Authy

- **Levels:** **L1 Self (SelfAuth internally) · L2 verified email (optional) ·
  L3 Telegram verified · L4 verified phone · L5 bio**. L3 is the owner of the
  ladder (CR26 resolved 2026-11-20); a bare Telegram link stays L1.
- **Self (L1; SelfAuth internally):** anything self-asserted — self, bio, a bare Telegram link.
  A bare link is a channel state; it does **not** raise the level and does not
  open MyNet.
- **Telegram verified (L3):** either a **risa signed presence claim** or the
  **Authy nonce + DM** flow. Both prove control; the handle is not published.
  L3 is the MyNet local gate and the Social/Public publishing gate in v1.
- **Email/phone/bio:** L2/L4 are optional verified channels and L5 is profile
  completeness; none is a different identity or a new content surface.
- **Invites as authentication.** An invite code can travel as a Telegram deep
  link; clicking it can start Authy authentication for the invitee. The invitee
  gets an identity hash and can join MyFamily/Invitees. **risa is a redirect to
  the Authy ID**, not a separate root; accept both risa-signed and Authy-signed
  proofs.
- **Persistence:** the canonical key is **`flove:authy/1`** in `localStorage`
  (localhost and `file://`). `flove:authy` is the legacy key: read it once,
  migrate to `/1`, and keep a `legacy` flag. Appy-basic and the Authy index
  share `flove:authy/1`.
- **Keepers:** the signed summary goes to a **local** keeper first and, only
  at L3, to a **social** keeper. Bridge hooks: `floveBrowsy.saveAuthy` /
  `floveNety.publishAuthy`, with local fallback.
- **Recovery:** self-backup rotation, social quorum fallback, probation after
  social recovery; never a central reset.

### 3.4 MyNet and MyFamily

- **Social ships inside MyNet, not as a standalone app.** The archived choice
  (`VARIOUS_Q07`, “Profily-integrated MyNet”) makes Social the MyNet tab of the
  tabbed Nety app — prominent at tab 3 of 5 — with social features as its
  headline content. There is no standalone Social entry point or duplicate
  card; Social publishing remains the L3 surface and is not a second MyNet
  tier. See BSP-M16.
- **Telegram verified enables MyNet.** A bare presence link does not. Once L3
  is verified, MyNet exposes people, favourites, flat local groups, feed,
  invites + lineage and local sharing.
- **MyNet uses the MyFamily profile, not a simplified copy.** The profile is
  the **7 MyFamily areas × 5 replies**, summarised as **5 type percentages**
  (Cousin, Sibling, Grandparent, Parent, Partner). There are no separate
  relation/traits/affinity fields.
- **MyFamily is the full record manager.** A new person defaults to **P**
  (Personal/private); **Wizy may read P locally on the owner’s device**.
  Sharing requires an **L** projection or an **S** card. **L** is
  Local/shareable with named peers or groups; **S** is Social = Public. The app
  stays the editor; Browsy is the record manager.
- **Fallback:** `window.floveMyFamily` exposes `toRecord`, `save`, `setClass`,
  `list` and `groups`. When Browsy is absent, the app downloads the portrait
  and links to the Browsy info page; no hard dependency and no network call.

#### 3.4.1 MyNet local groups, built on the MyFamily profile

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
- **5 replies per area**, mapped to the 5 types, least → most:
  1. Cousin
  2. Sibling
  3. Grandparent
  4. Parent
  5. Partner
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
4. **No public group join in v1.** Visibility is Private / MyNet / Group.
   An owner may publish an **S stats card** (invitee count/activity); the group
   itself stays L.
5. **Creating or joining a group is Local.** No Nety call; no Public card.
6. **Every group has its own key.** Add member → L grant; remove member →
   version++ and key rotation. Removal writes a tombstone and requests
   deletion; copies cannot be recalled. Revocation is forward-only.
7. **Posts and invites are signed.** Groups are owner-managed; there is **no
   group moderation** in v1.
8. **Invite lineage is included.** The invite code, parent, uses, expiry and
   status are M/L; the tree is visible locally.
9. **A person can be in several groups** without merging or reclassifying the
   person.
10. **Consult agreements.** An owner can sign a scoped, revocable
    `flove-consult/1` agreement that lets a selected member’s **Wizy** consult
    selected MyFamily data across groups. It returns derived answers, never a
    raw P copy. See [`pre-build/09-consult-agreements.md`](pre-build/09-consult-agreements.md).
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

### 3.5 Wizy and derivation

Wizy supports the D options already tabled: D0 none, D1 deterministic rules,
D2 on-device model, D3 remote de-identified, D4 remote encrypted (future),
D5 peer-assisted. Others-view options: O0 signed projection (default), O1
recomputation under grant (opt-in), O2 social comparison (S only, later).

Defaults: D0/D1 local; D2 optional; D3 per-request consent; D4/D5 later; O0.

### 3.6 Permissions and grants

- A grant is signed by Authy and travels with the bundle.
- Fields: grantor, grantee (key/circle/group), bundle, paths, capabilities
  (`view`, `derive`, `aggregate`; no implicit `copy`), expiry, content key,
  version, signature.
- Unit for v1: JSON path with array ranges. Field-level is a later refinement.
- Enforcement: Browsy on send/receive; Wizy on projection; apps never read the
  vault directly.
- P2P permission enforcement is a separate trunk; the current scope is local
  federation between Browsy instances.

### 3.7 Interfaces and files

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
| `flove:authy/1` (schema `flove-authy/1`) | `{schema, level, identities[], channels{...}, updatedAt}` |
| `flove-bundle/0.1` (proposed) | owner, class, documents[], grants[], signature |
| `flove-group/0.1` (proposed) | id, name, kind, memberIds, roles, defaultClass, visibility, projection, keyId, version, signature |
| `flove-consult/1` (proposed) | owner, member, wizy, scope{personIds, groupIds, paths, capabilities}, purpose, expiresAt, version, signature |

### 3.8 Browsy extension standards (draft)

**Identity hash.** One identity, one hash:

```
hash = PeerId = CIDv1(sha256(ed25519_pubkey)) → bafk…
```

The full value is stored; the UI shows a short prefix with copy. Nety's
`PeerId::from_public_key_bytes` already implements this formula.

**Generation.** Hybrid:
- Extension installed: the service worker creates and stores the root. The hash
  is shown in the extension UI (popup/side panel); Appy/Browsy index may display
  it only through an explicit handoff, never as a portable root.
- No extension: Browsy index / Appy embed may create a **full local identity**
  in `flove:identity` with `source:"web"` and a visible warning. It works on
  mobile and can sign local grants, but there is no web→extension migration;
  installing the extension starts a new canonical identity.
- `file://`: web fallback; the manifest does not cover `file://`.
- One canonical hash per profile; the extension wins when installed, and a web
  demo stays a separate record.

**Status (2026-11-18).** The web fallback is live: `apps/sys/browsy/index.html`
generates an Ed25519 key with WebCrypto, derives the CIDv1 PeerId
(`bafk…`), stores `flove:identity` with `source:"web"` and `notPortable:true`,
and Appy embeds the same generator through `?embed=1`. The private seed stays in
the Browsy page; Appy only mirrors the public hash. The extension
`getOrCreateIdentity()`/bridge and the Nety root import are next.

**Direction: Browsy pulls, the page does not ask.** There is no
page→extension identity or vault API. The pipeline is:

1. The user clicks Browsy.
2. The content script reads the current public page (visible text/DOM).
3. The service worker/worker parses it; Wizy mixes it with local P/L content.
4. Browsy renders suggestions in the page or side panel.

The page never receives the vault, the root key or the identity hash from this
pipeline.

**Pull scope (Q004).** Full DOM, including form fields and hidden inputs,
selected for signal. This is a high-risk choice: it needs an explicit redaction
policy before shipping (Q006).

**Consent (Q005).** A persistent Browsy indicator while pulling, a **Stop**
button and a per-site allowlist. Never pull silently.

**Redaction (Q006).** A full-DOM pull includes normal `input`, `textarea` and
`select` values for context, but never `type=password`, secret `autocomplete`
tokens, hidden inputs, cookies or tokens. Raw values never go to logs.

**Failure (Q002).** Typed state `idle · pulling · no-access · error` with a
retry. No silent injection.

| Stage | Internal interface | Notes |
|---|---|---|
| pull | `browsy.pullPage()` | current public page; click only |
| derive | `wizy.suggest()` | page content + local classes; no network |
| present | `browsy.render()` | badges/side panel; no P/L |
| sign | `authy.sign()` | internal; app handoffs only |
| export | `authy.exportRoot()` | extension UI; explicit gesture |

**Runtime (v1).** Chrome/Edge use WebCrypto Ed25519; Firefox/Safari use the
bundled tweetnacl fallback. Both paths are tested; `lib/tweetnacl.min.js` and
`lib/worker.js` must exist in the package.

**Storage (Q007).** v1 keeps `browsy-keys` in `chrome.storage.local`; the
encrypted vault is M2. The web fallback uses `flove:identity`.

**Identity record (Q010).** Canonical `flove-identity/1`:
`{schema, hash, publicKey, source, createdAt, label?}`. `flove-browsy/1` is a
read-only view; `flove:authy.self.browsyHash` is a display cache.

**Web local identity lifecycle (Q009/Q013).** An existing `source:"web"`
record is hidden but kept when the extension identity appears; the extension
hash is canonical. Never auto-delete the local identity.

**Recovery (Q014).** A 12-word seed is generated at identity creation; social
quorum is a later path. The seed is the only recovery for a local key, so the
warning must say so.

**Origins (Q012).** Only `https://flove.org/*`, `http://localhost/*` and
`http://127.0.0.1/*`; no `<all_urls>`; no `file://` (use the web fallback).

**Nety (direction: same root; transport open).** The root should be imported
into Nety's encrypted keystore so the PeerId is the same hash. The transport is
undecided: encrypted export, native messaging or seed phrase (K08). Delegation
is the v2 path for multi-device.

**Open.** Vault/unlock, Nety transport, app sessions,
release, logging, masks, sync and the test matrix: see `browsy-questions.md` K01–K18.

---

## 4. Requirements

| ID | Requirement | Acceptance |
|---|---|---|
| **BSP-A01** | Browsy hosts Authy and Wizy; neither is a separate network client. | Authy/Wizy run inside Browsy; no second key store; pages do not query the vault. |
| **BSP-A02** | Nety carries only S; Local goes peer-to-peer. | A Local payload is never routed through the Nety gateway. |
| **BSP-A03** | Central is optional. | Disabling Central leaves Local/Social flows working. |
| **BSP-D01** | P/L/S/D/M classes apply to every bundle and field. | Every shipped JSON maps to a class; export refuses P paths. |
| **BSP-D02** | Defaults are private. | New record/field starts P or L by explicit choice; no public default. |
| **BSP-I01** | Authy implements L1–L5: Self (SelfAuth internally), verified email (optional), Telegram verified, verified phone, bio. | Ladder shows L1–L5; a bare Telegram link stays Self/L1; L3 is the MyNet/publish gate. |
| **BSP-I02** | Telegram verification is either a risa redirect to the Authy ID or Authy nonce → deep link → DM. | Both paths persist L3; risa does not create a second root; a bare link does not. |
| **BSP-I03** | Authy state persists in `flove:authy/1`; `flove:authy` is legacy and migrated once. | Reload appy-basic/Authy index; `/1` survives; the legacy read flag is set. |
| **BSP-I04** | Local keeper before social keeper; social keeper only at L3. | Social send is rejected below L3; local payload is stored first. |
| **BSP-I05** | The Browsy identity hash is the Nety PeerId: `CIDv1(sha256(ed25519_pubkey))`. | The same key yields the same `bafk…` in Browsy and Nety. |
| **BSP-I06** | Identity generation is hybrid: extension canonical, web provisional. | With the extension the page never receives the private key; without it a `source:"web"` key is marked provisional and importable. |
| **BSP-M01** | Verified Telegram (L3) enables MyNet; a bare presence link does not. | Without L3 MyNet is read-only; after L3 local people/groups/feed open. |
| **BSP-M02** | MyNet uses the MyFamily 7×5 profile; the group projection is L, while the person record defaults P. | Profile has 7 areas × 5 replies and percentages summing to 100; no relation/traits/affinity fields. |
| **BSP-M03** | MyFamily records are kept P/L/S; a new person defaults to P and Wizy may read P locally. | Class selector persists; P stays private; L only when shared; S is Social = Public. |
| **BSP-M04** | MyFamily works without Browsy. | With no bridge it downloads the portrait and links to the info page. |
| **BSP-M05** | MyNet v1 exposes people, favourites, flat local groups, feed, invites + lineage and visibility Private/MyNet/Group. Public/moderation deferred. | Local surface works at L3; no Nety calls; Public control absent. |
| **BSP-M06** | Local groups are created from MyFamily `personId`s; there is one person store, not a copy. | A group created in MyNet opens the same record from MyFamily; renaming/reclassifying updates both views. |
| **BSP-M07** | Group projection = display name + 5 type percentages; raw 7×5 answers stay P/L unless opted in. | A group bundle has the 5 percentages and no raw area answers; opt-in adds them. |
| **BSP-M08** | Creating or joining a local group makes no Nety call. | Group creation and member pull work with the Social toggle off. |
| **BSP-M09** | Every group has its own key and L grants; removing a member rotates the key and bumps the version. | Removed member cannot decrypt new posts; old copies remain and are labelled as such. |
| **BSP-M10** | Visibility v1: Private (P), MyNet (L), Group (L); Public (S) is deferred. | Picker has three values; no Public option; Group never appears in Nety. |
| **BSP-M11** | Posts and invites are signed; v1 is local only. | A tampered post is rejected; no moderation state exists in v1. |
| **BSP-M12** | Groups are flat and a person can belong to several; no nesting and no public groups. | No `parentId`; two groups show the same `personId`; no public group create/join. |
| **BSP-M13** | An owner can grant a member’s Wizy a scoped consult agreement over selected MyFamily data. | Agreement is signed, revocable, scoped to person/group/paths, and returns derived answers only. |
| **BSP-M14** | Groups are one owner list with free names and optional labels; `Invitees` is invite-only and each code admits one person who joins themselves. | A group can be freely named and labelled; an Invitees code is single-use; the invitee self-joins. |
| **BSP-M15** | The owner can publish an S stats card (invitee count/activity) while members, roles, posts and lineage stay L. | The S card contains only counts/stats; full details require an L grant. |
| **BSP-M16** | Social is the MyNet tab of the tabbed app, not a standalone Social app. | MyNet is tab 3 of 5; no standalone Social entry point or card; Social publishing still requires L3 and is not a MyNet tier. |
| **BSP-W01** | Wizy derives locally by default. | D0/D1 work offline; D3 requires explicit consent. |
| **BSP-W02** | Wizy explains what it used. | A recommendation shows its input classes and paths. |
| **BSP-P01** | Grants are signed and travel with bundles. | A tampered/grant-mismatched bundle is rejected. |
| **BSP-P02** | Revocation stops future reads; copies remain. | Revoke bumps version/rotates key; UI states the limit. |
| **BSP-N01** | Nety Social is S-only and consent-based. | Toggle off = zero Nety calls; publish requires consent. |
| **BSP-U01** | Vocabulary is consistent across page, diagrams and appy. | Personal/Local/Social names match; no stale “P/L/S” in user copy where words are required. |
| **BSP-U02** | Diagrams and indexes are the public map. | Decentral/browsy/authy pages link to one another and to the masters. |
| **BSP-T01** | Each phase has an offline test path. | `file://` and localhost both work; no runtime CDN. |

---

## 5. Old plans — reconciliation

Each old plan gets a status notice pointing here. The table records what remains
useful.

| Old document | Old assumption | Status now | What to keep |
|---|---|---|---|
| removed 2026-11-17 (browser-extension plan) | Broad extension MVP: discovery, save-to-flove, badges, profile scoring, sync. | **Superseded in scope** by BSP-A/U. Discovery features are backlog, not current spec. | Extension skeleton, on-demand rule, size/performance constraints. |
| `development/standards/debates/browsy/README.md` | Central is the trust/permissions hub; extension is thin. | **Superseded in authority** by BSP-A/P. | MV3 architecture, storage split, crypto primitives, F2F. |
| `development/standards/debates/browsy/browsy-questions.md` | 244 decisions across tiers, UI, sync. | **Historical decision log**; use BSP IDs for current work. | Questions still open; pointers to old surveys. |
| `development/standards/debates/browsy/port-nety.md` | Port crypto/store now; Central permissions layer. | **Port mechanics kept; permissions layer superseded** by BSP-P. | `lib/crypto.js`/`lib/store.js` seams, key namespacing, message registry. |
| `development/standards/debates/browsy/TESTING.md` | Old risk matrix. | **Extend** with §7 tests; old cases remain as regression ideas. | On-demand tests, crypto/risk analysis, browser matrix. |
| removed 2026-11-17 (nety-frontend plan) | Nety as extension of Browsy with tiers/masks/MyNet. | **Partially superseded** by BSP-M/N; the MyNet surface is now integrated in §3.4.1. | Identity masks, f2f base, people/groups/feed/invites/moderation ideas. |
| removed 2026-11-17 (nety-trust plan) | Central computes ranking/trust; curators/jury. | **Superseded for Browsy trust**; Nety WoT only ranks S. | Facets, vouch concepts, anti-collusion ideas. |
| `development/standards/debates/plans/central-backend.md` | Central is the data bank and permissions authority. | **Demoted to optional mirror** by BSP-A03. | FastAPI/Turso hosting for public bundles, sync patterns. |
| removed 2026-11-17 (appy-normal plan) | Wizy mini at normal tier; MyNet+Browsy demo. | **Partially superseded**: Wizy lives in Browsy from the start; MyNet is now the local group surface. | Appy shell, MyNet people/groups/feed UI, tier wording. |
| `development/index.html` §P2P | Browsy v3/Nety v4/Wizy v3 presentation. | **To overwrite** at release (see §6 Phase 7). | Visual language, links, badges. |

---

## 6. Development plan

### Phase 0 — Spec consolidation (this document)

**Requirements:** all. **Deliverables:** this plan; notices in old plans; index
row; pending list. **Gate:** every old plan points here; no contradictory
“current spec” claim remains.

### Phase 1 — Authy foundation

**Spec:** BSP-I01–I04, BSP-A01.
**Tasks:** settle `flove:authy/1` (migrate `flove:authy`); persist/unlock in
appy-basic/Authy index; optional L2 email; L3 Telegram verified via **risa
signed claim or nonce → DM**; keepers at L3; recovery placeholders. **Gate:**
reload survives; a bare Telegram link stays L1; L3 can publish; a tampered
payload is rejected. **Status:** mostly built in appy-basic + Authy index;
needs schema migration, risa/claim backend and the L1–L4 ladder.

### Phase 2 — Wizy inside Browsy (shell)

**Spec:** BSP-A01, BSP-W01–02.
**Tasks:** extension module boundary; Wizy workspace; bundle registry; class
tags; local-only D0/D1; explanation panel; no network. **Gate:** works offline
from a bundle; derives without network; no separate keys.

### Phase 3 — MyFamily records and flat local groups

**Spec:** BSP-M02–M08, BSP-M12, BSP-M16, BSP-D01–D02.
**Tasks:** person list/personId; the **7 areas × 5 replies** profile and the
**5 type percentages** (Cousin · Sibling · Grandparent · Parent · Partner);
class P/L/S with **P as the new-person default**; Wizy reads P locally on the
owner’s device; **flat** group model (name, kind, members, owner/member,
visibility `local`/`group`, projection `myfamily-profile/1`, keyId, version,
**no parentId**); MyNet Groups panel that opens the MyFamily people list;
projection = display name + 5 percentages (raw 7×5 opt-in); group creation and
membership; invites + lineage; `floveMyFamily` bridge (`list`, `groups`);
fallback download; no network. **Gate:** a person has 7×5 answers and 5
percentages summing to 100; a group with two people survives reload; the group
projection has the 5 bars and no raw areas; two flat groups share a person; no
Public/nesting; lineage is visible; no bridge still works. **Status:** bridge
and class selector built; record list, 7×5 profile and group model pending
(B10; L01 local group, L02 owner/member, L04 flat and L05 MyFamily profile
decided; L03 invitee-only distinction, L06–L09 open).

### Phase 4 — Grants and permissioned projections

**Spec:** BSP-P01–P02, BSP-M09, BSP-D01–D02.
**Tasks:** grant schema; path/array grammar; per-group content key; member L
grants; encryption per recipient; expiry/rotation; projection preview; group
key rotation on removal; **consult agreements** (`flove-consult/1`) for a
member’s Wizy over selected person/group/paths. **Gate:** grant mismatch
rejected; expired grant stops reads; removed member cannot decrypt new posts;
old copies are labelled; a consult agreement returns only its scope and stops
on revoke.

### Phase 5 — Local net transport (native host)

**Spec:** BSP-A02, BSP-P02, BSP-M08–M09.
**Tasks:** native messaging host (mDNS/UDP discovery, local WebSocket/QUIC or
signed JSON frames); group bundle pull/push; feed; invites; signatures;
delta/version; offline queue; audit log. **Gate:** two Browsy instances exchange
group posts through the host; a non-member is rejected; no Nety calls for L;
revoke stops the next pull. **Status:** transport choice decided: native host,
not browser WebRTC.

### Phase 6 — Nety Social (deferred)

**Spec:** BSP-N01, BSP-A02–A03, BSP-M10–M11.
**Status:** **postponed for v1.** MyNet ships local only; Public/S, public
groups and moderation stay out of the first build.
**Tasks for later:** opt-in toggle; S schema; public group cards; signed reads;
moderation pending → curator → live; Nety gateway/daemon; Central mirror
optional. **Gate:** S contains no P; Group/L never reaches Nety; toggle off =
zero Nety traffic; Public requires L3 verified Telegram.

### Phase 7 — Documents, diagrams, public map

**Spec:** BSP-U01–U02.
**Tasks:** refresh Authy index; Browsy use cases; decentral diagram; menu/About;
diagram masters; replace Development index P2P presentation. **Gate:** vocabulary
matches; links resolve; mobile/desktop render; no stale “old plan” presentation.

### Phase 8 — Hardening and release

**Spec:** BSP-T01 + all.
**Tasks:** offline/file:// matrix; accessibility; extension permissions audit;
bundle signing review; release package; overwrite old landing copy. **Gate:**
`check-distro` clean; no high-risk finding; Chrome+Firefox manual pass.

---

## 7. Acceptance and test plan

| Area | Test |
|---|---|
| Authy | bare link stays L1; risa/claim reaches L3; reload persistence; L1 cannot publish; keeper local/social rules |
| MyFamily | 7 areas × 5 replies; 5 percentages sum to 100; new person defaults P; Wizy reads P locally; P export refusal; no-Browsy fallback; reload |
| MyNet surface | Social is the MyNet tab (tab 3 of 5); no standalone Social app or card; Social publishing still requires L3 and is not a MyNet tier |
| MyNet groups | one free-named list; optional `Invitees` label; single-use invitee self-join; create from MyFamily; one `personId`; projection = display name + 5 percentages, no raw areas; flat groups; two groups per person; lineage visible; no public group join/nesting; S stats card counts only; details L |
| Consult | owner→member Wizy agreement; scope only; derived answers only; revoke stops the next consult |
| Wizy | D0/D1 offline; explanation; projection cannot include P |
| Grants | tamper rejection; expiry; revoke; path intersection |
| Local net | two instances; granted-only paths; zero Nety calls; offline queue |
| Nety | S-only; toggle off; consent; optional Central off |
| UI | vocabulary; links; mobile; keyboard; no runtime CDN |

Every test is runnable from `file://` and localhost; no test may require Central.

---

## 8. Pending / out of scope

The open questions remain in [`browsy-questions.md`](browsy-questions.md),
including the **Pre-build pendings** section. The closed answer log is
[`pre-build/open-issues.md`](pre-build/open-issues.md).
Highlights: group defaults (F3), subject consent (F6), app sessions, offline
queue, bridge/security, grant defaults, DPIA and erasure.
**Decided:** L01 local group, L02 owner/member, L04 flat groups, L05 MyFamily
7×5 profile, P as the new-person default, no group moderation, consult
agreements, native host transport, Nety/Public postponed, Social integrated as
the MyNet tab (not a standalone app, `VARIOUS_Q07`).

Out of scope for v1: browser P2P transport, a real Telegram bot, Nety
gateway/daemon, public groups/moderation, and replacing the public P2P
presentation before Phase 7. Browsy is the Nety **client**; the gateway/daemon
stays a separate prerequisite.

**Pending UI/design tracks:** Browsy UI and Nety UI models (EN/ES, standard patterns only) are in [`pre-build/11-ui-pending.md`](pre-build/11-ui-pending.md); routing field colours and future DB are pending in [`../../frontend/routing-colours-db.md`](../../frontend/routing-colours-db.md). Routing optimisation is done (validator, flat index, `floveFieldsFlat()`); no app UI code was changed.

**Pre-build artifacts:** [`pre-build/README.md`](pre-build/README.md) — MVP,
Authy levels, schemas, MyFamily profile, native host, bridge threat model,
lineage/tests and model labels. They are the working contracts for the first
slice. The **closed answer log** is
[`pre-build/open-issues.md`](pre-build/open-issues.md); open items live in
[`browsy-questions.md`](browsy-questions.md) §Pre-build pendings.

---

## 9. Changelog

| Date | Change |
|---|---|
| 2026-11-17 | Initial spec-driven plan; reconciles old browsy/nety/central plans with today’s Authy/MyNet/MyFamily/Wizy/Nety decisions. |
| 2026-11-17 | Integrates the MyNet surface (people, favourites, groups, feed, invites, visibility, moderation) and adds the MyFamily-based local-group model (BSP-M05–M12, Phase 3–6, group tests, pendings L01–L14). |
| 2026-11-17 | Refines before build: SelfAuth/verified Telegram ladder (no presence level), MyFamily 7×5 profile + 5 type percentages, flat groups/no public groups, native-host transport, Nety/Public postponed, `flove:authy/1` canonical. |
| 2026-11-18 | Owner answers: P default + local Wizy read, owner-only membership, single free-named group list + `Invitees` label, S stats card vs L details, no group moderation, consult agreements, invite code + Telegram/Authy auth, risa redirect; Self label, Rust host, WebSocket+JSON, entry/host labels, retire Else. |
| 2026-11-20 | Integrates `VARIOUS_Q07`: Social ships as the MyNet tab, not a standalone app (BSP-M16); closes the mirrored pendings row. |
