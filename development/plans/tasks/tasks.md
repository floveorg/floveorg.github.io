---
status: stable
section: docs/work
created: 2026-11-21
also: [development/standards/tasks/tasks.md, development/standards/backend/mynet/mynet.md, development/standards/backend/systems/systems.md, development/standards/data/ai/flows/flows.md]
---

<a id="browsy-questions"></a>
# Browsy questions

> Source: `development/archive/old/browsy/browsy-questions.md` (archived 2026-11-21).
> Live questions A–L and the pre-build pendings are here; the 244-answer historical log is preserved in the archive.

> **Status 2026-11-17 — superseded in part.** Current spec:
> [`spec.md`](../../archive/old/browsy/spec.md).
> Historical decision log. Current work uses BSP IDs in the new plan.

> Fresh question interface for browsy architecture decisions.
> Load this file to continue asking questions without full session context.

---

## Live questions — 2026-11-17 (Browsy · Authy · Wizy · Nety)

> Moved from the old `pendings.md` on 2026-11-17. These are the live
> survey questions; the 244-answer historical log is preserved in the archive.

This is the **only** register for these questions: the formerly parked A01–A10
copy in [`plans/2026-11-19-authy-open-questions.md`](../../archive/old/plans/2026-11-19-authy-open-questions.md)
now points back here. Update status here, not in both files. Work filter:
[backend · systems](https://flove.org/development/index.html#backend).

## A · Authy and identity

| ID | Question | Why it matters |
|---|---|---|
| A01 | Should the five steps stay Self → Email → Telegram → Phone → Bio, or be reordered by proof strength? | The current UI implies a progression the protocol does not enforce. |
| A02 | (Decided 2026-11-17) Is the publish gate verified Telegram **L3**? | Yes: risa signed claim or Authy nonce+DM. A bare presence link is SelfAuth L1. |
| A03 | Do the displayed points (+4/+12/+6/+8) or the awarded points (20/50/100/200) become the single source? | Both exist in appy-basic today; they cannot both be right. |
| A04 | Is "Self" a level or just the default profile state? | It has a bar, points and a form but is not a channel. |
| A05 | What exactly is a session token for an app: JWT, signed capability object, or opaque handle? | Wizy/Appy need to act without the private key. |
| A06 | How many identities can one human hold, and how do masks relate to the root key? | nety-frontend already has a mask selector; Authy has no model yet. |
| A07 | What is the recovery quorum: how many peers, which circles, what probation? | "Social quorum" is named but undefined. |
| A08 | Does a channel proof live as P (private) or M (metadata)? Can peers verify it without seeing the handle? | Proofs can leak the handle/phone. |
| A09 | Should biometrics ever leave the device as a proof, or stay as a local unlock factor? | Highest sensitivity; current UI treats it as a channel. |
| A10 | Does Authy bind to the Nety PeerId, or is the PeerId a separate key? | Duplicate identities complicate trust and revocation. |
| A11 | What is the lifecycle of `flove:authy` (schema, versioning, migration, reset)? | It now persists across appy-basic and the Authy index. |
| A12 | What exactly goes to the local keeper vs the social keeper, and who signs it? | The index stores two payloads; the contract is provisional. |
| A13 | Is the claim nonce issued by a server, a bot, or locally? | The demo mints it locally; risa uses server-side libSQL with TTL. |
| A14 | (Decided 2026-11-17) Should Telegram presence already allow local sharing? | No. Only verified Telegram L3 opens MyNet/local sharing. |
| A15 | (Decided 2026-11-17) Does verified Telegram L3 enable MyNet? | Yes; bare presence enables nothing. Public/S is deferred. |
| B11 | Which MyFamily fields survive in MyNet's group projection? | **Decided 2026-11-17:** the 5 type percentages; the raw 7×5 answers are opt-in. |

> **Decided 2026-11-17:** A02/A14/A15 — **verified Telegram L3** is the gate
> (risa signed claim or Authy nonce+DM); a bare presence link is SelfAuth L1
> and enables nothing. A11 — **`flove:authy/1`** is canonical; `flove:authy` is
> migrated once. B11 — group projection is the 5 MyFamily percentages.
> **Still open:** A01, A03, A05–A10, A12–A13.

## B · MyFamily and third-party data

| ID | Question | Why it matters |
|---|---|---|
| B01 | Is L the right default for an added person, and when should P or S win? | The record profiles an identifiable third person. |
| B02 | Does the subject (the friend) have a right to see, correct or delete the record? | Current app has no subject-facing flow. |
| B03 | Can the owner share a MyFamily record at all without the subject's consent? Under which conditions? | The product intent is sharing, the ethics are unresolved. |
| B04 | What is the minimum viable L projection: traits, raters, nuances, or a derived sentence? | Raw nuances can be more revealing than traits. |
| B05 | What is a "public card" for a third person, and can it exist without their approval? | The possible web-social path needs a boundary. |
| B06 | How are children or vulnerable people handled? | MyFamily explicitly includes family. |
| B07 | Does each person get a stable `personId`, and who owns it across devices? | Needed for records, grants and erasure. |
| B08 | What happens to grants and peer copies when the owner deletes a person? | Erasure must propagate as far as honestly possible. |
| B09 | Can MyFamily records be imported from another user, or only authored? | Determines whether it is a manager or a one-way export. |
| B10 | Is the current one-person-per-page model replaced by a list, or kept as a detail view? | UI and data model both change. |

## C · Permissions and grants

| ID | Question | Why it matters |
|---|---|---|
| C01 | Is the grant unit a file, a JSON path, an array slice or a field? | Determines the whole enforcement engine. |
| C02 | What does `derive` mean exactly, and can it be revoked separately from `view`? | D1–D3 need a capability boundary. |
| C03 | What does `aggregate` allow, and can the result be shared? | Aggregates can leak the inputs. |
| C04 | Is `copy` ever allowed, or is every share a reference plus encrypted projection? | Copy defeats revocation. |
| C05 | Are circles the only principal, or can single keys/groups be principals too? | Old specs disagree. |
| C06 | What is the default TTL for an L grant? | Short TTL is the main revocation mitigation. |
| C07 | Does revocation rotate the content key, and who re-encrypts what? | Costly but necessary for real revocation. |
| C08 | How are grants displayed to a non-technical user (paths vs friendly labels)? | Path grammar must not become the UI. |
| C09 | Can a grant be delegated (A grants B the right to grant C)? | Not needed for v1, but changes the schema. |
| C10 | What does "denied" look like: hide existence, or say "no access"? | Metadata leakage vs clarity. |
| C11 | Is P2P permission enforcement a separate trunk from Browsy local federation? | The plan assumes yes; it needs an owner and a boundary. |

## D · Local network and transport

| ID | Question | Why it matters |
|---|---|---|
| D01 | QR/manual endpoint, LAN discovery, WebRTC, or Nety DHT for addresses? | The core of "directly from users". |
| D02 | Does the local net work across NAT without a relay, and is a relay allowed? | Determines mobile/remote viability. |
| D03 | Is the transport peer-to-peer at the browser level or via a localhost helper? | MV3 cannot open arbitrary sockets. |
| D04 | How does a peer authenticate before the first pull: key fingerprint, invite, both? | Prevents impersonation. |
| D05 | What is the delta format and conflict model (vector clock, CRDT, last-write-wins)? | Needed for offline sessions. |
| D06 | What is the maximum stale window for L before Wizy warns? | Freshness is part of the privacy contract. |
| D07 | How is spam/Sybil handled on the local net? | Direct peers can still be malicious. |
| D08 | Does turning the local net off still allow cached L? | UX and expectations. |

## E · Wizy and derivation

| ID | Question | Why it matters |
|---|---|---|
| E01 | Which derivation ships first: D0, D1, or both? | Scope for M5. |
| E02 | Does D2 (on-device model) need a specific runtime (WASM, WebGPU), and what size budget? | Extension size and battery. |
| E03 | What exactly is in a D3 de-identified payload, and who audits the de-identification? | The highest-risk outbound path. |
| E04 | Can D be shared as L or S, and does it inherit the inputs' grants? | A derived file can leak its sources. |
| E05 | What does the explanation show: inputs, weights, both, or a natural-language rationale? | Trust and inspectability. |
| E06 | Does Wizy see P values directly, or only aggregates? | Current plan says Wizy sees P in memory; confirm. |
| E07 | Is there a "no derivation" mode that only filters and merges? | D0 is the safe default. |
| E08 | How are recommendations versioned and invalidated when inputs change? | Stale advice is a trust bug. |

## F · Nety and the social layer

> **Nota 2026-11-17 — Browsy es cliente de Nety, no nodo.** La extensión no abre
> sockets ni corre un DHT; habla con el gateway/daemon por HTTPS/WebSocket. El
> transporte Local es otro carril (WebRTC o helper nativo) y nunca pasa por Nety.
> No se forkeará `nety.html` para identidad: Authy es la raíz y Nety importa la
> misma raíz (BSP-I05).

| ID | Question | Why it matters |
|---|---|---|
| F09 | ¿Browsy es cliente o nodo de Nety? | MV3 no puede ser un nodo completo; el gateway/daemon es obligatorio. |
| F01 | When will the gateway and daemon actually connect (bootstrap/mDNS)? | M4 is blocked until then. |
| F02 | What is the S bundle schema, and is it exactly the L schema with a different class? | "Structured like local data" needs a contract. |
| F03 | Are group-visible S bundles encrypted, and with which key model? | Public is not the only social mode. |
| F04 | What does Nety store, for how long, and who can delete it? | Retention is a privacy decision. |
| F05 | Can Nety rank S results without learning the user's L graph? | Privacy-preserving ranking. |
| F06 | Are likes/reposts/trust part of S or separate metadata? | They reveal the social graph. |
| F07 | Does Central mirror S automatically, or only on request? | Duplicate copies and takedown. |
| F08 | What is the takedown path for a public S bundle? | Legal and ethical requirement. |

## G · Browsy engineering and security

| ID | Question | Why it matters |
|---|---|---|
| G01 | Which storage backend for the vault: IndexedDB + WebCrypto, OPFS, native messaging? | MV3 limits and quotas. |
| G02 | What is the unlock factor: passphrase, WebAuthn, OS keychain, combination? | Defines the "supersafe" bar. |
| G03 | How is the extension updated and reviewed (store, signed builds, reproducible)? | Supply-chain risk. |
| G04 | What are the minimum permissions in the manifest for local net + Nety? | Over-broad permissions kill trust. |
| G05 | How does the bridge expose data to flove.org apps without letting XSS read the vault? | Same-origin apps are the attack surface. |
| G06 | What happens when storage is full or the vault is corrupted? | Recovery without plaintext leaks. |
| G07 | Is there a panic/lock button, and what does it wipe? | Physical threat model. |
| G08 | How are logs redacted before a bug report? | Diagnostics can leak P. |

## H · UX and product

| ID | Question | Why it matters |
|---|---|---|
| H01 | What does first-run onboarding show: privacy classes, peers, or an empty vault? | Sets expectations. |
| H02 | How does a user create their first grant without understanding paths? | Usability vs precision. |
| H03 | Where do the "local net" and "Nety social" toggles live? | They are the two big switches. |
| H04 | What does "what others see" look like on mobile? | Projection preview is core. |
| H05 | How are denied/expired/revoked states shown? | Honest limits are part of privacy. |
| H06 | Should Wizy be a popup, side panel, or full workspace? | MV3 and focus. |
| H07 | What is the empty state for MyFamily with no records? | Sensitive onboarding. |
| H08 | Which language(s) ship first for the Authy index and MyFamily use case? | flove is bilingual; scope matters. |

## I · Legal, ethics and governance

| ID | Question | Why it matters |
|---|---|---|
| I01 | Who is the data controller for a MyFamily record: the owner, the subject, or both? | Determines consent and erasure duties. |
| I02 | What is the age policy for P2P sharing and third-party records? | Children in family data. |
| I03 | Does the project need a privacy notice / DPIA before M3? | Shipping personal data cross-peer. |
| I04 | How are subject-access and deletion requests handled peer-to-peer? | Copies make this hard. |
| I05 | What is the policy for law-enforcement or abuse requests? | Governance gap. |
| I06 | Are there categories that must never be shareable (health, sexual, political)? | Product ethics. |

## J · Integration, schema and legacy

| ID | Question | Why it matters |
|---|---|---|
| J01 | Does `flove-bundle/0.1` become the canonical envelope, or does the portrait stay primary? | Compatibility with Appy and apps. |
| J02 | How are existing `*-portrait.json` files migrated into bundles? | Users already have files. |
| J03 | Does Appy render from a file, from Browsy, or both? | Determines the bridge. |
| J04 | What is the versioning policy when `flove-portrait/1` gains fields? | Apps and Appy must not break. |
| J05 | Which parts of the old browser-extension plan survive, and which are archived? | Avoid two conflicting plans. |
| J06 | How does the appy-basic Authenticate card hand off to the Authy index? | One source of truth. |
| J07 | Do MyFamily records get a routing.json entry and a fields manifest? | jsony/routing expectations. |
| J08 | What is the deprecation path for `tools/pending/sync-puzzy.py` and the parked checks? | Ties into the pending plan. |

---

## K · Browsy extension standards (2026-11-17)

> Decided in the main plan (`2026-11-17-appy-authy-mynet.md` §7d): the hash is
> the Nety PeerId, generation is hybrid (extension canonical, web provisional),
> and Nety v1 imports the same root. The questions below are the remaining
> standards for the extension.
>
> Session 1 (2026-11-17): Browsy **pulls** public pages on demand and mixes them
> with local content; pages do not query identity or vault. V1 targets
> Chrome/Edge + Firefox/Safari with the tweetnacl fallback. K02–K03 and K18 are
> narrowed by those answers.
>
> Session 2: pull failure shows typed states + retry; pull scope is the full
> DOM (redaction policy still open); consent is a persistent indicator + Stop +
> per-site allowlist.
>
> Session 3: full-DOM pull includes `input`/`textarea`/`select` values but
> excludes password/secret/hidden fields, cookies and tokens; v1 uses plain
> `chrome.storage.local` (vault in M2); there is no web→extension portability —
> the web identity is fallback/demo only.
>
> Session 4: a web demo is hidden but kept when the extension appears; the
> canonical record is `flove-identity/1`, with `flove-browsy/1` as a view; the
> same-root Nety transport is still open (K08).
>
> Session 5: v1 pulls only flove.org/localhost/127.0.0.1 (no `<all_urls>`, no
> `file://`); the web fallback is a full local identity with a warning,
> including mobile, and is not portable; recovery is a 12-word seed in v1.

| ID | Question | Why it matters |
|---|---|---|
| K01 | Is the extension the canonical identity host for every flove app, or only when installed? | Decides whether the web can create identities at all. |
| K02 | What is the exact internal contract for pull → suggest → render: inputs, outputs, errors and timeouts? | The current bridge only has stubs; pages must not become a vault API. |
| K03 | (Resolved) v1 pulls only flove.org/localhost/127.0.0.1; no `<all_urls>`, no `file://`. How is the origin allowlist maintained and audited? | Pulling is the main boundary; XSS on flove.org is the attack surface. |
| K04 | (Resolved) v1 uses plain `chrome.storage.local`; the encrypted vault is M2. Which unlock factor should M2 use? | Security vs delivery speed. |
| K05 | (Resolved) There is no web→extension portability; the web identity is fallback/demo only. What is its lifecycle? | Avoid implying a migration path that does not exist. |
| K06 | (Resolved) The web demo is hidden but kept; the extension hash is canonical. | One canonical hash per profile. |
| K07 | (Resolved) Canonical `flove-identity/1`; `flove-browsy/1` is a read-only view. What are the versioning and migration rules? | Appy, Authy and Nety must read the same record. |
| K08 | (Open) How does the root reach Nety: encrypted export, native messaging or seed phrase? How is the same PeerId verified? | Same identity without leaking the root. |
| K09 | What is the minimum manifest permission set for flove.org/localhost only (no `<all_urls>`, no `file://`)? | Over-broad permissions kill trust. |
| K10 | (Resolved) Without the extension, the web creates a full local identity with a warning, including mobile; `file://` uses the same fallback. | The extension cannot cover every context. |
| K11 | (Resolved) v1 uses a 12-word seed at creation; social quorum is later. Where is the seed stored/shown? | Loss and rotation are unsolved. |
| K12 | What does an app receive to act without the private key: session token, capability object or one-shot signature? What can it sign? | Authy sessions are still undefined. |
| K13 | What is the release standard: store, signed builds, reproducible, Firefox/Safari packaging? | Supply-chain and review risk. |
| K14 | What is redacted from a full-DOM pull and from logs: password fields, hidden inputs, keys, hashes, identity events? | Pulls and bug reports can leak P. |
| K15 | What is the local identity warning UX: text, expiry, upgrade prompt and deletion? | Users must understand a non-portable key store. |
| K16 | Can one root hold multiple profiles or masks, and how are they selected? | nety-frontend already has masks; Authy does not. |
| K17 | Is identity synced across devices: `chrome.storage.sync`, an encrypted file, or not in v1? | Multi-device changes the storage model. |
| K18 | What is the identity test matrix beyond browsers: installed/not installed, `file://`, storage blocked, locked service worker? | Acceptance must cover the fallbacks. |

## L · MyNet local groups (2026-11-17)

> The MyNet surface (people, favourites, groups, feed, invites, visibility,
> moderation) and the MyFamily-based local-group model are now in the main plan
> §3.4.1. These are the remaining product and consent questions.
>
> **Decided 2026-11-17:** L01 use **local group**; L02 owner/member only in v1;
> L04 **flat, no nesting/alias**; L05 **MyFamily 7×5 profile + 5 type
> percentages**, projection = display name + percentages; L07 multi-group yes;
> L10 **feed only**, chat deferred; L11 **no public groups in v1**; L14 MyFamily
> remains the person editor. **Still open:** L03, L06, L08, L09, L12, L13.
>
> **Answers 2026-11-18:** O01 A, O02 B, O03 A, O04 D, O08 P default,
> O10 A, O11 D, O12 B, O13 B, O15 A, O16 invite code + Telegram/Authy auth,
> O17 B, O18 A, O24 B, O25 entry/host labels, O26 A, O30 consult agreement.
> F1/F2/F4/F5 closed; F3/F6/F7 moved to §Pre-build pendings below.
> Closed log: [`pre-build/open-issues.md`](../../archive/old/browsy/pre-build/open-issues.md).
>
> **2026-11-18:** L03/L06/L08/L09 decided by O01–O04; L12/L13 moved to F3;
> subject consent is F6.

| ID | Question | Why it matters |
|---|---|---|
| L01 | Is the user-facing term “group”, “circle”, or both (group = circle with a name)? | The current Appy UI mixes “Groups” and “circle / group name”. |
| L02 | Which roles ship in v1: owner/member only, or owner/curator/member/guest? | Roles change the grant and removal model. |
| L03 | Can a person be added to a local group without their consent, and what does the invite show them? | A group profiles third people; ties to B02/B03. |
| L04 | Can groups nest or alias (family ⊂ close friends), or is membership flat? | Nesting affects projection and key inheritance. |
| L05 | Which MyFamily categories/traits are in the default group projection, and are the seven categories P until selected? | The projection is the privacy boundary. |
| L06 | Is the member list visible to members, or only to the owner? | The list itself leaks the local graph. |
| L07 | Can the same person be in several groups with different projections? | Assumed yes (BSP-M12), but the UI needs to explain it. |
| L08 | Who can invite or remove: owner only, or curators/members too? | Determines the signed action set. |
| L09 | On removal, is the old group history kept for the removed member, deleted, or re-encrypted? | Revocation is forward-only; copies remain. |
| L10 | Are group posts a feed, a chat, or both? Chat is a separate tab today. | Two different retention and consent models. |
| L11 | Can a public group be joined from an S card, or only by local invite? Who moderates it? | Nety moderation and discoverability. |
| L12 | What does group deletion/erasure propagate to member copies and invites? | Honest deletion limits. |
| L13 | Max members and size per group; what is the key-rotation cost with offline members? | Rotation can be expensive and asynchronous. |
| L14 | Does MyFamily remain the only person editor, or can MyNet create a simplified record inline? | The plan assumes MyFamily edits; the UI may want quick-add. |

### Questy session 1 — readout (2026-11-17)

Closed by the owner after 14 answers. The remaining questions stay open.

**Decided**

| Q | Decision |
|---|---|
| Q001 | Browsy pulls public pages on demand; pages do not query identity or vault. |
| Q002 | Pull failures show typed states `idle · pulling · no-access · error` + retry. |
| Q003 | Chrome/Edge use WebCrypto; Firefox/Safari use the tweetnacl fallback in v1. |
| Q004 | Pull scope is the full DOM, including forms and hidden fields. |
| Q005 | Persistent indicator + **Stop** + per-site allowlist; no silent pulls. |
| Q006 | Include normal `input`/`textarea`/`select` values; exclude password/secret/hidden fields, cookies and tokens. |
| Q007 | v1 stores keys in plain `chrome.storage.local`; encrypted vault is M2. |
| Q008 | No web→extension portability; the web identity is fallback/local. |
| Q009 | A web local identity is hidden but kept; the extension hash is canonical. |
| Q010 | Canonical `flove-identity/1`; `flove-browsy/1` is a read-only view. |
| Q012 | v1 pulls only flove.org/localhost/127.0.0.1; no `<all_urls>`, no `file://`. |
| Q013 | Without the extension, the web creates a full local identity with a warning, mobile included; still not portable. |
| Q014 | Recovery is a 12-word seed in v1; social quorum later. |

**Open**

| Item | Why it is still open |
|---|---|
| K08 / Q011 | How the root reaches Nety: encrypted export, native messaging or seed phrase. |
| K09 | Exact manifest permission set for the confirmed origin scope. |
| K12 / Q015 | App sessions: capability object, JWT or opaque handle. |
| K13 / Q016 | Release standard across Chrome/Edge, Firefox and Safari. |
| K14 / Q017 | Logging/redaction beyond the DOM pull rules. |
| K15 | Warning UX for a non-portable local key. |
| K16 / K17 / Q018 | Masks and cross-device sync. |
| K18 | Test matrix for installed/not, `file://`, storage blocked, locked worker. |

---

## Suggested survey order

1. **Batch 1:** A01, A03, A05 — the identity baseline.
2. **Batch 2:** B01, B03, B05 — third-party boundaries.
3. **Batch 3:** C01, C04, C06 — grant mechanics.
4. **Batch 4:** D01, D03, D05 — the local net.
5. **Batch 5:** E01, E03, E04 — derivation exposure.
6. **Batch 6:** F01, F02, F05 — Nety readiness.
7. **Batch 7:** G01, G02, G05 — vault and bridge.
8. **Batch 8:** H02, H04, H05 — usability of privacy.
9. **Batch 9:** I01, I03, I06 — legal/ethics.
10. **Batch 10:** J01, J03, J06 — integration.
11. **Batch 11:** L01, L03, L06 — MyNet groups, consent and member visibility.
12. **Batch 12:** F3, F6, Q5–Q7, Q9, Q14, Q19–Q23, Q27–Q29, Q31–Q32 — the moved pre-build pendings.

## Pre-build pendings — 2026-11-18

> Moved from `pre-build/open-issues.md`. Answer with letters A–D; ★ is a default.

### Q5 · O05 · What does group deletion propagate to member copies?
A. Local delete only; members keep copies.
B. ★ Send a signed tombstone; members delete cached group data; copies may
   remain and are labelled.
C. Rotate the key and archive; no delete.
D. Owner deletes; members keep everything.

**Answer (A–E):** ____

### Q6 · O06 · Max members and key rotation with offline members?
A. ★ 10 members; rotate on removal; offline members miss new posts until the
   next pull.
B. 50 members; rotate; queue updates for offline members.
C. No hard limit; best-effort rotation.
D. 10 members; no rotation until every member is online.

**Answer (A–E):** ____

### Q7 · O07 · Is the default group projection just the 5 percentages, or the raw 7×5 too?
A. ★ 5 percentages only; raw 7×5 is opt-in per group.
B. Raw 7×5 + percentages by default.
C. Per-area toggle: each area can be shared or hidden.
D. 5 percentages + a per-area dominant type.

**Answer (A–E):** ____

### Q9 · O09 · What is “disown”?
A. ★ Retire it from v1; keep `revoke` only.
B. Define it as a local reputation action (−10 local).
C. Move it to Nety later.
D. Keep it as a UI-only label with no data effect.

**Answer (A–E):** ____

---

### Q14 · O14 · What is an app session? (A05)
A. ★ Signed capability object, short TTL, scoped paths/actions.
B. JWT.
C. Opaque handle stored by Browsy.
D. One-shot signature per action.

**Answer (A–E):** ____

---

### Q19 · O19 · Offline queue?
A. ★ Extension queues; host forwards when the peer is back.
B. Host queues for offline peers.
C. No queue in v1.
D. Both queue.

**Answer (A–E):** ____

---

### Q20 · O20 · Page API allowlist?
A. Current list: status, read, save L record, list groups, feed, save L post,
   create invite.
B. ★ Read + save L records/posts; **groups and invites only in the extension
   UI**.
C. Read-only page API.
D. Full CRUD from the page.

**Answer (A–E):** ____

### Q21 · O21 · XSS boundary?
A. ★ L-only page API + user gesture for writes.
B. L-only, no gesture.
C. Read-only page API.
D. Full API with origin allowlist only.

**Answer (A–E):** ____

### Q22 · O22 · Panic/lock wipe scope?
A. ★ Wipe keys + session; records stay encrypted.
B. Wipe the whole vault.
C. Lock only, no wipe.
D. Configurable.

**Answer (A–E):** ____

### Q23 · O23 · Logs?
A. ★ Error codes only.
B. Redacted metadata.
C. Full logs by opt-in.
D. No logs.

**Answer (A–E):** ____

---

### Q27 · O27 · Default L grant TTL? (C06)
A. ★ 7 days.
B. 24 hours.
C. 30 days.
D. No expiry.

**Answer (A–E):** ____

### Q28 · O28 · Revocation key rotation? (C07)
A. ★ Rotate on every member removal.
B. Rotate manually.
C. Per-group key only.
D. No rotation.

**Answer (A–E):** ____

### Q29 · O29 · Is `copy` ever allowed? (C04)
A. ★ Never; every share is a reference + encrypted projection.
B. S only.
C. Allowed with a warning.
D. Allowed.

**Answer (A–E):** ____

---

### Q31 · O31 · When does the DPIA/privacy review happen?
A. ★ Before any L sharing.
B. Before S/Nety only.
C. After the MVP.
D. Not needed.

**Answer (A–E):** ____

### Q32 · O32 · What does erasure propagate?
A. ★ Signed tombstone + local delete; copies may remain and are labelled.
B. Local delete only.
C. No delete.
D. Re-encrypt everything.

**Answer (A–E):** ____

---

### F3 · O05/O06/O07 · Defaults under self-managed groups
No moderation, no public groups. Pick the v1 defaults:

A. Deletion: tombstone (O05-B); max 10 members/rotate (O06-A); projection 5
   percentages (O07-A).
B. Deletion: local only (O05-A); max 50/queue (O06-B); raw 7×5 by default (O07-B).
C. Deletion: archive/rotate (O05-C); no hard limit (O06-C); per-area toggle (O07-C).
D. Deletion: owner only (O05-D); no rotation (O06-D); percentages + dominant
   type (O07-D).

**Answer (A–D):** ____

### F6 · O30 · Agreement vs subject consent
The owner lets a member’s Wizy consult selected MyFamily data. Does the
**subject** (the person the record is about) also consent?

A. Owner-only agreement; no subject consent.
B. Owner agreement + subject consent for L/S sharing.
C. Subject consent only for S/Public; L is owner-only.
D. No third-person record sharing.

**Answer (A–D):** ____

<a id="questy-proposals"></a>
## Historical record

The full pre-2026-11-23 text of this chapter is preserved in
`development/archive/2026-11-23/plans/docs/work.md` with checksums in the partition's
`SHA256SUMS`. This plan keeps the accepted decisions and the archived-note index only.

<!-- historical anchors kept for evidence resolution
<a id="agentsmd-resolved"></a>
<a id="authoring-presets"></a>
<a id="commands-reference"></a>
<a id="conflict-resolution-skill-standard-vs-html-form"></a>
<a id="deferred"></a>
<a id="error-handling-fallbacks"></a>
<a id="follow-ups-applied-2026-11-20"></a>
<a id="frontend"></a>
<a id="naming-resolved"></a>
<a id="p001-resolved-archive-resolved-items-instead-of-deleting"></a>
<a id="p002-resolved-addon-row-layout-and-continue-config"></a>
<a id="p003-resolved-info-texts-for-archive-pro-scripts"></a>
<a id="p004-resolved-human-icon-and-use-case-button"></a>
<a id="p005-resolved-scripts-row-layout-and-demonstrative-use-cases"></a>
<a id="p006-resolved-move-questy-out-of-agentsskills"></a>
<a id="p007-resolved-consolidate-questy-html"></a>
<a id="p008-resolved-standardsmd-for-questy"></a>
<a id="p009-resolved-tour-html"></a>
<a id="paths"></a>
<a id="phase-1-config-check-setup-steps-112"></a>
<a id="phase-2-project-context-steps-1320"></a>
<a id="phase-3-perspective-the-thinking-hats-as-type-steps-2148"></a>
<a id="phase-4-addons-core-scripts-integrations-steps-4968"></a>
<a id="phase-5-workflows-pr-standards-steps-6980"></a>
<a id="phase-6-output-export-steps-8188"></a>
<a id="phase-7-scan-understand-steps-8995"></a>
<a id="phase-8-generate-process-close-steps-96100"></a>
<a id="proposals-format"></a>
<a id="q061q090-hitos-y-estndares-2026-11-20"></a>
<a id="q091q120-hitos-tasks-y-stage-2026-11-20"></a>
<a id="q121q141-conflictos-orden-y-procedures-2026-11-20"></a>
<a id="q142q150-cierre-de-la-sesin-2026-11-20"></a>
<a id="q151q153-correccin-de-la-auditora-y-filtros-del-work-2026-11-20"></a>
<a id="q154-registro-de-jev-y-cierre-de-lote-2026-11-20"></a>
<a id="q155-optimizy3-sobre-developmentindexhtml-2026-11-20"></a>
<a id="q156-optimizy4-sobre-developmentindexhtml-2026-11-20"></a>
<a id="questy-standards"></a>
<a id="questy-usecase"></a>
<a id="rules"></a>
<a id="structure-resolved"></a>
<a id="version-changelog"></a>
<a id="what-questy-creates-for-other-projects"></a>
-->

## Source index

### bridges/oasis.md — 2026-08-01

- Archive: `development/archive/old/bridges/oasis.md`
- Stable home: `development/standards/tasks/tasks.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/browsy-questions.md — 2026-08-01

- Archive: `development/archive/old/browsy/browsy-questions.md`
- Live home: `development/plans/tasks/tasks.md#browsy-questions` (this page)
- Status: live questions A–L and pre-build pendings are owned here; the 244-answer log stays in the archive.

### browsy/pre-build/README.md — 2026-11-17

- Archive: `development/archive/old/browsy/pre-build/README.md`
- Stable home: `development/standards/tasks/tasks.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/rationale.md — 2026-11-17

- Archive: `development/archive/old/browsy/rationale.md`
- Live detail: `development/plans/plans/plans.md#rationale`
- Status: accepted facts in the stable page; rationale detail owned by the child plan.

### browsy/spec.md — 2026-11-17

- Archive: `development/archive/old/browsy/spec.md`
- Stable home: `development/standards/tasks/tasks.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/2026-11-17-appy-authy-mynet.md — 2026-11-17

- Archive: `development/archive/old/plans/2026-11-17-appy-authy-mynet.md`
- Stable home: `development/standards/tasks/tasks.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/2026-11-19-authy-open-questions.md — 2026-11-19

- Archive: `development/archive/old/plans/2026-11-19-authy-open-questions.md`
- Stable home: `development/standards/tasks/tasks.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/2026-11-21-app-database-stages.md — 2026-11-21

- Archive: `development/archive/old/plans/2026-11-21-app-database-stages.md`
- Stable home: `development/standards/tasks/tasks.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/puzzy.md — 2026-08-01

- Archive: `development/archive/old/plans/puzzy.md`
- Stable home: `development/standards/tasks/tasks.md`
- Status: summarised in the stable page; no open decision is recorded here.

### proposals/frontend-wizy.md — 2026-11-19

- Archive: `development/archive/old/proposals/frontend-wizy.md`
- Stable home: `development/standards/tasks/tasks.md`
- Status: summarised in the stable page; no open decision is recorded here.
