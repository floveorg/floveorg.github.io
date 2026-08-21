---
name: updaty-web
description: >-
  Publish the project's live website (flove.org by default) by building a
  FILTERED subset of the latest committed changes and pushing it to the GitHub
  repo floveorg/floveorg.github.io, which is served by GitHub Pages at flove.org.
  Gitea tracks the full dev workspace; the public site only gets the
  web-relevant subset (see development/standards/scripts/publish-web.sh).
  Use whenever the owner (Marc by default) says "updaty-web", "update the web",
  "publish the site", "push flove to the web", "deploy flove.org", "actualiza la
  web", "sube esto a flove.org", or otherwise asks to make the current state of
  the project visible on the live site. Trigger even without the exact words —
  any request to make committed work appear on the public flove.org counts. It
  does NOT create commits: it takes the already-committed local `main`, pushes
  any pending commits to Gitea (`origin`) first, then mirrors `main` to GitHub —
  so commit your work first and it handles both pushes. Before publishing it
  regenerates the offline service worker (`sw.js`) from committed HEAD and
  commits it if changed, so the live site always has a fresh precache list.
  Read-only toward the working tree otherwise; never stages or commits the
  owner's in-progress source edits. Does NOT rebuild `flove.zip` — use skill
  `upgrady` for that. Flove-first by default; override via the personal config
  (see CONFIG.md).
---

# updaty-web — publish flove.org via GitHub Pages

flove.org is hosted on **GitHub Pages** from `floveorg/floveorg.github.io` (branch `main`,
root folder). The local repo `~/Documents/flove` is the owner's source of truth, synced
to Gitea (`localhost:3000/marc/flove`, remote `origin`). This skill first pushes any
pending commits on `main` to Gitea, then mirrors `main` to GitHub; Pages rebuilds and
flove.org shows it in ~1 min.

## Personal config

This skill ships with flove-first defaults. To fork/reuse it for another
project, create a personal config that overrides the defaults instead of
editing the skill (see `development/standards/skills/CONFIG.md`): a shared
`~/.config/flove/skills-config.yml`, a per-skill `settings.yml`, a hidden
`.settings`, or a `config.yml` in the skill folder. Only the keys you set
change; everything else falls back to these defaults.

## Scope — MAIN SITE + project subdomain deploys

`floveorg/floveorg.github.io` → `flove.org`, plus each project's own GitHub Pages repo:
- **risa** → `floveorg/risa` → `risa.liberada.net`
- **ama** → `floveorg/ama` → `ama.liberada.net`
- **liberada.net** → `floveorg/liberada` → `liberada.net`
- **lowai** → `LowAiorg/web` → `lowai.org`

These publish on their OWN, not via publish-web.sh:
- **Blog** (`flove.org/development/blog`): the Hugo blog lives IN this repo at
  `development/blog` (source + built HTML committed in place, no `/public`
  segment). Rebuild the output with `./build-blog.sh build` (or `publish`,
  which also commits + pushes + runs publish-web.sh) — then a normal
  `updaty-web` ships it to `flove.org/development/blog`. Drafts stay private.
- **Android APK** (`~/flove-apk/`): TWA app wrapping flove.org. Use skill `updaty-apk`
  to rebuild and publish to GitHub Releases. Content updates automatically (web wrapper);
  only rebuild for manifest/version changes.

The main repo is the **org site** `floveorg/floveorg.github.io` (renamed from
`floveorg/flove`; holds the `flove.org` CNAME), so project repos under `floveorg`
(e.g. `floveorg/blog` — the retired blog deploy repo) serve at `flove.org/<repo>`.

## Preconditions
- Repo: `~/Documents/flove`, branch `main`, remote `github` →
  `https://github.com/floveorg/floveorg.github.io.git`.
- A GitHub fine-grained PAT (Contents: read/write on `floveorg/floveorg.github.io`) lives in
  `~/agents/token-github-flove.md`, one token per line, format `github_pat_…` or `ghp_…`.
- Pages is already enabled with custom domain flove.org (one-time setup). The
  repo root contains `CNAME` (=`flove.org`) and `.nojekyll`.
- Project tokens (each a fine-grained PAT with Contents: read/write on its repo):
  - `~/agents/token-github-risa.md` → `floveorg/risa`
  - `~/agents/token-github-ama.md` → `floveorg/ama`
  - `~/agents/token-github-liberada.md` → `floveorg/liberada`
  - `~/agents/token-github-lowai.md` → `LowAiorg/web`

## Procedure

1. **Read the token** from `~/agents/token-github-flove.md` (grep the `github_pat_…`/`ghp_…`
   line). If it's absent or still the placeholder, STOP and tell the owner to paste a
   fine-grained PAT there — do not proceed.

2. **Confirm local `main` is the intended state, and offer to commit pending work.**
   Show `git -C ~/Documents/flove log --oneline -3` and `git status -sb`. Uncommitted/
   untracked files will NOT be published (only commits go) and — because the zip is
   built from HEAD (step 3) — would also be missing from the download. So if there
   is pending work, do NOT just remind: proactively **offer to commit it first**,
   listing exactly which files would be staged. Stage them scoped by name (never
   `-A` — the owner edits in parallel; see the scoped-git-add rule), and STOP for the owner's
   go-ahead before committing. If anything in the diff looks unfinished or like it
   should not go public (secrets, private data, half-done edits), flag it and wait.
   Only once the working tree reflects what the owner wants published do you continue.

3. **Rebuild sw.js from committed HEAD, then commit only if changed.**
   `sw.js` is machine-generated from the *committed* site (`build-sw.mjs` uses
   `git ls-files`), so regenerating and committing it is NOT authoring the owner's work
   — it's refreshing the build output for the live site's service worker.
   - `node ~/Documents/flove/build-sw.mjs` — regenerates `sw.js` (precache list).
   - If `git -C ~/Documents/flove status --porcelain sw.js` shows a change, commit it
     alone: `git -C ~/Documents/flove add sw.js && git -C ~/Documents/flove commit -m
     "Rebuild sw.js (updaty-web)"`. If unchanged, skip.
   - NEVER `git add` anything but `sw.js` here, and NEVER `-A`. If the build script
     fails, STOP and report — do not publish with a broken service worker.
   - Note: `flove.zip` is NOT rebuilt here. Use skill `upgrady` to rebuild the
     downloadable package separately.

4. **Push pending commits to Gitea (`origin`) first.** Bring Gitea up to the state
   you're about to publish:
   - `git -C ~/Documents/flove fetch origin`.
   - If `origin/main` has commits local `main` lacks, `git -C ~/Documents/flove
     merge --ff-only origin/main`; if that is NOT a fast-forward, STOP and report
     the divergence — do not force anything.
   - `git -C ~/Documents/flove push origin main` — pushes any local-only commits
     up to Gitea. A no-op if already in sync. Only after this succeeds, continue.

5. **Push to GitHub via the filtered publisher** — Gitea tracks the full dev
   workspace, so the public site is built as a *filtered subset* and
   force-pushed to `floveorg/floveorg.github.io` (serves flove.org):
   ```
   bash ~/Documents/flove/development/standards/scripts/publish-web.sh
   ```
   `publish-web.sh` unpacks the committed tree at HEAD, strips the Gitea-only
   paths (root build/launcher artifacts, editor/OS noise, python caches, apk
   build dirs, the nety gitlink) and keeps the GitHub keep-list
   (`development/skills`, `development/standards/skills`, the `decentral/` web
   part, `development/blog/public` + `resources`, `package.json`/`package-lock.json`)
   plus a single copy of `decentral/nety/index.html`. It force-pushes a fresh
   single commit to GitHub `main` (deploy-repo style, like the blog). This
    means GitHub `main` is always a filtered snapshot, never the owner's full dev
    tree — that divergence is intentional.

6. **Deploy project subdomain sites** — each project has its own GitHub Pages repo
   with a custom domain. Run each publish script:
   ```
   bash ~/Documents/flove/development/standards/scripts/publish-risa.sh
   bash ~/Documents/flove/development/standards/scripts/publish-ama.sh
   bash ~/Documents/flove/development/standards/scripts/publish-liberada.sh
   bash ~/Documents/flove/projects/lowai/publish-lowai.sh
   ```
   Each script clones the target repo, rsyncs the project content (preserving
   the repo's CNAME/.github/README), and force-pushes. They are idempotent —
   if no changes, they print "sin cambios que publicar" and exit cleanly.
   If a token is missing, the script stops with a clear error — do NOT skip it,
   the deploy is expected to succeed.

7. **Report**: the commit SHA/subject now on GitHub `main`, and that Pages will
   redeploy in ~1 min. If you want to confirm the deploy, poll
   `curl -sI https://flove.org` for a fresh `last-modified`/`etag`, but don't
   block on it — DNS/CDN caching can lag.

## Guardrails
- **Never print the PAT.** Mask it in any echoed command or URL.
- **The ONLY commit this skill may create is `sw.js`** (step 3), staged by name
  and committed alone — it is regenerated deterministically from committed HEAD,
  so this refreshes the build output, not the owner's work. Everything else is
  off-limits: never `git add` a source or app file, never `-A`, never author on
  the owner's behalf (see the scoped-git-add rule). Pushing already-made commits to
  `origin` (Gitea) and GitHub is fine — that moves existing history, not new work.
- `flove.zip` is NOT rebuilt by this skill. Use `upgrady` for that.
- The flove.org push goes through `development/standards/scripts/publish-web.sh` (filtered,
  force-push to a deploy repo — same model as the blog). Never push flove `main` to GitHub
  directly: that would leak the full dev workspace (keystores are ignored, but
  editor noise, skills workspaces and launchers are not public content).
- Project subdomain deploys (step 6) use each project's own `publish-*.sh` script.
  These rsync content to the target repo (preserving CNAME/.github/README) and
  force-push. Each is idempotent. If a token is missing, STOP and report — do not
  skip a failed deploy silently.
- This pushes public content to the open internet. If `main` contains anything
  that looks secret (tokens, private data), flag it before pushing.
- Pages serves what's on `main`. There is no separate deploy step to babysit.
