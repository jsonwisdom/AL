#!/usr/bin/env bash
set -euo pipefail

HISTORY="${1:-_truth/routing/history.jsonl}"

command -v jq >/dev/null 2>&1 || { echo "DIAG_FAIL reason=missing_jq" >&2; exit 2; }

if [ ! -f "$HISTORY" ]; then
  echo "DIAG_FAIL reason=missing_history path=$HISTORY" >&2
  exit 2
fi

jq -s '
  def selected_row($d):
    (($d.leaderboard // []) | map(select(.agent_id == $d.selected_agent)) | .[0] // {});

  . as $rows
  | ($rows | length) as $rounds
  | ([$rows[]?.selected_agent] | reduce range(1; length) as $i (0; if . == null then 0 else . end)) as $unused
  | (reduce range(1; $rounds) as $i (0; if $rows[$i].selected_agent != $rows[$i-1].selected_agent then . + 1 else . end)) as $flips
  | ([ $rows[] | select(.selected_agent == "agent_beta") | selected_row(.) | .consistency // empty ]) as $beta_cons
  | ([ $rows[] | selected_row(.) | .routing_weight // empty ]) as $winner_weights
  | ([ $rows[] | .selected_agent ] | group_by(.) | map({agent: .[0], wins: length})) as $wins
  | {
      schema: "routing_history_diagnostic_v1",
      rounds: $rounds,
      flip_count: $flips,
      winners: $wins,
      beta_wins: ($beta_cons | length),
      beta_peak_consistency_on_wins: (if ($beta_cons|length)>0 then ($beta_cons|max) else null end),
      avg_winner_weight: (if ($winner_weights|length)>0 then (($winner_weights|add)/($winner_weights|length)) else null end),
      diagnosis:
        (if $flips <= 1 then "OVER_CONSTRAINED_OR_ALPHA_DOMINANT"
         elif $flips <= 7 then "HEALTHY_CONTESTABILITY"
         else "CHAOTIC_OR_UNDER_CONSTRAINED" end),
      tuning_hint:
        (if $flips <= 1 then "try DECAY_LAMBDA=0.12 or REPUTATION_ALPHA=0.15"
         elif $flips <= 7 then "ready_for_adaptive_agents_v1"
         else "raise REPUTATION_ALPHA or add stronger volatility penalty" end)
    }
' "$HISTORY"
