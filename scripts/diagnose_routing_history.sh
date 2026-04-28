#!/usr/bin/env bash
set -euo pipefail

HISTORY="${1:-_truth/routing/history.jsonl}"
PROFILE_HISTORY="${PROFILE_HISTORY:-_truth/routing/profile_history.jsonl}"

command -v jq >/dev/null 2>&1 || { echo "DIAG_FAIL reason=missing_jq" >&2; exit 2; }

if [ ! -f "$HISTORY" ]; then
  echo "DIAG_FAIL reason=missing_history path=$HISTORY" >&2
  exit 2
fi

PROFILE_JSON='[]'
if [ -f "$PROFILE_HISTORY" ]; then
  PROFILE_JSON="$(jq -s '.' "$PROFILE_HISTORY")"
fi

jq -s --argjson profiles "$PROFILE_JSON" '
  def selected_row($d):
    (($d.leaderboard // []) | map(select(.agent_id == $d.selected_agent)) | .[0] // {});

  . as $rows
  | ($rows | length) as $rounds
  | (reduce range(1; $rounds) as $i (0; if $rows[$i].selected_agent != $rows[$i-1].selected_agent then . + 1 else . end)) as $flips
  | ([ $rows[] | select(.selected_agent == "agent_beta") | selected_row(.) | .consistency // empty ]) as $beta_cons
  | ([ $rows[] | selected_row(.) | .routing_weight // empty ]) as $winner_weights
  | ([ $rows[] | .selected_agent ] | group_by(.) | map({agent: .[0], wins: length})) as $wins
  | ($profiles | group_by(.strategy // "unknown") | map({strategy: .[0].strategy, count: length})) as $strategy_counts
  | ($profiles | group_by(.agent_id) | map({agent_id: .[0].agent_id, first: .[0], last: .[-1]})) as $profile_drift
  | {
      schema: "routing_history_diagnostic_v2",
      rounds: $rounds,
      flip_count: $flips,
      winners: $wins,
      beta_wins: ($beta_cons | length),
      beta_peak_consistency_on_wins: (if ($beta_cons|length)>0 then ($beta_cons|max) else null end),
      avg_winner_weight: (if ($winner_weights|length)>0 then (($winner_weights|add)/($winner_weights|length)) else null end),
      strategy_distribution: $strategy_counts,
      profile_drift: $profile_drift,
      diagnosis:
        (if $flips <= 1 then "OVER_CONSTRAINED_OR_ALPHA_DOMINANT"
         elif $flips <= 10 then "HEALTHY_CONTESTABILITY"
         else "CHAOTIC_OR_UNDER_CONSTRAINED" end),
      tuning_hint:
        (if $flips <= 1 then "increase evolutionary pressure or loosen thresholds"
         elif $flips <= 10 then "ready_for_observation_or_agent_gamma"
         else "tighten dampening or reputation penalty" end)
    }
' "$HISTORY"
