# flove · Standards — the matrix (stable index)

The stable index of the flove frontend standards. This file changes rarely: it
only **names** each standard and points to where it's specified. The full text
lives once — in `frontend/frontend.md`, or, for the biggest standards, in its own
`frontend/<topic>.md` or root chapter such as `vocabulary.md`; keep descriptions
*there*, not here. An
interactive, navigable **vocabulary matrix** (labelers × slots, filled by
`/texty` level 3) is [`vocabulary.html`](vocabulary.html) (renamed 2026-08-03 from
`flove-tiers-matrix.html`, flat at the standards root since 2026-11-19).

**The files of this sub-book:**

| File | What | Nature |
|------|------|--------|
| [`contract.md`](contract.md) | the **values and the floor** every app honours | short · stable · non-negotiable |
| [`frontend/frontend.md`](frontend/frontend.md) | the **opt-in catalogue** (§13) + regions · elements · conventions | long · grows |
| [`worldview.md`](worldview.md) | the **philosophy** — what flove is, the whole map, ambition | ethos |
| [`adoption.md`](adoption.md) | the **per-page gates** (§14) — what is enforced | per-page gates |
| [`backend.md`](backend.md) | the **all-backends overview** — architecture, roadmap, strategic persistence (§10) and Central (§11) | long · deep spec |
| [`puzzy.md`](puzzy.md) | the **extended-definition standard** — entries, senses, thesaurus relations, frames, annotations, and how they attach to app data | normative · ships F5 |

**Implementation plans & cross-plan conflicts** live in [`debates/plans/`](debates/plans/). Check [`debates/plans/conflicts.md`](debates/plans/conflicts.md) before starting work.

## The catalogue at a glance (§13 → `frontend/frontend.md`)

Standards with their own deep chapter link to `frontend/…`; the rest live inline in `frontend/frontend.md`.

| § | Standard | One line |
|---|----------|----------|
| 13.1 | [**Tier model**](debates/proposals/frontend-tiers.md) | ⏹ design sketch only — moved to debates, not in this trunk |
| 13.2 | **i18n** | pure-CSS `.t-en`/`.t-es` swap; shared `flove:lang` default |
| 13.3 | **Forms-in-iframe** | user-extensible: newlabeler / newwizard / newlanguage / newsound |
| 13.4 | **Compass** | re-presents contents *within* the current surface |
| 13.5 | **Topbar** | which controls the topbar carries (grows with app depth) |
| 13.6 | **Onboarding** | **MANDATORY** — loud first time, discrete after |
| 13.7 | [**Canonical vocabulary**](vocabulary.md) | `entry-` `labeler-` `wizard-` `step-` … (was `ray-`/`bot-`) |
| 13.8 | [**Counters**](frontend/counters.md) | floating arcade chips (no tier gate) |
| 13.9 | [**Summary panel**](frontend/summary.md) | phrase + editable summary box + global Copy + Magic General/Custom · Share (Save/Appy/Telegram/More) |
| 13.10 | **Nav-tab title** | `<App> · FLOVE` (favicon · name · brand) |
| 13.11 | **Surfaces** | the medium axis (hardware · 2D · 3D · AR · VR) |
| 13.12 | [**Export & share**](frontend/export.md) | **JSON-only**: `flove-portrait/1` + the Appy renderer; `blogy` and `fivy` keep multi-format exports as documented exceptions; keys/souls are standard targets |
| 13.13 | **Locking** | method (Low · Mid · High) × trigger (pass · threshold) |
| 13.14 | **Contrast / theme** | light↔dark ◐ toggle; shared `flove:theme` key |
| 13.15 | [**Publish to Appy**](frontend/publish.md) | Share → **Appy** one-click (local play) + Appy auto-render; writer trio retired; manual upload fallback |
| 13.16 | **CSS pattern catalog** | shared interaction classes (`flove-focus`, `flove-lift`, …) |
| 13.17 | **Transparent stats** | local, clearable time stats — the keys-advanced model (no third party) |
| 13.18 | **Usability levels** | 3 minimum · 4 function · 5 craft, per section |
| 13.19 | **Design tokens** | colours, radii, motion — from `flove.css` |
| 13.20 | **Single-file app skeleton** | doctype → head → flove-bar → main → script |
| 13.21 | **Brand marks** | the sprout and the genesiacal pair |
| 13.22 | **Harvested UX patterns** | the family's recurring interaction ideas |
| 14 | **Adoption gates** | per-page gates → [`adoption.md`](adoption.md) |

**Wizy** has its own draft: [`debates/proposals/frontend-wizy.md`](debates/proposals/frontend-wizy.md) — operating
areas (custom magic, field influence, agent prompts, embeds, questy-flove,
Browsy federation, NetyBrowsy permissions), pending its standardization pass.

The `§13.x` labels are **canonical** — references across the whole context book
resolve to them here, regardless of which file physically hosts the section.
**Trunk apps** (`apps/`) are the canonical spec; the **Solo** distro
(`apps/`, local-first) is the reference fallback — see
[`apps/README.md`](apps/README.md).

*If a standard outgrows `frontend/frontend.md`, split it to `frontend/<topic>.md` and
leave a pointer in that file and in this table — deepen without moving the index.*

## Working with these standards

The standards are the **dev-docs** chapter of flove. They live in the
`development/standards/` book (published at `flove.org/development/standards/`) —
the canonical home of the whole context pack (docs · standards · theory). This
`standards/` folder is that home's source of truth.

- **Consult** — open `development/standards/index.html` and use its sidebar +
  built-in search, or ask the **agent search**: the knowledge base under
  `docs/theory/kb/` indexes the whole corpus, these standards included. It runs
  on FTS keyword search out of the box (`python3 ingest.py --reset` to rebuild,
  `retrieve.py` / `serve.py` to query); semantic embeddings are optional and
  **kept off for now**, so no heavyweight model is needed.
- **Edit** — change the `.md` file that *owns* the fact (one home per fact; every
  other file points to it). Edit the markdown here — the standalone
  `standards-tour.html` page is maintained separately, so don't hand-edit it to
  change a standard. When you add or rename a doc, update `development/standards/_sidebar.md`
  so it shows in the docsify nav.
- **Edit in the browser** — run `./tools/serve-dev.sh` and open
  `http://127.0.0.1:8642/development/standards/`. On localhost an **✎ Edit page**
  button appears: the rendered page becomes editable (toolbar for bold, headings,
  lists, links…), and **Save** / `Ctrl+S` writes the `.md` back to disc and
  reloads. Only the blocks you touched are re-serialized; untouched blocks keep
  their exact source text and line wrapping. The previous file is copied to
  `~/.cache/flove-wiki-edits/` on every save; **Cancel** / `Esc` discards. This
  needs `tools/serve-edit.py` (started by `serve-dev.sh`) — the public site is
  static, so the button never appears there. Use the `127.0.0.1` URL rather than
  `localhost`: it is a separate origin from the installed offline service
  worker, so dev always serves the file you just edited.
  The editor itself is a reusable docsify plugin (MIT) under
  `tools/docsify-edit/`; this wiki loads the built copy from
  `vendor/docsify-edit.js`. A standalone demo lives at
  `/addons/docsify-edit/` — run
  `python3 tools/serve-edit.py --editable addons/docsify-edit` to edit it.
- **Publish** — commit + push (scoped) to Gitea `marc/flove`; the live site
  updates via `updaty` (quick main-site publish). Packages and build
  artifacts (`flove-localhost.zip`, `sw.js`, vocabulary) are the heavy
  `updaty4` path. The Android TWA app updates via `updaty-apk` (rebuild +
  GitHub Release); content updates automatically (web wrapper).

## Development tools

### Interview pattern (questy-html)

Design-question interviews follow a standardized HTML form pattern (reference:
`flove-decisions-interview.html`). Key conventions:

- **"don't keep" checkbox** per question — excludes the question from the copied
  prompt and frozen HTML. State stored as `qN_skip` in localStorage.
- **History button** — appends kept answers (timestamped) to `localStorage`.
  A `buildMakingOf()` function generates a standalone `decisions.html` from this
  history, which feeds into `development/standards/decisions/decisions.html`.
- **localStorage keys**: `qN` (picks), `qN_skip` (boolean), `__intent`,
  `__extra`, `__addon`, `flove-history`.
- **Bar buttons**: ★ suggested, expand all, clear, save frozen HTML, copy prompt,
  save to history.
- Full spec in `~/.agents/skills/questy-html/SKILL.md` §Standardized Interview Pattern.
