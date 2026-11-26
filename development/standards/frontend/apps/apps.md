<!-- CONTEXT:BEGIN
schema: flove-page/1
id: frontend/apps
path: development/standards/frontend/apps/apps.md
trunk: frontend
topic: apps
kind: topic
status: stable
html_place: ["#apps"]
owns: ["App rollout", "tiers", "frontend build"]
updated: 2026-11-21
read_next: ["#app-tree-05", "#app-tree-06", "#app-tree-07", "#app-tree-08", "#app-tree-09", "#app-tree-10", "#app-shell-05", "#app-shell-06", "#app-shell-07", "#app-shell-08", "#app-shell-09", "#app-shell-10", "#app-visual-05", "#app-shell-13", "#app-tree-13", "#app-shell-11", "#app-visual-06", "#app-tree-14", "#app-shell-12", "#app-visual-07"]
CONTEXT:END -->

# Apps

```text
frontend/
├─ frontend.md                         §13 catalogue · §13.12 export owner
├─ accessibility/accessibility.md      a11y pass owner
├─ experience/experience.md            §14 gates
├─ apps/apps.md                        app tree / shell / tiers  ★ YOU
├─ summary.md                         §13.9 summary panel owner
├─ counters.md                   ✗     → frontend.md#138-counters
├─ publish.md                    ✗     → frontend.md#flove-publish-to-appy-1315
├─ routing-colours-db.md         ✗     → frontend.md#routing-colours-optimisation-and-future-databases
├─ export.md                     ✗     → frontend.md#1312-model
└─ optimizy-pass.md              ✗     removed, no home
See also: ↑ README.md · ↓ data/content/json.md · → data/ai/skills/optimizy/SKILL.md
```


## Browsy extension standards (draft)

**Identity hash.** One identity, one hash:

```text
hash = PeerId = CIDv1(sha256(ed25519_pubkey)) → bafk…
```

The full value is stored; the UI shows a short prefix with copy. Nety’s
`PeerId::from_public_key_bytes` already implements this formula.

**Generation.** Hybrid:

- Extension installed: the service worker creates and stores the root. The hash
  is shown in the extension UI (popup/side panel); Appy/Browsy index may display
  it only through an explicit handoff, never as a portable root.
- No extension: Browsy index / Appy embed may create a **full local identity**
  in `flove:identity` with `source:"web"` and a visible warning. It works on
  mobile and can sign local grants, but there is no web→extension migration;
  installing the extension starts a new canonical identity.
- `file://`: web fallback; the manifest does not cover `file://`.
- One canonical hash per profile; the extension wins when installed, and a web
  demo stays a separate record.

**Status (2026-11-18).** The web fallback is live: `apps/sys/browsy/index.html`
generates an Ed25519 key with WebCrypto, derives the CIDv1 PeerId (`bafk…`),
stores `flove:identity` with `source:"web"` and `notPortable:true`, and Appy
embeds the same generator through `?embed=1`. The private seed stays in the
Browsy page; Appy only mirrors the public hash. The extension
`getOrCreateIdentity()`/bridge and the Nety root import are next.

**Direction: Browsy pulls, the page does not ask.** There is no page→extension
identity or vault API. The pipeline is:

1. The user clicks Browsy.
2. The content script reads the current public page (visible text/DOM).
3. The service worker/worker parses it; Wizy mixes it with local P/L content.
4. Browsy renders suggestions in the page or side panel.

The page never receives the vault, the root key or the identity hash from this
pipeline.

**Pull scope (Q004).** Full DOM, including form fields and hidden inputs,
selected for signal. This is a high-risk choice: it needs an explicit redaction
policy before shipping (Q006).

**Consent (Q005).** A persistent Browsy indicator while pulling, a **Stop**
button and a per-site allowlist. Never pull silently.

**Redaction (Q006).** A full-DOM pull includes normal `input`, `textarea` and
`select` values for context, but never `type=password`, secret `autocomplete`
tokens, hidden inputs, cookies or tokens. Raw values never go to logs.

**Failure (Q002).** Typed state `idle · pulling · no-access · error` with a
retry. No silent injection.

| Stage | Internal interface | Notes |
|---|---|---|
| pull | `browsy.pullPage()` | current public page; click only |
| derive | `wizy.suggest()` | page content + local classes; no network |
| present | `browsy.render()` | badges/side panel; no P/L |
| sign | `authy.sign()` | internal; app handoffs only |
| export | `authy.exportRoot()` | extension UI; explicit gesture |

**Runtime (v1).** Chrome/Edge use WebCrypto Ed25519; Firefox/Safari use the
bundled tweetnacl fallback. Both paths are tested; `lib/tweetnacl.min.js` and
`lib/worker.js` must exist in the package.

**Storage (Q007).** v1 keeps `browsy-keys` in `chrome.storage.local`; the
encrypted vault is M2. The web fallback uses `flove:identity`.

**Identity record (Q010).** Canonical `flove-identity/1`:
`{schema, hash, publicKey, source, createdAt, label?}`. `flove-browsy/1` is a
read-only view; `flove:authy.self.browsyHash` is a display cache. The schema row
is owned by [`schemas.md#schema-envelopes`](../../data/schemas/schemas.md#schema-envelopes).

**Web local identity lifecycle (Q009/Q013).** An existing `source:"web"`
record is hidden but kept when the extension identity appears; the extension
hash is canonical. Never auto-delete the local identity.

**Recovery (Q014).** A 12-word seed is generated at identity creation; social
quorum is a later path. The seed is the only recovery for a local key, so the
warning must say so.

**Origins (Q012).** Only `https://flove.org/*`, `http://localhost/*` and
`http://127.0.0.1/*`; no `<all_urls>`; no `file://` (use the web fallback).

**Nety (direction: same root; transport open).** The root should be imported
into Nety’s encrypted keystore so the PeerId is the same hash. The transport is
undecided: encrypted export, native messaging or seed phrase (K08). Delegation
is the v2 path for multi-device.

**Open.** Vault/unlock, Nety transport, app sessions, release, logging, masks,
sync and the test matrix: see `browsy-questions.md` K01–K18.

## Work

39 hitos · 162 tasks · 22 open · 17 closed. This page owns the
`Frontend/shell`, `Frontend/tree`, `Frontend/types` and `Frontend/visual`
chapters.

## Puzzy engine

The puzzy abstraction — extended definitions, thesaurus, polysemic dictionary,
the multi-axis/multi-rater engine and how entries attach to app data — lives in
the standing book [`puzzy.md`](../../data/schemas/puzzy.md). It ships in F4 · Full.

<a id="publish-to-appy"></a>
## Publish to Appy (§13.15)

The app → Appy bridge (`flove-appy.js`). State today (audit 2026-07-20):

| Role | App(s) | Publish state |
|---|---|---|
| READER | `appy-mini` · `appy-mini-full` · `appy-basic` | reads the bridge (`floveAppy.played` + `onChange`) **and** accepts the manual `<app>-portrait.json` upload |
| WRITER | `goddy` · `souls` · `pracsys` · `inventary` · `realy` · `myfamily` · `keys` | full trio — script + `window.floveSummary` + `appy/wizy/more` buttons; all 7 carry a domain `window.floveAgentBlock` and auto-publish on Update (F1) |

Rollout order: the WRITER trio is on all seven `COLOURS` emitters; `souls` was
the template and every one was already in `COLOURS`. `mini` never publishes;
`basic`+ carry appy/wizy; `more` (nety / 0asis) waits for F2+. Cross-device sync
is a backend milestone, not this phase.

| Environment | What the appy apps do today |
|---|---|
| `file://` | only the manual upload delivers; the publish button downloads `<app>-portrait.json` to drop on Appy's “Upload portrait here” |
| `http://localhost:<port>` | bridge live: a WRITER publishes → `appy-mini` / `appy-mini-full` / `appy-basic` show it instantly; manual upload also works |
| `https://flove.org` | same as localhost |

For a `file://` workflow the real path is **download → upload**; the automatic
bridge only kicks in once the apps are served over HTTP.

## Self-contained assets

`apps/` is published at `flove.org/apps/`, shipped in `flove-localhost.zip`,
installed as a PWA, and opened from `file://` or a plain HTTP server. It cannot
depend on `central/` code at runtime. Every app page inlines its own CSS and JS
and calls no external library. The only shared runtime dependency is artwork,
and it lives once in `development/addons/media/`:

| Canonical source | Used by |
|---|---|
| `development/addons/media/` | captions, logo animations, icons, `apps-full.html`, the root home |

Audio is web-only (`development/addons/media/audio/`, ~22 MB) and stays out of
the download. There is deliberately **no `apps/shared/css` or `apps/shared/js`**:
an app that needs a stylesheet or script must inline it. `central/apps/` is
archived; runtime apps live in `apps/`.

## Entry model

| Entrance | What it shows | Forces a language? |
|---|---|---|
| `/index.html` (live root and package root) | the full flove entrance | no — it has the 🌐 switcher, never blocks |
| `/apps/` | the app launcher (graph / entrance / grid) | no |
| `/tools/dev/assets/start.html` | the language-selection page | yes, on first run |
| `/tools/dev/assets/start.html?tour=1` | the intro tour | no — always shows the slides |

`start.html` is the single page behind both the language gate and the tour; the
`?tour=1` flag only suppresses the “language already saved → go home” shortcut.
The package keeps the same depth: `flove-localhost/index.html`,
`flove-localhost/apps/…`, `flove-localhost/tools/…`, `flove-localhost/docs/…`.
The language choice is stored in `localStorage` under `flove:lang` and
`translaty-lang`; every app reads it. Launchers write `tools/dev/assets/devices.json` with
LAN/Tailscale addresses.

<a id="running-flove"></a>
## Running flove — the four options

1. **Desktop / `.zip`** — download `flove-localhost.zip`, unzip and run
   `START-FLOVE-<os>`; it serves `flove-localhost/` on `localhost:8642` and opens
   `/index.html`.
2. **Android / Termux** — run it on the phone in Termux (offline, no network).
3. **Over the network (Red)** — reach the running instance from another device
   (same Wi-Fi, or Tailscale anywhere via HTTPS).
4. **`.aab` Android app** — the TWA built by `tools/apps/v1/flove-apk/`, published to
   GitHub Releases as `flove.aab`.

## Dashboard redesign

Appy keeps every feature and real value; Profily is a design reference only.
The full spec — goal, feature lock, layout, data contract, theme redo,
verification and rollout — is owned by
[`plans/frontend/apps.md#goal`](../../../plans/frontend/apps.md#goal). The stable
page only records the boundary: no demo data, no second renderer, no second
theme path.

## App tiers

**Status (2026-11-15): closed for this trunk.** `tier` is **not** part of
`tools/apps/routing.json`; no app carries tier markup, CSS or fields. The mini →
super variants survive only as demo sketches under `apps/blogy/`,
`apps/economy/dealy/`, `apps/language/puzzy/keys/` and `apps/appy/`.

A tier would be a **routing/distribution** class
(`nano · mini · basic · normal · advanced · super · mega`), read from a
per-app `<meta name="tier">` and written to `apps[].tier`. It does not affect
fields, category colour/hat or the influence ladder.

It is not live because the first imported apps do not all declare the meta tag;
guessing produces false metadata and obscures field completeness. Until adopted,
`status` means **field completeness only**: `complete` = full field tree
extracted; `partial` = curated subset still to extract.

The owner decided on 2026-11-15 that tiers are not going into this trunk. The
Puzzy launcher stepper, Souls ladder, Fivy tier module, shared `flove.js` module,
catalog tiles and distro pages were stripped; the demo sketches are kept on
purpose. Left alone: `apps/sys/nety/index.html` “hybrid local tiers” about
storage replication — a different meaning.

## nety / appy frontend build

The miniappy prototype is the ground truth for the access system; the original
section-stacked `nety.html` was superseded. The full status, tabs, vocabulary,
Phase A–D roadmap and constraints are owned by
[`plans/frontend/apps.md#nety--appy-frontend-build`](../../../plans/frontend/apps.md#nety--appy-frontend-build).

## App types

> Source: `tools/apps/routing.json` and each app's `flove-fields/1` manifest (canonical).

Every app declares its fields and type through `flove-fields/1`; `tools/apps/routing.json`
is the sole registry (54 apps). The type vocabulary is Act, Wish, Bond, Place,
Person, Time, Object, Freedom and Rating. Consumers read the flat field list
through `floveFieldsFlat()`; no app keeps a private type or field list.

This section is the owner for the app-type catalogue and its consumer list.

**Mirror contract.** `development/index.html → Apps → Types` is a read-only
projection of this catalogue plus `tools/apps/routing.json`; it invents no
type. [vocabulary.html](https://flove.org/development/standards/vocabulary.html)
mirrors that table verbatim and computes its chip counts from those rows.
Skills remain a type in both tables; the Dev layer does not re-list them.
The orthogonal **View: Apps | Dev** switch and Dev layer chips live only in
`vocabulary.html`, never in the development index.

A `check-types-sync.py` gate is **pending**: see `GATE01` in
[`development/tasks/pendings.md`](https://flove.org/development/tasks/pendings.md).
Until it lands, this paragraph is the only contract and no checker enforces it.

<a id="app-tree-05"></a>
## App tree with a manifest per route: inventory and owner

> Owner: apps. Canonical app-tree/shell/visual item for `tree-05`.

<a id="app-tree-06"></a>
## Lazy loading per section: what loads and when

> Owner: apps. Canonical app-tree/shell/visual item for `tree-06`.

<a id="app-tree-07"></a>
## Navigation without reload: route and state contract

> Owner: apps. Canonical app-tree/shell/visual item for `tree-07`.

<a id="app-tree-08"></a>
## Style isolation per app: scope and exceptions

> Owner: apps. Canonical app-tree/shell/visual item for `tree-08`.

<a id="app-tree-09"></a>
## Registry of canonical routes and aliases: redirect and canonical link

> Owner: apps. Canonical app-tree/shell/visual item for `tree-09`.

<a id="app-tree-10"></a>
## Predictive preload of the next destination: signals and limit

> Owner: apps. Canonical app-tree/shell/visual item for `tree-10`.

<a id="app-shell-05"></a>
## UI data client: backend consumption contract

> Owner: apps. Canonical app-tree/shell/visual item for `shell-05`.

<a id="app-shell-06"></a>
## Nety UI: Social feed, card S and network state (S only)

> Owner: apps. Canonical app-tree/shell/visual item for `shell-06`.

<a id="app-shell-07"></a>
## MV3 with menus, badge and popup; backend 0/14

> Owner: apps. Canonical app-tree/shell/visual item for `shell-07`.

<a id="app-shell-08"></a>
## Two switches: local network and Social Nety

> Owner: apps. Canonical app-tree/shell/visual item for `shell-08`.

<a id="app-shell-09"></a>
## Seven-tab miniappy prototype in iteration

> Owner: apps. Canonical app-tree/shell/visual item for `shell-09`.

<a id="app-shell-10"></a>
## Publish button: destinations and preview before sending

> Owner: apps. Canonical app-tree/shell/visual item for `shell-10`.

<a id="app-visual-05"></a>
## Nety UI without P/L; no moderation until the curator contract

> Owner: apps. Canonical app-tree/shell/visual item for `visual-05`.

<a id="app-shell-13"></a>
## Chatland 1:1 adapter in the Chat tab

> Owner: apps. Canonical app-tree/shell/visual item for `shell-13`.

<a id="app-tree-13"></a>
## Implement routing and colour map in Tree

> Owner: apps. Canonical app-tree/shell/visual item for `tree-13`.

<a id="app-shell-11"></a>
## Implement the shared interface layer in Shell

> Owner: apps. Canonical app-tree/shell/visual item for `shell-11`.

<a id="app-visual-06"></a>
## Implement token and motion system in Visual

> Owner: apps. Canonical app-tree/shell/visual item for `visual-06`.

<a id="app-tree-14"></a>
## Execute the frontend shared-code plan in Tree

> Owner: apps. Canonical app-tree/shell/visual item for `tree-14`.

<a id="app-shell-12"></a>
## Execute the Publisher adapter plan in Shell

> Owner: apps. Canonical app-tree/shell/visual item for `shell-12`.

<a id="app-visual-07"></a>
## Execute the harvested-patterns guide in Visual

> Owner: apps. Canonical app-tree/shell/visual item for `visual-07`.

## Sources

Source history is owned by `development/plans/`; this page holds the accepted facts.

