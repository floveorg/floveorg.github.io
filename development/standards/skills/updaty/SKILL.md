---
name: updaty
description: >-
  Publish or heavy-release the flove website: gate, commit source, rebuild
  packages and sw.js, publish main and subdomains. Use for "updaty", "update the
  web", "publish the site", "upgrade", "rebuild zip", "full release", or updaty
  levels 1–5.
---

# updaty — publish and release flove

One skill for the site and its artifacts. **Default from now on:** auto-pick the
level from the state and the request; no number needed.

## Depth

`/updatyN` runs levels 1 → N and stops.

1. **Gate** — read-only standards check; no writes.
2. **Commit** — source only; no push.
3. **Publish main** — push + publish; no heavy.
4. **Heavy + publish main** — sync + `sw.js` + zip, then one push + publish.
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
- Run `bash development/scripts/check-distro.sh`; hard errors → STOP.
- If `apps/` or manifests changed: `python3 development/scripts/jsony_check.py`.
- If vocabulary/routing changed: `python3 development/standards/scripts/check-drift.py`.
- If HTML changed: `python3 tools/check-a11y.py`.
- If the diff touches `docs/index.html`: `python3 development/scripts/build-whole-md.py --check`;
  drift → STOP and flag `development/standards/worldview.md`.
- If the diff touches `development/index.html`: `python3 development/scripts/build-depth-md.py --check`;
  drift → STOP and flag `development/standards/backend.md`.
- Report warnings, the level chosen and the next one. Do not commit, push or
  publish.

Mappings: `docs/index.html` → `worldview.md`; `development/index.html` →
`backend.md`.

### 2. Commit
- Clean tree → continue.
- Pending edits → list the source paths and **ask for confirmation**.
- On a yes: stage only those named paths (never `-A`) and commit.
- If level 1 flagged index drift, run `build-whole-md.py` / `build-depth-md.py`
  and include `worldview.md` / `backend.md` in the commit.
- Never stage `sw.js`, `tools/flove-localhost.zip` or the vocabulary index.
- Stop before push.

### 3. Publish main
- `git fetch origin`; if `origin/main` has commits local `main` lacks,
  `merge --ff-only`; a non-fast-forward → STOP.
- `git push origin main`.
- Do not repeat `jsony` or `check-distro`: level 1 is the gate.
- `bash development/scripts/publish-web.sh`.
- Report the GitHub SHA/subject; Pages takes ~1 min.

### 4. Heavy + publish main
- Run [`heavy.md`](heavy.md): sync vocabulary, Whole and Data depth; rebuild
  `sw.js` and the zip; commit only those artifacts.
- Then do the level-3 fetch/ff-only, push and `publish-web.sh` **once**.
- Before the push: `git gc --prune=now`; report `git count-objects -vH`.
- After the push: Gitea Admin → `marc/flove` → Git GC (or wait for
  `git_gc_repos`); never raw `git gc` on the live bare repo.
- Do not run level 3 first; this is the single publish after heavy. No repeated
  gate or jsony.

### 5. Full release
- Complete level 4.
- Publish `development/standards/scripts/publish-risa.sh`,
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
- The main site goes through `publish-web.sh`; never push flove `main` to GitHub.
- Subdomains only at level 5; APK via `updaty-apk`.
- This publishes to the open internet: flag secrets or private data first.

## Personal config

See `https://flove.org/development/standards/skills/CONFIG.md` for overrides.

Standing rules: `https://flove.org/development/standards/skills/standing.md`.
