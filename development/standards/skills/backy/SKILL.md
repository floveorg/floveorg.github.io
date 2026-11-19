---
name: backy
description: >-
  Light local backup of flove: bare repo mirrors plus the R2 buckets, with
  manifest, checksums and restore notes. Read-only. Use for "backy",
  "back up flove", "copia de seguridad".
---

# backy — light snapshot of flove's repositories and media

`backy` copies everything that is **not reproducible from a single remote** into
one dated folder under `~/Documents/backs/`: every repository, plus the R2 buckets
holding the site media. It is deliberately **read-only** — it never commits,
pushes, edits a repo or rebuilds an artifact.

**Rule of thumb:** publishing → `updaty` (levels 3–5). Preserving a copy →
**backy**. Never run the heavy release first "just in case".

Need the Gitea database, docs-files, secrets, encryption, offsite or retention?
Not part of this skill — don't promise them here.

## Procedure

Run the script; never hand-roll the steps.

```bash
development/scripts/backy.sh                      # everything
development/scripts/backy.sh --skip r2            # repositories only
development/scripts/backy.sh --skip flove,extra   # subset
development/scripts/backy.sh --buckets "all ama"  # subset of media
development/scripts/backy.sh --dry-run            # plan only
development/scripts/backy.sh --verify --verify-r2 # check latest
```

It runs preflight (tools, free space, credentials, buckets), hardlinks the previous
snapshot forward, mirrors the repositories, syncs R2, writes
`MANIFEST.json` / `SHA256SUMS` / `RESTORE.md` / `CHANGES.md`, renames the
`.partial` folder to its dated name, then prunes to `--keep`.

What a snapshot contains, the bucket map, the promisor trick, exclusions,
naming/retention and config keys are in **What a snapshot holds** below.

## Prerequisites

- `git`, `jq`, `tar`, `du`, `curl` (all present on this machine).
- Cloudflare credentials for the R2 pull: the API token in
  `~/agents/token-r2-flove-all.md`, account id in the same file. No rclone, no S3
  key pair — backy talks to the Cloudflare REST API directly.

Override the credential file with `BACKY_CF_TOKEN_FILE`, or pass
`CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID` in the environment.

## Verify

Do it after the first run, and periodically:

```bash
development/scripts/backy.sh --verify                 # SHA256SUMS + git fsck on every mirror
development/scripts/backy.sh --verify --verify-r2     # also re-list every bucket and diff
```

`--verify-r2` re-reads object *listings*, not bodies, so it is cheap enough to run
every time. A quarterly `--hash-all` snapshot plus
`sha256sum -c SHA256SUMS.all` is the deeper drill.

## Restore

`RESTORE.md` inside the snapshot holds the exact commands. In short:

```bash
git clone Flove26-11-14/repos/flove/flove.git ~/Documents/flove-restored
git clone Flove26-11-14/repos/github/risa.git ~/Documents/risa
rclone copy Flove26-11-14/r2/banco-risa/ r2flove:banco-risa   # media back up
```

The Gitea database, docs-files and secrets are not in here.

## Relationship to updaty

- **Never** run `updaty4` as part of `backy`: a release mutates `sw.js`, the
  package zip and the vocabulary index, and can fail halfway. A backup must not
  depend on that.
- Want a **release snapshot**? Run `updaty4` first, then `backy` — in that order,
  manually. The snapshot records the GitHub mirror's `HEAD` in `MANIFEST.json`,
  so it is traceable to a release.

## Secrets

This skill references secret **locations**, never values:
`~/agents/token-r2-flove-all.md`, the git credential store. The bearer header goes
into a `0600` file in `$TMPDIR` and reaches curl via `--config`, so the token
never lands in `argv`, a log or the snapshot. Never paste a token into a command
that gets logged, and never sync a snapshot to a public bucket.

## What a snapshot holds

`repos/flove/flove.git` (rsync of the working `.git` — it is a blobless partial
clone, so `git clone` fails and the missing objects are fetched from the promisor
remote), bare mirrors of the GitHub repos, `r2/{all,ama,banco-risa}/` hardlinked
from the previous snapshot, and generated `MANIFEST.json`, `SHA256SUMS`,
`RESTORE.md`, `CHANGES.md`.

- Folder `FloveYY-MM-DD`; **one snapshot only** (`--keep 1` default). A same-day
  re-run replaces it; `CHANGES.md` records ref tips and R2 adds/removes.
- Not backed up: the Gitea database, `docs/docs-files`, `~/agents` tokens,
  `~/.ssh`, `~/.gnupg`, `~/.agents`, `~/.config`, build caches.
- Config keys (first `CONFIG.md` match): `dest`, `prefix`, `keep`, `flove_repo`,
  `github_repo`, `extra_repos`, `buckets`, `cf_token_file`; env equivalents
  `BACKY_*`. A failed run leaves `.partial` reusable.

**Failure modes.** No Cloudflare credentials → token file missing/unreadable or no
`cfat_…` token. `bucket not found` → a name in `--buckets` is wrong; the message
lists the real ones. `R2 list failed` → token lacks R2 read or account id is
wrong. `flove mirror still missing N object(s)` → promisor remote unreachable;
re-run. `rsync failed` → the working repo moved; check `--flove-repo`.
`git clone/fetch failed` → network/credential helper. `No space left` → prune
with `--keep`. Interrupted run → just re-run; `.partial` resumes.

Standing rules: `https://flove.org/development/standards/skills/standing.md`.
