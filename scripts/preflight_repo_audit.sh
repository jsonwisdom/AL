#!/usr/bin/env bash
set -euo pipefail

echo "PREFLIGHT_REPO_AUDIT"

test -f scripts/build_merkle_root.sh || { echo "FAIL missing merkle builder"; exit 1; }
test -f _truth/merkle/root.txt || { echo "FAIL missing merkle root"; exit 1; }
test -f _truth/merkle/manifest.json || { echo "FAIL missing merkle manifest"; exit 1; }

jq . _truth/merkle/manifest.json >/dev/null

CANON_ROOT="$(cat _truth/merkle/root.txt | tr -d '\n')"
MANIFEST_ROOT="$(jq -r '.root // empty' _truth/merkle/manifest.json | sed 's/^sha256://')"

if [ "$CANON_ROOT" != "$MANIFEST_ROOT" ]; then
  echo "FAIL canonical root mismatch"
  echo "root_txt=$CANON_ROOT"
  echo "manifest=$MANIFEST_ROOT"
  exit 1
fi

if [ -f status.json ]; then
  STATUS_ROOT="$(jq -r '.merkle_root // empty' status.json 2>/dev/null || true)"
  if [ -n "$STATUS_ROOT" ] && [ "$STATUS_ROOT" != "$CANON_ROOT" ]; then
    echo "WARN ROOT_SURFACE_DRIFT status_root=$STATUS_ROOT canonical_root=$CANON_ROOT"
  fi
fi

if grep -R "UNKNOWN_HASH" _truth/receipts receipts docs studio scripts site 2>/dev/null; then
  echo "WARN UNKNOWN_HASH present"
fi

if git status --short | grep -q '^?? site/index.html'; then
  echo "FAIL new homepage detected: site/index.html"
  echo "Use studio/live-intel or site/cards instead."
  exit 1
fi

echo "PREFLIGHT_OK"
