#!/usr/bin/env bash
set -euo pipefail

AGENT_ID="$1"
CURRENT_RANK="$2"
RECENT_DECAY_PRESSURE="$3"
REPUTATION_MULT="$4"

PROFILE="agents/${AGENT_ID}_profile.json"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

command -v jq >/dev/null 2>&1 || { echo "ADAPT_FAIL missing_jq" >&2; exit 2; }

ACC=$(jq -r '.accuracy_target' "$PROFILE")
COST=$(jq -r '.cost_target' "$PROFILE")

ADAPT_BUDGET=0.05

if [ "$CURRENT_RANK" -eq 1 ]; then
  NEW_ACC=$(awk "BEGIN {print ($ACC + ($ADAPT_BUDGET * 0.6))}")
  NEW_COST=$(awk "BEGIN {print ($COST + ($ADAPT_BUDGET * 0.3))}")
  STRAT="leader_precision"
else
  if (( $(awk "BEGIN {print ($RECENT_DECAY_PRESSURE < 0.7)}") )); then
    NEW_COST=$(awk "BEGIN {print ($COST - ($ADAPT_BUDGET * 0.7))}")
  else
    NEW_COST=$COST
  fi
  NEW_ACC=$(awk "BEGIN {print ($ACC + ($ADAPT_BUDGET * 0.4))}")
  STRAT="challenger_efficiency"
fi

# clamp
NEW_ACC=$(awk "BEGIN {if ($NEW_ACC>1) print 1; else if ($NEW_ACC<0.5) print 0.5; else print $NEW_ACC}")
NEW_COST=$(awk "BEGIN {if ($NEW_COST<0.001) print 0.001; else if ($NEW_COST>0.02) print 0.02; else print $NEW_COST}")

jq -n \
  --arg id "$AGENT_ID" \
  --argjson acc "$NEW_ACC" \
  --argjson cost "$NEW_COST" \
  --arg strat "$STRAT" \
  --arg reason "rank_${CURRENT_RANK}_decay_${RECENT_DECAY_PRESSURE}" \
  '{agent_id:$id, accuracy_target:$acc, cost_target:$cost, strategy:$strat, last_reason:$reason}' > "$TMP"

mv "$TMP" "$PROFILE"

echo "ADAPT_OK agent=$AGENT_ID acc=$NEW_ACC cost=$NEW_COST strat=$STRAT"
