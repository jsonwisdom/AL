#!/usr/bin/env bash
set -euo pipefail

OUT="_truth/status/last_run.json"
PUB="status.json"

mkdir -p _truth/status

NOW="$(date -u +%FT%TZ)"
COMMIT="$(git rev-parse HEAD)"
ROOT_HASH="$(jq -r '.root_sha256' _truth/root/alms_root.json)"

jq -n \
  --arg t "$NOW" \
  --arg c "$COMMIT" \
  --arg r "$ROOT_HASH" \
  '{
    last_run: $t,
    commit: $c,
    root_sha256: $r,
    runner: "github-actions",
    status: "OK"
  }' > "$OUT"

cp "$OUT" "$PUB"

echo "LAST_RUN_WRITTEN $NOW"
