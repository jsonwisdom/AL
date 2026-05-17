#!/usr/bin/env bash
set -euo pipefail

echo "[ROOT CONTINUITY CHECKPOINT]"

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

HEAD_COMMIT="$(git rev-parse HEAD)"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
TIMESTAMP_ISO="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
OUT_DIR="receipts/root-continuity"
OUT_FILE="$OUT_DIR/cr_${TIMESTAMP}_root_continuity.json"
REPO_NAME="$(basename "$REPO_ROOT")"
LOCAL_BARE_PATH="../constitutional-root/${REPO_NAME}.git"
RESTORE_DOC="docs/restore.md"

mkdir -p "$OUT_DIR"

echo "[1] checking remotes"
git remote -v

echo "[2] checking local bare root"
if test -d "$LOCAL_BARE_PATH"; then
  LOCAL_BARE=true
else
  LOCAL_BARE=false
fi

echo "[3] checking restore documentation"
if test -f "$RESTORE_DOC"; then
  RESTORE_DOCUMENTED=true
else
  RESTORE_DOCUMENTED=false
fi

echo "[4] checking GitHub origin"
if git ls-remote origin HEAD > /tmp/root_continuity_github_head.txt; then
  GITHUB_OK=true
else
  GITHUB_OK=false
fi

echo "[5] checking mirror remote: codeberg"
if git remote get-url codeberg >/dev/null 2>&1 && git ls-remote codeberg HEAD > /tmp/root_continuity_mirror_head.txt; then
  MIRROR_OK=true
else
  MIRROR_OK=false
  : > /tmp/root_continuity_mirror_head.txt
fi

echo "[6] comparing heads"
GITHUB_HEAD="$(awk '{print $1}' /tmp/root_continuity_github_head.txt 2>/dev/null || true)"
MIRROR_HEAD="$(awk '{print $1}' /tmp/root_continuity_mirror_head.txt 2>/dev/null || true)"

COMMITS_ALIGNED=false
if [[ "$GITHUB_OK" == true && "$MIRROR_OK" == true && "$GITHUB_HEAD" == "$HEAD_COMMIT" && "$MIRROR_HEAD" == "$HEAD_COMMIT" ]]; then
  COMMITS_ALIGNED=true
fi

STATUS="failure"
if [[ "$LOCAL_BARE" == true && "$GITHUB_OK" == true && "$MIRROR_OK" == true && "$COMMITS_ALIGNED" == true && "$RESTORE_DOCUMENTED" == true ]]; then
  STATUS="success"
fi

cat > "$OUT_FILE" <<EOF
{
  "receipt_id": "cr_${TIMESTAMP}_root_continuity",
  "version": "0.1",
  "timestamp": "${TIMESTAMP_ISO}",
  "operation": {
    "type": "root_continuity_checkpoint",
    "description": "Verify local bare repo, GitHub remote, mirror remote, commit alignment, restore path"
  },
  "checks": {
    "local_bare_repo": ${LOCAL_BARE},
    "github_reachable": ${GITHUB_OK},
    "mirror_reachable": ${MIRROR_OK},
    "commits_aligned": ${COMMITS_ALIGNED},
    "restore_path_documented": ${RESTORE_DOCUMENTED}
  },
  "outcome": {
    "status": "${STATUS}",
    "result": {
      "head_commit": "${HEAD_COMMIT}",
      "github_head": "${GITHUB_HEAD}",
      "mirror_head": "${MIRROR_HEAD}",
      "local_bare_path": "${LOCAL_BARE_PATH}",
      "restore_doc": "${RESTORE_DOC}"
    },
    "error": null
  }
}
EOF

echo "[7] validating receipt JSON"
python3 -m json.tool "$OUT_FILE" >/dev/null

cat "$OUT_FILE"

echo "[ROOT CONTINUITY CHECKPOINT COMPLETE] $STATUS"
