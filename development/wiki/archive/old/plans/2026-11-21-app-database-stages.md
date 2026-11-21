# App database — stages seed → full

> **Living plan.** Updated 2026-11-21. This document is refined in place and
> reflected in the Development index Database panel.
>
> **Stage vocabulary:** the five canonical stage words from
> [`index.md`](index.md) — **seed · infant · mature · grown · full**. Here they
> name the app-data ladder; they do not move any hito in the Work register.
>
> **Minimal-model source:** `apps/appy/index.html`, function `exportProfile()`
> (lines 4087–4111). The envelope is replicated in §3; the source file remains
> the authority for its exact field names.
>
> **Boundary:** this database holds app data and the sys apps that serve apps.
> It holds no development-task or project data: `milestones.json`,
> `common.json`, `development/**`, `whole/` and `docs/**` stay in git and never
> enter a table.

## 1 · Goal and boundary

1.1 The goal is a **play store** for flove: one unified profile per user,
opt-in sharing of app data, and relations between data from several users
without a new table per feature. The database is the substrate; Browsy is the
storefront and Central is the version/health manager.

1.2 **In scope:** every app under `apps/**` and the sys apps that help them —
`authy` (identity), `browsy` (portable profile + storefront), `nety` (local
store + mesh), `wizy` (discovery), `central` (version/health). `sety` is not a
separate local app: its controls are the Privacy tab of `apps/appy/index.html`,
and Appy owns their state at every stage.

1.3 **Out of scope:** development hitos, tasks, standards, scripts, `whole/`
and documentation. A task in the Work register is not a row in this database.

1.4 **Golden rule:** git owns code and routing; `routing.json` owns which apps
exist; the database owns app state and its SHA projection; the service worker
is the cache; `updaty` is the publisher. `risa.json` remains the feed truth and
`flove.json` is an optional, fail-silent enrichment (stage infant), never a
second truth.

## 2 · The five stages

| Stage | Name | What holds | Writer | Store contribution |
|---|---|---|---|---|
| `seed` | Local | `localStorage` + JSON in git + SW precache | the app itself | Per-app profiles; the fragmentation we start from |
| `infant` | Bridge | Optional `flove.json` enrichment + hosted SQLite replica (`flove-authy/1` carried by Browsy) | hosted replica | First unified identity: claiming a word links the profile; Lovy activates already authenticated; same profile on two devices with the node off |
| `mature` | Local backend | `rusqlite` + FTS5, derived slices, SHA gate, event log | `rusqlite` in the local node | The unified profile is born: one `profiles` row served to every app; apps stop owning identity |
| `grown` | Local sys services | Typed local services, no cloud; `rusqlite` remains the writer | local gateway | The store: `catalog` is the shelf, Browsy loads on click, Central manages version/health, `shares` and `edges` appear |
| `full` | Federated mesh | Several nodes, no central authority; stages seed–grown are each node's offline mode | each node's replica | Portable profile, verifiable relations across nodes, signed manifests; Meilisearch only as a derived discovery index |

2.1 Stage `infant` does not disappear at stage `mature`: it stays as the "no
node" mode. What changes is the writer — hosted replica in `infant`,
`rusqlite` in `mature`.

2.2 Non-goals at every stage: Dexie, Cloudflare D1, gRPC to the browser, and
Meilisearch as a source. gRPC is allowed only between local services at stage
`grown`; Meilisearch only as a derived discovery index at stage `full`.

## 3 · Minimal model — replicated from Appy index

3.1 The minimal model is the envelope that `apps/appy/index.html` already
exports as `kind: 'flove-profile'`. It is replicated here field for field; no
new envelope is invented.

| Field | Type / origin | Meaning |
|---|---|---|
| `kind` | constant `'flove-profile'` | envelope discriminator |
| `version` | `1` | envelope version |
| `routing` | constant `'flove-routing/3'` | routing contract in git |
| `exported` | ISO timestamp | generation time |
| `handle` | `state.handle` | public @handle |
| `presence` | `state.activity` | LIVE / DARK / RECENT |
| `stage` | `{ name, index, stars }` | ladder position; thresholds from `state.stageThresholds` |
| `contributionsCU` | `state.contributions` | compute contributed to the mesh |
| `trust` | `state.facets` | `{ personal, local, social, global }` |
| `identities` | `state.linkedIdentities[]` | self / email / telegram / phone / biometrics |
| `socialProfiles` | `state.socialProfiles[]` | linked public profiles |
| `self` | `flove-authy/1.self` | Authy self-card, null until authenticated |
| `risa` | `{ key, clips[] } \| null` | risa feed key and clips |
| `about` | `state.aboutEntries[]` | user-authored about lines |
| `appsPlayed` | `played[]` | one row per stored play (shape in 3.2) |
| `network` | `{ groups[], follows[], supports[], favourites[] }` | relations owned by the user |
| `posts` | `state.queue[]` | queued local posts |
| `visibility` | `state.permissions` | `{ content, resources, profile, scores }` |

3.2 Each `appsPlayed[]` row is:

```
{ app, appId, category, schema, cells, portrait, via, date, play }
```

`appId`/`category` resolve through `APP_ROUTING`; `portrait` is the app's
`flove-portrait/1` envelope; `cells` is derived from its `rows[]`; `via` is
`upload`, `share` or `app`; `play` is the stored play id.

3.3 The per-app portrait envelope is `flove-portrait/1`:

```
{ schema: 'flove-portrait/1', app, version: 1, generatedAt, rows: [{ key, kind, title, items }] }
```

3.4 **Stage-`mature` tables derived from the envelope.** The profile envelope
is one `profiles` row; its arrays become the tables the play store needs. No
development data is stored.

| Table | From the envelope | Role |
|---|---|---|
| `catalog` | `routing.json` + each app's `flove-fields` SHA | the store shelf; `appId`, `category`, `folder`, `version`, `sha`, `entry` |
| `profiles` | whole envelope | one row per user: scalars plus `trust`, `socialProfiles`, `about` and `network` as JSON columns |
| `plays` | `appsPlayed[]` | one row per app played, with `portrait` JSON + `cells` |
| `claims` | `identities[]` + `flove-authy/1` + `flove:identity` | verified claims (authy nonce, mail, OAuth, web key) |
| `preferences` | `visibility` + Appy Privacy controls | visibility, group visibility, `flove:theme`, `chat_ephemeral`, language |
| `posts` | `posts[]` (`state.queue`) | `id`, `type`, `visibility`, `content`, `status` |
| `messages` | `state.chats[]` | local 1:1 outbox; `peer`, `from`, `text`, `status` |
| `installs` | `appId` + last open | which user uses which app version |
| `events` | sync log | `last_seen`, key rotation, backup confirmation, stage changes; `last_seen` in `localStorage` |
| `catalog_fts` | `catalog` + `plays` + `posts` text | FTS5 over name, description, tags, fields, post content |

3.5 `shares` (`{ owner, object_id, sha, scope, expires }`) and `edges`
(`{ from_id, rel, to_id, visibility, evidence }`) are **stage `grown`**: they
are the sharing and relation layer of the store, not part of the minimal
stage-`mature` model. `edges` is the one generic table for follows, reactions,
chains and reputation — no new table per feature.

3.6 **Appy inventory → stage-`mature` storage.** Appy supplies the **basic
fields** of the database. Only state that Appy actually writes is mapped:
demo pools (`peers`, `morePeople`, `extraPeople`, `feedPosts`, `moreGroups`,
`extraGroups`), UI flags (`*Open`, `peopleShown`, `feedShown`) and mock-only
flows (`generateInvite`, `revokeInvite`, raw CPU/GPU/RAM stats) stay out. Their
real side effects — points, probation, `contributionsCU` — are stored instead.

| Appy source | Real writer | Stage-3 target | Note |
|---|---|---|---|
| `state.handle`, `state.activity` | profile card, presence badge | `profiles.handle`, `profiles.presence` | envelope scalars |
| `state.stars`, `state.stage`, `state.stageName[stage]` | `awardPoints()`, `checkStageThreshold()` | `profiles.stage_*` | thresholds stay in code |
| `state.facets` | `awardPoints()` | `profiles.trust` | Activity rings read this row |
| `state.contributions`, `state.shared`, `state.resourcePreset` | `shareHardware()` | `profiles.contributions_cu` + `events(kind=contribution)` | raw resource stats not stored |
| `state.linkedIdentities`, `readAuthy()` | `persistAuthy()` | `claims` | verified Telegram gates MyNet and publish |
| `flove:identity` | `saveBrowsyIdentity()` | `claims` (web key) | Browsy handoff |
| `state.socialProfiles`, `state.aboutEntries` | `saveSocial()`, `saveAbout()` | `profiles.social_profiles`, `profiles.about` | typed JSON columns |
| `state.risaKey`, `state.risaClips` | risa cache key | `profiles.risa` | `flove:appy:risa:*` stays a cache |
| `state.joinedGroups`, `state.groups`, `state.tags` | group UI | `profiles.network.groups` | local membership only |
| `state.follows`, `state.supports`, `state.favourites` | `followMore`, `supportMore`, `toggleFavourite` | `profiles.network.*` | no `edges` until `grown` |
| `state.permissions` | `updatePerm()` | `profiles.visibility` + `preferences.visibility` | M06 |
| group visibility selects (4) | `updateVis()` | `preferences.group_visibility` | no-op today; M08 makes it real |
| `flove:theme` | theme toggle | `preferences.theme` | canonical key |
| `state.chatEphemeral`, `state.chats[]` | `chatSend()`, `chatInvite()` | `preferences.chat_ephemeral`, `messages` | local outbox, no XMPP yet |
| `state.queue[]` | `submitContent()` | `posts` | FTS5 indexes the content |
| `state.recovered`, `state.inProbation`, `backup-check` | `rotateKey()`, backup checkbox | `events` + `preferences.backup_confirmed` | state flag, not real crypto |
| `state.peerId`, `state.keypair`, `state.inviteBudget` | identity and invite prototypes | not stored | mock; only derived points are kept |

3.7 Goddy and Realy are the **demo of the remaining fields**: neither owns a
profile row. Goddy projects `flove:goddy:matrix` into `plays.cells` plus a
`flove-portrait/1` row set; Realy projects `flove:realy:state` (sections,
notes, `extraRealms`, `moreRealmsLabels`) into the same shape, including its
one-way legacy read of `realy_state`. Both fill `catalog` through their
`fieldsSource` SHA, proving the basic Appy tables accept a second app without
a new table.

3.8 **Embedded and sys-owned state is special, not Appy-owned.** Appy sometimes
reads or displays data whose owner is another app or a sys app. That data keeps
its owner and reaches the database through the existing bridge, never as new
Appy profile fields.

| Embedded source | Real mechanism | Stage-3 target | Note |
|---|---|---|---|
| Blogy | `window.flovePortrait.get()` / `floveSummary()` fed to the shared `flove-appy.js` bridge (`data-flove-publish="appy"`) | `plays[app='Blogy']` with `portrait` | `flove:appy:plays` is the local cache; Blogy owns the portrait |
| MyFamily | `floveSummary = () => getModel()` publisher; Appy's `wizyMyFamily()` reads legacy `flove:myfamily:state` | `plays[app='MyFamily']` | `myfamily.html` no longer writes that key; absent state is N/A, not a mock row |
| Any other published app | same bridge, `via = appy \| wizy` | `plays` + `catalog` | one writer, no per-app table |
| Browsy embed | `apps/sys/browsy/index.html?embed=1&source=appy` posts `flove-browsy-identity` into `saveBrowsyIdentity()` | `claims` (web key) | the iframe is a handoff, not a profile owner |
| Authy handoff | `flove-authy/1` posted from `apps/sys/authy/index.html` | `claims` (self, email, Telegram) | gate source for MyNet and publish (M07) |
| Wizy / Central / Nety | discovery, SHA gate and local store for apps | their own tables, no profile row | sys helpers stay out of `profiles` |
| Rendery (`addons/rendery`) | renders an existing JSON | no row | read-only formatter, not a source |

## 4 · First objective — migrate Goddy, Realy and Appy to stage `mature`

4.1 These three apps are the first migration because together they already
exercise the whole minimal model: Appy owns the profile envelope and the
`flove:appy:plays` bridge; Goddy and Realy are portrait producers that write
into that bridge.

4.2 **Execution order:** Appy first — it defines `profiles`/`plays` and the
bridge both others write to — then Goddy, then Realy. The rows below keep the
order Goddy, Realy, Appy as named in the objective; M01/M02 depend on the
bridge being readable from M03.

| ID | Deliverable | Done when | Owner path | Evidence `{kind, value}` |
|---|---|---|---|---|
| M01 | Goddy matrix → `plays` row | `flove:goddy:matrix` is read once into `plays[app='Goddy']`; reload reproduces the same cells and the same `flove-portrait/1`; `localStorage` keeps only control keys | `apps/metas/goddy.html` | `state` → Goddy reloads its matrix from `plays` with identical cells |
| M02 | Realy state → `plays` row | `flove:realy:state` (sections, notes, extraRealms, moreRealmsLabels) is read once into `plays[app='Realy']`; reload reproduces the same portrait | `apps/psychosocial/realy.html` | `state` → Realy reloads its realms from `plays` with identical rows |
| M03 | Appy `flove-profile` → `profiles` + `claims` + `plays` | One `profiles` row resolves the envelope of §3 for every app; `identities[]` become `claims`; `flove:appy:plays` becomes `plays` rows; two apps show the same profile | `apps/appy/index.html` | `state` → two apps resolve the same `profile_id` |
| M04 | FTS5 over `catalog` + `plays` | `catalog_fts` answers by app name, tags and portrait text; Wizy suggests without parsing `routing.json` | `apps/sys/wizy/index.html` | `state` → Wizy returns suggestions from `catalog_fts` |
| M05 | SHA gate | A changed `routing.json` or portrait that is not re-projected is reported as stale by Central; no app reads a stale row | `apps/sys/central/index.html` | `state` → Central flags stale SHA, apps refuse the row |
| M06 | Appy Privacy → `profiles.visibility` | `updatePerm()` writes each change of Content / Resources / Profile to the `profiles` row; reload restores the three selects and `exportProfile()` emits the same `visibility` object | `apps/appy/index.html` | `state` → three selects and export agree after reload |
| M07 | MyNet and publish gates from `claims` | `mynetFlags()`, `socialEnabled()` and `publishUnlocked` derive from `claims`, not from `flove:authy`; a presence claim opens local people/circles/feed, a verified claim enables public publish | `apps/appy/index.html` | `state` → preview, local and social gates follow the row |
| M08 | Privacy controls beyond visibility | The four group-visibility selects, Backup-confirmed and a key rotation write `preferences.group_visibility`, `preferences.backup_confirmed` and `events(kind=key_rotation)`; reload restores the selects and checkbox and the event appears once | `apps/appy/index.html` | `state` → selects, checkbox and event agree after reload |
| M09 | Activity from the profile row | Rings read `profiles.trust`, stage chips `profiles.stage`, the presence pulse `profiles.presence`, and the one-shot Share-hardware button is spent when its `events(kind=contribution)` row exists; a circle marked `private` in Privacy hides its Activity values | `apps/appy/index.html` | `state` → rings, stage, pulse and spent button from the row |

4.3 **Fallback during migration:** stage `seed` stays live. An app that cannot
reach the local backend reads `localStorage` exactly as today; migration is a
one-way copy by the app itself, never a destructive reset. The old keys remain
as the source until the new row round-trips unchanged.

4.4 **Done-criterion for the whole objective:** with the local node running,
Goddy, Realy and Appy each reload from SQLite with the same data they had in
`localStorage`; with the node off, the same apps still work from stage `seed`.
The profile is unified in the node and nowhere else.

4.5 **Activation surface at stage `mature`:** Appy's own tabs are the only place
that flips functions on. `sety` is retired as a separate local app because those
controls already live in Privacy; no third control surface and no feature-flags
envelope are added. The `flove-profile` envelope stays the only wire format. On
boot Appy resolves one `profiles` row (`SQLite` with the node up, `localStorage`
at stage `seed` otherwise) and maps fields it already owns to gates it already
implements:

| Tab | Function | Row field | Work |
|---|---|---|---|
| Privacy | Content / Resources / Profile selects | `visibility` | M06 |
| Privacy | Group visibility, Backup confirmed, key rotation | `preferences.*`, `events` | M08 |
| MyNet | Preview / local / social gates, people, circles, feed, follow | `claims` | M07 replaces `flove:authy` in `mynetFlags()` |
| MyNet | Publish button and public option | `claims` + `visibility.content` | M07 |
| Activity | Trust rings, stage chips, presence pulse | `trust`, `stage`, `presence` | M09 through M03 |
| Activity | One-shot Share hardware and the circle columns | `events(kind=contribution)`, `preferences.group_visibility` | M09 + M08 |
| Profile | Risa card, portrait and export | `risa`, `plays`, `appsPlayed` | already works; M03 makes it row-backed |
| Chat | Local outbox and ephemeral flag | `messages`, `preferences.chat_ephemeral` | row-backed by M03; XMPP stays a proposal (4.6) |

None of this needs `nety`. Mock-only controls — invite codes, seed phrase,
quorum signing and raw resource stats — stay demonstrative; no row activates
them or pretends they are real security.

4.6 **Chatland / XMPP in the Chat tab — proposal, not a stage-3 task.**

4.6.1 Chatland is currently a specification page, not shipped code:
`projects/chatland/index.html` names Prosody on `:5222`, 1:1 chat, MUC zones and
a short-lived JWT for the 3D room. There is no XMPP client or server in the
repo, so stage `mature` keeps Chat's local `messages` outbox. The ideas below
are opt-in and need a real server.

4.6.2 One thin adapter, not a new app: a small WebSocket (or BOSH) XMPP adapter
owned by the Appy Chat tab, with one vendored client library, no build step and
no second control surface. Chatland remains the spec and brand page.

4.6.3 Identity from `claims`, not a new login: derive the JID from a verified
claim already in the profile row; Appy stores no separate XMPP password.

4.6.4 Message parity: each sent or received stanza becomes a `messages` row
`{ peer, from, text, status, jid }`; the local outbox stays the `seed` fallback
when the adapter is off.

4.6.5 Respect `chat_ephemeral` and Privacy: ephemeral conversations are not
written to `messages`; the group visibility from M08 decides whether a zone is
offered at all.

4.6.6 Start with 1:1. MUC zones, presence and Chatland's 3D room token
(Colyseus + Filament) are stage `grown` / `full` ideas only, never a `mature`
dependency.

4.6.7 Fail silent: if Prosody is unreachable, Chat shows the local outbox with
a disabled connect control; no error blocks the rest of Appy.

4.7 **MyNet backend subsection — hitos and tasks in all five stages.**
MyNet is a backend subsystem of Appy, not a separate app and not a third
control surface. The register owns its six hitos and 44 tasks in section
`mynet` of `development/standards/debates/milestones.json`; the Work page
renders them in the Backend → MyNet tab. The read-only preview and export
stay on the existing `flove-profile` envelope; `claims` and the `profiles`
row drive every gate. No new envelope and no feature-flags envelope.

4.7.1 **Hitos by stage.**

| ID | Stage | Deliverable | Done when | Owner path | Evidence `{kind, value}` |
|---|---|---|---|---|---|
| mynet-01 | `seed` | read-only MyNet preview and MyFamily JSON export owned by Appy. | the MyNet tab shows people, circles and feed in preview with no claim and exportProfile() emits the same visibility and network fields after reload, with no node and no new envelope. | `apps/appy/index.html` | `state` → T03 passes with MyNet preview open |
| mynet-02 | `infant` | claim rows from the Authy and Browsy handoffs. | flove-authy/1 and flove-browsy-identity produce claims rows and the MyNet preview reflects presence with no new password or login. | `apps/sys/authy/index.html` | `state` → T01 and T02 pass with claims visible |
| mynet-03 | `infant` | mynetFlags(), socialEnabled() and publishUnlocked derived from claims. | no claim keeps preview, a presence claim opens local people/circles/feed and a verified claim enables public publish, with no flag written outside the row. | `apps/appy/index.html` | `state` → T06 passes with preview, local and social gates |
| mynet-06 | `mature` | the profiles/claims row as the single source Chatland reads, so the mature database enables 1:1 chat. | a row written by Appy is read by the Chatland adapter without a second envelope, the JID comes from a verified claim, and no new envelope is introduced. | `apps/appy/index.html` | `state` → T03 and T06 pass with the Chatland bridge |
| mynet-04 | `grown` | row-backed people, circles, feed, follow and local sharing. | those surfaces read profiles, network, posts and edges from the profile row, a circle marked private hides its values and sharing defaults to private with no schema migration. | `apps/appy/index.html` | `state` → shared row resolves by SHA in a second profile |
| mynet-05 | `full` | a signed portable MyNet profile and its edges. | another node verifies the profile and edges by signature + SHA, public posts, groups and grants follow the portable profile, and no central authority is required. | `apps/sys/browsy/index.html` | `state` → public posts, groups and grants resolve from the portable profile |

4.7.2 **Tasks — 1 seed + 3 infant + 3 mature per hito, plus one task at the
hito stage for `grown` and `full`.** Every task names its deliverable, its
done-criterion, one owner path and a machine-readable evidence pointer;
the same rows are the canonical source in `milestones.json` and its
generated `common.json` / Work projections.

| ID | Stage | Concrete title | Done when | Owner path | Evidence `{kind, value}` |
|---|---|---|---|---|---|
| mynet-01.1b | `seed` | Name the MyNet preview owner | one owner path, apps/appy/index.html, is recorded for the read-only preview and no second control surface is named. | `apps/appy/index.html` | `state` → apps/appy/index.html owns the MyNet preview |
| mynet-01.2a | `infant` | List the preview fields from flove-profile | the preview reads handle, presence, stage, network and visibility from the existing flove-profile envelope and writes no new envelope. | `apps/appy/index.html` | `state` → preview renders handle, presence, stage, network and visibility |
| mynet-01.2b | `infant` | Wire the MyNet tab preview | the MyNet tab renders people, circles and feed from the row in preview mode with no claim and makes no network call. | `apps/appy/index.html` | `state` → MyNet tab shows people, circles and feed in preview |
| mynet-01.2c | `infant` | Keep the MyFamily export read-only | Export emits the same network and visibility fields after reload and never edits the rows it previews. | `apps/appy/index.html` | `state` → export carries the same network and visibility fields |
| mynet-01.3 | `mature` | Restore preview state from localStorage | with the node off the preview restores from localStorage and keeps the same three visibility selects. | `apps/appy/index.html` | `state` → preview restores from localStorage with the node off |
| mynet-01.3b | `mature` | Block every preview write | no control in preview mode writes profiles, claims or posts and the block is observable in state. | `apps/appy/index.html` | `state` → preview mode leaves profiles, claims and posts unchanged |
| mynet-01.3c | `mature` | Verify the preview against test T03 | test T03 of the app database plan passes unchanged while the MyNet preview is open. | `apps/appy/index.html` | `state` → T03 passes with MyNet preview open |
| mynet-02.1b | `seed` | Name the claim handoff owner | one owner path, apps/sys/authy/index.html, is recorded for the claim handoff and the Browsy source is named as its peer. | `apps/sys/authy/index.html` | `state` → apps/sys/authy/index.html owns the claim handoff |
| mynet-02.2a | `infant` | Map Authy identities to claims | each verified identity in flove-authy/1 becomes one claims row with the same level and no duplicate on reload. | `apps/sys/authy/index.html` | `state` → flove-authy/1 identities appear once in claims |
| mynet-02.2b | `infant` | Map the Browsy web key to claims | the flove-browsy-identity postMessage becomes one claims row carrying the web-key hash. | `apps/sys/browsy/index.html` | `state` → web-key hash appears as a claims row |
| mynet-02.2c | `infant` | Fire a claim change event | a claim write fires one flove claim-changed event and Appy refreshes the MyNet preview from the row. | `apps/appy/index.html` | `state` → one claim-changed event refreshes the preview |
| mynet-02.3 | `mature` | Read claims in the MyNet preview | the preview reads presence and verified state from claims and shows no separate password field. | `apps/appy/index.html` | `state` → preview reflects presence and verified claims |
| mynet-02.3b | `mature` | Fail silent on an absent claim | with no claim row the preview stays read-only and no error or mock claim is written. | `apps/appy/index.html` | `state` → no claim leaves the preview read-only |
| mynet-02.3c | `mature` | Verify tests T01 and T02 with MyNet open | tests T01 and T02 pass and the same identities and web key are visible in claims. | `apps/sys/authy/index.html` | `state` → T01 and T02 pass with claims visible |
| mynet-03.1b | `seed` | Name the MyNet gate owner | one owner path, apps/appy/index.html, is recorded for the gate logic and no flags envelope is named. | `apps/appy/index.html` | `state` → apps/appy/index.html owns the MyNet gates |
| mynet-03.2a | `infant` | Replace the flove:authy read in mynetFlags | mynetFlags() reads claims instead of flove:authy and keeps the same preview result with no claim. | `apps/appy/index.html` | `state` → mynetFlags() derives preview from claims |
| mynet-03.2b | `infant` | Derive socialEnabled from claims | socialEnabled() is true only when a presence claim exists in the row and false is observable otherwise. | `apps/appy/index.html` | `state` → socialEnabled() follows the presence claim |
| mynet-03.2c | `infant` | Derive publishUnlocked from a verified claim | publishUnlocked is true only with a verified claim and the publish button stays disabled without one. | `apps/appy/index.html` | `state` → publishUnlocked follows the verified claim |
| mynet-03.3 | `mature` | Guard publish with visibility.content | a public post is refused when visibility.content is private even with a verified claim. | `apps/appy/index.html` | `state` → private content blocks the public publish |
| mynet-03.3b | `mature` | Remove flag envelope writes | no gate writes a flag outside the profile row and the previous flove:authy keys are read-only fallbacks. | `apps/appy/index.html` | `state` → no flag is written outside the row |
| mynet-03.3c | `mature` | Verify test T06 | test T06 passes: preview, local and social gates follow claims in order. | `apps/appy/index.html` | `state` → T06 passes with preview, local and social gates |
| mynet-06.1b | `seed` | Name the row-to-chat owner | one owner path, apps/appy/index.html, is recorded for the profile-to-Chatland bridge and no second envelope is named. | `apps/appy/index.html` | `state` → apps/appy/index.html owns the row-to-chat bridge |
| mynet-06.2a | `infant` | Expose the profiles row to Chatland | Chatland reads handle, presence, stage, network and visibility from the existing flove-profile row and writes no new envelope. | `apps/appy/index.html` | `state` → Chatland reads the existing flove-profile row |
| mynet-06.2b | `infant` | Map claims to the Chatland JID | the JID is derived from a verified claim and no password field or second identity store is added. | `apps/sys/authy/index.html` | `state` → Chatland JID derives from a verified claim |
| mynet-06.2c | `infant` | Define the read-only chat fallback | with no node or no claim the adapter stays read-only and no mock message row is written. | `apps/appy/index.html` | `state` → no claim leaves chat read-only with no mock row |
| mynet-06.3 | `mature` | Bind one profile row to one chat identity | one profile row resolves to exactly one chat identity after reload and no duplicate JID appears. | `apps/appy/index.html` | `state` → one profile row resolves to one chat identity |
| mynet-06.3b | `mature` | Keep visibility on every chat read | private visibility.content and visibility.resources hide their chat metadata while the row keeps the values. | `apps/appy/index.html` | `state` → private visibility hides chat metadata |
| mynet-06.3c | `mature` | Verify T03 and T06 with the bridge open | nety-free tests T03 and T06 pass while the Chatland bridge reads the row. | `apps/appy/index.html` | `state` → T03 and T06 pass with the Chatland bridge |
| mynet-04.1b | `seed` | Name the row-surface owner | one owner path, apps/appy/index.html, is recorded for the MyNet row surfaces and the store path is named as its peer. | `apps/appy/index.html` | `state` → apps/appy/index.html owns the MyNet row surfaces |
| mynet-04.2a | `infant` | Bind people and circles to the row | people and circles read network and profiles from the same profile row and no local copy is created. | `apps/appy/index.html` | `state` → people and circles render from the row |
| mynet-04.2b | `infant` | Bind the feed to posts | the feed reads posts from the profile row and keeps the same order after reload. | `apps/appy/index.html` | `state` → feed order survives reload from posts |
| mynet-04.2c | `infant` | Bind follow to edges | a follow writes one edges row and unfollow removes that row without a schema change. | `apps/appy/index.html` | `state` → follow and unfollow map to edges rows |
| mynet-04.3 | `mature` | Hide a private circle | a circle marked private in Privacy hides its Activity and MyNet values while the row keeps them. | `apps/appy/index.html` | `state` → private circle hides values without deleting them |
| mynet-04.3b | `mature` | Default local sharing to private | a share starts with scope private and a URL appears only when scope public is chosen. | `apps/appy/index.html` | `state` → share URL appears only with public scope |
| mynet-04.3c | `mature` | Keep the seed fallback for MyNet | with the node off, people, circles and feed still open from localStorage with the same rows. | `apps/appy/index.html` | `state` → MyNet surfaces work from seed with the node off |
| mynet-04.4 | `grown` | Verify the local sharing round-trip | a shared row opened in a second local profile resolves to the same posts and edges by SHA. | `apps/appy/index.html` | `state` → shared row resolves by SHA in a second profile |
| mynet-05.1b | `seed` | Name the portable-profile owner | one owner path, apps/sys/browsy/index.html, is recorded for the portable MyNet profile and Appy is named as its reader. | `apps/sys/browsy/index.html` | `state` → apps/sys/browsy/index.html owns the portable profile |
| mynet-05.2a | `infant` | Pack the profile for transport | the exported bundle carries the existing flove-profile fields plus its edges and no new envelope. | `apps/appy/index.html` | `state` → bundle carries flove-profile fields and edges |
| mynet-05.2b | `infant` | Sign the profile and its edges | one signature covers the profile row and its edges and the bundle carries the key id. | `apps/sys/browsy/index.html` | `state` → signature covers profile and edges |
| mynet-05.2c | `infant` | Publish the bundle through Browsy | the bundle travels through the Browsy handoff with the SHA in the manifest and no direct node call from Appy. | `apps/sys/browsy/index.html` | `state` → bundle travels with SHA in the manifest |
| mynet-05.3 | `mature` | Verify the SHA on arrival | a changed bundle is rejected before it reaches the MyNet surfaces and the source row stays untouched. | `apps/appy/index.html` | `state` → SHA drift rejects the bundle before render |
| mynet-05.3b | `mature` | Verify the signature on another node | a second node accepts the profile and edges only when the signature matches the claimed key id. | `apps/sys/browsy/index.html` | `state` → second node verifies signature and key id |
| mynet-05.3c | `mature` | Keep private circles private across nodes | a private circle is omitted from the transported bundle and stays visible only on the owner node. | `apps/appy/index.html` | `state` → private circles stay on the owner node |
| mynet-05.4 | `full` | Follow public posts, groups and grants from the portable profile | public posts, groups and grants resolve from the verified portable profile with no central registry. | `apps/appy/index.html` | `state` → public posts, groups and grants resolve from the portable profile |

4.7.3 **Section decision.** No third control surface is introduced: the
read-only preview and export live in Appy, the claim handoff in Authy and
Browsy, the gate logic in Appy, and the portable profile in Browsy with
Appy as reader. The new Backend → MyNet tab groups their hitos by stage;
it does not duplicate the Privacy or MyNet tabs of Appy.

4.8 **Chatland hitos across the other axes.** The `mature` database is what
enables Chatland: `mynet-06` makes the `profiles`/`claims` row the single
source, `schemas-11` owns the `messages` shape and `chat_ephemeral`,
`storage-08` persists the table and `shell-13` wires the thin 1:1 adapter.
Phase 4 (`grown`) adds MUC zones and the Prosody bridge; phase 5 (`full`)
adds the short-lived-JWT 3D room and Nety federation over the portable
profile. Docs → Work owns the dependency map in `work-25`; AI has no new
model, skill, flow or depth level and therefore no hito.

4.8.1 **Hitos by stage and axis.**

| ID | Stage | Axis · domain | Deliverable | Owner path | Evidence `{kind, value}` |
|---|---|---|---|---|---|
| mynet-06 | `mature` | Backend · mynet | the profiles/claims row as the single source Chatland reads, so the mature database enables 1:1 chat. | `apps/appy/index.html` | `state` → T03 and T06 pass with the Chatland bridge |
| schemas-11 | `mature` | Data · schemas | a canonical schema for messages and chat_ephemeral with one owner doc. | `development/standards/backend.md` | `state` → backend.md §13 anchors the messages schema |
| storage-08 | `mature` | Backend · storage | a persistent messages table backing Chatland 1:1 chat. | `development/standards/backend.md` | `state` → T03 and T04 pass with messages persisted |
| shell-13 | `mature` | Frontend · shell | a thin opt-in XMPP adapter in Appy Chat over WebSocket/BOSH. | `apps/appy/index.html` | `state` → T06 and T07 pass with the adapter |
| work-25 | `mature` | Docs · work | one canonical map of the Chatland enablement chain and its owner in Docs → Work. | `development/standards/debates/plans/2026-11-21-app-database-stages.md` | `state` → jsony critical=0 and Work --check green |
| channels-09 | `grown` | Community · channels | MUC zones with group visibility driven by M08. | `projects/chatland/index.html` | `state` → zones resolve from the row after reload |
| systems-25 | `grown` | Backend · systems | a thin Prosody bridge for presence and MUC. | `projects/chatland/index.html` | `state` → reconnect replays unseen stanzas only |
| channels-10 | `full` | Community · channels | a short-lived JWT room for Colyseus + Filament. | `projects/chatland/index.html` | `state` → two nodes resolve the same 3D room |
| systems-26 | `full` | Backend · systems | a portable profile and edges that carry Chatland identity between nodes. | `apps/sys/browsy/index.html` | `state` → public posts, groups and grants resolve without a registry |

4.8.2 **Enablement chain.** `mynet-06` + `schemas-11` → `storage-08` → `shell-13` → `channels-09` / `systems-25` → `channels-10` / `systems-26` + `mynet-05`. Each arrow names the hito that must be
satisfied before the next one can be demonstrated; none of them writes a
new envelope or a flag outside the row. The Chatland spec page remains the
source for Prosody `:5222`, MUC zones and the 3D-room JWT (4.6).

4.8.3 **Cap exception.** The live queue moved 1,455 → 1,492 with the five
MyNet hitos and again 1,492 → 1,559 with these nine hitos, both by explicit
owner decision on 2026-11-21 recorded here. `recommendedMax` is 1,504 and
the 55-slot headroom is preserved. This is an exception to PROC-09, which
otherwise forbids growing the cap by accumulation; AGENTS.md, the register
and both generators carry the same numbers.

## 5 · Sys-app functionality tests — no nety required

5.1 Each test is run from a shipped app or sys app, from its own UI or its own
JS contract. None needs `nety`, a build step or a server other than flove's
static host. Evidence is app-observable state (`kind: state`), not a dev
script.

| ID | Test | How to run | Expected state | Owner sys app |
|---|---|---|---|---|
| T01 | Authy persistence | Open `apps/sys/authy/index.html`, add an identity, reload | `flove:authy` still holds `schema: flove-authy/1` with the same `level` and `identities`; `flove:authy:changed` fired | `apps/sys/authy/index.html` |
| T02 | Browsy → Appy identity handoff | Open `apps/sys/browsy/index.html?embed=1&source=appy`, generate the web key | `postMessage` of type `flove-browsy-identity` reaches Appy; `flove:identity` holds the hash and the profile card shows it | `apps/sys/browsy/index.html` |
| T03 | Appy Privacy activation | Open `apps/appy/index.html`, Privacy tab, change Content to `public`, reload, then Export | The three selects restore their values, the exported `flove-profile` carries the same `visibility`, and with the node up the `profiles` row matches | `apps/appy/index.html` |
| T04 | Wizy offline suggestions | Open `apps/sys/wizy/index.html`, pick two apps, use `compact` surface | Three local suggestions appear from Wizy's own hint tables; the exported prompt names `tools/routing.json` and the flow makes no network call | `apps/sys/wizy/index.html` |
| T05 | Central catalogue | Open `apps/sys/central/index.html` | Links to the system cluster and the app catalogue resolve; at stage `grown` the same panel shows version + SHA per app from `catalog` | `apps/sys/central/index.html` |
| T06 | MyNet and publish gates from claims | Open `apps/appy/index.html` with no Telegram claim, then verify one through Authy | MyNet starts in preview and opens local when the presence claim is in `claims`; public publish stays disabled until the verified claim is there; no flag is written outside the row | `apps/appy/index.html` |
| T07 | Privacy controls round-trip | Privacy tab: set Personal group visibility to `private`, tick Backup confirmed, rotate the key, reload | The four selects and the checkbox restore from `preferences`; one `events(kind=key_rotation)` row remains and no flag is written elsewhere | `apps/appy/index.html` |
| T08 | Activity from the row | With a row-backed profile, mark Social `private` in Privacy and open Activity | Rings, stage chips and pulse match `trust`, `stage` and `presence`; Social values are hidden; Share hardware stays spent after its contribution event | `apps/appy/index.html` |

5.2 These tests are the acceptance gate for stages `mature` and `grown`: they
prove identity, privacy, discovery and version reporting work before any mesh
or hosted replica exists.

## 6 · Update log

6.1 **2026-11-21** — plan created; five levels renamed to the canonical stage
words `seed · infant · mature · grown · full`; minimal model replicated from
the Appy index `flove-profile` envelope; first objective set to the Goddy,
Realy and Appy migration to stage `mature`; nety-free app tests added.
Scope restricted to apps and helping sys apps; no development tasks.

6.2 **2026-11-21** — `sety` removed from the local scope: its controls are
Appy's Privacy tab. Stage `mature` activation is specified as M06 (persist
`visibility`) and M07 (publish gate from `claims`), with 4.5 naming the five
gates Appy already implements; T03 and T06 replace the Sety test. Applied to
the Development index Database panel.

6.3 **2026-11-21** — full Appy inventory mapped to the basic stage-`mature`
tables (3.6); Goddy and Realy confirmed as demos of the remaining fields (3.7).
Embedded and sys-owned state is specified as special in 3.8 (Blogy, MyFamily,
Browsy, Authy, sys helpers, Rendery). Activation extended to M08 (Privacy
controls beyond visibility) and M09 (Activity from the row), with the tab map
in 4.5 and tests T07/T08. Chatland / XMPP is recorded as a proposal in 4.6:
the Chat tab keeps its local outbox at stage `mature`, with a thin opt-in
adapter, `claims`-derived identity and `messages` parity for later stages.

6.4 **2026-11-21** — MyNet got its own Backend tab and subsection in the
register and in the backend plan: six hitos (`mynet-01`–`mynet-06`) and
44 fully specified tasks cover seed · infant · mature · grown · full.
The queue cap moved from 1,455 to 1,492 with 55 slots of headroom; the
Work and common projections were rebuilt from `milestones.json`.

6.5 **2026-11-21** — Chatland adapted across axes: nine new hitos
(`mynet-06`, `schemas-11`, `storage-08`, `shell-13`, `work-25`,
`channels-09`, `systems-25`, `channels-10`, `systems-26`) with 67 fully
specified tasks. `mynet-03` moved from `mature` to `infant` and `mynet-06`
took its `mature` box. The Docs → Work hito owns the cross-axis dependency
map; AI stays without hitos. Queue cap 1,492 → 1,559 by owner exception
(4.8.3), with `mynet-03` and the new tasks visible in Work and common.
