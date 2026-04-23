#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_LOG="${1:-${ROOT}/_truth/run_log.jsonl}"

if [[ ! -f "$RUN_LOG" ]]; then
  echo "run log not found: $RUN_LOG" >&2
  exit 1
fi

if [[ ! -s "$RUN_LOG" ]]; then
  echo "run log is empty: $RUN_LOG"
  exit 0
fi

declare -A COUNTS=(
  [NO_CHANGE]=0
  [CHANGE_DETECTED]=0
  [FAIL]=0
  [OTHER]=0
)

line_no=0
while IFS= read -r line; do
  line_no=$((line_no + 1))

  parsed="$(jq -cr '{
    ts: (.ts // ""),
    source_id: (.source_id // ""),
    status: (.status // ""),
    event: (.event // ""),
    reason: (.reason // ""),
    watcher_path: (.watcher_path // ""),
    output_b64: (.output_b64 // "")
  }' <<<"$line" 2>/dev/null || true)"

  if [[ -z "$parsed" ]]; then
    COUNTS[OTHER]=$((COUNTS[OTHER] + 1))
    printf 'line=%d | INVALID_JSON | raw=%s\n' "$line_no" "$line"
    continue
  fi

  ts="$(jq -r '.ts' <<<"$parsed")"
  source_id="$(jq -r '.source_id' <<<"$parsed")"
  status="$(jq -r '.status' <<<"$parsed")"
  event="$(jq -r '.event' <<<"$parsed")"
  reason="$(jq -r '.reason' <<<"$parsed")"
  watcher_path="$(jq -r '.watcher_path' <<<"$parsed")"
  output_b64="$(jq -r '.output_b64' <<<"$parsed")"

  decoded=""
  if [[ -n "$output_b64" ]]; then
    decoded="$(printf '%s' "$output_b64" | base64 --decode 2>/dev/null || true)"
  fi

  outcome="OTHER"
  if [[ "$status" == "FAIL" ]]; then
    outcome="FAIL"
  elif [[ "$event" == "NO_CHANGE" ]]; then
    outcome="NO_CHANGE"
  elif [[ "$event" == "CHANGE_DETECTED" ]]; then
    outcome="CHANGE_DETECTED"
  fi
  COUNTS[$outcome]=$((COUNTS[$outcome] + 1))

  printf '%s | %s | status=%s | outcome=%s' "$ts" "$source_id" "$status" "$outcome"

  if [[ -n "$event" ]]; then
    printf ' | event=%s' "$event"
  fi

  if [[ -n "$reason" ]]; then
    printf ' | reason=%s' "$reason"
  fi

  if [[ -n "$watcher_path" ]]; then
    printf ' | watcher_path=%s' "$watcher_path"
  fi

  if [[ -n "$decoded" ]]; then
    compact_decoded="$(printf '%s' "$decoded" | tr '\n' ' ' | sed 's/[[:space:]]\+/ /g; s/^ //; s/ $//')"
    printf ' | decoded=%s' "$compact_decoded"
  fi

  printf '\n'
done < "$RUN_LOG"

printf '\nSummary: NO_CHANGE=%d CHANGE_DETECTED=%d FAIL=%d OTHER=%d\n' \
  "${COUNTS[NO_CHANGE]}" "${COUNTS[CHANGE_DETECTED]}" "${COUNTS[FAIL]}" "${COUNTS[OTHER]}"
