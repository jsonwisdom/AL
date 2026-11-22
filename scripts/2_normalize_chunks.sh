#!/usr/bin/env bash
# ZTVS normalize & chunk stage — contained repair v0.1
# Missing raw.pdf => HOLD. Does not invent chunks. Does not set VERIFIED.
set -euo pipefail

RAW="${1:-}"
OUT_DIR="${2:-registry/MN_001}"
CHUNKS="$OUT_DIR/chunks"
RECEIPT="$OUT_DIR/normalize_receipt.json"

mkdir -p "$OUT_DIR" "$CHUNKS"

write_hold() {
  local reason="$1"
  jq -n --arg reason "$reason" --arg utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    '{stage:"normalize",status:"HOLD",reason:$reason,utc:$utc,verified:false,no_fake_green:true}' \
    > "$RECEIPT"
  echo "HOLD: $reason"
  exit 2
}

if [ -z "$RAW" ] || [ ! -f "$RAW" ]; then
  write_hold "MISSING_RAW_PDF"
fi

# Presence of file is not authenticity. Record hash only.
HASH=$(sha256sum "$RAW" | awk '{print $1}')
jq -n --arg utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg hash "$HASH" --arg raw "$RAW" \
  '{stage:"normalize",status:"HOLD",reason:"NORMALIZE_NOT_IMPLEMENTED",raw:$raw,raw_sha256:$hash,utc:$utc,verified:false,no_fake_green:true,note:"file present; chunking contract not yet implemented; do not treat as VERIFIED"}' \
  > "$RECEIPT"
echo "HOLD: NORMALIZE_NOT_IMPLEMENTED (file present, no fake chunks)"
echo "Receipt: $RECEIPT"
exit 2
