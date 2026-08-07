---
name: upgrady
description: >-
  Rebuild and commit the downloadable flove-solo.zip package from committed HEAD.
  Use whenever Marc says "upgrade", "rebuild zip", "actualizar zip", "rebuild
  flove.zip", "rebuild flove-solo.zip", "reconstruir el paquete", or otherwise
  wants to refresh the downloadable package. This skill is separate from
  updaty-web because the zip is a heavy artifact that doesn't need rebuilding on
  every publish. It runs build-flove-zip.sh, commits the result if changed, and
  optionally pushes to Gitea/GitHub. Solo-scoped (see development/standards/solo/README.md).
---

# upgrady — rebuild flove-solo.zip (solo)

> **Only the `upgrady` skill rebuilds `flove-solo.zip`, and only when asked**
> ("upgrade", "rebuild zip", "actualizar zip", "reconstruir el paquete").
> Regular source commits **never** trigger a rebuild — the zip is a heavy,
> shipped artifact that isn't refreshed automatically after each edit of the
> files it carries (e.g. `index.html`). It stays pointing at committed HEAD
> until an explicit `upgrady` request. So: commit source first, then run this
> when the downloadable package needs refreshing. See
> `development/standards/solo/README.md`.

`solo/flove-solo.zip` is the downloadable package that users get when clicking
"Download / Go local" on the solo home. It's built from committed HEAD via
`solo/build-flove-zip.sh` and ships **exactly two things** from the tracked
tree:

- `solo/` — the app. Renamed per flove-solo and **flattened**: its content sits
  directly in the `flove-solo/` folder of the zip (START.html, index.html, apps/,
  audio/, images/, sw.js, … at the package root), not nested under `solo/`. The
  shared images now live inside the app (`solo/images/`, `images/…` in the
  package), so nothing is pulled from repo-root `central/`. The download is
  **text-only**: `audio/` and `images/` are stripped (no sounds, no captions, no
  big icons), and the Android build dir `solo/flove-apk/` never ships (apk-only).
  Per-app tiny favicon SVGs that the tab icons need are kept.
- `docs/` — a minimal reading library, kept as `docs/`: just `index.html` +
  `paradigms.html` (the only two pages the site links to). The embedded
  packs/backups folder `docs/docs-files/` never ships (gitignored and removed).

The three launchers (START-FLOVE-LINUX.sh / -MAC.command / -WINDOWS.bat) are
generated at the zip root beside those folders and open `flove-solo/START.html`
(language selector, renamed from `launch.html` in the download). Add a fourth,
`START-ANDROID.sh` (Termux): it serves the same package on the phone's **own**
`localhost:8642` — phone `localhost` is a secure context, so offline/SW works
with no shared Wi-Fi and no Tailscale (needs `pkg install python` in Termux).

### Phones / mobile reachability
A phone can't open the desktop's `localhost`, so the launchers (Linux/macOS)
now write `devices.json` into the served folder — `{localhost, lan[], tailscale}`
— and print the reachable addresses. The app's Settings ▸ Devices section
(`solo/apps/appy/appy-basic.html`, with the vendored MIT `appy-qr.js` encoder)
reads that file and renders the QR/URLs a phone can scan:
- **same Wi-Fi**: `http://<PC-LAN-IP>:8642` (python http.server already binds 0.0.0.0; unblock TCP 8642 in the firewall if needed).
- **Tailscale, any network + HTTPS/offline**: the script reads `tailscale ip -4`.
  For a signed-HTTPs context on the phone, run `tailscale serve --bg http://127.0.0.1:8642`
  (a manual/account step — never automated here).
- On the live site there's no `devices.json`, so the Devices section falls back
  to the current origin.
Note: plain `http://<LAN-IP>` is not a secure context — the phone can browse and
use `localStorage`, but without HTTPS (Tailscale `serve`) it gets no service
worker / PWA offline. That's the tracked browsy·wisy offline item.

The canonical description of the repo layout and publish pipeline is
`docs/README.md` (served at flove.org/docs/) — when in doubt, read that and
follow it.

## Scope

This skill ONLY rebuilds `flove-solo.zip`. It does NOT:
- Push to Gitea or GitHub (that's updaty-web)
- Rebuild `sw.js` (that's also updaty-web, done before push)
- Touch the Android app (that's updaty-apk — the APK is a TWA wrapping the live
  site, so it never needs a rebuild for content changes)
- Rebuild `lowai` (published separately via its own publish-lowai.sh)
- Commit source files or author Marc's work

## Preconditions
- Repo: `~/Documents/flove`, branch `main`
- `solo/build-flove-zip.sh` exists (under `solo/`, not the repo root)
- `solo/sw.js` must be up to date (run `node ~/Documents/flove/solo/build-sw.mjs`
  first if unsure — but updaty-web already handles this before publishing)
- Commit site changes BEFORE running — the zip is built from `git archive HEAD`

## Procedure

1. **Check sw.js is current.** Run `node ~/Documents/flove/solo/build-sw.mjs` and
   check if `git -C ~/Documents/flove status --porcelain solo/sw.js` shows a
   change. If yes, commit it:
   `git -C ~/Documents/flove add solo/sw.js && git -C ~/Documents/flove commit -m "Rebuild sw.js (upgrady)"`.
   If unchanged, skip. This ensures the zip ships a fresh service worker.

2. **Rebuild the package.** Run `bash ~/Documents/flove/solo/build-flove-zip.sh`.
   It outputs the size of `solo/flove-solo.zip`. If the script fails, STOP and
   report.

3. **Commit if changed.** Check `git -C ~/Documents/flove status --porcelain
   solo/flove-solo.zip`. If there's a change:
   - `git -C ~/Documents/flove add solo/flove-solo.zip`
   - `git -C ~/Documents/flove commit -m "Rebuild flove-solo.zip (upgrady)"`
   If unchanged, report that the package is already current and skip.

4. **Report.** Tell Marc the commit SHA/subject, the zip size, and whether it
   was actually rebuilt or was already up to date.

## Optional: push after rebuild

If Marc says "upgrade and publish" or "upgrade + updaty-web", after committing
the zip, run the updaty-web skill to push everything (Gitea + GitHub + Pages).
Do NOT push automatically unless asked.

## Guardrails
- **Only `solo/sw.js` and `solo/flove-solo.zip` may be committed** — never `-A`,
  never source files.
- The package is exactly `solo/` (as `flove-solo/`, flattened) + a minimal
  `docs/` (only `index.html` and `paradigms.html`). If the zip ever contains
  anything else (other `docs/` files, anything from `central/`, decentral/,
  development/, addons/, root files), STOP and report — don't ship it.
- The older `solo/flove.zip` is no longer rebuilt; leave it alone.
- Never push unless Marc explicitly asks.
- This skill is safe to run anytime: it only touches build artifacts.
