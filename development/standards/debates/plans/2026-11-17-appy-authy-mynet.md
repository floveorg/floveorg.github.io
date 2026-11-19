# Plan: Authy → Appy → MyNet, over web and Browsy

> 2026-11-17. Spec draft. Authy owns the levels; Appy owns the profile and the
> MyNet surface; Browsy is the preferred transport because it already carries
> the web of trust.

## 1. What activates what

Authy owns the numbered ladder. MyNet has no levels of its own; it is the name
of the local feature set that opens at Authy L3.

| Level | Claim | What it unlocks |
|---|---|---|
| **L1** | self | local profile; MyNet read-only + MyFamily JSON export |
| **L2** | email (planned) | email presence; still no MyNet features |
| **L3** | Telegram **presence** via @AuthyTgBot (risa handoff included) | **MyNet local features**: people, circles, feed, local sharing, MyFamily, local invites |
| **L4** | Telegram **verified** (nonce + private DM) | **publishing / social layer** (Nety/Wizy/platforms); trust-graph writes |
| **L5** | phone | recovery and higher-trust actions |
| **L6** | bio | strongest local unlock |

Rules:

- **L1/L2 are the versions without AuthyTg or risa bot.** MyNet shows its
  functions in read-only and exports the MyFamily JSON; no people, circles,
  feed or sharing.
- **L3 opens MyNet.** It is presence, not permission: the bot records a
  private `/start` (including the risa handoff `/start risa_<key>`), but the
  account is not bound to the Authy profile with a challenge.
- **L4 opens publishing.** Authy generates a one-time nonce, the user sends
  `/start claim_<nonce>` in a private DM, and the verifier matches it to the
  profile. Fresh, one-use, replay-resistant — the only level that can sign
  Social cards.
- **L5/L6** never unlock new *content* surfaces by themselves; they raise
  recovery and co-signing weight.
- A level without its claim is presence, not permission: `telegram:present`
  ≠ `telegram:verified`.

## 2. Portable auth record — `flove-auth/1`

```json
{
  "schema": "flove-auth/1",
  "handle": "@marc",
  "levels": { "self": true, "telegram": "verified", "phone": false, "bio": false },
  "claims": [
    {
      "network": "telegram",
      "handleHash": "sha256:…",
      "level": "present|verified",
      "proof": "nonce-or-signature",
      "at": "2026-11-17T…",
      "expires": null
    }
  ],
  "visibility": { "telegram": "self", "claims": "mynet" },
  "updatedAt": "2026-11-17T…"
}
```

- No secrets, no raw phone numbers, no Telegram session tokens.
- `handleHash` instead of the public handle; the handle renders only when the
  user chooses.
- The record is **signed** by the Authy key; Appy re-validates, Browsy attests.

## 3. Transport

### A. Web (today, local-first)

1. Authy page links Telegram (L3 presence) or claims the bot DM (L4).
2. Authy writes `flove:authy` and offers **Send to Appy**.
3. The handoff is the same one used by Share → Appy:
   - same origin: write `flove:appy:auth` (or `flove:authy`) and let Appy
     refresh;
   - `file://`: open Appy with `postMessage` `{type:'flove-appy-auth', record}`.
4. Appy validates, stores, unlocks MyNet at L3, shows the level in the
   Authenticate card.

### B. Browsy (preferred)

1. Authy publishes the signed `flove-auth/1` record to **Browsy’s web of trust**
   (a `flove-trust/1` edge: `subject`, `claim`, `level`, `signature`).
2. Browsy peers co-sign / attest; the record becomes a trust-graph fact, not a
   local secret.
3. Appy subscribes to the user’s Browsy identity and imports the latest valid
   record; MyNet and publish unlock from the attested level.
4. Revocation is a new Browsy edge (`revoked:at`); Appy drops the level on the
   next sync. Offline stays on the last valid record with a `stale` marker.

Why Browsy: the levels are only as good as their attestations. Browsy already
owns the web of trust, the peer graph and the P2P permissions variant
(NetyBrowsy). Appy should not become a second trust store.

## 4. UI

- Appy Profile title → **See · Export · Render** (current).
- Authenticate card shows the level (`L1 · self`, `L2 · email`,
  `L3 · presence`, `L4 · verified`) and a **Send to Appy / Sync from Browsy**
  action when the Authy page is open.
- MyNet gate at L3: people, circles, feed, local sharing. L4 adds the publish
  button; do not show a publish control before L4.
- A small “attested by Browsy · 2 peers” line when the record came from Browsy.

## 5. Security checklist

- One-time nonce for the L4 claim; expire it.
- Never store Telegram tokens, phone numbers or raw handles in the portable
  record.
- Appy validates the signature and the claim level before unlocking.
- Browsy attestations are revocable; Appy re-checks on focus/sync.
- Visibility: `self` by default for claims; `mynet` for the level; public only
  by an explicit user action.
- `file://` uses postMessage; no JSON in URLs.

## 6. Open questions

1. Does L3 presence alone unlock *local sharing*, or only people/circles/feed?
2. Who signs `flove-auth/1` on `file://` where there is no key store?
3. Does Browsy attest the level or only the claim hash?
4. Is `flove:appy:auth` a copy of `flove:authy`, or a cache of Browsy facts?
5. When a claim is revoked, does Appy lock MyNet immediately or keep a grace
   period?

## 7. Spec-driven development map

| Phase | Spec / contract | Acceptance test | State |
|---|---|---|---|
| **A0** Authy store | `flove:authy` = `flove-authy/1` with `level`, `identities`, `telegram`, `nonce`/`nonceAt` | Authy writes it; reload keeps the level | ✅ |
| **A1** Telegram claim client | nonce (crypto, 10 min TTL) → `https://t.me/<bot>?start=claim_<nonce>` → poll verifier | with a verifier, L4 only after a signed `{ok, level:'verified'}` | ✅ client; verifier URL configurable |
| **A2** Telegram verifier | `GET {verify}?nonce=…` → `{ok, level:'verified', at}`; bot accepts `/start claim_<nonce>` | a DM to the bot releases exactly one nonce; replay is rejected | ✅ code + tests; ⏳ BotFather token/deploy |
| **A3** Appy status sync | `storage` + `focus` + `visibilitychange` re-read `flove:authy`; L3 unlocks MyNet, L4 unlocks publish | changing the level in Authy updates Appy without reload | ✅ |
| **A4** Authy → Appy handoff | `postMessage {type:'flove-appy-auth', auth}` + `flove:authy` on same origin | `file://` and blocked storage still update Appy | ✅ |
| **A5** Send to Appy UI | button in the L4 card; opens Appy `#profile` | level and MyNet gate follow on the next screen | ✅ |
| **A9** SelfAuth (L1) | `flove:authy.self = { browsyHash }`; Authy self form + **Open Browsy** link; Appy keeps name/about/links/social on its username card, no SelfAuth mirror | save the hash; Appy username card stays the profile data | ✅ |
| **A11** Canonical card | Appy play cards use its internal card renderer; **View & Export** builds the full profile HTML with Share; Rendery is a standalone dev addon | every play renders; the profile HTML carries the whole profile | ✅ |
| **A10** Email (L2) | Google ID token + email code; L2 email presence, no MyNet | Google or code → L2 email; MyNet stays closed | ⏳ **planned only — not implemented** |
| **A6** Browsy attestation | signed `flove-auth/1` edge in Browsy’s web of trust; Appy imports the attested level | 2 peers attest; revocation drops the level | ⏳ |
| **A7** NetyBrowsy permissions | P2P permission variant reads the same auth record | no central server; peers enforce | ⏳ |
| **A8** Tests | unit (level, claim TTL, handoff) + e2e (`file://` and http) | all green | partial |

**File map**

- `apps/sys/authy/index.html` — ladder, claim nonce, verifier polling, Send to Appy.
- `apps/sys/authy/bot/` — `server.mjs` (polling bot + `/claim` verifier), `logic.mjs`
  (pure claim/TTL), `test/logic.test.mjs`, `README.md` (BotFather + deploy).
- `apps/appy/appy-basic.html` — `authyLevel()`, `refreshAuthyStatus()`, MyNet gate, auth handoff.
- `debates/proposals/frontend-wizy.md` — Wizy areas that consume the same auth (custom magic, MyNet influence).
- `frontend/publish.md` — the play handoff pattern reused for auth.

## 7b. Email authentication — planned, not implemented

The email step stays in the ladder as **planned**. When it is built:

| Provider | Flow | Level |
|---|---|---|
| Google | Google Identity Services → ID token → verifier validates `aud` + `email_verified` via Google `tokeninfo` | L2 presence |
| Email code | `POST /email/request {email}` → 6-digit code (10 min, rate-limited) → `POST /email/verify` | L2 presence |
| Other providers | same contract, one verifier per provider | L2 presence |

Rules:

- The page never validates a Google token alone and never holds a client secret.
  The verifier holds `GOOGLE_CLIENT_ID` (public) and any SMTP credentials.
- Codes are single-use, TTL 10 min, rate-limited per email/IP; no code in the
  page.
- Success adds `email` to `identities`, sets `email.status = verified`, and
  opens Appy with `?unlock=email`; L2 is email presence, not MyNet.
- The email step in Authy must stay a **“planned” note** until the verifier and
  the SMTP transport exist.

Out of scope until then: no Google script in Authy, no `/email/*` endpoints in
the bot server, no `state.email` writes.

## 7c. Risa as identity provider — signed claim (planned)

The second risa → Appy model. Risa already knows the Telegram account behind a
clip; instead of sending the user through `@AuthyTgBot` again, risa signs a
portable presence claim.

```json
{
  "schema": "flove-auth/1",
  "iss": "risa-bot",
  "risaKey": "<public risa key>",
  "telegram": { "idHash": "sha256:…", "username": "…" },
  "level": "presence",
  "iat": "…",
  "exp": "…",
  "signature": "…"
}
```

Flow:

1. Risa bot signs the claim with its key (the raw Telegram id stays private;
   `idHash` is enough).
2. The claim is published as a **Browsy web-of-trust edge**; peers pull it
   locally; Wizy derives on the peer; Nety receives only an optional Social
   card.
3. Appy verifies the signature and grants **presence**. **MyNet still needs
   Authy L3**; a risa signature alone is not an Authy claim.
4. **L4 / publishing** remains the separate `@AuthyTgBot` claim. A risa
   signature never unlocks publishing.

Trust requirements: issuer public key, audience/expiry, replay cache, revocation
(Browsy edge), and no raw Telegram ids. The diagrams live in
`apps/sys/authy/index.html` §03b (Models A and B).

## 7d. MyNet feature flags and Browsy identity

MyNet is not a second ladder. It is the name of the local feature set that
opens with **Authy L3 · Telegram presence**. Publishing is a separate
**Social** section at **Authy L4 · Telegram verified**; it shares the tab but
is not a MyNet tier. L1/L2 (the versions without AuthyTg or risa bot) see the
MyNet functions in read-only and can export the MyFamily JSON.

L3 is **presence**: the bot records a private `/start` (including the risa
handoff `/start risa_<key>`), but the Telegram account is not bound to the
Authy profile with a challenge. L4 is **verified**: Authy generates a one-time
nonce, the user sends `/start claim_<nonce>` in a private DM, and the verifier
matches it to the profile. That is a fresh, one-use, replay-resistant binding;
only L4 can sign Social cards or publish.

| Flag | Requires | Surface | When locked |
|---|---|---|---|
| `mynet.preview` | always | tab, explanation, links, counts | visible |
| `mynet.family.export` | always | MyFamily JSON export | visible |
| `mynet.invite.redeem` | L3 | enter/validate invite code | hidden |
| `mynet.invite.manage` | L3 | generate, revoke, disown, chain | hidden |
| `mynet.people` | L3 | favourites and people list | placeholder + lock |
| `mynet.people.add` | L3 | add friend / search | disabled |
| `mynet.circles` | L3 | groups, follows/supports | placeholder + lock |
| `mynet.circles.join` | L3 | join group | disabled |
| `mynet.feed.local` | L3 | local feed | placeholder |
| `mynet.post.local` | L3 | publish to MyNet/Group/Private | disabled |
| `mynet.follow` | L3 | follow/support | disabled |
| `mynet.family.record` | L3 | simplified MyFamily record | hidden |
| `social.feed.read` | L3 | read public posts (no groups) | visible, read-only |
| `social.publish.post` | L4 | publish Public / queue | disabled + “Verify Telegram” |
| `social.groups` | L4 | read/join/create public groups | hidden |
| `social.grants.public` | L4 | public grants | disabled |
| `social.moderation` | L4 + role | curator queue | hidden |
| `mynet.trust.weight` | L5/L6 | invite quota, co-sign weight | unchanged |

**Two lock cards, not one gate.** The tab shows a **MyNet local** card (L3) and
a **Social publishing** card (L4). The public feed is read-only at L3 and sits
outside the L4 card. `mynet.invite.redeem` and `manage` live inside the MyNet
local card; there is no anonymous redeem. The current single `mynet-locked`
class hides almost everything; it must become per-feature.

**Transitions.**

- L1/L2 → L3: local flags on; social still off.
- L3 → L4: social on; local unchanged.
- L4 → L3: social off; local on; queued posts stay.
- L3 → L1/L2: local and social off; preview/export on; stored data stays.
- `issuer:"risa-bot"` or email-only: no flags; show “Link Telegram via Authy”.
- A verified claim never downgrades to presence automatically; only revoke or
  expiry does.

**Implementation in Appy.**

- `mynetFlags()` returns the Set; `applyMyNetFlags()` toggles `hidden`,
  `disabled` and `aria-disabled` on `[data-mynet]` elements.
- `mynetEnabled()` = Authy-issued Telegram presence; `socialEnabled()` = L4
  verified. `publishUnlocked` reads `socialEnabled()`, not `level >= 3`.
- `refreshAuthyStatus()` calls `applyMyNetFlags()`; `storage`/`focus` re-check.
- `renderMyNet()` must not render local lists when the local flag is off; show
  placeholders, not stale data.
- Replace the top “demonstrative only” notice with the two lock cards.

**Resolved.**

- Invite redeem requires L3; no anonymous redeem.
- Public feed is read-only at L3.
- Public groups are all L4: read, join, create.

**Flag resolution.**

```js
function authyFacts() {
  const a = readAuthy() || {};
  const tg = a.telegram || {};
  const issuerOk = !tg.issuer || tg.issuer === 'authy-bot';
  const presence = !!tg.status && tg.status !== 'none' && issuerOk;
  return {
    presence,
    verified: presence && tg.status === 'verified',
    email: !!(a.email && a.email.status === 'verified'),
    issuer: tg.issuer || null
  };
}

function mynetFlags() {
  const f = authyFacts();
  const flags = new Set(['mynet.preview', 'mynet.family.export']);
  if (f.presence) {
    ['mynet.invite.redeem', 'mynet.invite.manage', 'mynet.people',
     'mynet.people.add', 'mynet.circles', 'mynet.circles.join',
     'mynet.feed.local', 'mynet.post.local', 'mynet.follow',
     'mynet.family.record', 'social.feed.read'].forEach(x => flags.add(x));
  }
  if (f.verified) {
    ['social.publish.post', 'social.groups', 'social.grants.public']
      .forEach(x => flags.add(x));
  }
  return flags;
}
```

**DOM contract.**

| Hook | Flag | Locked behaviour |
|---|---|---|
| `[data-mynet="local"]` | any local flag | replace with the local lock card |
| `[data-mynet="social"]` | `social.publish.post` | replace with the social lock card |
| `[data-mynet="people"]` | `mynet.people` | placeholder, no data |
| `[data-mynet="circles"]` | `mynet.circles` | placeholder, no data |
| `[data-mynet="feed.local"]` | `mynet.feed.local` | placeholder |
| `[data-mynet="invite.redeem"]` | `mynet.invite.redeem` | hidden |
| `[data-mynet="invite.manage"]` | `mynet.invite.manage` | hidden |
| `[data-mynet="people.add"]` | `mynet.people.add` | disabled |
| `[data-mynet="circles.join"]` | `mynet.circles.join` | disabled |
| `[data-mynet="post.local"]` | `mynet.post.local` | disabled |
| `[data-mynet="follow"]` | `mynet.follow` | disabled |
| `[data-mynet="social.feed"]` | `social.feed.read` | read-only; no actions |
| `[data-mynet="social.publish"]` | `social.publish.post` | disabled + verify hint |
| `[data-mynet="social.groups"]` | `social.groups` | hidden |
| `[data-mynet="social.grants"]` | `social.grants.public` | hidden |
| `[data-mynet="social.moderation"]` | `social.moderation` | hidden |

**Copy (bilingual).**

- Local lock: “Link Telegram with @AuthyTgBot to unlock MyNet: people, circles,
  local feed and sharing.” / “Vincula Telegram con @AuthyTgBot para activar
  MyNet: personas, círculos, feed local y compartir.”
- Social lock: “Verify Telegram in Authy to publish and join public groups.
  MyNet local stays available.” / “Verifica Telegram en Authy para publicar y
  unirte a grupos públicos. MyNet local sigue disponible.”
- Risa issuer: “Telegram is linked to risa, not Authy. Link it with
  @AuthyTgBot.” / “Telegram está vinculado a risa, no a Authy. Vincúlalo con
  @AuthyTgBot.”
- Email only: “Email is presence, not MyNet. Link Telegram with @AuthyTgBot.”
  / “El email es presencia, no MyNet. Vincula Telegram con @AuthyTgBot.”
- Read-only public feed: “Read-only. Verify Telegram to publish.” / “Solo
  lectura. Verifica Telegram para publicar.”

**Acceptance.**

1. No Authy Telegram: preview + export visible; local and social cards visible;
   no data lists; invites hidden.
2. Risa-only: same as (1) plus the risa message.
3. Email L2: same as (1) plus the email message.
4. L3: local flags on; public feed read-only; `Public` option absent or
   disabled; groups, grants and moderation hidden; invites redeem/manage on.
5. L4: social flags on; `Public` option visible; groups and grants visible;
   moderation only for curators.
6. L4→L3: social off; local on; queued posts remain; `Public` disappears.
7. L3→L1: local off; preview/export on; stored data remains; no stale lists.
8. Storage blocked: flags derive from in-memory authy; show an “unknown” state
   if authy cannot be read.
9. `file://` and mobile: same flags; no extension required.
10. Keyboard: locked actions use `aria-disabled` with a reason; lock cards are
    focusable; no hidden focus traps.

**Out of scope.** L5/L6 trust-weighted quotas and curator roles beyond
`isCurator()` are not in v1.

**No MyNet hash.** Browsy has its own user hash; MyNet is only a name for the
local feature set.

### Browsy hash

**Definition.** One identity, one hash:

```
hash = PeerId = CIDv1(sha256(ed25519_pubkey)) → bafk…
```

The full `bafk…` value is stored; the UI shows a short prefix with a copy
action. Nety's `PeerId::from_public_key_bytes` already implements the same
formula, so Browsy and Nety share the identity without a second hash.

**Generation (hybrid).**

| Context | Creates the root | Stores the private key | What the page sees |
|---|---|---|---|
| Extension installed | background service worker | `chrome.storage.local` (v1) → encrypted vault (M2), key `browsy-keys` | extension UI; optional display handoff to Appy/Browsy index |
| No extension (web) | Browsy index / Appy embed | `flove:identity` (full local, `source:"web"`) | public hash; visible “local key, not portable” warning |
| `file://` | web fallback | `flove:identity` (local, `source:"web"`) | public hash; the extension manifest does not cover `file://` |

- The extension is canonical whenever present. Its own UI creates and shows the
  root; no page asks it for identity, signatures or vault data.
- The web fallback is a **full local identity** with `source:"web"` and a
  visible warning; it can sign local grants, works on mobile, and is **not
  portable** to the extension. There is no web→extension migration in v1.
- An existing web local identity stays a separate `source:"web"` record, hidden
  by default, and never becomes the extension root.
- The web fallback generator lives in Browsy index and Appy embed; the
  extension’s own UI owns the canonical generator. The extension exposes
  `getOrCreateIdentity()` and `sign()` internally; it never hands out the seed
  to a page.
- Appy SelfAuth and Authy Self replace the paste-only field with the web
  fallback generator; when the extension is installed they show its hash through
  an explicit display handoff, not by importing the root.
- **Recovery (v1):** a 12-word seed at creation; social quorum later. The seed
  is the only recovery path for a local key, so the warning must say it.

**Status (2026-11-18).** The web fallback is live:
`apps/sys/browsy/index.html` generates an Ed25519 key with WebCrypto, derives
the CIDv1 PeerId, stores `flove:identity` (`source:"web"`, `notPortable:true`)
and keeps the private seed only in that page's localStorage. Appy embeds the
generator (`?embed=1`) in the Authenticate card and mirrors the public hash to
`flove:authy.self.browsyHash`. The extension `getOrCreateIdentity()`/bridge and
the Nety root import remain pending.

**Persistence.** Canonical record `flove:identity` (schema
`flove-identity/1`):

```json
{ "schema":"flove-identity/1", "hash":"bafk…", "publicKey":"…", "source":"extension|web", "createdAt":"…", "label":"" }
```

`flove:browsy` is a read-only view of the same record. Authy Self may cache the
public hash in `flove:authy.self.browsyHash` for display; it is Browsy’s hash,
not a MyNet hash. Same persistence pattern as Authy: localStorage,
`storage`/`focus` refresh, one-shot handoff when blocked.

**Nety (direction: same root; transport open).** The chosen direction is to
import the same root into Nety’s encrypted keystore, so the resulting `PeerId`
is the same hash. The transport is undecided — encrypted export, native
messaging or seed phrase (see `pendings.md` K08). Delegation (a Nety peer key
attested by the Browsy root) remains the v2 path for multi-device.

## 7e. MyNet state and storage

**Goal.** Persist the local MyNet record across reloads and lock changes without
ever deleting it on downgrade. Local data is L; public posts are S and only
exist after L4.

**Key and schema.** `flove:mynet` (`flove-mynet/1`):

```json
{
  "schema": "flove-mynet/1",
  "owner": "bafk…",
  "updatedAt": "…",
  "people": [],
  "circles": [],
  "follows": [],
  "supports": [],
  "favourites": [],
  "posts": { "local": [], "social": [] },
  "invites": { "budget": 3, "used": 0, "codes": [] },
  "seeded": false
}
```

| Field | Class | Notes |
|---|---|---|
| `owner` | M | Browsy hash; absent in a web/demo identity |
| `people` | L | person, relation, 2–3 traits, affinity, optional note |
| `circles` | L | name, members |
| `follows` / `supports` / `favourites` | L | handles/ids |
| `posts.local` | L | visibility MyNet/Group/Private; status live |
| `posts.social` | S | public posts/queue; status pending/live/rejected |
| `invites` | M | budget, used, codes and lineage |
| `seeded` | M | true when the demo state was first persisted |

**Rules.**

- Read on load; if missing, seed from the current in-memory demo once and set
  `seeded:true`. Never re-seed after the user edits.
- Write on mutation with a 250 ms debounce; immediate on publish or invite.
- Locking (L3 off) hides UI but never clears storage.
- `L4→L3`: local posts stay; social posts become read-only; no new public posts.
- `owner` mismatch (new Browsy hash): prompt **Keep local / Export / Start
  fresh**; never merge silently.
- Storage blocked: keep an in-memory copy and show a warning; do not pretend it
  was saved.
- Corrupt JSON: keep the raw value under `flove:mynet:broken`, start empty and
  show a recovery note.
- Public posts contain no P fields; only the user’s chosen text and S metadata.

**API.**

```js
readMyNet()            // flove-mynet/1 or null
writeMyNet(patch)      // merge + schema + updatedAt
saveMyNet()            // debounced persistence
mynetOwner()           // flove:identity.hash || flove:authy.self.browsyHash || null
```

Event: `flove:mynet:changed` with `{ schema, counts }`; a `storage` listener on
`flove:mynet`.

**Migration.**

1. `flove:mynet` absent → seed from `state` once.
2. `schema` missing or old → map known fields, keep unknown under `legacy`.
3. `owner` absent → attach `mynetOwner()` when available; otherwise leave null.
4. Never delete a field the UI no longer uses; keep it for export.

**Acceptance.**

1. Add a person, reload, it survives.
2. Lock L3, reload: data survives; lists are empty until unlock.
3. L4→L3: social posts remain but are read-only.
4. New owner: prompt, no silent merge.
5. Storage blocked: memory warning, no false “saved”.
6. Corrupt JSON: does not crash; recovery note.
7. Public post contains no P fields.

## 8. Status

SelfAuth (L1), the Telegram claim (L3→L4) and the Appy unlock tour are live. **Email authentication is moved to the plan below and is not implemented** — the Authy email step says so.

The client, the bot/verifier code, Appy sync and the handoff are live. The only
human step left is **BotFather**: create `@AuthyTgBot`, put its token in
`TELEGRAM_BOT_TOKEN`, run `node apps/sys/authy/bot/server.mjs`, and point
Authy at `?bot=AuthyTgBot&verify=https://…/claim`. Until then the demo
confirmation is the fallback. Browsy attestation is the next build.
