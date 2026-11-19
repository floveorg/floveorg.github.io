# flove · Frontend Standards Upgrade — Design Spec

- **Date:** 2026-06-12
- **Status:** Draft — design approved in brainstorming; **open for more standards (Marc)**
- **Author:** Marc + Claude (brainstorming session)
- **Target document:** `flove/frontend_standards.md`
- **Spec location note:** lives under `docs/superpowers/specs/` in the context repo
  (version-controlled, *outside* `_sidebar.md` so it does not appear in the published
  docsify site).

---

## 1 · Goal & scope

Make **`flove/frontend_standards.md`** the complete, well-structured, single source of
truth for how flove frontends are built — and **upgrade its content**, starting with a
unified complexity model.

**Scope = the frontend standards doc (decision "A").** We do *not* split
`backend_plan.md` into `coordinate-system.md` / `fuzzy-engine.md`, nor reorganize the
backend plan beyond what's needed to remove the frontend-standards duplication.

**In scope**
- `flove/frontend_standards.md` — completed, restructured, and content-upgraded.
- `flove/backend_plan.md` — `§13`/`§14` replaced by a one-line pointer to
  `frontend_standards.md` (kills the duplication; rest of the file untouched).
- `flove/AGENTS.md` `§9` and `flove/overview.md` `§3` — their standards catalogues
  shrink to pointers at `frontend_standards.md`.

**Out of scope**
- No flove **app code** changes (Part VIII migration debt may *imply* future code work
  — tracked, not done here).
- No `coordinate-system` / `fuzzy-engine` split.
- `flovenet/`, `research/`, `development.md`, `theory/` untouched.

---

## 2 · Approach — two phases

Run in order, each its own commit, so we never move text and decide standards in the
same churn.

1. **Phase 1 — Mechanical** (complete · clarify · single source of truth). No standards
   decisions; only relocate, merge, reorganize existing content.
2. **Phase 2 — Substance** (content upgrade). The unified complexity model below, plus
   an audit-then-decide loop for everything else.

---

## 3 · Phase 1 — Mechanical pass

1. **Absorb the deep detail.** Fold the full `backend_plan.md §13` content that
   `frontend_standards.md` currently only *points* to — vocabulary tables,
   Brand/Buttons/Menu-sections, topbar form-element IDs (§13.7), counter internals
   (§13.8), summary-panel internals (§13.9) — into the matching Parts. The doc becomes
   standalone; **no `(§X)` deferrals remain**.
2. **Clarity restructure.** Consistent depth across standards, tightened Part I–VIII
   flow, code examples pulled from flovy where they sharpen a rule. Content-preserving.
3. **One source of truth.** `backend_plan.md §13–14` → one-line pointer;
   `overview.md §3` → pointer; `AGENTS.md §9`'s "look in `backend_plan §13`" → repointed
   to `frontend_standards.md`. Everything else in `backend_plan.md` untouched.
4. **Verify** dead anchors (`§13`, `§14`) + docsify site loads; **commit + push** to
   `marc/context`; update the `standards_catalog` memory (§13 is no longer the source of
   truth → `frontend_standards.md`).

---

## 4 · Phase 2 — The unified complexity model (the core content upgrade)

The headline new standard: **one tier number is a single dial** that sets, together,
*features · topbar · menu · layout breadth · mobile-friendliness*. Today these are
specified piecemeal (§13.1 features, §13.5 topbar) and the menu/layout/mobile axes
aren't tiered at all. This unifies them.

### 4.1 · Complexity categories (tier ↔ formal/technical register)

Keep the seven friendly tier names as primary; attach a **parallel technical /
"formal" register** (a one-word complexity descriptor). The two registers are the same
ladder seen two ways.

| # | Category (friendly) | Formal / technical |
|---|---------------------|--------------------|
| 0 | nano | seed |
| 1 | mini | minimal |
| 2 | basic | simple |
| 3 | normal | medium |
| 4 | advanced | full |
| 5 | super | networked |
| 6 | mega | orchestrated |

**Labeler-driven surfacing.** The technical register is tied to the **labeler
(personality) system**: when the **formal** labeler is active, the app surfaces the
technical complexity terms; friendlier labelers show the casual tier names. *(Reading
confirmed in brainstorming; re-verify against the labeler implementation during
Phase 2.)*

### 4.2 · Layout regions (refines Part IV)

Six named regions, stacked vertically with a three-space **Stage** band in the middle
(2026-06-12 region model):

```
┌──────────────────── TOPBAR (sticky) ────────────────────┐
├──────────────────────── TOP ────────────────────────────┤   optional banner/context
├──────────┬─────────────────────────────┬────────────────┤
│   LEFT   │          CENTER             │     RIGHT      │   ← the Stage band
│ optional │  canonical · mobile-first   │   optional     │
│  rail    │  single-column flow (blogy) │   aux panel    │
├──────────┴─────────────────────────────┴────────────────┤
├──────────────────────── BELOW ──────────────────────────┤   ← Step nav lives here
└──────────────────────── FOOTER ─────────────────────────┘   action bar / badges
```

- **Center** — **mandatory at every tier**. The mobile-first default column; blogy is
  Center-only. Core flow lives here at a comfortable reading measure, centered.
- **Left / Right** — **optional flanking spaces**, progressively unlocked by complexity
  (see 4.5): left = nav rail / secondary controls; right = summary / insights / aux.
- **Top** — optional banner/context strip below the topbar; **Below** — strip above the
  footer that houses **Step nav** (the stepper); **Footer** — action bar / badges.
- **Mobile contract:** only Center is guaranteed. Below the breakpoint, Left/Right/Top/
  Below collapse — into the ☰ menu, a drawer, or stacked under Center. Design Center
  first, enhance outward.
- **Modal** sub-region unchanged (recursive overlays, per Part IV).

### 4.3 · Per-tier topbar types

Named, escalating topbar archetypes (harvested + extended from §13.5):

| Topbar type | Elements (cumulative) |
|-------------|-----------------------|
| **bare** | none |
| **identity** | mark · title · tier-switcher · ☰ |
| **featured** | identity + tier badge · compass · magic labelers |
| **full** | featured + magic-mode variant · app-toggle |
| **full + net** | full + backend/network affordances |
| **full + orch** | full + orchestration affordances |

### 4.4 · Per-tier menu types

Named, escalating menu archetypes. **New standard** — the menu is not tiered today
(§13.7 defines one global Search·Main·Related·Core model). Buckets per §13.7.

| Menu type | Contents |
|-----------|----------|
| **none** | — |
| **minimal** | About only |
| **simple** | language · About |
| **standard** | Main bucket: settings (mode · sound · language) + internal sub-views |
| **full** | Search · Main · Related · Core (all four buckets) |
| **full + net** | full + account / network / publish-target rows |
| **full + orch** | full + multi-instance / orchestration rows |

### 4.5 · Mobile-friendliness ↔ desktop-fullness ladder

The same tier number is also a **responsive breadth** dial — from pure mobile
(Center-only) to full desktop page (Left·Center·Right):

- **nano / mini** — pure mobile: narrow single Center column, max compact (one-hand).
- **basic** — comfortable mobile: roomier single Center column.
- **normal** — adaptive: Center-first, widens on tablet+; *one* collapsible side allowed.
- **advanced** — full desktop page: Left · Center · Right, whole viewport, multi-column.
- **super / mega** — full desktop + extra panes (network / multi-instance).

**Region rule that falls out:** Center is mandatory everywhere; Left/Right unlock by
complexity — first a single collapsible side at `normal`, then full Left·Center·Right at
`advanced+`. **Layout breadth and complexity are the same ladder.**

### 4.6 · The unified table (the deliverable artifact)

| # | Category | Formal | Layout breadth & mobile-friendliness | Regions | Topbar | Menu |
|---|----------|--------|--------------------------------------|---------|--------|------|
| 0 | nano | seed | bare center · ultra-mobile seed | Center (no chrome) | bare | none |
| 1 | mini | minimal | **most mobile** — narrow single column, max compact | Center only | identity | minimal |
| 2 | basic | simple | **comfortable mobile** — roomier single column | Center only | identity | simple |
| 3 | normal | medium | **adaptive** — center-first, widens tablet+; 1 collapsible side | Center (+1 opt. side) | featured | standard |
| 4 | advanced | full | **full desktop page** — whole viewport, multi-column | Left · Center · Right | full | full |
| 5 | super | networked | full desktop + network panes | L·C·R + net | full + net | full + net |
| 6 | mega | orchestrated | full desktop + multi-instance | L·C·R + orch | full + orch | full + orch |

This table (and the supporting 4.1–4.5 detail) lands in `frontend_standards.md`,
reconciling and replacing the current §13.1 tier model and §13.5 topbar table, and
extending Part IV regions.

### 4.7 · Content elements per tier (`entry · labeler · wizard · rater`)

Filled with Marc (2026-06-12 matrix). **Correction vs. an earlier draft:** the
labeler+wizard+rater triad does **not** all enter at `normal` — input richness ramps
earlier and more granularly.

| Category | `entry-*` | `labeler-*` | `wizard-*` | `rater-*` |
|---|---|---|---|---|
| nano | 1 plain field | — | — | — |
| mini | `--main` | — | **1 wizard · inline text** | **heart only** |
| basic | `--main` + Add (`--sibling`) | **1 labeler · changes to random** | 1 wizard · normal text | heart · 3 click-sizes |
| normal | `--main·--alternative·--extra·--note` | **3 labelers** (Formal · Casual · Hotter) | 3 wizards (lovely · joy · wisdom) | heart + 4 subs |
| advanced | all 5 types + nesting | **3 main + 4 teleological** (Lovely · Fatal · Lucky · Random) + `labeler-sub` fan-out | wizards + `wizard-arm--more` fan-out | scoped (4 emoji, main vs extra) |
| super | + affinity-network personalization (F4+) | networked labelers (web-of-trust) | web-of-trust wizard suggestions | networked rating |
| mega | + orchestrated personalization | orchestrated labelers | orchestrated wizards | orchestrated rating |

**Escalation rules:**
- **Rater is heart-based from `mini`:** heart-only → 3 click-sizes (basic) → heart + 4
  subs (normal) → scoped 4-emoji main/extra (advanced).
- **A single wizard from `mini`:** inline text → normal text (basic) → 3 named wizards
  (normal) → `wizard-arm--more` fan-out (advanced).
- **Labelers from `basic`:** 1 (random) → 3 *Formal·Casual·Hotter* (normal) → 3 main +
  4 teleological *Lovely·Fatal·Lucky·Random* + `labeler-sub` (advanced).
- **Entry fields** grow `--main` (mini) → `+--sibling` (basic) → 4-type set (normal) →
  all 5 + nesting (advanced).

### 4.8 · Feedback components per tier (`summary · counters · Summary Insights · Insights · toast`)

> **Naming (2026-06-12):** the old `insights` column is now **Summary Insights** (the
> about→insight progression *inside* the summary panel); a separate **Insights** surface
> covers main areas *beyond* the summary.

| Category | summary | `counter-*` | Summary Insights | toast / splash |
|---|---|---|---|---|
| nano | inline result only | — | — | — |
| mini | minimal result | — | **about slogan** | — |
| basic | static summary + Copy | **expand/collapse timer + clicks** | about section | basic toast |
| normal | summary + magic-phrase swap + Bars chart | arcade chips · **gated unlocks** | about extended section | toast / splash |
| advanced | full panel: live phrase · insights cycle · view toggles · download/copy + 4 charts | full counters | **insights (AI provider call)** | full feedback set |
| super | networked / aggregated summary | networked counters | networked insights | — |
| mega | orchestrated summary | orchestrated counters | orchestrated insights | — |

**Escalation rules:**
- **The "insights" surface is an *about* progression at low tiers** — slogan (mini) →
  section (basic) → extended section (normal) — and becomes the **AI insight-cycle** at
  advanced.
- **Counters from `basic`:** expand/collapse timer + clicks (basic) → arcade chips with
  **gated tier-unlocks** (normal) → full (advanced).
- **Summary** grows inline result → static + Copy (basic) → live phrase + magic-swap +
  Bars chart (normal) → full insight-cycling panel + 4 charts (advanced).

> **Source artifact:** the full 105-cell matrix is editable at
> `~/flove-tiers-matrix.html` (tiers × 15 element columns, numbered cells). The numbered
> export is the canonical record of Marc's per-cell decisions; this spec is the prose
> reconciliation of it.

### 4.9 · Three-level standards hierarchy + `flovy → blogy` rename

A new framing that re-homes some standards:

- **Level 1 — family standards** (the §4 matrix): primitives every app shares
  (tiers, layout regions, topbar/menu types, entry/labeler/wizard, feedback).
- **Level 2 — `blogy`** (the **reference app, renamed from `flovy`**): app-level standards
  and vocabularies that **most level-3 apps inherit**.
- **Level 3 — other apps** that follow blogy's lead.

**Composites move down to level 2.** The **rater is not a family primitive** — `hearts`
and `subemos` are the base categories, and **each becomes a rater when multi-clickable**.
So `rater-*` is removed from the family ELEMENTS group and re-homed in blogy, **split in
two** (`hearts` + `subemos`). The editable matrix carries this as a dedicated **blogy
(level-2)** grid.

**`flovy → blogy` rename — scope = FULL** (Marc, 2026-06-12): app code + filenames +
context docs + memories + live repo. **Not yet executed** — treated as its own carefully
planned task because of blast radius and a blocking hazard:

- **Blast radius:** app repo 407 occurrences / 27 files (filenames, `flovy-*` classes/IDs,
  content, inter-file tier-pop links); context docs 111 mentions (95 in `backend_plan.md`);
  14 memory files + `MEMORY.md` + 2 `project_flovy_*` filenames.
- **🚩 Blocking hazard:** two divergent, **dirty** working copies of `marc/flove` exist
  (`~/Desktop/flove` 82 changed; `~/Documents/flove` 84 changed) on the **same** remote.
  Must be reconciled (pick canonical, commit/stash, align) **before** any rename.
- **Method (when unblocked):** atomic per-file edits (HTML+CSS+JS together to keep
  selector pairing), `git mv` for filenames, update all internal links, then docs, then
  memories; verify with a post-rename `grep` for residual `flovy` (excluding backups in
  `Pictures/_backup`, `Downloads`). Backups + export dumps are **out of scope**.

> **Status (2026-06-12): rename DONE & pushed.** App repo `marc/flove` commit `2e2ad97`
> (then `c16d210`); context docs `marc/context` commit `748aff8`; memories content +
> 4 slug files renamed + `MEMORY.md`/wikilinks fixed. 0 residual `flovy`; `flove`
> family name untouched. Canonical clone = `~/Documents/flove` (Desktop archived).

### 4.10 · Media & Animations per tier

**Media** (`graphic · audio · video`):

| Category | graphic | audio | video |
|---|---|---|---|
| nano | inline SVG mark only | — | — |
| mini | SVG mark + favicon | — | — |
| basic | + category gradient | click sounds (newsound) | — |
| normal | + icon/emoji set | sound engine (depth levels) | — |
| advanced | full SVG icon system + charts | full engine + magic tones | optional embeds |
| super | networked media | shared sounds | shared/streamed |
| mega | orchestrated media | orchestrated audio | orchestrated video |

**Animations** (`Thresholds & Triggers · Transitions/Motion · Reduced-motion`):

| Category | Thresholds & Triggers | Transitions / Motion | Reduced-motion |
|---|---|---|---|
| nano | — | — | respects PRM |
| mini | — | basic CSS transitions | respects `prefers-reduced-motion` |
| basic | counter click thresholds | CSS transitions (tokens) | respects PRM |
| normal | gated-unlock thresholds; compass triggers | motion tokens (fast/medium/slow) | respects PRM |
| advanced | full thresholds (unlocks, celebrate) + JS triggers | full motion system + celebrate anim | PRM gates **CSS + JS** |
| super | networked thresholds | — | respects PRM |
| mega | orchestrated thresholds | — | respects PRM |

**Rule:** reduced-motion (PRM = `prefers-reduced-motion`) is mandatory at **every** tier
(it's already the §I.6 a11y floor); thresholds/triggers escalate from none → counter
clicks (basic) → gated unlocks + compass (normal) → full unlock/celebrate + JS (advanced).

### 4.11 · Layout-nav details & pages per tier

Captures the remaining columns added to the matrix:

| Category | Compass (display) | Footer | Step nav | Auth | System states |
|---|---|---|---|---|---|
| nano–basic | — | — | — | — | — |
| normal | 3 layouts (canonical·random·compact) | stepper nav + badges | 3-step + node nav | — | — |
| advanced | full display-mode switcher | full action bar (copy·share·magic·insight·publish·format) + badges | full 6-step | — | WIP/404 placeholder |
| super | (inherits advanced) | (inherits) | (inherits) | account login (web-of-trust) | "developing these features" placeholder (super reference) |
| mega | (inherits) | (inherits) | (inherits) | orchestrated auth | (inherits) |

*(`Login` / `Error page` rows are first drafts — open for Marc to refine; super's WIP
placeholder page is the existing pattern from §13.1.)*

### 4.12 · Cross-app integration & federation readiness

So the standard stays solid as new apps join and as flove federates with external
networks, the vocabulary + tier model follow these principles (frontend owns 1–3;
4–6 hand off to the backend roadmap):

1. **Stable namespaced keys, not display strings.** Every app / slot / labeler / element
   has a stable ID (`app:blogy`, `slot:add-button`, `labeler:formal`) — the canonical
   CSS-class vocabulary (§13.7) *is* this ID layer. Display text is just one
   labeler-scoped, localized **value** over a stable key. Renames go through the
   versioned deferred-renames pattern so federated peers reconcile cleanly.
2. **Inheritance / override (the three levels).** Level-1 family defaults → level-2
   app (blogy) overrides → level-3 apps inherit, overriding only deltas. A new app
   starts from defaults; minimal per-app surface = minimal drift. The per-app
   vocabulary grid is built for exactly this (one shared slot/labeler structure, values
   per app).
3. **Portable data format.** Vocabulary + tier-matrix export as **versioned JSON**
   (the tool already does), mapping onto the `FloveElement` schema + `asterism_path` +
   coordinate system (backend_plan §3, §A). The **CSS-pure distro** is the portable,
   JS-free artifact other platforms can host.
4. **Provenance & web-of-trust (super/mega).** Networked labelers/wizards/wordings carry
   authorship; affinity-network / web-of-trust weighting (F4+) decides which peer's
   vocabulary a user sees. Federation primitives = F2+ publisher adapter (§6) + flovenet.
5. **i18n as a first-class dimension.** vocabulary = slot × labeler × **language**
   (`.t-en/.t-es` + newlanguage); federation spans locales.
6. **External interop mapping.** A mapping layer bridges flove vocabulary to external
   protocols (Nostr NIP-07/09, oasis/SSB); the LowAI/oasis adaptation is the first target.

**Scope note:** federation itself is a backend concern already roadmapped (F2+, flovenet,
0asis). This spec only commits the *frontend* to be federation-**ready** — principles
1–3 are frontend work; 4–6 are handoffs.

### 4.13 · Canonical naming & taxonomy (2026-06-12)

The matrix tool (`flove/flove-tiers-matrix.html`) is the editable source for these names.

**Group taxonomy (family columns):** `Default` · **Structure** (Viewport reach · Stage
regions · Footer · Surfaces) · **Navigation** (Topbar type · Topbar controls · Menu type ·
Menu contents · Compass · Step nav) · **Input** (Entry fields) · **Assistants** (Labelers ·
Wizards) · **Output** (Summary panel · counters · Summary Insights · Insights · Transient
feedback) · **Media** (graphic · audio · video) · **Motion** (Triggers · Transitions ·
Reduced-motion) · **Theming** (Theme tokens) · **Flows & States** (Onboarding · Extension
forms · Auth · System states).

**Resolved collisions / regroupings:**
- tier register `Formal` → **Default** (kills clash with the `Formal` labeler).
- `labeler-*`/`wizard-*` regrouped under **Assistants**.
- `insights` split → **Summary Insights** (in-summary) + **Insights** (other areas).
- `Mobile / Layout` → **Viewport reach**; Compass + Menu sit under **Navigation**.

**Labelers — two influencer axes over a Default base:**
- **Default** = canonical/base wording.
- **Register** (tone): Formal · Casual · Hotter.
- **Disposition** (fate): Lovely · Fatal · Lucky · Random.
  All Capitalized; `informal` → `Casual`.

**Vocabulary slots:** App title · Tagline · Entry label · Add (CTA) · Wizard label · Rater
prompt · Summary heading · About (body). Per-app extra slots allowed.

**Region model:** Top · [Left · Center · Right = Stage] · Below · Footer — **Step nav lives
in Below** (§4.2).

**Abstract principles** (editable, top of the tool): Stance · Distro · Surface · Region
model · Stepper region · A11y floor · Source of truth · Onboarding · Federation.

**daty exception:** kept `Desired relationship` (not "Relationship goal"); other daty slots
tidied (`Gender`, `About-me`, `Media`, `Profiles`, `Menu`).

---

## 5 · Substance audit (the decide-by-item loop)

Beyond the unified model, run an audit pass on the completed `frontend_standards.md`,
producing a numbered list of proposed substance changes in three buckets — **Marc
decides each (approve / reject / amend); Claude invents no standard unilaterally:**

- **(a) Migration-debt resolutions** (Part VIII) — most already have a stated canonical
  target: i18n `.t-*`, vocab `labeler-*`/`wizard-*`, unify radio group names.
- **(b) Gaps** — missing or under-specified standards surfaced by the audit.
- **(c) Vague rules to tighten** — rules currently too loose to be testable.

---

## 6 · Open — still to standardize

> **Marc flagged "we have to standardize more things."** This section is the slot for
> them.
>
> **Done (folded into §4):** topbar types · menu types · layout regions ·
> mobile-friendliness ladder (§4.1–4.6); content elements entry/labeler/wizard/rater
> (§4.7); feedback components summary/counters/insights/toast (§4.8).
>
> **Still open (candidates not yet standardized):**
> - Color · tokens · theming (accent palette, family vs per-app tokens, dark mode,
>   per-tier token escalation flat → stacking/panel).
> - Surfaces axis (2D → 3D/AR/VR) mapped onto the ladder.
> - Onboarding paso-a-paso per tier (mini/basic = N/A today — confirm).
> - Forms-in-iframe (newlabeler/newwizard/newlanguage/newsound) per tier.
> - _(add as they come up)_

---

## 7 · Verification & workflow

- **Per phase:** grep for dead anchors / broken `(§X)` refs; confirm the docsify site
  loads (`python3 -m http.server 8000`). The repo is clean → each phase is one
  reviewable diff, easy to revert.
- **Commit + push** to `marc/context` (main) per the context-repo workflow; commit
  message carries the prompt + a summary.
- **Memory updates:** `standards_catalog` (source of truth moves to
  `frontend_standards.md`); update `tier_model` if the complexity-category /
  layout-breadth standard changes a recorded fact.

---

## 8 · Boundaries (restated)

`flove/` docs only · no app-code changes · no coordinate-system/fuzzy split · Center is
the one mandatory region · the complexity ladder is the single organizing dial.
