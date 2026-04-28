#!/usr/bin/env bash
set -euo pipefail

CLAIM_ID="${1:-}"
RECEIPTS_DIR="${RECEIPTS_DIR:-receipts}"
OUT_DIR="${OUT_DIR:-_truth/routing}"
LEDGER="$OUT_DIR/leaderboard.json"

if [ -z "$CLAIM_ID" ]; then
  echo "ROUTER_FAIL reason=missing_claim_id" >&2
  echo "usage: scripts/router.sh CLAIM_ID" >&2
  exit 2
fi

command -v jq >/dev/null 2>&1 || { echo "ROUTER_FAIL reason=missing_jq" >&2; exit 2; }
command -v sha256sum >/dev/null 2>&1 || { echo "ROUTER_FAIL reason=missing_sha256sum" >&2; exit 2; }

mkdir -p "$OUT_DIR"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

# Build candidate set from agent income receipts only.
# Valid candidates must be paid, have an agent_id, and expose routing.weight.
jq -s '
  map(select(.schema == "agent_income_receipt_v1"))
  | map(select(.payment.paid == true))
  | map(select(.agent_id != null and .routing.weight != null))
  | group_by(.agent_id)
  | map({
      agent_id: .[0].agent_id,
      receipts: length,
      latest_receipt_id: (sort_by(.receipt_id)[-1].receipt_id),
      avg_accuracy: ((map(.accuracy.score) | add) / length),
      avg_cost_usd: ((map(.payment.cost_usd | tonumber) | add) / length),
      routing_weight: ((map(.routing.weight) | add) / length)
    })
  | sort_by(.routing_weight, (0 - .avg_cost_usd), .receipts)
  | reverse
' "$RECEIPTS_DIR"/*.json 2>/dev/null > "$TMP" || echo '[]' > "$TMP"

if [ ! -s "$TMP" ] || [ "$(jq 'length' "$TMP")" = "0" ]; then
  WINNER="fallback"
  WEIGHT="0"
else
  WINNER="$(jq -r '.[0].agent_id' "$TMP")"
  WEIGHT="$(jq -r '.[0].routing_weight' "$TMP")"
fi

TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
DECISION_ID="route_${CLAIM_ID}_${TS}"
HASH_INPUT="agent_router_v1|$CLAIM_ID|$WINNER|$WEIGHT|$TS"
HASH="$(printf '%s' "$HASH_INPUT" | sha256sum | awk '{print $1}')"

jq -n \
  --arg schema "agent_routing_decision_v1" \
  --arg decision_id "$DECISION_ID" \
  --arg claim_id "$CLAIM_ID" \
  --arg selected_agent "$WINNER" \
  --argjson routing_weight "$WEIGHT" \
  --arg timestamp "$TS" \
  --arg hash_input "$HASH_INPUT" \
  --arg hash "$HASH" \
  --slurpfile leaderboard "$TMP" \
  '{schema:$schema, decision_id:$decision_id, claim_id:$claim_id, selected_agent:$selected_agent, routing_weight:$routing_weight, timestamp:$timestamp, leaderboard:$leaderboard[0], hash_input:$hash_input, hash:$hash}' \
  | tee "$OUT_DIR/${DECISION_ID}.json" >/dev/null

cp "$TMP" "$LEDGER"
echo "ROUTER_OK claim=$CLAIM_ID selected_agent=$WINNER weight=$WEIGHT hash=$HASH"
