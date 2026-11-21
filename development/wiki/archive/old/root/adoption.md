# flove · Frontend adoption gates (§14)

The per-page gates that prove the frontend standards hold. The old per-app
adoption table drifted and is retired; what is enforced mechanically on every
release is the list below. The stable index of what the standards *are* is
`README.md`; the full spec is `frontend.md`; the usability minimum is §13.18.

**Before starting adoption work**, check [`plans/conflicts.md`](debates/plans/conflicts.md) for known tensions between plans.

## Architecture

**Browser Extension + Central = CORE** — browsy is the main navigation +
identity/trust bridge; Central is the data bank + frontend apps; Decentral Nety
is an extension for P2P distributed computation only. Repo: `apps/sys/` (Nety + P2P map) + `apps/sys/central/` (web-database home). Full spec in [`backend.md`](backend.md) §17.

## Web of Trust Persistence Budget

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Hop depth** | 3 hops | Full network (~1MB) |
| **Max users** | 100 | ~20KB storage |
| **Compression** | JSON | ~70% reduction with gzip |
| **Eviction** | LRU | Least recently used |

**Trust visibility:** first circle, second circle, social groups, public.

Per-app adoption of the frontend standards is **no longer tracked in a table
here** — it drifts too fast and went stale. What is enforced mechanically, on
every release:

| Check | What it proves |
|-------|----------------|
| `tools/extract-fields.py --check` | every app's `flove-fields` manifest matches `routing.json` (54/54 apps) |
| `tools/dev/check-portrait-protocol.py` | common layer + portrait adapter present |
| `node --check` over every inline script | no broken JS ships |
| `html-validate` with `tools/.htmlvalidate.json` | validity, a11y, i18n attributes |
| `python3 tools/dev/check-skills.py` | skills are consistent |
| `python3 tools/fa-subset.py` | each app's icon block matches `tools/fa/` (no stale/extra icons) |
| `python3 tools/check-a11y.py` | main landmark, one `<h1>`, reduced-motion, `lang` on bilingual spans, no positive `tabindex`, no placeholder links, labelled controls, focus styles |
| `optimizy3` · §13.18 | every applicable row in the usability matrix has its minimum (manual gate) |

The tier column is gone on purpose: app tiers are not part of this trunk (see
`debates/plans/2026-11-14-app-tier-planned.md`). Mark **N/A** where a standard
does not apply; onboarding/vocab may be `partial` while a rename is in flight
(track renames with the §13.7 deferred-renames doc-comment in the file).

> **Reference note:** **blogy** is the Solo fallback reference; the **trunk**
> apps in `apps/` are the canonical spec — see
> [`apps/README.md`](apps/README.md).

## CSS abstraction checklist (§13.16)

**Trunk status (2026-11-15): no app links shared CSS.** Every app in the trunk is
self-contained — it carries its own palette and, where it uses the family skin,
an inlined copy of `flove.css` pruned to the components it actually renders
(Raty and Socy are the reference for that pruning).

| App | Shared CSS | Tokens | Notes |
|-----|:----------:|--------|-------|
| all 48 routing apps | — (inline) | per-app `--app-accent*`, `--ink`, `--line`, `--panel` | no `href` to `addons/` anywhere |
| `addons/code/css/flove.css` | reference copy | canonical token block | shipped in the offline package, never loaded at runtime |

The canonical tokens (`--ink`, `--line`, `--card`, `--signal`) live in that
reference file; apps redeclare only their accent overrides. `.flove-focus`,
`.flove-selected` and `.flove-lift` remain the shared interaction vocabulary —
they travel inside the inlined copy, not through a stylesheet link.

## Publish to Appy (§13.15) — adoption & rollout

The app → Appy bridge (`flove-appy.js`). State today (audit 2026-07-20):

| Role | App(s) | Publish state |
|------|--------|---------------|
| READER | `appy-mini` · `appy-mini-full` · `appy-basic` | ✓ read the bridge (`floveAppy.played` + `onChange`) **and** accept the manual `<app>-portrait.json` upload |
| WRITER | `goddy` · `souls` · `pracsys` (`apps/bio/`) · `inventary` (`apps/economy/dealy/`) · `realy` (`apps/psychosocial/`) · `myfamily` (`apps/trusty/`) · `keys` (`apps/puzzy/keys/keys-advanced.html`) | ✓ full trio — script + `window.floveSummary` + `appy/wizy/more` buttons. **All 7 carry a domain `window.floveAgentBlock`** (wizy) and **auto-publish on Update** (F1). souls was the 2026-07-20 reference; keys (the 7th, in `COLOURS`) wired 2026-07-20 alongside its existing CSS-only Go/platforms cycle |

**Rollout order** (scalability): the WRITER trio is now on all **seven** `COLOURS`
emitters above; `souls` was the template and `COLOURS` already held every one, so no
registry edit was needed. Each also ships a domain wizy agent block and auto-publish
(F1, always on, local-only). `mini` never publishes; `basic`+ carry appy/wizy; `more`
(nety / 0asis) waits for F2+. Cross-device sync is a backend milestone, not this phase.
Full rule: [`frontend/publish.md`](frontend/publish.md).

**The current appy apps, per environment** (Marc runs on `file://`):

| Environment | What the appy apps do today |
|---|---|
| `file://` | **Only the manual upload delivers** to the profile — the bridge can't cross `file://` documents. With the new fallback, an app's publish button **downloads its `<app>-portrait.json`** for you to drop on Appy's "Upload portrait here". |
| `http://localhost:<port>` | **Bridge live**: a WRITER (e.g. `goddy`) publishes → `appy-mini` / `appy-mini-full` / `appy-basic` show it instantly (`onChange`). Manual upload also works. |
| `https://flove.org` | Same as localhost. |

So for a `file://` workflow the real path is **download → upload**; the automatic
bridge is a bonus that only kicks in once the apps are served over http.

## Distro adoption (§13.11) — self-contained trunk

**The enrichment loader is retired from this trunk (2026-11-15).** There is no
tier-gated `flove-loader.js` rollout: the mini → super variants survive only as
demo sketches under `apps/blogy/`, `apps/economy/dealy/`, `apps/puzzy/keys/` and
`apps/appy/`.

What every routing app does instead:

| Layer | Where it lives | Loaded at runtime |
|-------|----------------|-------------------|
| `floveStore` / `floveFields` / `flovePort` | inline block in each app | always (inline) |
| `flove.js` (summary actions, counters, formats) | inline where used (Fivy, Blogy) | inline |
| `flove-appy.js` (Appy bridge) | inline where used (Goddy, Souls, PracSys, MyFamily, Inventary, Realy) | inline |
| `flove-theme.js` + `flove.css` | inline where used (Puzzy launcher) | inline |
| `vendor/leaflet/leaflet.{css,js}` | `apps/economy/dealy/vendor/` | local files inside the app folder (Freed only) |
| webfonts (Inter + display face) | inline `@font-face` + `data:` URI in every page | always inline (latin subsets) |
| FontAwesome (subset) | inline `@font-face` + only that app's icons | always inline — 4.5–63.6 KB per app |

`addons/code/{css,js}` is the reference set: it documents the canonical
shape, ships in the offline package, and is never referenced by an app's markup.
**No app links a stylesheet at all** (only favicons, and Freed's local
`vendor/leaflet/leaflet.{css,js}`). Fonts and icons are inline `data:` URIs; no app
loads shared **code**. `addons/vendor/fonts/` was deleted (3.7 MB) — its
content now lives inside the pages.

`addons/vendor/` no longer exists — fonts and icons live inside the pages
and nothing referenced the folder. Its removal also fixed the offline-package
build, whose `git archive` pathspec still listed it (the folder was untracked, so
the command aborted).`
Browsy remains the main navigation app; Central adds backend depth on separate
branches (see `plans/central-backend.md`).

## Generic Webhook Exports

Browsy and Central can export profile data to external services via generic webhooks.

| Parameter | Decision |
|-----------|----------|
| **Storage** | Both (browsy local + Central synced copy) |
| **Trigger** | Manual only (user clicks export) |
| **Auth** | User-configurable (supports all methods) |
| **Proxy** | Both (browsy direct OR via Central) |

**Export targets:** GitHub repo, GitHub Pages, Gitea, custom URL, local file.
