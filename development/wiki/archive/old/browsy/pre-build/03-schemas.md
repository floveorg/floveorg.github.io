# 03 · Schemas

> Naming convention: **schema ids** use `flove-*` + version; **storage keys**
> use `flove:*` + version. This keeps the document type separate from where it
> is stored.

## Decision: `flove:authy/1`

Use **`flove:authy/1`** as the canonical storage key and `flove-authy/1` as the
schema id. It is versioned, matches the other schemas, and leaves room for
migration:

1. Read `flove:authy/1`.
2. If missing, read legacy `flove:authy`.
3. Migrate to `/1`, set `legacy: true`, keep the old key for one release.
4. Never write a new state without a version.

`flove-auth/1` stays reserved for a **risa presence claim**, not for the Authy
state.

## Identity — `flove-identity/1`

```json
{
  "schema": "flove-identity/1",
  "publicKey": "ed25519:hex",
  "identityHash": "bafk…",
  "source": "extension" | "web",
  "createdAt": "2026-11-17T00:00:00Z",
  "legacy": false
}
```

`identityHash = CIDv1(sha256(ed25519_pubkey))`; the same value is the Nety
PeerId.

## Authy state — `flove-authy/1`

```json
{
  "schema": "flove-authy/1",
  "level": "L1" | "L2" | "L3" | "L4",
  "identities": [],
  "channels": {
    "email": { "state": "none" | "linked" | "verified", "proof": null },
    "telegram": { "state": "none" | "linked" | "verified", "proof": null, "source": "risa" | "authy" },
    "phone": { "state": "none" | "linked" | "verified", "proof": null },
    "bio": { "state": "none" | "filled" }
  },
  "keepers": { "local": null, "social": null },
  "updatedAt": "2026-11-17T00:00:00Z",
  "legacy": false
}
```

A bare `linked` Telegram is L1. `verified` with `source: "risa"` or `"authy"`
is L3.

## Person profile — `flove-portrait/1`

```json
{
  "schema": "flove-portrait/1",
  "personId": "p_…",
  "displayName": "Ana",
  "class": "P" | "L" | "S",  // new person defaults to P
  "areas": {
    "attention": [1,0,0,0,0],
    "contact":   [0,1,0,0,0],
    "influence": [0,0,1,0,0],
    "feedback":  [0,0,0,1,0],
    "gifting":   [0,1,0,0,0],
    "sharing":   [0,0,0,0,1],
    "money":     [1,0,0,0,0]
  },
  "percentages": {
    "cousin": 28.6,
    "sibling": 28.6,
    "grandparent": 14.3,
    "parent": 14.3,
    "partner": 14.2
  },
  "updatedAt": "2026-11-17T00:00:00Z"
}
```

Each area is a 5-slot vector (`col1`…`col5`). `percentages` is derived, not
hand-edited. See [`04-myfamily-profile.md`](04-myfamily-profile.md).

## Group — `flove-group/0.1`

```json
{
  "schema": "flove-group/0.1",
  "id": "g_…",
  "name": "Family",  // free name, one single group list
  "kind": "family" | "friends" | "work" | "custom",
  "labels": ["invitees"],
  "invitePolicy": "single" | "multi",
  "memberIds": ["p_ana", "p_bob"],
  "roles": { "p_ana": "owner", "p_bob": "member" },
  "defaultClass": "L",
  "visibility": "local" | "group",
  "card": {
    "public": { "inviteeCount": 3, "activityCount": 12 },
    "local": { "members": true, "roles": true, "posts": true, "lineage": true }
  },
  "projection": "myfamily-profile/1",
  "keyId": "k_…",
  "version": 3,
  "signature": "ed25519:hex"
}
```

**No `parentId`** — groups are flat. **No public group join** in v1. One
owner list, free names, optional labels. `Invitees` means invite-only, one
person per code, self-join. The `card.public` counts are an **S stats card**;
`card.local` details are **L**.

## Consult agreement — `flove-consult/1`

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

No `copy`; only scoped `view`/`derive`/`aggregate`. Revoke bumps version.

## Grant — `flove-grant/1` (proposed)

```json
{
  "schema": "flove-grant/1",
  "grantor": "bafk…",
  "grantee": "bafk…" | "group:g_…",
  "bundle": "b_…",
  "paths": ["displayName", "percentages"],
  "capabilities": ["view", "derive", "aggregate"],
  "expiresAt": "2026-12-17T00:00:00Z",
  "contentKey": "k_…",
  "version": 3,
  "signature": "ed25519:hex"
}
```

## Post — `flove-post/1`

```json
{
  "schema": "flove-post/1",
  "id": "post_…",
  "author": "bafk…",
  "groupId": "g_…",
  "visibility": "myNet" | "group",
  "body": "…",
  "class": "L",
  "createdAt": "2026-11-17T00:00:00Z",
  "signature": "ed25519:hex"
}
```

No `public` visibility in v1.

## Invite — `flove-invite/1`

```json
{
  "schema": "flove-invite/1",
  "code": "FLOVE-…",
  "inviter": "bafk…",
  "parent": "FLOVE-…" | null,
  "uses": 1,
  "expiresAt": "2026-12-17T00:00:00Z",
  "status": "active" | "revoked" | "used",
  "signature": "ed25519:hex"
}
```

## Bundle — `flove-bundle/0.1`

```json
{
  "schema": "flove-bundle/0.1",
  "owner": "bafk…",
  "class": "P" | "L" | "S",  // new person defaults to P
  "documents": [],
  "grants": [],
  "signature": "ed25519:hex"
}
```

## Rules

1. `P` never appears in a bundle with `class: "L"` or `"S"`.
2. `S` is **Social = Public**; it is the only class allowed on Nety.
3. `L` is shareable with named peers/groups; promotion to `S` is explicit.
4. Every schema has a version; unknown versions are rejected, not guessed.
5. The signature covers canonical JSON without the `signature` field.
