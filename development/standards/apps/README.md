# LocalHost distro — status & index

The local-first flove distro lives in **`apps/`** (every app) and **`tools/`**
(the machinery: language gate, manifest, service worker, build/check scripts,
APK, download package). It has no backend and works from `file://` or a plain
`python3 -m http.server`.

**Solo** is no longer a folder — it is the *property* of the app design:
each app is one self-contained HTML file, with its CSS/JS inline and no shared
code. The run mode is called **LocalHost**.

The **Central** apps (`central/apps/`) remain the **canonical spec** for the
standards in this book; the local-first distro is its reference/fallback
counterpart (see [`adoption.md`](../adoption.md) and
[`debates/plans/conflicts.md`](../debates/plans/conflicts.md) D20).

This page is the index of the distro pipeline and points to the Solo-scoped
skills, which live in [`../skills/`](../skills/).

## Pipeline

1. **Build** — `tools/build-flove-zip.sh` builds `flove-localhost.zip` as a
   **path-preserving subset of the repo root**: `index.html`, `apps/`,
   `central/shared/media/images/`, `tools/`, `docs/` and `sw.js`, all at the
   same paths as the live
   site. It never rewrites an `href`. **Only run via the `upgrady` skill, on an
   explicit request ("rebuild zip", "actualizar zip", "upgrade")** — never
   rebuilt automatically after a source commit. Commit source first.
2. **Service worker** — `sw.js` at the repo/package **root** is **generated** by
   `node tools/build-sw.mjs` (never hand-edited). **Only run it in the heavy
   `upgrady` release**, like the zip; normal page work and `updaty-web` never
   rebuild it. Its scope is `/`, so it can precache the home, every app,
   `central/shared/media/images/` and `docs/`.
3. **Download** — the zip ships from flove.org as
   `tools/flove-localhost.zip`, also attached to GitHub Releases.
4. **Android TWA** — `tools/flove-apk/` builds the APK/AAB that wraps
   flove.org as a Trusted Web Activity (rebuilt only when manifest settings
   change; content updates automatically because it's a web wrapper). The
   signing key stays in `tools/flove-apk/android.keystore` — never committed.
   See the `updaty-apk` skill.
5. **Routing.json** — meta-tag scan of `apps/*/[name].html` (id, name, url,
   tier, description, tags) → `tools/routing.json`. Tier values:
   `nano · mini · basic · normal · advanced · super · mega`.

### Self-contained assets (artwork in one canonical folder; code never)

`apps/` is published at `flove.org/apps/`, shipped in `flove-localhost.zip`,
installed as a PWA, and opened from `file://` or a plain `python3 -m http.server`.
It therefore **cannot depend on `central/` code at runtime**. Every app page
inlines its own CSS and JS and calls no external library. The only shared runtime
dependency is artwork, and it lives once in `central/shared/media/images/`:

| Canonical source | Used by |
|---|---|
| `central/shared/media/images/` | captions, logo animations, icons, `apps-full.html`, the root home |

The root home (`index.html`) and every app point at `central/shared/media/images/…`
too, so the same path resolves on flove.org
(`/central/shared/media/images/…`) and inside the download — no build-time
rewriting. Audio is web-only (`central/shared/media/audio/`, ~22 MB) and stays
out of the download; the `Audio()` calls fail silently there.

Edit the files directly in `central/shared/media/images/` and commit them: the
publish tree and the download both carry that folder at the same path (no
mirror, no symlinks — GitHub Pages does not resolve symlinks and `git archive`
stores the link, not the target). There is deliberately **no `apps/shared/css`
or `apps/shared/js`**: an app that needs a stylesheet or script must inline it.
`central/apps/` is not a runtime dependency either: Central stays a mock /
advanced-apps area.

### Entry model (one home, one optional gate)

| Entrance | What it shows | Forces a language? |
|---|---|---|
| `/index.html` (live root and package root) | the **full flove entrance** | **no** — it has the 🌐 switcher, but never blocks |
| `/apps/` | the **app launcher** (graph / entrance / grid) | no |
| `/tools/start.html` | the **language-selection page** | yes, on first run |
| `/tools/start.html?tour=1` | the **intro tour** (the home's “Why” button) | no — always shows the slides |

`start.html` is the single page behind both the language gate and the tour; the
`?tour=1` flag only suppresses the “language already saved → go home” shortcut.

The download package keeps the same depth: `flove-localhost/index.html`,
`flove-localhost/apps/…`, `flove-localhost/tools/…`, `flove-localhost/docs/…`.
The launchers serve that root and open `/index.html` — the same entry as
flove.org — so one relative link is valid everywhere:

```
flove-localhost/index.html   ← the same full entrance as flove.org/
        ▼
flove-localhost/apps/…       ← the same app folders as /apps/
flove-localhost/tools/start.html  ← optional language gate / tour
flove-localhost/docs/…       ← the same reading library
```

The choice is stored in `localStorage` under `flove:lang` and `translaty-lang`;
every app reads it, so it persists across all played apps.

Launchers write `tools/devices.json` with the LAN/Tailscale addresses so a phone
can open the same instance (Settings ▸ Devices).

### Milestones

**2026-11-09 · `apps/` + `tools/`** — the old `solo/` folder mixed the apps with
all the machinery and carried a nested `solo/solo/apps` forwarder. Now `apps/`
holds every app, `tools/` holds the machinery, the shared artwork lives in
`central/shared/media/images/`,
and `sw.js` + `.well-known/assetlinks.json` + `404.html` sit at the root because
the browser/Android require it. The package was renamed `flove-localhost.zip`.
No folder is called `solo` anymore.

**2026-11-08 · one root, no link rewriting** — before this, the same site had
three roots: flove.org served the repo root, the zip flattened the distro and
`sed`-rewrote the home's links, and `serve-dev.sh` served a third layout. Now
there is one canonical root in every run mode; a link is written once, relative,
and never rewritten at build time. The only absolute internal links are the
zip-download button and a handful of links to sections that deliberately do not
ship (central/decentral/development).

### Enforcement

`tools/check-distro.sh` is the single distro gate. It checks the entry pages,
a single canonical `central/shared/media/images/` folder (and no duplicate
`images/` mirror), that no `apps/shared` code tree exists, that no
internal link is root-absolute, that every local `href`/`src` resolves (with the
known unbuilt-app gaps allowlisted), the app routing count, and whether `sw.js`
matches the tracked tree. Run it before committing or publishing:

```sh
tools/check-distro.sh          # report + non-zero exit on new breakage
tools/check-distro.sh --build  # also rebuild the zip to prove packaging works
```

The general JSON distro architecture (routing schema, app discovery, hosting,
auth, DB) is specced in [`../backend.md`](../backend.md) §10.3e.

## Running flove — the four options

1. **Desktop / `.zip`** — download `flove-localhost.zip`, unzip and run
   `START-FLOVE-<os>` (serves `flove-localhost/` on `localhost:8642`, opening
   `/index.html`).
2. **Android / Termux** — run it directly on the phone in Termux (offline, no
   network), via the install-and-serve command shown on the home page.
3. **Over the network (Red)** — reach the running instance from another device
   (same Wi-Fi, or Tailscale anywhere via HTTPS).
4. **`.aab` Android app** — the ready **Android app** (no Termux): the TWA built
   by `tools/flove-apk/` (see `updaty-apk`), published to **GitHub Releases** as
   `flove.aab`.

## Solo-scoped skills

These skills live in [`../skills/`](../skills/) (one real copy, symlinked from
`~/.agents/skills/`) and are **Solo-scoped** — they build, audit, or ship the
local-first distro:

| Skill | Path | Scope |
|-------|------|-------|
| **upgrady** | [`../skills/upgrady-solo/SKILL.md`](../skills/upgrady-solo/SKILL.md) | heavy release: packages (`flove-localhost.zip`), `sw.js`, vocabulary, all-repo checks; optionally publishes main + subdomains |
| **exporty** | [`../skills/exporty-solo/SKILL.md`](../skills/exporty-solo/SKILL.md) | audit an app's export & share surface against §13.12 |
| **updaty-apk** | [`../skills/updaty-apk/SKILL.md`](../skills/updaty-apk/SKILL.md) | recompile & publish the flove Android TWA to GitHub Releases |

`updaty-web` (quick publish of flove.org) is **not** Solo-scoped — it ships the
whole web, including this standards book. The heavy package/artifact/all-targets
release path is `upgrady`.
