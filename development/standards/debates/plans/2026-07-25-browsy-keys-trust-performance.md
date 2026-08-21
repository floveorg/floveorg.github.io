# Browsy: Keys, Trust & Performance Architecture

> 2026-07-25. Where keys/trust live, what browsy actually does, and what stays out of the short term.

## Core Principle

**Browsy is the on-demand data layer.** Not Central. Central holds published files and their stats. Browsy gives you a custom layer of insights and matches based on what you're browsing — accurate on flove.org, less so on theguardian.co.uk, but always local and on-demand.

## Keys, Auth, Trust: Inseparable

Trust networks are hard to decouple from keys. They stay together in browsy.

- Keys: Ed25519, deterministic from auth factors (Q93a)
- Auth: device + Telegram + email + trust vouches (Q93c)
- Trust: vouches signed locally, stored in Extension storage
- Recovery: 12-word mnemonic, 2-of-5 social recovery (Q112-Q124)

**v1:** Keys created IN browsy (self-contained, works offline)
**v2:** Nety-bridge API when nety Rust stack matures

## What Browsy Actually Does

Four categories. Everything else is a subelement within them.

1. **Keys** — Ed25519 keypair, deterministic, recoverable
2. **Auth** — device + Telegram + email + trust vouches, composite identity
3. **Trust network** — vouches, 3-hop chains, heritage, recovery, tiers, sync, webhooks, DMs, permission groups, publish consent
4. **Finetuner** — on-demand insights and matches from the data you're browsing

Sync, DMs, heritage, webhooks are subelements of these 4, not separate features.

## Finetuner Spec

### Interaction model

- **Click-only** — finetuner runs when user clicks wizy icon, zero background CPU
- No reactive scoring, no badge, no background parsing
- Wizy.js does the deep analysis client-side

### Detection (v1: flove.org only)

- HTML parsing for content extraction (visible text, entities, structure)
- User-declared interests from profile for matching
- External sites deferred entirely — v1 is flove.org pages only

### Whitelist (v2: + external)

Whitelist is the agent's knowledge base. Two types:

- **Web pages** to parse (URL patterns for fast routing)
- **Context documents** — local base info the agent uses to make suggestions

Context docs format:
- **Full text** for small docs (stored in Extension storage, agent reads directly)
- **Pointers** for large docs (URLs/file paths, agent fetches on demand)
- Agent decides based on size which approach to use
- Pointers can reference other pointers if more comfortable for the agent

Whitelist managed in browsy settings page. Browsy parses locally, sends to user only — never to parsed site, Central, or trusts.

### Storage

- Results stored in Extension storage alongside trust data
- **Separate keys:** trust = `browsy:trust:*`, finetuner = `browsy:score:*`
- Shape per match: `{ score, reason }` — lightweight
- **LRU with 1MB cap** for finetuner results, trust always wins on eviction
- Accessible from any page via `flove-bridge.js`

### Re-scoring

- **Full navigation only** — score once on `document_idle`, never re-score
- Manual re-score button in browsy if user thinks content changed
- Zero background CPU, no MutationObserver

### Wizy trigger

- **Local first, Central optional**
- Wizy.js does deep analysis client-side using local trust + profile data
- **Degrades gracefully when Central is offline** — fewer suggestions, local-only ones show, "offline mode" hint

### Wizy data from browsy

- **Summary only** (~1KB): `{ trustScore, topConnections, tierSummary }`
- No raw trust graph sent to pages
- Page can whitelist-request specific filtered data on top of summary

## Permission Groups (Standardized from appy-basic)

### Critical design: permissions must be fast

The permission system resolves on every wizy click. It must be zero-background-CPU and fast click response.

### What they control

Permission groups control **content visibility** AND **context scope for the finetuner**.

- Who sees content
- Which context documents the agent uses when scoring a page

### Group model (4 groups, flat)

| Group | Default visibility | Purpose |
|-------|-------------------|---------|
| **Close** | MyNet | Friends — direct vouches only |
| **Public** | Public | Everything public, discovery |
| **Private** | Private | Only you see this |
| **Custom** (1 slot) | Private | User-created, user-named |

**4 total, flat** — no nesting, no subgroups. Simple O(1) lookup.

### Friends (MyNet v1)

**Friends = Close group.** A friend is someone you've directly vouched for, or who directly vouched for you. No chains, no delegation.

- Friends list is the Close group member list
- Direction: mutual (strongest), outgoing (you trust them), incoming (they trust you)
- Friends see your Close content automatically
- Stale after 60 days no interaction (dimmed, access continues)
- Adding = vouching, removing = revoking

The MyNet tab shows: friends (sorted by mutual → outgoing → incoming), trusts, scores.

### Group structure

Each group contains:
- **People** — list of group members
- **Rules** — visibility rules (who in this group sees what)
- **Context pointers** — references to context documents the finetuner uses for this group

Context documents are added **in the group creation flow** — when user creates or edits a group, there's a "Context docs" section with add/remove. No separate settings page.

### Publish flow (replaces basic's dropdown)

**appy-basic:** textarea → visibility dropdown (MyNet/Group/Public/Private) → submit

**appy-normal:** textarea → checkbox group selection (up to 3 groups) → browsy signs → Save local / Publish

The dropdown is replaced entirely by checkboxes. No backward compat needed.

### Resolution model

- **On wizy click only** — zero background work
- **Index in memory** — lightweight group IDs + member count stored in Extension storage
- **Full data fetched on click** — groups, trust slice, context pointers loaded when user clicks wizy
- No pre-computation, no caching, no MutationObserver

### Invalidation

- Context doc changes → mark affected scores **stale**
- Stale scores re-computed on next wizy click (lazy)
- No aggressive invalidation, no TTL, no full re-score cascade

### Externalization

Permission groups are a **flove standard**. Any flove system can read and respect them:
- Browsy uses them for visibility + finetuner context scope
- Central respects them for server-side visibility
- Nety can use them for trust scoping
- Any flove app can query groups via `flove-bridge.js`

### Storage

Groups live in Extension storage (`browsy:groups:*`). Synced to Central when user publishes. Conflict: last sync wins.

### Tier scaling

- **Basic:** Simple visibility (dropdown or minimal groups) — no context pointers
- **Normal:** Full 4 groups with context pointers, checkbox publish, browsy signing
- **Advanced+:** Groups persist, context pointers multiply, finetuner deepens

## What Stays Out of the Short Term

- Advanced visualization → HTML pages, not extension
- External site parsing → v2
- P2P features → nety extension layer, optional

## Vanguard Demo: Rewardy

Rewardy (`apps/economy/dealy/rewardy.html`) is the first browsy-powered app. It demonstrates the suggestion API in a real comparison tool.

### Current state

Hardcoded `s/t/d` scores per person (souls, trust, deal). No browsy connection.

### Browsy integration

Rewardy's 3 scores come from 3 different systems:

| Rewardy score | Source | What it measures |
|---|---|---|
| **souls** (s) | souls app | Matching/compatibility between two people |
| **trust** (t) | browsy facets | Reliability: social + local vouches |
| **deal** (d) | browsy finetuner | Value: offer vs market, trust-weighted pricing |

### Suggestion API

Browsy provides trust + deal. Souls comes from the souls app separately.

```
// Browsy suggestion
browsy.suggest(['bob', 'alice', ...])
→ [{ key, trust:{score,reason,confidence}, deal:{score,reason,confidence} }]

// Souls from souls app (separate call)
souls.match(['bob', 'alice', ...])
→ [{ key, score, reason }]
```

- **confidence** (0-1): how sure browsy is, based on data freshness + chain depth
- **reason**: human-readable explanation ("social:45 + local:15")
- Fallback: Central stats when browsy offline

### Data flow

```
Rewardy loads → sends user list to browsy + souls app
Browsy evaluates: trust facets + finetuner (deal scoring)
Souls app evaluates: matching/compatibility
Both return suggestions with confidence
Rewardy renders with combined scores
If browsy offline → Central stats fallback (less accurate)
```

### What Central contributes

Central provides published offers, transaction history, profiles, and stats. Browsy combines these with its local trust graph for richer scoring.

## Performance Budget

50MB storage / 100MB memory / 1% CPU idle.

- WASM (sql.js) gets priority, everything else defers until it loads
- Browsy is a data store + signal emitter, not a computation engine
- Finetuner is click-only — zero background CPU
- Pages do the rendering and heavy logic via `flove-bridge.js` postMessage
- Central does its own stats from published files, browsy doesn't duplicate that

## Architecture

```
browsy (extension)     →  keys + auth + trust + finetuner (local, on-demand, click-only)
flo pages (HTML)       →  advanced viz + wizy agent + external load
Central (FastAPI)      →  published files + their stats + sync hub
nety (future ext)      →  P2P compute donation, optional layer on top of browsy
```

## Decisions Summary

| # | Decision |
|---|----------|
| Q1 | Finetuner is click-only, no reactive scoring |
| Q2 | Flove.org only for v1, external sites deferred |
| Q3 | LRU with 1MB cap for finetuner results |
| Q4 | Summary only (~1KB) to pages + whitelist-request filtered data |
| Q5 | 4 categories ARE the superset, sync/DMs/heritage/webhooks are subelements |
| Q6 | Browsy parses locally for user only, never sends to parsed site/Central/trusts |
| Q7 | Wizy degrades gracefully when Central offline |
| Q8 | Whitelist in browsy settings page |
| Q9 | Separate keys in Extension storage, shared 10MB pool |
| Q10 | Full navigation only, manual re-score button |
| Q11 | Whitelist = web pages + context documents (full text or pointers, agent decides) |
| Q12 | Permission groups = people + rules + context pointers (no scores) |
| Q13 | Groups are a flove standard, any system can read them |
| Q14 | Group-to-context mapping deferred, agent picks based on page content |
| Q15 | Permission check = on wizy click only, zero background CPU |
| Q17 | Context doc changes = mark stale, re-score on next click (lazy) |
| Q18 | Memory = index only, full data fetched on wizy click |
| Q19 | 4 groups total (Close, Public, Private + 1 custom), flat, no nesting |
| Q20 | Publish flow: checkboxes replace dropdown, browsy signs |
| Q21 | Context docs added in group creation flow, not separate settings |
| Q22 | Defaults: Close=MyNet, Public=Public, Private=Private |
| Q23 | Basic tier uses simple visibility, Normal gets full groups + context |
| Q24 | Friends = Close group, direct vouches only, MyNet v1 |
| Q25 | v1 = direct vouches only, no delegation/chains (v2) |

## Recommendation

1. **v1:** Keys + auth + trust + finetuner in browsy. Self-contained. Flove.org only.
2. **v2:** Nety-bridge for P2P, external site whitelist, richer finetuner.
3. **Never in browsy:** Heavy viz, agent finetuning, background computation.
4. **Don't bloat short term.** Ship the four core things well.
