---
name: updaty-apk
description: >-
  Recompile and publish the project's Android TWA app (APK/AAB) to GitHub
  Releases. Use whenever the owner (Marc by default) says "updaty-apk",
  "recompile apk", "build apk", "subir apk", "actualizar apk", "recompilar apk",
  or otherwise wants to rebuild and distribute the Android app. The APK wraps
  flove.org as a Trusted Web Activity — it only needs rebuilding when manifest
  settings change (icons, colors, start URL, version). Content updates
  automatically because it's a web wrapper, not a native app. Solo-scoped: the
  APK wraps flove.org, the published web (see development/standards/solo/README.md).
  Flove-first by default; override via the personal config (see CONFIG.md).
---

# updaty-apk — rebuild & publish flove TWA app (solo)

The flove Android app is a **TWA (Trusted Web Activity)** that wraps `flove.org`.
It lives at `~/Documents/flove/solo/flove-apk/` (inside the repo; the keystore itself is gitignored and must NEVER be committed). The app loads the live website,
so it only needs rebuilding when the **manifest** changes (icons, colors, version)
or when you want to force a Play Store update.

## Personal config

This skill ships with flove-first defaults. To fork/reuse it for another
project, create a personal config that overrides the defaults instead of
editing the skill (see `development/standards/skills/CONFIG.md`): a shared
`~/.config/flove/skills-config.yml`, a per-skill `settings.yml`, a hidden
`.settings`, or a `config.yml` in the skill folder. Only the keys you set
change; everything else falls back to these defaults.

## When to rebuild

- **Milestone adoption reached** — bump version when a feature milestone ships (e.g. new tier, new app, new standard adopted)
- Changed `twa-manifest.json` (colors, icons, start URL)
- Want to force users to update via Play Store
- Changed signing key or keystore
- **NOT needed** for website content changes (it's a web wrapper)

## Preconditions

- `bubblewrap` installed (`which bubblewrap`)
- `~/Documents/flove/solo/flove-apk/` exists with `twa-manifest.json` and `android.keystore`
- GitHub token in `~/agents/token-github-flove.md` (for releases)
- `gh` CLI installed OR use GitHub API with curl

## Procedure

1. **Read the token** from `~/agents/token-github-flove.md`. If absent, STOP.

2. **Check current version** in `~/Documents/flove/solo/flove-apk/twa/twa-manifest.json`:
   ```bash
   grep -E "appVersion" ~/Documents/flove/solo/flove-apk/twa/twa-manifest.json
   ```
   Show the owner the current version and ask if it should increment.

3. **Rebuild the TWA** (if manifest changed):
   ```bash
   cd ~/Documents/flove/solo/flove-apk/twa
   bubblewrap update  # or bubblewrap build if first time
   ```
   If build fails, STOP and report.

4. **Create GitHub release** with the AAB:
   ```bash
   # Using gh CLI:
   gh release create v<VERSION> ~/Documents/flove/solo/flove-apk/flove.aab \
     --repo floveorg/floveorg.github.io \
     --title "flove v<VERSION>" \
     --notes "TWA app (Android) — wraps flove.org"
   
   # OR using curl if gh not installed:
   curl -X POST \
     -H "Authorization: token <PAT>" \
     -H "Content-Type: application/json" \
     "https://api.github.com/repos/floveorg/floveorg.github.io/releases" \
     -d '{"tag_name":"v<VERSION>","name":"flove v<VERSION>","body":"TWA app (Android) — wraps flove.org"}'
   ```
   Then upload the AAB as a release asset.

5. **Report**: release URL, version, and that users can download from GitHub Releases.

## Versioning

- Follows flove standard: `FloveAndroidYY-M` (e.g. `FloveAndroid26-7`)
- `appVersionName`: matches the `YY-M` part (e.g. "26-7")
- `appVersionCode`: integer, must increment for Play Store (e.g. 2, 3, 4)
- Tag format: `FloveAndroid<YY-M>` (e.g. `FloveAndroid26-7`)

## Files involved

- `~/Documents/flove/solo/flove-apk/twa/twa-manifest.json` — TWA config (host, colors, version)
- `~/Documents/flove/solo/flove-apk/android.keystore` — signing key (NEVER commit)
- `~/Documents/flove/solo/flove-apk/flove.aab` — built app bundle (upload to releases)
- `~/Documents/flove/solo/flove-apk/twa/app-release-signed.apk` — signed APK (alternative distribution)

## Guardrails

- **Never commit** the keystore or APK to the flove repo.
- **Never print** the GitHub token.
- The APK content updates automatically — only rebuild for manifest/version changes.
- If Play Store is the distribution channel, upload the `.aab` (not `.apk`).
