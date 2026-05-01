#!/usr/bin/env bash
set -euo pipefail

ROOT_FILE="_truth/courts/COURT_ROOT.canonical.json"
BATCH_FILE="courts_batch.txt"

EXPECTED_ROOT="f3bc4bbff21138e99574d80757d3d39c60eed7272cb5e9511be008d356a28a3f"

echo "=== GOBLIN COURT ROOT VERIFIER ==="

if [ ! -f "$ROOT_FILE" ]; then
  echo "FAIL: missing $ROOT_FILE"
  exit 1
fi

jq -cS . _truth/courts/leaf*/verdict_*.canonical.json | sort > "$BATCH_FILE"

ACTUAL_ROOT="$(sha256sum "$BATCH_FILE" | awk '{print $1}')"

echo "expected_root=$EXPECTED_ROOT"
echo "actual_root=$ACTUAL_ROOT"

if [ "$ACTUAL_ROOT" != "$EXPECTED_ROOT" ]; then
  echo "COURT_ROOT_INVALID"
  exit 1
fi

echo "COURT_ROOT_VALID"
echo "POLICY: leaf MUST have UPHELD verdict before inclusion"
