# Pre-build answers — closed log

> Status: **answered/closed log** (2026-11-18). The unanswered issues moved to
> [`browsy-questions.md`](../browsy-questions.md) §Pre-build pendings.
>
> ★ = the recommended default that was used unless the answer table says otherwise.

## How to read

1. The **answer table** above is the current decision.
2. The blocks below keep the options for traceability.
3. Unanswered items live in `browsy-questions.md` §Pre-build pendings.

---

## Answers logged 2026-11-18

| Q | Answer | Note |
|---|---|---|
| 1 | **A** | Local group; no notification; sharing needs invite/accept. |
| 2 | **B** | Owner sees full member list; members see a count. |
| 3 | **A** | Owner only; one group list with free names + optional `Invitees` label (F1 closed). |
| 4 | **D** | Delete for everyone — **intent**, not enforceable for copies; document the limit (F2=4). |
| 8 | **P** | Private by default; Wizy may read locally on the owner’s device. |
| 10 | **A** | L1 SelfAuth + L3 Telegram verified only; email/phone later. |
| 11 | **D** | Pin risa + keep Authy nonce+DM fallback. |
| 12 | **B** | L1 UI word: **Self**. |
| 13 | **B** | Hide a bare Telegram link until verified. |
| 15 | **A** | Rust host. |
| 16 | **Invite code + Telegram deep link** | Authy authentication on click; risa is a redirect to Authy ID; option 3 accepted (F4 closed). |
| 17 | **B** | WebSocket + JSON for v1. |
| 18 | **A** | Signed host release + version check. |
| 24 | **B** | Retire “Else”. |
| 25 | **A** | Label **Browsy entry** / **Browsy host** (F5 closed). |
| 26 | **A** | JSON path with array ranges. |
| 30 | **Agreement** | Owner allows selected members’ Wizys to consult selected MyFamily data (see `09-consult-agreements.md`; F6). |

**5/6/7:** no more group moderation; focus on crossing info from different users’ self-managed local groups. O05/O06/O07 moved to F3 in the pendings.

**Unanswered:** moved to `browsy-questions.md` §Pre-build pendings.

## Follow-ups

> F3 and F6 moved to `browsy-questions.md` §Pre-build pendings; the remaining Qs are in the same section.

### F1 · O03 · Group concepts — **closed**
**Decided 2026-11-18:** one group list, free names, optional labels; `Invitees`
is a label for an invite-only group where each code admits one person who joins
themselves. No separate local/invitee list.

1. **Local group** (owner’s records) vs **Invitee group** (accepted members).
2. **Private group** vs **Shared group**.
3. **Group** vs **Circle** (circle = accepted peers).
4. One group object with a `status: local|shared` field.

**Answer:** Single list + `Invitees` label
### F2 · O04 · Is “delete for everyone” enforceable? — **closed**
**Decided 2026-11-18: 4** — keep “delete for everyone” as intent; document that
copies cannot be recalled. Implementation: tombstone + remote delete request +
label copies.

Options kept for history:

1. Tombstone + local delete + remote delete request; label copies that may remain.
2. Tombstone + local delete only; no remote request.
3. Rotate key + archive; old copies remain.
4. Keep “delete for everyone” as intent, document the limit.

**Answer:** 4
### F4 · O16 · Invitations/discovery via Telegram — **closed**
**Decided 2026-11-18:** option **3 + Authy**: invite code + QR/Telegram deep
link; clicking starts Authy authentication; risa is a **redirect to the Authy
ID**, not a separate root. External invitees get an identity hash and can join
MyFamily. risa-signed and Authy-signed proofs are both accepted.

Options kept for history:

1. Telegram username search + **risa-signed public directory JSON**
   (`@user → identityHash`), then a signed contact card.
2. Telegram numeric ID + deep link (`t.me/bot?start=…`) + QR/manual fingerprint
   fallback.
3. Invite code + QR only; no username directory.
4. Local mDNS/QR only; Telegram only carries the invite code, not the directory.

A hybrid is possible: (1) for discovery, (2) for pairing, (3) as fallback.
**Privacy risk:** username search leaks queries; prefer hashed lookup or
on-device directory.

**Answer:** 3 + Authy
### F5 · O25 · Two Browsy chips — **closed**
**Decided 2026-11-18:** label them **Browsy entry** / **Browsy host** in the
decentral index chips too. They are the same product in two roles.

Options kept for history:

1. Label them **Browsy entry** / **Browsy host**.
2. Merge into one Browsy chip.
3. Keep two “Browsy” chips with a footnote.
4. Rename to Extension / Host.

**Answer:** A

## A · Groups and MyFamily

### Q1 · O01 · Can a person be added to a local group without their consent?
A group is the owner’s local projection; nothing leaves the device until the
person becomes a peer. The question is consent to be *listed* in a shared group.

A. ★ Yes: the group is local; no notification; sharing to the person needs an
   invite/accept. The person can leave when they join.
B. Yes, but the invite shows the group and its members; the person can decline.
C. No: every member must accept an invite before appearing in a shared group.
D. No: groups are self-declared only; no third-person membership.

**Answer:** A
### Q2 · O02 · Is the member list visible to all members?
A. Yes: every member sees the full member list.
B. ★ No: only the owner sees the full list; members see a member count.
C. Members see only people they already know.
D. Configurable per group.

**Answer:** B
### Q3 · O03 · Who can invite or remove members?
A. ★ Owner only.
B. Owner invites; owner and members can invite; owner removes.
C. Owner + curator roles; members cannot.
D. Configurable per group.

**Answer:** A
### Q4 · O04 · On removal, what happens to the old group history?
A. ★ The removed member keeps copies they already have; new posts are
   inaccessible; the UI labels the old copy.
B. The owner deletes or re-encrypts the history for everyone.
C. The removed member loses the key; the owner keeps history; no re-encryption.
D. Delete the history for everyone.

**Answer:** D
### Q8 · O08 · Default class for a new MyFamily person?
A. ★ **L** (shareable) — the current MyFamily use case.
B. **P** (private) — stricter default.
C. Ask at creation: P or L.
D. Always P; L only after an explicit share.

**Answer:** B

## B · Authy

### Q10 · O10 · Are L2 email and L4 phone in the first build?
A. ★ No: first build is L1 SelfAuth + L3 Telegram verified; email/phone later.
B. Add L2 email; phone later.
C. Add L1–L4.
D. L1 only; no external proof in v1.

**Answer:** A
### Q11 · O11 · Which key signs the risa claim, and how is it pinned?
A. Pin the risa key in the Browsy release; rotate through a signed update.
B. Trust on first use; the user confirms the fingerprint.
C. Use Central/Nety web-of-trust; no pin.
D. ★ Pin risa **and** keep the Authy nonce+DM as a fallback.

**Answer:** D
### Q12 · O12 · What is the L1 UI word?
A. ★ **SelfAuth**.
B. **Self**.
C. **Unverified**.
D. **Local only**.

**Answer:** B
### Q13 · O13 · How does a bare Telegram link appear in the UI?
A. ★ “Linked · unverified” with a warning; it stays L1.
B. Hide it until verified.
C. Show it only in advanced settings.
D. Treat it as verified.

**Answer:** B

## C · Native host

### Q15 · O15 · Host language?
A. ★ Rust: single binary, QUIC, mDNS.
B. Go: simpler build, smaller team surface.
C. Node: shared TypeScript, heavier runtime.
D. Start with Node, rewrite later.

**Answer:** A
### Q16 · O16 · Peer discovery?
A. ★ mDNS + a manual `host:port` fallback.
B. mDNS only.
C. Manual pairing only.
D. Nety/DHT lookup.

**Answer:** C + Authy
### Q17 · O17 · Wire framing?
A. QUIC + CBOR.
B. ★ WebSocket + JSON for v1; revisit QUIC later.
C. Unix socket + JSON (same device only).
D. HTTP + signed JSON.

**Answer:** B
### Q18 · O18 · Host update channel?
A. ★ Signed release; the extension checks the host version.
B. OS package manager only.
C. Manual download only.
D. No update path in v1.

**Answer:** A

## E · Model labels

### Q24 · O24 · “Else”?
A. Define it: non-flove web/apps that use Authy and keep records L.
B. ★ Retire the chip; the branch is not a product.
C. Rename it “Other apps”.
D. Make it a separate product.

**Answer:** B
### Q25 · O25 · The two Browsy chips?
A. ★ Label them **Browsy entry** and **Browsy host**.
B. Merge into one Browsy chip.
C. Keep two “Browsy” chips with a footnote.
D. Rename to Extension / Host.

**Answer:** A

---

## F · Grants (confirm the defaults)

### Q26 · O26 · Grant unit? (C01)
A. ★ JSON path with array ranges.
B. Whole record/file.
C. Field-level.
D. Slice-level.

**Answer:** A

## G · Legal and ethics

### Q30 · O30 · Can a person record be shared without the subject’s consent?
A. ★ No: local private use only; sharing L/S requires consent.
B. Yes for L, no for S.
C. Yes with a notice.
D. Yes.

**Answer:** Agreement

## Z · Already decided (do not re-answer)

| Decision | Value |
|---|---|
| Authy gate | L3 verified Telegram (risa or Authy claim); bare presence is L1 |
| MyFamily profile | 7 areas × 5 replies → 5 type percentages |
| 5 types | Cousin · Sibling · Grandparent · Parent · Partner |
| Groups | Flat, no nesting, no public groups in v1 |
| Transport | Native messaging host |
| Nety/Public | Postponed for v1 |
| Authy key | `flove:authy/1` canonical; `flove:authy` legacy |
| Social/Public | Synonyms; S is the class |
| Local | Shareable with named peers/groups |
| Personal | Private, owner only |
| Lineage | Included in v1 |
| Projection default | Display name + 5 percentages (raw 7×5 opt-in) unless O07 changes it |
