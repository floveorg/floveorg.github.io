---
status: stable
section: frontend/apps
created: 2026-11-21
also: [development/standards/frontend/apps/apps.md, development/standards/frontend/experience/experience.md, development/standards/plans/plans.md, development/standards/data/content/json.md]
---

# frontend/apps — Appy dashboard redesign

> Source: `development/archive/old/plans/2026-11-20-appy-dashboard-redesign.md` (archived 2026-11-21).
> Stable owner: `development/standards/frontend/apps/apps.md`.

## Goal

1. Give Appy Profily’s card-and-grid rhythm for **Apps played** without copying
   any of Profily’s demo data.
2. Keep Appy’s own username box (`#reg-handle`), JS tab system, plays bridge and
   every existing feature.
3. Redo the theme mechanism once, on the canonical `flove:theme` key, instead of
   maintaining a third, unused toggle.

## Sources and ownership

| Fact | Source |
|---|---|
| App routes and fields | `tools/apps/routing.json` (app entry points at `apps/appy/index.html`) |
| Tree / Types view | `development/index.html` |
| Reference design | `addons/profily.html` (moved from `development/addons/profily.html`) |
| Plays record and rollout | `frontend/frontend.md` §13.12.2 · Share → Appy rollout |
| Shared HTML renderer | `development/addons/rendery/index.html` (`accept()` → `profileHtml()`) |
| Theme contract | `frontend/frontend.md` §13.14 |

Profily is a **visual reference only**. Its demo handle, Soul stats, trusts,
offers, Wanty data, wizards and hardcoded `APPS` array stay out of Appy. Only
`flove:profily:subavatars` is persisted there; Appy does not read it.

<a id="feature-lock"></a>
## Feature lock — no regressions

Anchors are in `apps/appy/index.html`; the demo changes CSS and markup only.

| Area | Anchor |
|---|---|
| Self-contained runtime + i18n | `4-54`, `2155-2160`, `6638-6665` |
| Profile card and handle box | `2331-2370`, `4297-4300`, `4566`, `4580` |
| Plays launcher, upload, cards, bridge | `2294-2327`, `5866-6107`, `6162-6497` |
| Export / share / view profile | `4203-4285`, `3077-3081` |
| Wizy Magic | `2412-2428`, `4193-4200`, `5949-5967` |
| Authy / Browsy / Risa | `3330`, `3376-3384`, `3388`, `4509`, `4539` |
| Tiers / extension cards | `2460-2571`, `5716`, `5775` |
| Nety / MyNet | `4304-4320`, `5168`, `5230`, `5325` |
| Chat / Activity / Privacy | `2916-2941`, `5274`, `2952-2996`, `3576-3603`, `4828` |
| Keyboard and ARIA conventions | `2275-2284`, `6453-6455` |

## Layout

- **Header:** keep the brand button and editable `#reg-handle`. Stat chips appear
  only when a real key supplies a value (`flove:appy:plays`, Authy level, stage)
  — never a placeholder.
- **Apps played grid:** show the existing `#played-grid` (currently `d-none`),
  carrying Profily’s card rhythm while keeping the DOM built by
  `addPlayedApp()`: `.ac-title`, `.ac-sub`, `.ac-body`, `.ac-card`, `.open`.
  `#played-icons` remains the small-screen fallback.
- **Detail:** clicking a card keeps `.open` and the embedded `portraitHtml()`
  iframe. Rendery’s `accept()` is the canonical renderer; no second renderer.
- **Tabs:** same ids and order — profile · nety · mynet · chat · activity ·
  extensions · privacy. `switchTab()`, `role=tablist` and `aria-selected` stay.

<a id="data-contract"></a>
## Data contract — preserved exactly

- **Record shape** written by all 54 apps:
  `{app, appId, category, schema, portrait, colour, url, via, date, id, file}`.
  Bridge records replace the same app; uploads stay as history.
- **Live update:** keep `storage`, `focus`, `visibilitychange`,
  `refreshPlays()` and `window.floveAppy.onChange(hydrateFromBridge)`. Re-render
  only the plays grid — never reload the page.
- **Handoff:** keep the `flove-appy-ready` / `flove-appy-play` postMessage pair,
  the opener/origin check, the `schema === 'flove-portrait/1'` +
  `Array.isArray(rows)` validation, and the iframe-height message.
- **Broken records:** a play whose portrait fails validation is discarded with a
  visible message, never a blank card (EXP03c).

## Theme redo (§13.14)

Neither `index.html` nor `profily.html` loads the old shared theme script (formerly `apps/appy/flove-theme.js`, then `tools/flove-theme.js`; now inlined where used);
Profily’s `--auto`/`--dark` bar CSS is inert because its markup uses a plain
`.flove-bar`.

Use one canonical mechanism: a pre-paint inline script sets `data-theme` from
`localStorage['flove:theme']` or the OS query; the toggle flips it and persists
`light`/`dark`; unset follows the OS. The ◐ control sits in the topbar dropdown
next to the language ball. Appy stops using the shared script (key `flove-theme`,
`.dark` class). The shared file is gone: every launcher and project page
inlines its own copy.

<a id="dashboard-customisation"></a>
## Dashboard customisation — planned only

A future `flove:appy:dashboard` key holds widget order and visibility with a
fixed default layout. No customisation UI or storage write in this pass.

## Verification

1. `python3 tools/dev/checks/validaty-static.py --quiet` — exit 0.
2. `node --check` on every inline script changed in the demo.
3. EXP03c — inject a malformed play and confirm the visible discard.
4. EXP06 — confirm the portrait iframe resizes via `flove-card-height` and
   “See profile” opens `apps/appy/index.html#profile`.
5. Render the demo to PNG and inspect the plays grid, dark palette and compact
   fallback before merging.

## Rollout

1. Write this spec; move Profily to `addons/`; point routing at
   `apps/appy/index.html` and regenerate `tools/apps/routing-index.json`.
2. Build `apps/appy/appy-next.html` as a copy with the layout and theme changes,
   no data changes. The live app keeps working.
3. After sign-off, port the demo to `apps/appy/index.html` and delete the demo
   copy.

<a id="nety--appy-frontend-build"></a>
## nety / appy frontend build

> Source: `development/archive/old/plans/2026-06-18-nety-frontend-build.md` (archived 2026-11-21).

> **Revision 2026-06-19** — this plan was rewritten in place to match what actually got
> built. The original section-by-section `nety.html` build (Tasks 1–7, now archived in
> `…-frontend-build.md.bak-orig`) was **superseded** by an interactive tabbed prototype,
> `apps/miniappy.html`. The **design spec** (archived at
> [`../../archive/old/archive/making-of/superpowers/specs/2026-06-18-nety-access-ecosystem-design.md`](../../archive/old/archive/making-of/superpowers/specs/2026-06-18-nety-access-ecosystem-design.md)
> remains the source of truth for *what* the system is; this plan tracks *how* it's being
> realized in the frontend and what's next.
>
> **For agentic workers:** REQUIRED SUB-SKILL: use superpowers:executing-plans (or
> subagent-driven-development) to work Phase A–D task-by-task. Steps use `- [ ]` checkboxes.

**Goal:** Prototype, then productionize, the flove access system (registration, invite web,
MyNet/permissions, four-facet trust, stars/stages, donation directing, recovery) as an
interactive mock first — validating the UX in one self-contained file — then port the
validated patterns into the real apps and finally wire a backend.

**What this plan now covers:** the current state of `apps/miniappy.html`, the divergences
from the original section plan, and a four-phase roadmap: **A** keep refining miniappy ·
**B** port validated patterns into the real apps · **C** build/refresh wizy·sety·profily ·
**D** backend wiring.

---

### Status at a glance

| Area | State |
|---|---|
| `apps/miniappy.html` — interactive nety/appy mock (7 tabs) | **Built & iterating** (~40 commits, 38be6e1 → HEAD) |
| Original `nety.html` section-stacked landing (orig. Tasks 1–7) | **Superseded** by miniappy.html — not built as written |
| `apps/wizy.html` (orig. Task 8) | **Not started** |
| `apps/language/puzzy/sety.html` improvements (orig. Task 9) | **Not started** |
| `apps/profily.html` improvements (orig. Task 10) | **Not started** |
| Backend (flovenet/oasis) | **Deferred** (separate plan) |

---

### What got built — `apps/miniappy.html` (ground truth, 2026-06-19)

A single self-contained HTML/CSS/JS file (~3760 lines), light theme (`--bg #f3f4fb`,
`--ink #16141f`, `--accent #6c5ce7`, `--signal #02855c`), rainbow "appy bee" logo. All
state-driven via one `const state = {…}` + a master `render()`. No build step, no deps.

#### Tabs (display order)

| # | Tab | panel id | Holds |
|---|-----|----------|-------|
| 1 | **Profile** | `panel-profile` | `marcflove` card (handle/peerId/presence/stage/stars), expandable detail (handle edit + keypair), **Extend profile** 5-bar identity scale (Self·Email·Telegram·Phone·Bio) + per-step auth form, **publish-to-queue** column (visibility dropdown + "What's in your love" + Submit), pending posts |
| 2 | **Nety** | `panel-nety` | Welcome banner (animated bee logo) + collapsible "about the mesh" (big ✕ to close) + live network stats ticker; "I can't" is the default resource posture |
| 3 | **MyNet** | `panel-mynet` | Invites (enter code / budget 2-of-3 / generate) + collapsible SVG **invite lineage tree** (revoke/disown) + social feed + **Favourites / Groups** two-column + **Be more social** (people to follow / groups to support; follow·support·★ toggles) |
| 4 | **Chat** | `panel-chat` | Inbox + search-to-invite + conversation view (me/them bubbles, ephemeral toggle, 🎙/🎥 upgrade-gated) |
| 5 | **Activity** | `panel-activity` | 3-col: stage ladder (newbie→legend) · concentric **facet rings** SVG · facet scores (+suggestions/upgrade popups); stage-detail expand; **Donated Computing** stats; posts queue + moderation pipeline (pending→review→live) |
| 6 | **Extensions** | `panel-extensions` | **Appy navs** 5-tier feature ladder (mini·basic·normal·advanced·super) w/ thresholds + per-nav "see more" detail rows; **Be more appy** cards: Donate Computing (CPU/GPU/RAM presets+bars, in-card see-more), Add content, Add invite code, Ask for trusts; "More appy flove" (jobs/talent/donations) |
| 7 | **Privacy** | `panel-privacy` | Visibility scopes (content/resources/profile/scores) + per-facet circle visibility + self-backup seed phrase + social-quorum (2-of-3) + key rotation + loss-vs-compromise notes |

#### Vocabulary in use (UI-displayed)

- **Tiers:** `mini · basic · normal · advanced · super` (`state.tierCeilingMap`)
- **Stages:** `newbie · known · homie · expert · legend` (thresholds `[0,10,100,1000,10000]`)
- **Trust facets/scopes:** **Personal** (#02a85f) · **Local** (#0bb5c9) · **Social** (#6c5ce7) · **Global** (#3a86ff)
- **Circles/groups:** `close · friends · mynet · collaborators` (+ demo groups)
- **Resources:** CPU (cores/8) · GPU (GB/12) · RAM (GB/16); contribution unit = **CU**
- **Presence:** `LIVE · RECENT · REACHABLE · DARK`

#### Known vocabulary / code drift — **resolved in A1 (commit on 2026-06-19)**

- ✅ `tc-*` ids + `tour*` card keys/functions (dismantled-"tour" leftovers) → renamed onto the
  live `ec`/`ecard` (expandable-card) family: `tc-*`→`ec-*` ids, `tourCardOpen`→`ecardOpen`,
  `toggleTourCard`→`toggleEcard`, `renderTourCardState`→`renderEcardState`,
  `tourValidateInvite`→`ecardValidateInvite`, `tcGoPublish`→`ecGoPublish`,
  `tcRemoveSocialProfile`→`ecRemoveSocialProfile`.
- ✅ Dead state removed: 8 `tour*` engagement keys (superseded by `state.engagement[id]`) and
  the write-only tier trio `tierCeiling`/`tierCeilingMap`/`currentMode` (never read) + their 5
  assignments. (This *was* the "tierCeiling vs currentMode" item — answer: both dead, removed.)
- ↩︎ **Kept** `state.peers` (live — `mynetAddFriend`/`findPerson` use it) and `updateVis` (live
  no-op called by 4 circle-visibility selects). The earlier "vestigial/dead" flags were wrong.
- `state.activity` vs per-peer `presence` use the same enum — parallel by design; left as-is.

---

### Phase A — Keep refining `apps/miniappy.html`

Polish + cleanup passes on the prototype. Each change: verify (`<div>` balance grep +
`node -e "new Function(script)"` JS parse + handler-resolution), render-to-PNG when visual,
then commit + push to Gitea `localhost:3000/marc/flove` (main), message = prompt + explanation.

- [x] **A1 · Vocabulary & dead-code cleanup** — DONE 2026-06-19. Renamed `tc-*`/`tour*`
  leftovers → `ec`/`ecard` family; removed 16 lines of dead state (tour engagement keys + the
  write-only tier trio); kept the live `state.peers`/`updateVis`. Verified (304/304 divs, JS
  parses, 58 handlers resolve, every card toggle↔body). Net 3760→3744 lines.
- [ ] **A2 · Mobile + i18n hardening** — structural pass done (lang, utf-8, fluid SVG,
  `toLocaleString` numbers). Remaining if pursued: externalize UI strings + audit the ~21
  physical directional CSS props for RTL. (Large; only if the user opts in.)
- [ ] **A3 · Continued UX polish** — per turn-by-turn user requests (the ongoing mode).

> Working agreement: bottom-up, no skipping stages, no time pressure ("ke fluya"). Visual
> work → suggest `/output-style flove-frontend`. Don't ask Marc deep-backend questions —
> decide or defer to Phase D.

### Phase B — Port validated patterns into the real apps

> **Sequencing (user, 2026-06-19): do Phase B LAST.** The B1 architecture decision
> (tabbed app vs section landing vs hybrid) is deferred to the end; tackle Phase C first.

Once a pattern is settled in miniappy, carry it into the production files. miniappy stays as
the living reference/mock; the real apps adopt only what's validated.

- [ ] **B1 · Decide the target shape (deferred to last)** — does the real access point become a
  tabbed app like miniappy, the section-stacked `nety.html` of spec §8, or a hybrid (public
  section landing + tabbed member app)? Resolve before porting.
- [ ] **B2 · Port Access/identity/stars** — registration, four-path entry, identity ladder,
  stars/stage board → real `nety.html` (CSS-pure + one inline script per spec §9).
- [ ] **B3 · Port MyNet/circles/permissions + invite web** into the real flow.
- [ ] **B4 · Honesty line + page order + cross-links** (spec §6/§8).

### Phase C — Build / refresh the linked apps (original Tasks 8–10)

- [ ] **C1 · `apps/wizy.html`** (new) — athenea finetuner-agents app: navy `#0d1430` + gold
  `#d4af37`, owl mark; mirror sety's structure; agents (Summaries/Suggestions/Offers/Matches/
  Polarities/Reminders) + per-agent strength/temp sliders; Wizy vs MyWizy framing.
- [ ] **C2 · `apps/language/puzzy/sety.html`** — ecosystem back-link; brand "Wizard" as **athen-ia
  finetuner agents** + link to wizy; 24–28px slider thumbs; shape glyphs.
- [ ] **C3 · `apps/profily.html`** — extended-profile framing + back-link; manage-identity
  card; actionable Trusts; stars/tier reflection; custom MyNet + named circles + circle-level
  permissions; MyWizy entry + Apps grid.
- [ ] **C4 · Cross-link pass** — nety ↔ profily ↔ sety ↔ wizy ↔ apps/index; invariant checks
  (zero-extra-JS, reduced-motion block, `.vh` inputs); commit/push.

### Phase D — Backend wiring (deferred to its own plan)

The full backend realization — flovenet-native (4 derived facets, native circles via OR-Set
CRDT + forward-secret group keys, invite/lineage module, presence, follows-as-mirror, native
AI) and the **oasis add-on** (SSB bridge, "42" pluggable engine) — is specified in
[`../../archive/old/archive/making-of/superpowers/specs/2026-06-18-nety-spec-vs-flovenet-oasis-comparison.md`](../../archive/old/archive/making-of/superpowers/specs/2026-06-18-nety-spec-vs-flovenet-oasis-comparison.md) and becomes its own plan. Don't start
until Phase B settles the frontend data contracts. MyWizy inference-engine details (local vs
shared-mesh, pluggable backend) are further-spec-later.

---

### Constraints & workflow (carried forward)

- **Source of truth:** `archive/making-of/superpowers/specs/2026-06-18-nety-access-ecosystem-design.md` (the *what*).
- **Naming & tier model (spec §2.1) — verbatim:** `nety` = hardware (resource quota ladder),
  `appy` = data-software (feature ladder), each `mini → basic → normal → advanced → super`.
  Stages = `newbie · known · homie · expert · legend`. A **stage = earned ceiling**; the
  **tier/mode you browse is your choice**. **Access gating:** `mini`(nety) open (no invite);
  `basic`(appy) invite-gated. Profiles: `profily-mini` (open) ↔ `profily` (full).
- **Fonts/hues:** keep each app's own identity; no Inter/Roboto/Arial.
- **All data is mock/illustrative** until Phase D (stars reset on reload, etc.).
- **`docs/` is gitignored** → the Gitea workflow does NOT apply to this plan file; keep
  **local backups** before rewrites (this plan's original = `…-frontend-build.md.bak-orig`).
  Two synced copies exist: canonical `debates/plans/` + bundle `docs/nety-specs/`.
- **App-file workflow:** every change to `apps/*` → commit + push to Gitea `marc/flove` (main),
  message carrying the prompt + explanation; render-to-PNG before committing visual changes.

---

## Historical record

The full pre-2026-11-23 text of this chapter is preserved in
`development/archive/2026-11-23/plans/frontend/apps.md` with checksums in the partition's
`SHA256SUMS`. This plan keeps the accepted decisions and the archived-note index only.

<!-- historical anchors kept for evidence resolution
<a id="appendix-archived-original-task-list-superseded"></a>
-->

## Source index

### apps/README.md — 2026-11-09

- Archive: `development/archive/old/apps/README.md`
- Stable home: `development/standards/frontend/apps/apps.md`
- Status: summarised in the stable page; no open decision is recorded here.

### apps/onboarding-copy.md — 2026-11-17

- Archive: `development/archive/old/apps/onboarding-copy.md`
- Stable home: `development/standards/frontend/apps/apps.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/TESTING.md — 2026-08-01

- Archive: `development/archive/old/browsy/TESTING.md`
- Stable home: `development/standards/frontend/apps/apps.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/rationale.md — 2026-11-17

- Archive: `development/archive/old/browsy/rationale.md`
- Stable home: `development/standards/frontend/apps/apps.md`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/spec.md — 2026-11-17

- Archive: `development/archive/old/browsy/spec.md`
- Stable home: `development/standards/frontend/apps/apps.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/2026-06-18-nety-frontend-build.md — 2026-06-18

- Archive: `development/archive/old/plans/2026-06-18-nety-frontend-build.md`
- Stable home: `development/standards/frontend/apps/apps.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/2026-11-14-app-tier-planned.md — 2026-11-14

- Archive: `development/archive/old/plans/2026-11-14-app-tier-planned.md`
- Stable home: `development/standards/frontend/apps/apps.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/2026-11-17-appy-authy-mynet.md — 2026-11-17

- Archive: `development/archive/old/plans/2026-11-17-appy-authy-mynet.md`
- Stable home: `development/standards/frontend/apps/apps.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/2026-11-20-appy-dashboard-redesign.md — 2026-11-20

- Archive: `development/archive/old/plans/2026-11-20-appy-dashboard-redesign.md`
- Stable home: `development/standards/frontend/apps/apps.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/2026-11-21-app-database-stages.md — 2026-11-21

- Archive: `development/archive/old/plans/2026-11-21-app-database-stages.md`
- Stable home: `development/standards/frontend/apps/apps.md`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/puzzy.md — 2026-08-01

- Archive: `development/archive/old/plans/puzzy.md`
- Stable home: `development/standards/frontend/apps/apps.md`
- Status: summarised in the stable page; no open decision is recorded here.

### proposals/frontend-tiers.md — 2026-11-19

- Archive: `development/archive/old/proposals/frontend-tiers.md`
- Stable home: `development/standards/frontend/apps/apps.md`
- Status: summarised in the stable page; no open decision is recorded here.

### proposals/frontend-wizy.md — 2026-11-19

- Archive: `development/archive/old/proposals/frontend-wizy.md`
- Stable home: `development/standards/frontend/apps/apps.md`
- Status: summarised in the stable page; no open decision is recorded here.

### root/adoption.md — 2026-08-01

- Archive: `development/archive/old/root/adoption.md`
- Stable home: `development/standards/frontend/apps/apps.md`
- Status: summarised in the stable page; no open decision is recorded here.

### root/backend.md — 2026-08-01

- Archive: `development/archive/old/root/backend.md`
- Stable home: `development/standards/frontend/apps/apps.md`
- Status: summarised in the stable page; no open decision is recorded here.
