#!/usr/bin/env bash
set -euo pipefail

# This script verifies the payload for leaf 008.
# Patterned after verify_leaf006_payload.sh

PAYLOAD="_truth/anchors/leaf008/payload.b64"
OUT="_truth/anchors/leaf008/leaf008_verified.json"

if [ ! -f "$PAYLOAD" ]; then
  echo "LEAF008_PAYLOAD_MISSING file=$PAYLOAD" >&2
  exit 1
fi

echo "[0] DECODING PAYLOAD"
base64 -d "$PAYLOAD" > "$OUT"

ACTUAL_SHA="$(sha256sum "$OUT" | awk '{print $1}')"
ACTUAL_SIZE="$(wc -c < "$OUT" | tr -d ' ')"

echo "LEAF008_PAYLOAD_DECODED file=$OUT sha=$ACTUAL_SHA bytes=$ACTUAL_SIZE"

echo "[1] VALIDATING JSON"
if jq . "$OUT" > /dev/null 2>&1; then
  echo "LEAF008_JSON_VALID"
  jq . "$OUT" | head -n 20
else
  echo "LEAF008_JSON_INVALID" >&2
  exit 1
fi

echo "[2] EXTENDING MERKLE CHAIN"
# Using the existing merkle_chain.sh logic if applicable
if [ -f "$HOME/jay-agent/_truth/emotional/merkle_chain.sh" ]; then
    bash "$HOME/jay-agent/_truth/emotional/merkle_chain.sh"
fi

echo "LEAF008_PROCESS_COMPLETE"
