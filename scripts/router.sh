#!/usr/bin/env bash
set -euo pipefail

CLAIM_ID="${1:-}"
RECEIPTS_DIR="${RECEIPTS_DIR:-receipts}"
OUT_DIR="${OUT_DIR:-_truth/routing}"
LEDGER="$OUT_DIR/leaderboard.json"
HISTORY="$OUT_DIR/history.jsonl"
DECAY_LAMBDA="${DECAY_LAMBDA:-0.1}"
REPUTATION_ALPHA="${REPUTATION_ALPHA:-0.25}"
NOW_EPOCH="${NOW_EPOCH:-$(date -u +%s)}"

if [ -z "$CLAIM_ID" ]; then
  echo "ROUTER_FAIL reason=missing_claim_id" >&2
  echo "usage: scripts/router.sh CLAIM_ID" >&2
  exit 2
fi

command -v jq >/dev/null 2>&1 || { echo "ROUTER_FAIL reason=missing_jq" >&2; exit 2; }
command -v sha256sum >/dev/null 2>&1 || { echo "ROUTER_FAIL reason=missing_sha256sum" >&2; exit 2; }

mkdir -p "$OUT_DIR"
TMP="$(mktemp)"
DECISION_TMP="$(mktemp)"
trap 'rm -f "$TMP" "$DECISION_TMP"' EXIT

jq -s \
  --argjson now "$NOW_EPOCH" \
  --argjson lambda "$DECAY_LAMBDA" \
  --argjson repalpha "$REPUTATION_ALPHA" \
  '
  def ts_to_epoch:
    if . == null then $now else (try (fromdateiso8601) catch $now) end;

  map(select(.schema == "agent_income_receipt_v1"))
  | map(select(.payment.paid == true))
  | map(select(.agent_id != null and .routing.weight != null))
  | map(. + {
      receipt_epoch: ((.timestamp // .created_at // .date // null) | ts_to_epoch),
      age_days: ((($now - ((.timestamp // .created_at // .date // null) | ts_to_epoch)) / 86400) | if . < 0 then 0 else . end)
    })
  | map(. + {
      decay_factor: ((-.age_days * $lambda) | exp),
      decayed_routing_weight: (.routing.weight * ((-.age_days * $lambda) | exp))
    })
  | group_by(.agent_id)
  | map(. as $g
      | (($g | map(.accuracy.score) | add) / length) as $avg_acc
      | (($g | map((.accuracy.score - $avg_acc) | if . < 0 then -. else . end) | add) / length) as $mad
      | (1 - $mad) as $consistency
      | (($g | map(.decayed_routing_weight) | add) / length) as $decayed_weight
      | (1 + ($repalpha * $avg_acc * $consistency)) as $rep_mult
      | {
          agent_id: $g[0].agent_id,
          receipts: length,
          latest_receipt_id: ($g | sort_by(.receipt_id)[-1].receipt_id),
          avg_accuracy: $avg_acc,
          consistency: $consistency,
          accuracy_mad: $mad,
          avg_cost_usd: (($g | map(.payment.cost_usd | tonumber) | add) / length),
          raw_routing_weight: (($g | map(.routing.weight) | add) / length),
          decayed_routing_weight: $decayed_weight,
          reputation_multiplier: $rep_mult,
          routing_weight: ($decayed_weight * $rep_mult),
          avg_decay_factor: (($g | map(.decay_factor) | add) / length),
          decay_lambda: $lambda,
          reputation_alpha: $repalpha
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
HASH_INPUT="agent_router_v1|time_decay|lambda=$DECAY_LAMBDA|reputation_alpha=$REPUTATION_ALPHA|$CLAIM_ID|$WINNER|$WEIGHT|$TS"
HASH="$(printf '%s' "$HASH_INPUT" | sha256sum | awk '{print $1}')"

jq -n \
  --arg schema "agent_routing_decision_v1" \
  --arg decision_id "$DECISION_ID" \
  --arg claim_id "$CLAIM_ID" \
  --arg selected_agent "$WINNER" \
  --argjson routing_weight "$WEIGHT" \
  --arg timestamp "$TS" \
  --arg decay_lambda "$DECAY_LAMBDA" \
  --arg reputation_alpha "$REPUTATION_ALPHA" \
  --arg hash_input "$HASH_INPUT" \
  --arg hash "$HASH" \
  --slurpfile leaderboard "$TMP" \
  '{schema:$schema, decision_id:$decision_id, claim_id:$claim_id, selected_agent:$selected_agent, routing_weight:$routing_weight, timestamp:$timestamp, decay:{type:"exponential", lambda_per_day:($decay_lambda|tonumber)}, reputation:{type:"avg_accuracy_times_consistency", alpha:($reputation_alpha|tonumber)}, leaderboard:$leaderboard[0], hash_input:$hash_input, hash:$hash}' > "$DECISION_TMP"

cp "$DECISION_TMP" "$OUT_DIR/${DECISION_ID}.json"
cp "$TMP" "$LEDGER"
jq -c '{timestamp, claim_id, selected_agent, routing_weight, leaderboard}' "$DECISION_TMP" >> "$HISTORY"

echo "ROUTER_OK claim=$CLAIM_ID selected_agent=$WINNER weight=$WEIGHT decay_lambda=$DECAY_LAMBDA reputation_alpha=$REPUTATION_ALPHA hash=$HASH"
