#!/usr/bin/env bash
set -euo pipefail

FILE="${1:?usage: ./scripts/wi_assign_role.sh <artifact_file> <role>}"
ROLE="${2:?usage: ./scripts/wi_assign_role.sh <artifact_file> <role>}"

OUT="receipts/wi_budget_negotiation_2026"
MANIFEST="$OUT/artifact_manifest.jsonl"
TMP="$OUT/artifact_manifest.tmp.jsonl"
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

case "$ROLE" in
  governor_press_release_pdf|special_session_order_pdf|lfb_fiscal_memo_pdf|enrolled_bill_text_pdf|unknown) ;;
  *) echo "INVALID_ROLE: $ROLE"; exit 1 ;;
esac

test -f "$MANIFEST" || { echo "MISSING_MANIFEST"; exit 1; }

jq -c --arg file "$FILE" --arg role "$ROLE" --arg ts "$TS" '
  if .artifact_file == $file then
    .artifact_role = $role
    | .role_assigned_by = "operator_manual"
    | .role_assigned_timestamp_utc = $ts
  else . end
' "$MANIFEST" > "$TMP"

mv "$TMP" "$MANIFEST"

jq -s --arg ts "$TS" '{
  event:"WI_BUDGET_NEGOTIATION_2026",
  state:"ARTIFACT_ROLE_ASSIGNED",
  posture:"SEALED_PASSIVE_WITNESS",
  transition_allowed:true,
  hash_ready:true,
  anchor_ready:false,
  semantic_expansion:"DISABLED",
  role_assignment:"operator_manual",
  artifacts:.
}' "$MANIFEST" > "$OUT/state.json"

jq -cS '.receipt_hash=null' "$OUT/state.json" > "$OUT/state.canonical.json"
HASH="$(sha256sum "$OUT/state.canonical.json" | awk '{print $1}')"
jq --arg h "$HASH" '. + {receipt_hash:$h}' "$OUT/state.json" > "$OUT/state.receipt.json"

echo "ROLE_ASSIGNMENT_OK"
echo "file=$FILE"
echo "role=$ROLE"
echo "receipt_hash=$HASH"
