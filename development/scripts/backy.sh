#!/usr/bin/env bash
# backy.sh — read-only snapshot of flove's media and repositories.
# See ../SKILL.md for scope, prerequisites and restore instructions.
set -euo pipefail
IFS=$'\n\t'

VERSION="1.3.0"

DEST="${BACKY_DEST:-$HOME/Documents/backs}"
PREFIX="${BACKY_PREFIX:-Flove}"
GITHUB_REPO="${BACKY_GITHUB_REPO:-https://github.com/floveorg/floveorg.github.io.git}"
FLOVE_REPO="${BACKY_FLOVE_REPO:-$HOME/Documents/flove}"
# Mirrored from GitHub, one bare mirror each.
EXTRA_REPOS="${BACKY_EXTRA_REPOS:-https://github.com/floveorg/risa.git https://github.com/floveorg/ama.git https://github.com/floveorg/liberada.git}"
# R2 buckets pulled through the Cloudflare API.
BUCKETS="${BACKY_BUCKETS:-all ama banco-risa}"
CF_TOKEN_FILE="${BACKY_CF_TOKEN_FILE:-$HOME/agents/token-r2-flove-all.md}"
R2_PARALLEL="${BACKY_R2_PARALLEL:-6}"

# One snapshot only: the new run replaces the previous one (see CHANGES.md).
KEEP=1
SKIP=""
FULL=0
DRY=0
HASH_ALL=0
VERIFY_SNAP=""
VERIFY_R2=0
DEFAULT_NAME="${PREFIX}$(date +%y-%m-%d)"

WARNINGS=()
LOG=""

usage() {
  cat <<'EOF'
backy — light snapshot of flove (repositories + R2 media).

Usage:
  backy.sh [options]

Options:
  --dest DIR          destination root            (default ~/Documents/backs)
  --name NAME         override FloveYY-MM-DD base (default: today's date)
  --keep N            how many snapshots to keep (default 1 = overwrite)
  --skip LIST         comma list: r2,flove,github,extra
  --buckets LIST      R2 buckets to pull      (default "all ama banco-risa")
  --flove-repo PATH   flove working repo to mirror (default ~/Documents/flove)
  --github-repo URL   GitHub Pages mirror source
  --full              ignore the previous snapshot's hardlinks (slow, full copy)
  --hash-all          also write SHA256SUMS.all for every file (slow)
  --dry-run           print the plan, write nothing
  --verify [SNAP]     verify a snapshot (default: newest complete)
  --verify-r2         with --verify, also re-list the buckets and compare
  -h, --help          this help
  -V, --version       version

Cloudflare credentials come from $BACKY_CF_TOKEN_FILE (default
~/agents/token-r2-flove-all.md) or from CLOUDFLARE_API_TOKEN +
CLOUDFLARE_ACCOUNT_ID in the environment.

Exit codes: 0 ok, 1 error, 2 bad usage.
EOF
}

log()  { local msg; msg="$(date +%H:%M:%S) $*"; printf '%s\n' "$msg" >&2; [ -n "$LOG" ] && printf '%s\n' "$msg" >> "$LOG" || true; }
warn() { WARNINGS+=("$*"); log "WARN: $*"; }
die()  { log "ERROR: $*"; exit 1; }
want() { [[ "$SKIP" != *",$1,"* ]]; }

need_cmd() { command -v "$1" >/dev/null 2>&1 || die "missing command: $1"; }

avail_kb() {
  local p="$1"
  while [ ! -d "$p" ]; do p="$(dirname "$p")"; done
  df -Pk "$p" | awk 'NR==2{print $4}'
}

latest_complete() {
  [ -d "$DEST" ] || return 0
  find "$DEST" -mindepth 1 -maxdepth 1 -type d \
       -name "${PREFIX}[0-9][0-9]-[0-9][0-9]*" ! -name ".*" \
       -exec sh -c 'test -f "$1/MANIFEST.json"' _ {} \; -print 2>/dev/null \
    | while IFS= read -r d; do printf '%s\t%s\n' "$(stat -c %Y "$d")" "$d"; done \
    | sort -rn | sed -n '1p' | cut -f2- || true
}

latest_partial() {
  local base="$1"
  [ -d "$DEST" ] || return 0
  find "$DEST" -mindepth 1 -maxdepth 1 -type d -name ".${base}.partial.*" 2>/dev/null \
    | while IFS= read -r d; do printf '%s\t%s\n' "$(stat -c %Y "$d")" "$d"; done \
    | sort -rn | sed -n '1p' | cut -f2- || true
}

parse_args() {
  while [ $# -gt 0 ]; do
    case "$1" in
      --dest)        DEST="${2:?}"; shift 2 ;;
      --name)        DEFAULT_NAME="${2:?}"; shift 2 ;;
      --keep)        KEEP="${2:?}"; shift 2 ;;
      --skip)        SKIP=",${2:?},"; shift 2 ;;
      --buckets)     BUCKETS="${2:?}"; shift 2 ;;
      --flove-repo)  FLOVE_REPO="${2:?}"; shift 2 ;;
      --github-repo) GITHUB_REPO="${2:?}"; shift 2 ;;
      --full)        FULL=1; shift ;;
      --hash-all)    HASH_ALL=1; shift ;;
      --dry-run)     DRY=1; shift ;;
      --verify)
        VERIFY_REQUESTED=1
        if [ $# -ge 2 ] && [ "${2#--}" = "$2" ]; then
          VERIFY_SNAP="$2"; shift 2
        else
          shift
        fi ;;
      --verify-r2)   VERIFY_R2=1; shift ;;
      -h|--help)     usage; exit 0 ;;
      -V|--version)  echo "backy $VERSION"; exit 0 ;;
      *) usage >&2; exit 2 ;;
    esac
  done
}

# ---------------------------------------------------------------- verification

verify_snapshot() {
  local snap="$1"
  [ -d "$snap" ] || die "no such snapshot: $snap"
  [ -f "$snap/MANIFEST.json" ] || die "not a complete snapshot (no MANIFEST.json): $snap"
  log "verifying $snap"

  ( cd "$snap" && sha256sum -c SHA256SUMS >/dev/null ) \
    || die "SHA256SUMS mismatch in $snap"
  log "checksums OK"

  local rc=0 repo
  while IFS= read -r -d '' repo; do
    if git -C "$repo" fsck --connectivity-only --no-dangling >/dev/null 2>&1; then
      log "git fsck OK  ${repo#"$snap"/}"
    else
      log "git fsck FAIL ${repo#"$snap"/}"; rc=1
    fi
  done < <(find "$snap/repos" -type d -name '*.git' -print0 2>/dev/null)

  if [ "$VERIFY_R2" = 1 ] && want r2; then
    local b rc2=0 remote
    cf_init
    for b in "${BUCKET_LIST[@]}"; do
      [ -d "$snap/r2/$b" ] || { log "r2: bucket $b not in snapshot — skip"; continue; }
      remote="$(bucket_objects "$b" | cut -f1,3 | LC_ALL=C sort)"
      if [ "$remote" = "$(cut -f1,3 "$snap/r2/$b/.backy-index.tsv" | LC_ALL=C sort)" ]; then
        log "r2: $b OK ($(wc -l < "$snap/r2/$b/.backy-index.tsv") objects)"
      else
        log "r2: $b DIFFERS from the bucket listing"; rc2=1
      fi
    done
    [ "$rc2" = 0 ] || rc=1
  fi
  [ "$rc" = 0 ] || die "verification failed"
  log "OK — $snap"
}

# --------------------------------------------------------------------- backup

require_tools() {
  need_cmd git
  need_cmd jq
  need_cmd tar
  need_cmd du
  need_cmd rsync
  if want r2; then need_cmd curl; fi
}

preflight() {
  local free_kb
  log "preflight"

  if want flove; then
    [ -d "$FLOVE_REPO" ] || die "flove repo not found: $FLOVE_REPO (use --flove-repo or --skip flove)"
    log "flove: $FLOVE_REPO"
  fi

  if want r2; then
    cf_init
    local known
    known="$(cf_api "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT}/r2/buckets?per_page=1000" \
      | jq -r '.result.buckets[].name')" \
      || die "cannot reach the Cloudflare API with the configured token"
    local b
    for b in "${BUCKET_LIST[@]}"; do
      grep -qx "$b" <<< "$known" \
        || die "bucket not found in this account: '$b' (known: $(printf '%s' "$known" | tr '\n' ' '))"
    done
    log "r2: buckets $BUCKETS"
  else
    warn "R2 pull skipped (--skip r2)"
  fi

  free_kb=$(avail_kb "$DEST")
  log "free space: $((free_kb / 1024 / 1024)) GiB at $DEST"
  if [ "$free_kb" -lt 5242880 ]; then
    warn "less than 5 GiB free — the first snapshot may not fit"
  fi
}

farm_from() {
  # Echo the directory to hardlink from, or nothing.
  local stage
  if [ "$FULL" = 1 ]; then return 0; fi
  if [ -n "$VERIFY_SNAP" ]; then return 0; fi
  stage="$(latest_partial "$DEFAULT_NAME")"
  if [ -n "$stage" ] && [ -d "$stage" ]; then echo "$stage"; return 0; fi
  latest_complete
}

hardlink_tree() {
  # $1 = source dir, $2 = target dir. Returns 1 on failure (leftovers removed).
  local src="$1" dst="$2"
  [ -d "$src" ] || return 1
  mkdir -p "$dst"
  if cp -al "$src/." "$dst/" 2>/dev/null; then
    return 0
  fi
  rm -rf "$dst"
  mkdir -p "$dst"
  return 1
}

sync_r2() {
  want r2 || { log "skip r2"; return 0; }
  local b
  for b in "${BUCKET_LIST[@]}"; do
    sync_bucket "$b"
  done
  log "r2: done"
}

# ------------------------------------------------------------------ cloudflare
# The REST API can list and fetch objects, so no rclone and no S3 key pair are
# needed: the Cloudflare API token in $CF_TOKEN_FILE is enough.

cf_creds() {
  CF_ACCOUNT="${CLOUDFLARE_ACCOUNT_ID:-}"
  CF_TOKEN="${CLOUDFLARE_API_TOKEN:-${CF_API_TOKEN:-}}"
  if [ -z "$CF_ACCOUNT" ] || [ -z "$CF_TOKEN" ]; then
    [ -f "$CF_TOKEN_FILE" ] \
      || die "no Cloudflare credentials: set CLOUDFLARE_API_TOKEN + CLOUDFLARE_ACCOUNT_ID, or $CF_TOKEN_FILE"
    [ -n "$CF_ACCOUNT" ] || CF_ACCOUNT="$(awk '
      /^# Account ID:/ { n = split($0, a, /[[:space:]]+/); print a[n]; exit }' "$CF_TOKEN_FILE")"
    [ -n "$CF_TOKEN" ] || CF_TOKEN="$(awk '
      match($0, /cfat_[A-Za-z0-9]+/) { print substr($0, RSTART, RLENGTH); exit }' "$CF_TOKEN_FILE")"
  fi
  [ -n "$CF_ACCOUNT" ] && [ -n "$CF_TOKEN" ] \
    || die "could not parse account id + API token (from environment or $CF_TOKEN_FILE)"
}

cf_init() {
  # The bearer header lives in a 0600 config file so the token never appears in
  # argv (ps) or in the log.
  cf_creds
  CF_CURLRC="$(umask 077 && mktemp "${TMPDIR:-/tmp}/backy-cf.XXXXXX")"
  printf 'header = "Authorization: Bearer %s"\n' "$CF_TOKEN" > "$CF_CURLRC"
}

cf_cleanup() { if [ -n "${CF_CURLRC:-}" ]; then rm -f "$CF_CURLRC"; fi; CF_CURLRC=""; }

cf_api() { curl -sS --fail --retry 3 --retry-delay 2 --connect-timeout 20 \
             --globoff --config "$CF_CURLRC" "$@"; }

cf_list() {
  # $1 = bucket → NDJSON, one object per line, following the cursor.
  local bucket="$1" cur="" resp trunc
  while :; do
    resp="$(cf_api "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT}/r2/buckets/${bucket}/objects?per_page=1000${cur:+&cursor=$cur}")" \
      || die "R2 list failed for bucket '$bucket'"
    printf '%s' "$resp" | jq -c '.result[]?'
    trunc="$(printf '%s' "$resp" | jq -r '.result_info.is_truncated // false')"
    cur="$(printf '%s' "$resp" | jq -r '.result_info.cursor // empty')"
    [ "$trunc" = "true" ] && [ -n "$cur" ] || break
  done
}

bucket_objects() {
  # $1 = bucket → "key<TAB>etag<TAB>size<TAB>last_modified", sorted; directory
  # markers (keys ending in /) are dropped: they hold no data.
  cf_list "$1" | jq -r 'select(.key | endswith("/") | not)
    | [.key, (.etag // ""), (.size | tostring), (.last_modified // "")]
    | @tsv' | LC_ALL=C sort
}

sync_bucket() {
  local bucket="$1"
  local dir="$PARTIAL/r2/$bucket"
  local idx="$dir/.backy-index.tsv"
  local new="$PARTIAL/.r2-$bucket.new" old="$PARTIAL/.r2-$bucket.old"
  local todo="$PARTIAL/.r2-$bucket.todo" curlrc="$PARTIAL/.r2-$bucket.curlrc"
  local n removed

  mkdir -p "$dir"
  if [ -d "$FARM/r2/$bucket" ] && hardlink_tree "$FARM/r2/$bucket" "$dir"; then
    log "r2: $bucket — hardlinked previous copy"
  fi

  bucket_objects "$bucket" > "$new"
  if [ -f "$idx" ]; then cp "$idx" "$old"; else : > "$old"; fi

  # new/changed = in the listing but not in the previous index (key+etag+size)
  # (FILENAME, not NR==FNR: an empty index would make NR==FNR swallow file 2)
  awk -F'\t' 'FILENAME == ARGV[1] { seen[$1 SUBSEP $2 SUBSEP $3] = 1; next }
               !(($1 SUBSEP $2 SUBSEP $3) in seen)' "$old" "$new" > "$todo"

  # No index yet (first run into this snapshot): an interrupted run has already
  # written some files, so skip rows whose file is on disk at the right size.
  if [ ! -s "$old" ]; then
    local kept="$todo.keep" k et sz lm
    : > "$kept"
    while IFS=$'\t' read -r k et sz lm; do
      if [ -f "$dir/$k" ] && [ "$(stat -c %s -- "$dir/$k")" = "$sz" ]; then
        continue
      fi
      printf '%s\t%s\t%s\t%s\n' "$k" "$et" "$sz" "$lm" >> "$kept"
    done < "$todo"
    mv -f "$kept" "$todo"
  fi

  # deleted remotely = in the previous index but not in the listing
  cut -f1 "$old" | LC_ALL=C sort > "$old.keys"
  cut -f1 "$new" | LC_ALL=C sort > "$new.keys"
  removed="$(LC_ALL=C comm -23 "$old.keys" "$new.keys")"
  if [ -n "$removed" ]; then
    while IFS= read -r k; do
      rm -f -- "$dir/$k"
    done <<< "$removed"
    find "$dir" -mindepth 1 -type d -empty -delete 2>/dev/null || true
    log "r2: $bucket — removed $(printf '%s\n' "$removed" | wc -l) object(s) gone from the bucket"
  fi
  rm -f "$old.keys" "$new.keys"

  n="$(wc -l < "$todo")"
  if [ "$n" -gt 0 ]; then
    log "r2: $bucket — downloading $n new/changed object(s) of $(wc -l < "$new")"
    # Download into a scratch dir, then rename into place: writing straight to
    # the target would truncate a hardlinked file and corrupt the snapshot we
    # are diffing against.
    local incoming="$dir/.backy-incoming" k
    rm -rf "$incoming"; mkdir -p "$incoming"
    ( umask 077
      { cat "$CF_CURLRC"
        jq -Rr --arg base "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT}/r2/buckets/${bucket}/objects" \
               --arg dir "$incoming" '
          split("\t") as $f | $f[0] as $k
          | "url = \"\($base)/\($k | split("/") | map(@uri) | join("/"))\"",
            "output = \"\($dir)/\($k)\""' "$todo"
      } > "$curlrc" )
    curl -sS --fail --retry 3 --retry-delay 2 --connect-timeout 20 --globoff \
      --create-dirs --parallel --parallel-max "$R2_PARALLEL" --config "$curlrc" \
      || die "R2 download failed for bucket '$bucket'"
    rm -f "$curlrc"
    while IFS=$'\t' read -r k _; do
      mkdir -p "$dir/$(dirname -- "$k")"
      mv -f -- "$incoming/$k" "$dir/$k"
    done < "$todo"
    rm -rf "$incoming"
  else
    log "r2: $bucket — up to date ($(wc -l < "$new") objects)"
  fi

  # temp+rename: a plain cp would write through the farm hardlink
  cp "$new" "$idx.tmp.$$" && mv -f "$idx.tmp.$$" "$idx"
  rm -f "$new" "$old" "$todo"
}

prepare_repo() {
  # $1 = relative name (github/floveorg.github.io.git), $2 = source path or URL
  local name="$1" src="$2" target="$PARTIAL/repos/$1" f tmp clone_args
  mkdir -p "$(dirname "$target")"

  # A local-path source would otherwise hardlink objects into the working repo,
  # so a clobbered working .git could damage the snapshot. Copy instead.
  clone_args=()
  [ -d "$src" ] && clone_args=(--no-hardlinks)

  if [ -d "$FARM/repos/$name" ] && hardlink_tree "$FARM/repos/$name" "$target"; then
    # Break hardlinks on files git may rewrite in place, so the old snapshot
    # stays byte-identical. Refs/packed-refs are updated via rename anyway.
    for f in FETCH_HEAD packed-refs config HEAD; do
      if [ -f "$target/$f" ]; then
        tmp="$target/.relink.$$"
        cp -p "$target/$f" "$tmp"
        mv -f "$tmp" "$target/$f"
      fi
    done
    rm -rf "$target/logs"
    rm -f "$target/FETCH_HEAD"
    log "git: fetch $name"
    GIT_TERMINAL_PROMPT=0 git -C "$target" -c gc.auto=0 \
      fetch --prune --tags origin '+refs/*:refs/*' >>"$PARTIAL/git.log" 2>&1 \
      || die "git fetch failed: $name (see git.log)"
  else
    rm -rf "$target"
    log "git: clone $name"
    GIT_TERMINAL_PROMPT=0 git clone --mirror "${clone_args[@]}" "$src" "$target" \
      >>"$PARTIAL/git.log" 2>&1 \
      || die "git clone failed: $src (see git.log)"
  fi
}

repo_source() {
  # $1 = relative mirror name → the source(s) it is kept in sync with.
  case "$1" in
    flove/flove.git)               printf '%s' "$FLOVE_REPO" ;;
    github/floveorg.github.io.git) printf '%s' "$GITHUB_REPO" ;;
    github/*)
      local u name
      u="${1#github/}"; name="${u%.git}"
      for u in "${EXTRA_LIST[@]}"; do
        case "$u" in "*/$name.git"|"*/$name") printf '%s' "$u"; return 0 ;; esac
      done
      printf '' ;;
    *)                             printf '' ;;
  esac
}

prepare_flove_repo() {
  # A byte-for-byte mirror of the working repo's .git — no Gitea anywhere.
  # It keeps every branch, tag and remote-tracking ref the working copy has,
  # including the branches that were never pushed anywhere. rsync is used
  # instead of git fetch because the working repo is a blobless partial clone:
  # git refuses to pack it, rsync does not care.
  local name="flove/flove.git" target="$PARTIAL/repos/flove/flove.git" f
  mkdir -p "$(dirname "$target")"

  if [ -d "$FARM/repos/$name" ] && hardlink_tree "$FARM/repos/$name" "$target"; then
    for f in packed-refs config HEAD FETCH_HEAD; do
      [ -f "$target/$f" ] || continue
      cp -p "$target/$f" "$target/.relink.$$" && mv -f "$target/.relink.$$" "$target/$f"
    done
    log "git: update flove ← $FLOVE_REPO"
  else
    rm -rf "$target"; mkdir -p "$target"
    log "git: mirror flove ← $FLOVE_REPO"
  fi

  rsync -a --delete \
    --exclude 'index' --exclude 'logs/' --exclude 'worktrees/' \
    --exclude 'FETCH_HEAD' --exclude 'ORIG_HEAD' --exclude 'COMMIT_EDITMSG' \
    "$FLOVE_REPO/.git/" "$target/" || die "rsync failed for $FLOVE_REPO/.git"

  git -C "$target" config gc.auto 0
  git -C "$target" config core.bare true
  # No Gitea in the snapshot: the working repo's `origin` points at the local
  # Gitea server. Drop just the URL — the remote-tracking refs stay (they are
  # history, not a dependency); restore sets its own URL.
  git -C "$target" config --unset-all 'remote.origin.url' 2>/dev/null || true

  # The working copy is a blobless partial clone: objects live only in the
  # promisor remote (GitHub). Walk every reachable object through cat-file so
  # git fetches exactly the ones that are absent (rev-list's own --missing
  # under-reports, and fsck tolerates promisor gaps without fetching).
  log "git: completing flove from the promisor remote"
  GIT_TERMINAL_PROMPT=0 git -C "$target" rev-list --objects --all 2>/dev/null \
    | cut -d' ' -f1 \
    | GIT_TERMINAL_PROMPT=0 git -C "$target" cat-file --batch-check \
      >>"$PARTIAL/git.log" 2>&1 \
    || warn "could not complete the flove mirror — re-run online (see git.log)"

  GIT_TERMINAL_PROMPT=0 git -C "$target" fsck --connectivity-only --no-dangling \
    >>"$PARTIAL/git.log" 2>&1 \
    || warn "flove mirror fsck reported problems — see git.log"
  local missing
  missing="$(git -C "$target" rev-list --objects --all --missing=print 2>/dev/null | grep -c '^?' || true)"
  if [ "${missing:-0}" -gt 0 ]; then
    warn "flove mirror still missing $missing object(s) — the promisor remote did not answer"
  fi
}

sync_repos() {
  if want flove; then
    prepare_flove_repo
  else
    log "skip flove"
  fi
  if want github; then
    prepare_repo "github/floveorg.github.io.git" "$GITHUB_REPO"
  else
    log "skip github"
  fi
  if want extra; then
    local u name
    for u in "${EXTRA_LIST[@]}"; do
      name="$(basename "$u")"; name="${name%.git}"
      prepare_repo "github/$name.git" "$u"
    done
  else
    log "skip extra"
  fi
}

write_changes() {
  # Compare this run with the previous snapshot (the hardlink farm) and write a
  # real changelog: refs that moved, objects added / overwritten / removed.
  local prev="${FARM:-}" prev_name="none (first snapshot)" prev_created=""
  local out="$PARTIAL/CHANGES.md"
  # An interrupted .partial is not a previous snapshot: use it for hardlinks,
  # but never as the changelog baseline.
  case "${prev##*/}" in .*.partial.*) prev="" ;; esac
  if [ -n "$prev" ] && [ ! -f "$prev/MANIFEST.json" ]; then prev=""; fi
  if [ -n "$prev" ]; then
    prev_name="$(jq -r '.name // "?"' "$prev/MANIFEST.json")"
    prev_created="$(jq -r '.created // ""' "$prev/MANIFEST.json")"
  elif [ -n "$prev" ]; then
    prev_name="$(basename "$prev")"
  fi

  local repo_rows="$PARTIAL/.chg-repos" refs="$PARTIAL/.chg-refs"
  : > "$repo_rows"; : > "$refs"
  local repo rel status counts

  while IFS= read -r -d '' repo; do
    rel="${repo#"$PARTIAL/repos/"}"
    if [ -z "$prev" ] || [ ! -d "$prev/repos/$rel" ]; then
      printf 'added\t`%s`\tnew mirror\n' "$rel" >> "$repo_rows"
      continue
    fi
    git -C "$prev/repos/$rel" for-each-ref --format='%(refname) %(objectname)' 2>/dev/null \
      | LC_ALL=C sort > "$PARTIAL/.o"
    git -C "$repo" for-each-ref --format='%(refname) %(objectname)' 2>/dev/null \
      | LC_ALL=C sort > "$PARTIAL/.n"
    awk -v rel="$rel" '
      FILENAME == ARGV[1] { o[$1] = $2; next }
      { n[$1] = $2 }
      END {
        for (r in n) {
          if (!(r in o))            print "added\t" rel "\t" r "\t(new) " n[r]
          else if (o[r] != n[r])    print "moved\t" rel "\t" r "\t" o[r] " → " n[r]
        }
        for (r in o) if (!(r in n)) print "gone\t" rel "\t" r "\t" o[r]
      }' "$PARTIAL/.o" "$PARTIAL/.n" | LC_ALL=C sort > "$PARTIAL/.d"
    rm -f "$PARTIAL/.o" "$PARTIAL/.n"

    counts="$(awk -F'\t' '{ c[$1]++ } END {
      printf "%d\t%d\t%d", (c["moved"]+0), (c["added"]+0), (c["gone"]+0) }' "$PARTIAL/.d")"
    if [ "$counts" = "0	0	0" ]; then
      printf 'unchanged\t`%s`\t—\n' "$rel" >> "$repo_rows"
    else
      printf 'updated\t`%s`\t%s ref(s) moved, %s added, %s gone\n' "$rel" \
        "$(printf '%s' "$counts" | cut -f1)" \
        "$(printf '%s' "$counts" | cut -f2)" \
        "$(printf '%s' "$counts" | cut -f3)" >> "$repo_rows"
      awk -F'\t' -v rel="$rel" '{ printf "- `%s` %s %s: %s\n", rel, $1, $3, $4 }' \
        "$PARTIAL/.d" >> "$refs"
    fi
    rm -f "$PARTIAL/.d"
  done < <(find "$PARTIAL/repos" -type d -name '*.git' -print0 2>/dev/null)

  # A mirror that exists in the old snapshot but not in this one.
  if [ -n "$prev" ] && [ -d "$prev/repos" ]; then
    while IFS= read -r -d '' oldrepo; do
      rel="${oldrepo#"$prev/repos/"}"
      [ -d "$PARTIAL/repos/$rel" ] || printf 'removed\t`%s`\tno longer mirrored\n' "$rel" >> "$repo_rows"
    done < <(find "$prev/repos" -type d -name '*.git' -print0 2>/dev/null)
  fi

  local r2_blocks="$PARTIAL/.chg-r2"; : > "$r2_blocks"
  local b newidx oldidx tot a o r
  for b in "${BUCKET_LIST[@]}"; do
    newidx="$PARTIAL/r2/$b/.backy-index.tsv"
    [ -f "$newidx" ] || continue
    oldidx="$prev/r2/$b/.backy-index.tsv"
    [ -n "$prev" ] && [ -f "$oldidx" ] || oldidx=/dev/null

    awk -F'\t' '
      FILENAME == ARGV[1] { o[$1] = $2 "\t" $3; next }
      { n[$1] = $2 "\t" $3 }
      END {
        for (k in n) {
          if (!(k in o))         print "added\t" k "\t" n[k]
          else if (o[k] != n[k]) print "overwritten\t" k "\t" n[k]
        }
        for (k in o) if (!(k in n)) print "removed\t" k "\t" o[k]
      }' "$oldidx" "$newidx" | LC_ALL=C sort > "$PARTIAL/.r2d"

    tot="$(wc -l < "$newidx")"
    a="$(awk -F'\t' '$1=="added"' "$PARTIAL/.r2d" | wc -l)"
    o="$(awk -F'\t' '$1=="overwritten"' "$PARTIAL/.r2d" | wc -l)"
    r="$(awk -F'\t' '$1=="removed"' "$PARTIAL/.r2d" | wc -l)"

    {
      printf '### `%s` — %s objects, %s\n\n' "$b" "$tot" \
        "$(du -sh --exclude='.backy-index.tsv' "$PARTIAL/r2/$b" 2>/dev/null | cut -f1)"
      if [ $((a + o + r)) -eq 0 ]; then
        printf 'No change.\n\n'
      else
        printf '%s added · %s overwritten · %s removed\n\n' "$a" "$o" "$r"
        awk -F'\t' '$1=="added" && ++n<=100 { printf "- **+** `%s` (%s B)\n", $2, $4 }' "$PARTIAL/.r2d"
        awk -F'\t' '$1=="overwritten" && ++n<=100 { printf "- **~** `%s`\n", $2 }' "$PARTIAL/.r2d"
        awk -F'\t' '$1=="removed" && ++n<=100 { printf "- **−** `%s`\n", $2 }' "$PARTIAL/.r2d"
        if [ "$a" -gt 100 ] || [ "$o" -gt 100 ] || [ "$r" -gt 100 ]; then
          printf '\n_(lists capped at 100 per category; the counts above are exact.)_\n'
        fi
        printf '\n'
      fi
    } >> "$r2_blocks"
    rm -f "$PARTIAL/.r2d"
  done

  local prev_bytes="—" now_bytes
  if [ -n "$prev" ] && [ -d "$prev" ]; then
    prev_bytes="$(du -sh "$prev" 2>/dev/null | cut -f1)"
  fi
  now_bytes="$(du -sh "$PARTIAL" 2>/dev/null | cut -f1)"

  {
    printf '# Changes — %s\n\n' "$NAME"
    printf 'Compared with: **%s**%s\n\n' "$prev_name" \
      "${prev_created:+ (created $prev_created)}"
    printf 'On disk: %s → %s\n\n' "$prev_bytes" "$now_bytes"
    printf '## Repositories\n\n'
    printf '| Mirror | Change | Detail |\n|---|---|---|\n'
    awk -F'\t' '{ printf "| %s | %s | %s |\n", $2, $1, $3 }' "$repo_rows"
    printf '\n'
    if [ -s "$refs" ]; then
      printf '### Ref changes\n\n'
      cat "$refs"
      printf '\n'
    fi
    printf '## R2 media\n\n'
    cat "$r2_blocks"
    printf '## Totals\n\n'
    printf -- '- repositories: `%s`\n' "$(jq -r '[.repos[]] | length' "$PARTIAL/MANIFEST.json")"
    printf -- '- r2 objects: `%s` in `%s` bucket(s)\n' \
      "$(jq -r '.r2.files' "$PARTIAL/MANIFEST.json")" \
      "$(jq -r '.r2.buckets | length' "$PARTIAL/MANIFEST.json")"
    printf -- '- logical size: `%s` bytes\n' \
      "$(jq -r '.totals.bytes_logical' "$PARTIAL/MANIFEST.json")"
    printf '\nGenerated by backy %s at %s.\n' "$VERSION" "$(date -Iseconds)"
  } > "$out"

  rm -f "$repo_rows" "$refs" "$r2_blocks"
  log "changes: $(printf '%s' "$prev_name") → $NAME"
}

write_manifest() {
  local repo_jsonl="$PARTIAL/.repos.jsonl"
  : > "$repo_jsonl"
  local repo rel head refs bytes src
  while IFS= read -r -d '' repo; do
    rel="${repo#"$PARTIAL/repos/"}"
    head=$(git -C "$repo" rev-parse HEAD 2>/dev/null || true)
    refs=$(git -C "$repo" for-each-ref --format='%(refname)' 2>/dev/null | wc -l)
    bytes=$(du -sb "$repo" | cut -f1)
    src="$(repo_source "$rel")"
    jq -cn --arg name "$rel" --arg head "$head" --arg source "$src" \
      --argjson refs "$refs" --argjson bytes "$bytes" \
      '{name:$name, source:$source, head:$head, refs:$refs, bytes:$bytes}' >> "$repo_jsonl"
  done < <(find "$PARTIAL/repos" -type d -name '*.git' -print0 2>/dev/null)

  local repos_json warnings_json
  repos_json=$(jq -s '.' "$repo_jsonl")
  if [ "${#WARNINGS[@]}" -eq 0 ]; then
    warnings_json='[]'
  else
    warnings_json=$(printf '%s\n' "${WARNINGS[@]}" | jq -R . | jq -s '.')
  fi

  local r2_bytes=0 r2_files=0 repos_bytes=0 total r2_enabled=true b
  local r2_jsonl="$PARTIAL/.r2.jsonl" bfiles bbytes
  : > "$r2_jsonl"
  if [ -d "$PARTIAL/r2" ]; then
    for b in "${BUCKET_LIST[@]}"; do
      [ -d "$PARTIAL/r2/$b" ] || continue
      bbytes=$(du -sb "$PARTIAL/r2/$b" | cut -f1)
      bfiles=$(find "$PARTIAL/r2/$b" -type f ! -name '.backy-index.tsv' \
        ! -path '*/.backy-incoming/*' | wc -l)
      jq -cn --arg bucket "$b" --argjson files "$bfiles" --argjson bytes "$bbytes" \
        '{bucket:$bucket, files:$files, bytes:$bytes}' >> "$r2_jsonl"
      r2_bytes=$((r2_bytes + bbytes))
      r2_files=$((r2_files + bfiles))
    done
  fi
  local r2_json; r2_json=$(jq -s '.' "$r2_jsonl"); rm -f "$r2_jsonl"
  if [ -d "$PARTIAL/repos" ]; then
    repos_bytes=$(du -sb "$PARTIAL/repos" | cut -f1)
  fi
  want r2 || r2_enabled=false
  total=$((r2_bytes + repos_bytes))

  local prev_name=""
  if [ -n "${FARM:-}" ]; then
    if [ -f "$FARM/MANIFEST.json" ]; then
      prev_name="$(jq -r '.name // ""' "$FARM/MANIFEST.json")"
    fi
    [ -n "$prev_name" ] || prev_name="$(basename "$FARM")"
  fi

  jq -n \
    --arg name "$NAME" \
    --arg created "$(date -Iseconds)" \
    --arg host "$(hostname)" \
    --arg dest "$DEST" \
    --arg version "$VERSION" \
    --arg backend "cloudflare-api" \
    --arg previous "$prev_name" \
    --argjson r2_enabled "$r2_enabled" \
    --argjson r2_bytes "$r2_bytes" \
    --argjson r2_files "$r2_files" \
    --argjson r2_buckets "$r2_json" \
    --argjson repos "$repos_json" \
    --argjson total_bytes "$total" \
    --argjson warnings "$warnings_json" \
    '{
      name: $name, created: $created, host: $host, dest: $dest,
      backy_version: $version,
      previous: ($previous | if . == "" then null else . end),
      r2: {backend: $backend, enabled: $r2_enabled, bytes: $r2_bytes,
           files: $r2_files, buckets: $r2_buckets},
      repos: $repos,
      totals: {bytes_logical: $total_bytes},
      warnings: $warnings
    }' > "$PARTIAL/MANIFEST.json"

  log "manifest: $(jq -c '{totals, warnings}' "$PARTIAL/MANIFEST.json")"
  rm -f "$repo_jsonl"
}

write_restore() {
  local R2_RESTORE="" b
  for b in "${BUCKET_LIST[@]}"; do
    [ -d "$PARTIAL/r2/$b" ] || continue
    R2_RESTORE="${R2_RESTORE}### Bucket \`${b}\` — \`r2/${b}/\`

\`\`\`bash
rclone copy r2/${b}/ r2flove:${b}
\`\`\`

"
  done
  [ -n "$R2_RESTORE" ] || R2_RESTORE="_(none — this snapshot was taken with --skip r2)_"
  cat > "$PARTIAL/RESTORE.md" <<EOF
# Restore — ${NAME}

Created: $(date -Iseconds)
Snapshot: \`${NAME}\`

All paths below are relative to this folder. Media and git objects are
hardlinked from the snapshot this one replaced, so copying this folder with
\`cp -a\` (or rsync \`-H\`) preserves the space saving.

Only one snapshot is kept: the next run writes a new dated folder and removes
this one. \`CHANGES.md\` records exactly what moved, appeared or disappeared
since the snapshot it replaced.

## 1. Repositories

### 1a. flove source repo (a copy of the working repo)

\`\`\`bash
git clone repos/flove/flove.git ~/Documents/flove-restored
cd ~/Documents/flove-restored
git remote add origin <the remote you use now>
\`\`\`

This mirror is a byte-for-byte copy of the working repo's \`.git\`, completed
from the promisor remote. It carries **every** local branch, tag and
remote-tracking ref — including the branches that were never pushed anywhere:

\`\`\`bash
git -C repos/flove/flove.git for-each-ref --format='%(refname:short)'
\`\`\`

No Gitea is involved at any point: no clone, no fetch, no URL in the snapshot.

### 1b. GitHub Pages source

\`\`\`bash
git clone repos/github/floveorg.github.io.git ~/Documents/flove-github
\`\`\`

### 1c. Project sites

One bare mirror each, self-contained:

\`\`\`bash
git clone repos/github/risa.git      ~/Documents/risa
git clone repos/github/ama.git       ~/Documents/ama
git clone repos/github/liberada.git  ~/Documents/liberada
\`\`\`

## 2. R2 media

${R2_RESTORE}

These are live buckets, not an archive: restore by uploading the tree back with
any S3 client (rclone, aws-cli, wrangler). Nothing else in the snapshot uses them.

## 3. Verify

\`\`\`bash
cd ${NAME}
sha256sum -c SHA256SUMS
for r in repos/*/*.git; do git -C "\$r" fsck --connectivity-only || echo "BAD \$r"; done
# media: re-list the buckets and diff against each .backy-index.tsv
backy.sh --verify --verify-r2
\`\`\`

## Not included (by design)

- \`~/agents/**\` tokens and recovery codes
- \`~/.ssh\`, \`~/.gnupg\`
- \`~/.agents/**\`, \`~/.config/**\`
- build caches (\`flove-artifacts/nety/target\`, \`android-sdk\`, \`node_modules\`)
EOF
}

write_checksums() {
  ( cd "$PARTIAL" && sha256sum MANIFEST.json RESTORE.md CHANGES.md > SHA256SUMS )
  if [ "$HASH_ALL" = 1 ]; then
    log "hashing every file (slow)"
    ( cd "$PARTIAL" && find r2 repos -type f -print0 2>/dev/null \
        | sort -z | xargs -0 -r sha256sum > SHA256SUMS.all )
  fi
}

prune_old() {
  [ "$KEEP" -gt 0 ] || return 0
  local old
  while IFS= read -r old; do
    [ -n "$old" ] || continue
    [ "$old" = "$FINAL" ] && continue
    log "prune: removing $old"
    rm -rf "$old"
  done < <(find "$DEST" -mindepth 1 -maxdepth 1 -type d \
             -name "${PREFIX}[0-9][0-9]-[0-9][0-9]*" ! -name ".*" \
             -exec sh -c 'test -f "$1/MANIFEST.json"' _ {} \; -print 2>/dev/null \
           | while IFS= read -r d; do printf '%s\t%s\n' "$(stat -c %Y "$d")" "$d"; done \
           | sort -rn | tail -n +$((KEEP + 1)) | cut -f2-)
}

main() {
  parse_args "$@"
  trap cf_cleanup EXIT

  # IFS excludes space, so split these lists explicitly.
  IFS=' ' read -r -a BUCKET_LIST <<< "$BUCKETS"
  IFS=' ' read -r -a EXTRA_LIST <<< "$EXTRA_REPOS"

  if [ "$VERIFY_REQUESTED" = 1 ]; then
    local snap="${VERIFY_SNAP:-}"
    [ -n "$snap" ] || snap="$(latest_complete)"
    [ -n "$snap" ] || die "no complete snapshot found under $DEST"
    verify_snapshot "$snap"; return
  fi

  require_tools
  preflight

  local base="${DEFAULT_NAME}"
  PARTIAL="$DEST/.${base}.partial.$$"
  FARM="$(farm_from)"

  if [ "$DRY" = 1 ]; then
    log "dry-run plan"
    log "  dest:    $DEST"
    log "  name:    $base (replaces a same-date snapshot)"
    log "  farm:    ${FARM:-none (full copy)}"
    log "  r2:      $(want r2 && echo "buckets: $BUCKETS" || echo skipped)"
    log "  repos:   repos/flove/flove.git ← $FLOVE_REPO $(want flove || echo '(skip)')"
    log "           repos/github/floveorg.github.io.git ← $GITHUB_REPO $(want github || echo '(skip)')"
    for _u in "${EXTRA_LIST[@]}"; do
      log "           repos/github/$(basename "$_u" .git).git ← $_u $(want extra || echo '(skip)')"
    done
    log "  keep:    $KEEP (1 = overwrite the previous snapshot)"
    return 0
  fi

  mkdir -p "$DEST"
  chmod 700 "$DEST" 2>/dev/null || true
  mkdir -p "$PARTIAL"
  LOG="$PARTIAL/backy.log"
  log "backy $VERSION — ${base}"

  if [ -n "$FARM" ]; then
    log "hardlink farm: $FARM"
  else
    log "hardlink farm: none (first snapshot or --full)"
  fi

  sync_r2
  sync_repos

  NAME="$base"
  write_manifest
  write_changes
  write_restore
  write_checksums

  # Overwrite model: one snapshot per date. A same-day re-run replaces the
  # folder instead of piling up -2, -3 …
  FINAL="$DEST/$base"
  if [ -e "$FINAL" ]; then
    local old="$DEST/.replaced-$base.$$"
    log "overwrite: replacing existing $FINAL"
    mv "$FINAL" "$old"
    mv "$PARTIAL" "$FINAL" || { mv "$old" "$FINAL"; die "could not move snapshot into place"; }
    rm -rf "$old"
  else
    mv "$PARTIAL" "$FINAL"
  fi
  LOG="$FINAL/backy.log"
  # keep MANIFEST.name in sync with the real folder name
  jq --arg n "$NAME" '.name = $n' "$FINAL/MANIFEST.json" > "$FINAL/.m.json" \
    && mv "$FINAL/.m.json" "$FINAL/MANIFEST.json"
  ( cd "$FINAL" && sha256sum MANIFEST.json RESTORE.md CHANGES.md > SHA256SUMS )

  # remove other interrupted partials for today
  find "$DEST" -mindepth 1 -maxdepth 1 -type d -name ".${base}.partial.*" -exec rm -rf {} + 2>/dev/null || true

  log "done: $FINAL"
  log "size on disk: $(du -sh "$FINAL" | cut -f1)"
  log "next: $(basename "$0") --verify '$FINAL'"

  prune_old
}

# --verify is handled inside parse_args; initialise the flag here.
VERIFY_REQUESTED=0
main "$@"
