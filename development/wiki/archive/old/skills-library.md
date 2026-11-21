# Skills library — archived README sections

> Moved out of `skills/README.md` on 2026-11-18. The live index is the verified
> table in `https://flove.org/development/index.html`; each skill's own
> `SKILL.md` is the source for what it does. This file keeps the prose that used
> to duplicate them.

## Choosing a skill

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
| Place a chosen mark: tree, launcher, catalog, tab | `brandy` (stage 3) |
| Compact Excalidraw mini → ×3 Mermaid thread | `diagramy` |
| Rewrite a mark, name or slogan everywhere | `brandy` (rebrand) |
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

App registration is stage 3 of `brandy/SKILL.md`.

## Secrets rule

Skills reference secret **locations**, never values:

- Tokens: `~/agents/token-github-flove.md` (never inline, never printed).
- Android signing key: `~/flove-apk/android.keystore` (never committed).
- Remote URLs stay credential-free; auth comes from the git credential helper.

Conventions:

1. Never embed a token, password, key or cookie in a skill or its assets.
2. `.gitignore` excludes `*-workspace/`, `*.skill` and scratch files with
   machine paths.
3. Before a push, grep the tree and the diff for `github_pat_`, `ghp_`, `gho_`,
   `ghs_`, `glpat-` and private-key blocks.
4. `git push` pushes refs only; never `--mirror`.

## Health check

`/skilly` is the gate — see
`https://flove.org/development/standards/skills/skilly/SKILL.md`. It is
the library gate after a skill edit, and `development/scripts/check-distro.sh` runs the same script.

## Publishing split

- **`updaty`** — quick publish of the main site only: commits the pending source
  after listing it, pushes `main` to Gitea, runs `publish-web.sh`.
- **`updaty4`** — heavy release: packages, `sw.js`, the vocabulary index, the
  distro and token checks; `updaty5` adds subdomains.
- **`updaty-apk`** — the Android APK, independent of both.

Rule of thumb: page/site update → `updaty`; package, artifact or all-targets
release → `updaty4`.

## Publish

The skills ship with the flove repo; the site updates via `publish-web.sh`.
There is no separate skills remote.
