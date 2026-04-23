#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_LOG="${ROOT}/_truth/run_log.jsonl"

if [[ ! -f "$RUN_LOG" ]]; then
  echo "run log not found: $RUN_LOG" >&2
  exit 1
fi

if [[ ! -s "$RUN_LOG" ]]; then
  echo "run log is empty: $RUN_LOG"
  exit 0
fi

jq -c '.' "$RUN_LOG" | while read -r line; do
  ts="$(jq -r '.ts // ""' <<<"$line")"
  source_id="$(jq -r '.source_id // ""' <<<"$line")"
  status="$(jq -r '.status // ""' <<<"$line")"
  event="$(jq -r '.event // ""' <<<"$line")"
  reason="$(jq -r '.reason // ""' <<<"$line")"
  watcher_path="$(jq -r '.watcher_path // ""' <<<"$line")"
  output_b64="$(jq -r '.output_b64 // ""' <<<"$line")"

  decoded=""
  if [[ -n "$output_b64" ]]; then
    decoded="$(printf '%s' "$output_b64" | base64 --decode 2>/dev/null || true)"
  fi

  printf '%s | %s | %s' "$ts" "$source_id" "$status"

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
done
