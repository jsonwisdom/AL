#!/usr/bin/env bash
# reproduce.sh - FED-AI-2026-006 Meta-Replay Stranger Test
# Usage: ./reproduce.sh

set -euo pipefail

START_TIME=$(date +%s)

echo "FED-AI-2026-006 Meta-Replay Starting..."
echo "Verifying committed artifacts against manifest.json..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v jq >/dev/null 2>&1; then
  echo "ERROR: jq is required"
  exit 1
fi

for f in manifest.json derivative_map.json; do
  if [[ ! -f "$f" ]]; then
    echo "ERROR: missing $f"
    exit 1
  fi
  jq empty "$f" >/dev/null
  echo "$f: OK"
done

FAILED=0
while IFS= read -r row; do
  file=$(echo "$row" | jq -r '.file')
  expected=$(echo "$row" | jq -r '.sha256')

  if [[ ! -f "$file" ]]; then
    echo "MISSING: $file"
    FAILED=1
    continue
  fi

  actual=$(sha256sum "$file" | awk '{print $1}')
  if [[ "$actual" != "$expected" ]]; then
    echo "MISMATCH: $file"
    echo "EXPECTED: $expected"
    echo "ACTUAL:   $actual"
    FAILED=1
  else
    echo "HASH_OK: $file"
  fi
done < <(jq -c '.artifacts[]' manifest.json)

if [[ "$FAILED" != "0" ]]; then
  echo "FAILED: artifact verification failed"
  exit 1
fi

if ! jq -e '.legitimacy_can_override_evidence == false' derivative_map.json >/dev/null; then
  echo "FAILED: derivative_map invariant missing or false check failed"
  exit 1
fi

echo "Lineage check: OK"
echo "Invariants check: legitimacy_can_override_evidence = false"

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo "SUCCESS: REALITY_CONFIRMED"
echo "Duration: ${DURATION} seconds"
