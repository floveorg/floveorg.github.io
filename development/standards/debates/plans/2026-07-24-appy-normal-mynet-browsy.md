# appy-normal.html — MyNet Browsy + Wizy Mini

> **Status:** plan (2026-07-24). Derived from browsy/appy survey Q1–Q101.
> **Decisions:** see §14 for full decision log.
> **Goal:** New single-file HTML app at the normal tier (500⭐) that houses MyNet
> social features and wizy mini (agents preview), with all features activated and
> managed through the browsy browser extension. First Central + browsy demo app.
> MyNet is delivered by browsy — appy-normal is the frontend shell.

## 1. Context: the revised tier model + Central role

Post-survey, the appy diagonal is:

| Tier | Threshold | Headline | Identity |
|------|-----------|----------|----------|
| mini | 0⭐ | profily | You appear |
| basic | 100⭐ | social | You belong |
| **normal** | **500⭐** | **MyNet browsy + wizy mini** | **You connect + preview agents** |
| advanced | 2000⭐ | vizy + sety pro + full wizy + full blogy | You visualise + control data |
| super | 10000⭐ | governance + group chat + XR/VR | You host + govern |

Normal's identity: the user's social mesh lives here (MyNet browsy), and they
get their first taste of agents (wizy mini — summaries + suggestions, on/off only).

### Central = Solo evolved

Central is not a content platform — it's **Solo with persistence**. Same apps, hosted
on flove.org, Turso persistence, optimized code. Central is **read-only** for content:
- Stores profile (public) + published items (what browsy makes public)
- Enriches browsy navigation with trust data
- All content creation lives in browsy/appy → browsy decides what to publish
- User-owned repos (`users/` default) receive export JSON, not Central

### Publishing model

```
appy apps → export JSON on profile → synced to user-chosen repo (editable/forkable)
Central ← read-only mirror of profile + public items (browsy pushes)
```

## 2. File structure

Single self-contained HTML file: `apps/appy/appy-normal.html`

Follows the exact pattern of `appy-mini.html` / `appy-basic.html`:
- Same CSS tokens (`--bg`, `--ink`, `--accent`, `--signal`, etc.)
- Same mesh background, glass cards
- Same `flove:lang` i18n engine (`.en`/`.es` spans, `bx()` helper)
- Same Account panel (language selector + wizy toggles + rainbow roadmap)
- **Bottom nav bar** (48px fixed, injected by flove.js) — replaces top tab bar
- No build step, no framework, no bundler (AGENTS.md §4)

### Bottom nav layout (Q52b, Q58a, Q82c)

```
┌─────────────────────────────────────────────────────┐
│  [☰ Menu]  [◉ Net ▾]  Profile  MyNet  Chat  Act  ⚙ │  ← 48px fixed bottom bar
└─────────────────────────────────────────────────────┘
```

- **Menu (logo/site title)** — opens full-screen menu overlay (chapters → apps)
- **Net icon** — collapsed dropdown with tab shortcuts (Profile, MyNet, Chat, Activity, Settings)
- **Individual tabs** — direct access to each section
- Injected by flove.js (shared nav layer, same as Central apps)

## 3. What normal unlocks (vs basic)

Basic has: profily, apps, social groups, publish queue, invites.
Normal adds:

### 3a. MyNet browsy (social, managed by browsy)
- **Live social feed** — posts from followed people, bookmarks, and circle content (Q31c)
- **Circle management** — create/name circles, assign people, no member limits (Q29a)
  - Visibility: **Private / Close (friends) / Related (share groups) / Public** (Q37c)
- **DMs only** — no group chat at normal (Q41: group chat → super)
  - Text + reactions + read receipts + editing, unlimited edit window (Q45d, Q47a)
  - Custom reactions: pick from full emoji grid, user-defined set (Q48d, Q49a)
  - Ephemeral mode: retention follows ephemeral setting (Q33c)
- **Notifications** — mentions, trust events, circle invites, new followers, agent activity (Q23d)
  - Manual dismiss, stays until closed (Q25b)
- **Publish to Nety P2P** — signed Flove post format, verified client-side (Q5a, Q34c, Q36a)
  - Publish option in the publish form (Q5a)

### 3b. Wizy mini (agents preview)
- **Two agents:** Summaries + Suggestions — on/off only (Q16b)
- Data sources: followed posts + bookmarks + circle content (Q31c)
- Summaries: auto-generates summaries of accessible content
- Suggests: suggests people/groups to follow based on activity
- Controls live in **Account panel** below language (Q35b)
- No sliders, no configuration — on/off toggle per agent

### 3c. Authentication (managed by browsy)
- Login via browsy popup (Q59b, Q62d) — minimal for returning, full for first-time
- Browsy auto-links Central on first detection if already authenticated (Q84c)
- Auth requires **email + Telegram** for repo sync; export JSON is free (Q90d)
- Session persisted in browsy, appy-normal reads from `window.flove.central` (Q85b)

### 3d. Blogy publishing (split across tiers)
- Normal: publish text posts to queue (moderated, blogy-style flow) (Q63a)
- Advanced: full blogy features (drafts, scheduling, rich editor, SEO, RSS)
- Posts go to user-chosen repo (not Central), Central is read-only (Q61 context)

## 4. Browsy integration architecture

### 4a. How browsy activates features

Browsy is the **control plane**. appy-normal renders the UI but browsy decides
what's enabled:

```
┌──────────────────────────────────────────────┐
│  BROWSY (extension)                          │
│  - Feature flags (which tabs/panels active)  │
│  - Authentication (session/token)            │
│  - Central sync (last snapshot embedded)     │
│  - Notification triggers                     │
│  - P2P publish targets                       │
│  - Settings (theme, language, permissions)   │
├──────────────────────────────────────────────┤
│  ↓ postMessage bridge (floave-bridge.js)     │
├──────────────────────────────────────────────┤
│  APPY-NORMAL (flove page)                    │
│  - Renders UI based on browsy feature flags  │
│  - Reads auth state from browsy              │
│  - Sends actions through bridge              │
│  - Falls back to local-only if no browsy     │
└──────────────────────────────────────────────┘
```

### 4b. Bridge API (browsy → appy-normal)

Via `window.postMessage` (per BX02):

| Event (browsy → app) | Payload | Effect |
|---|---|---|
| `browsy:features` | `{ mynet: true, wizyMini: true, ... }` | Enable/disable tabs and panels |
| `browsy:auth` | `{ user: {...}, token: '...' }` | Set auth state, show profile |
| `browsy:central` | `{ version, snapshot }` | Load Central data (feed, circles, etc.) |
| `browsy:notification` | `{ type, data }` | Show overlay notification (Q21c) |
| `browsy:p2p:published` | `{ id, target }` | Confirm P2P publish |

| Event (app → browsy) | Payload | Effect |
|---|---|---|
| `appy:requestFeatures` | `{}` | Browsy responds with feature flags |
| `appy:publish` | `{ content, target: 'nety-p2p' }` | Publish to Nety P2P (Q5a) |
| `appy:chat` | `{ to, message, ephemeral }` | Send DM via browsy bridge |
| `appy:circle` | `{ action, circleId, data }` | Manage circles |

### 4c. Fallback (no browsy installed)

When browsy is not detected, appy-normal shows:
- A notice: "Install browsy to activate MyNet features"
- The profile/account tabs still work (local-only)
- MyNet and wizy tabs are dimmed with upgrade-style affordance
- Same pattern as appy-mini's "demo-notice" for basic features

## 5. Tab structure

Bottom nav: Profile | MyNet | Chat | Activity | Settings

### MyNet tab — sub-tabs (Q100b)
```
MyNet
├── Feed         (live posts from followed people, bookmarks, circle content)
├── Circles      (Private / Close / Related / Public management)
└── Notifications (mentions, trust events, invites, agent activity)
```

### Chat tab
- **DMs only** (Q43a) — one-on-one conversations
- Text + reactions (custom emoji set) + read receipts + unlimited editing (Q45d, Q47a, Q48d)
- Ephemeral mode toggle (retention follows setting, Q33c)
- Group chat: **not at normal** — moved to super (Q41)

### Settings tab
- **Update alerts** at the top (badge count from browsy, tap → flove.org release notes, Q13d)
- Browsy permissions (what browsy can access)
- Notification preferences

### Account panel (wizy controls here)
- Language selector (first item)
- **Wizy mini toggles** — Summaries on/off, Suggestions on/off (Q35b)
- Rainbow roadmap cards

## 6. Central integration

### Central = read-only data bank
- flove.js pings `/api/ping` → gets `{ok: true, version, apps: [...]}` (Q89b)
- Central stores profile (public) + published items (browsy pushes)
- All writes go through browsy → Central, not from app directly
- Central is always backwards-compatible, no version handshake needed (Q101d)

### Central sync (on save/share/export actions, Q86b)
- Sync triggers at action points (not on page load)
- Auto-sync: batched, one request per load (Q72c), full state dump (Q74a)
- Manual Sync button in bottom nav (CB11)
- Error handling: specific server message + "Retry" (CB22)
- Service worker caches Central apps, detects new versions, prompts reload (Q94a)

### Central app serving
- Apps served as static HTML from `flove.org/apps/` (D20)
- Same app experience as Solo but with persistence via Turso
- flove.js injects bottom nav + sync + shared CSS (D16, E24)
- URL-based routing: `flove.org/apps/appy-normal.html` → Central version (Q78a)

### Identity on Central
- Anonymous by default (device UUID)
- Browsy auto-links auth on first Central detection (Q84c)
- Claim flow: browsy handles Telegram + email linking (Q92d)
- Email marked as "certified" in metadata export (Q88 context)

## 7. State model

Extends the existing `state` object from appy-basic:

```js
const state = {
  // ... inherited from appy-basic via appyTransfer ...
  nav: 'normal',                    // current nav tier
  // MyNet
  feed: [],                         // posts from Central/browsy (followed + bookmarks + circles)
  circles: [],                      // { id, name, people: [], visibility: 'private'|'close'|'related'|'public' }
  notifications: [],                // { type, data, read, timestamp }
  unreadCount: 0,
  // Chat (DMs only — group chat is super)
  conversations: [],                // { id, peer, messages: [], ephemeral, lastEdit }
  activeConversation: null,
  // Wizy mini (toggled in Account panel)
  agents: {
    summaries: false,               // on/off only
    suggestions: false,             // on/off only
  },
  // Custom reactions (user-defined set, picked from emoji grid)
  reactions: [],                    // ['🔥', '❤️', ...] — user's reaction set
  // Export / repo sync
  repoUrl: null,                    // user-chosen repo URL (default: users/ repo)
  repoBranch: 'main',
  lastExport: null,                 // timestamp of last export
  // Central state
  centralAvailable: false,          // from flove.js ping
  centralVersion: null,
  // Browsy bridge state
  browsyConnected: false,
  browsyFeatures: {},
  auth: null,                       // { user, token } from browsy
};
```

## 8. Upgrade path

### From basic → normal
- When user reaches 500⭐ in appy-basic, show upgrade banner
- `location.href = 'appy-normal.html'` with `appyTransfer` carrying state
- First-run loud entrance: "Welcome to normal — MyNet is now live"
- Account panel shows "reached ✓" on normal-tier rainbow cards

### From normal → advanced
- When user reaches 2000⭐, show upgrade banner to advanced
- Advanced unlocks vizy lite + sety pro + full wizy (Q22d, Q18b)

## 9. Export + repo architecture

### Export JSON
- Updated on every state change (real-time, Q73a)
- Debounce + throttle + Web Worker (Q79d) for performance
- Downloads as file to user's device (Q93a)
- Shape: `{profile, items: [{app, type, data, timestamp}], meta: {identity: {email: "masked", telegram: "verified"}, certified: true}}`

### Repo sync (users/ repo)
- Default repo: `users/` — one file per user: `users/{uuid}.json` or `{email}.json` (Q76a)
- Marc's file: seed/example data (Q77b)
- User can repoint to any GitHub/Gitea repo (Q88c)
- Auth required: email + Telegram for repo sync; export is free (Q90d)
- browsy pushes via GitHub/Gitea API (Q67, Q88c)
- Git history as versioning — each commit = one state snapshot (Q75d)

### Export JSON structure
```json
{
  "profile": { "username": "...", "displayName": "...", "avatar": "..." },
  "items": [
    { "app": "blogy", "type": "post", "data": {...}, "timestamp": "..." },
    { "app": "souls", "type": "rating", "data": {...}, "timestamp": "..." }
  ],
  "meta": {
    "identity": { "email": "masked@email.com", "telegram": "verified" },
    "certified": true,
    "exportedAt": "..."
  }
}
```

## 10. Cross-plan dependencies

- **browser-extension.md** — browsy provides the bridge, feature flags, auth, Central sync
- **central-backend.md** — Central is read-only data bank, /api/ping, /api/nety/sync
- **nety-frontend.md** — MyNet social features share patterns with nety
- **nety-trust.md** — Trust events feed into notifications
- **shared-code.md** — Reuses routing.json, flove-i18n.js, enrichment loader

## 11. Browsy overlay integration (Q20c, Q30b)

When browsy is active and the user is on any flove.org page:

All overlays live in a **single collapsible sidebar panel** (Q30b).
- Starts collapsed on every page load (Q32a), auto-expands if unread content (Q97d)
- Contains: DM access, feed snippet, notification alerts (Q23d)
- Injected by browsy's content scripts into the page layout (Q27c: in the menu area)

Overlay content:
- **DM access** — tap to open conversation
- **Feed snippet** — recent posts from circles
- **Notification alerts** — mentions, trust events, agent activity (Q23d)
- Manual dismiss for notifications (Q25b)

## 12. Implementation tasks

### Task 1: Scaffold appy-normal.html from appy-basic.html
- Copy appy-basic.html as starting point
- Rename all references (title, description, meta)
- Update FEATURE_TIERS to reflect the revised tier model
- Add `nav: 'normal'` to state
- Static check + visual verify + commit

### Task 1b: First circle UI (Trusts | Recovery | Heritage tabs)
- Three tabs: Trusts (mutual view, outgoing + incoming vouches, trust scores)
- Recovery: max 5 contacts, 2-of-5 threshold, approval required (browsy request → contact approves)
- Heritage: public by default, full chain visible, claim after 1 year idle, approval required
- Empty by default, user adds manually
- Static check + visual verify + commit

### Task 2: Tab bar — add MyNet, Settings tabs (remove Wizy tab)
- Add tab buttons: MyNet, Settings (Chat stays, Wizy removed — controls in Account)
- Add tab panels: `#panel-mynet`, `#panel-settings`
- Wire `switchTab()` for new tabs
- Static check + visual verify + commit

### Task 3: MyNet tab — live social feed
- Render feed from `state.feed` (populated by browsy bridge)
- Post cards with author, content, timestamp, engagement buttons
- Full-text search: text + author + tags + URLs, trust-weighted ranking (Q38d, Q42d)
- If no browsy: show demo feed with sample data + "Install browsy for live feed"
- Static check + visual verify + commit

### Task 4: MyNet tab — circle management (Private / Close / Related / Public)
- Circle list with create/rename/delete, no member limits (Q29a)
- Assign people to circles
- Visibility selector: Private / Close (friends) / Related (share groups) / Public
- Static check + visual verify + commit

### Task 5: MyNet tab — notifications
- Notification list with badge count
- Types: mentions, trust events, circle invites, followers, agent activity (Q23d)
- Manual dismiss, stays until closed (Q25b)
- Mark all as read
- Static check + visual verify + commit

### Task 6: Chat tab — DMs only (no group chat)
- Port chat UI from appy-mini
- Wire to browsy bridge for real messaging
- Text + custom reactions (Q48d, Q49a) + read receipts + unlimited editing (Q45d, Q47a)
- Ephemeral mode toggle (Q33c)
- Static check + visual verify + commit

### Task 7: Custom reactions setup
- Emoji grid picker for user to define their reaction set
- Store in `state.reactions`
- Render in DM message actions
- Static check + visual verify + commit

### Task 8: Account panel — wizy mini toggles
- Add Summaries + Suggestions on/off toggles in Account panel (Q35b)
- Below language selector, above rainbow roadmap
- Store in `state.agents`
- Static check + visual verify + commit

### Task 9: Browsy bridge integration
- Listen for `browsy:*` postMessage events
- Send `appy:requestFeatures` on load
- Update state from `browsy:features`, `browsy:auth`, `browsy:central`
- Fallback notice when browsy not detected
- Static check + visual verify + commit

### Task 10: Settings tab — update alerts + permissions
- Update alerts at top (badge count from browsy, tap → flove.org release notes)
- Browsy permissions panel
- Notification preferences
- Static check + visual verify + commit

### Task 11: P2P publish option
- Add "Publish to Nety P2P" in the publish form (MyNet tab)
- Signed Flove post format (Q34c), client-side verification (Q36a)
- Wire to browsy bridge `appy:publish` event
- Static check + visual verify + commit

### Task 12: Upgrade flow — basic → normal
- In appy-basic: show upgrade banner at 500⭐
- `appyTransfer` state carry
- First-run loud entrance in appy-normal
- Rainbow roadmap "reached ✓" on normal cards
- Static check + visual verify + commit

### Task 13: Overlay injection hooks
- Expose overlay mount points for browsy content scripts
- Single collapsible sidebar: DM access + feed snippet + notifications (Q30b)
- Starts collapsed on every load (Q32a)
- CSS for overlay positioning (Q27c: in the menu area)
- Static check + visual verify + commit

## 13. Open questions (deferred)

- Exact notification sound/haptic feedback
- Agent data processing details (how summaries/suggestions compute from content)
- Offline feed cache size for appy-normal
- DM message search (is DM content included in full-text search?)
- Reaction limit per message

## 14. Decision log (Q29–Q101)

| Q | Topic | Decision |
|---|-------|----------|
| Q29 | Circle member limits | **No limits** — unlimited members per circle |
| Q30 | Overlay layout | **Single collapsible sidebar panel** |
| Q31 | Agent data sources | **Followed posts + bookmarks + circle content** |
| Q32 | Sidebar collapse | **Starts collapsed every time** |
| Q33 | Chat retention | **Follows ephemeral setting** |
| Q34 | P2P publish format | **Signed Flove post format** |
| Q35 | Agent toggle location | **Account panel** below language |
| Q36 | Signature verification | **Client-side only** |
| Q37 | Circle visibility | **Private / Close (friends) / Related (share groups) / Public** |
| Q38 | Search index scope | **Full-text: text + author + tags + URLs** |
| Q39 | Close vs Related | **Close = friends; Related = people you share groups with** |
| Q40 | Search content in index | (covered by Q38) |
| Q41 | Group chat tier | **Moved to super** (not at normal) |
| Q42 | Search ranking | **Trust-weighted** |
| Q43 | Chat at normal | **DMs only** |
| Q44 | Trust score source | **Local + Central enrichment (Central optional)** |
| Q45 | DM features | **Text + reactions + read receipts + editing** |
| Q46 | Central enrichment privacy | **Anonymous pull, no identification sent** |
| Q47 | Edit window | **Unlimited** |
| Q48 | Reactions format | **Custom user-defined set** |
| Q49 | Reactions setup | **Pick from full emoji grid** |
| Q50 | Scope confirmation | **Confirmed** |
| Q51 | Tier model | **Revised:** mini=profily, basic=social, normal=MyNet+browsy+wizy mini, advanced=vizy+sety+full wizy, super=governance+group chat+XR |
| Q52 | Central role | **Central = Solo evolved** (hosted on flove.org, Turso, read-only for apps) |
| Q53 | Central auth | **Anonymous default**, browsy links auth on first Central detection |
| Q54 | Publishing model | **appy apps → export JSON → sync to chosen repo**, Central receives read-only mirror |
| Q55 | Export JSON | **Real-time on state change**, downloads as file, no auth needed |
| Q56 | Repo sync auth | **Email + Telegram required** for repo sync |
| Q57 | Bottom nav | **48px fixed bottom**, 5 items: Menu (logo), Net icon (collapsed), Profile, MyNet, Chat, Activity, Settings |
| Q58 | MyNet sub-tabs | **Feed | Circles | Notifications** |
| Q59 | Circle visibility | **Private / Close / Related / Public** — no member limits |
| Q60 | Chat at normal | **DMs only**, group chat is super |
| Q61 | DM features | **Text + reactions + read receipts + editing + ephemeral** |
| Q62 | Custom reactions | **Emoji grid picker**, user-defined set |
| Q63 | Wizy mini | **Summaries + Suggestions on/off only**, toggles in Account panel |
| Q64 | Browsy overlay | **Single collapsible sidebar**, DM + feed snippet + notifications |
| Q65 | Overlay start | **Collapsed always**, auto-expands if unread |
| Q66 | Central sync | **On save/share/export actions**, batched one request per load |
| Q67 | Offline fallback | **browsy embeds last Central snapshot**, redirects online to flove.org |
| Q68 | P2P publish | **In app's share/export menu**, signed Flove post format |
| Q69 | Extension targets | **Chrome + Firefox** (Manifest V3 + V2 polyfill) |
| Q70 | Content extraction | **Removed** — not in browsy |
| Q71 | Search | **Full-text indexed**, trust-weighted ranking, Central enrichment optional |
| Q72 | Settings state | **localStorage primary** with libSQL fallback |
| Q73 | Central update | **Service worker prompts reload** |
| Q74 | Bottom nav items | **Menu, Net, Profile, MyNet, Chat, Activity, Settings** |
| Q75 | MyNet feed | **Followed posts + bookmarks + circle content** |
| Q76 | Notifications | **Mentions, trust events, circle invites, followers, agent activity** |
| Q77 | DM actions | **Text + reactions + read receipts + unlimited editing + ephemeral** |
| Q78 | Circle actions | **Create/rename/delete, assign people, visibility** |
| Q79 | Repo default | **users/ directory**, one file per user |
| Q80 | Marc's file | **Seed/example data** |
| Q81 | Repo repoint | **User can repoint to any GitHub/Gitea repo** |
| Q82 | Repo push | **browsy pushes via GitHub/Gitea API** |
| Q83 | Git versioning | **Each commit = one state snapshot** |
| Q84 | Export debouncing | **Debounce + throttle + Web Worker** |
| Q85 | P2P publish menu | **In app's share/export menu** |
| Q86 | Offline cache | **browsy embeds last Central snapshot** |
| Q87 | Online redirect | **flove.org when online** |
| Q88 | Extension manifests | **Chrome V3 + Firefox V2 polyfill** |
| Q89 | Search index | **Full-text: text + author + tags + URLs** |
| Q90 | Trust ranking | **Trust-weighted** |
| Q91 | Central enrichment | **Optional, anonymous** |
| Q92 | Auth flow | **browsy auto-links on first Central detection** |
| Q93 | Claim flow | **browsy handles Telegram + email linking** |
| Q94 | Export file | **Downloads as file to device** |
| Q95 | Repo auth | **Email + Telegram required**, export free |
| Q96 | Auto-sync | **Batched one request per load** |
| Q97 | Overlay auto-expand | **If unread content** |
| Q98 | Bottom nav injection | **floved by flove.js** |
| Q99 | MyNet sub-tabs | **Feed | Circles | Notifications** |
| Q100 | State model | **Extended with repoUrl, repoBranch, lastExport, centralAvailable** |
| Q101 | Central compat | **Always backwards-compatible**, no version handshake |
| Q51 | Popup layout | **Full dashboard: tabs (Activity \| Profile \| Settings)** |
| Q52 | Side panel | **Popup only (no side panel)** |
| Q53 | Options page | **Everything: permissions, theme, data export, account link, debug mode** |
| Q54 | Badge rules | **Only on flove.org pages** |
| Q55 | Content script injection | **On demand only (user clicks browsy icon)** |
| Q56 | Permission request UI | **Onboarding + just-in-time** |
| Q57 | Auth token storage | **Extension-internal encrypted store** |
| Q58 | Feature flag source | **App bridge first, Central fallback** |
| Q59 | Dev tools panel | **No dev tools panel (use browser devtools console)** |
| Q60 | Error recovery | **Auto-retry with exponential backoff (3 attempts)** |
| Q61 | Update flow | **Silent update** |
| Q62 | Keyboard shortcuts | **None** |
| Q63 | Context menu | **No context menu (deferred per BD06)** |
| Q64 | Multi-device sync | **Via GitHub repo (export JSON on each device)** |
| Q65 | Crash recovery | **Full state preserved: overlay, conversations, notifications, auth** |
| Q66 | First-run onboarding | **Quick tour: 3-step walkthrough (detect → overlay → auth)** |
| Q67 | Performance budget | **User-configurable, recommended defaults (50MB / 100MB / 1%)** |
| Q68 | Web permissions model | **flove.org + user-whitelisted sites** |
| Q69 | Telemetry | **Full telemetry with consent** |
| Q70 | Storage sync across updates | **Backward-compatible by design** |
| Q93 | Message encryption | **Encrypted with composite auth token (identity layers)** |
| Q93a | Signing key type | **Deterministic — derived from auth factors, recoverable** |
| Q93b | Factor count visibility | **Visible to receivers ("3-factor signed")** |
| Q93c | Auth model | **Extends existing: device + Telegram + email + trust vouches** |
| Q93d | Factor display privacy | **Count visible, specific factors TBD** |
| Q93e | Bonus scope | **Navigation bonuses + feature access + visibility weight** |
| Q93f | Trust hierarchy | **Layer 0: device → Layer 1: Telegram → Layer 2: Email → Layer 3: Trust vouches** |
| Q93g | Browsy slogan | **Authenticity and web of trust for flove apps** |
| Q93h | Fork source | **nety.html — extract crypto/identity layer, adapt for browsy** |
| Q93i | Key recovery | **Re-link factors + recovery code at setup (like nety masks)** |
| Q93j | Vouch mechanism | **Signed statement → B's key gains trust factor + stored in browsy + Central** |
| Q93k | First circle scope | **Trusts/heritage + trusts/recovery are browsy config actions, part of first circle** |
| Q101 | First circle contents | **Empty, user adds manually. Three tabs: Trusts \| Recovery \| Heritage** |
| Q102 | Vouch chain depth | **3 hops (matches nety's trust graph)** |
| Q103 | Heritage purpose | **Accountability partners + inherit trust chain. Public by default, claim after 1 year idle** |
| Q104 | Recovery purpose | **Trusted contacts who can help recover your account** |
| Q105 | Idle claim process | **1 year idle → heritage can claim** |
| Q106 | First circle size | **Unlimited. Heritage + recovery require approval to join** |
| Q107 | Trusts tab view | **Both outgoing + incoming vouches + trust scores** |
| Q108 | Recovery approval | **browsy sends request → contact approves in their browsy** |
| Q109 | Heritage visibility | **Full heritage chain visible (who vouched for whom, depth)** |
| Q110 | Key rotation | **User-initiated rotation only** |
| Q111 | Rotation effect on vouches | **Vouches remain valid (old key signatures still verify)** |
| Q112 | Recovery contact limits | **Max 5, threshold of 2 (2-of-5 to approve recovery)** |
| Q113 | Heritage claim notification | **Both browsy notification + email** |
| Q114 | Recovery threshold flexibility | **Fixed at 2 (no flexibility)** |
| Q115 | Heritage claim delay | **7-day grace period** |
| Q116 | Vouch revocation | **Yes, anytime (removes trust factor from recipient)** |
| Q117 | Multi-device signing | **Same key derived from same auth factors** |
| Q118 | Recovery contact requirement | **Yes, must have browsy installed** |
| Q119 | Heritage claim verification | **Signing key proves they're in the heritage list** |
| Q120 | First circle editing | **Yes, anytime (all three tabs)** |
| Q121 | Heritage chain depth | **Unlimited** |
| Q122 | Signing key export | **Only as recovery code (not raw key)** |
| Q123 | Recovery code format | **12-word mnemonic (like crypto wallets)** |
| Q124 | Recovery code usage | **Only when all auth factors are lost** |
| Q125 | Heritage chain visibility depth | **Full chain regardless of depth** |
| Q126 | Vouch signature format | **{ from, to, timestamp, trustLevel, signature }** |
| Q127 | Trust level values | **Determined by circle/group membership** |
| Q128 | Browsy first-run flow | **Link Telegram first, then set up first circle** |
| Q129 | Circle hierarchy | **Nested (circles within circles, like appy scores/stats)** |
| Q130 | First circle groups | **Heritage, Recovery, Closest (3 groups)** |
| Q131 | MyNet = Trusts | **Yes — Trusts replaces Circles terminology throughout** |
| Q132 | Close circle groups | **Friends, Family, Colleagues (second circle of trusts)** |
| Q133 | Trust tiers | **Closest → Close → Groups → Social (4 tiers)** |
| Q134 | Groups tier structure | **Groups of affinity (private or public), 4th = Social (public)** |
| Q135 | Full trust tier model | **Closest → Close → Groups → Social, each with sub-groups** |
| Q136 | Social tier purpose | **All of the above (public profile + posts + activity)** |
| Q137 | Groups tier types | **All (interest, project, geographic)** |
| Q138 | Trust tier visibility | **Yes, tier is part of public profile** |
| Q139 | Trust tier naming | **Closest → Close → Groups → Social** |
| Q140 | Trust tier transition | **User manually moves them** |
| Q141 | Trust tier limits | **No limits on any tier** |
| Q142 | Groups sub-structure | **Fixed categories + nested groups** |
| Q143 | Groups sub-categories | **Interest, Project, Geographic** |
| Q144 | Social tier content | **Everything you've made public** |
| Q145 | Closest sub-groups | **Heritage, Recovery, Closest (3 tabs)** |
| Q146 | Close sub-groups | **Friends, MyFamily (app), Others** |
| Q147 | MyFamily connection | **Pending — needs "push to trusts" + "Invite them" buttons** |
| Q148 | Close/Others group | **All of the above (uncategorized, other apps, temporary)** |
| Q149 | Tier movement rules | **Simple move. Heritage requires confirmation, recovery auto-processes** |
| Q150 | Browsy badge per tier | **No badge changes (tier is internal to browsy)** |
| Q151 | Trust storage | **browsy default. Trusts require publish consent. Heritage = mandatory public** |
| Q152 | Publish consent flow | **Consent at trust time ("Allow B to publish your trust?")** |
| Q153 | Heritage public mandate | **Both heritage membership + full chain published** |
| Q154 | Publish consent scope | **Only the fact of trust (A trusts B)** |
| Q155 | Publish consent revocation | **Yes, anytime** |
| Q156 | Publish vs heritage | **Heritage = always visible + accountability; Trusts = consent-based + social** |
| Q157 | Publish notification | **No notification, B sees it in their trusts list** |
| Q158 | Publish consent visibility | **Yes, list in trusts settings** |
| Q159 | Recovery publish rules | **Recovery contacts never get published (always private)** |
| Q160 | Publish model summary | **Heritage = always published. Trusts = consent required. Recovery = never published** |
| Q161 | Groups tier publish | **User chooses per group (public or private)** |
| Q162 | Social tier publish | **Always public (by definition)** |
| Q163 | Publish consent UI | **Trusts settings in browsy (one list)** |
| Q164 | Social tier discovery | **Yes (public by definition)** |
| Q165 | Publish consent granularity | **First tier (Close default). Groups = permission groups (3 max)** |
| Q166 | Publish to group limit | **Up to3 groups. Close = default extra group** |
| Q167 | Permission group count | **3 max** |
| Q168 | Permission group structure | **List of people + publish rules** |
| Q169 | Permission group naming | **Yes, custom names** |
| Q170 | Default permission groups | **Close + Public + Private (3 defaults)** |
| Q171 | Permission group visibility | **No (private to the group creator)** |
| Q172 | Permission group selection | **Checkbox (select multiple, up to 3)** |
| Q173 | Permission group editing | **Yes, but only the creator can edit** |
| Q174 | Permission group rules | **User-defined labels** |
| Q175 | Permission group inheritance | **No (each group is independent)** |
| Q176 | Permission group storage | **browsy local. Public only if manually synced** |
| Q177 | Permission group deletion | **All content becomes private** |
| Q178 | Permission group sync | **Manual only. "Save in browsy local" + "Save and Publish"** |
| Q179 | Permission group conflict | **Last sync wins** |
| Q180 | Publish to group flow | **Select groups → browsy signs → Publish** |
| Q181 | Publish signature content | **Full content + timestamp + sender key** |
| Q182 | Publish destination | **browsy local + GitHub (users/) + Central** |
| Q183 | Publish feedback | **Success toast ("Published to 2 groups")** |
| Q184 | Publish vs save | **Save = local storage; Publish = local + GitHub + Central** |
| Q185 | Publish content types | **All content types** |
| Q186 | Publish visibility | **Everyone (public by default). Groups = share button subs** |
| Q187 | Close group rules | **Hidden from everyone except the creator** |
| Q188 | Permission group visibility | **Group members only see content marked "share with [group]"** |
| Q189 | No group selected | **Private (only creator sees)** |
| Q190 | Full publish model | **Save = local only. Publish = local + GitHub + Central. Group = share with. No group = private** |
| Q191 | Permission groups standard | **Subs of Share button — new standard** |
| Q192 | Share button scope | **Only in appy-normal (new standard starts here)** |
| Q193 | Share button placement | **Global bottom bar + per-item actions** |
