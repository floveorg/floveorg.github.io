<!-- CONTEXT:BEGIN
schema: flove-page/1
id: frontend/experience
path: development/standards/experience.md
trunk: frontend
topic: experience
kind: topic
status: stable
html_place: ["#apps"]
owns: ["UX tiers", "model labels", "pending surfaces"]
updated: 2026-11-21
read_next: ["#exp-levels-03", "#exp-levels-04", "#exp-quality-03", "#exp-quality-05", "#exp-quality-06", "#exp-tours-02", "#exp-quality-09", "#exp-quality-10", "#exp-levels-10", "#exp-quality-11", "#exp-levels-11", "#exp-quality-12", "#exp-tours-05", "#exp-levels-12", "#exp-quality-13", "#exp-levels-13", "#exp-tours-06", "#exp-levels-14"]
supersedes:
  - development/wiki/archive/old/UseCase-adv.md
  - development/wiki/archive/old/apps/onboarding-copy.md
  - development/wiki/archive/old/browsy/TESTING.md
  - development/wiki/archive/old/browsy/browsy-questions.md
  - development/wiki/archive/old/browsy/pre-build/04-myfamily-profile.md
  - development/wiki/archive/old/browsy/pre-build/08-model-labels.md
  - development/wiki/archive/old/browsy/pre-build/11-ui-pending.md
  - development/wiki/archive/old/browsy/spec.md
  - development/wiki/archive/old/plans/2026-06-18-nety-frontend-build.md
  - development/wiki/archive/old/plans/2026-11-17-appy-authy-mynet.md
  - development/wiki/archive/old/plans/2026-11-20-appy-dashboard-redesign.md
  - development/wiki/archive/old/plans/central-backend.md
  - development/wiki/archive/old/proposals/frontend-wizy.md
  - development/wiki/archive/old/research/vr_interfaces.md
  - development/wiki/archive/old/root/adoption.md
heavy: false
CONTEXT:END -->

# Experience

> **Stable page.** Migrated from the pre-cutover sources on 2026-11-21.
> The chapters below are the only owners; the child plan records source history.


<a id="css-abstraction-checklist"></a>
## CSS abstraction checklist (§13.16)

> Source: `development/wiki/archive/old/root/adoption.md#css-abstraction-checklist-1316` (archived 2026-11-21).

**Trunk status (2026-11-15): no app links shared CSS.** Every app in the trunk is
self-contained — it carries its own palette and, where it uses the family skin,
an inlined copy of `flove.css` pruned to the components it actually renders
(Raty and Socy are the reference for that pruning).

| App | Shared CSS | Tokens | Notes |
|---|:---:|---|---|
| all 48 routing apps | — (inline) | per-app `--app-accent*`, `--ink`, `--line`, `--panel` | no `href` to `addons/` anywhere |
| `addons/code/css/flove.css` | reference copy | canonical token block | shipped in the offline package, never loaded at runtime |

The canonical tokens (`--ink`, `--line`, `--card`, `--signal`) live in that
reference file; apps redeclare only their accent overrides. `.flove-focus`,
`.flove-selected` and `.flove-lift` remain the shared interaction vocabulary —
they travel inside the inlined copy, not through a stylesheet link.

## Onboarding copy

> Source: `development/wiki/archive/old/apps/onboarding-copy.md#shared-shape` (archived 2026-11-21).

Every 10-step sequence follows the same rhythm: welcome · the one idea · the
first field · the main action · a second layer · review · save/export · privacy ·
a power tip · done/start again.

The full 30-app table is owned by
[`plans/frontend/experience.md#app-blocks`](../wiki/plans/frontend/experience.md#app-blocks);
`language.md` links to the same table. No app copy is restated here.

## Central navigation

> Source: `development/wiki/archive/old/plans/central-backend.md#central-navigation-bottom-bar` (archived 2026-11-21).

Central apps share a 48px bottom bar injected by `flove.js`: logo left, full-screen
menu, chapters mirroring `apps/`, two levels (Category → App), current app from
the URL. No per-app topbar. Full spec:
[`plans/backend/systems.md#central-navigation-bottom-bar`](../wiki/plans/backend/systems.md#central-navigation-bottom-bar).

<a id="model-labels"></a>
## Model labels — Else and the two Browsy chips

> Source: `development/wiki/archive/old/browsy/pre-build/08-model-labels.md` (archived 2026-11-21).

**Else** was a dashed chip below Authy meaning “everything outside the flove
loop”. It had no data model, owner, class or index page. **Decided 2026-11-18:
retire the chip** (O24=B); the decentral diagram removes the chip and its
Authy→Else arrow.

**Browsy** appears twice because it is one product with two roles:

- **Browsy entry** — popup, bridge, “open Authy”.
- **Browsy host** — vault, records, groups, Wizy, peer pulls.

Use: **Browsy** (product), **Browsy extension** (installed MV3/Firefox
artifact), **Browsy entry**, **Browsy host**, **Browsy index**. No third meaning.

## Browsy and Nety UI (pending)

> Source: `development/wiki/archive/old/browsy/pre-build/11-ui-pending.md` (archived 2026-11-21).

Status: pending; design only, no code. Use existing flove tokens, EN/ES copy
pattern, accessibility rules and extension boundaries. No new UI framework.

Browsy surfaces: entry popup, host workspace, Authy ladder, MyFamily editor,
MyNet local, Wizy panel, settings/security. Constraints: EN+ES first, no remote
fonts/CDN/code, no private key or P record in the UI layer, locked/empty/error/
offline states, narrow-screen fit.

Nety surfaces: social feed, public card, moderation, public group card, network
status. S-only; no Local; Nety is a client in Browsy, not a local node; no
moderation UI before the gateway/curator contract.

Gate: do not implement either UI until the local Browsy slice is defined, copy
uses settled vocabulary, screen inventory/states are accepted, and the bridge/
security boundary is signed off.

## Libs and VR research

The flove-libs insights and the abandoned Godot/VR research are owned by
[`plans/frontend/experience.md#libs-insights`](../wiki/plans/frontend/experience.md#libs-insights)
and [`.md#vr-research`](../wiki/plans/frontend/experience.md#vr-research).
They are historical evidence, not current build targets.

<a id="exp-levels-03"></a>
## Experience flags noted in the docs, with a closing criterion

> Owner: experience. Canonical UX item for `levels-03`; evidence lives in the register.

<a id="exp-levels-04"></a>
## Level 3: §13.18 minimums

> Owner: experience. Canonical UX item for `levels-04`; evidence lives in the register.

<a id="exp-quality-03"></a>
## Ana/Bob/Charlie fixtures: expected data and tampered/expired/revoked bundles

> Owner: experience. Canonical UX item for `quality-03`; evidence lives in the register.

<a id="exp-quality-05"></a>
## A2 mobile+i18n: structure ready, RTL and externalisation pending

> Owner: experience. Canonical UX item for `quality-05`; evidence lives in the register.

<a id="exp-quality-06"></a>
## Phase A gate: div balance, JS parse and handler resolution

> Owner: experience. Canonical UX item for `quality-06`; evidence lives in the register.

<a id="exp-tours-02"></a>
## REV01: review the tours

> Owner: experience. Canonical UX item for `tours-02`; evidence lives in the register.

<a id="exp-quality-09"></a>
## Response budgets: bridge, key and vouch chain

> Owner: experience. Canonical UX item for `quality-09`; evidence lives in the register.

<a id="exp-quality-10"></a>
## WebCrypto Ed25519 primary with Firefox/Safari fallback

> Owner: experience. Canonical UX item for `quality-10`; evidence lives in the register.

<a id="exp-levels-10"></a>
## Audit the remaining sections: scope and criterion

> Owner: experience. Canonical UX item for `levels-10`; evidence lives in the register.

<a id="exp-quality-11"></a>
## Implement the web quality gates in Quality

> Owner: experience. Canonical UX item for `quality-11`; evidence lives in the register.

<a id="exp-levels-11"></a>
## Implement the frontend degree ladder in Levels

> Owner: experience. Canonical UX item for `levels-11`; evidence lives in the register.

<a id="exp-quality-12"></a>
## Counter catalogue §13.8: when to show them and when to stay quiet

> Owner: experience. Canonical UX item for `quality-12`; evidence lives in the register.

<a id="exp-tours-05"></a>
## Implement all onboarding tours and copy in Tours

> Owner: experience. Canonical UX item for `tours-05`; evidence lives in the register.

<a id="exp-levels-12"></a>
## Implement User Experience ladder in Levels

> Owner: experience. Canonical UX item for `levels-12`; evidence lives in the register.

<a id="exp-quality-13"></a>
## Execute accessibility report in Quality

> Owner: experience. Canonical UX item for `quality-13`; evidence lives in the register.

<a id="exp-levels-13"></a>
## Execute the experience-level plan in Levels

> Owner: experience. Canonical UX item for `levels-13`; evidence lives in the register.

<a id="exp-tours-06"></a>
## Execute the advanced-review plan in Tours

> Owner: experience. Canonical UX item for `tours-06`; evidence lives in the register.

<a id="exp-levels-14"></a>
## Execute the visual-craft plan in Levels

> Owner: experience. Canonical UX item for `levels-14`; evidence lives in the register.

## Source map

| Archived source | Date | Stable home |
|---|---|---|
| `archive/old/UseCase-adv.md` | 2026-08-01 | development/standards/experience.md |
| `archive/old/apps/onboarding-copy.md` | 2026-11-17 | development/standards/experience.md |
| `archive/old/browsy/TESTING.md` | 2026-08-01 | development/standards/experience.md |
| `archive/old/browsy/browsy-questions.md` | 2026-08-01 | development/standards/experience.md |
| `archive/old/browsy/pre-build/04-myfamily-profile.md` | 2026-11-17 | development/standards/experience.md |
| `archive/old/browsy/pre-build/08-model-labels.md` | 2026-11-17 | development/standards/experience.md |
| `archive/old/browsy/pre-build/11-ui-pending.md` | 2026-11-18 | development/standards/experience.md |
| `archive/old/browsy/spec.md` | 2026-11-17 | development/standards/experience.md |
| `archive/old/plans/2026-06-18-nety-frontend-build.md` | 2026-06-18 | development/standards/experience.md |
| `archive/old/plans/2026-11-17-appy-authy-mynet.md` | 2026-11-17 | development/standards/experience.md |
| `archive/old/plans/2026-11-20-appy-dashboard-redesign.md` | 2026-11-20 | development/standards/experience.md |
| `archive/old/plans/central-backend.md` | 2026-08-01 | development/standards/experience.md |
| `archive/old/proposals/frontend-wizy.md` | 2026-11-19 | development/standards/experience.md |
| `archive/old/research/vr_interfaces.md` | 2026-08-01 | development/standards/experience.md |
| `archive/old/root/adoption.md` | 2026-08-01 | development/standards/experience.md |

Chapters without a separate source row are `milestone-only`: they are
specified from the register (hitos and tasks) and remain owned here.
