#!/usr/bin/env bash
set -euo pipefail
ROOT="_truth/receipts/index.json"
test -f "$ROOT" || { echo "REPLAY_DIVERGED: canonical index file missing"; exit 1; }
COUNT=$(jq '.index.receipts | length' "$ROOT" 2>/dev/null || echo "0")
[ "$COUNT" -gt 0 ] || { echo "REPLAY_DIVERGED: canonical index is empty or path mismatch"; exit 1; }
echo "Verifying $COUNT canonical receipts..."
while IFS= read -r receipt; do
  path=$(echo "$receipt" | jq -r '.path')
  expected=$(echo "$receipt" | jq -r '.hash')
  test -f "$path" || { echo "REPLAY_DIVERGED: missing receipt -> $path"; exit 1; }
  actual=$(sha256sum "$path" | awk '{print "sha256:"$1}')
  if [ "$actual" != "$expected" ]; then
    echo "REPLAY_DIVERGED: canonical index mismatch -> $path"
    echo "expected: $expected"
    echo "actual:   $actual"
    exit 1
  fi
done < <(jq -c '.index.receipts[]' "$ROOT")
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "REPLAY_CONFIRMED $TS"
exit 0
