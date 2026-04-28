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

# v2 damped mutation: max ~3% absolute move per adaptation.
MAX_STEP=0.03

# Strategy selection from real signals.
# attack: challenger with weak reputation attacks price and lifts accuracy.
# defend: leader under decay pressure protects quality.
# stabilize: any agent with low rep slows down and buys reliability.
if (( $(awk "BEGIN {print ($REPUTATION_MULT < 1.12)}") )); then
  STRAT="stabilize"
  NEW_ACC=$(awk "BEGIN {print $ACC + ($MAX_STEP * 0.8)}")
  NEW_COST=$(awk "BEGIN {print $COST + ($MAX_STEP * 0.5)}")
elif [ "$CURRENT_RANK" -gt 1 ]; then
  STRAT="attack"
  NEW_ACC=$(awk "BEGIN {print $ACC + ($MAX_STEP * 0.6)}")
  NEW_COST=$(awk "BEGIN {print $COST - ($MAX_STEP * 0.8)}")
elif (( $(awk "BEGIN {print ($RECENT_DECAY_PRESSURE < 0.85)}") )); then
  STRAT="defend"
  NEW_ACC=$(awk "BEGIN {print $ACC + ($MAX_STEP * 1.0)}")
  NEW_COST=$(awk "BEGIN {print $COST + ($MAX_STEP * 0.4)}")
else
  STRAT="hold"
  NEW_ACC="$ACC"
  NEW_COST="$COST"
fi

# clamp
NEW_ACC=$(awk "BEGIN {if ($NEW_ACC>1) print 1; else if ($NEW_ACC<0.5) print 0.5; else print $NEW_ACC}")
NEW_COST=$(awk "BEGIN {if ($NEW_COST<0.001) print 0.001; else if ($NEW_COST>0.02) print 0.02; else print $NEW_COST}")

jq -n \
  --arg id "$AGENT_ID" \
  --argjson acc "$NEW_ACC" \
  --argjson cost "$NEW_COST" \
  --arg strat "$STRAT" \
  --arg reason "v2_rank_${CURRENT_RANK}_decay_${RECENT_DECAY_PRESSURE}_rep_${REPUTATION_MULT}" \
  '{agent_id:$id, accuracy_target:$acc, cost_target:$cost, strategy:$strat, last_reason:$reason}' > "$TMP"

mv "$TMP" "$PROFILE"

echo "ADAPT_OK agent=$AGENT_ID acc=$NEW_ACC cost=$NEW_COST strat=$STRAT rep=$REPUTATION_MULT decay=$RECENT_DECAY_PRESSURE"
