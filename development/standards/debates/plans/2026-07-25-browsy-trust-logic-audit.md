# Browsy — Trust Logic & Audit Trail

**Date:** 2026-07-25
**Status:** draft
**Depends on:** `2026-07-25-browsy-keys-trust-performance.md`

---

## 1. Core Principle

Permissions aren't a separate system. They're a **query** against trust contracts.

```
can(keyA, action, context) → contract.evaluate(keyState) → boolean
```

A trust contract is a deterministic rule: given key state + context → yes/no + score. Portable across browsy, Central, nety, any app.

---

## 2. Trust Contracts

### 2.1 Format

```json
{
  "id": "publish:mynet:close",
  "action": "publish",
  "context": "mynet",
  "scope": "close",
  "require": { "social": 20, "local": 10 },
  "weight": 1.0,
  "decay": "30d",
  "delegate": false
}
```

| Field | Purpose |
|---|---|
| `id` | Unique contract identifier |
| `action` | What the user wants to do |
| `context` | Where (app/site) |
| `scope` | Trust tier required |
| `require` | Facet thresholds |
| `weight` | Multiplier for reputation weighting |
| `decay` | Trust freshness period |
| `delegate` | Can someone vouch on your behalf? |

### 2.2 Standard Contracts (v1)

| Contract | Action | Require | Notes |
|---|---|---|---|
| `publish:{app}:{scope}` | publish content | facet thresholds by scope | checkbox = contract check |
| `view:{app}:{scope}` | see private/Close content | tier match | wizy permission check |
| `vouch:{scope}` | vouch for someone | personal ≥ 5 | you need identity to vouch |
| `unvouch:{scope}` | revoke a vouch | same as vouch | symmetric |
| `delegate:{scope}` | vouch on behalf of another | social ≥ 50 | chain trust |
| `rotate:{scope}` | rotate keys | personal ≥ 10 | identity required |
| `context:read:{doc}` | read a context document | scope match | staleness checked |
| `context:write:{doc}` | update a context document | owner or delegate | pointer invalidation |

### 2.3 Permission Contract Templates

Permission contracts are **automated templates**, not hand-coded per app. Browsy (or agents) instantiate them. Two demos:

**maty** — personal trust circle. Shows content only from people you've directly vouched for or who vouched for you. Filters out strangers.

```
maty = {
  name: "maty",
  filter: "direct-vouch-or-vouched-by",
  scope: "close",
  visibility: "circle",
  content: "show-more-from-trusted"
}
```

**myfamily** — family circle. Even tighter: only keys with `local ≥ 30` and identity verified. Browsy enforces this on flove.org — you see more content from family, less or nothing from outsiders.

```
myfamily = {
  name: "myfamily",
  filter: "local≥30 + identity-verified",
  scope: "close",
  visibility: "circle",
  content: "show-only-family"
}
```

**How it works:**
- Templates define a trust filter (which facets, which thresholds)
- Browsy evaluates the filter against every key you encounter
- flove.org (or any app) queries browsy: "who passes the maty filter?"
- Results: content from passing keys is shown more prominently or exclusively
- Agents can apply templates: "only read/write to myfamily contexts"

**Why templates, not per-app contracts:**
- Permission logic is reusable: "trusted people" means the same thing everywhere
- Apps don't need to define trust rules — they inherit from templates
- Users pick a template (maty, myfamily) and browsy enforces it across all apps
- Custom contracts still exist for edge cases, but most permissions are template-based

---

## 3. Trust Logic

### 3.1 Facet Computation

Each facet is a number 0–100, computed independently:

```javascript
function computeFacet(facet, keyState) {
  var score = 0;
  keyState.vouches.forEach(function(vouch) {
    if (vouch.facet !== facet) return;
    if (vouch.expired(vouch.decay)) return;
    var chainWeight = 1 / (vouch.chainDepth + 1);
    score += vouch.strength * chainWeight;
  });
  return Math.min(100, score);
}
```

**Facet rules:**

| Facet | Source | Max chain depth | Decay rate |
|---|---|---|---|
| Personal | Identity links only | 0 (no delegation) | None |
| Local | Peer vouches (nearby) | 1 | 90 days |
| Social | Network vouches | 3 | 60 days |
| Global | Hardware share + published content | 0 (measured) | 30 days idle |

Personal is the anchor: earned through identity links, never vouched. Prevents circular trust gaming.

### 3.2 Vouch

The atomic trust action:

```
Vouch {
  from:       keyA
  to:         keyB
  facet:      "social"
  strength:   25           // 0-100
  scope:      "close"
  context:    "blogy"      // optional: context-specific
  chainDepth: 0
  created:    timestamp
  decay:      "60d"
  revocable:  true
}
```

**Rules:**
- `from.personal ≥ 5` (must prove identity to vouch)
- `strength ≤ from.facet` (can't give more than you have)
- Max active vouches per key: 50 (prevents spam)
- One active vouch per `(from, to, facet, scope)` — duplicates overwrite

### 3.3 Friends (MyNet v1)

A **friend** = someone you've directly vouched for, or who directly vouched for you. No chains, no delegation. Direct trust only.

```
Friend {
  key:        fingerprint
  handle:     "@ana"
  direction:  "mutual" | "outgoing" | "incoming"
  vouch:      { facet: "social", strength: 25, created: timestamp }
  lastSeen:   timestamp
  status:     "active" | "stale"
}
```

**Direction:**
- **Mutual:** you vouch for each other → closest
- **Outgoing:** you vouched for them → you trust them
- **Incoming:** they vouched for you → they trust you

**Friends list:**
```
MyNet
├── friends (12)
│   ├── mutual (5)      ← strongest
│   ├── outgoing (4)
│   └── incoming (3)
├── trusts
└── scores
```

**Friends = Close group.** Friends map directly to the Close permission group:
- Friends see your Close content automatically
- When you publish with `scope: close`, only friends can access
- Wizy check: `isKeyInCloseList(key)` → yes/no

**Adding/removing friends:**

| Action | How | Effect |
|---|---|---|
| Add friend | Vouch for someone | They appear in friends list |
| Remove friend | Revoke vouch | They leave friends list |
| Friend request | You vouch (outgoing) | They see "X trusts you" |
| Accept | They vouch back | Direction → mutual |

**Staleness:** Friends without interaction in 60 days are flagged stale (dimmed, access continues, re-activate by interacting or re-vouching).

### 3.4 Delegation — v2

> Not in v1. v1 is direct vouches only. Delegation ships in v2.

@maria (social: 60) wants to vouch for you, but @ana knows you. @ana delegates:

```
Delegation {
  delegator:  @ana
  delegate:   @maria
  target:     you
  facet:      "social"
  strength:   20
  chainDepth: 1
}
```

**Rules:**
- `delegator.social ≥ 50`
- `delegate.social ≥ delegator.social`
- Chain depth: delegator.chainDepth + 1, max 3
- Each hop halves effective strength: `strength × 0.5^chainDepth`
- Revocable by delegator at any time

**Example:**
```
@ana (social: 60) → delegates to @maria → vouches for you
Your social += 20 × 0.5^1 = 10

@maria (social: 55) → delegates to @pedro → vouches for you
Your social += 15 × 0.5^2 = 3.75
```

Direct trust is worth most. Long chains are weak by design.

### 3.4 Decay

Trust without interaction fades:

```javascript
function applyDecay(vouch, now) {
  var daysSince = (now - vouch.lastAction) / 86400000;
  var decayDays = parseDuration(vouch.decay);

  if (daysSince > decayDays) {
    vouch.strength *= 0.5;
    vouch.lastAction = now;
  }

  if (vouch.strength < 1) {
    vouch.expired = true;
  }
}
```

**Decay triggers (reset the clock):**
- Direct interaction between vouching keys
- Re-vouch (explicitly refreshing)
- Context activity (both active in same app)

### 3.5 Revocation

```
Revocation {
  from:      keyA
  to:        keyB
  facet:     "social"
  scope:     "close"
  reason:    "behavior"    // behavior | inactive | compromised
  timestamp: now
}
```

**Rules:**
- Only original vouching key can revoke
- Revocation propagates: chain-trusted keys notified
- Downstream scores recalculated immediately
- Irreversible (but can re-vouch)

**Propagation example:**
```
@ana vouched for @pedro (social: 30)
@pedro vouched for you (social: 20, chainDepth: 1)
Your effective: 20 × 0.5^1 = 10

@ana revokes @pedro
→ @pedro's social drops
→ Your effective recalculated (now 0 if @pedro has no other vouches)
→ Notification: "trust chain broken: @ana revoked @pedro"
```

---

## 4. Permission Visibility

Trust relationships have visibility levels:

| Level | Who sees it | Use case |
|---|---|---|
| Public | Anyone | Reputation building |
| Circle | People in that circle | Group trust |
| Private | Only you and the other key | Sensitive vouches |
| Opaque | Relationship exists, strength hidden | "trusted" without exact number |

Contracts specify which visibility applies. `publish:close` might require `visibility=public` so others can verify why you had access.

---

## 5. Trust-for-Actions Mapping

Trust weight affects outcomes beyond yes/no:

| Trust Level | Action Effect |
|---|---|
| None (0) | Read-only, no interaction |
| Low (1–19) | Basic interaction, limited publish |
| Medium (20–49) | Full publish, can vouch others |
| High (50–99) | Can delegate (v2), moderate content |
| Max (100+) | Full access, can create contracts |

Avoids hard thresholds. Trust is a gradient mapping to capabilities.

### 5.1 Rewardy Mapping (Vanguard Demo)

Rewardy's 3 scores come from 3 different systems:

| Rewardy | Source | Meaning |
|---|---|---|
| **souls** (s) | souls app | Matching/compatibility between two people |
| **trust** (t) | browsy facets | Reliability: social + local vouches |
| **deal** (d) | browsy finetuner | Value: offer vs market, trust-weighted pricing |

Browsy provides trust + deal. Souls app provides souls. Three systems feeding one UI.

---

## 6. Trust Chains — v2

> v1 is direct vouches only. Chains and delegation ship in v2.

### 6.1 Path Computation

```
trustPath(from, to):
  direct = vouches where from=from, to=to
  delegated = delegations where target=to, transitively
  
  for each path:
    effective = strength × 0.5^chainDepth
    weight = 1 / (chainDepth + 1)
  
  final = sum(effective × weight) across all paths
  return min(100, final)
```

### 6.2 Contextual Trust

Trust in `blogy` doesn't transfer to `sensy`. Contracts are per-context. You build reputation separately per app. Prevents "one vouch unlocks everything."

### 6.3 Trust Portability

Your trust score travels with your key. Moving from `appy-basic` to `appy-normal` carries your personal facet. Keys are the portable identity layer.

---

## 7. Audit Trail

### 7.1 Log Entry Format

Every trust action creates an immutable entry:

```json
{
  "seq": 142,
  "action": "vouch",
  "from": "keyA_fingerprint",
  "to": "keyB_fingerprint",
  "facet": "social",
  "scope": "close",
  "context": "blogy",
  "strength": 25,
  "prevHash": "a3f2...",
  "hash": "b7c1...",
  "timestamp": 1753468800000
}
```

The `prevHash` links to the previous entry. SHA-256 of `(seq + action + from + to + ... + prevHash)` produces `hash`. Tamper-evident: modifying any entry breaks all subsequent hashes.

### 7.2 Action Types

| Action | What is logged |
|---|---|
| `vouch` | New vouch created |
| `revoke` | Vouch revoked |
| `delegate` | Delegation created (v2) |
| `permission_check` | wizy checked a contract |
| `publish` | Content published under a contract |
| `key_rotate` | Key rotation event |
| `context_update` | Context document changed |

### 7.3 Permission Check Logging

```json
{
  "seq": 143,
  "action": "permission_check",
  "key": "yourKey_fingerprint",
  "site": "flove.org/apps/blogy",
  "contract": "publish:blogy:close",
  "result": true,
  "facets": { "personal": 45, "social": 32, "local": 18, "global": 5 },
  "timestamp": 1753468800000
}
```

Accountability: you can see exactly why a permission passed or failed.

---

## 8. Storage

### 8.1 Extension (browsy)

```
browsy:audit:index      → last seq number
browsy:audit:entry:{n}  → AuditEntry
browsy:audit:hash       → current chain head hash
```

Local-first. You own your audit trail.

### 8.2 Central (optional backup)

```
{profile}/audit.jsonl   → append-only log, encrypted with your key
```

### 8.3 LRU Eviction

When audit hits 1MB cap, oldest entries are pruned. Their hashes are preserved in a compact **merkle summary** so the chain remains verifiable without storing every entry.

Standard binary merkle tree. Each pruned entry becomes a leaf in the summary. Proofs walk the tree without needing the original data.

```
browsy:audit:merkle → {
  root: "hash",
  depth: 3,
  leaves: [hash, hash, hash, ...],  // pruned entry hashes
  tree: [hash, hash, ...]           // internal nodes, bottom-up
}
```

Verification with pruned entries: supply the leaf hash + merkle path (sibling hashes at each level). Recompute root, compare. Works even when the original entry is gone.

### 8.4 Encryption at Rest

Extension storage isolation is sufficient for v1. Trust relationships are semi-public by nature (you vouch for people, that's visible). Audit entries don't contain secrets — the key's private key never leaves the key store. Encrypting the entire audit trail adds complexity without meaningful security gain at this stage.

If needed later: encrypt each entry with the local key before writing. The merkle tree hashes the plaintext (for verification), not the ciphertext.

---

## 9. Query API

```javascript
// What trust actions involved this key?
browsy.audit.query({ key: keyFingerprint, action: 'vouch' })

// What happened in a specific context?
browsy.audit.query({ context: 'blogy', after: date })

// Verify the chain is intact
browsy.audit.verify()
// → { valid: true, entries: 142, head: "b7c1..." }

// Prove a vouch existed at a specific time
browsy.audit.proof(seq: 87)
// → { entry: ..., hash: ..., merklePath: [...] }

// Cross-key: query another key's public audit entries (v2)
browsy.audit.query({ key: otherKeyFingerprint, public: true })
// → only returns entries with visibility=public
```

Cross-key queries only return public-visibility entries. Private and circle entries are not exposed to other keys. **v2 feature** — v1 audit is local only.

---

## 10. Verification Flow

When browsy encounters a trust claim:

```
1. Receive trust proof from keyB ("I have social:40")
2. Fetch audit entries forming the trust chain
3. Verify hash chain integrity (entry[n].prevHash == entry[n-1].hash)
4. Check each vouch for expiry (decay)
5. Recompute facets from live vouches
6. Compare: claimed score vs computed score
7. If match → trust claim verified
8. If mismatch → reject, log anomaly
```

---

## 11. Anomaly Detection — v2

> v1 has basic audit logging only. Anomaly detection requires chain analysis, ships in v2.

| Anomaly | Detection | Response |
|---|---|---|
| Rapid vouching | >10 vouches in 1 hour | Flag, suggest review |
| Chain depth abuse | vouches at depth 3 from low-trust keys | Ignore, log warning |
| Revocation storm | >5 revocations in 1 day | Alert, possible compromise |
| Permission creep | key gains access to >20 contexts | Prompt review |
| Stale trust | trust scores used but vouches expired | Re-score alert |

---

## 12. Portability

Export/import your audit trail with your key:

```
Export:
  key fingerprint + audit.jsonl (encrypted with your key)

Import (new device/extension):
  1. Load key
  2. Decrypt audit.jsonl
  3. Verify hash chain
  4. Import vouches (non-expired)
  5. Recompute facets
  6. Ready
```

---

## 13. v1/v2 Scope

### v1 — Ship It

| Feature | Status |
|---|---|
| Keys (Ed25519, self-contained) | v1 |
| Auth (identity links) | v1 |
| 4 facets (personal/local/social/global) | v1 |
| Direct vouches only | v1 |
| Friends list (= Close group) | v1 |
| Permission contracts (standard) | v1 |
| Publish flow (checkboxes, browsy signs) | v1 |
| Wizy permission checks | v1 |
| Audit trail (hash chain, local) | v1 |
| Contextual trust (per-app) | v1 |
| Trust portability (via key) | v1 |
| Templates (maty, myfamily) | v1 |
| Decryption at rest (extension isolation) | v1 |

### v2 — Extend

| Feature | Why deferred |
|---|---|
| Delegation | Needs chain trust logic, more complex |
| Chain depth (up to 3 hops) | Depends on delegation |
| Key rotation + probation | Needs trust revocation propagation |
| Re-vouch (explicit refresh) | Nice-to-have, decay handles it |
| Context pointers (large docs) | Agent complexity |
| Staleness detection (pointers) | Depends on context pointers |
| Publish audit logging | Basic audit covers v1 |
| Cross-key audit | Needs public entry visibility |
| Central backup | Optional, user-triggered |
| Anomaly detection | Needs chain analysis |
| Agent enforcement of templates | Agent integration deferred |
| flove.org content filtering | Needs templates + agent |
| WASM scoring | Performance optimization |

---

## 14. Decisions

1. **Merkle format:** Standard binary merkle tree. Each pruned entry becomes a leaf. Proofs walk the tree with sibling hashes. Well-understood, efficient, battle-tested.
2. **Audit replication:** Optional. Central backup exists but is not automatic. User triggers explicit backup.
3. **Cross-key audit:** Yes (v2). You can query another key's public audit entries. Private/circle entries stay private.
4. **Contract evolution:** Permission contracts are automated templates (maty, myfamily are demos). Browsy/agents instantiate them. flove.org shows more or only content from users passing the template filter. No need to store permission contracts alongside custom contracts — templates are the standard, custom is the exception.
5. **Encryption at rest:** Extension storage isolation sufficient for v1. Audit entries don't contain secrets (private key stays in key store). Trust relationships are semi-public by nature. Encrypt later if needed — merkle hashes plaintext for verification regardless.
6. **Friends = Close group:** A friend is someone with a direct vouch relationship (mutual, outgoing, or incoming). Friends list IS the Close group member list. No separate "friends" data structure.
7. **v1 = direct vouches only:** No delegation, no chains, no key rotation. Trust is simple: you vouch for someone, they're in your friends/Close group. Chains and delegation are v2.
8. **4 groups, not 6:** Q16 (6 groups) is superseded by Q19 (4 groups). Close, Public, Private + 1 custom. Flat, no nesting.
