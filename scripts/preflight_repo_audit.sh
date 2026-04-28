#!/usr/bin/env bash
set -euo pipefail

echo "PREFLIGHT_REPO_AUDIT"

test -f scripts/build_merkle_root.sh || { echo "FAIL missing merkle builder"; exit 1; }
test -f _truth/merkle/root.txt || { echo "FAIL missing merkle root"; exit 1; }
test -f _truth/merkle/manifest.json || { echo "FAIL missing merkle manifest"; exit 1; }

if git status --short | grep -q '^?? site/index.html'; then
  echo "FAIL new homepage detected: site/index.html"
  echo "Use site/live/index.html instead."
  exit 1
fi

if grep -R "UNKNOWN_HASH" _truth/receipts _truth/cards site/cards 2>/dev/null; then
  echo "WARN UNKNOWN_HASH present"
fi

jq . _truth/merkle/manifest.json >/dev/null

echo "PREFLIGHT_OK"
