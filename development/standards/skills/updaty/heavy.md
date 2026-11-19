# updaty · heavy release (level 3+)

Level 4 of `updaty`: refresh the artifacts a page push cannot rebuild, then
publish main. Level 5 adds the subdomains.

## Preflight

Show `git status -sb` and `git log --oneline -3`. Artifacts build from committed
HEAD, so pending source is a STOP — commit it at `updaty2` first. Dirty
`projects/liberada/ama`, `projects/liberada/liberada.net` and
`projects/liberada/risa` are expected: their scripts publish the working trees.
Any other dirty submodule needs a decision. For level 5, verify the target tokens
now.

## Sync

1. **Vocabulary.** Refresh `development/standards/vocabulary.html` from the latest
   slot texts (titles, taglines, entry labels, about bodies); commit
   `Sync vocabulary index (updaty4)`.
2. **Whole table.** `python3 development/scripts/build-whole-md.py` regenerates the
   33-row taxonomy in `development/standards/worldview.md`; `--check` reports
   drift. Commit `Sync Whole table (updaty4)` if changed.
3. **Data depth.** `python3 development/scripts/build-depth-md.py` regenerates the
   five-level table in `development/standards/backend.md`; `--check` reports
   drift. Commit `Sync Data depth (updaty4)` if changed.

## Rebuild

1. **Service worker.** `node tools/build-sw.mjs`. This is the only place `sw.js`
   is refreshed. Commit it if changed.
2. **Packages.** `bash tools/build-flove-zip.sh`; it reports the zip size. A build
   failure is a STOP. Commit only the changed artifacts.

## Gitea compaction (level 4)

- **Local:** `git gc --prune=now` before the push; report
  `git count-objects -vH`.
- **Gitea:** Admin → Repositories → `marc/flove` → Git GC, or wait for the
  `[cron.git_gc_repos]` schedule. Never run raw `git gc` on the live bare repo
  while Gitea is serving.
- GC consolidates packs and drops prune-packable objects; it cannot remove
  reachable zip blobs. Report before/after. Bare repo inside the Gitea
  container: `/data/git/repositories/marc/flove.git`.

## Zip growth (pending decision)

`tools/flove-localhost.zip` (~12 MB) is committed on every release and stays in
history; `git gc` cannot drop reachable blobs. This is level 3's main repo growth.

- **Clean:** stop versioning the zip — upload it as a Gitea release asset (or R2)
  and keep only the latest local copy; add `tools/flove-localhost.zip` to
  `.gitignore`.
- **Deterministic:** if it stays tracked, fix the mtimes (e.g. `SOURCE_DATE_EPOCH`
  via `touch -d`) and keep `zip -X` so an unchanged tree yields an identical zip
  and the commit becomes a no-op. Today the mtime changes every release.

## Targets (level 5)

- **Main site:** `bash development/scripts/publish-web.sh`
- **Subdomains:** run each from the repo root:
  `bash development/standards/scripts/publish-risa.sh`,
  `bash development/standards/scripts/publish-ama.sh`,
  `bash development/standards/scripts/publish-liberada.sh`, and
  `bash projects/lowai/publish-lowai.sh`.
  Each clones its target, rsyncs the source working tree and force-pushes; they
  are idempotent and print "sin cambios que publicar" when unchanged. Never
  commit inside the three submodules.
- **APK:** `updaty-apk`, never rebuilt here.

## Package & targets

`tools/flove-localhost.zip` is built from committed HEAD by
`tools/build-flove-zip.sh`, a path-preserving subset of the repo root nested under
`flove-localhost/`: `index.html`, `apps/`, the shared images, `tools/`
(`start.html`, `manifest.webmanifest`, icon, `routing.json`, `devices.json`),
`docs/` (without `docs/docs-files/`) and root `sw.js`. Audio and
`tools/flove-apk/` never ship; paths match the live site, so no href is rewritten.

Tokens by target (name the file, never the value): main site
`~/agents/token-github-flove.md`; risa `…-risa.md`; ama `…-ama.md`; liberada
`…-liberada.md`; lowai `…-lowai.md`. A missing token for a requested target is a
STOP, not a skip.

## Guardrails

- **Only build artifacts may be committed at this level:** `sw.js`, the vocabulary
  index, `tools/flove-localhost.zip` and other configured package artifacts.
  Never source files, never `git add -A`.
- **Never print a PAT.** Mask it in echoed commands and URLs.
- **A hard distro-check failure aborts publishing** — no bypass for a full
  release.
- The package must contain exactly the list above under `flove-localhost/`.
  Anything else, or a flattened tree → STOP and report.
- The main site always goes through `publish-web.sh`; never push the full dev tree
  to GitHub.
- Subdomains are level 5 only. The APK is `updaty-apk`.
