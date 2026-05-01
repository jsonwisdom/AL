#!/usr/bin/env bash
set -euo pipefail

EXPECTED_SHA="21829f0be11cd04a64f379ad90003fc39338d91b2242720cd6c0497aed067d8b"
EXPECTED_SIZE="10240"
PAYLOAD="payload.b64"
OUT="verify_leaf006.tar"

if [ ! -f "$PAYLOAD" ]; then
  echo "LEAF006_PAYLOAD_MISSING file=$PAYLOAD" >&2
  exit 1
fi

base64 -d "$PAYLOAD" > "$OUT"

ACTUAL_SHA="$(sha256sum "$OUT" | awk '{print $1}')"
ACTUAL_SIZE="$(wc -c < "$OUT" | tr -d ' ')"

if [ "$ACTUAL_SHA" = "$EXPECTED_SHA" ] && [ "$ACTUAL_SIZE" = "$EXPECTED_SIZE" ]; then
  echo "LEAF006_PAYLOAD_VERIFIED sha=$ACTUAL_SHA bytes=$ACTUAL_SIZE"
else
  echo "LEAF006_PAYLOAD_MISMATCH sha=$ACTUAL_SHA bytes=$ACTUAL_SIZE expected_sha=$EXPECTED_SHA expected_bytes=$EXPECTED_SIZE" >&2
  exit 1
fi
