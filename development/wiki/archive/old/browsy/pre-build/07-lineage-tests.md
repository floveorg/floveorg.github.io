# 07 · Invite lineage and test fixtures

> Lineage is in v1. It is local metadata plus a visible tree; it is not a
> public/Nety feature.

## Lineage model

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

- `parent` is the code that invited the inviter; `null` for a root invite.
- The tree is `parent → inviter → invitee`.
- Lineage is **M/L**; it never goes to Nety in v1.
- Revoke marks `status: "revoked"`; it does not erase the tree.
- “Disown” is a reputation action in the old Appy UI; **defer/retire** it until
  its meaning is defined.

## MVP UI

1. Invites panel: generate one code, copy, validate, revoke.
2. “See lineage”: a simple tree (root → you → invitees).
3. A used code shows the invitee (display name/alias) if the invitee accepted
   locally.
4. No public group join, no discovery.

## Fixtures

### People

| Fixture | Person | Areas | Expected percentages |
|---|---|---|---|
| `ana` | Ana (P by default) | 7 selections: 2 cousin, 2 sibling, 1 grandparent, 1 parent, 1 partner | 28.6 / 28.6 / 14.3 / 14.3 / 14.2 |
| `bob` | Bob (P by default) | 5 selections: 1 each | 20 / 20 / 20 / 20 / 20 |
| `charlie` | Charlie (P by default) | 3 selections: 3 partner | 0 / 0 / 0 / 0 / 100 |

### Groups

| Group | Members | Visibility | Projection |
|---|---|---|---|
| `family` | Ana (owner), Bob | `group` | 5 percentages |
| `friends` | Ana (owner), Charlie | `group` | 5 percentages + raw areas opt-in |
| `work` | Bob (owner), Ana | `local` | 5 percentages |
| `invitees` | Ana (owner), one invitee | `group` + label `Invitees` | single-use code; S stats card count |

### Bundles

| Fixture | Expected |
|---|---|
| `bundle.valid` | signature verifies; class L; 5 percentages only |
| `bundle.tampered` | one percentage changed → verify fails |
| `bundle.expired` | grant `expiresAt` in the past → read rejected |
| `bundle.revoked` | group version++ → old key rejected |
| `bundle.p-leak` | contains `areas` without opt-in → rejected |

### Acceptance cases

1. Create identity → lock → unlock; wrong passphrase fails.
2. Add Ana; defaults to P; 7×5 answers; percentages sum to 100; Wizy reads P locally.
3. Create `family` with Ana/Bob; projection has 5 bars and no raw areas.
4. Ana is also in `work`; same `personId`, different group.
5. Post to `family`; reload; post survives.
6. Remove Bob → version++ → Bob cannot decrypt new posts.
7. Generate invite → accept as Bob → lineage shows parent.
8. Sign a consult agreement for Bob’s Wizy; it sees only the scope; revoke stops it.
9. Page calls `saveRecord` with P → stored L (page writes are L-only).
10. No Nety call; no Public control.
11. `file://` and localhost both pass.
12. Create an `Invitees` group; one code admits one person who self-joins; the owner sees the count; the S card contains only counts, not details.

## E2E smoke

- Load the built extension in Chrome (`channel: 'chrome'`, persistent context).
- Open the popup; create identity; lock; unlock.
- Add Ana/Bob; create family; post; reload.
- Open a localhost page; call `flove.browsy.status()` and `listRecords()`.
- Assert no P and no key methods.
