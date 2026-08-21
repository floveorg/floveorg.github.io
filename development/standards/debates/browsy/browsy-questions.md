# Browsy Questions — Standalone Interface

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
5. **Sync to browser-extension.md** periodically

---

## Related Files

- `plans/browser-extension.md` — Full browsy plan with all decisions
- `plans/2026-07-24-appy-normal-mynet-browsy.md` — appy-normal plan (MyNet + wizy mini)
- `pendings.md` — All pending items across categories
- `plans/central-backend.md` — Central backend decisions
- `plans/nety-frontend.md` — Nety frontend decisions
- `plans/nety-trust.md` — Nety trust decisions
