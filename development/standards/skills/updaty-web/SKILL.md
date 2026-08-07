---
name: updaty-web
description: >-
  Publish the live flove.org website by building a FILTERED subset of the latest
  committed flove changes and pushing it to the GitHub repo floveorg/floveorg.github.io,
  which is
  served by GitHub Pages at flove.org. Gitea tracks the full dev workspace; the
  public site only gets the web-relevant subset (see development/standards/scripts/publish-web.sh).
  Use whenever Marc says "updaty-web",
  "update the web", "publish the site", "push flove to the web", "deploy
  flove.org", "actualiza la web", "sube esto a flove.org", or otherwise asks to
  make the current state of flove visible on the live site. Trigger even without
  the exact words — any request to make committed flove work appear on the
  public flove.org counts. It does NOT create commits: it takes the
  already-committed local `main`, pushes any pending commits to Gitea (`origin`)
  first, then mirrors `main` to GitHub — so commit your work first and it handles
  both pushes. Before publishing it regenerates the offline service worker (`sw.js`)
  from committed HEAD and commits it if changed, so the live site always has a
  fresh precache list. Read-only toward the working tree otherwise; never stages
  or commits Marc's in-progress source edits. Does NOT rebuild `flove.zip` — use
   skill `upgrady` for that.
---

# updaty-web — publish flove.org via GitHub Pages

flove.org is hosted on **GitHub Pages** from `floveorg/floveorg.github.io` (branch `main`,
root folder). The local repo `~/Documents/flove` is Marc's source of truth, synced
to Gitea (`localhost:3000/marc/flove`, remote `origin`). This skill first pushes any
pending commits on `main` to Gitea, then mirrors `main` to GitHub; Pages rebuilds and
flove.org shows it in ~1 min.

## Scope — this skill is the MAIN SITE only

`floveorg/floveorg.github.io` → `flove.org`. These publish on their OWN, not here:
- **Blog** (`flove.org/development/blog`): the Hugo blog lives IN this repo at
  `development/blog` (source + built HTML committed in place, no `/public`
  segment). Rebuild the output with `./build-blog.sh build` (or `publish`,
  which also commits + pushes + runs publish-web.sh) — then a normal
  `updaty-web` ships it to `flove.org/development/blog`. Drafts stay private.
- **LowAI** (`lowai.org`, repo `LowAiorg/web`): separate org/domain entirely.
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

## Procedure

1. **Read the token** from `~/agents/token-github-flove.md` (grep the `github_pat_…`/`ghp_…`
   line). If it's absent or still the placeholder, STOP and tell Marc to paste a
   fine-grained PAT there — do not proceed.

2. **Confirm local `main` is the intended state, and offer to commit pending work.**
   Show `git -C ~/Documents/flove log --oneline -3` and `git status -sb`. Uncommitted/
   untracked files will NOT be published (only commits go) and — because the zip is
   built from HEAD (step 3) — would also be missing from the download. So if there
   is pending work, do NOT just remind: proactively **offer to commit it first**,
   listing exactly which files would be staged. Stage them scoped by name (never
   `-A` — Marc edits in parallel; see the scoped-git-add rule), and STOP for his
   go-ahead before committing. If anything in the diff looks unfinished or like it
   should not go public (secrets, private data, half-done edits), flag it and wait.
   Only once the working tree reflects what Marc wants published do you continue.

3. **Rebuild sw.js from committed HEAD, then commit only if changed.**
   `sw.js` is machine-generated from the *committed* site (`build-sw.mjs` uses
   `git ls-files`), so regenerating and committing it is NOT authoring Marc's work
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
   means GitHub `main` is always a filtered snapshot, never Marc's full dev
   tree — that divergence is intentional.

6. **Report**: the commit SHA/subject now on GitHub `main`, and that Pages will
   redeploy in ~1 min. If you want to confirm the deploy, poll
   `curl -sI https://flove.org` for a fresh `last-modified`/`etag`, but don't
   block on it — DNS/CDN caching can lag.

## Guardrails
- **Never print the PAT.** Mask it in any echoed command or URL.
- **The ONLY commit this skill may create is `sw.js`** (step 3), staged by name
  and committed alone — it is regenerated deterministically from committed HEAD,
  so this refreshes the build output, not Marc's work. Everything else is
  off-limits: never `git add` a source or app file, never `-A`, never author on
  Marc's behalf (see the scoped-git-add rule). Pushing already-made commits to
  `origin` (Gitea) and GitHub is fine — that moves existing history, not new work.
- `flove.zip` is NOT rebuilt by this skill. Use `upgrady` for that.
- The GitHub push goes through `development/standards/scripts/publish-web.sh` (filtered, force-push to a
  deploy repo — same model as the blog). Never push flove `main` to GitHub
  directly: that would leak the full dev workspace (keystores are ignored, but
  editor noise, skills workspaces and launchers are not public content).
- This pushes public content to the open internet. If `main` contains anything
  that looks secret (tokens, private data), flag it before pushing.
- Pages serves what's on `main`. There is no separate deploy step to babysit.
