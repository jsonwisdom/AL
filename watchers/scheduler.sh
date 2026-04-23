#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGETS_FILE="${ROOT}/watchers/targets.json"
RUN_LOG="${ROOT}/_truth/run_log.jsonl"

cd "$ROOT"

jq -c '.targets[] | select(.enabled == true)' "$TARGETS_FILE" | while read -r target; do
  SOURCE_ID="$(printf "%s" "$target" | jq -r '.source_id')"
  WATCHER_PATH="$(printf "%s" "$target" | jq -r '.watcher_path')"
  STARTED_AT="$(date -u +%FT%TZ)"

  if [[ ! -x "$WATCHER_PATH" ]]; then
    printf '{"ts":"%s","source_id":"%s","status":"FAIL","reason":"watcher_not_executable","watcher_path":"%s"}\n' \
      "$STARTED_AT" "$SOURCE_ID" "$WATCHER_PATH" >> "$RUN_LOG"
    continue
  fi

  OUTPUT="$("$WATCHER_PATH" 2>&1)" || {
    printf '{"ts":"%s","source_id":"%s","status":"FAIL","output_b64":"%s"}\n' \
      "$STARTED_AT" "$SOURCE_ID" "$(printf "%s" "$OUTPUT" | base64 | tr -d '\n')" >> "$RUN_LOG"
    continue
  }

  EVENT="$(printf "%s" "$OUTPUT" | jq -r '.event // "UNKNOWN"' 2>/dev/null || echo "UNKNOWN")"

  printf '{"ts":"%s","source_id":"%s","status":"OK","event":"%s","output_b64":"%s"}\n' \
    "$STARTED_AT" "$SOURCE_ID" "$EVENT" "$(printf "%s" "$OUTPUT" | base64 | tr -d '\n')" >> "$RUN_LOG"
done
