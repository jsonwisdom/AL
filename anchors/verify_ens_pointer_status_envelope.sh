#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

ENV_FILE="anchors/ens_pointer_status_envelope.json"

need() { command -v "$1" >/dev/null 2>&1 || { echo "MISSING_BIN $1"; exit 1; }; }
need jq
need sha256sum

[ -f "$ENV_FILE" ] || { echo "ENV_MISSING $ENV_FILE"; exit 1; }

PAYLOAD_PATH="$(jq -r '.payload' "$ENV_FILE")"
PAYLOAD_HASH_EXPECTED="$(jq -r '.payload_sha256' "$ENV_FILE")"

[ -n "$PAYLOAD_PATH" ] || { echo "STATUS_ENV_INVALID missing=payload"; exit 1; }
[ -n "$PAYLOAD_HASH_EXPECTED" ] || { echo "STATUS_ENV_INVALID missing=payload_sha256"; exit 1; }
[ -f "$PAYLOAD_PATH" ] || { echo "PAYLOAD_MISSING $PAYLOAD_PATH"; exit 1; }

PAYLOAD_HASH_LOCAL="$(jq -cS . "$PAYLOAD_PATH" | sha256sum | awk '{print $1}')"

[ "$PAYLOAD_HASH_LOCAL" = "$PAYLOAD_HASH_EXPECTED" ] || {
  echo "STATUS_ENV_INVALID payload_hash_mismatch expected=$PAYLOAD_HASH_EXPECTED got=$PAYLOAD_HASH_LOCAL"
  exit 1
}

echo "STATUS_ENV_HASH_OK payload=$PAYLOAD_PATH hash=$PAYLOAD_HASH_LOCAL"
