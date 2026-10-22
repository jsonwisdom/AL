#!/usr/bin/env bash
# ZTVS evidence card — contained repair v0.1
# Never emits VERIFIED. Missing or incomplete evidence => HOLD.
set -euo pipefail

TARGET_ID="MN_001"
STATE_IN="HOLD"
COMMIT_SHA=""
RECEIPT_HASH=""
OUT_DIR="registry/MN_001"

while [ $# -gt 0 ]; do
  case "$1" in
    --target_id) TARGET_ID="$2"; shift 2 ;;
    --state) STATE_IN="$2"; shift 2 ;;
    --commit) COMMIT_SHA="$2"; shift 2 ;;
    --receipt_hash) RECEIPT_HASH="$2"; shift 2 ;;
    *) shift ;;
  esac
done

mkdir -p "$OUT_DIR"
CARD="$OUT_DIR/evidence_card.json"

# Force HOLD. The original workflow's git-diff-quiet VERIFIED path is not accepted here.
jq -n \
  --arg target "$TARGET_ID" \
  --arg requested_state "$STATE_IN" \
  --arg commit "$COMMIT_SHA" \
  --arg receipt_hash "$RECEIPT_HASH" \
  --arg utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  '{artifact:"ztvs_evidence_card",target_id:$target,requested_state:$requested_state,status:"HOLD",commit:$commit,receipt_hash:$receipt_hash,utc:$utc,verified:false,no_fake_green:true,reason:"PROOF_NOT_ESTABLISHED",note:"Contained repair does not promote to VERIFIED."}' \
  > "$CARD"

echo "HOLD: PROOF_NOT_ESTABLISHED"
echo "Card: $CARD"
exit 2
