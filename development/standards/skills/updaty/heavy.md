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
2. **Retired generators.** `build-whole-md.py` / `build-depth-md.py` and their
   `worldview.md` / `backend.md` chapters were retired together (N16, 2026-11-21);
   there is no Whole/Data-depth sync step in heavy.

## Rebuild

1. **Service worker.** `node tools/build-sw.mjs`. This is the only place `sw.js`
   is refreshed. Commit it if changed.
2. **Packages.** `bash tools/build-flove-zip.sh`; it reports the zip size. A build
   failure is a STOP. The zip is untracked (latest only): do not commit it;
   `publish-web-files.sh` copies it into the public tree.

## Gitea compaction (level 4)

- **Local:** `git gc --prune=now` before the push; report
  `git count-objects -vH`.
- **Gitea:** Admin → Repositories → `marc/flove` → Git GC, or wait for the
  `[cron.git_gc_repos]` schedule. Run it after the push and before the GitHub
  publish. Never run raw `git gc` on the live bare repo while Gitea is serving.
- GC consolidates packs and drops prune-packable objects; it cannot remove
  reachable zip blobs. Report before/after. Bare repo inside the Gitea
  container: `/data/git/repositories/marc/flove.git`.

## Zip growth (latest only)

The zip is untracked: `tools/flove-localhost.zip` is in `.gitignore` and
`git rm --cached`. `publish-web-files.sh` copies the latest local build into the
public tree, so the site keeps one zip without adding a 12 MB blob per release.
History still holds the old zips; only a history rewrite would remove them.
Optional: upload the zip as a Gitea release asset (or R2) instead of publishing it.

## Targets (level 5)

- **Main site:** `bash tools/dev/publish-web-files.sh <changed paths>`
  (incremental); `publish-web.sh` only for a full resync.
- **Subdomains:** run each from the repo root:
  `bash tools/dev/publish-risa.sh`,
  `bash tools/dev/publish-ama.sh`,
  `bash tools/dev/publish-liberada.sh`, and
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

**Next zip rebuild (2026-11-21):** the live site serves `community/index.html`, but
the downloaded package does not — `community/` is absent from the `git archive`
pathspec in `tools/build-flove-zip.sh`, and the bundled `sw.js` precaches that
missing path. Add `community/` to the pathspec and to the list above, rebuild, and
confirm `unzip -Z1 tools/flove-localhost.zip | grep -q community/index.html`
before publishing.

Tokens by target (name the file, never the value): main site
`~/agents/token-github-flove.md`; risa `…-risa.md`; ama `…-ama.md`; liberada
`…-liberada.md`; lowai `…-lowai.md`. A missing token for a requested target is a
STOP, not a skip.

## Guardrails

- **Only build artifacts may be committed at this level:** `sw.js`, the vocabulary
  index and other configured package artifacts. The zip is untracked. Never source
  files, never `git add -A`.
- **Never print a PAT.** Mask it in echoed commands and URLs.
- **A hard distro-check failure aborts publishing** — no bypass for a full
  release.
- The package must contain exactly the list above under `flove-localhost/`.
  Anything else, or a flattened tree → STOP and report.
- The main site always goes through `publish-web.sh`; never push the full dev tree
  to GitHub.
- Subdomains are level 5 only. The APK is `updaty-apk`.
