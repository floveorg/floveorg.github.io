---
name: updaty
description: >-
  Publish or heavy-release the flove website: gate, commit source, rebuild
  packages and sw.js, publish main and subdomains. Use for "updaty", "update the
  web", "publish the site", "upgrade", "rebuild zip", "full release", or updaty
  levels 1–5.
category: utility
---

# updaty — publish and release flove

One skill for the site and its artifacts. **Default from now on:** auto-pick the
level from the state and the request; no number needed.

## Depth

`/updatyN` runs levels 1 → N and stops.

1. **Gate** — read-only standards check; no writes.
2. **Commit** — source only; no push.
3. **Publish main** — push + publish only the changed paths; no heavy.
4. **Heavy + publish main** — sync + `sw.js` + zip + local/Gitea GC, then one
   incremental publish.
5. **Full release** — level 4 + subdomains; APK delegated.

Auto-pick: dirty or moving tree → 1; clean + "commit" → 2; + "publish" or no
qualifier → 3; + "upgrade" → 4; + "full release" → 5. Report the level used and
the next one; after a stop, "sigue" means the next level. Do 1–2 directly when
safe; stop if the tree is moving or the source set is unclear. Next-level
proposal: bullet **Pros**, **Cons**, **Redundancy**, **Effort vs result**; show
cons even when they outnumber pros.

## Actions by level

### 1. Gate (read-only)
- Read the PAT from `~/agents/token-github-flove.md`; absent or placeholder →
  STOP. Never print it.
- Show `git log --oneline -3` and `git status -sb`.
- Run `bash tools/dev/check-distro.sh`; hard errors → STOP.
- If `apps/` or manifests changed: `python3 tools/dev/jsony_check.py`.
- If `milestones.json` or the Work block changed:
  `python3 tools/dev/build-common.py --build` then `--check`.
- If `work-moves.json` exists: STOP — a reviewed Work export is pending; run
  `python3 tools/dev/build-work-tracker.py --apply-moves` first.
- If vocabulary/routing changed: `python3 tools/dev/check-drift.py`.
- If HTML changed: `python3 tools/check-a11y.py`.
- The `build-whole-md.py` / `build-depth-md.py` index-drift checks were retired
  with their `worldview.md` / `backend.md` chapters (N16, 2026-11-21).
- Report warnings, the level chosen and the next one. Do not commit, push or
  publish.

### 2. Commit
- Clean tree → continue.
- Pending edits → list the source paths and **ask for confirmation**.
- On a yes: stage only those named paths (never `-A`) and commit.
- Never stage `sw.js`, `tools/flove-localhost.zip` or the vocabulary index.
- Stop before push.

### 3. Publish main
- `git fetch origin`; if `origin/main` has commits local `main` lacks,
  `merge --ff-only`; a non-fast-forward → STOP.
- `git push origin main`.
- Do not repeat `jsony` or `check-distro`: level 1 is the gate.
- Push only the changed paths with `tools/dev/publish-web-files.sh`
  (explicit paths, or `--diff <last Flove-Source>`); never the full tree.
- Report the GitHub SHA/subject; Pages takes ~1 min.

### 4. Heavy + publish main
- Run [`heavy.md`](heavy.md): sync vocabulary, Whole and Data depth; rebuild
  `sw.js` and the zip; commit only those artifacts.
- `git gc --prune=now` locally; report `git count-objects -vH`.
- `git fetch origin`; ff-only; `git push origin main`.
- Gitea Admin → `marc/flove` → Git GC (or wait for `git_gc_repos`); never raw
  `git gc` on the live bare repo.
- Publish only what changed with `publish-web-files.sh`: `sw.js`,
  `development/standards/vocabulary.html`, `tools/flove-localhost.zip` and any
  source paths since the last `Flove-Source`. This is the single publish; do not
  run level 3 first. Use `publish-web.sh` only for a full resync.

### 5. Full release
- Complete level 4.
- Publish `tools/dev/publish-risa.sh`,
  `publish-ama.sh`, `publish-liberada.sh`, and
  `projects/lowai/publish-lowai.sh`.
- APK → `updaty-apk`. Report each target, including "sin cambios".

## Preconditions

- Repo `~/Documents/flove`, branch `main`, remote `github` →
  `https://github.com/floveorg/floveorg.github.io.git`.
- Main-site PAT in `~/agents/token-github-flove.md`; level 5 also needs the risa,
  ama, liberada and lowai tokens (see [`heavy.md`](heavy.md) §Targets).
- The work is committed, or listed for the owner's go-ahead in level 2.

## Guardrails

- **Never print a PAT**; mask it in echoed commands and URLs.
- **Source at level 2, artifacts at level 4** — never `-A`, never stage `sw.js`,
  zips or the vocabulary index at level 2.
- **Never push before level 3.** Never publish on a hard gate failure.
- The main site goes through `publish-web-files.sh` (incremental) or
  `publish-web.sh` (full resync); never push flove `main` to GitHub.
- **Level 4 skips level 3's publish; it still publishes once, after heavy.**
- Subdomains only at level 5; APK via `updaty-apk`.
- This publishes to the open internet: flag secrets or private data first.

## Personal config

See `https://flove.org/development/standards/skills/CONFIG.md` for overrides.

Standing rules: `https://flove.org/development/standards/skills/standing.md`.
