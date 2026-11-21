<!-- CONTEXT:BEGIN
schema: flove-page/1
id: ai/skills
path: development/standards/skills.md
trunk: ai
topic: skills
kind: topic
status: stable
html_place: ["#ai"]
owns: ["Skill procedures and decisions", "questy decisions"]
updated: 2026-11-21
read_next: ["#skill-skills-02", "#skill-skills-03", "#skill-skills-05", "#skill-skills-06", "#skill-skills-07", "#skill-skills-08", "#skill-skills-09", "#skill-skills-11", "#skill-skills-14", "#skill-skills-15", "#skill-skills-16", "#skill-skills-17", "#skill-skills-18", "#skill-skills-19", "#skill-skills-20", "#skill-skills-21", "#skill-skills-22", "#skill-skills-23", "#skill-skills-24"]
supersedes:
  - development/wiki/archive/old/apps/README.md
  - development/wiki/archive/old/proposals/frontend-wizy.md
  - development/wiki/archive/old/questy-proposals.md
  - development/wiki/archive/old/standards.md
  - development/wiki/archive/old/skills-library.md
heavy: false
CONTEXT:END -->

# Skills

> **Stable page.** Migrated from the pre-cutover sources on 2026-11-21.
> The chapters below are the only owners; the child plan records source history.


## Solo-scoped skills

> Source: `development/wiki/archive/old/apps/README.md#solo-scoped-skills` (archived 2026-11-21).

These skills live in `skills/` and build, audit or ship the local-first distro:

| Skill | Path | Scope |
|---|---|---|
| `archive/old/skills-library.md` | 2026-11-19 | development/standards/skills.md |
| **updaty4** | `skills/updaty/heavy.md` | heavy release: packages (`flove-localhost.zip`), `sw.js`, vocabulary, all-repo checks; `updaty5` adds subdomains |
| **exporty** | `skills/exporty/SKILL.md` | audit an app's export: `flove-portrait/1` JSON + Appy renderer |
| **updaty-apk** | `skills/updaty-apk/SKILL.md` | recompile and publish the Android TWA to GitHub Releases |

`updaty` (quick publish of flove.org) is **not** Solo-scoped — it ships the whole
web, including this standards book. The heavy package/artifact/all-targets
release path is `updaty4`.

<a id="skill-skills-02"></a>
## Question template with batches and A/B/C options

> Owner: skills. Canonical procedure for `skills-02`; no second skill copy.

<a id="skill-skills-03"></a>
## JSON backbone map: routing, APP_ROUTING and envelopes

> Owner: skills. Canonical procedure for `skills-03`; no second skill copy.

<a id="skill-skills-05"></a>
## Config precedence

> Owner: skills. Canonical procedure for `skills-05`; no second skill copy.

<a id="skill-skills-06"></a>
## questy-all default bundle

> Owner: skills. Canonical procedure for `skills-06`; no second skill copy.

<a id="skill-skills-07"></a>
## Flove profile of an app

> Owner: skills. Canonical procedure for `skills-07`; no second skill copy.

<a id="skill-skills-08"></a>
## Skill-library gate

> Owner: skills. Canonical procedure for `skills-08`; no second skill copy.

<a id="skill-skills-09"></a>
## skilly gate

> Owner: skills. Canonical procedure for `skills-09`; no second skill copy.

<a id="skill-skills-11"></a>
## First-match override

> Owner: skills. Canonical procedure for `skills-11`; no second skill copy.

<a id="skill-skills-14"></a>
## Verifiable local backup

> Owner: skills. Canonical procedure for `skills-14`; no second skill copy.

<a id="skill-skills-15"></a>
## Development-log entry

> Owner: skills. Canonical procedure for `skills-15`; no second skill copy.

<a id="skill-skills-16"></a>
## Identity and section icons

> Owner: skills. Canonical procedure for `skills-16`; no second skill copy.

<a id="skill-skills-17"></a>
## Mini-diagram and Mermaid thread

> Owner: skills. Canonical procedure for `skills-17`; no second skill copy.

<a id="skill-skills-18"></a>
## JSON ↔ HTML card parity

> Owner: skills. Canonical procedure for `skills-18`; no second skill copy.

<a id="skill-skills-19"></a>
## Narrated MP3

> Owner: skills. Canonical procedure for `skills-19`; no second skill copy.

<a id="skill-skills-20"></a>
## Publish and release

> Owner: skills. Canonical procedure for `skills-20`; no second skill copy.

<a id="skill-skills-21"></a>
## Heavy release

> Owner: skills. Canonical procedure for `skills-21`; no second skill copy.

<a id="skill-skills-22"></a>
## TWA APK/AAB

> Owner: skills. Canonical procedure for `skills-22`; no second skill copy.

<a id="skill-skills-23"></a>
## Skills library

> Owner: skills. Canonical procedure for `skills-23`; no second skill copy.

<a id="skill-skills-24"></a>
## Wizy skill plan

> Owner: skills. Canonical procedure for `skills-24`; no second skill copy.

## Choosing a skill

> Source: `development/wiki/archive/old/skills-library.md` (archived 2026-11-21).

| Need | Skill |
|---|---|
| Polish display copy only | `texty` |
| Align internal names / vocabulary / matrix | `texty` (level 3) |
| Add languages + the worldball | `translaty` |
| Polish one file or page | `optimizy` |
| Full app / cluster | run `/optimizyN` on each in-scope page |
| Structured Q&A / project review | `questy` (recommended) or `questy-all` |
| Interview the owner about an app | `questy-flove` |
| Render a Q&A as an HTML form | `questy-html` |
| Full logo pipeline: sketch → study → placement → tour | `brandy` |
| Compact Excalidraw mini → ×3 Mermaid thread | `diagramy` |
| Quick page/site publish | `updaty` |
| Heavy release: packages, sw.js, all repos | `updaty4` |
| Backup media + repositories | `backy` |
| Android APK | `updaty-apk` |
| Export audit: JSON + renderer | `exporty` |
| JSON backbone after apps/ commits | `jsony` |
| Validity / a11y / mobile / i18n / JSON + UX | `validaty` |
| Narrate a text to MP3 | `narraty` |
| Blog article | `blogy` |
| Skills library health check | `skilly` |

Questy subskills (`questy-all`, `questy-html`, `questy-flove`) use the core
`questy` skill for the main process and add their own catalogue.

## Secrets rule

> Source: `development/wiki/archive/old/skills-library.md` (archived 2026-11-21).

Skills reference secret **locations**, never values:

- Tokens: `~/agents/token-github-flove.md` (never inline, never printed).
- Android signing key: `~/flove-apk/android.keystore` (never committed).
- Remote URLs stay credential-free; auth comes from the git credential helper.

Never embed a token, password, key or cookie in a skill or its assets; keep
`*-workspace/`, `*.skill` and scratch files out of git; grep for
`github_pat_`, `ghp_`, `gho_`, `ghs_`, `glpat-` and private-key blocks before a
push; `git push` pushes refs only, never `--mirror`.

## Publishing split

> Source: `development/wiki/archive/old/skills-library.md` (archived 2026-11-21).

- **`updaty`** — quick publish of the main site only.
- **`updaty4`** — heavy release: packages, `sw.js`, vocabulary, all-repo checks;
  `updaty5` adds subdomains.
- **`updaty-apk`** — the Android APK, independent of both.

## Source map

| Archived source | Date | Stable home |
|---|---|---|
| `archive/old/apps/README.md` | 2026-11-09 | development/standards/skills.md |
| `archive/old/proposals/frontend-wizy.md` | 2026-11-19 | development/standards/skills.md |
| `archive/old/questy-proposals.md` | 2026-11-15 | development/standards/skills.md |
| `archive/old/standards.md` | 2026-08-01 | development/standards/skills.md |

Chapters without a separate source row are `milestone-only`: they are
specified from the register (hitos and tasks) and remain owned here.
