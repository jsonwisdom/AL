#!/usr/bin/env bash
# ZTVS evidence card — contained repair v0.1
# Never emits VERIFIED. Missing or incomplete evidence => HOLD.
# Distinguishes source_head_sha from executed_checkout_sha.
set -euo pipefail

TARGET_ID="MN_001"
STATE_IN="HOLD"
COMMIT_SHA=""
SOURCE_HEAD_SHA=""
EXECUTED_CHECKOUT_SHA=""
RUN_ID=""
JOB_ID=""
RECEIPT_HASH=""
OUT_DIR="registry/MN_001"

while [ $# -gt 0 ]; do
  case "$1" in
    --target_id) TARGET_ID="$2"; shift 2 ;;
    --state) STATE_IN="$2"; shift 2 ;;
    --commit) COMMIT_SHA="$2"; shift 2 ;;
    --source_head_sha) SOURCE_HEAD_SHA="$2"; shift 2 ;;
    --executed_checkout_sha) EXECUTED_CHECKOUT_SHA="$2"; shift 2 ;;
    --run_id) RUN_ID="$2"; shift 2 ;;
    --job_id) JOB_ID="$2"; shift 2 ;;
    --receipt_hash) RECEIPT_HASH="$2"; shift 2 ;;
    *) shift ;;
  esac
done

# Backward compatible: if only --commit is supplied, treat it as the executed checkout.
if [ -z "$EXECUTED_CHECKOUT_SHA" ] && [ -n "$COMMIT_SHA" ]; then
  EXECUTED_CHECKOUT_SHA="$COMMIT_SHA"
fi

mkdir -p "$OUT_DIR"
CARD="$OUT_DIR/evidence_card.json"

# Force HOLD. The original workflow's git-diff-quiet VERIFIED path is not accepted here.
jq -n \
  --arg target "$TARGET_ID" \
  --arg requested_state "$STATE_IN" \
  --arg commit "$COMMIT_SHA" \
  --arg source_head_sha "$SOURCE_HEAD_SHA" \
  --arg executed_checkout_sha "$EXECUTED_CHECKOUT_SHA" \
  --arg run_id "$RUN_ID" \
  --arg job_id "$JOB_ID" \
  --arg receipt_hash "$RECEIPT_HASH" \
  --arg utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  '{artifact:"ztvs_evidence_card",target_id:$target,requested_state:$requested_state,status:"HOLD",commit:$commit,source_head_sha:$source_head_sha,executed_checkout_sha:$executed_checkout_sha,run_id:$run_id,job_id:$job_id,receipt_hash:$receipt_hash,utc:$utc,verified:false,no_fake_green:true,reason:"PROOF_NOT_ESTABLISHED",note:"Contained repair does not promote to VERIFIED. source_head_sha is the PR head; executed_checkout_sha is the commit that was checked out."}' \
  > "$CARD"

echo "HOLD: PROOF_NOT_ESTABLISHED"
echo "Card: $CARD"
exit 2
