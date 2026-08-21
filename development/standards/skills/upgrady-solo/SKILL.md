---
name: upgrady
description: >-
  Rebuild and commit the downloadable solo package (.zip) from committed HEAD.
  Use whenever the owner says "upgrade", "rebuild zip", "actualizar zip", "rebuild
  package", "reconstruir el paquete", or otherwise wants to refresh the
  downloadable package. This skill is separate from updaty-web because the zip is
  a heavy artifact that doesn't need rebuilding on every publish. It also syncs
  the vocabulary index (slot texts) into development/standards/flove-vocaby.html,
  runs build-flove-zip.sh, commits the result if changed, and optionally pushes.
  See development/standards/skills/CONFIG.md for the personal-config override.
---

# upgrady — rebuild the downloadable package (solo)

> **This skill only rebuilds the downloadable `.zip`, and only when asked.**
> ("upgrade", "rebuild zip", "actualizar zip", "reconstruir el paquete").
> Regular source commits **never** trigger a rebuild — the package is a heavy,
> shipped artifact that isn't refreshed automatically after each edit of the
> files it carries. It stays pointing at committed HEAD until an explicit
> `upgrady` request, so: commit source first, then run this when the package
> needs refreshing.

This skill uses the **personal-config override** described in
`development/standards/skills/CONFIG.md`. All project-specific values below are
flove-first **defaults**; to fork this skill for another project, add
`~/.config/flove/skills-config.yml` (or a per-skill `settings.yml`) instead of
editing the skill. See the aliases `{PROJECT}`, `{repo}`, `{package}` below.

## Aliases used in this file

- `{PROJECT}` — project name, default `flove`.
- `{REPO}` — repository path, default `~/Documents/flove`.
- `{PACKAGE}` — downloadable package name, default `flove-solo`.
- `{OWNER}` — the maintainer, default `Marc`.

## What the package is

`{REPO}/solo/{PACKAGE}.zip` is the downloadable package users get when clicking
"Download / Go local" on the solo home. It's built from committed HEAD via
`solo/build-flove-zip.sh` and ships **exactly these folders** from the ranked
tree, renamed per `{PACKAGE}`:

- `solo/` — the app, **flattened**: its content sits directly in the `{PACKAGE}/`
  folder of the zip (START.html, index.html, apps/, audio/, images/, sw.js, … at
  the package root), not nested under `solo/`. The shared images now live inside
  the app (`solo/images/`, `images/…` in the package), so nothing is pulled from
  the repo-root `central/`. The download is **text-most**: `audio/` and `images/`
  may be stripped depending on your config; the Android build dir
  `solo/flove-apk/` never ships (apk-only). Per-app tiny favicon SVGs that the
  tab icons need are kept.
- `docs/` — a minimal reading library, kept as `docs/`: just `index.html` +
  `paradigms.html` (the two pages the site links to). The embedded packs/backups
  folder `docs/docs-files/` never ships (gitignored and removed).

The launchers (START-LINUX.sh / -MAC.command / -WINDOWS.bat) are generated at
the zip root and open `{PACKAGE}/START.html` (the language selector, renamed
from `launch.html` in the download). An Android launcher serves the same package
on the phone's own `localhost` (secure context, so offline/SW works with no
shared Wi-Fi and no Tailscale).

## Scope

This skill ONLY rebuilds the package. It does NOT:
- Push to a remote (that's a publish skill)
- Rebuild the service worker on its own (a publish skill does this before
  pushing)
- Touch the Android app (it's a TWA wrapping the live site)
- Commit source files or author your work

## Preconditions

- Repo at `{REPO}`, on the default branch.
- `solo/package-build.sh` (or your configured build script) exists (`solo/`,
  not the repo root).
- The service worker must be up to date — rebuild it first if unsure.
- Commit site changes BEFORE running — the package is built from the committed
  HEAD (`git archive HEAD`).

## Procedure

0. **Sync the vocabulary index (if your config enables it).** The package can
   carry the slot-vocabulary reference page (`development/standards/flove-vocaby.html`),
   which is maintained from the apps' slot texts. If your `vocab-sync` config is
   on (default on for the flove project), before rebuilding:
   - Refreshing the `vocab` object in
     `development/standards/flove-vocaby.html` so it mirrors the latest
     slot texts from the apps (titles, taglines, entry labels, about bodies).
   - Commit the refreshed page:
     `git -C {REPO} add development/standards/flove-vocaby.html` and commit
     with a message like `Sync vocabulary index (upgrady)`.
   - If the vocab sync is not configured, skip this step.

1. **Check the service worker is current.** Rebuild it and check whether the
   tracked file changed. If yes, commit it; if unchanged, skip. This ensures the
   package ships a fresh precache list.

2. **Rebuild the package.** Run your configured build script. It outputs the
   size of the zip. If the script fails, STOP and report.

3. **Commit if changed.** Check whether the zip changed. If it did, commit it.
   If unchanged, report that the package is already current and skip.

4. **Report.** Tell `{OWNER}` the commit SHA/subject, the zip size, and whether
   it was actually rebuilt or was already up to date.

## Optional: push after rebuild

If you are asked to "upgrade and publish", after committing the zip run the
release skill to push everything (local + host + Pages). Do NOT push
automatically unless asked.

## Guardrails

- **Only the war worker and the `.zip` may be committed** — never `-A`, never
  source files.
- The package is exactly the app folder (flattened as `{PACKAGE}/`) + a minimal
  `docs/`. If the zip ever contains anything else, or your source tree files,
  STOP and report — don't ship it.
- The older `solo/flove.zip` is no longer rebuilt; leave it alone.
- Never push unless explicitly asked.
- This skill is safe to run anytime: it only touches build artifacts and (when
  configured) the vocab index.