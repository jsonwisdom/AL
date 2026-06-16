#!/usr/bin/env bash
set -euo pipefail

echo "STRICT_MODE_START"

FAIL=0

find _truth receipts docs studio -type f -name "*.json" 2>/dev/null | LC_ALL=C sort | while read -r f; do
  jq . "$f" >/dev/null || { echo "FAIL invalid_json $f"; exit 1; }
done

if grep -R "UNKNOWN_HASH" _truth/receipts _truth/cards site/cards 2>/dev/null; then
  echo "FAIL UNKNOWN_HASH present in production paths"
  FAIL=1
fi

ROOT_TXT="$(cat _truth/merkle/root.txt | tr -d "[:space:]")"
ROOT_MANIFEST="$(jq -r ".root" _truth/merkle/manifest.json | sed "s/^sha256://")"

if [ "$ROOT_TXT" != "$ROOT_MANIFEST" ]; then
  echo "FAIL merkle_root_mismatch"
  FAIL=1
fi

if [ "$FAIL" -ne 0 ]; then
  echo "STRICT_MODE_FAIL"
  exit 1
fi

echo "STRICT_MODE_OK"
