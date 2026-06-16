#!/usr/bin/env bash
set -euo pipefail

MANIFEST="_truth/merkle/manifest.json"
ROOT_FILE="_truth/merkle/root.txt"

test -f "$MANIFEST" || { echo "FATAL: MISSING_MANIFEST"; exit 1; }
test -f "$ROOT_FILE" || { echo "FATAL: MISSING_ROOT_FILE"; exit 1; }

EXPECTED="$(cat "$ROOT_FILE" | sed 's/^sha256://')"
ACTUAL="$(jq -r '.leaves[].hash' "$MANIFEST" | ./scripts/merkle_from_hashes.sh | sed 's/^sha256://')"

if [ "$EXPECTED" != "$ACTUAL" ]; then
  echo "FATAL: MANIFEST_ROOT_RECOMPUTE"
  echo "expected=$EXPECTED"
  echo "actual=$ACTUAL"
  exit 1
fi

echo "MERKLE_ROOT_VERIFY_OK root=sha256:$ACTUAL"
