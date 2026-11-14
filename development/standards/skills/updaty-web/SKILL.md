---
name: updaty-web
description: >-
  Quick-publish the current flove website (flove.org by default). The LIGHT
  path: commit pending source work only if the owner approves it (list the
  files first), push to Gitea, then mirror the filtered committed tree to
  GitHub Pages via publish-web.sh. Use for "updaty-web", "update the web",
  "publish the site", "push this page", "deploy flove.org", "actualiza la web",
  "sube esto a flove.org", or any request to make a page visible on the live
  site. It does NOT rebuild packages, sw.js or the vocabulary index, deploy
  subdomains (risa, ama, liberada, lowai), or run all-repo/token checks — those
  are `upgrady` (the Android app is `updaty-apk`). Flove-first by default;
  override via CONFIG.md.
---

# updaty-web — quick publish of flove.org

`updaty-web` is the **light publish path**: commit the pending source, put
`main` on the live site and stop. It does not rebuild artifacts, packages or
other sites.

> **Rule of thumb:** page/site update → `updaty-web`.
> Packages, sw.js, vocabulary, all subdomains, all-repo checks → `upgrady`.

## Scope — main site only

- `floveorg/floveorg.github.io` → `flove.org`, via
  `development/standards/scripts/publish-web.sh`.
- That is the whole job.

**Out of scope** — do not run these from this skill:
- `tools/build-flove-zip.sh` / `flove-localhost.zip` or any downloadable package.
- `node tools/build-sw.mjs` (service worker).
- Vocabulary-index sync.
- `publish-risa.sh`, `publish-ama.sh`, `publish-liberada.sh`,
  `publish-lowai.sh` and the other project subdomains.
- Token/repository preflight for those subdomains.
- The Android APK (use `updaty-apk`).

If the owner asks for any of these, it is a heavy release: use `upgrady`
(or `updaty-apk` for the APK).

## Personal config

See `development/standards/skills/CONFIG.md` for the override routes and keys.

## Preconditions

- Repo: `~/Documents/flove`, branch `main`, remote `github` →
  `https://github.com/floveorg/floveorg.github.io.git`.
- A GitHub fine-grained PAT (Contents: read/write on
  `floveorg/floveorg.github.io`) lives in `~/agents/token-github-flove.md`, one
  token per line, format `github_pat_…` or `ghp_…`.
- Pages is already enabled with custom domain flove.org (one-time setup). The
  repo root contains `CNAME` (=`flove.org`) and `.nojekyll`.
- The work to publish is either already committed on `main` or listed for the
  owner's go-ahead in step 2.

## Procedure

1. **Read the token** from `~/agents/token-github-flove.md` (grep the
   `github_pat_…`/`ghp_…` line). If it is absent or still a placeholder, STOP
   and tell the owner to paste a fine-grained PAT there — do not proceed.

2. **Check the working tree and commit pending source.** Show
   `git -C ~/Documents/flove log --oneline -3` and
   `git -C ~/Documents/flove status -sb`. Only commits go live; uncommitted
   files are not published.
   - If the tree is clean, continue immediately.
   - If there are pending edits, list exactly which files would be staged and
     **ask the owner to confirm**. On confirmation, stage only those named
     source paths — never `-A` — and commit with a concise message. Never stage
     `sw.js`, package zips, the vocabulary index or other generated artifacts;
     those are `upgrady`'s job. Do not run the heavy build/check loop here.

3. **Push pending commits to Gitea (`origin`) first.**
   - `git -C ~/Documents/flove fetch origin`.
   - If `origin/main` has commits local `main` lacks, run
     `git -C ~/Documents/flove merge --ff-only origin/main`; if that is not a
     fast-forward, STOP and report the divergence — do not force anything.
   - `git -C ~/Documents/flove push origin main`. A no-op if already in sync.
     Only after this succeeds, continue.

4. **Publish the main site.**
   ```
   bash ~/Documents/flove/development/standards/scripts/publish-web.sh
   ```
   The script unpacks the committed tree at HEAD, applies the public filter and
   force-pushes a fresh single commit to `floveorg/floveorg.github.io`.
   It runs the fast `check-distro.sh`:
   - **hard errors** abort the publish — STOP and report;
   - **warnings** (stale `sw.js`, stale routing) do **not** block a page push.
     Report them and, only if the owner wants the offline artifact refreshed,
     switch to `upgrady`.
     A stale `sw.js` affects only the **offline/PWA** side: the live online
     pages are correct, but new/renamed pages are missing from the offline
     cache, removed ones may 404 there, and the cache version does not change
     so installed clients can keep old assets. Refreshing it is part of the
     heavy `upgrady` release — do not run `build-sw.mjs` here.

5. **Report** the commit SHA/subject now on GitHub `main`, and that Pages will
   redeploy in ~1 min. Do not block on polling the live site.

## Guardrails

- **Never print the PAT.** Mask it in any echoed command or URL.
- **Commit source, never build artifacts.** updaty-web commits the pending
  source after listing it and getting the owner's go-ahead — never `-A`, never
  `sw.js`, package zips or the vocabulary index. Those are refreshed only by
  `upgrady`.
- **No subdomains, no packages, no vocabulary sync, no APK.** Those are heavy
  release operations and belong to `upgrady` / `updaty-apk`.
- Pushing already-made commits to `origin` (Gitea) and GitHub is fine — that
  moves existing history, not new work.
- The flove.org push goes through `publish-web.sh` (filtered, force-push to a
  deploy repo). Never push flove `main` to GitHub directly: it would leak the
  full dev workspace.
- This pushes public content to the open internet. If `main` contains anything
  that looks secret (tokens, private data), flag it before pushing.
- Pages serves what's on `main`. There is no separate deploy step to babysit.
