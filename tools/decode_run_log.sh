#!/usr/bin/env bash
set -euo pipefail

RUN_LOG="${1:-_truth/run_log.jsonl}"

if [[ ! -f "$RUN_LOG" ]]; then
  echo "Usage: decode_run_log.sh [_truth/run_log.jsonl]" >&2
  exit 1
fi

echo "=== ALMS RUN LOG DECODER ==="
echo ""

while IFS= read -r line; do
  TS="$(printf '%s' "$line" | jq -r '.ts')"
  SOURCE="$(printf '%s' "$line" | jq -r '.source_id')"
  STATUS="$(printf '%s' "$line" | jq -r '.status')"
  EVENT="$(printf '%s' "$line" | jq -r '.event // ""')"
  B64="$(printf '%s' "$line" | jq -r '.output_b64 // ""')"

  printf "[%s] %s | %s | %s\n" "$TS" "$SOURCE" "$STATUS" "$EVENT"

  if [[ -n "$B64" && "$B64" != "null" ]]; then
    DECODED_JSON="$(printf '%s' "$B64" | base64 -d 2>/dev/null || true)"
    if [[ -n "$DECODED_JSON" ]]; then
      printf "  DECODED: %s\n" "$DECODED_JSON"
    fi
  fi

  if [[ "$STATUS" == "FAIL" ]]; then
    REASON="$(printf '%s' "$line" | jq -r '.reason // "unknown"')"
    printf "  REASON: %s\n" "$REASON"
  fi

  VERIFIED="$(printf '%s' "$line" | jq -r '.verified_hash // ""' 2>/dev/null || true)"
  if [[ -n "$VERIFIED" && "$VERIFIED" != "null" ]]; then
    printf "  VERIFIED: %s\n" "$VERIFIED"
  fi

  echo ""
done < "$RUN_LOG"

echo "=== END ==="
