#!/usr/bin/env bash
set -euo pipefail

mkdir -p _truth/status

NOW="$(date -u +%FT%TZ)"
COMMIT="$(git rev-parse HEAD)"
ROOT_HASH="$(jq -r '.root_sha256' _truth/root/alms_root.json)"

TMP="$(mktemp)"

jq -cS -n \
  --arg t "$NOW" \
  --arg c "$COMMIT" \
  --arg r "$ROOT_HASH" \
  '{
    last_run: $t,
    commit: $c,
    root_sha256: $r,
    runner: "github-actions",
    status: "OK"
  }' > "$TMP"

mv "$TMP" _truth/status/last_run.json
cp _truth/status/last_run.json status.json

echo "LAST_RUN_WRITTEN $NOW"
