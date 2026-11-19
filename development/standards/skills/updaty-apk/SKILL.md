---
name: updaty-apk
description: >-
  Rebuild and publish flove's Android TWA app (APK/AAB) to GitHub Releases. The
  wrapper loads flove.org live, so rebuild only when manifest settings, icons,
  colours or version change. Use for "updaty-apk", "recompile apk", "subir apk".
---

# updaty-apk — rebuild & publish the flove TWA

The flove Android app is a **TWA (Trusted Web Activity)** wrapping `flove.org`,
at `~/Documents/flove/tools/flove-apk/`. It loads the live site, so content
updates by itself — rebuild only when the **manifest** changes (icons, colours,
start URL, version) or to force a Play Store update. A feature milestone that
bumps the version is such a case.

## Preconditions

- `bubblewrap` installed (`which bubblewrap`).
- `~/Documents/flove/tools/flove-apk/` holds `twa-manifest.json` and
  `android.keystore`.
- GitHub token in `~/agents/token-github-flove.md`; `gh` CLI or curl.

## Procedure

1. **Read the token** from `~/agents/token-github-flove.md`. Absent → STOP.

2. **Check the version** in
   `~/Documents/flove/tools/flove-apk/twa/twa-manifest.json`
   (`grep -E "appVersion" …`). Show it and ask whether to increment.

3. **Rebuild** if the manifest changed:
   ```bash
   cd ~/Documents/flove/tools/flove-apk/twa
   bubblewrap update     # bubblewrap build on a first run
   ```
   Build failure → STOP and report.

4. **Create the GitHub release** with the AAB:
   ```bash
   gh release create v<VERSION> ~/Documents/flove/tools/flove-apk/flove.aab \
     --repo floveorg/floveorg.github.io \
     --title "flove v<VERSION>" \
     --notes "TWA app (Android) — wraps flove.org"
   ```
   Without `gh`, POST to
   `https://api.github.com/repos/floveorg/floveorg.github.io/releases` with a
   bearer token and `{"tag_name":"v<VERSION>","name":"…","body":"…"}`, then upload
   the AAB as a release asset.

5. **Report** the release URL, the version, and that users download from GitHub
   Releases.

## Versioning

- Name `FloveAndroidYY-M` (e.g. `FloveAndroid26-7`).
- `appVersionName` matches the `YY-M` part ("26-7").
- `appVersionCode` is an integer that **must increment** for the Play Store.
- Tag format `FloveAndroid<YY-M>`.

## Files

| Path | Role |
|---|---|
| `tools/flove-apk/twa/twa-manifest.json` | TWA config (host, colours, version) |
| `tools/flove-apk/android.keystore` | signing key — **never commit** |
| `tools/flove-apk/flove.aab` | built bundle, uploaded to releases |
| `tools/flove-apk/twa/app-release-signed.apk` | signed APK, alternative distribution |

## Guardrails

- **Never commit** the keystore or the APK/`.aab` to the flove repo.
- **Never print** the GitHub token.
- Play Store distribution takes the `.aab`, not the `.apk`.

## Personal config

See `https://flove.org/development/standards/skills/CONFIG.md` for the override routes and keys.

Standing rules: `https://flove.org/development/standards/skills/standing.md`.
