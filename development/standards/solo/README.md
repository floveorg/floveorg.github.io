# Solo — status & index

The **Solo** area (`solo/`) is the original, **local-first** flove distro
(no backend, works from `file://`). It stays a live, maintained distro;
the **Central** apps (`central/apps/`) are the **canonical spec** for the
standards in this book, and Solo is its reference/fallback counterpart
(see [`adoption.md`](../adoption.md) SoloRich→Central
migration and [`debates/plans/conflicts.md`](../debates/plans/conflicts.md) D20:
"Central URLs become primary; Solo URLs on main maintained as fallback").

This page is the index of everything Solo-scoped. It hosts the Solo **distro
pipeline** spec (below) and points to the Solo-scoped skills — which keep living
in [`../skills/`](../skills/), referenced here rather than moved.

## Solo distro pipeline

Extracted from the backend plan — the Solo-specific distribution machinery
(flove.zip, the apk TWA, the service worker):

1. **Build** — `solo/build-flove-zip.sh` bundles the `solo/` apps into
   `flove-solo.zip`. **Only run via the `upgrady` skill, on an explicit request
   ("rebuild zip", "actualizar zip", "upgrade")** — never rebuilt automatically
   after a source commit. Commit source first, and only regenerate the zip when
   the downloadable package actually needs refreshing.
2. **Service worker** — `solo/sw.js` is **generated** by `node solo/build-sw.mjs`
   (never hand-edited); it precaches the published app list for offline use.
3. **Download** — the zip ships from flove.org as `flove.zip`, also attached to
   GitHub Releases.
4. **Android TWA** — `solo/flove-apk/` builds the APK/AAB that wraps flove.org
   as a Trusted Web Activity (rebuilt only when manifest settings change; content
   updates automatically because it's a web wrapper). Signing key stays in
   `~/flove-apk/` — never committed. See the `updaty-apk` skill.
5. **Routing.json** — meta-tag scan of `apps/*/[name].html` (id, name, url,
   tier, description, tags) → `routing.json` at zip root; README.md lists the
   apps. Tier values: `nano · mini · basic · normal · advanced · super · mega`.

The general JSON distro architecture (routing schema, app discovery, hosting,
auth, DB) is specced in [`../backend.md`](../backend.md) §10.3e.

## Running flove — the four options

The download house on the home page offers four ways to run flove. They are, in
order:

1. **Desktop / `.zip`** — download `flove-solo.zip`, unzip and run
   `START-FLOVE-<os>` (serves `flove-solo/` on `localhost:8642`).
2. **Android / Termux** — run it directly on the phone in Termux (offline, no
   network), via the install-and-serve command shown on the home page.
3. **Over the network (Red)** — reach the running instance from another device
   (same Wi-Fi, or Tailscale anywhere via HTTPS).
4. **`.aab` Android app** — the ready **Android app** (no Termux): the TWA
   built by `solo/flove-apk/` (see `updaty-apk`), published to **GitHub
   Releases** as `flove.aab` — the 4th, lowest-effort option.

## Solo-scoped skills

These skills live in [`../skills/`](../skills/) (one real copy, symlinked from
`~/.agents/skills/`) and are **Solo-scoped** — they build, audit, or ship the
Solo distro:

| Skill | Path | Scope |
|-------|------|-------|
| **upgrady** | [`../skills/upgrady-solo/SKILL.md`](../skills/upgrady-solo/SKILL.md) | rebuild & commit `flove-solo.zip` (and sw.js) from committed HEAD |
| **exporty** | [`../skills/exporty-solo/SKILL.md`](../skills/exporty-solo/SKILL.md) | audit an app's export & share surface against §13.12 |
| **updaty-apk** | [`../skills/updaty-apk-solo/SKILL.md`](../skills/updaty-apk-solo/SKILL.md) | recompile & publish the flove Android TWA to GitHub Releases |

`updaty-web` (publish flove.org) is **not** Solo-scoped — it ships the whole
web, including this standards book.
