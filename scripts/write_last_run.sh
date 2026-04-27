#!/usr/bin/env bash
set -euo pipefail

mkdir -p _truth/status

NOW="$(date -u +%FT%TZ)"
COMMIT="$(git rev-parse HEAD)"
ROOT_HASH="$(jq -r '.root_sha256' _truth/root/alms_root.json)"

MERKLE_ROOT="$(jq -r '.merkle_root // "UNKNOWN"' merkle_proofs.json 2>/dev/null || echo "UNKNOWN")"
LEAF_COUNT="$(jq -r '.leaf_count // 0' merkle_proofs.json 2>/dev/null || echo "0")"
ALG="sha256_hex_concat_v1"

TMP="$(mktemp)"

jq -cS -n \
  --arg t "$NOW" \
  --arg c "$COMMIT" \
  --arg r "$ROOT_HASH" \
  --arg mr "$MERKLE_ROOT" \
  --arg alg "$ALG" \
  --argjson lc "$LEAF_COUNT" \
  '{
    last_run: $t,
    commit: $c,
    root_sha256: $r,
    merkle_root: $mr,
    merkle_algorithm: $alg,
    leaf_count: $lc,
    runner: "github-actions",
    status: "OK"
  }' > "$TMP"

mv "$TMP" _truth/status/last_run.json
cp _truth/status/last_run.json status.json

echo "LAST_RUN_WRITTEN $NOW"
