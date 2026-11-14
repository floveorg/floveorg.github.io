# flove-skills

Personal skill library for Claude Code (and compatible agents).

## Layout

One folder per skill: `<skill>/SKILL.md` plus the assets it needs
(`references/`, `scripts/`, `evals/`, …). Skills live and load from
`~/.agents/skills/`, which is a **symlink** to this folder
(`development/standards/skills/`) — there is exactly **one real copy** on disk.

The **Solo-scoped** skills (`upgrady`, `exporty`, `updaty-apk`) stay
here with the rest; they're indexed and described in
[`../apps/README.md`](../apps/README.md).

## Choosing a skill

| Need | Skill |
|---|---|
| Polish display copy only | `texty` |
| Align internal names / vocabulary / matrix | `vocaby` (superset of texty) |
| Add languages + the worldball | `translaty` |
| Run the full polish pipeline | `optimizy` |
| Structured Q&A / project review | `questy` or `questy1` |
| Interview the owner about an app | `questy-flove` |
| Render a Q&A as an HTML form | `questy-html` |
| Explore 5–10 logo sketches, then the full study | `brandy` (two stages) |
| Propagate a chosen mark everywhere | `rebrandy` |
| Quick page/site publish | `updaty-web` |
| Heavy release: packages, sw.js, all repos | `upgrady` |
| Android APK | `updaty-apk` |
| Export/share audit (§13.12) | `exporty` |
| Validity / a11y / mobile / i18n | `validaty` |
| Narrate a text to MP3 | `narraty` |
| Blog article | `blogy` |

**App registration:** when a chosen logo/identity is applied to an app, follow
[`app-registration.md`](app-registration.md) for the apps-full full card +
cube caption, category/background classes, the development tree and the slogan
propagation.

## How it lives in the repo

- This folder is tracked **directly in the flove repo** (no separate embedded
  git repo, no gitlink). Updates happen here and are committed to flove `main`.
- The public site publishes it under `development/standards/skills/` via
  `publish-web.sh` (it's on the GitHub keep-list), so flove.org serves the
  skills read-only.
- `~/.agents/skills` → `development/standards/skills` is a symlink, so editing
  through either path touches the same files.

## Secrets rule

Skills are designed to **reference** secret locations, never **contain** secrets:

- Tokens: `~/agents/token-github-flove.md` (never inline, never printed).
- Android signing key: `~/flove-apk/android.keystore` (never committed).
- Remote URLs are kept credential-free; auth comes from the git credential
  helper, not from the remote URL.

Rules enforced by convention (no secrets in this repo):

1. Never embed a token, password, key, or cookie in a skill or its assets.
   The whole file may only name the *file* where the secret lives.
2. `.gitignore` excludes `*-workspace/` (eval scaffolding), `*.skill` (legacy
   exports), and scratch files with machine-specific paths.
3. Before every push, grep the tree and the pending diff for secret patterns:
   `github_pat_`, `ghp_`, `gho_`, `ghs_`, `glpat-`, private key blocks.
4. `git push` only pushes refs — `.git/config` (which may hold local remote
   credentials) is never transferred. Never `--mirror`-push.

## Health check

Run `python3 tools/check-skills.py` after editing a skill. It validates each
`SKILL.md` frontmatter (valid YAML, unique `name`, non-empty `description`),
flags secret-looking strings and warns on overlong descriptions. A malformed
frontmatter is not cosmetic: it silently removes the skill from the agent's
loaded set.

## Publishing split

Two skills cover two different jobs — keep the light one light:

- **`updaty-web`** — quick publish of the main site only. Commits the pending
  source (after listing it and asking), pushes `main` to Gitea and runs
  `publish-web.sh` for GitHub. No package zip, no `sw.js`, no vocabulary sync,
  no subdomains, no all-repo/token checks.
- **`upgrady`** — heavy release. Refreshes packages and artifacts
  (`flove-localhost.zip`, `sw.js`, the vocabulary index), runs the distro and
  repository/token checks, and publishes the main site and subdomains only when
  explicitly asked.
- **`updaty-apk`** — the Android APK, independent of both.

Rule of thumb: page/site update → `updaty-web`; package, artifact or
all-targets release → `upgrady`.

## Publish

The skills ship with the flove repo — commit here and the site (flove.org,
`development/standards/skills/`) updates via the normal flove publish flow
(`publish-web.sh`). There is no separate skills remote to push to.
