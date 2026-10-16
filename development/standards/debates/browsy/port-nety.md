# Browsy → Nety port tunings

> What to change in browsy NOW so nety can extend it cleanly later.

## The relationship

```
browsy (base)              nety (extension)
─────────────              ───────────────
identity keys        ───►  P2P identity
trust (local)        ───►  trust (network)
storage (chrome)     ───►  storage (P2P)
crypto (local)       ───►  crypto (E2E)
settings (local)     ───►  settings (synced)
```

nety extends browsy. Browsy must be pluggable.

---

## 1 · Extract crypto into lib/crypto.js

**Why:** nety needs the same Ed25519 + ChaCha20 but with P2P transport. If crypto is a module, nety imports it directly.

**Now:**
```js
// background.js — crypto mixed into message handler
chrome.storage.local.get('browsy-keys', function(d) { ... });
```

**After:**
```js
// lib/crypto.js — standalone module
window.floveCrypto = {
  generateKeypair: function() { ... },      // Web Crypto / tweetnacl
  sign: function(key, data) { ... },
  verify: function(pubkey, data, sig) { ... },
  deriveCompositeKey: function(factors) { ... },
  mnemonicGenerate: function(key) { ... },
  mnemonicRestore: function(words) { ... }
};

// background.js — imports crypto module
importScripts('lib/crypto.js');
// uses window.floveCrypto.*
```

**Files:** Create `lib/crypto.js`, update `background.js`

---

## 2 · Abstract storage behind an interface

**Why:** browsy uses `chrome.storage.local`. nety might use IndexedDB, IndexedDB + P2P, or a different backend. If storage is abstracted, nety swaps the implementation.

**Now:**
```js
chrome.storage.local.get('browsy-keys', function(d) { ... });
chrome.storage.local.set({ 'browsy-vouches': vouches });
```

**After:**
```js
// lib/store.js — pluggable storage
window.floveStore = {
  get: function(key, cb) {
    chrome.storage.local.get(key, function(d) { cb(d[key] || null); });
  },
  set: function(key, val, cb) {
    var obj = {}; obj[key] = val;
    chrome.storage.local.set(obj, cb || function() {});
  },
  getAll: function(keys, cb) {
    chrome.storage.local.get(keys, cb);
  },
  remove: function(key, cb) {
    chrome.storage.local.remove(key, cb);
  },
  // nety overrides this with P2P storage
  _impl: 'chrome'
};

// background.js — uses store module
importScripts('lib/store.js');
window.floveStore.get('browsy-keys', function(key) { ... });
```

**nety port:** Replace `lib/store.js` with P2P-backed implementation. Same API.

**Files:** Create `lib/store.js`, update `background.js`

---

## 3 · Match vouch format to nety's trust protocol

**Why:** nety's trust graph uses `{ from, to, timestamp, trustLevel, signature }`. If browsy's vouch format matches, nety imports vouches directly.

**Now (browsy):**
```js
{ id, from, to, score, facets, message, created, revoked }
```

**nety format:**
```js
{ from, to, timestamp, trustLevel, signature, vectorClock }
```

**Compatible format (browsy uses this):**
```js
{
  id: "v_abc123",
  from: "ed25519_pubkey_hex",
  to: "ed25519_pubkey_hex",
  // nety-compatible fields:
  timestamp: "2026-07-27T10:00:00Z",     // was 'created'
  trustLevel: "close",                     // nety tier name
  signature: "ed25519_signature_hex",      // nety needs this
  vectorClock: { "user-a": 5 },            // nety CRDT
  // browsy-only fields (nety ignores):
  score: 0.85,
  facets: { personal: 0.9, local: 0.7, social: 0.8, global: 0.6 },
  message: "Known for 3 years",
  revoked: null
}
```

**Why this works:** nety reads `from, to, timestamp, trustLevel, signature, vectorClock` and ignores the rest. Browsy uses all fields. Zero conflict.

**Files:** Update `content.js` data structures, `background.js` storage format

---

## 4 · Message type registry (extensible)

**Why:** nety adds P2P messages (send-vouch, request-trust, sync-graph). If browsy uses a registry, nety registers new types without forking.

**Now:**
```js
// background.js — hardcoded if/else chain
if (msg.type === 'get-keypair') { ... }
if (msg.type === 'get-profile') { ... }
```

**After:**
```js
// lib/handler.js — message registry
window.floveHandlers = {};

window.floveHandlers.register = function(type, fn) {
  window.floveHandlers[type] = fn;
};

// background.js — registers browsy handlers
importScripts('lib/handler.js', 'lib/store.js', 'lib/crypto.js');

window.floveHandlers.register('get-keypair', function(msg, sender, cb) {
  window.floveStore.get('browsy-keys', function(key) {
    cb({ ok: true, data: key });
  });
});

// nety registers additional handlers:
window.floveHandlers.register('send-vouch', function(msg, sender, cb) {
  // P2P vouch sending
});

window.floveHandlers.register('sync-graph', function(msg, sender, cb) {
  // P2P trust graph sync
});
```

**Files:** Create `lib/handler.js`, update `background.js`

---

## 5 · Auth pipeline (layered, extensible)

**Why:** nety adds P2P auth (SSB, biometry). If browsy's auth is a pipeline, nety adds layers without touching core.

**Now:**
```js
// stubbed — no real auth
```

**After:**
```js
// lib/auth.js — auth pipeline
window.floveAuth = {
  layers: [
    { name: 'device', weight: 1, verify: function() { ... } },
    { name: 'telegram', weight: 2, verify: function() { ... } },
    { name: 'email', weight: 2, verify: function() { ... } },
    { name: 'trust', weight: 3, verify: function() { ... } }
  ],

  // nety adds layers:
  // { name: 'ssb', weight: 2, verify: function() { ... } }
  // { name: 'biometry', weight: 1, verify: function() { ... } }

  getCompositeKey: function() {
    // derive signing key from all active layers
  },

  getFactorCount: function() {
    // returns count for display ("3-factor signed")
  },

  addLayer: function(layer) {
    window.floveAuth.layers.push(layer);
  }
};
```

**Files:** Create `lib/auth.js`, update `background.js`

---

## 6 · Pluggable trust computation

**Why:** browsy computes trust locally (on-demand). nety computes trust over P2P network. If computation is pluggable, nety swaps the engine.

**Now:**
```js
// stubbed — trust returns 0
```

**After:**
```js
// lib/trust.js — pluggable trust engine
window.floveTrust = {
  computeScore: function(vouches) {
    // browsy: local only, simple average
    // nety: replaces with P2P graph traversal
    return localCompute(vouches);
  },

  computeFacets: function(vouches) {
    return { personal: 0, local: 0, social: 0, global: 0 };
  },

  computeChain: function(vouches, depth) {
    // browsy: depth 3, local
    // nety: depth 3, P2P
    return localChain(vouches, depth);
  },

  // nety overrides:
  // window.floveTrust.computeScore = p2pCompute;
};
```

**Files:** Create `lib/trust.js`, update `background.js`

---

## 7 · Bridge API versioning

**Why:** nety extends the bridge API (adds `nety.p2p.*`, `nety.sync.*`). If browsy's bridge has a version + extension point, nety adds without breaking.

**Now:**
```js
window.flove.browsy = { ... }; // fixed
```

**After:**
```js
window.flove = window.flove || {};
window.flove.browsy = { ... }; // browsy core

// extension point:
window.flove.extend = function(namespace, api) {
  window.flove[namespace] = api;
};

// nety uses:
window.flove.extend('nety', {
  p2p: { send: function() { ... }, receive: function() { ... } },
  sync: { push: function() { ... }, pull: function() { ... } }
});
```

**Files:** Update `content.js`

---

## 8 · Storage key namespacing

**Why:** browsy uses `browsy-keys`, `browsy-trust`, etc. nety uses `nety-keys`, `nety-trust`. If keys are namespaced, both coexist.

**Now:**
```js
chrome.storage.local.get('browsy-keys', ...);
chrome.storage.local.get('browsy-trust', ...);
```

**After:**
```js
// lib/store.js — namespaced
var NAMESPACE = 'browsy'; // nety sets 'nety'

window.floveStore = {
  get: function(key, cb) {
    chrome.storage.local.get(NAMESPACE + '-' + key, function(d) {
      cb(d[NAMESPACE + '-' + key] || null);
    });
  },
  set: function(key, val, cb) {
    var obj = {}; obj[NAMESPACE + '-' + key] = val;
    chrome.storage.local.set(obj, cb || function() {});
  }
};

// background.js — uses short keys
window.floveStore.get('keys', function(key) { ... });
window.floveStore.get('trust', function(trust) { ... });
```

**nety port:** Set `NAMESPACE = 'nety'`. Same API, different keys.

**Files:** Update `lib/store.js`

---

## Summary: what to create now

| File | Purpose | nety reuses |
|------|---------|-------------|
| `lib/crypto.js` | Ed25519, signing, mnemonic | Yes — same crypto |
| `lib/store.js` | Pluggable storage | Yes — swap backend |
| `lib/handler.js` | Message registry | Yes — add P2P handlers |
| `lib/auth.js` | Auth pipeline | Yes — add P2P layers |
| `lib/trust.js` | Trust computation | Yes — swap engine |
| `lib/vouch.js` | Vouch format (nety-compatible) | Yes — same format |

**Estimated effort:** ~2 hours to extract and refactor.
**nety port savings:** ~1-2 days (don't rewrite crypto, storage, auth, trust).

---

## Implementation order

1. `lib/store.js` — extract from background.js (15 min)
2. `lib/crypto.js` — extract stubs + add Web Crypto (30 min)
3. `lib/handler.js` — extract message routing (15 min)
4. `lib/vouch.js` — define nety-compatible format (15 min)
5. `lib/auth.js` — extract auth pipeline (15 min)
6. `lib/trust.js` — extract trust computation (15 min)
7. Update `background.js` — use all modules (15 min)
8. Update `content.js` — add `flove.extend()` (10 min)

---

## 9 · F2F (Face-to-Face) verification

**Why:** Strongest trust signal. "I met this person in real life." Can't be faked remotely. Feeds into the local facet (weight: 1.0).

### How it works

```
User A                          User B
──────                          ──────
shows QR code ──────────────► scans QR
  (pubkey + nonce)                │
                                  signs nonce with their key
◄────────────────────────── sends signed nonce
verifies signature               │
  │                              │
  └─ both sign "A↔B verified" ──┘
     central stores F2F record
```

### Data structure
```js
{
  type: "f2f",
  from: "pubkey_a",
  to: "pubkey_b",
  timestamp: "2026-07-27T10:00:00Z",
  nonce: "random_32_bytes",
  sigA: "ed25519_sig_of_nonce",
  sigB: "ed25519_sig_of_nonce",
  location: "optional_gps_or_null",
  trustLevel: "f2f",    // highest weight
  signature: "combined_sig"
}
```

### Where it lives
- **browsy:** generates QR, signs challenge, stores F2F record locally
- **central:** stores F2F record as special vouch type, includes in trust graph

### Trust weight
| Trust type | Weight | Why |
|-----------|--------|-----|
| f2f | 1.0 | Met in person, can't fake |
| vouch | 0.7 | Online trust statement |
| self | 0.3 | Self-declared |

**Files:** Create `lib/f2f.js`, update `background.js`, central `POST /api/trust/f2f`

---

## 10 · Permissions layer

**Why:** Not just "public or private" — granular access control. Who can see, comment, edit, admin.

### Permission levels
| Level | Can do |
|-------|--------|
| `none` | Can't see it exists |
| `view` | Can read |
| `comment` | Can read + comment |
| `edit` | Can modify |
| `admin` | Can change permissions |

### Where it lives
- **central:** permissions table (authoritative)
- **browsy:** caches permissions locally (fast check)

### Flow
```
User visits page
  → browsy checks local cache
  → cache miss? asks central: "can I see this?"
  → central checks permissions table
  → returns: yes/no + level
  → browsy caches result (TTL: 5 min)
  → shows or hides content
```

### Central API
| Endpoint | What it does |
|----------|-------------|
| `GET /api/permissions/:content_id` | Check if user can access content |
| `POST /api/permissions/:content_id` | Set permissions for content |
| `DELETE /api/permissions/:content_id/:user` | Revoke access |

**Files:** Central `permissions.py`, browsy `lib/permissions.js`

---

## 11 · URL obfuscation

**Why:** Hide private content URLs. Prevents snooping, guessing, indexing. Group members see real URLs, strangers see nothing.

### URL format
```
Public:    https://flove.org/apps/garden/public-post-123
Private:   https://flove.org/p/a1b2c3d4           ← obfuscated
Protected: https://flove.org/p/a1b2c3d4?token=xyz  ← signed, expires
```

### How it works
```
Central stores:
  content_id: "a1b2c3d4"
  real_path: "/my-secret-project/notes"
  owner: "pubkey_owner"

When user requests /p/a1b2c3d4:
  1. Central checks: is user authorized?
  2. If yes → redirects to real path (or serves content)
  3. If no → shows "access denied" or "request access"
```

### browsy's role
- Detects `/p/` URLs
- Asks central: "what is this?"
- Central checks permissions
- If authorized: browsy decrypts and renders
- If not: shows "request access" or "join group"

### Group alternative
Instead of per-user permissions:
```
User shares page with group "project-x"
  → all group members can access /p/a1b2c3d4
  → non-members see "access denied"
  → add/remove people from group → permissions update automatically
```

**Files:** Central `obfuscate.py`, browsy detects `/p/` URLs

---

## 12 · Group-based access

**Why:** Manage 1 group instead of 50 individual grants. Add/remove people → permissions update automatically.

### Group data structure
```js
{
  id: "grp_abc123",
  name: "project-x",
  owner: "pubkey_owner",
  members: ["alice_key", "bob_key", "carol_key"],
  permissions: { view: true, comment: true, edit: false },
  created: "2026-07-27T10:00:00Z",
  expiry: null  // or "2026-08-27T10:00:00Z"
}
```

### How it works
```
User creates group:
  name: "project-x"
  members: ["alice", "bob", "carol"]
  permissions: { view: true, comment: true }

User shares page with group:
  central: page_abc123 → group "project-x" → view+comment

All 3 members can view + comment

User removes bob from group:
  bob can no longer see page_abc123
```

### Relationship to browsy's existing groups
- browsy has: Close, Public, Private, 1 custom
- central extends: groups with members, permissions, expiry
- browsy checks central: "is user in my group?"
- central answers: yes/no + what level

### Central API
| Endpoint | What it does |
|----------|-------------|
| `POST /api/groups` | Create group |
| `GET /api/groups` | List user's groups |
| `POST /api/groups/:id/members` | Add member |
| `DELETE /api/groups/:id/members/:user` | Remove member |
| `POST /api/groups/:id/permissions` | Set group permissions |

**Files:** Central `groups.py`, browsy `lib/groups.js`

---

## 13 · Auto-decrypt for protected pages

**Why:** Like a password manager but for flove content. No manual password entry. browsy stores keys, central stores encrypted content. Central NEVER sees plaintext.

### Security model

```
Owner encrypts page:
  content → encrypt with key X → stored on central
  key X → encrypt with owner's pubkey → stored on central

Grant access to alice:
  key X → encrypt with alice's pubkey → stored on central

alice visits:
  central sends: key_X_for_alice (encrypted)
  alice's browsy: decrypts with private key → gets key X
  alice's browsy: decrypts content with key X
  alice sees: plaintext

central's view: encrypted content + encrypted keys
browsy's view: plaintext content + private key
nobody else sees anything
```

**What central knows:** that alice has access (permissions table)
**What central never sees:** the content or the decryption key in plaintext

### Attack scenarios

| Scenario | Result | Mitigation |
|----------|--------|------------|
| Central hacked | Attacker gets encrypted blobs, useless | Need private keys (in browsy) |
| Device stolen | Attacker gets private key + cache | Device auth layer |
| Member removed | Old key deleted, content re-encrypted | Key rotation |
| Man-in-the-middle | Can't decrypt (TLS + E2E) | Key never travels in plaintext |

### Key rotation (when member removed)

```
Owner removes bob:
  1. Generate new key Y
  2. Re-encrypt content with key Y
  3. Re-encrypt key Y for remaining members (alice, carol)
  4. Delete key X entirely
  5. bob's cached key X is useless (content re-encrypted with Y)
```

### How it appears in the feed

The feed mixes public and private posts. Private posts show a small indicator:

```
┌─────────────────────────────────────────┐
│  🌿 María shared a garden post          │
│  "How to grow tomatoes in shade"        │
│  2 hours ago                  public    │
├─────────────────────────────────────────┤
│  🔒 project-x · team only               │
│  "Sprint planning notes"                │
│  1 hour ago                   🔑 auto   │  ← you have access, auto-decrypts
├─────────────────────────────────────────┤
│  🌿 Carlos shared a garden post          │
│  "Best soil for containers"             │
│  30 min ago                  public     │
├─────────────────────────────────────────┤
│  🔒 🔒 encrypted                        │
│  "Q3 budget"                            │
│  5 min ago                   🔒 locked  │  ← no access
└─────────────────────────────────────────┘
```

**Three states:**
| State | Icon | What you see | What happens |
|-------|------|-------------|-------------|
| Public | `public` | Full content | Nothing |
| Private + access | `🔑 auto` | Full content (auto-decrypted) | browsy decrypts silently, <10ms |
| Private + no access | `🔒 locked` | Title only + "request access" | Can't see content |

### Flow

```
central returns feed items:
  [
    { id: "post_1", public: true, content: "..." },
    { id: "post_2", encrypted: true, group: "project-x", title: "Sprint planning" },
    { id: "post_3", encrypted: true, title: "Q3 budget" }
  ]

browsy checks each:
  if public → show full content
  if encrypted + you have key → auto-decrypt, show full content
  if encrypted + no key → show title + "request access"
```

### browsy's role
- Stores private key (never leaves device)
- Detects encrypted pages (checks `encrypted: true` flag)
- Requests encrypted key from central
- Decrypts locally (<10ms)
- Caches decrypted key (TTL: 1 hour)

### central's role
- Stores encrypted content
- Manages per-user encrypted keys
- Checks permissions before releasing keys
- Rotates keys when members are removed

### Central API
| Endpoint | What it does |
|----------|-------------|
| `POST /api/content/:id/encrypt` | Owner encrypts content |
| `GET /api/content/:id/decrypt-key` | Get encrypted decryption key |
| `POST /api/content/:id/grant/:user` | Grant access (encrypt key for user) |
| `DELETE /api/content/:id/revoke/:user` | Revoke access (delete user's key) |
| `POST /api/content/:id/rotate` | Rotate encryption key |

---

## How all 5 connect

```
F2F verify
  → high trust score
  → join group
  → group grants permissions
  → permissions allow access to obfuscated URL
  → central releases encrypted key
  → browsy auto-decrypts content
```

**Trust chain:**
```
meet in person → verify identity → trust score → group access → see content → auto-decrypt
```

### Central API summary (all 5 features)

| Endpoint | Feature | What it does |
|----------|---------|-------------|
| `POST /api/trust/f2f` | F2F | Store F2F verification record |
| `GET /api/permissions/:id` | Permissions | Check access level |
| `POST /api/permissions/:id` | Permissions | Set access level |
| `GET /api/p/:id` | Obfuscation | Resolve obfuscated URL |
| `POST /api/groups` | Groups | Create group |
| `POST /api/groups/:id/members` | Groups | Add/remove member |
| `POST /api/content/:id/decrypt-key` | Auto-decrypt | Get encrypted decryption key |
| `POST /api/content/:id/rotate-key` | Auto-decrypt | Rotate encryption key |

### browsy module summary

| Module | Feature | What it does |
|--------|---------|-------------|
| `lib/f2f.js` | F2F | QR generation, challenge signing |
| `lib/permissions.js` | Permissions | Cache + check access |
| `lib/decrypt.js` | Auto-decrypt | Decrypt content locally |
| `lib/groups.js` | Groups | Cache group membership |
