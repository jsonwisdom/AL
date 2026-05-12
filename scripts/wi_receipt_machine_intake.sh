#!/usr/bin/env bash
set -euo pipefail

EVENT="WI_BUDGET_NEGOTIATION_2026"
IN="incoming/wi_budget_negotiation_2026"
OUT="receipts/wi_budget_negotiation_2026"
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

mkdir -p "$IN" "$OUT"

COUNT="$(find "$IN" -maxdepth 1 -type f \( -name '*.pdf' -o -name '*.PDF' \) | wc -l | tr -d ' ')"

if [ "$COUNT" = "0" ]; then
  cat > "$OUT/state.json" <<JSON
{
  "event": "$EVENT",
  "state": "AWAITING_PRIMARY_ARTIFACT_UPLOAD",
  "posture": "SEALED_PASSIVE_WITNESS",
  "transition_allowed": false,
  "reason": "no operator-provided canonical pdf bytes found",
  "timestamp_utc": "$TS"
}
JSON
  cat "$OUT/state.json"
  exit 0
fi

MANIFEST="$OUT/artifact_manifest.jsonl"
: > "$MANIFEST"

find "$IN" -maxdepth 1 -type f \( -name '*.pdf' -o -name '*.PDF' \) -print0 \
| sort -z \
| while IFS= read -r -d '' f; do
  NAME="$(basename "$f")"
  SIZE="$(wc -c < "$f" | tr -d ' ')"
  SHA256="$(sha256sum "$f" | awk '{print $1}')"

  jq -cn \
    --arg event "$EVENT" \
    --arg file "$NAME" \
    --arg path "$f" \
    --arg sha256 "$SHA256" \
    --arg size "$SIZE" \
    --arg role "unknown" \
    --arg timestamp_utc "$TS" \
    '{
      event:$event,
      artifact_file:$file,
      artifact_path:$path,
      artifact_sha256:$sha256,
      artifact_size_bytes:($size|tonumber),
      artifact_role:$role,
      source:"operator_provided_local_bytes",
      canonical_status:"PRIMARY_BYTES_RECEIVED_UNCLASSIFIED",
      timestamp_utc:$timestamp_utc
    }' >> "$MANIFEST"
done

jq -s --arg event "$EVENT" --arg ts "$TS" '{
  event:$event,
  state:"ARTIFACT_BYTES_RECEIVED",
  posture:"SEALED_PASSIVE_WITNESS",
  transition_allowed:true,
  hash_ready:true,
  anchor_ready:false,
  semantic_expansion:"DISABLED",
  artifacts:.
}' "$MANIFEST" > "$OUT/state.json"

jq -cS '.receipt_hash=null' "$OUT/state.json" > "$OUT/state.canonical.json"
HASH="$(sha256sum "$OUT/state.canonical.json" | awk '{print $1}')"
jq --arg h "$HASH" '. + {receipt_hash:$h}' "$OUT/state.json" > "$OUT/state.receipt.json"

echo "RECEIPT_MACHINE_OK"
echo "receipt=$OUT/state.receipt.json"
echo "receipt_hash=$HASH"
