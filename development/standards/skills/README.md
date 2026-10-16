# flove-skills

Personal skill library for Claude Code (and compatible agents).

## Layout

One folder per skill: `<skill>/SKILL.md` plus the assets it needs
(`references/`, `scripts/`, `evals/`, …). Skills live and load from
`~/.agents/skills/`, which is a **symlink** to this folder
(`development/standards/skills/`) — there is exactly **one real copy** on disk.

The **Solo-scoped** skills (`upgrady`, `exporty`, `updaty-apk`) stay
here with the rest; they're indexed and described in
[`../solo/README.md`](../solo/README.md).

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

## Publish

The skills ship with the flove repo — commit here and the site (flove.org,
`development/standards/skills/`) updates via the normal flove publish flow
(`publish-web.sh`). There is no separate skills remote to push to.
