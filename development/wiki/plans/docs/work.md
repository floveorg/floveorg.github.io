---
status: stable
section: docs/work
created: 2026-11-21
also: [development/standards/work.md, development/standards/mynet.md, development/standards/systems.md, development/standards/flows.md]
---

<a id="browsy-questions"></a>
# Browsy questions

> Source: `development/wiki/archive/old/browsy/browsy-questions.md` (archived 2026-11-21).
> Live questions A–L and the pre-build pendings are here; the 244-answer historical log is preserved in the archive.

> **Status 2026-11-17 — superseded in part.** Current spec:
> [`spec.md`](../../archive/old/browsy/spec.md).
> Historical decision log. Current work uses BSP IDs in the new plan.

> Fresh question interface for browsy architecture decisions.
> Load this file to continue asking questions without full session context.

---

## Current Status

**Last updated:** Q244 (2026-07-24)
**Total decisions:** 244 questions answered
**Pending:** 2 items (BD30, BD31), Q147 (MyFamily integration)

---

## Decisions Made

| ID | Category | Question | Decision |
|----|----------|----------|----------|
| BD01 | Content | Content extraction? | **Performance-optimal** |
| BD02 | UI | Badge display? | **Floating badge (menu item later)** |
| BD03 | Loading | Plugin loading? | **Cache after first load** |
| BD04 | State | State management? | **Performance-optimal** |
| BD05 | Memory | Memory management? | **Global limit** |
| BD06 | Menu | Context menu? | **Native browser (defer)** |
| BD07 | UI | Quick panel? | **Not needed** |
| BD08 | Notifications | Notifications? | **Both (notifications + badge)** |
| BD10 | Notifications | Notification triggers? | **All (items, trust, mentions)** |
| BD11 | Cache | Cache strategy? | **Version-based** |
| BD12 | Security | Security? | **All (minimal + CSP + sandboxed)** |
| BD13 | Updates | Updates? | **Manual update** |
| BD14 | Errors | Error handling? | **User notification** |
| BD15 | Privacy | Privacy? | **All (local + encrypted)** |
| BD16 | Auth | Authentication flow? | **All (ID + badges + account)** |
| BD17 | Data | Data levels? | **All data (adds metadata ID)** |
| BD18 | Compat | Compatibility? | **Progressive enhancement** |
| BD19 | Performance | Performance? | **All (lazy + cache + background)** |
| BD20 | A11y | Accessibility? | **All (ARIA + keyboard + high contrast)** |
| BD21 | i18n | Internationalization? | **Flove standards + user-configurable** |
| BD22 | Theme | Theming? | **Flove theme standards (§13.14)** |
| BD23 | Settings | Customization? | **Settings page (extension options)** |
| BD24 | Integration | Integration? | **All (storage + messaging + API)** |
| BD25 | API | API exposure? | **Both (flove + custom)** |
| BD26 | Lifecycle | Lifecycle management? | **Browser-managed (automatic)** |
| BD27 | Testing | Testing approach? | **All (unit + integration + manual)** |
| BD28 | Logging | Logging? | **Console only (browser devtools)** |
| BD29 | Analytics | Analytics? | **Full analytics (with user consent)** |

### Survey decisions (2026-07-24, browsy + appy + plans)

| ID | Category | Question | Decision |
|----|----------|----------|----------|
| Q01 | Browsy | Content extraction feature? | **Not wanted — removed entirely** |
| Q02 | Appy | Mini→Basic threshold | **Seasonal/time-limited events lower threshold temporarily** |
| Q03 | Browsy | Nety P2P scope | **CPU/GPU + storage + bandwidth; publish to P2P addresses as new option** |
| Q04 | Appy | Rainbow roadmap display | **All visible always (dimmed locked tiers — current design)** |
| Q05 | Browsy | P2P publish targets | **In the flove app's share/export menu** |
| Q06 | Appy | Normal tier agent interaction | **On/off only — full control is advanced's reward** |
| Q07 | Browsy | Badge display context | **Flove pages + any page with public profile data embedded** |
| Q08 | Appy | Sety visualization gate | **Moved to advanced tier** |
| Q09 | Appy | Normal tier redefined | **MyNet browsy + wizy mini** |
| Q10 | Browsy | Offline capabilities | **Browse whole flove (last Central snapshot embedded); online → flove.org; local fallback** |
| Q11 | Appy | Advanced tier scope | **Everything — super is purely hosting/governing others** |
| Q12 | Browsy | Central sync frequency | **Big update alert messages, committed, shown in profile menu within browsy** |
| Q13 | Browsy | Update alert content | **Badge count + tap to see full release notes on flove.org** |
| Q14 | Appy | Super governance mechanics | **Deferred — leave for now** |
| Q15 | Browsy | Profile menu structure | **Update alerts + settings; alerts at top of appy settings tab** |
| Q16 | Appy | Wizy mini at normal | **Two agents: summaries + suggestions (on/off only)** |
| Q17 | Browsy | Extension manifest target | **Chrome + Firefox (Manifest V3 + V2 polyfill)** |
| Q18 | Appy | Sety pro at advanced | **Visualization + data export + complex perspective/rater rules** |
| Q19 | Browsy | Content script injection | **flove.org pages only** |
| Q20 | Appy | Normal MyNet browsy identity | **Browsy's own lightweight social feed + social overlays on flove pages** |
| Q21 | Browsy | Social overlay types | **Chat + feed + notifications (mentions, trust, followers, agents)** |
| Q22 | Appy | Vizy at advanced vs super | **Advanced: vizy lite (fewer shapes, smaller canvas); Super: full vizy studio** |
| Q23 | Browsy | Notification overlay triggers | **All (mentions, trust, circle invites, followers) + agent activity** |
| Q24 | Appy | Vizy lite shape count | **3 shapes: List + Rainbow + Circle** |
| Q25 | Browsy | Overlay dismiss behavior | **Stays until user dismisses (manual close)** |
| Q26 | Appy | XR/VR for super | **XR/VR from day one on super** |
| Q27 | Browsy | Overlay positioning | **Injected into page layout — single collapsible sidebar panel** |
| Q28 | Appy | Mini tier agent teasers | **Plan for appy-normal.html — MyNet + auth managed in browsy** |
| Q29 | Appy | Circle member limits | **No limits — unlimited members per circle** |
| Q30 | Browsy | Overlay priority | **Single collapsible sidebar panel (all overlays together)** |
| Q31 | Appy | Agent data sources | **Followed posts + bookmarks + circle content** |
| Q32 | Browsy | Sidebar collapse behavior | **Starts collapsed every time** |
| Q33 | Appy | Chat message retention | **Follows ephemeral setting** |
| Q34 | Browsy | P2P publish format | **Signed Flove post format** |
| Q35 | Appy | Agent activation UX | **Account panel (below language)** |
| Q36 | Browsy | Signed post verification | **Client-side only (receiving browsy instance)** |
| Q37 | Appy | Circle visibility levels | **Private / Close (friends) / Related (share groups) / Public** |
| Q38 | Browsy | Offline post indexing | **Full-text index (text + author + tags + URLs)** |
| Q39 | Appy | Close vs Related | **Close = friends; Related = people you share groups with** |
| Q41 | Appy | Chat group formation | **Group chat moved to super tier** |
| Q42 | Browsy | Search result ranking | **Trust-weighted** |
| Q43 | Appy | Chat scope post-Q41 | **DMs only at normal** |
| Q44 | Browsy | Trust weight source | **Local + Central enrichment (Central optional)** |
| Q45 | Appy | DM features | **Text + reactions + read receipts + editing** |
| Q46 | Browsy | Central enrichment privacy | **Anonymous pull — no identification sent** |
| Q47 | Appy | DM edit window | **Unlimited** |
| Q48 | Appy | Reactions format | **Custom user-defined set** |
| Q49 | Appy | Reactions setup | **Pick from full emoji grid** |
| Q50 | Appy | Normal scope confirmation | **Confirmed** |

### Browsy implementation decisions (2026-07-24, browsy only)

| ID | Category | Question | Decision |
|----|----------|----------|----------|
| Q51 | UI | Popup panel layout? | **Full dashboard: tabs (Activity \| Profile \| Settings)** |
| Q52 | UI | Side panel vs popup? | **Popup only (no side panel)** |
| Q53 | Settings | Options page scope? | **Everything: permissions, theme, data export, account link, debug mode** |
| Q54 | UI | Badge rules? | **Only on flove.org pages** |
| Q55 | Timing | Content script injection? | **On demand only (user clicks browsy icon)** |
| Q56 | UX | Permission request UI? | **Onboarding + just-in-time** |
| Q57 | Security | Auth token storage? | **Extension-internal encrypted store** |
| Q58 | Features | Feature flag source? | **App bridge first, Central fallback** |
| Q59 | Dev | Dev tools panel? | **No dev tools panel (use browser devtools console)** |
| Q60 | Errors | Error recovery? | **Auto-retry with exponential backoff (3 attempts)** |
| Q61 | Updates | Update flow? | **Silent update** |
| Q62 | UX | Keyboard shortcuts? | **None** |
| Q63 | Menu | Context menu structure? | **No context menu (deferred per BD06)** |
| Q64 | Sync | Multi-device sync? | **Via GitHub repo (export JSON on each device)** |
| Q65 | Resilience | Crash recovery? | **Full state: overlay, conversations, notifications, auth** |
| Q66 | UX | First-run onboarding? | **Quick tour: 3-step walkthrough (detect → overlay → auth)** |
| Q67 | Perf | Performance budget? | **User-configurable in options page, recommended defaults (50MB / 100MB / 1%)** |
| Q68 | Security | Web permissions model? | **flove.org + user-whitelisted sites** |
| Q69 | Privacy | Telemetry? | **Full telemetry (with consent): install count, feature usage, crash reports, page visits, trust graph stats** |
| Q70 | Storage | Storage sync across updates? | **Backward-compatible by design (no migration needed)** |
| Q93 | Security | Message encryption? | **Encrypted with user's composite auth token (identity layers)** |
| Q93a | Identity | Signing key type? | **Deterministic — derived from auth factors, recoverable** |
| Q93b | Identity | Factor count visibility? | **Visible to receivers ("3-factor signed")** |
| Q93c | Identity | Auth model? | **Extends existing: device + Telegram + email + trust vouches** |
| Q93d | Identity | Factor display privacy? | **TBD — count visible, specific factors TBD** |
| Q93e | Identity | Bonus scope? | **Navigation bonuses + feature access + visibility weight** |
| Q93f | Identity | Trust hierarchy? | **Layer 0: device → Layer 1: Telegram → Layer 2: Email → Layer 3: Trust vouches** |
| Q93g | Identity | Browsy slogan? | **Authenticity and web of trust for flove apps** |
| Q93h | Identity | Fork source? | **nety.html — extract crypto/identity layer, adapt for browsy** |
| Q93i | Identity | Signing key recovery? | **Re-link factors + recovery code at setup (like nety masks)** |
| Q93j | Identity | Vouch mechanism? | **Signed statement "A trusts B" → B's key gains trust factor + stored in browsy + Central** |
| Q93k | Identity | First circle scope? | **Trusts/heritage + trusts/recovery are browsy config actions, part of first circle** |
| Q95 | UI | Overlay animation? | **Scale from button (expand from bottom-left toggle)** |
| Q96 | Storage | Storage quota warning? | **Warn + prompt (notification + export/clear)** |
| Q97 | Trust | Navigation bonus mechanics? | **Deferred — first case: upload images if heritage** |
| Q98 | Trust | Vouch chain? | **Key gains + signed statement** |
| Q99 | Identity | Factor display default? | **Count only, signer can optionally reveal factors** |
| Q100 | Security | Key recovery? | **Re-link factors + recovery code at setup** |
| Q101 | Identity | First circle contents? | **Empty, user adds manually. Tabs: Trusts \| Recovery \| Heritage** |
| Q102 | Trust | Vouch chain depth? | **3 hops (matches nety's trust graph)** |
| Q103 | Identity | Heritage purpose? | **Accountability partners + inherit trust chain. Public by default, claim after 1 year idle** |
| Q104 | Identity | Recovery purpose? | **Trusted contacts who can help recover your account** |
| Q105 | Identity | Idle claim process? | **1 year idle → heritage can claim** |
| Q106 | Identity | First circle size? | **Unlimited. Heritage + recovery require approval to join** |
| Q107 | UI | Trusts tab view? | **Both outgoing + incoming vouches + trust scores** |
| Q108 | Identity | Recovery approval? | **browsy sends request → contact approves in their browsy** |
| Q109 | Identity | Heritage visibility? | **Full heritage chain visible (who vouched for whom, depth)** |
| Q110 | Security | Key rotation? | **User-initiated rotation only** |
| Q111 | Security | Rotation effect on vouches? | **Vouches remain valid (old key signatures still verify)** |
| Q112 | Identity | Recovery contact limits? | **Max 5, threshold of 2 (2-of-5 to approve recovery)** |
| Q113 | Identity | Heritage claim notification? | **Both browsy notification + email** |
| Q114 | Security | Recovery threshold flexibility? | **Fixed at 2 (no flexibility)** |
| Q115 | Identity | Heritage claim delay? | **7-day grace period** |
| Q116 | Trust | Vouch revocation? | **Yes, anytime (removes trust factor from recipient)** |
| Q117 | Security | Multi-device signing? | **Same key derived from same auth factors** |
| Q118 | Identity | Recovery contact requirement? | **Yes, must have browsy installed** |
| Q119 | Identity | Heritage claim verification? | **Signing key proves they're in the heritage list** |
| Q120 | Identity | First circle editing? | **Yes, anytime (all three tabs)** |
| Q121 | Trust | Heritage chain depth? | **Unlimited** |
| Q122 | Security | Signing key export? | **Only as recovery code (not raw key)** |
| Q123 | Security | Recovery code format? | **12-word mnemonic (like crypto wallets)** |
| Q124 | Security | Recovery code usage? | **Only when all auth factors are lost** |
| Q125 | Identity | Heritage chain visibility depth? | **Full chain regardless of depth** |
| Q126 | Trust | Vouch signature format? | **{ from, to, timestamp, trustLevel, signature }** |
| Q127 | Trust | Trust level values? | **Determined by circle/group membership** |
| Q128 | UX | Browsy first-run flow? | **Link Telegram first, then set up first circle** |
| Q129 | Trust | Circle hierarchy? | **Nested (circles within circles, like appy scores/stats)** |
| Q130 | Trust | First circle groups? | **Heritage, Recovery, Closest (3 groups)** |
| Q131 | Trust | MyNet = Trusts? | **Yes — Trusts replaces Circles terminology throughout** |
| Q132 | Trust | Close circle groups? | **Friends, Family, Colleagues (second circle of trusts)** |
| Q133 | Trust | Trust tiers? | **Closest → Close → Groups → Social (4 tiers)** |
| Q134 | Trust | Groups tier structure? | **Groups of affinity (private or public), 4th = Social (public)** |
| Q135 | Trust | Full trust tier model? | **Closest → Close → Groups → Social, each with sub-groups** |
| Q136 | Trust | Social tier purpose? | **All of the above (public profile + posts + activity)** |
| Q137 | Trust | Groups tier types? | **All (interest, project, geographic)** |
| Q138 | Trust | Trust tier visibility? | **Yes, tier is part of public profile** |
| Q139 | Trust | Trust tier naming? | **Closest → Close → Groups → Social** |
| Q140 | Trust | Trust tier transition? | **User manually moves them** |
| Q141 | Trust | Trust tier limits? | **No limits on any tier** |
| Q142 | Trust | Groups sub-structure? | **Fixed categories + nested groups** |
| Q143 | Trust | Groups sub-categories? | **Interest, Project, Geographic** |
| Q144 | Trust | Social tier content? | **Everything you've made public** |
| Q145 | Trust | Closest sub-groups? | **Heritage, Recovery, Closest (3 tabs)** |
| Q146 | Trust | Close sub-groups? | **Friends, MyFamily (app), Others** |
| Q147 | Integration | MyFamily connection? | **Pending — needs "push to trusts" + "Invite them" buttons** |
| Q148 | Trust | Close/Others group? | **All of the above (uncategorized, other apps, temporary)** |
| Q149 | Trust | Tier movement rules? | **Simple move. Heritage requires confirmation, recovery auto-processes** |
| Q150 | UI | Browsy badge per tier? | **No badge changes (tier is internal to browsy)** |
| Q151 | Trust | Trust storage? | **browsy default. Trusts require publish consent (at trust time or request after). Heritage = mandatory public + publish consent once accepted** |
| Q152 | Trust | Publish consent flow? | **Consent at trust time ("Allow B to publish your trust?")** |
| Q153 | Trust | Heritage public mandate? | **Both heritage membership + full chain published** |
| Q154 | Trust | Publish consent scope? | **Only the fact of trust (A trusts B)** |
| Q155 | Trust | Publish consent revocation? | **Yes, anytime** |
| Q156 | Trust | Publish vs heritage difference? | **Heritage = always visible + accountability chain; Trusts = consent-based + social connections** |
| Q157 | Trust | Publish notification? | **No notification, B sees it in their trusts list** |
| Q158 | Trust | Publish consent visibility? | **Yes, list in trusts settings** |
| Q159 | Trust | Recovery publish rules? | **Recovery contacts never get published (always private)** |
| Q160 | Trust | Publish model summary? | **Heritage = always published. Trusts = consent required. Recovery = never published** |
| Q161 | Trust | Groups tier publish? | **User chooses per group (public or private)** |
| Q162 | Trust | Social tier publish? | **Always public (by definition)** |
| Q163 | Trust | Publish consent UI? | **Trusts settings in browsy (one list)** |
| Q164 | Trust | Social tier discovery? | **Yes (public by definition)** |
| Q165 | Trust | Publish consent granularity? | **First tier (Close included as default). Groups tier = permission groups (3 max, pre-defined + user-created)** |
| Q166 | Trust | Publish to group limit? | **Up to3 groups. Close = default extra group between private and public** |
| Q167 | Trust | Permission group count? | **3 max** |
| Q168 | Trust | Permission group structure? | **List of people + publish rules** |
| Q169 | Trust | Permission group naming? | **Yes, custom names** |
| Q170 | Trust | Default permission groups? | **Close + Public + Private (3 defaults)** |
| Q171 | Trust | Permission group visibility? | **No (private to the group creator)** |
| Q172 | UI | Permission group selection? | **Checkbox (select multiple, up to 3)** |
| Q173 | Trust | Permission group editing? | **Yes, but only the creator can edit** |
| Q174 | Trust | Permission group rules? | **User-defined labels** |
| Q175 | Trust | Permission group inheritance? | **No (each group is independent)** |
| Q176 | Trust | Permission group storage? | **browsy local storage. Public only if manually synced in UI** |
| Q177 | Trust | Permission group deletion? | **All content becomes private** |
| Q178 | Trust | Permission group sync? | **Manual only. Two buttons: "Save in browsy local" + "Save and Publish"** |
| Q179 | Trust | Permission group conflict? | **Last sync wins** |
| Q180 | Trust | Publish to group flow? | **Select groups → browsy signs → Publish** |
| Q181 | Trust | Publish signature content? | **Full content + timestamp + sender key** |
| Q182 | Trust | Publish destination? | **browsy local + GitHub (users/ or else repo) + Central** |
| Q183 | UX | Publish feedback? | **Success toast ("Published to 2 groups")** |
| Q184 | Trust | Publish vs save distinction? | **Save = local storage; Publish = local + GitHub + Central** |
| Q185 | Trust | Publish content types? | **All content types** |
| Q186 | Trust | Publish visibility? | **Everyone (public by default). Groups = share button subs** |
| Q187 | Trust | Close group rules? | **Hidden from everyone except the creator** |
| Q188 | Trust | Permission group visibility model? | **Group members only see content marked "share with [group]"** |
| Q189 | Trust | No group selected? | **Private (only creator sees)** |
| Q190 | Trust | Full publish model? | **Save = local only. Publish = local + GitHub + Central. Select group = "share with group." No group = private** |
| Q191 | Trust | Permission groups standard? | **Subs of Share button — new standard** |
| Q192 | Standard | Share button scope? | **Only in appy-normal (new standard starts here)** |
| Q193 | UI | Share button placement? | **Global bottom bar + per-item actions** |
| Q194 | Sync | Conflict UI (major)? | **Side-by-side diff** |
| Q195 | Sync | Clock skew handling? | **Accept risk (NTP usually suffices)** |
| Q196 | Sync | JSON merge strategy? | **Merge by field (preserve non-conflicting fields)** |
| Q197 | Sync | Nety ↔ Central authority? | **Nety is authoritative** |
| Q198 | Sync | Browsy ↔ Central conflict? | **Detect and resolve (show diff to user)** |
| Q199 | Sync | Offline queue? | **Local queue (IndexedDB), sync when back online** |
| Q200 | Sync | Decentral → Central push? | **Nety pushes all public data to Central** |
| Q201 | Sync | Recovery source authority? | **Nety authoritative; browsy = ask user** |
| Q202 | Sync | Conflict log storage? | **browsy local only (IndexedDB)** |
| Q203 | Sync | Schema migration sync? | **Server accepts any version, ignores missing fields** |
| Q204 | Identity | Device revocation? | **Re-vouch all trusts from another device** |

### Interoperability & Sync — Round 2 (Q205–Q224)

| ID | Category | Question | Decision |
|----|----------|----------|----------|
| Q205 | Sync | Sync protocol? | **Timestamps del cliente (simple, NTP suele basta)** |
| Q206 | Sync | Conflict detection granularity? | **Documento entero** |
| Q207 | Sync | Sync retry strategy? | **Exponential backoff (3 attempts)** |
| Q208 | Sync | Server validates schema on sync? | **Sí, rechaza si es inválido + log + notify user** |
| Q209 | Sync | Partial sync (subset of data)? | **Delta sync (only changed fields)** |
| Q210 | Sync | Real-time vs batched sync? | **Batched 5 min + real-time for trust changes** |
| Q211 | Sync | Conflict notification timing? | **En la próxima visita (badge en popup)** |
| Q212 | Sync | Max devices per account? | **5** |
| Q213 | Sync | Bandwidth limit per sync? | **No limit (delta sync lo mantiene pequeño)** |
| Q214 | Sync | Offline staleness threshold? | **7 días** |
| Q215 | Sync | Trust graph sync scope? | **Full graph (3 hops, ~1MB max)** |
| Q216 | Sync | Permission group sync mode? | **Semi-automático (auto-save local, push con botón)** |
| Q217 | Sync | Profile sync scope? | **Full profile on each sync** |
| Q218 | Sync | Undo conflict resolution? | **Sí, 30 días** |
| Q219 | Sync | Sync history retention? | **30 días, archive local** |
| Q220 | Sync | Device identification? | **Nombre del usuario + browser fingerprint** |
| Q221 | Sync | Sync status UI? | **Badge en popup (synced/syncing/error)** |
| Q222 | Sync | Sync error handling? | **Queue + notify user después de 3 intentos** |
| Q223 | Sync | Data compression? | **gzip en transmission, raw en storage** |
| Q224 | Sync | Encryption in transit? | **TLS + E2E para trust data** |

### Development Strategy — Browser Plugin First (Q225–Q244)

| ID | Category | Question | Decision |
|----|----------|----------|----------|
| Q225 | Strategy | Browser plugin MVP scope? | **Auth + mynet + publish bridge (los 3 pilares)** |
| Q226 | Content | Content sync priority? | **App data > mynet > auth (orden inverso)** |
| Q227 | Perf | Memory/CPU budget? | **50MB storage / 100MB memory / 1% CPU idle** |
| Q228 | Offline | Offline data strategy? | **IndexedDB local queue + sync when online** |
| Q229 | Local-first | What stays local vs synced? | **Local: keys, drafts. Synced: profile, trust, app state** |
| Q230 | Privacy | Public by default? | **No — private by default, user publishes explicitly** |
| Q231 | Multiplatform | Target platforms first? | **Chrome + Firefox desktop, then mobile** |
| Q232 | Size | Max extension size? | **<10MB (target 5MB)** |
| Q233 | Updates | Extension update strategy? | **Auto-update + changelog visible** |
| Q234 | Testing | Testing strategy? | **Unit + integration + manual** |
| Q235 | Docs | Required documentation? | **README + API docs + user guide** |
| Q236 | UX | First-time user experience? | **Tour completo (5+ pasos con explicaciones)** |
| Q237 | Errors | Error reporting? | **Console + crash reports con consent** |
| Q238 | Analytics | Metrics to track? | **Todo detallado, con opción "No trace"** |
| Q239 | Security | Security audit timing? | **Después del MVP** |
| Q240 | Perf | Performance monitoring? | **Configurable en options, defaults recomendados** |
| Q241 | Feedback | User feedback collection? | **GitHub issues + botón in-app + circle en users/ para sugerencias** |
| Q242 | Release | Release cadence? | **No preestablecido — cuando hayan features** |
| Q243 | Compat | Backward compatibility? | **Últimas 2 versiones mayores** |
| Q244 | Open source | Open source strategy? | **Todo open source** |

---

## Next Questions to Ask

### BD30 — Documentation: How is browsy documented?

Browsy needs documentation. How?

a. README only (minimal)
b. Full docs (API, usage, examples)
c. Interactive docs (live examples)
d. All of the above

★ suggested: d

### BD31 — Support: How does browsy provide user support?

Users may need help with browsy. How?

a. GitHub issues (public)
b. Email support (private)
c. Community forum (discussion)
d. All of the above

★ suggested: d

---

## How to Use

1. **Load this file** to get fresh context
2. **Answer questions** by replying with letters (e.g. 1a, 2d)
3. **Add new questions** as needed
4. **Update decisions** table when answered
5. **Sync decisions** to `spec.md` and the plans index.

---

## Related Files

- `spec.md` — Current Browsy spec
- Live questions below (A–L, 2026-11-17)
- `plans/central-backend.md` — Central backend decisions
- `plans/2026-11-17-appy-authy-mynet.md` — Authy/MyNet decisions

---

## Live questions — 2026-11-17 (Browsy · Authy · Wizy · Nety)

> Moved from the old `pendings.md` on 2026-11-17. These are the live
> survey questions; the decisions above are historical.

This is the **only** register for these questions: the formerly parked A01–A10
copy in [`plans/2026-11-19-authy-open-questions.md`](../../archive/old/plans/2026-11-19-authy-open-questions.md)
now points back here. Update status here, not in both files. Work filter:
[backend · systems](https://flove.org/development/index.html#work?tab=docs&view=r2&subtab=work&category=backend&section=systems).

## A · Authy and identity

| ID | Question | Why it matters |
|---|---|---|
| A01 | Should the five steps stay Self → Email → Telegram → Phone → Bio, or be reordered by proof strength? | The current UI implies a progression the protocol does not enforce. |
| A02 | (Decided 2026-11-17) Is the publish gate verified Telegram **L3**? | Yes: risa signed claim or Authy nonce+DM. A bare presence link is SelfAuth L1. |
| A03 | Do the displayed points (+4/+12/+6/+8) or the awarded points (20/50/100/200) become the single source? | Both exist in appy-basic today; they cannot both be right. |
| A04 | Is "Self" a level or just the default profile state? | It has a bar, points and a form but is not a channel. |
| A05 | What exactly is a session token for an app: JWT, signed capability object, or opaque handle? | Wizy/Appy need to act without the private key. |
| A06 | How many identities can one human hold, and how do masks relate to the root key? | nety-frontend already has a mask selector; Authy has no model yet. |
| A07 | What is the recovery quorum: how many peers, which circles, what probation? | "Social quorum" is named but undefined. |
| A08 | Does a channel proof live as P (private) or M (metadata)? Can peers verify it without seeing the handle? | Proofs can leak the handle/phone. |
| A09 | Should biometrics ever leave the device as a proof, or stay as a local unlock factor? | Highest sensitivity; current UI treats it as a channel. |
| A10 | Does Authy bind to the Nety PeerId, or is the PeerId a separate key? | Duplicate identities complicate trust and revocation. |
| A11 | What is the lifecycle of `flove:authy` (schema, versioning, migration, reset)? | It now persists across appy-basic and the Authy index. |
| A12 | What exactly goes to the local keeper vs the social keeper, and who signs it? | The index stores two payloads; the contract is provisional. |
| A13 | Is the claim nonce issued by a server, a bot, or locally? | The demo mints it locally; risa uses server-side libSQL with TTL. |
| A14 | (Decided 2026-11-17) Should Telegram presence already allow local sharing? | No. Only verified Telegram L3 opens MyNet/local sharing. |
| A15 | (Decided 2026-11-17) Does verified Telegram L3 enable MyNet? | Yes; bare presence enables nothing. Public/S is deferred. |
| B11 | Which MyFamily fields survive in MyNet's group projection? | **Decided 2026-11-17:** the 5 type percentages; the raw 7×5 answers are opt-in. |

> **Decided 2026-11-17:** A02/A14/A15 — **verified Telegram L3** is the gate
> (risa signed claim or Authy nonce+DM); a bare presence link is SelfAuth L1
> and enables nothing. A11 — **`flove:authy/1`** is canonical; `flove:authy` is
> migrated once. B11 — group projection is the 5 MyFamily percentages.
> **Still open:** A01, A03, A05–A10, A12–A13.

## B · MyFamily and third-party data

| ID | Question | Why it matters |
|---|---|---|
| B01 | Is L the right default for an added person, and when should P or S win? | The record profiles an identifiable third person. |
| B02 | Does the subject (the friend) have a right to see, correct or delete the record? | Current app has no subject-facing flow. |
| B03 | Can the owner share a MyFamily record at all without the subject's consent? Under which conditions? | The product intent is sharing, the ethics are unresolved. |
| B04 | What is the minimum viable L projection: traits, raters, nuances, or a derived sentence? | Raw nuances can be more revealing than traits. |
| B05 | What is a "public card" for a third person, and can it exist without their approval? | The possible web-social path needs a boundary. |
| B06 | How are children or vulnerable people handled? | MyFamily explicitly includes family. |
| B07 | Does each person get a stable `personId`, and who owns it across devices? | Needed for records, grants and erasure. |
| B08 | What happens to grants and peer copies when the owner deletes a person? | Erasure must propagate as far as honestly possible. |
| B09 | Can MyFamily records be imported from another user, or only authored? | Determines whether it is a manager or a one-way export. |
| B10 | Is the current one-person-per-page model replaced by a list, or kept as a detail view? | UI and data model both change. |

## C · Permissions and grants

| ID | Question | Why it matters |
|---|---|---|
| C01 | Is the grant unit a file, a JSON path, an array slice or a field? | Determines the whole enforcement engine. |
| C02 | What does `derive` mean exactly, and can it be revoked separately from `view`? | D1–D3 need a capability boundary. |
| C03 | What does `aggregate` allow, and can the result be shared? | Aggregates can leak the inputs. |
| C04 | Is `copy` ever allowed, or is every share a reference plus encrypted projection? | Copy defeats revocation. |
| C05 | Are circles the only principal, or can single keys/groups be principals too? | Old specs disagree. |
| C06 | What is the default TTL for an L grant? | Short TTL is the main revocation mitigation. |
| C07 | Does revocation rotate the content key, and who re-encrypts what? | Costly but necessary for real revocation. |
| C08 | How are grants displayed to a non-technical user (paths vs friendly labels)? | Path grammar must not become the UI. |
| C09 | Can a grant be delegated (A grants B the right to grant C)? | Not needed for v1, but changes the schema. |
| C10 | What does "denied" look like: hide existence, or say "no access"? | Metadata leakage vs clarity. |
| C11 | Is P2P permission enforcement a separate trunk from Browsy local federation? | The plan assumes yes; it needs an owner and a boundary. |

## D · Local network and transport

| ID | Question | Why it matters |
|---|---|---|
| D01 | QR/manual endpoint, LAN discovery, WebRTC, or Nety DHT for addresses? | The core of "directly from users". |
| D02 | Does the local net work across NAT without a relay, and is a relay allowed? | Determines mobile/remote viability. |
| D03 | Is the transport peer-to-peer at the browser level or via a localhost helper? | MV3 cannot open arbitrary sockets. |
| D04 | How does a peer authenticate before the first pull: key fingerprint, invite, both? | Prevents impersonation. |
| D05 | What is the delta format and conflict model (vector clock, CRDT, last-write-wins)? | Needed for offline sessions. |
| D06 | What is the maximum stale window for L before Wizy warns? | Freshness is part of the privacy contract. |
| D07 | How is spam/Sybil handled on the local net? | Direct peers can still be malicious. |
| D08 | Does turning the local net off still allow cached L? | UX and expectations. |

## E · Wizy and derivation

| ID | Question | Why it matters |
|---|---|---|
| E01 | Which derivation ships first: D0, D1, or both? | Scope for M5. |
| E02 | Does D2 (on-device model) need a specific runtime (WASM, WebGPU), and what size budget? | Extension size and battery. |
| E03 | What exactly is in a D3 de-identified payload, and who audits the de-identification? | The highest-risk outbound path. |
| E04 | Can D be shared as L or S, and does it inherit the inputs' grants? | A derived file can leak its sources. |
| E05 | What does the explanation show: inputs, weights, both, or a natural-language rationale? | Trust and inspectability. |
| E06 | Does Wizy see P values directly, or only aggregates? | Current plan says Wizy sees P in memory; confirm. |
| E07 | Is there a "no derivation" mode that only filters and merges? | D0 is the safe default. |
| E08 | How are recommendations versioned and invalidated when inputs change? | Stale advice is a trust bug. |

## F · Nety and the social layer

> **Nota 2026-11-17 — Browsy es cliente de Nety, no nodo.** La extensión no abre
> sockets ni corre un DHT; habla con el gateway/daemon por HTTPS/WebSocket. El
> transporte Local es otro carril (WebRTC o helper nativo) y nunca pasa por Nety.
> No se forkeará `nety.html` para identidad: Authy es la raíz y Nety importa la
> misma raíz (BSP-I05).

| ID | Question | Why it matters |
|---|---|---|
| F09 | ¿Browsy es cliente o nodo de Nety? | MV3 no puede ser un nodo completo; el gateway/daemon es obligatorio. |
| F01 | When will the gateway and daemon actually connect (bootstrap/mDNS)? | M4 is blocked until then. |
| F02 | What is the S bundle schema, and is it exactly the L schema with a different class? | "Structured like local data" needs a contract. |
| F03 | Are group-visible S bundles encrypted, and with which key model? | Public is not the only social mode. |
| F04 | What does Nety store, for how long, and who can delete it? | Retention is a privacy decision. |
| F05 | Can Nety rank S results without learning the user's L graph? | Privacy-preserving ranking. |
| F06 | Are likes/reposts/trust part of S or separate metadata? | They reveal the social graph. |
| F07 | Does Central mirror S automatically, or only on request? | Duplicate copies and takedown. |
| F08 | What is the takedown path for a public S bundle? | Legal and ethical requirement. |

## G · Browsy engineering and security

| ID | Question | Why it matters |
|---|---|---|
| G01 | Which storage backend for the vault: IndexedDB + WebCrypto, OPFS, native messaging? | MV3 limits and quotas. |
| G02 | What is the unlock factor: passphrase, WebAuthn, OS keychain, combination? | Defines the "supersafe" bar. |
| G03 | How is the extension updated and reviewed (store, signed builds, reproducible)? | Supply-chain risk. |
| G04 | What are the minimum permissions in the manifest for local net + Nety? | Over-broad permissions kill trust. |
| G05 | How does the bridge expose data to flove.org apps without letting XSS read the vault? | Same-origin apps are the attack surface. |
| G06 | What happens when storage is full or the vault is corrupted? | Recovery without plaintext leaks. |
| G07 | Is there a panic/lock button, and what does it wipe? | Physical threat model. |
| G08 | How are logs redacted before a bug report? | Diagnostics can leak P. |

## H · UX and product

| ID | Question | Why it matters |
|---|---|---|
| H01 | What does first-run onboarding show: privacy classes, peers, or an empty vault? | Sets expectations. |
| H02 | How does a user create their first grant without understanding paths? | Usability vs precision. |
| H03 | Where do the "local net" and "Nety social" toggles live? | They are the two big switches. |
| H04 | What does "what others see" look like on mobile? | Projection preview is core. |
| H05 | How are denied/expired/revoked states shown? | Honest limits are part of privacy. |
| H06 | Should Wizy be a popup, side panel, or full workspace? | MV3 and focus. |
| H07 | What is the empty state for MyFamily with no records? | Sensitive onboarding. |
| H08 | Which language(s) ship first for the Authy index and MyFamily use case? | flove is bilingual; scope matters. |

## I · Legal, ethics and governance

| ID | Question | Why it matters |
|---|---|---|
| I01 | Who is the data controller for a MyFamily record: the owner, the subject, or both? | Determines consent and erasure duties. |
| I02 | What is the age policy for P2P sharing and third-party records? | Children in family data. |
| I03 | Does the project need a privacy notice / DPIA before M3? | Shipping personal data cross-peer. |
| I04 | How are subject-access and deletion requests handled peer-to-peer? | Copies make this hard. |
| I05 | What is the policy for law-enforcement or abuse requests? | Governance gap. |
| I06 | Are there categories that must never be shareable (health, sexual, political)? | Product ethics. |

## J · Integration, schema and legacy

| ID | Question | Why it matters |
|---|---|---|
| J01 | Does `flove-bundle/0.1` become the canonical envelope, or does the portrait stay primary? | Compatibility with Appy and apps. |
| J02 | How are existing `*-portrait.json` files migrated into bundles? | Users already have files. |
| J03 | Does Appy render from a file, from Browsy, or both? | Determines the bridge. |
| J04 | What is the versioning policy when `flove-portrait/1` gains fields? | Apps and Appy must not break. |
| J05 | Which parts of the old browser-extension plan survive, and which are retired? | Avoid two conflicting plans. |
| J06 | How does the appy-basic Authenticate card hand off to the Authy index? | One source of truth. |
| J07 | Do MyFamily records get a routing.json entry and a fields manifest? | jsony/routing expectations. |
| J08 | What is the deprecation path for `tools/pending/sync-puzzy.py` and the parked checks? | Ties into the pending plan. |

---

## K · Browsy extension standards (2026-11-17)

> Decided in the main plan (`2026-11-17-appy-authy-mynet.md` §7d): the hash is
> the Nety PeerId, generation is hybrid (extension canonical, web provisional),
> and Nety v1 imports the same root. The questions below are the remaining
> standards for the extension.
>
> Session 1 (2026-11-17): Browsy **pulls** public pages on demand and mixes them
> with local content; pages do not query identity or vault. V1 targets
> Chrome/Edge + Firefox/Safari with the tweetnacl fallback. K02–K03 and K18 are
> narrowed by those answers.
>
> Session 2: pull failure shows typed states + retry; pull scope is the full
> DOM (redaction policy still open); consent is a persistent indicator + Stop +
> per-site allowlist.
>
> Session 3: full-DOM pull includes `input`/`textarea`/`select` values but
> excludes password/secret/hidden fields, cookies and tokens; v1 uses plain
> `chrome.storage.local` (vault in M2); there is no web→extension portability —
> the web identity is fallback/demo only.
>
> Session 4: a web demo is hidden but kept when the extension appears; the
> canonical record is `flove-identity/1`, with `flove-browsy/1` as a view; the
> same-root Nety transport is still open (K08).
>
> Session 5: v1 pulls only flove.org/localhost/127.0.0.1 (no `<all_urls>`, no
> `file://`); the web fallback is a full local identity with a warning,
> including mobile, and is not portable; recovery is a 12-word seed in v1.

| ID | Question | Why it matters |
|---|---|---|
| K01 | Is the extension the canonical identity host for every flove app, or only when installed? | Decides whether the web can create identities at all. |
| K02 | What is the exact internal contract for pull → suggest → render: inputs, outputs, errors and timeouts? | The current bridge only has stubs; pages must not become a vault API. |
| K03 | (Resolved) v1 pulls only flove.org/localhost/127.0.0.1; no `<all_urls>`, no `file://`. How is the origin allowlist maintained and audited? | Pulling is the main boundary; XSS on flove.org is the attack surface. |
| K04 | (Resolved) v1 uses plain `chrome.storage.local`; the encrypted vault is M2. Which unlock factor should M2 use? | Security vs delivery speed. |
| K05 | (Resolved) There is no web→extension portability; the web identity is fallback/demo only. What is its lifecycle? | Avoid implying a migration path that does not exist. |
| K06 | (Resolved) The web demo is hidden but kept; the extension hash is canonical. | One canonical hash per profile. |
| K07 | (Resolved) Canonical `flove-identity/1`; `flove-browsy/1` is a read-only view. What are the versioning and migration rules? | Appy, Authy and Nety must read the same record. |
| K08 | (Open) How does the root reach Nety: encrypted export, native messaging or seed phrase? How is the same PeerId verified? | Same identity without leaking the root. |
| K09 | What is the minimum manifest permission set for flove.org/localhost only (no `<all_urls>`, no `file://`)? | Over-broad permissions kill trust. |
| K10 | (Resolved) Without the extension, the web creates a full local identity with a warning, including mobile; `file://` uses the same fallback. | The extension cannot cover every context. |
| K11 | (Resolved) v1 uses a 12-word seed at creation; social quorum is later. Where is the seed stored/shown? | Loss and rotation are unsolved. |
| K12 | What does an app receive to act without the private key: session token, capability object or one-shot signature? What can it sign? | Authy sessions are still undefined. |
| K13 | What is the release standard: store, signed builds, reproducible, Firefox/Safari packaging? | Supply-chain and review risk. |
| K14 | What is redacted from a full-DOM pull and from logs: password fields, hidden inputs, keys, hashes, identity events? | Pulls and bug reports can leak P. |
| K15 | What is the local identity warning UX: text, expiry, upgrade prompt and deletion? | Users must understand a non-portable key store. |
| K16 | Can one root hold multiple profiles or masks, and how are they selected? | nety-frontend already has masks; Authy does not. |
| K17 | Is identity synced across devices: `chrome.storage.sync`, an encrypted file, or not in v1? | Multi-device changes the storage model. |
| K18 | What is the identity test matrix beyond browsers: installed/not installed, `file://`, storage blocked, locked service worker? | Acceptance must cover the fallbacks. |

## L · MyNet local groups (2026-11-17)

> The MyNet surface (people, favourites, groups, feed, invites, visibility,
> moderation) and the MyFamily-based local-group model are now in the main plan
> §3.4.1. These are the remaining product and consent questions.
>
> **Decided 2026-11-17:** L01 use **local group**; L02 owner/member only in v1;
> L04 **flat, no nesting/alias**; L05 **MyFamily 7×5 profile + 5 type
> percentages**, projection = display name + percentages; L07 multi-group yes;
> L10 **feed only**, chat deferred; L11 **no public groups in v1**; L14 MyFamily
> remains the person editor. **Still open:** L03, L06, L08, L09, L12, L13.
>
> **Answers 2026-11-18:** O01 A, O02 B, O03 A, O04 D, O08 P default,
> O10 A, O11 D, O12 B, O13 B, O15 A, O16 invite code + Telegram/Authy auth,
> O17 B, O18 A, O24 B, O25 entry/host labels, O26 A, O30 consult agreement.
> F1/F2/F4/F5 closed; F3/F6/F7 moved to §Pre-build pendings below.
> Closed log: [`pre-build/open-issues.md`](../../archive/old/browsy/pre-build/open-issues.md).
>
> **2026-11-18:** L03/L06/L08/L09 decided by O01–O04; L12/L13 moved to F3;
> subject consent is F6.

| ID | Question | Why it matters |
|---|---|---|
| L01 | Is the user-facing term “group”, “circle”, or both (group = circle with a name)? | The current Appy UI mixes “Groups” and “circle / group name”. |
| L02 | Which roles ship in v1: owner/member only, or owner/curator/member/guest? | Roles change the grant and removal model. |
| L03 | Can a person be added to a local group without their consent, and what does the invite show them? | A group profiles third people; ties to B02/B03. |
| L04 | Can groups nest or alias (family ⊂ close friends), or is membership flat? | Nesting affects projection and key inheritance. |
| L05 | Which MyFamily categories/traits are in the default group projection, and are the seven categories P until selected? | The projection is the privacy boundary. |
| L06 | Is the member list visible to members, or only to the owner? | The list itself leaks the local graph. |
| L07 | Can the same person be in several groups with different projections? | Assumed yes (BSP-M12), but the UI needs to explain it. |
| L08 | Who can invite or remove: owner only, or curators/members too? | Determines the signed action set. |
| L09 | On removal, is the old group history kept for the removed member, deleted, or re-encrypted? | Revocation is forward-only; copies remain. |
| L10 | Are group posts a feed, a chat, or both? Chat is a separate tab today. | Two different retention and consent models. |
| L11 | Can a public group be joined from an S card, or only by local invite? Who moderates it? | Nety moderation and discoverability. |
| L12 | What does group deletion/erasure propagate to member copies and invites? | Honest deletion limits. |
| L13 | Max members and size per group; what is the key-rotation cost with offline members? | Rotation can be expensive and asynchronous. |
| L14 | Does MyFamily remain the only person editor, or can MyNet create a simplified record inline? | The plan assumes MyFamily edits; the UI may want quick-add. |

### Questy session 1 — readout (2026-11-17)

Closed by the owner after 14 answers. The remaining questions stay open.

**Decided**

| Q | Decision |
|---|---|
| Q001 | Browsy pulls public pages on demand; pages do not query identity or vault. |
| Q002 | Pull failures show typed states `idle · pulling · no-access · error` + retry. |
| Q003 | Chrome/Edge use WebCrypto; Firefox/Safari use the tweetnacl fallback in v1. |
| Q004 | Pull scope is the full DOM, including forms and hidden fields. |
| Q005 | Persistent indicator + **Stop** + per-site allowlist; no silent pulls. |
| Q006 | Include normal `input`/`textarea`/`select` values; exclude password/secret/hidden fields, cookies and tokens. |
| Q007 | v1 stores keys in plain `chrome.storage.local`; encrypted vault is M2. |
| Q008 | No web→extension portability; the web identity is fallback/local. |
| Q009 | A web local identity is hidden but kept; the extension hash is canonical. |
| Q010 | Canonical `flove-identity/1`; `flove-browsy/1` is a read-only view. |
| Q012 | v1 pulls only flove.org/localhost/127.0.0.1; no `<all_urls>`, no `file://`. |
| Q013 | Without the extension, the web creates a full local identity with a warning, mobile included; still not portable. |
| Q014 | Recovery is a 12-word seed in v1; social quorum later. |

**Open**

| Item | Why it is still open |
|---|---|
| K08 / Q011 | How the root reaches Nety: encrypted export, native messaging or seed phrase. |
| K09 | Exact manifest permission set for the confirmed origin scope. |
| K12 / Q015 | App sessions: capability object, JWT or opaque handle. |
| K13 / Q016 | Release standard across Chrome/Edge, Firefox and Safari. |
| K14 / Q017 | Logging/redaction beyond the DOM pull rules. |
| K15 | Warning UX for a non-portable local key. |
| K16 / K17 / Q018 | Masks and cross-device sync. |
| K18 | Test matrix for installed/not, `file://`, storage blocked, locked worker. |

---

## Suggested survey order

1. **Batch 1:** A01, A03, A05 — the identity baseline.
2. **Batch 2:** B01, B03, B05 — third-party boundaries.
3. **Batch 3:** C01, C04, C06 — grant mechanics.
4. **Batch 4:** D01, D03, D05 — the local net.
5. **Batch 5:** E01, E03, E04 — derivation exposure.
6. **Batch 6:** F01, F02, F05 — Nety readiness.
7. **Batch 7:** G01, G02, G05 — vault and bridge.
8. **Batch 8:** H02, H04, H05 — usability of privacy.
9. **Batch 9:** I01, I03, I06 — legal/ethics.
10. **Batch 10:** J01, J03, J06 — integration.
11. **Batch 11:** L01, L03, L06 — MyNet groups, consent and member visibility.
12. **Batch 12:** F3, F6, Q5–Q7, Q9, Q14, Q19–Q23, Q27–Q29, Q31–Q32 — the moved pre-build pendings.

## Pre-build pendings — 2026-11-18

> Moved from `pre-build/open-issues.md`. Answer with letters A–D; ★ is a default.

### Q5 · O05 · What does group deletion propagate to member copies?
A. Local delete only; members keep copies.
B. ★ Send a signed tombstone; members delete cached group data; copies may
   remain and are labelled.
C. Rotate the key and archive; no delete.
D. Owner deletes; members keep everything.

**Answer (A–E):** ____

### Q6 · O06 · Max members and key rotation with offline members?
A. ★ 10 members; rotate on removal; offline members miss new posts until the
   next pull.
B. 50 members; rotate; queue updates for offline members.
C. No hard limit; best-effort rotation.
D. 10 members; no rotation until every member is online.

**Answer (A–E):** ____

### Q7 · O07 · Is the default group projection just the 5 percentages, or the raw 7×5 too?
A. ★ 5 percentages only; raw 7×5 is opt-in per group.
B. Raw 7×5 + percentages by default.
C. Per-area toggle: each area can be shared or hidden.
D. 5 percentages + a per-area dominant type.

**Answer (A–E):** ____

### Q9 · O09 · What is “disown”?
A. ★ Retire it from v1; keep `revoke` only.
B. Define it as a local reputation action (−10 local).
C. Move it to Nety later.
D. Keep it as a UI-only label with no data effect.

**Answer (A–E):** ____

---

### Q14 · O14 · What is an app session? (A05)
A. ★ Signed capability object, short TTL, scoped paths/actions.
B. JWT.
C. Opaque handle stored by Browsy.
D. One-shot signature per action.

**Answer (A–E):** ____

---

### Q19 · O19 · Offline queue?
A. ★ Extension queues; host forwards when the peer is back.
B. Host queues for offline peers.
C. No queue in v1.
D. Both queue.

**Answer (A–E):** ____

---

### Q20 · O20 · Page API allowlist?
A. Current list: status, read, save L record, list groups, feed, save L post,
   create invite.
B. ★ Read + save L records/posts; **groups and invites only in the extension
   UI**.
C. Read-only page API.
D. Full CRUD from the page.

**Answer (A–E):** ____

### Q21 · O21 · XSS boundary?
A. ★ L-only page API + user gesture for writes.
B. L-only, no gesture.
C. Read-only page API.
D. Full API with origin allowlist only.

**Answer (A–E):** ____

### Q22 · O22 · Panic/lock wipe scope?
A. ★ Wipe keys + session; records stay encrypted.
B. Wipe the whole vault.
C. Lock only, no wipe.
D. Configurable.

**Answer (A–E):** ____

### Q23 · O23 · Logs?
A. ★ Error codes only.
B. Redacted metadata.
C. Full logs by opt-in.
D. No logs.

**Answer (A–E):** ____

---

### Q27 · O27 · Default L grant TTL? (C06)
A. ★ 7 days.
B. 24 hours.
C. 30 days.
D. No expiry.

**Answer (A–E):** ____

### Q28 · O28 · Revocation key rotation? (C07)
A. ★ Rotate on every member removal.
B. Rotate manually.
C. Per-group key only.
D. No rotation.

**Answer (A–E):** ____

### Q29 · O29 · Is `copy` ever allowed? (C04)
A. ★ Never; every share is a reference + encrypted projection.
B. S only.
C. Allowed with a warning.
D. Allowed.

**Answer (A–E):** ____

---

### Q31 · O31 · When does the DPIA/privacy review happen?
A. ★ Before any L sharing.
B. Before S/Nety only.
C. After the MVP.
D. Not needed.

**Answer (A–E):** ____

### Q32 · O32 · What does erasure propagate?
A. ★ Signed tombstone + local delete; copies may remain and are labelled.
B. Local delete only.
C. No delete.
D. Re-encrypt everything.

**Answer (A–E):** ____

---

### F3 · O05/O06/O07 · Defaults under self-managed groups
No moderation, no public groups. Pick the v1 defaults:

A. Deletion: tombstone (O05-B); max 10 members/rotate (O06-A); projection 5
   percentages (O07-A).
B. Deletion: local only (O05-A); max 50/queue (O06-B); raw 7×5 by default (O07-B).
C. Deletion: archive/rotate (O05-C); no hard limit (O06-C); per-area toggle (O07-C).
D. Deletion: owner only (O05-D); no rotation (O06-D); percentages + dominant
   type (O07-D).

**Answer (A–D):** ____

### F6 · O30 · Agreement vs subject consent
The owner lets a member’s Wizy consult selected MyFamily data. Does the
**subject** (the person the record is about) also consent?

A. Owner-only agreement; no subject consent.
B. Owner agreement + subject consent for L/S sharing.
C. Subject consent only for S/Public; L is owner-only.
D. No third-person record sharing.

**Answer (A–D):** ____

<a id="questy-proposals"></a>
## Questy proposals (historical)

> Source: `development/wiki/archive/old/questy-proposals.md` (archived 2026-11-21).

> **Current task set (2026-11-20):** **1,455 live tasks + 805 archived**; see
> [`task-set-plan.md`](../../archive/old/task-set-plan.md). The counts below are historical and
> do not describe the current register.

> **Scope / Ámbito:** EN: Historical record of the questy skill proposals (P001–P009), all resolved. · ES: Registro histórico de las propuestas de questy (P001–P009), todas resueltas.

### P001 [resolved] Archive resolved items instead of deleting

**Source:** questy skill enhancement
**Status:** resolved
**Description:** When a user selects the "archive" option in the questy HTML survey, resolved items should be moved to an archive file instead of being deleted. This preserves history while keeping the main file clean.

**Resolution:** Implemented in SKILL.md — archive mode moves resolved items to archived-questions.md instead of deleting them. HTML toggle exists in Addons → Agents.md → archive.

**Date resolved:** 2026-07-27

### P002 [resolved] Addon row layout and Continue config

**Source:** questy HTML redesign
**Status:** resolved
**Description:** Restructure addons layout with Archive/Pro on left and Scripts on right. Move .github before HTML. Workflows only shown when Git is selected. Add Continue Addons Config button to show additional settings.

**Resolution:** Implemented — layout restructured, workflows conditional on Git, Continue button added with per-addon config fields.

**Date resolved:** 2026-07-27

### P003 [resolved] Info texts for Archive, Pro, Scripts

**Source:** questy UX enhancement
**Status:** resolved
**Description:** Show info texts when Archive, Pro, or Scripts are checked. One row per addon with X to hide. Info stays visible when collapsed.

**Resolution:** Implemented — addon-info-row elements with close button, shown on check, hidden on uncheck or X click.

**Date resolved:** 2026-07-27

### P004 [resolved] Human icon and use case button

**Source:** questy UX enhancement
**Status:** resolved
**Description:** Add human icon floating top right that shows humanized descriptions. Move Scripts to Continue config section. Add info button at bottom that generates use case narrative.

**Resolution:** Implemented — 👤 icon toggles human descriptions, Scripts in Continue config, ℹ button generates use case text based on selections.

**Date resolved:** 2026-07-27

### P005 [resolved] Scripts row layout and Demonstrative Use Cases

**Source:** questy UX enhancement
**Status:** resolved
**Description:** Rename Continue Addons Config to Scripts. Show scripts one per row with tech description on click. Convert ℹ button to option style, rename to Demonstrative Use Cases, request use case generation in prompt.

**Resolution:** Implemented — Scripts button shows script rows with expandable descriptions, Demonstrative Use Cases option triggers use case generation request in prompt.

**Date resolved:** 2026-07-27

---

> Consolidated 2026-08-01 from the older `debates/PROPOSALS.md` snapshot
> (deleted — this file is the single home for questy proposals).

### P006 [resolved] Move questy out of .agents/skills

**Source:** project structure cleanup
**Status:** resolved
**Description:** All questy files should live in visible project dirs, not hidden `~/.agents/skills/`.
**Resolution:** Moved out of `~/.agents/skills` into the visible flove tree. Final location (2026-08-01): `development/standards/skills/questy/` — skill (SKILL.md), web app (index.html, crowd-questy.html, tour.html), and shared assets (presets/, templates/) together as one real copy, loaded via the `~/.agents/skills` symlink. `~/.agents/skills/questy/` removed.
**Date resolved:** 2026-07-28

### P007 [resolved] Consolidate questy-html

**Source:** project structure cleanup
**Status:** resolved
**Description:** Two questy-html files existed separately. Consolidate into tools/questy-html/ folder.
**Resolution:** Consolidated at `development/standards/skills/questy-html/` with SKILL.md, README.md, questy-html-flove.md, DESIGN-questy-html.md, gen-feeds.js, template.html, template123.html. Old pointer SKILL.md and `central/questy/tools/questy-html/` removed (2026-08-01).
**Date resolved:** 2026-07-28

### P008 [resolved] standards.md for questy

**Description:** Create questy's own development standards (official routes, rules, error handling, version format, preset authoring guide).
**Resolution:** Created at `development/wiki/archive/old/standards.md`. Expanded with error handling, version/changelog, preset authoring, commands reference, proposals format.

### P009 [resolved] Tour HTML

**Description:** Create professional 5-slide graphical tour explaining why/what/how questy works.
**Resolution:** Created at `development/standards/skills/questy/tour.html`. 5 slides (problem, solution, system, workflow, get started), keyboard nav, dark theme.

### Conflict resolution — skill standard vs HTML form

#### Naming (resolved)

| # | Area | Decision |
|---|------|----------|
| 1 | Types | **Words only** — vision, arch, trust, data, integration (no colors) |
| 2 | Hats yellow | **optimism** (not vision) |
| 3 | Hats blue | **make** (not process) |
| 4 | Lens type | **Removed** — not in KISS |
| 5 | Agents.md naming | **Current technical names** (shortcuts, constraints, etc.) |

#### Structure (resolved)

| # | Area | Decision |
|---|------|----------|
| 6 | File count question | **Not needed** — routes field covers it |
| 7 | Resume flow | **Not needed** — will add later if needed |
| 8 | Addons naming | **Keep both** — skill uses folders, form uses addons |
| 9 | Workflows | **Added to skill** — full section |
| 10 | PR standards | **Added to skill** — full section |

#### Agents.md (resolved)

| # | Area | Decision |
|---|------|----------|
| 11-14 | Existing sections | **Keep** — shortcuts, constraints, pending-resolutions, decision-log |
| 15-21 | New sections | **Added** — batch-overrides, export-prefs, territory, aliases, danger zone, archive |

### Deferred

| # | Area | Decision |
|---|------|----------|
| 1 | questy-html progress indicator | Defer — implement when questy-html is active |
| 2 | questy-html save/load state | Defer — localStorage already handles this |
| 3 | Multi-user scenarios | Defer — not needed yet |
| 4 | Error recovery for malformed config | Deferred — fallback to defaults works for now |

### Q061–Q090 — hitos y estándares (2026-11-20)

Thirty decisions on the milestone tracker and the standard/checker map. The
canonical register is [`milestones.json`](../../archive/old/milestones.json); the agent-facing
detail of the execution policy is [`development/AGENTS.md`](https://flove.org/development/AGENTS.md),
indexed in [`../README.md#procedures`](https://flove.org/development/standards/README.md#procedures).

**Later move (2026-11-21):** the PROC policy itself moved out of `milestones.json`
into `development/AGENTS.md`; the JSON block was retired and both projections are
regenerated from the Markdown source. The Q062 row below records the earlier state.

| Range | Decision carried into the files |
|-------|---------------------------------|
| Q061 | `depends_on` stays optional — a hito may stand alone. |
| Q062–Q064 · Q068 · Q071 · Q076 · Q079–Q082 | `procedures` is one root roadmap execution policy (`id · title · standard · checker · advice · inputs · outputs · gates`) in `milestones.json`; `standards/README.md` owns its mirror and the one checker map. |
| Q065–Q067 · Q075 · Q085 | Section URLs keep anchors, derived from MD headings by the wiki slug rule and verified by both validators. |
| Q069 · Q070 · Q073 · Q078 · Q083 | Hito-level `skill:stage` arrays are gone; their URLs folded into `standards[]`. Q070/Q078 closed by Q083; Q077 closed by Q076. |
| Q074 · Q087 | Each of the 60 top hitos has one section-specific acceptance sentence. |
| Q088 | Frontend Advanced/Super stay `todo` until the UX01 evidence pass. |
| Q089 | Builder and `check-skills.py` fail on missing fields, bad anchors, duplicate owners and stale hito fields. |
| Q090 | Decisions applied; Q084 later closed with three added policy fields (inputs, outputs, gates). |


### Q091–Q120 — hitos, tasks y stage (2026-11-20)

Thirty questions on milestone identity, evidence, vocabulary and tasks.
Decisions are applied additively to [`milestones.json`](../../archive/old/milestones.json);
the old keys stay as mirrors until the page code is migrated (see tasks below).

| Q | Decision |
|---|----------|
| Q091 | One opaque id per hito; `ticket` becomes a group label and dependencies use the id. |
| Q092 | The UX01 table drives `todo → part → on`; evidence means app + section + gap. |
| Q093 | The 1–5 ladder becomes an explicit field on every hito. |
| Q094 | The value protected is the done-criterion per section. |
| Q095 | Work must show state and evidence in the same row. |
| Q096 | Debate tickets are generators, not hitos (free answer corrected the premise: S1 ≠ F3). |
| Q097 | Rename fields, keep structure: `phase→stage`, `axes→sections`, `boxes→subsections`; 425 items unchanged. |
| Q098 | `state` belongs to the task; the hito derives it from its tasks. |
| Q099 | *Hecho · fácil · difícil* classifies tasks only; hitos keep the 1–5 ladder. |
| Q100 | Every hito must have tasks; dependencies are separate and free per item. |
| Q101 | No need to tell debates / plans / pendings apart — only task effort matters. |
| Q102 | Colours: green = hecha, yellow = fácil, red = difícil. |
| Q103 | Dependencies go task → task, with no inheritance from the hito. |
| Q104 | The hito row shows a counter (`2/3 hechas`), not a traffic light. |
| Q105 | Hitos are task containers; refine the hitos themselves in a later questy before generating more tasks. |
| Q106 | Closed 2026-11-20 — the "2" was option B: the first three roadmap stages, now `seed · infant · mature`. |
| Q107 | A hito groups ≥2 tasks; a single action is reclassified as a task. |
| Q108 / Q110 | `optimizy` generates the evidence and writes it into the task; the 18-row table is its mirror. |
| Q109 / Q114 | One field called `stage`, values `seed · infant · mature · grown · full`; `degree`, `phase` and "etapa" are retired. |
| Q111 | Closed 2026-11-20 by the owner — confirmed option B of Q106, so 945 tasks (3 per hito) stand. |
| Q112 / Q113 | Dismissed; regenerated as Q115 / Q119. |
| Q115 | Closed 2026-11-20 — one `stage` scale, no type discriminator. Subsections are the filter/list unit and are treated as sections via the `section` field. |
| Q116 | Short id `<section>-<n>` (e.g. `map-01`). |
| Q117 / Q118 | Q084 was closed later: `inputs` / `outputs` / `gates` were added to the six PROC. |
| Q119 | Audit coherence: every hito has a coherent structure and associated tasks; flag single-action rows. |
| Q120 | Apply all resolutions to the documents and list easy follow-ups. |

**Applied to `milestones.json`:** 315 opaque ids, 315 `stage` values, 945 tasks
(3 per hito: `seed · infant · mature`), 124 dependencies rewritten to ids, 99 rows
flagged `needs_split: true` for the refining questy. `new_tickets[]` gained a
`stage` alias of `phase`. The builder now rejects a hito without id, stage,
coherent tasks or optimizy evidence.

**Open items carried forward:** none from Q091–Q120.
**Closed afterwards:** Q084 (inputs/outputs/gates added to the six PROC), Q106/Q111
(confirmed as seed · infant · mature), Q105/Q119 (the 99 `needs_split` rows were split
into concrete stage tasks and cleared), Q115 (one `stage` scale; subsections filter and
list as sections), and the code migration of `axes→sections` / `boxes→subsections` in
builder and page.

#### Follow-ups applied (2026-11-20)

1. `axes → sections`, `boxes → subsections` and `axis → section` in `milestones.json`, the builder and the page JSON reader; 425 items and `--check` counts unchanged.
2. `degreeLadder → stageNames` with `seed · infant · mature · grown · full`; Raw…Super labels retired from the embedded JSON and the Prose.
3. Work rows show a `<done>/<total>` task counter (Q104) with an expandable task list (Q102/Q110).
4. ~~Task chips carry green = *hecha*, yellow = *fácil*, red = *difícil* (Q102); no new column.~~ **Superseded by Q123/Q124:** colour is effort (green/yellow/red); `✓` marks `hecha`.
5. Expanding a row shows app · section · gap from `optimizy` evidence (Q113), with an explicit empty state while the arrays are unfilled. *(Evidence display still holds; the old colour note in item 4 does not.)*
6. ~~A `needs_split` filter chip exposes the group; the canonical `groups[]` keeps it.~~ **Superseded by Q152:** the retired chip was replaced by `Estado de tareas / Task state`; the 99 flagged hitos were cleared in item 11.
7. Stage equivalence F1–F5 → seed…full published in `plans/index.md`.
8. Q106/Q111 closed by the owner: the "2" was option B, so 945 tasks in `seed · infant · mature` stand.
9. `hitos-audit.md` carries the per-section refinement plan and its executed result.
10. One sr-only bilingual `<h1>` added; the static a11y gate is now clean.
11. The 99 flagged hitos were split into concrete stage tasks — `define locally` ·
    `apply in the basic flow` · `publish in the canonical index` — all three marked
    `fácil`; every hito now has `needs_split: false`, and 315/945 counts are intact.
12. Q084 closed: the six PROC gained `inputs`, `outputs` and `gates`; the builder
    validates all eight fields.
13. ~~The `needs_split` chip sorts the flagged value ahead of `ready`.~~ **Superseded by Q152:** the chip no longer exists; the task-state chips use the canonical `hecha · fácil · difícil · muy difícil` order.
14. Q115 closed: counting stays on one `stage` scale; Work and Docs · Plan keep
    filtering and listing by subsection (`section` field), treated as section values.
15. Degree-card milestones carry the same `x/y hechas` counter as the Work table.
16. The Stage filter shows canonical `seed (F1) … full (F5)` names; `check.js`
    guards the sr-only `<h1>` against regression.

### Q121–Q141 · conflictos, orden y procedures (2026-11-20)

Config: 30 questions (Q121–Q150), batches of 3, six hats, simple + ★, no extra
lenses, no audio. Asked so far: Q121–Q141.

| Q | Decisión |
|---|----------|
| Q121 | Cerrada por Q133: «nivel» era sinónimo de stage; se ignoran los números. |
| Q122 | Sin respuesta directa; reformulada y cerrada como Q134. |
| Q123 | Escala de esfuerzo de tres valores: `fácil · difícil · muy difícil`. |
| Q124 | Color = esfuerzo (verde/amarillo/rojo); `✓` marca `hecha`, independiente del color. |
| Q125 | Sin respuesta directa; reformulada y cerrada como Q134. |
| Q126 | El valor se deriva de los dependientes del hito (0–1 fácil, 2 difícil, ≥3 muy difícil) y se aplica solo a la task `mature`. |
| Q127 | Cola: desbloqueantes primero, luego fáciles; el `stage` no ordena la ejecución. |
| Q128 | El registro de conflictos vive en `hitos-audit.md`. |
| Q129 | Éxito = menos retrabajo: no empezar un dependiente antes de su prerrequisito. |
| Q130 | C6 se registra como excepción; no se cambian estados ni aristas. |
| Q131 / Q135 | Fusionar `contracts-04` + `quality-02`; sobrevive `contracts-04`. |
| Q132 | La sección de Procedure va en `standards/README.md` más una entrada PROC-07. |
| Q133 | «Nivel» era sinónimo: crear tasks generalistas derivadas de los hitos `grown`/`full`. |
| Q134 | Fusionar los tres duplicados en `work-15`. |
| Q136 | Una task generalista por hito, con el `stage` del hito. |
| Q137 / Q140 | PROC-07 es recomendación, no gate duro: si hay ciclo, avisar y seguir. |
| Q138 | Tabla de conflictos con tres columnas: ID · Conflicto · Decisión. |
| Q139 | Las tasks nuevas son `difícil` (o `muy difícil` con ≥3 dependientes), con dependencias task→task derivadas del hito. Las 124 aristas hito→hito quedan reflejadas en las tasks de valoración (`.3`/`.4`), sin ciclos. |
| Q141 | El desplegable de tasks del Work sigue la cola de Q127. |

**Efecto en datos:** 312 hitos, 1012 tasks (76 generalistas), 7 PROC,
422 features y `--check` en verde. Q121–Q141 cerradas (Q122/Q125 vía Q134);
la continuación Q142–Q150 está registrada en la sección siguiente.

### Q142–Q150 · cierre de la sesión (2026-11-20)

Config heredada de Q121: 30 preguntas, tandas de 3, seis sombreros, simple + ★,
sin lentes extra, sin audio. Q148b corrige una premisa errónea de Q146.

| Q | Decisión |
|---|----------|
| Q142 | Sin respuesta útil: el usuario confundió `ticket` con tasks; reformulada como Q145. |
| Q143 | `--check` avisa de ciclos task→task como warning no bloqueante, según Q140. |
| Q144 | No mostrar `unlocks=N` en el detalle de Work; el orden de Q141 basta. |
| Q145 | Quitar el campo `ticket` de los 312 hitos; el id opaco es la única clave. Los 33 tickets de debate conservan el suyo. |
| Q146 | El usuario pidió explicar `keep` antes de decidir; respondido en Q148. |
| Q147 | No publicar la cifra de 11 tasks que desbloquean 36 aristas; queda como principio, no como métrica. |
| Q148 | «Quitar `keep`», revocada por Q148b al descubrir que es load-bearing. |
| Q148b | Conservar `keep` y documentarlo: 127 `true` → `feature / stage-matrix / production`, 185 `false` → `question / debate / plansdebates`. |
| Q149 | Añadir guarda de igualdad `state_mirror == state` en el builder. |
| Q150 | Puntero de una línea en `debates/INDEX.md` a `README.md#task-order-proc-07` y cierre del log. |

**Estado final:** 312 hitos · 1012 tasks · 124 dependencias hito→hito y sus
124 espejos task→task · 7 PROC · 422 features. Gates verdes: builder `--check`,
`check.js`, `check-skills.py` (0/0) y a11y. Sin commit. Q121–Q150 cerradas
(Q122/Q125 vía Q134, Q142 vía Q145, Q148 vía Q148b).

**Mantenimiento posterior:** dos guardas nuevas en `--check` (ningún
`needs_split` pendiente y aviso si C6 deja de tener 7 inversiones), bloque
«Verificar el Work» en `README.md` con los gates permitidos, puntero en
`plans/index.md` y seis pruebas negativas sobre copias temporales: effort
inválido, dependencia task colgante, `state_mirror` roto y `needs_split`
activo fallan con mensaje propio; los ciclos task→task y un C6 con 8
inversiones solo avisan. El skill externo no rastreado `jev/` se movió a
`/tmp/opencode/jev-external` para recuperar los 18 skills canónicos.

### Q151–Q153 · corrección de la auditoría y filtros del Work (2026-11-20)

| Q | Decisión |
|---|----------|
| Q151 | La auditoría no puede usar las subsecciones de `docs` para todas las secciones: cada sección tiene sus propios campos (`docs`→map/plan/work; `backend`→contracts/delivery/storage/systems; `frontend`→a11y/levels/quality/shell/tours/tree/types/visual; `ai`→flows/levels/models/skills; `data`→index/json/mds/schemas; `community`→channels/docs/feedback/language/levels). `hitos-audit.md` regenera la tabla campo→tasks desde `milestones.json`: 28 campos, 312 hitos, 1012 tasks (903/98/11 esfuerzo, 345/19/648 estado). Los ids inventados (`docs-01` bajo `community`) desaparecen; `levels` son tres campos distintos (`levels-01`/`levels-15`/`levels-20`). |
| Q152 | En Work se elimina el filtro «Por dividir / Needs split» (`needs_split`, vacío desde Q119) y se sustituye por «Estado de tareas / Task state» con `hecha · fácil · difícil · muy difícil`. Cada feature deriva `taskcat` de las `state`/`effort` de sus tasks; el filtro usa OR sobre las tasks del hito (115 hitos con `hecha`, 312 `fácil`, 98 `difícil`, 11 `muy difícil`). |
| Q153 | Se documenta el cambio en README y se regenera el tracker. Gates verdes: `--check` (422 features, 14 grupos), `check.js`, `check-skills.py` (0/0) y a11y. Sin commit. |

### Q154 · registro de `jev` y cierre de lote (2026-11-20)

| Q | Decisión |
|---|----------|
| Q154 | Se registra el skill externo `jev` — antes en `/tmp/opencode/jev-external` — en `development/standards/skills/jev/`: categoría `utility`, H1 `# jev`, trigger `Use for`, cuerpo comprimido a ~700 palabras y 5 referencias planas enlazadas por URL de flove.org (sin carpeta `references/`). Contadores 18→19 skills y `utility` 2→3 en builder, chips y README. Gates verdes: `--check`, `check.js`, `check-skills.py` (0/0) y a11y. Sin commit. |

### Q155 · `/optimizy3` sobre `development/index.html` (2026-11-20)

| Q | Decisión |
|---|----------|
| Q155.1 | Nivel 1: `html-validate` pasa de 2 errores a 0 — se retira un `style=` redundante del SVG y el `aria-label` inválido del contenedor `#work-tabs`. El menú devuelve el foco a `#brand-map` al cerrar con Esc. Muros load-bearing verificados antes y después: `:has(#lang-en:checked)` (795–796), pares `for=`/`id=` de idioma, `#work-data` y `hashchange`. Sin refactor ni reformato. |
| Q155.2 | Nivel 2: `export` = N/A (índice de documentación, sin retrato ni modelo de usuario); `texty` sin cambios de nombre; `translaty` ya en 100 % en/es. No se tocó `routing.json`, `APP_ROUTING` ni envelopes → `jsony` = N/A. |
| Q155.3 | Nivel 3 contra [§13.18](https://flove.org/development/standards/frontend/frontend.md#1318-usability-levels-3-minimum-4-function-5-craft) (la matriz vive allí, no se copia): se corrigen los huecos reales de `States` y `Language` — estado vacío de Work bilingüe y accionable vía «Limpiar» (5 call sites → `emptyMsg()`), `Fase/Stage` y los `aria-label`/placeholder de la barra de Work con pares en/es. Tour, Summary, Export/share, Publish, Counters y Locking = N/A en una página de docs; Metadata sin OG = N/A (los índices de desarrollo no comparten tarjeta, coherente con `standards/index.html`); Google Fonts = mejora progresiva con fallback `system-ui`, patrón de todo el sitio. |
| Q155.4 | Gates finales: `html-validate` 0 errores, `check.js` en/es 100 %, builder `--check` 422 features/14 grupos, `check-skills.py` 0/0, a11y limpio. Filtro `taskcat` verificado (115/312/98/11). Sin commit. |

### Q156 · `/optimizy4` sobre `development/index.html` (2026-11-20)

| Q | Decisión |
|---|----------|
| Q156.1 | `Theme` (nivel 4): el `<head>` aplica antes del primer paint la preferencia guardada o, si no hay, `prefers-color-scheme: light`; `applyTheme(light, persist)` no escribe `flove:theme` cuando el valor viene del sistema, así que un cambio del SO se sigue respetando. El toggle explícito sí persiste. Sin flash y con `meta[color-scheme]` sincronizado. |
| Q156.2 | `Counters`/`Language`: la tira generada por `updateStrip()` estaba solo en inglés (`rows`, `Planned`, `View in tracker ↓`); ahora usa `degText` en/es como el resto del Work. `Metadata`: se añade `rel=canonical`; la tarjeta OG sigue siendo N/A en índices de desarrollo, coherente con `standards/index.html`. |
| Q156.3 | Nivel 4 N/A en esta página de docs: PWA/cached shell (no reclama instalación; `sw.js` queda para `updaty4`), Tour, Summary, Export/share, formularios largos con autosave/undo, reset destructivo, offline notice y Publish. `Identity`, `Menu`, `Navigation` (6 pestañas + `hashchange` + `replaceState`), `Compass` (las pestañas principales) y `States` ya cumplen sin cambios. |
| Q156.4 | Gates: `html-validate` 0, `check.js` 100 % en/es, builder 422/14, `check-skills.py` 0/0, a11y limpio. Sin commit. |

<a id="questy-standards"></a>
## Questy project standards

> Source: `development/wiki/archive/old/standards.md` (archived 2026-11-21).

Official routes and development rules for the questy skill itself.

### Paths

- `SKILL.md` — main skill definition (single source of truth)
- `presets/` — project-specific config overrides
- `tools/` — companion docs (questy-html.md, etc.)
- `proposals.md` — internal dev history (kept as-is, not cleaned)
- `~/.config/questy/config.md` — user's active config
- `~/.config/questy/overrides.md` — personal behavior overwrites

### Frontend

- URL: `https://flove.org/questy/`
- Source: `development/standards/skills/questy/index.html`
- Single-file HTML/CSS/JS, no build step
- State persisted in localStorage (`questy-state`)
- Mode format: `modeRadio` (simple|explained) + `numbered` (boolean checkbox)

### What questy creates for other projects

When tree addon selected, questy creates:
- `docs/`, `plans/`, `standards/` folders
- `pendings.md`, `conflicts.md`, `proposals.md`, `archive.md` files
- `agents.md`, `.gitignore`, `.github/`, `docs/adr/`, `scripts/` (if selected)

### Rules

- SKILL.md is the single source of truth — HTML form must match it
- Presets override doc-roots and extra-files, not the other way around
- Extra-files are NOT read by default — only when the addon that creates them is selected
- session.md does not exist — user manages their own files
- Config has no required fields — copy whatever is filled
- HTML form is the config builder, not the skill entrance
- Skill entrance is 4 steps: purpose → hats → volume → details

### Error handling & fallbacks

- **Missing doc-roots:** If a configured path doesn't exist, skip it silently — don't error. Warn once, continue with what exists.
- **Malformed config.md:** If config can't be parsed, fall back to SKILL.md defaults. Don't ask the user to fix it — just use defaults for that session.
- **Missing extra-files:** If an extra-file (pendings.md, conflicts.md) doesn't exist, don't create it automatically. Only create when the addon that generates it is selected.
- **No presets matched:** If `/questy {name}` doesn't match any preset file, treat `{name}` as a project name and use defaults.
- **Empty doc-roots:** If no doc-roots are configured, scan the current working directory for .md files as a fallback.
- **Talk2web not installed:** Generate static HTML as fallback. Don't block the session.

### Version & changelog

- Current version: 1.0.0
- Changelog lives in `proposals.md` (internal dev history)
- Version bump when: new addon, new mode, breaking config change, new preset
- Version format: semver (major.minor.patch)

### Authoring presets

To create a new preset:
1. Create `presets/{name}.md` in the questy skill directory
2. Use this template:
```markdown
# questy preset — {name}

## paths
- doc-roots: ../path1/, ../path2/
- extra-files: ../

## preferences
- prefer 🟥 heart questions
- batch size: 4
- mode: numbered+explained

## constraints
- don't touch standards/ — those are frozen
```
3. The first argument after `/questy` matches against preset filenames (case-insensitive)
4. Presets override `doc-roots` and `extra-files` from config.md

### Commands reference

- `c` or `continue` — next batch
- `more {hat}` — generate more questions with that hat (e.g. `more red`, `more green`)
- `update` — re-scan docs for new gaps
- `stop` — end session, offer export
- Numbers (e.g. `1,4,7`) — answer questions by global number
- Letters (e.g. `a,b`) — answer within a single question's options

### Proposals format

User-facing proposals (in `proposals.md`) follow this schema:
```markdown
### P{NNN} — {title}
- **status:** active | resolved | deferred
- **source:** {where it came from}
- **description:** {what and why}
- **resolution:** {how it was resolved} (if resolved)
- **date:** YYYY-MM-DD
```

<a id="questy-usecase"></a>
## Questy advanced use case

> Source: `development/wiki/archive/old/UseCase-adv.md` (archived 2026-11-21).

All perspectives + all addons + all workflows + all scripts + all integrations.
Two parallel tracks: **HTML form** (left) and **console prompt** (right).

For each step: what questy does, what it asks, and how the user responds.

> **Type policy (2026)**: questy's type is the **Thinking Hats** — facts ·
> heart · risk · optimism · creative · make. The KISS catalogue (vision/arch/
> trust/data/integration) is deprecated and only kept here as the legacy steps
> below; anywhere the live skill runs, hats are the only type. Steps 21–31
> describing `vision/arch/…` read as the older console tracking they replaced.

---

### Phase 1 — Config check & setup (steps 1–12)

| # | What questy does | HTML form | Console prompt |
|---|-----------------|-----------|----------------|
| 1 | Check ~/.config/questy/config.md | Skip setup, load saved config | `/questy new-project` |
| 2 | If missing: ask setup mode | Present [1] HTML form [2] Console [3] Modal | `No config found. Setup? (1/2/3)` |
| 3 | User picks HTML form | Open flove.org/questy/ in browser | `2` → console mode |
| 4 | Prompt: Project name | [Project name...] input | `Q1: Project name? → new-project` |
| 5 | Prompt: Type | [docs] [code] [mixed] buttons | `Q2: Type? [1]code [2]docs [3]mixed → 3` |
| 6 | Prompt: State | Nowadays it's [Ok] [Messy] | `Q3: State? [1]fresh [2]ok [3]messy → 2` |
| 7 | Detect doc-roots | [Route(s)] text input | `Q4: Doc roots? → ./docs/, ./src/` |
| 8 | Validate config | No required fields, copy whatever filled | Config stored as markdown |
| 9 | Fallback check | If malformed → SKILL.md defaults | `Config parse error, using defaults` |
| 10 | Save config | Writes ~/.config/questy/config.md | Saved automatically |
| 11 | Batch mode check | + button for multi-project | `Batch mode? (y/N)` |
| 12 | Load defaults | type = the six Thinking Hats (facts/heart/risk/optimism/create/make), batch: 5, per-type: 5 | Defaults loaded |

### Phase 2 — Project context (steps 13–20)

| # | What questy does | HTML form | Console prompt |
|---|-----------------|-----------|----------------|
| 13 | Set active workflow | It's about [docs] [code] selector | `Workflow: code + docs` |
| 14 | Detect existing git | Scans .git in project dir | `.git found → synced workflow available` |
| 15 | Confirm extra-files path | Text input for extra session | `Extra doc roots? (optional)` |
| 16 | Map file territory | Standards/ → principles, Plans/ → proposals, Docs/ → reference | `Found: 3 standards, 2 plans, 5 docs` |
| 17 | Detect pendings.md | Check if exists from previous session | `Pending items from last session: 2` |
| 18 | Detect conflicts.md | Check if exists | `Open conflicts: 1 (plan-vs-standard)` |
| 19 | Detect proposals.md | Check if exists | `Proposals: 3 active, 1 resolved` |
| 20 | Session resume check | "What changed since last time?" | `What changed since last session? (text)` |

### Phase 3 — Perspective: the Thinking Hats as type (steps 21–48)

| # | What questy does | HTML form | Console prompt |
|---|-----------------|-----------|----------------|
| 21 | Show the Thinking Hats (the type) | [facts] [heart] [risk] [optimism] [creative] [make] | `Q8: Hats? [1]white [2]red [3]black [4]yellow [5]green [6]blue` |
| 22 | User selects vision | Click once → selected, twice → x2 weight | `1, 1 again → weighted` |
| 23 | Questy notes vision scope | What is this? Who for? Why? Others? Blind spots? | `vision active, weight: 2` |
| 24 | User selects arch | Same click pattern | `2 → arch active` |
| 25 | Questy notes arch scope | Component boundaries, data flow, scope, blind spots | `arch active` |
| 26 | User selects trust | Click | `3 → trust active` |
| 27 | Questy notes trust scope | Threat model, privacy, edge cases, recovery | `trust active` |
| 28 | User selects data | Click | `4 → data active` |
| 29 | Questy notes data scope | Structure, relationships, lifecycle, retention | `data active` |
| 30 | User selects integration | Click twice → x2 weight | `5, 5 → weighted` |
| 31 | Questy notes integration scope | A↔B contract, boundary failure, protocol, sync | `integration active, weight: 2` |
| 32 | Show rainbow hats | [white] [red] [black] [yellow] [green] [blue] | `Q9: Hats? [1]facts [2]heart [3]risk [4]optimism [5]creative [6]make` |
| 33 | User selects ⬜ white/facts | Click | `1 → facts` |
| 34 | ⬜ white explanation | What do we know? Data? Specs? What's missing? | `facts: data-proven questions` |
| 35 | User selects 🟥 red/heart | Click twice → x2 | `2, 2 → heart (weighted)` |
| 36 | 🟥 red explanation | How does it feel? User fear? Trust? | `heart: feeling + trust questions` |
| 37 | User selects ⬛ black/risk | Click | `3 → risk` |
| 38 | ⬛ black explanation | What could go wrong? Threats? Blast radius? | `risk: threat + failure questions` |
| 39 | User selects 🟨 yellow/optimism | Click | `4 → optimism` |
| 40 | 🟨 yellow explanation | Benefits? Value? Why build? User gain? | `optimism: value + benefit questions` |
| 41 | User selects 🟩 green/creative | Click | `5 → creative` |
| 42 | 🟩 green explanation | Alternatives? Wild ideas? Flipped perspective? | `creative: alternative + novel questions` |
| 43 | User selects 🟦 blue/make | Click | `6 → make` |
| 44 | 🟦 blue explanation | Flow? Connection? Contract? How A↔B? | `make: process + contract questions` |
| 45 | Show Wisy lenses | Explainers / Formalise / Tone / Teleology / Field / Time span | `Q10: Extended perspectives? (multiselect)` |
| 46 | Explainers (7) | [why] [what] [how] [what-for] [who] [where] [when] | `1-7: explainers selected` |
| 47 | Formalise (5) | [axiom] [evidence] [prediction] [proposal] [challenge] | `8-12: formalise selected` |
| 48 | Tone (4) + Teleology (4) + Field (5) + Time span (7) | Each multiselect | `13-33: all lenses configured` |

### Phase 4 — Addons: Core + Scripts + Integrations (steps 49–68)

| # | What questy does | HTML form | Console prompt |
|---|-----------------|-----------|----------------|
| 49 | Show core addons | [index] [agents] [tree] [git] [html] [.github/] [archive] [pro] [scripts] | `Q11: Addons? [1]index [2]agents [3]tree [4]git [5]html [6].github [7]archive [8]pro [9]scripts` |
| 50 | User selects tree | Click → creates docs/, plans/, standards/, pendings.md, conflicts.md, proposals.md | `3 → tree addon` |
| 51 | User selects index | Click → generates README.md | `1 → index addon` |
| 52 | User selects agents | Click → creates agents.md | `2 → agents addon` |
| 53 | User selects git | Click → .gitignore + repo sync | `4 → git addon` |
| 54 | User selects html | Click → web output, questy-html preview | `5 → html addon` |
| 55 | User selects .github/ | Click → issue/PR templates | `6 → github addon` |
| 56 | User selects archive | Click → archive.md for resolved items | `7 → archive addon` |
| 57 | User selects pro | Click → docs/adr/ folder | `8 → pro addon` |
| 58 | User selects scripts | Click → scripts/ folder | `9 → scripts addon` |
| 59 | Show script options | [build] [test] [deploy] [lint] [format] [typecheck] [docker] [audit] [benchmark] [docs] [release] [deps] | `Q15: Scripts? (multiselect from 12)` |
| 60 | User selects build+test+lint+format | Click each | `1,2,4,5 → build+test+lint+format` |
| 61 | User selects deploy+docs+release | Click | `3,10,11 → deploy+docs+release` |
| 62 | Show integrations | [tickets] [board] [linear] [notify] [pulse] | `Q16: Integrations? (multiselect)` |
| 63 | User selects tickets+board | Click | `1,2 → tickets+board` |
| 64 | Show agents.md sections | [shortcuts] [constraints] [pending-resolutions] [batch-overrides] [export-prefs] [territory] [aliases] [danger-zone] [decision-log] [archive] | `Q14: Agents.md options?` |
| 65 | User selects shortcuts+constraints+territory | Click | `1,2,6 → selected` |
| 66 | Show workflow options | [synced] [merge rules] [commit guard] [finish line] [blueprint] | `Q12: Workflows?` |
| 67 | User selects synced (git prerequisite) | Click (only if git selected) | `1 → synced workflow` |
| 68 | User selects merge rules | Click → opens PR standards sub-options | `2 → merge rules` |

### Phase 5 — Workflows & PR Standards (steps 69–80)

| # | What questy does | HTML form | Console prompt |
|---|-----------------|-----------|----------------|
| 69 | Show PR title format | [conventional] [ticket-number] [branch-name] | `Q13a: Title format? [1]conv [2]ticket [3]branch → 1` |
| 70 | Title → conventional | Selected | `conventional commits` |
| 71 | Show description template | [basic] [detailed] [none] | `Q13b: Description? [1]basic [2]detailed [3]none → 2` |
| 72 | Description → detailed | Selected | `detailed PR description` |
| 73 | Show review checklist | [code quality] [tests pass] [docs updated] [no breaking] [screenshot] | `Q13c: Checklist? (multiselect) → 1,2,3` |
| 74 | Checklist items → 3 selected | Click | `code+tests+docs` |
| 75 | Show merge strategy | [squash] [merge-commit] [rebase] | `Q13d: Merge? [1]squash [2]merge [3]rebase → 1` |
| 76 | Merge → squash | Selected | `squash commits` |
| 77 | Show branch naming | [feature/ticket] [feature/description] [none] | `Q13e: Branch? → 1` |
| 78 | Branch → feature/ticket | Selected | `feature/TICKET-123` |
| 79 | Show commit format | [conventional] [imperative] [none] | `Q13f: Commit? → 1` |
| 80 | Commit → conventional | Selected | `feat: conventional format` |

### Phase 6 — Output & export (steps 81–88)

| # | What questy does | HTML form | Console prompt |
|---|-----------------|-----------|----------------|
| 81 | Show output formats | [story] [data dump] [spreadsheet] [notion sync] [obsidian vault] | `Q17: Output? (multiselect)` |
| 82 | User selects story | Click → narrative format | `1 → story output` |
| 83 | User selects data dump | Click → raw JSON/MD | `2 → data dump` |
| 84 | Check questy-html | If installed → offer live preview | `questy-html found. Render as HTML?` |
| 85 | Fallback | If not installed → static HTML | `questy-html not found. Static HTML?` |
| 86 | Check skill integration | [validaty] [optimizy] [translaty] [exporty] | `Post-questy: run /validaty? /optimizy?` |
| 87 | Offer skill chain | Only installed skills shown | `Skipping — no installed skills` |
| 88 | Final config review | "Save Config" button / "Copy Prompt" | `Config complete. Save? (y/N)` |

### Phase 7 — Scan & understand (steps 89–95)

| # | What questy does | What it finds | Console output |
|---|-----------------|--------------|----------------|
| 89 | Scan standards/ | Read all .md files, map frozen decisions | `Reading standards/… found 3 files` |
| 90 | Scan plans/ | Read active proposals, architecture docs | `Reading plans/… found 2 files` |
| 91 | Scan docs/ | Read reference, ADRs, changelogs | `Reading docs/… found 5 files` |
| 92 | Detect conflicts | Compare plan-vs-plan, plan-vs-standard | `Conflict: P002 vs standards §3.1` |
| 93 | Assess coverage | Map types to existing content | `Arch: covered ∎∎∎∎∘ 80% \| Trust: covered ∎∘∘∘∘ 20%` |
| 94 | Prioritise gaps | Order by risk + coverage deficit | `Priority: trust (gap) > integration (gap) > data (partial) > vision > arch` |
| 95 | Filter answered | Cross-ref proposals.md resolved items | `Skipping: Q004, Q007, Q015 (already resolved)` |

### Phase 8 — Generate, process, close (steps 96–100)

| # | What questy does | Presentation | User action |
|---|-----------------|-------------|-------------|
| 96 | Generate trust questions (gap priority) | Batch 1: 5 trust questions with ⬛ risk hat, global Q016-Q020 | `1,3,5 → answered 3, skipped 2` |
| 97 | Generate integration questions | Batch 2: 5 integration questions, type→hat mapping applied | `2,4 → answered 2` |
| 98 | Generate remaining | Arch, data, vision in impact order | `c → next batch` |
| 99 | Process answers | Update proposals.md (new decisions), pendings.md (skipped), conflicts.md (new clashes), archive.md (if resolved) | `stop → end session` |
| 100 | Export & commit | Git add+commit all changed files; offer markdown/JSON/HTML export; if questy-html → live preview | `Exported to exports/questy-2026-07-29.md` |

## Source index

### bridges/oasis.md — 2026-08-01

- Archive: `development/wiki/archive/old/bridges/oasis.md`
- Stable home: `development/standards/work.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/browsy-questions.md — 2026-08-01

- Archive: `development/wiki/archive/old/browsy/browsy-questions.md`
- Stable home: `development/standards/work.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/pre-build/README.md — 2026-11-17

- Archive: `development/wiki/archive/old/browsy/pre-build/README.md`
- Stable home: `development/standards/work.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/rationale.md — 2026-11-17

- Archive: `development/wiki/archive/old/browsy/rationale.md`
- Stable home: `development/standards/work.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/spec.md — 2026-11-17

- Archive: `development/wiki/archive/old/browsy/spec.md`
- Stable home: `development/standards/work.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/2026-11-17-appy-authy-mynet.md — 2026-11-17

- Archive: `development/wiki/archive/old/plans/2026-11-17-appy-authy-mynet.md`
- Stable home: `development/standards/work.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/2026-11-19-authy-open-questions.md — 2026-11-19

- Archive: `development/wiki/archive/old/plans/2026-11-19-authy-open-questions.md`
- Stable home: `development/standards/work.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/2026-11-21-app-database-stages.md — 2026-11-21

- Archive: `development/wiki/archive/old/plans/2026-11-21-app-database-stages.md`
- Stable home: `development/standards/work.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/puzzy.md — 2026-08-01

- Archive: `development/wiki/archive/old/plans/puzzy.md`
- Stable home: `development/standards/work.md`
- Status: summarised in the stable page; no open decision is recorded here.

### proposals/frontend-wizy.md — 2026-11-19

- Archive: `development/wiki/archive/old/proposals/frontend-wizy.md`
- Stable home: `development/standards/work.md`
- Status: summarised in the stable page; no open decision is recorded here.
