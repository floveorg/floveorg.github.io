#!/usr/bin/env bash
# publish-web-files.sh — incremental flove.org publish.
#
# Pushes only the named (or diffed) paths to floveorg/floveorg.github.io,
# applying the same public filter as publish-web.sh but without re-uploading the
# whole tree. Use it for updaty3/4; keep publish-web.sh for a full resync.
#
# Usage:
#   publish-web-files.sh [--diff <base>] [--dry-run] [path...]
#
#   publish-web-files.sh development/index.html
#   publish-web-files.sh --diff 90ea5944
#   publish-web-files.sh sw.js development/standards/vocabulary.html tools/flove-localhost.zip
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$(readlink -f "$0")")/../.." && pwd)"
GH_REPO="floveorg/floveorg.github.io"
TOKEN_FILE="$HOME/agents/token-github-flove.md"
TOKEN=$(grep -oP 'github_pat_\S+|ghp_\S+' "$TOKEN_FILE" 2>/dev/null | head -1)
[ -n "${TOKEN:-}" ] || { echo "no GitHub token in $TOKEN_FILE"; exit 1; }

DIFF_BASE=""
DRY=0
PATHS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --diff) DIFF_BASE="${2:-}"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    -h|--help) sed -n '2,15p' "$0"; exit 0 ;;
    *) PATHS+=("$1"); shift ;;
  esac
done

cd "$REPO_ROOT"
git fetch -q github main

# A path is public unless it is in a Gitea-only / filtered area.
is_publishable() {
  case "$1" in
    development/addons/*|apps/flove-apk/*|tools/flove-apk/*|public/*|\
    frotis/*|chacrikun/*|electroorchestra/*) return 1 ;;
    apps/sys/nety/index.html) return 0 ;;
    apps/sys/nety/*) return 1 ;;
    .DS_Store|Thumbs.db|*.swp|*.swo|*.kate-swp|*.log) return 1 ;;
    *) return 0 ;;
  esac
}

# path -> A (add/update) or D (delete)
OPS=()
if [ -n "$DIFF_BASE" ]; then
  while IFS=$'\t' read -r status p1 p2; do
    case "$status" in
      R*|C*) OPS+=("D $p1"); OPS+=("A $p2") ;;
      D)     OPS+=("D $p1") ;;
      *)     OPS+=("A $p1") ;;
    esac
  done < <(git diff --name-status "$DIFF_BASE"..HEAD)
fi
for p in "${PATHS[@]}"; do
  if git cat-file -e "HEAD:$p" 2>/dev/null || [ -f "$REPO_ROOT/$p" ]; then
    OPS+=("A $p")
  else
    OPS+=("D $p")
  fi
done

# Deduplicate while keeping the last operation for each path.
declare -A LAST=()
ORDER=()
for op in "${OPS[@]}"; do
  p="${op#* }"
  if [ -z "${LAST[$p]+x}" ]; then ORDER+=("$p"); fi
  LAST["$p"]="$op"
done

STAGE_ROOT="${FLOVE_PUBLISH_TMP:-$HOME/.cache/flove-publish}"
mkdir -p "$STAGE_ROOT"
IDX="$(mktemp "$STAGE_ROOT/index.XXXXXX")"
trap 'rm -f "$IDX"' EXIT
export GIT_INDEX_FILE="$IDX"
git read-tree github/main

CHANGED=0
for p in "${ORDER[@]}"; do
  op="${LAST[$p]}"
  status="${op%% *}"
  if ! is_publishable "$p"; then
    echo "skip (not public): $p" >&2
    continue
  fi
  if [ "$status" = "D" ]; then
    if git ls-files --stage -- "$p" | grep -q .; then
      git update-index --force-remove "$p"
      CHANGED=1
      echo "remove $p"
    fi
    continue
  fi
  if git cat-file -e "HEAD:$p" 2>/dev/null; then
    mode=$(git ls-tree HEAD -- "$p" | awk '{print $1}')
    if [ "$mode" = "160000" ]; then
      echo "skip (submodule): $p" >&2
      continue
    fi
    blob=$(git rev-parse "HEAD:$p")
  elif [ -f "$REPO_ROOT/$p" ]; then
    mode=100644
    blob=$(git hash-object -w "$REPO_ROOT/$p")
  else
    echo "missing: $p" >&2
    continue
  fi
  git update-index --add --cacheinfo "$mode,$blob,$p"
  CHANGED=1
  echo "add    $p"
done

if [ "$CHANGED" -eq 0 ]; then
  echo "no publishable changes"
  exit 0
fi

TREE=$(git write-tree)
BASE_TREE=$(git rev-parse 'github/main^{tree}')
if [ "$TREE" = "$BASE_TREE" ]; then
  echo "no changes to publish (identical tree)"
  exit 0
fi

SOURCE=$(git rev-parse HEAD)
COMMIT=$(git -c user.name='Marc' -c user.email='marc@futbolia.org' commit-tree "$TREE" \
  -p github/main \
  -m "publish flove.org (incremental)" \
  -m "Flove-Source: $SOURCE")

if [ "$DRY" -eq 1 ]; then
  echo "dry-run: tree $TREE, commit $COMMIT, source $SOURCE"
  exit 0
fi

git push "https://x-access-token:${TOKEN}@github.com/${GH_REPO}.git" "$COMMIT:main"
echo "published → https://flove.org/ (incremental, $SOURCE)"
