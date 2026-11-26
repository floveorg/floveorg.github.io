<!-- CONTEXT:BEGIN
schema: flove-page/1
id: tasks/tasks
path: development/standards/tasks/tasks.md
trunk: docs
topic: work
kind: topic
status: stable
html_place: ["#work-tracker"]
owns: ["Open questions", "status", "acceptance tests"]
updated: 2026-11-21
read_next: ["#work-work-02", "#work-work-07", "#work-work-08", "#work-work-10", "#work-work-11", "#work-work-25", "#work-work-12", "#work-work-13", "#work-work-14", "#work-work-15", "#work-work-17", "#work-work-19", "#work-work-20", "#work-work-21", "#work-work-22", "#work-work-23", "#work-work-24"]
CONTEXT:END -->

# Work

```text
standards/
├─ README.md · AGENTS.md · contract.md · vocabulary.md · wiki.md
├─ plans/plans.md · tasks/tasks.md  ★ YOU
├─ backend/ · frontend/ · data/ · community/
See also: ↑ ../AGENTS.md · ↓ frontend/frontend.md · → frontend/frontend.md#1320-data-depth-levels
```


## BSP requirements

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

## Acceptance and test plan

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

## Pending and out of scope

The live open questions and **Pre-build pendings** are owned by
[`plans/tasks/tasks.md#browsy-questions`](../../plans/tasks/tasks.md#browsy-questions).

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

Pending UI/design tracks: Browsy UI and Nety UI models are recorded in the plan
register; routing field colours and future DB are in
[`§13.24`](../frontend/frontend.md#routing-colours-optimisation-and-future-databases).
Routing optimisation is done (validator, flat index, `floveFieldsFlat()`); no app
UI code was changed.

## Open questions

The live A–L questions from `browsy-questions.md` are owned by
[`plans/tasks/tasks.md#browsy-questions`](../../plans/tasks/tasks.md#browsy-questions).
This page does not duplicate the table.

## Work

23 hitos · 130 tasks · 17 open · 6 closed. This page owns the `docs/work`
chapter.

## Authy open questions

The A01–A10 questions once parked in the Authy index are **not a second
register**. The live A–L register is
[`plans/tasks/tasks.md#browsy-questions`](../../plans/tasks/tasks.md#browsy-questions);
the accepted answers below are authoritative.

**Stale copy archived (2026-11-20):** A02 (publish gate) is decided — verified
Telegram **L3** is the gate (A02/A14/A15); a bare presence link is SelfAuth L1
and enables nothing. §A is the only home for that answer. Still open there:
A01, A03, A05–A10, A12–A13.


## Question register

The live A–L questions and the pre-build pendings are owned by
[`plans/tasks/tasks.md#browsy-questions`](../../plans/tasks/tasks.md#browsy-questions),
the single live register. This page carries only the accepted facts.

<a id="work-work-02"></a>
## Inventory of live MDs with owner and degree

> Owner: work. Canonical work item for `work-02`; status and evidence live in the register.

<a id="work-work-07"></a>
## Index of agent rules with their source MD

> Owner: work. Canonical work item for `work-07`; status and evidence live in the register.

<a id="work-work-08"></a>
## Docsify sidebar with one entry per live MD

> Owner: work. Canonical work item for `work-08`; status and evidence live in the register.

<a id="work-work-10"></a>
## Authy/MyNet: spec draft

> Owner: work. Canonical work item for `work-10`; status and evidence live in the register.

<a id="work-work-11"></a>
## BUI01/NUI01 as rows in pendings.md §Browsy pre-build

> Owner: work. Canonical work item for `work-11`; status and evidence live in the register.

<a id="work-work-25"></a>
## Owner of the cross-axis dependency map

> Owner: work. Canonical work item for `work-25`; status and evidence live in the register.

<a id="queue-policy"></a>
## Queue policy

The numbers source is `taskSet.queuePolicy` in [`../../tasks/milestones.json`](../../tasks/milestones.json); the rule is [`../../AGENTS.md#proc-09-replenish`](../../AGENTS.md#proc-09-replenish). `work-25.3d` owns trimming the live queue toward the historical target without exceeding the ceiling. This page links to those facts instead of restating them.

<a id="work-work-12"></a>
## Implement work tracker in Work

> Owner: work. Canonical work item for `work-12`; status and evidence live in the register.

<a id="work-work-13"></a>
## Execute pendings register in Work

> Owner: work. Canonical work item for `work-13`; status and evidence live in the register.

<a id="work-work-14"></a>
## How should docs search work?

> Owner: work. Canonical work item for `work-14`; status and evidence live in the register.

<a id="work-work-15"></a>
## Should docs include code examples?

> Owner: work. Canonical work item for `work-15`; status and evidence live in the register.

<a id="work-work-17"></a>
## What navigation pattern for docs?

> Owner: work. Canonical work item for `work-17`; status and evidence live in the register.

<a id="work-work-19"></a>
## Should docs have a contribution guide?

> Owner: work. Canonical work item for `work-19`; status and evidence live in the register.

<a id="work-work-20"></a>
## How should users get help or contact support?

> Owner: work. Canonical work item for `work-20`; status and evidence live in the register.

<a id="work-work-21"></a>
## How should docs be maintained over time?

> Owner: work. Canonical work item for `work-21`; status and evidence live in the register.

<a id="work-work-22"></a>
## Should docs support extensibility (plugins)?

> Owner: work. Canonical work item for `work-22`; status and evidence live in the register.

<a id="work-work-23"></a>
## What is the primary audience for flove docs?

> Owner: work. Canonical work item for `work-23`; status and evidence live in the register.

<a id="work-work-24"></a>
## How should docs handle versioning?

> Owner: work. Canonical work item for `work-24`; status and evidence live in the register.

## Sources

Source history is owned by `development/plans/`; this page holds the accepted facts.

