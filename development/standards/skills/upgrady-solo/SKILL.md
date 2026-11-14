---
name: upgrady
description: >-
  Heavy release for flove: refresh the downloadable packages (the localhost
  .zip and any other configured package), rebuild generated artifacts such as
  sw.js (the only path that refreshes it), sync the vocabulary index, run the
  distro and all repository/token checks, and — when explicitly asked — publish the main site and the project
  subdomains. Use for "upgrade", "rebuild zip", "actualizar zip", "reconstruir
  el paquete", "repackage", "full release", "check all repos", or whenever
  packages or artifacts are being refreshed. For a plain page push use the
  light skill `updaty-web`; the Android APK stays in `updaty-apk`.
  This skill is separate from updaty-web because packages and all-repo checks
  are heavy and do not need to run on every publish. See
  development/standards/skills/CONFIG.md for the personal-config override.
---

# upgrady — heavy release: packages, artifacts & all targets

`upgrady` is the **heavy path**. It is for changes where the downloadable
packages or build artifacts must be refreshed, or where every repository and
condition must be checked — not for a simple page push.

> **Rule of thumb:** page/site update → `updaty-web`.
> Packages, sw.js, vocabulary, all subdomains, all-repo checks → `upgrady`.

| The request sounds like | Use |
| --- | --- |
| "push this page", "update the web", "publish flove.org" | `updaty-web` (light) |
| "upgrade", "rebuild zip", "actualizar zip", "repackage" | **this skill** |
| "full release", "upgrade and publish", "check all repos" | **this skill** |
| "recompile/publish the APK" | `updaty-apk` |

## Scope

**Packages & artifacts**
- `tools/build-flove-zip.sh` → `tools/flove-localhost.zip` (the downloadable
  local distro).
- `node tools/build-sw.mjs` → `sw.js` (generated service worker).
- The vocabulary index (`development/standards/vocabulary/index.html`), when
  the personal config enables the vocab sync.
- Any other package/artifact build script configured for the project.

**Checks**
- `tools/check-distro.sh` (entry, self-containment, one shared-images folder,
  dead local references).
- Token and repository preconditions for every target being published.

**Publishing — only when asked** ("upgrade and publish", "full release"):
- The main site (`flove.org`) via `publish-web.sh`.
- Project subdomains: risa, ama, liberada.net, lowai.org.
- The Android APK is delegated to `updaty-apk`, not rebuilt here.

## Aliases used in this file

- `{PROJECT}` — project name, default `flove`.
- `{REPO}` — repository path, default `~/Documents/flove`.
- `{PACKAGE}` — downloadable package name, default `flove-localhost`.
- `{OWNER}` — the maintainer, default `Marc`.

## What the package is

`{REPO}/tools/{PACKAGE}.zip` is the downloadable package users get when clicking
"Download / Go local" on the flove home. It is built from committed HEAD via
`tools/build-flove-zip.sh` and is a **path-preserving subset of the repo root**,
nested under `{PACKAGE}/` in the zip:

- `index.html` — the flove home, verbatim (the same file flove.org serves).
- `apps/` — every app, kept at `apps/` (NOT flattened).
- `central/shared/media/images/` — shared artwork (single canonical folder).
- `tools/` — `start.html`, `manifest.webmanifest`, `apple-touch-icon.png`,
  `routing.json` and the generated `devices.json` (runtime only).
- `docs/` — the reading library; `docs/docs-files/` never ships.
- `sw.js` — the service worker at the package root, so its scope is `/`.

Because the paths match the live site, every relative link works in both — the
build never rewrites an `href`. Audio is web-only and does not ship. The Android
build dir `tools/flove-apk/` never ships (apk-only).

The launchers (`START-FLOVE-LINUX.sh` / `-MAC.command` / `-WINDOWS.bat` /
`-ANDROID.sh`) are generated at the zip root and serve `{PACKAGE}/` on
`localhost:8642`, opening `/index.html` — the same entry as flove.org. The Linux
launcher also writes `tools/devices.json` with LAN/Tailscale addresses for the
phone view.

## Preconditions

- Repo at `{REPO}`, on the default branch, with the source work committed (the
  artifacts are built from committed HEAD).
- `tools/build-flove-zip.sh` exists.
- For a package-only run: no publishing tokens needed.
- For a full release: the main-site PAT (`~/agents/token-github-flove.md`) and
  the token for each subdomain being deployed:
  - `~/agents/token-github-risa.md` → `floveorg/risa`
  - `~/agents/token-github-ama.md` → `floveorg/ama`
  - `~/agents/token-github-liberada.md` → `floveorg/liberada`
  - `~/agents/token-github-lowai.md` → `LowAiorg/web`
  If a required token is missing, STOP and report — do not skip that target.

## Procedure

0. **Pick the release scope.**
   - "upgrade", "rebuild zip", "actualizar zip", "repackage" → packages and
     artifacts only; **no push**.
   - "check all repos", "check conditions" → checks only; no rebuild, no push.
   - "upgrade and publish", "full release" → packages/artifacts, checks **and**
     publish.
   - If the owner names a single subdomain, publish only that one.
   - If the owner asks for the APK, hand that part to `updaty-apk`.

1. **Preflight.** Show `git -C {REPO} status -sb` and
   `git -C {REPO} log --oneline -3`. The source must be committed before the
   artifacts are built. If there are pending edits, list them and STOP — ask the
   owner to commit the source first; this skill does not author source commits.
   For a full release, verify the target tokens now. For a checks-only request,
   verify the same tokens/repos and report their state without deploying.

2. **Sync the vocabulary index (if configured).** *Rebuild/full-release scope
   only; for a checks-only request skip to step 5.* If `vocab-sync` is on
   (default on for flove):
   - Refresh the `vocab` object in
     `development/standards/vocabulary/index.html` from the latest slot texts
     (titles, taglines, entry labels, about bodies).
   - Commit it:
     `git -C {REPO} add development/standards/vocabulary/index.html` and commit
     with a message like `Sync vocabulary index (upgrady)`.
   - If the config disables it, skip.

3. **Rebuild the service worker.** Run `node tools/build-sw.mjs`. This is the
   **only** place `sw.js` is refreshed — never in normal development and never
   in `updaty-web`. If `sw.js` changed, commit it (`git add sw.js`, message
   `Rebuild sw.js (upgrady)`); if unchanged, skip.

4. **Rebuild the packages.** Run `bash tools/build-flove-zip.sh`; it reports the
   size of `tools/{PACKAGE}.zip`. If other package build scripts are configured,
   run them too. If a build fails, STOP and report — never ship a broken
   package. Commit only the changed artifacts.

5. **Run the heavy checks.** Run `bash tools/check-distro.sh`. This is the main
   deliverable for a checks-only request, and a required gate for a rebuild or
   full release.
   - Hard errors (entry, self-containment, shared-images, dead references)
     abort the release — STOP and report.
   - Warnings (stale routing, stale `sw.js`) are reported; fix them or explain
     before publishing.
   This is the "all conditions" gate, so do not skip it for a full release.

6. **Publish — only when asked.**
   - Main site:
     `bash {REPO}/development/standards/scripts/publish-web.sh`
   - Subdomains (all, or only the ones requested):
     ```
     bash {REPO}/development/standards/scripts/publish-risa.sh
     bash {REPO}/development/standards/scripts/publish-ama.sh
     bash {REPO}/development/standards/scripts/publish-liberada.sh
     bash {REPO}/projects/lowai/publish-lowai.sh
     ```
     Each script clones its target, rsyncs the content (preserving
     CNAME/.github/README) and force-pushes. They are idempotent — unchanged
     targets print "sin cambios que publicar". A missing token is a hard stop.
   - APK: if requested, use `updaty-apk`; do not rebuild it here.

7. **Report.** List what was rebuilt (zip size, sw.js, vocabulary), the artifact
   commit SHA/subject, and — if published — the main site and each subdomain
   deployed. Mention that Pages takes ~1 min.

## Guardrails

- **Only build artifacts may be committed:** `sw.js`, the vocabulary index and
  `tools/{PACKAGE}.zip` (plus other configured package artifacts). Never source
  files, never `-A`.
- **Never push unless explicitly asked.** "Upgrade" alone means rebuild and
  commit, not publish.
- **Never print a PAT.** Mask it in echoed commands and URLs.
- **A hard distro-check failure aborts publishing.** Do not bypass it for a
  full release.
- The package must contain exactly `index.html`, `apps/`,
  `central/shared/media/images/`, `tools/`, `docs/` and `sw.js` under
  `{PACKAGE}/`. If it contains anything else or a flattened tree, STOP and
  report.
- The main site always goes through `publish-web.sh`; never push the full dev
  tree to GitHub.
- Project subdomain scripts are independent deploys; never skip a requested one
  silently.
- This skill is heavy by design. If the task is only "push one page", use
  `updaty-web` instead.
