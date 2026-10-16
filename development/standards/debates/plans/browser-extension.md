# Browser Extension Plan

> A lightweight browser extension that bridges flove apps with the rest of the web.
> Could be the most optimal tool for the project: extends flove's reach beyond flove.org.

## Why a browser extension?

1. **Discovery** — Users stumble on flove apps from any context (links, search, social)
2. **Integration** — Export/save/share any web content directly into flove apps
3. **Bridge** — flove apps can read/write to any page (context injection)
4. **Offline first** — Extension works offline, syncs when online (mirrors flove philosophy)
5. **Universal** — One install, works everywhere flove apps exist

## Core features (MVP)

### 1. Flove detection
- Detects `flove.org` pages and local flove instances
- Shows extension badge when on a flove page
- Quick actions: Open app, Download, Share

### 2. Web → Flove bridge
- "Save to flove" button on any webpage
- Content extraction (text, images, links) → flove apps
- Works with blogy (save articles), economy apps (save deals), etc.

### 3. Flove → Web bridge  
- Export flove content to any page (paste into forms, share on social)
- Copy/paste bridge between flove apps and other sites

### 4. Nety share integration
- Right-click on any page → "Share to Nety"
- Extracts page title, URL, selected text → Nety post draft
- Works from any site, not just flove pages

### 5. Context menu
- Right-click → "Open in flove" (detects relevant app)
- Right-click → "Save selection to flove"

### 6. Quick panel
- Popup panel showing nearby flove apps
- Search flove apps
- Recent flove activity

### 7. Smart app detection
- Analyzes page content → suggests relevant flove app
- URL pattern matching (e.g., github.com → blogy)
- User can override suggestion

### 8. Batch export
- Select multiple pages/tabs → export to flove
- Create reading list in blogy
- Bulk save deals in economy apps

### 9. Flove notifications
- Badge shows unread items from flove apps
- Click badge → see recent activity
- Syncs with Central when online

### 10. Developer tools
- Inspect flove app structure from any page
- Debug flove-bridge.js connections
- View app routing and data flow

### 11. Discovery (custom scores)
- **Badge** on all public profiles — shows when browsing any page
- **+50% threshold** — always show when match > 50%
- **Data source** — parse page HTML (simplest)
- **Detail view** — custom breakdown like rewardy (souls, trusts, deal scores)
- **Privacy** — client-side only, full profile stays local

**Flow:**
1. User browses any page
2. Browsy detects profile data in HTML
3. Parses public info (interests, mynet, app usage)
4. Compares to private profile (full score spectrum)
5. Shows badge: "New: 3 connections" or "New: 87% match"
6. Click → detail view with souls/trusts/deal breakdown

### 12. Profile system
- Stores user preferences, reading habits, app usage history
- Minimal schema: interests + app usage frequency
- Nety data: connections list + activity scores
- All data stored locally (privacy-first)

### 13. Compatibility scoring
- Analyzes pages against profile
- Suggests best flove app based on interests
- Shows percentage match (e.g., "87% compatible with your reading style")

### 14. Auth integration
- Email magic link (Phase 1)
- Telegram bot verification (Phase 1)
- Same login across nety, browsy, and Central (no separate logins)
- WhatsApp, Signal, SSB, Biometry (Phase 2)

### 15. Profile sync
- Bidirectional sync with nety, Central, browser, local
- Sync priority: nety → Central → browser → local
- Auto-sync when online (every 5 min batched)
- Queue changes when offline

## Development Strategy

### MVP Scope
- **Pillars:** Auth + mynet + publish bridge (Q225)
- **Sync priority:** App data > mynet > auth (Q226)
- **Local vs synced:** Keys/drafts stay local; profile, trust, app state synced (Q229)
- **Privacy default:** Private by default, user publishes explicitly (Q230)

### Platform & Size
- **Target:** Chrome + Firefox desktop first, then mobile (Q231)
- **Size:** <10MB target 5MB (Q232)
- **Compat:** Last 2 major browser versions (Q243)

### Performance Budget
- 50MB storage / 100MB memory / 1% CPU idle (Q227)
- Configurable in options, recommended defaults (Q240)

### WASM Budget (SoloRich local persistence)
- sql.js WASM: ~1.5MB binary, ~8MB peak memory during init, ~200ms cold-start
- **Headroom rule:** Non-essential features (discovery scoring, notification badge, webhook exports) must defer until WASM is loaded. WASM init is the first priority after extension install.
- **Fallback:** If WASM fails to load, app falls back to localStorage silently (CA40). No error shown to user.
- **Alternative:** wa-sqlite (~400KB WASM, same API) is a drop-in replacement if sql.js exceeds budget. Evaluate if cold-start >500ms or peak memory >15MB.
- **Future:** Turso embedded replicas (no WASM, native SQLite file) when Turso Database stabilizes. Deferred to CentralRich.

### Unified Browsy Storage
- **Single API:** Extension storage (`chrome.storage.local`) for ALL browsy data
- Replaces: IndexedDB (trust scores, profiles), localStorage (export history), sessionStorage (panel state)
- Extension storage: persistent, synchronous API, 10MB quota in MV3 (enough for ~1.2MB trust working set)
- **Migration:** On first update after unified storage lands, one-time export from IndexedDB → Extension storage. Old keys removed after successful migration.
- **Exception:** nety keeps IndexedDB for structured circle queries (not browsy's concern)

### Offline Strategy
- IndexedDB log of pending operations (ordered by timestamp), replays on next connectivity check (Q228)
- `flove:pending-sync` flag shows count of pending items in bottom nav badge

### Testing & Docs
- Unit + integration + manual (Q234)
- README + API docs + user guide (Q235)
- Security audit after MVP (Q239)

### UX
- Tour completo 5+ pasos (Q236)
- Auto-update + changelog (Q233)
- Error reporting: console + crash reports con consent (Q237)
- Analytics: todo detallado, opción "No trace" (Q238)

### Feedback & Release
- GitHub issues + botón in-app + circle en users/ para sugerencias (Q241)
- Release: cuando hayan features, no preestablecido (Q242)

### Open Source
- Todo open source (Q244)

## Architecture

### Manifest V3 (Chrome/Edge) + Manifest V2 (Firefox)
- Service worker (background)
- Content scripts (page injection)
- Popup panel (UI)
- Options page (settings)

### Architecture: Browsy as Base Layer

**Target experience:** When browsing `flove.org/appy/*` with browsy, MyNet is active. When browsing with nety, additional P2P features are available.

**Layer model:**
- **Browsy (Base):** Detects flove pages, activates MyNet, main navigation
- **Nety (Extension):** Adds P2P features, computing donors only, optional

**Key insight:** Browsy is the base layer that works on all flove pages. Nety extends browsy with P2P capabilities.

### flove.js integration
- Extension injects `flove-bridge.js` into flove pages
- Bridge exposes extension APIs to flove apps
- Apps can opt-in to extension features

### Shared code with central/
- Reuse `flove-i18n.js` for extension UI
- Reuse `routing.json` for app detection
- Reuse `flove.css` for popup styling

## Profile sync architecture

### Priority order
1. **nety** — primary source for mynet data (connections, activity scores)
2. **Central** — sync hub for cross-device profile (libSQL)
3. **browser** — local cache (IndexedDB, 100MB limit)
4. **local** — file export (last resort)

### Sync behavior
| Aspect | Behavior |
|--------|----------|
| Threshold | Batched (every 5 min if changes exist) |
| Trigger | Auto-sync when online |
| Size limit | None (delta sync keeps it small) (Q213) |
| Multiple devices | Sync all (same profile everywhere), max 5 devices (Q212) |
| Offline | Local queue (IndexedDB), sync when back online (Q199) |
| Trust sync | Real-time (Q210) |
| Compression | gzip in transmission, raw in storage (Q223) |
| Encryption | TLS + E2E for trust data (Q224) |
| Staleness | 7 days offline = flagged (Q214) |
| Status UI | Badge in popup (Q221) |
| Error handling | Queue + notify after 3 retries (Q222) |

### Conflict resolution
| Scenario | Resolution |
|----------|------------|
| Conflict detection | Document level (Q206) |
| Minor conflict (single field) | Auto-resolve: latest timestamp wins |
| Major conflict (multiple fields) | Side-by-side diff, user decides (Q194) |
| Merge strategy | Field-level merge (preserve non-conflicting fields) (Q196) |
| Clock skew | Accept risk — NTP usually suffices (Q195) |
| Nety ↔ Central | Nety is authoritative (Q197) |
| Browsy ↔ Central | CRDT merge (vector clocks). Conflicts surfaced to browsy for display. (Q198) |
| Recovery source | Nety authoritative; browsy = ask user (Q201) |
| Undo | Yes, 30 days (Q218) |
| Logging | browsy local only (IndexedDB) (Q202) |
| History | 30 days, archive local (Q219) |
| Schema migration | Server accepts any version, ignores missing fields (Q203) |
| Device revocation | Re-vouch all trusts from another device (Q204) |
| Server validation | Reject invalid + log + notify (Q208) |

### Recovery
| Scenario | Recovery option |
|----------|-----------------|
| Local deletion | Keep in nety/Central, remove from browsy |
| Re-import | From Central, nety, or fresh start |
| Profile versioning | Timestamped snapshots (full history, restore any point) |

## Mynet sync (browsy ↔ Central ↔ nety)

### Sync architecture
| Source | Data | Sync method | Timing |
|--------|------|-------------|--------|
| **nety** | Connections, activity scores | API (future nety API) | Event-driven (chrome.alarms) |
| **Central** | Full mynet (libSQL) | Central backend API | Auto-sync when online |
| **Central** | Trust data | `POST /api/trust/sync` (separate endpoint) | Real-time (immediate on change) |
| **browsy** | Cached subset (last 24h) | Local Extension storage | Always available |

### Mynet data flow
1. **nety → browsy** — Pull connections + scores on sync
2. **browsy → Central** — Push profile + mynet subset
3. **Central → browsy** — Pull synced data from other devices
4. **browsy → nety** — Push profile preferences (interests, app usage)
5. **nety → Central** — Push all public data (Q200)

### Central backend requirements
- [ ] libSQL schema for browsy profiles
- [ ] API endpoints: GET/PUT /profile, GET/PUT /mynet
- [ ] Auth integration (same email/Telegram as browsy)
- [ ] Conflict resolution logic (timestamp-based)

### Nety future API requirements
- [ ] GET /connections — return user's connections list
- [ ] GET /activity-scores — return connection activity scores
- [ ] PUT /preferences — update nety preferences from browsy

## Specs at appy tabs (opacity)

### Profile tab (appy)
- **Opacity:** 100% when browsy installed, 60% when not
- **Content:** Profile overview, sync status, connected devices
- **Actions:** Export profile, view sync history, manage auth

### Mynet tab (appy)
- **Opacity:** 100% when browsy + nety connected, 40% when not
- **Content:** Connections list, activity scores, sync status
- **Actions:** Refresh from nety, export mynet, view conflicts

### Sync tab (appy)
- **Opacity:** 100% when Central configured, 50% when not
- **Content:** Sync history, conflict log, device list
- **Actions:** Force sync, view snapshots, manage devices

### Auth tab (appy)
- **Opacity:** 100% when auth configured, 70% when not
- **Content:** Email/Telegram status, recovery options
- **Actions:** Change email, add Telegram, recovery codes

### Portable format (JSON)
```json
{
  "version": "1.0",
  "profile": {
    "interests": [...],
    "appUsage": {...}
  },
  "mynet": {
    "connections": [...],
    "activityScores": {...},
    "lastSync": "2026-07-23T10:00:00Z"
  },
  "centralSyncId": "optional-uuid"
}
```

## Benefits for flove project

1. **Zero-friction onboarding** — Install once, use everywhere
2. **Offline capability** — Extension caches flove apps for offline use
3. **Cross-platform** — Works on Chrome, Firefox, Edge, Brave
4. **SEO boost** — Extension increases flove visibility
5. **Data portability** — Users can export/import flove data across devices
6. **Developer tools** — Debug flove apps from any page
7. **Social context** — Shows what connections saved (via mynet)
8. **Smart routing** — Auto-suggests best app for content

## Implementation phases

### Phase 1: Detection + Profile (week 1-2)
- [ ] Manifest setup (MV3 + MV2)
- [ ] Flove page detection (URL patterns)
- [ ] Badge indicator
- [ ] Basic popup panel
- [ ] Profile system (schema, storage)
- [ ] Auth integration (email + Telegram)
- [ ] Compatibility scoring (basic)
- [ ] Appy tabs: Profile tab (opacity 100%/60%)

### Phase 2: Bridge + Sync (week 3-4)
- [ ] Content script injection
- [ ] "Save to flove" context menu
- [ ] Content extraction API
- [ ] flove-bridge.js for app integration
- [ ] Profile sync (nety ↔ browsy ↔ Central)
- [ ] Conflict resolution UI
- [ ] Export/import (full profile JSON)
- [ ] Mynet sync (browsy ↔ Central)
- [ ] Appy tabs: Mynet tab (opacity 100%/40%)

### Phase 3: Integration (week 5-6)
- [ ] Export to web (copy/paste bridge)
- [ ] Quick panel with app search + recent activity
- [ ] Nety share integration
- [ ] Batch export (multi-tab)
- [ ] Options/settings page
- [ ] Appy tabs: Sync tab (opacity 100%/50%)

### Phase 4: Polish (week 7-8)
- [ ] Firefox compatibility
- [ ] Icon/badge design
- [ ] Store listings (Firefox + Chrome)
- [ ] Documentation
- [ ] Local web distribution (before store approval)
- [ ] Appy tabs: Auth tab (opacity 100%/70%)

### Phase 3: Integration (week 5-6)
- [ ] Export to web (copy/paste bridge)
- [ ] Quick panel with app search + recent activity
- [ ] Nety share integration
- [ ] Batch export (multi-tab)
- [ ] Options/settings page

### Phase 4: Polish (week 7-8)
- [ ] Firefox compatibility
- [ ] Icon/badge design
- [ ] Store listings (Firefox + Chrome)
- [ ] Documentation
- [ ] Local web distribution (before store approval)

### Phase 2+ (future)
- [ ] WhatsApp, Signal, SSB, Biometry auth
- [ ] flove-bridge.js opt-in/auto-detect integration
- [ ] API bridge (expose flove to other extensions)
- [ ] Reading mode (strip ads/clutter)
- [ ] Tab manager (group flove tabs)
- [ ] QR code generator
- [ ] Community highlights (anonymous)

### Phase 5: Discovery (week 5)
- [ ] Profile detection in page HTML
- [ ] Client-side matching engine
- [ ] Floating badge UI
- [ ] Detail view (souls, trusts, deal scores)

## Decisions made

### Brainstorm 2026-07-23

| ID | Question | Decision |
|----|----------|----------|
| BE01 | Extension name? | **browsy** |
| BE02 | Default behavior on flove pages? | **Manual activation** |
| BE03 | Content extraction scope? | **Full page** |
| BE04 | Offline storage limit? | **100MB** |
| BE05 | Sync method? | **Manual export** (Phase 1), auto-sync (Phase 2) |
| BE06 | Target browsers? | **Chrome + Firefox** |
| BE07 | Context menu behavior? | **Both** (Open in flove + Save selection) |
| BE08 | Quick panel features? | **App search + recent activity** |
| BE09 | flove-bridge.js integration? | **Both** (Auto-detect URL + Opt-in attribute) |
| BE10 | Store listing strategy? | **Firefox + Chrome, local web first** |
| BE11 | Discovery trigger? | **Badge on all profiles, +50% always** |
| BE12 | Discovery data source? | **Page HTML parsing** |
| BE13 | Discovery button style? | **Floating badge** |
| BE14 | Discovery detail view? | **Custom (souls, trusts, deal scores)** |
| BE15 | Discovery privacy? | **Client-side only** |
| BE16 | Auth methods (Phase 1)? | **Email + Telegram** |
| BE17 | Same login across nety/Central/browsy? | **Yes** |
| BE18 | Profile schema? | **Minimal** (interests, app usage frequency) |
| BE19 | Nety data in browsy? | **Connections list + activity scores** |
| BE20 | Sync threshold? | **Batched (5 min)** |
| BE21 | Sync trigger? | **Auto-sync when online** |
| BE22 | Sync priority? | **nety → Central → browser → local** |
| BE23 | Multiple devices? | **Sync all (same profile everywhere)** |
| BE24 | Conflict resolution? | **Hybrid** (auto-resolve minor, show major) |
| BE25 | Major conflict threshold? | **Single field change** |
| BE26 | Minor conflict resolution? | **Latest timestamp wins** |
| BE27 | Merge strategy? | **Non-destructive** (preserve extra fields) |
| BE28 | Export scope? | **Full profile** |
| BE29 | Sync logging? | **Conflicts only** |
| BE30 | Sync size limit? | **None** |
| BE31 | Offline behavior? | **Queue changes, sync when online** |
| BE32 | Profile deletion? | **Keep in nety/Central, remove locally** |
| BE33 | Recovery options? | **All** (Central, nety, or fresh start) |
| BE34 | Profile versioning? | **Timestamped snapshots** (full history) |
| BE35 | Central auth? | **Same as nety/browsy** (no separate login) |

### BX Questions 2026-07-24

| ID | Question | Decision |
|----|----------|----------|
| BX01 | Permissions? | **`activeTab` only** |
| BX02 | Bridge communication? | **Window messaging (`postMessage`)** |
| BX03 | Profile HTML format? | **JSON-LD** |
| BX04 | Batch export handling? | **Chunked export** |
| BX05 | Notification sync? | **Push notifications from Central** |
| BX06 | Fallback if no extension? | **Reduced features** |
| BX07 | 100MB storage limit? | **User-managed** |
| BX08 | Manifest V3 vs V2? | **Shared codebase** |
| BX09 | Store review policies? | **Focus on flove pages only** |
| BX10 | Timeline for 11 features? | **Extend to 10-12 weeks** |

### Browsy implementation decisions 2026-07-24 (Q51–Q70)

| ID | Question | Decision |
|----|----------|----------|
| Q51 | Popup panel layout? | **Full dashboard: tabs (Activity \| Profile \| Settings)** |
| Q52 | Side panel vs popup? | **Popup only (no side panel)** |
| Q53 | Options page scope? | **Everything: permissions, theme, data export, account link, debug mode** |
| Q54 | Badge rules? | **Only on flove.org pages** |
| Q55 | Content script injection timing? | **On demand only (user clicks browsy icon)** |
| Q56 | Permission request UI? | **Onboarding + just-in-time** |
| Q57 | Auth token storage? | **Extension-internal encrypted store** |
| Q58 | Feature flag source? | **App bridge first, Central fallback** |
| Q59 | Dev tools panel? | **No dev tools panel (use browser devtools console)** |
| Q60 | Error recovery? | **Auto-retry with exponential backoff (3 attempts)** |
| Q61 | Update flow? | **Silent update** |
| Q62 | Keyboard shortcuts? | **None** |
| Q63 | Context menu structure? | **No context menu (deferred per BD06)** |
| Q64 | Multi-device sync? | **Via GitHub repo (export JSON on each device)** |
| Q65 | Crash recovery? | **Full state preserved: overlay, conversations, notifications, auth** |
| Q66 | First-run onboarding? | **Quick tour: 3-step walkthrough (detect → overlay → auth)** |
| Q67 | Performance budget? | **User-configurable in options, recommended defaults (50MB storage / 100MB memory / 1% CPU idle)** |
| Q68 | Web permissions model? | **flove.org + user-whitelisted sites** |
| Q69 | Telemetry? | **Full telemetry with consent (install count, feature usage, crash reports, page visits, trust graph stats)** |
| Q70 | Storage sync across updates? | **Backward-compatible by design (no migration needed)** |
| Q93 | Message encryption? | **Encrypted with composite auth token (identity layers)** |
| Q93a | Signing key type? | **Deterministic — derived from auth factors, recoverable** |
| Q93b | Factor count visibility? | **Visible to receivers ("3-factor signed")** |
| Q93c | Auth model? | **Extends existing: device + Telegram + email + trust vouches** |
| Q93d | Factor display privacy? | **Count visible, specific factors TBD** |
| Q93e | Bonus scope? | **Navigation bonuses + feature access + visibility weight** |
| Q93f | Trust hierarchy? | **Layer 0: device → Layer 1: Telegram → Layer 2: Email → Layer 3: Trust vouches** |
| Q93g | Browsy slogan? | **Authenticity and web of trust for flove apps** |
| Q93h | Fork source? | **nety.html — extract crypto/identity layer, adapt for browsy** |
| Q93i | Key recovery? | **Re-link factors + recovery code at setup (like nety masks)** |
| Q93j | Vouch mechanism? | **Signed statement → B's key gains trust factor + stored in browsy + Central** |
| Q93k | First circle scope? | **Trusts/heritage + trusts/recovery are browsy config actions, part of first circle** |
| Q101 | First circle contents? | **Empty, user adds manually. Tabs: Trusts \| Recovery \| Heritage** |
| Q102 | Vouch chain depth? | **3 hops (matches nety's trust graph)** |
| Q103 | Heritage purpose? | **Accountability partners + inherit trust chain. Public by default, claim after 1 year idle** |
| Q104 | Recovery purpose? | **Trusted contacts who can help recover your account** |
| Q105 | Idle claim process? | **1 year idle → heritage can claim** |
| Q106 | First circle size? | **Unlimited. Heritage + recovery require approval to join** |
| Q107 | Trusts tab view? | **Both outgoing + incoming vouches + trust scores** |
| Q108 | Recovery approval? | **browsy sends request → contact approves in their browsy** |
| Q109 | Heritage visibility? | **Full heritage chain visible (who vouched for whom, depth)** |
| Q110 | Key rotation? | **User-initiated rotation only** |
| Q111 | Rotation effect on vouches? | **Vouches remain valid (old key signatures still verify)** |
| Q112 | Recovery contact limits? | **Max 5, threshold of 2 (2-of-5 to approve recovery)** |
| Q113 | Heritage claim notification? | **Both browsy notification + email** |
| Q114 | Recovery threshold flexibility? | **Fixed at 2 (no flexibility)** |
| Q115 | Heritage claim delay? | **7-day grace period** |
| Q116 | Vouch revocation? | **Yes, anytime (removes trust factor from recipient)** |
| Q117 | Multi-device signing? | **Same key derived from same auth factors** |
| Q118 | Recovery contact requirement? | **Yes, must have browsy installed** |
| Q119 | Heritage claim verification? | **Signing key proves they're in the heritage list** |
| Q120 | First circle editing? | **Yes, anytime (all three tabs)** |
| Q121 | Heritage chain depth? | **Unlimited** |
| Q122 | Signing key export? | **Only as recovery code (not raw key)** |
| Q123 | Recovery code format? | **12-word mnemonic (like crypto wallets)** |
| Q124 | Recovery code usage? | **Only when all auth factors are lost** |
| Q125 | Heritage chain visibility depth? | **Full chain regardless of depth** |
| Q126 | Vouch signature format? | **{ from, to, timestamp, trustLevel, signature }** |
| Q127 | Trust level values? | **Determined by circle/group membership** |
| Q128 | Browsy first-run flow? | **Link Telegram first, then set up first circle** |
| Q129 | Circle hierarchy? | **Nested (circles within circles, like appy scores/stats)** |
| Q130 | First circle groups? | **Heritage, Recovery, Closest (3 groups)** |
| Q131 | MyNet = Trusts? | **Yes — Trusts replaces Circles terminology throughout** |
| Q132 | Close circle groups? | **Friends, Family, Colleagues (second circle of trusts)** |
| Q133 | Trust tiers? | **Closest → Close → Groups → Social (4 tiers)** |
| Q134 | Groups tier structure? | **Groups of affinity (private or public), 4th = Social (public)** |
| Q135 | Full trust tier model? | **Closest → Close → Groups → Social, each with sub-groups** |
| Q136 | Social tier purpose? | **All of the above (public profile + posts + activity)** |
| Q137 | Groups tier types? | **All (interest, project, geographic)** |
| Q138 | Trust tier visibility? | **Yes, tier is part of public profile** |
| Q139 | Trust tier naming? | **Closest → Close → Groups → Social** |
| Q140 | Trust tier transition? | **User manually moves them** |
| Q141 | Trust tier limits? | **No limits on any tier** |
| Q142 | Groups sub-structure? | **Fixed categories + nested groups** |
| Q143 | Groups sub-categories? | **Interest, Project, Geographic** |
| Q144 | Social tier content? | **Everything you've made public** |
| Q145 | Closest sub-groups? | **Heritage, Recovery, Closest (3 tabs)** |
| Q146 | Close sub-groups? | **Friends, MyFamily (app), Others** |
| Q147 | MyFamily connection? | **Pending — needs "push to trusts" + "Invite them" buttons** |
| Q148 | Close/Others group? | **All of the above (uncategorized, other apps, temporary)** |
| Q149 | Tier movement rules? | **Simple move. Heritage requires confirmation, recovery auto-processes** |
| Q150 | Browsy badge per tier? | **No badge changes (tier is internal to browsy)** |
| Q151 | Trust storage? | **browsy default. Trusts require publish consent. Heritage = mandatory public** |
| Q152 | Publish consent flow? | **Consent at trust time ("Allow B to publish your trust?")** |
| Q153 | Heritage public mandate? | **Both heritage membership + full chain published** |
| Q154 | Publish consent scope? | **Only the fact of trust (A trusts B)** |
| Q155 | Publish consent revocation? | **Yes, anytime** |
| Q156 | Publish vs heritage? | **Heritage = always visible + accountability; Trusts = consent-based + social** |
| Q157 | Publish notification? | **No notification, B sees it in their trusts list** |
| Q158 | Publish consent visibility? | **Yes, list in trusts settings** |
| Q159 | Recovery publish rules? | **Recovery contacts never get published (always private)** |
| Q160 | Publish model summary? | **Heritage = always published. Trusts = consent required. Recovery = never published** |
| Q161 | Groups tier publish? | **User chooses per group (public or private)** |
| Q162 | Social tier publish? | **Always public (by definition)** |
| Q163 | Publish consent UI? | **Trusts settings in browsy (one list)** |
| Q164 | Social tier discovery? | **Yes (public by definition)** |
| Q165 | Publish consent granularity? | **First tier (Close default). Groups = permission groups (3 max)** |
| Q166 | Publish to group limit? | **Up to3 groups. Close = default extra group** |
| Q167 | Permission group count? | **3 max** |
| Q168 | Permission group structure? | **List of people + publish rules** |
| Q169 | Permission group naming? | **Yes, custom names** |
| Q170 | Default permission groups? | **Close + Public + Private (3 defaults)** |
| Q171 | Permission group visibility? | **No (private to the group creator)** |
| Q172 | Permission group selection? | **Checkbox (select multiple, up to 3)** |
| Q173 | Permission group editing? | **Yes, but only the creator can edit** |
| Q174 | Permission group rules? | **User-defined labels** |
| Q175 | Permission group inheritance? | **No (each group is independent)** |
| Q176 | Permission group storage? | **browsy local. Public only if manually synced** |
| Q177 | Permission group deletion? | **All content becomes private** |
| Q178 | Permission group sync? | **Manual only. "Save in browsy local" + "Save and Publish"** |
| Q179 | Permission group conflict? | **Last sync wins** |
| Q180 | Publish to group flow? | **Select groups → browsy signs → Publish** |
| Q181 | Publish signature content? | **Full content + timestamp + sender key** |
| Q182 | Publish destination? | **browsy local + GitHub (users/) + Central** |
| Q183 | Publish feedback? | **Success toast ("Published to 2 groups")** |
| Q184 | Publish vs save? | **Save = local storage; Publish = local + GitHub + Central** |
| Q185 | Publish content types? | **All content types** |
| Q186 | Publish visibility? | **Everyone (public by default). Groups = share button subs** |
| Q187 | Close group rules? | **Hidden from everyone except the creator** |
| Q188 | Permission group visibility? | **Group members only see content marked "share with [group]"** |
| Q189 | No group selected? | **Private (only creator sees)** |
| Q190 | Full publish model? | **Save = local only. Publish = local + GitHub + Central. Group = share with. No group = private** |
| Q191 | Permission groups standard? | **Subs of Share button — new standard** |
| Q192 | Share button scope? | **Only in appy-normal (new standard starts here)** |
| Q193 | Share button placement? | **Global bottom bar + per-item actions** |

### Interoperability & Conflict Resolution (Q194–Q204)

| ID | Question | Decision |
|----|----------|----------|
| Q194 | Conflict UI (major)? | **Side-by-side diff** |
| Q195 | Clock skew handling? | **Accept risk (NTP usually suffices)** |
| Q196 | JSON merge strategy? | **Merge by field (preserve non-conflicting fields)** |
| Q197 | Nety ↔ Central authority? | **Nety is authoritative** |
| Q198 | Browsy ↔ Central conflict? | **Detect and resolve (show diff to user)** |
| Q199 | Offline queue? | **Local queue (IndexedDB), sync when back online** |
| Q200 | Decentral → Central push? | **Nety pushes all public data to Central** |
| Q201 | Recovery source authority? | **Nety authoritative; browsy = ask user** |
| Q202 | Conflict log storage? | **browsy local only (IndexedDB)** |
| Q203 | Schema migration sync? | **Server accepts any version, ignores missing fields** |
| Q204 | Device revocation? | **Re-vouch all trusts from another device** |

### Interoperability & Sync — Round 2 (Q205–Q224)

| ID | Question | Decision |
|----|----------|----------|
| Q205 | Sync protocol? | **Timestamps del cliente (simple, NTP suele basta)** |
| Q206 | Conflict detection granularity? | **Documento entero** |
| Q207 | Sync retry strategy? | **Exponential backoff (3 attempts)** |
| Q208 | Server validates schema on sync? | **Sí, rechaza si es inválido + log + notify user** |
| Q209 | Partial sync? | **Delta sync (only changed fields)** |
| Q210 | Real-time vs batched sync? | **Batched 5 min + real-time for trust changes** |
| Q211 | Conflict notification timing? | **En la próxima visita (badge en popup)** |
| Q212 | Max devices per account? | **5** |
| Q213 | Bandwidth limit per sync? | **No limit (delta sync lo mantiene pequeño)** |
| Q214 | Offline staleness threshold? | **7 días** |
| Q215 | Trust graph sync scope? | **Full graph (3 hops, ~1MB max)** |
| Q216 | Permission group sync mode? | **Semi-automático (auto-save local, push con botón)** |
| Q217 | Profile sync scope? | **Full profile on each sync** |
| Q218 | Undo conflict resolution? | **Sí, 30 días** |
| Q219 | Sync history retention? | **30 días, archive local** |
| Q220 | Device identification? | **Nombre del usuario + browser fingerprint** |
| Q221 | Sync status UI? | **Badge en popup (synced/syncing/error)** |
| Q222 | Sync error handling? | **Queue + notify user después de 3 intentos** |
| Q223 | Data compression? | **gzip en transmission, raw en storage** |
| Q224 | Encryption in transit? | **TLS + E2E para trust data** |

### Development Strategy — Browser Plugin First (Q225–Q244)

| ID | Question | Decision |
|----|----------|----------|
| Q225 | Browser plugin MVP scope? | **Auth + mynet + publish bridge (los 3 pilares)** |
| Q226 | Content sync priority? | **App data > mynet > auth (orden inverso)** |
| Q227 | Memory/CPU budget? | **50MB storage / 100MB memory / 1% CPU idle** |
| Q228 | Offline data strategy? | **IndexedDB local queue + sync when online** |
| Q229 | Local vs synced? | **Local: keys, drafts. Synced: profile, trust, app state** |
| Q230 | Public by default? | **No — private by default, user publishes explicitly** |
| Q231 | Target platforms first? | **Chrome + Firefox desktop, then mobile** |
| Q232 | Max extension size? | **<10MB (target 5MB)** |
| Q233 | Extension update strategy? | **Auto-update + changelog visible** |
| Q234 | Testing strategy? | **Unit + integration + manual** |
| Q235 | Required documentation? | **README + API docs + user guide** |
| Q236 | First-time user experience? | **Tour completo (5+ pasos con explicaciones)** |
| Q237 | Error reporting? | **Console + crash reports con consent** |
| Q238 | Metrics to track? | **Todo detallado, con opción "No trace"** |
| Q239 | Security audit timing? | **Después del MVP** |
| Q240 | Performance monitoring? | **Configurable en options, defaults recomendados** |
| Q241 | User feedback collection? | **GitHub issues + botón in-app + circle en users/ para sugerencias** |
| Q242 | Release cadence? | **No preestablecido — cuando hayan features** |
| Q243 | Backward compatibility? | **Últimas 2 versiones mayores** |
| Q244 | Open source strategy? | **Todo open source** |

### BF Questions 2026-07-24 (Browsy + FastAPI Convivence)

| ID | Question | Decision |
|----|----------|----------|
| BF02 | Trust data to Central? | **Full trust graph** |
| BF03 | Conflict resolution? | **Last-write-wins** |
| BF04 | Trust computation mode? | **Hybrid** (offline web of trust + optional Central enrichment) |
| BF11 | Webhook config storage? | **Both** (browsy local + Central synced copy) |
| BF12 | Webhook trigger? | **Manual only** |
| BF13 | Webhook auth? | **User-configurable** |
| BF14 | Central proxy webhooks? | **Both** (browsy direct OR via Central) |
| BF08 | JSON-LD generation? | **Browsy generates from local data** |
| BF09 | Auth with Nety bridge? | **Same OAuth as Nety** |
| BF10 | Nav interaction? | **Browsy replaces Central nav** (main navigation hub) |
| BF01 | Score sync to Central? | **Manual trigger** + Trustnet level visibility (L2 sees L2 content) |
| BF05 | Push notification trigger? | **New items in followed apps** |
| BF06 | API rate limits? | **Client-side throttling** |
| BF07 | Central down? | **Continue fully functional offline** |

### BL Questions 2026-07-24 (Browsy Limitations)

| ID | Question | Decision |
|----|----------|----------|
| BL01 | Storage budget? | **Dynamic allocation** |
| BL02 | Memory usage? | **Memory limits per feature** |
| BL03 | API rate limits? | **Client-side throttling + Batching + Cache-first** |
| BL04 | Offline capabilities? | **All features work offline** |
| BL05 | Cross-origin? | **Active tab access** |
| BL06 | Update mechanisms? | **Manual update** (auto-update later) |
| BL07 | Conflict resolution? | **Peer-to-peer sync** |
| BL08 | Privacy concerns? | **Encryption at rest** |
| BL09 | Feature scope? | **Plugin system + Multiple extensions** |
| BL10 | Performance? | **Preload essentials + Lazy load rest + Background processing** |
| BL11 | Browser compatibility? | **Progressive enhancement** |

### BD Questions 2026-07-24 (Browsy Decisions)

| ID | Question | Decision |
|----|----------|----------|
| BD01 | Content extraction? | **Performance-optimal** |
| BD02 | Badge display? | **Floating badge (menu item later)** |
| BD03 | Plugin loading? | **Cache after first load** |
| BD04 | State management? | **Performance-optimal** |
| BD05 | Memory management? | **Global limit** |
| BD06 | Context menu? | **Native browser (defer)** |
| BD07 | Quick panel? | **Not needed** |
| BD08 | Notifications? | **Both (notifications + badge)** |
| BD10 | Notification triggers? | **All (items, trust, mentions)** |
| BD11 | Cache strategy? | **Version-based** |
| BD12 | Security? | **All (minimal + CSP + sandboxed)** |
| BD13 | Updates? | **Manual update** |
| BD14 | Error handling? | **User notification** |
| BD15 | Privacy? | **All (local + encrypted)** |
| BD16 | Authentication flow? | **All (ID + badges + account)** |
| BD17 | Data levels? | **All data (adds metadata ID)** |
| BD18 | Compatibility? | **Progressive enhancement** |
| BD19 | Performance? | **All (lazy + cache + background)** |
| BD20 | Accessibility? | **All (ARIA + keyboard + high contrast)** |
| BD21 | i18n? | **Flove standards + user-configurable** |
| BD22 | Theming? | **Flove theme standards (§13.14)** |
| BD23 | Customization? | **Settings page (extension options)** |
| BD24 | Integration? | **All (storage + messaging + API)** |
| BD25 | API exposure? | **Both (flove + custom)** |
| BD26 | Lifecycle? | **Browser-managed (automatic)** |
| BD27 | Testing? | **All (unit + integration + manual)** |
| BD28 | Logging? | **Console only (browser devtools)** |
| BD29 | Analytics? | **Full analytics (with user consent)** |

**Key architecture:** 
- Browsy = main navigation app
- **Links flove.org apps with web of trust**
- Reardy is a POC for browsy
- Some scores only visible for browsy users within web of trust (permissions set there)
- Gets HTML from Central (or solo fallback backup)
- Updates via central/shared (JS and CSS)
- Lightweight, considering browser consumption and persistence
- Trust acceptances need visibility parameter: first circle, second circle, social groups, public
- **Publishes to GitHub/webhooks, keeps copy of recent ones locally**
- **Auth:** Browsy authenticates with Telegram, OAuth accounts on top of them
- **Strategy:** Light browsy distro + Central backend + full fallback distro
- **Slogan:** Authenticity and web of trust for flove apps
- **Signing:** Composite key derived from auth layers (deterministic, recoverable)
- **Heritage chain:** Trust vouches create responsible chains (vouch = signed statement + key gain)
- **Recovery:** Re-link factors + recovery code at setup (like nety masks)

### Composite Identity Model (Q93a–Q93g)

Browsy's identity is layered — each factor adds weight to the signing key:

```
Layer 0: Device (base, always present)
Layer 1: Telegram (verified)     ← personal auth
Layer 2: Email (certified)       ← personal auth  
Layer 3: Trust vouches           ← web of trust
```

- **Signing key:** Deterministic, derived from auth factors (same inputs = same key, recoverable)
- **Factor count:** Visible to receivers ("3-factor signed")
- **Bonuses:** More factors = navigation bonuses + feature access + visibility weight
- **Recovery:** Re-link Telegram + email → key regenerated; recovery code saved at setup
- **Vouch:** Signed statement "A trusts B" → B's key gains trust factor + stored in browsy + Central
- **First circle:** Trusts/heritage and trusts/recovery are actions within browsy config, part of first circle
- **Rotation:** User-initiated only, vouches remain valid (old key signatures still verify)

### First Circle Model (Q101–Q112)

The first circle is browsy's default trust group with three tabs:

**Trusts tab:**
- Mutual view: outgoing + incoming vouches + trust scores
- Vouch chain depth: 3 hops (matches nety's trust graph)
- Vouch = signed statement → key gains trust factor

**Recovery tab:**
- Max 5 contacts, threshold of 2 (2-of-5 to approve recovery)
- browsy sends request → contact approves in their browsy
- Empty by default, user adds manually

**Heritage tab:**
- Accountability partners + inherit trust chain if gone
- Public by default, full chain visible (who vouched for whom, depth)
- Heritage can claim account after 1 year idle
- Approval required to join
- Empty by default, user adds manually

### Trust Tier Model (Q129–Q165)

Browsy organizes connections in 4 nested tiers:

```
Closest → Close → Groups → Social
```

**Closest (first circle):** Heritage, Recovery, Closest (3 tabs)
- Heritage: accountability partners, mandatory public, claim after 1 year idle
- Recovery: max 5 contacts, 2-of-5 threshold, never published
- Closest: closest connections, publish consent required

**Close (second circle):** Friends, MyFamily (app), Others
- Friends: personal friends
- MyFamily: integrated with flove MyFamily app (pending: "push to trusts" + "Invite them" buttons)
- Others: uncategorized close contacts

**Groups (third circle):** Interest, Project, Geographic
- User-defined groups (3 max permission groups)
- Nested groups within categories
- Private or public per group

**Social (fourth circle):** Everything public
- Always public by definition
- Public profile + posts + activity

### Permission Groups & Share Button (Q166–Q193)

Permission groups control content visibility via the Share button:

**Defaults:** Close, Public, Private (3 pre-defined)
**Custom:** Up to 3 user-created groups (independent, no inheritance)

**Share button flow:**
1. User clicks Share → selects groups (checkbox, up to3)
2. browsy signs content (full content + timestamp + sender key)
3. Save = local storage only. Publish = local + GitHub (users/) + Central
4. "Save in browsy local" + "Save and Publish" buttons
5. Success toast ("Published to 2 groups")

**Visibility rules:**
- No group selected = private (only creator sees)
- Group selected = "share with group" (group members only)
- Heritage = always published (mandatory)
- Trusts = publish consent required (at trust time)
- Recovery = never published (always private)
- Social = always public

**Publish consent:**
- Consent at trust time ("Allow B to publish your trust?")
- Scope: only the fact of trust (A trusts B)
- Revocable anytime
- Visible in trusts settings (one list)

```
┌─────────────────────────────────────────────────────────────┐
│                    BROWSY (Local Navigation)                 │
│  - Improves local navigation with Central HTTP navigation   │
│  - Local web of trust calling                               │
│  - Extended profile display                                 │
│  - Private mode browse                                      │
│  - Fallback of default browsy                               │
│  - Downloads from another repo, displays info minimally     │
│  - No external calls — self-contained after download        │
├─────────────────────────────────────────────────────────────┤
│  ↓ calls                                                     │
│  CENTRAL (Full Content Pack)                                 │
│  - HTTP navigation                                          │
│  - Offline mode pack                                        │
│  - Core features                                            │
├─────────────────────────────────────────────────────────────┤
│  ↓ fallback to                                               │
│  FLOVE FULL BROWSY DISTRO (optional)                         │
│  Full content, all features, offline capability              │
└─────────────────────────────────────────────────────────────┘
```

**Strategy:**
1. **Local navigation enhancer** — Browsy improves navigation with trust data
2. **Private mode browse** — Operates in private/incognito mode
3. **Fallback** — Serves as backup when primary fails
4. **Trust caller** — Uses local web of trust to enrich navigation
5. **Downloads from repo** — Content from Central/other repos
6. **Minimal display** — Shows info without external calls
7. **Central full pack** — Complete content for offline mode

### Web of Trust Persistence Budget

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Hop depth** | 3 hops | Full network (~1MB) |
| **Max users** | 100 | ~20KB storage |
| **Compression** | JSON | ~70% reduction with gzip |
| **Eviction** | LRU | Least recently used |

**Storage breakdown:**
- Profile: ~1KB/user × 100 = ~100KB
- Trust scores: ~100B/user × 100 = ~10KB
- Vouch entries: ~200B × connections = ~20KB
- 3-hop web: ~1MB total
- **Total budget: ~1.2MB** (fits in 10MB Extension storage quota)

### Trust Sync Protocol

Trust syncs separately from profile/app data via `POST /api/trust/sync`.

**Payload (browsy → Central):**
```json
{
  "user": "device-uuid-or-email",
  "vouches": [
    {
      "from": "user-a-key",
      "to": "user-b-key",
      "timestamp": "2026-07-25T10:00:00Z",
      "trustLevel": "close",
      "signature": "ed25519-signature",
      "vectorClock": {"user-a": 5, "user-b": 3}
    }
  ],
  "lastSync": "2026-07-25T09:55:00Z"
}
```

**Response (Central → browsy):**
```json
{
  "ok": true,
  "merged": 2,
  "conflicts": [
    {
      "vouch": {"from": "user-a", "to": "user-c"},
      "serverVersion": {"trustLevel": "close", "vectorClock": {"user-a": 4}},
      "clientVersion": {"trustLevel": "groups", "vectorClock": {"user-a": 5}}
    }
  ]
}
```

**Conflict resolution:**
- Vector clocks determine causality (client A's vouch supersedes server if A's clock > server's clock for that user)
- If clocks are concurrent (neither dominates): server returns both versions in `conflicts[]`
- Browsy shows conflict to user for manual resolution
- Merged vouches stored permanently (D01: no TTL for trust data)

**Timing:**
- Trust changes push immediately (real-time, Q210)
- Profile/app data batches on idle (chrome.alarms, no arbitrary timer)
- Delta-only: only changed vouches since `lastSync` are sent

**1MB limit handling:**
- Trust sync is delta-only, typically <10KB per sync
- Full 3-hop graph rebuilds happen client-side in browsy (Extension storage)
- If delta exceeds 1MB (extremely rare): paginate into multiple POSTs

### Nety-derived patterns for browsy

Browsy inherits these patterns from nety's codebase:

| Pattern | Nety source | Browsy use |
|---------|-------------|------------|
| **Ed25519 + keystore** | nety F4 | Composite signing key (device + Telegram + email + trust) |
| **Trust graph (2nd-order transitivity)** | nety F7 | Heritage chain + vouch verification |
| **CRDT reputation** | nety F6 | Trust accumulation across auth layers |
| **ChaCha20 encryption** | nety stack | Local DM + state encryption |
| **Recovery code** | nety-frontend §C03 | Key recovery: re-link factors + recovery code at setup |
| **Mask creation flow** | nety-frontend | Auth setup: guided onboarding with recovery code generation |

## Latest decisions (2026-07-27)

> Source: browsy PLANS.md + TESTING.md. Architecture rule: browsy = backend only, central = all frontends. On-demand only — no background calculations, no auto-sync.

### Architecture decisions

| Topic | Decision |
|-------|----------|
| Calculations | On-demand only (click) — lightest for browsy |
| Crypto | Web Crypto primary + tweetnacl fallback |
| Key generation | Background service worker |
| Vouches expected | 20–100 per user |
| Trust chain | On demand, < 2s for 100 vouches |
| Vouch revocation | Recalculate in bundled daily session |
| Settings sync | Unidirectional: browsy → central |
| Conflict resolution | Browsy wins |
| chrome.storage.sync | Yes for settings (multi-device) |
| Web Workers | Yes, if crypto exceeds 30s SW lifetime |
| Cache in central | Yes — central caches bridge responses |
| Bridge response target | < 100ms |
| Testing | Both installed + not-installed |
| Browsers | Chrome, Firefox, Safari |
| Mock bridge | Yes, for automated tests |
| Profile data | Identity + settings |
| browsy-trust data | MyNet + vouches + chain + facets |

### Data structures

**Vouch:** `{ id, from, to, score, facets: {personal, local, social, global}, message, created, revoked }`
**Profile:** `{ pubkey, displayName, avatar, settings: {theme, language, sound, soundLevel, notifications, wizy}, created, lastSync }`
**Trust:** `{ score, facets: {personal, local, social, global}, mynet: {categories, circles}, vouchCount, lastCalculated }`

### Implementation priorities

| Priority | Features | Files |
|----------|----------|-------|
| P1: Bridge work | Keypair, profile, trust APIs | content.js, background.js |
| P2: Settings sync | chrome.storage mirror, dual persistence | background.js, flove-settings.js |
| P3: On-demand crypto | Key gen in SW, trust chain in Worker | background.js, lib/worker.js |
| P4: Reliability | 100ms timeout, retry, re-bridge | content.js, background.js |
| P5: Testing | test.html, mock bridge, benchmarks | test.html, mock-bridge.js |

### Storage budget (100 vouches)

| Item | Size | % of 5MB |
|------|------|----------|
| Vouches | ~40 KB | 0.8% |
| Keys + trust + profile + settings | ~3 KB | 0.06% |
| **Total** | **~43 KB** | **0.86%** |

Safe up to ~500 vouches. Monitor at 200+.

### Crypto comparison

| Factor | tweetnacl | Web Crypto Ed25519 |
|--------|-----------|-------------------|
| Support | All (polyfill) | Chrome 113+ only |
| Size | ~20KB | 0 (built-in) |
| Async | No (blocks thread) | Yes |
| Future-proof | Risk (unmaintained) | Yes (standard) |

**Decision:** Web Crypto primary, tweetnacl fallback for older browsers.

### Bridge API targets

```
getKeypair(cb)    → < 100ms
getProfile(cb)    → < 100ms
getScore(cb)      → < 100ms
getFacets(cb)     → < 100ms
getVouches(cb)    → < 100ms
onUpdate(fn)      → immediate
```

### Performance risks mitigated

| Risk | Mitigation |
|------|------------|
| SW killed after 30s | On-demand only, ops < 500ms |
| 5MB storage limit | 43KB at 100 vouches |
| Content script timing | Central waits, fallback to cache |
| Crypto on main thread | Offload to SW + Web Worker |

## Open questions

BF01, BF05-BF07 pending.

## Cross-plan dependencies

- **central-backend.md** — Extension syncs with Central via push notifications + libSQL
- **shared-code.md** — Reuses routing.json, flove-i18n.js
- **standards.md** — Follows flove offline-first philosophy
- **nety-frontend.md** — Extension provides core trust features (local score, web of trust) + profile data syncs with nety (connections, activity scores)
- **nety-trust.md** — Trust computation in Browser Extension + Central
