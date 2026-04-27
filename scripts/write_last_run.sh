#!/usr/bin/env bash
set -euo pipefail

OUT="_truth/status/last_run.json"

TS="$(date -u +%FT%TZ)"
ROOT_HASH="$(jq -r '.root_sha256' _truth/root/alms_root.json 2>/dev/null || echo UNKNOWN)"
COMMIT="$(git rev-parse HEAD 2>/dev/null || echo UNKNOWN)"

jq -n -cS \
  --arg ts "$TS" \
  --arg hash "$ROOT_HASH" \
  --arg commit "$COMMIT" \
  --arg runner "github-actions" \
  '{
    last_run:$ts,
    root_sha256:$hash,
    commit:$commit,
    runner:$runner,
    status:"OK"
  }' > "$OUT"

echo "LAST_RUN_WRITTEN $TS"
