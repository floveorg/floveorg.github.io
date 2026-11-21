# 09 · Consult agreements (Wizy across local groups)

> Decision: an owner can let selected members’ **Wizy** consult selected
> MyFamily data through an explicit, signed, revocable agreement. No group
> moderation; each owner manages their own local groups.

## Actors

| Actor | Meaning |
|---|---|
| **Owner** | the person who created the MyFamily record and the local group |
| **Subject** | the person the record is about (may be a third person) |
| **Member** | another user/peer allowed into a shared group |
| **Wizy** | the member’s local derivation runtime, inside their Browsy |

The owner controls the record. The member’s Wizy never receives the raw P
record; it receives a scoped consultation capability and returns derived
answers.

## Agreement object — `flove-consult/1`

```json
{
  "schema": "flove-consult/1",
  "id": "c_…",
  "owner": "bafk…",
  "member": "bafk…",
  "wizy": "bafk…",
  "scope": {
    "personIds": ["p_ana"],
    "groupIds": ["g_family"],
    "paths": ["percentages", "areas.attention"],
    "capabilities": ["view", "derive"]
  },
  "purpose": "recommend a gift",
  "expiresAt": "2026-12-18T00:00:00Z",
  "version": 1,
  "signature": "ed25519:hex"
}
```

- `capabilities`: `view`, `derive`, `aggregate`; **no `copy`**.
- `scope` is the intersection of person/group/paths; the most specific wins.
- `purpose` is shown in the UI and in Wizy’s explanation.
- Revocation bumps `version`; the next pull refuses the old agreement.

## Flow

1. Member asks to consult a person/group (or the owner offers it).
2. Owner picks: person(s), group(s), paths, capabilities, purpose, expiry.
3. Authy signs the agreement; the owner stores it locally.
4. Member’s Wizy pulls under the agreement and derives locally.
5. Wizy shows “used: <person/group> · <paths> · purpose”.
6. Owner revokes or shortens expiry; version++.
7. Old derived results are labelled as old; copies cannot be recalled.

## What crosses groups

Wizy may combine:

- the owner’s local groups;
- the member’s own local groups;
- the agreements between them.

It does **not** merge raw records into a central store. Cross-group results are
derived answers, not a new shared group. This is the “crossing info from
different local groups from different users” path: each user manages their own
groups; only signed consult agreements connect them.

## No group moderation

- Local groups have **no moderation**.
- Public/S groups and moderation are deferred with Nety.
- The owner is the only authority over their local group.

## Subject consent

The agreement is between owner and member. The **subject** is a third person.
The open question is whether the subject must also consent before the owner
lets another member’s Wizy consult the record. Options:

1. Owner-only agreement; no subject consent (fast, ethically weak).
2. Owner agreement + subject consent for L/S sharing (recommended for real
   sharing).
3. Subject consent only for S/Public; L is owner-only.
4. No sharing of third-person records at all.

## UI

- MyFamily person → “Allow a Wizy to consult…”.
- Choose member, scope, purpose, expiry.
- The group card shows “consulted by N Wizys” with a list the owner can revoke.
- The member sees the agreement in their Browsy/Wizy, not the raw record.

## Open

- Does the subject consent? (O30 follow-up)
- Can a member delegate the consultation to another Wizy?
- What does `aggregate` allow across groups?
- How are consult agreements audited/exported?
- Do agreements expire by default (7 days, like L grants)?
