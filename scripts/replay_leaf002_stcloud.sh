#!/usr/bin/env bash
set -euo pipefail

CID="bafkreicv6zorahyi47hcg7tje24grvxzdmgko5ekbz6ewrcyj6ujvvoita"
EXPECTED_SHA256="55f65d101f08e7ce237e6926b868d6f91b0ca7748a0e7c4b44584fa89ad5c898"
EXPECTED_SIZE="10240"
EXPECTED_BATCH_ID="f574a8741d5ed0cc67310a686ac0ba59f132a98171e723ebf001081ba04c0d21"
OUT="stcloud_leaf002_replay_bundle.tar"
DIR="stcloud_leaf002_replay"

curl -L -o "$OUT" "https://gateway.pinata.cloud/ipfs/$CID"
ACTUAL_SHA256="$(sha256sum "$OUT" | awk '{print $1}')"
ACTUAL_SIZE="$(wc -c < "$OUT" | tr -d ' ')"

if [ "$ACTUAL_SHA256" != "$EXPECTED_SHA256" ]; then
  echo "{\"verdict\":\"FAIL\",\"failure_code\":\"PAYLOAD_SHA256_MISMATCH\",\"expected\":\"$EXPECTED_SHA256\",\"actual\":\"$ACTUAL_SHA256\"}"
  exit 1
fi

if [ "$ACTUAL_SIZE" != "$EXPECTED_SIZE" ]; then
  echo "{\"verdict\":\"FAIL\",\"failure_code\":\"PAYLOAD_SIZE_MISMATCH\",\"expected\":\"$EXPECTED_SIZE\",\"actual\":\"$ACTUAL_SIZE\"}"
  exit 1
fi

rm -rf "$DIR"
mkdir -p "$DIR"
tar -xf "$OUT" -C "$DIR"

MANIFEST_SHA256="$(sha256sum "$DIR/manifest.json" | awk '{print $1}')"
BATCH_ID="$(python3 - <<'PY'
import json
with open('stcloud_leaf002_replay/manifest.json','r',encoding='utf-8') as f:
    print(json.load(f)['batch_id'])
PY
)"

if [ "$BATCH_ID" != "$EXPECTED_BATCH_ID" ]; then
  echo "{\"verdict\":\"FAIL\",\"failure_code\":\"BATCH_ID_MISMATCH\",\"expected\":\"$EXPECTED_BATCH_ID\",\"actual\":\"$BATCH_ID\"}"
  exit 1
fi

echo "{\"verdict\":\"PASS\",\"leaf_id\":\"002\",\"asset_id\":\"ST_CLOUD_CITY_BUDGET_FY2026_PROPOSED\",\"payload_cid\":\"$CID\",\"payload_sha256\":\"$ACTUAL_SHA256\",\"payload_size_bytes\":$ACTUAL_SIZE,\"manifest_sha256\":\"$MANIFEST_SHA256\",\"batch_id\":\"$BATCH_ID\"}"
