# 05 · Native host transport

> Decision: **native messaging host**, not browser WebRTC. MV3 cannot open raw
> sockets or run mDNS; the host owns the local network. **Rust** host,
> **WebSocket + JSON** for v1, signed release + version check.

## Shape

```
Browsy extension (MV3)
  background service worker
        │  chrome.runtime.connectNative / sendNativeMessage
        ▼
Browsy native host (Rust/Go/Node)
  mDNS / UDP discovery
  local WebSocket or QUIC listener
  peer handshake + signed frames
        │
        ▼
another Browsy host on the LAN
```

The host does **not** own the vault. Authy keys and P data stay in the
extension; the host moves signed L bundles and group posts.

## Invitations vs LAN discovery

These are different problems:

- **LAN discovery** (host): mDNS + manual `host:port`; no Telegram needed.
- **Invitation discovery** (Browsy UI): an **invite code + QR**, sent through
  Telegram as a deep link. Clicking it can start **Authy authentication** for
  the invitee, who then gets an identity hash and can join MyFamily/Invitees.
  **risa is a redirect to the Authy ID**, not a separate root; both risa-signed
  and Authy-signed proofs are accepted.

Telegram is an **invite/authentication channel**, not the LAN transport.

## First message set

| Message | Direction | Payload |
|---|---|---|
| `hello` | extension → host | `{protocol: 1, extensionVersion}` |
| `ready` | host → extension | `{hostVersion, peerId, capabilities}` |
| `pair.start` | extension → host | `{ttl}` → `{code, qr}` |
| `pair.accept` | extension → host | `{code}` → `{peerId, fingerprint}` |
| `peers.list` | extension → host | `{}` → `[{peerId, name, lastSeen}]` |
| `pull` | extension → host | `{peerId, groupId?, since}` → frames |
| `push` | extension → host | `{peerId, frames}` → `{accepted, rejected}` |
| `revoke` | extension → host | `{peerId, groupId, version}` |
| `status` | extension → host | `{}` → `{listening, peers, port}` |

Request/response uses an `id`; the host never executes arbitrary commands.

## Security

1. **Native messaging manifest** allows only the Browsy extension ID.
2. Pairing uses a one-time code + fingerprint; the user confirms.
3. All L frames are signed by Authy; the host verifies before forwarding.
4. The host never receives P plaintext or the root key.
5. Local listener binds `127.0.0.1` and/or the LAN interface explicitly; no
   `0.0.0.0` by default.
6. Replay protection: nonce + timestamp + version per frame.
7. The host has no shell/exec surface; its only inputs are the protocol
   messages.
8. Update channel is signed; the extension checks the host version.

## Install and update

- Per-OS installer or package: `browsy-host` binary + native messaging
  manifest in the browser’s `NativeMessagingHosts` directory.
- Linux: `~/.config/<browser>/NativeMessagingHosts/org.flove.browsy.json`.
- macOS: `~/Library/Application Support/<browser>/NativeMessagingHosts/`.
- Windows: registry key per browser.
- The extension shows “host missing / outdated / running” states and a
  copyable install command.

## MVP transport scope

- `pair.start` / `pair.accept` with a code.
- `peers.list`.
- `pull`/`push` for **group posts** and group membership grants.
- `revoke` for a member/group version.
- No public/Nety traffic; no P data.

## Open

- **Decided:** Rust host (O15=A).
- **Decided:** mDNS + manual `host:port` (O16=A for LAN; Telegram is separate).
- **Decided:** WebSocket + JSON for v1, QUIC/CBOR later (O17=B).
- **Decided:** signed release + version check (O18=A).
- Open: signing key, relay queue for offline peers, deep-link replay protection.
