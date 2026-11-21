# 06 · Bridge and threat model

> The page is untrusted. The bridge exposes a small API; it never exposes the
> vault, the root key, P data or signing.

## Boundary

```
page (flove.org / localhost)
  window.flove.browsy        ← MAIN-world bridge
        │ window.postMessage (origin-checked)
  isolated content script    ← allowlist + schema
        │ browser.runtime.sendMessage
  background service worker ← vault + policy
        │
  IndexedDB / native host
```

The MAIN-world bridge defines `window.flove.browsy`; the isolated content
script is the only one that talks to the extension. The page never gets a
`CryptoKey`, a private key or raw P records.

## API allowlist (v1)

| Method | Returns | Page can write? |
|---|---|---|
| `status()` | `{hasIdentity, level, locked, identityHash?}` | no |
| `info()` | version + status | no |
| `saveRecord(record)` | `{id, class}` | **forces L** |
| `listRecords()` | only L/S records | no |
| `listGroups()` | group cards (name, member count, 5 bars) | no |
| `listFeed({groupId?})` | L posts | no |
| `savePost({groupId, body})` | L post | yes (L only) |
| `createInvite()` | `{code}` | yes (local) |

**Never exposed:** `sign`, `unlock`, `exportRoot`, `getKeypair`, raw `P`, the
vault, keepers, or arbitrary storage.

## Rules

1. Origin allowlist: `https://flove.org`, `http://localhost`, `http://127.0.0.1`.
2. Check `event.source === window` and `event.origin === location.origin`.
3. Validate every message with a schema; unknown fields are rejected.
4. Page-originated records are forced to **class L**; the page cannot create P
   or S.
5. `listRecords`/`listFeed` filter out P before returning.
6. Rate-limit per second; drop oversized messages.
7. No `eval`, no dynamic script injection, no remote code.
8. Logs redact record bodies, hashes and keys.

## Threats

| Threat | Impact | Mitigation |
|---|---|---|
| XSS in a flove app calls the bridge | Reads/writes L records | L-only API; no P; origin check; CSP; rate limit |
| Malicious page on localhost | Calls the bridge | Same allowlist; no P; user gesture for writes |
| Compromised content script | Talks to background | Allowlist + schema + no secrets in content |
| Malicious peer sends a bundle | Forged person/group data | Verify signature, grant and version; reject unknown schema |
| Replay of an old post/grant | Stale/duplicate data | Nonce + timestamp + monotonic version |
| Stolen device | Vault access | Passphrase/Argon2id, lock, panic wipe, no plaintext logs |
| Extension update supply chain | Full compromise | Signed builds, pinned deps, review, reproducible package |

## Test cases

1. Page calls `saveRecord` with `class: "P"` → stored as L.
2. Page calls `listRecords` → no P record returned.
3. Foreign origin posts a message → ignored.
4. Oversized message → rejected.
5. Tampered post/bundle → rejected.
6. Locked vault → API returns `locked`, no data.
7. `sign`/`getKeypair` are not defined on `window.flove.browsy`.
