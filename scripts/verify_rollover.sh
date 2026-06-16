#!/usr/bin/env bash
set -euo pipefail

ROLLOVER="${1:-}"

fail() {
  echo "ALMS_ROLLOVER_INVALID: $1"
  exit 1
}

[ -n "$ROLLOVER" ] || fail "missing_rollover_file"
[ -f "$ROLLOVER" ] || fail "missing_rollover_file"

jq empty "$ROLLOVER" 2>/dev/null || fail "invalid_rollover_json"

# Top-level fields must be exactly from_segment and to_segment
TOP_KEYS="$(jq -r 'keys_unsorted | sort | join(",")' "$ROLLOVER")"
[ "$TOP_KEYS" = "from_segment,to_segment" ] || fail "unknown_fields"

jq -e 'has("from_segment")' "$ROLLOVER" >/dev/null || fail "missing_from_segment"
jq -e 'has("to_segment")' "$ROLLOVER" >/dev/null || fail "missing_to_segment"

# Nested fields must be exact
FROM_KEYS="$(jq -r '.from_segment | keys_unsorted | sort | join(",")' "$ROLLOVER")"
TO_KEYS="$(jq -r '.to_segment | keys_unsorted | sort | join(",")' "$ROLLOVER")"

[ "$FROM_KEYS" = "global_root,segment_id,state" ] || fail "unknown_fields"
[ "$TO_KEYS" = "next_gate,parent_global_root,segment_id,state" ] || fail "unknown_fields"

FROM_ID="$(jq -r '.from_segment.segment_id // empty' "$ROLLOVER")"
FROM_STATE="$(jq -r '.from_segment.state // empty' "$ROLLOVER")"
FROM_ROOT="$(jq -r '.from_segment.global_root // empty' "$ROLLOVER")"

TO_ID="$(jq -r '.to_segment.segment_id // empty' "$ROLLOVER")"
TO_STATE="$(jq -r '.to_segment.state // empty' "$ROLLOVER")"
TO_PARENT_ROOT="$(jq -r '.to_segment.parent_global_root // empty' "$ROLLOVER")"
TO_NEXT_GATE="$(jq -r '.to_segment.next_gate // empty' "$ROLLOVER")"

[ -n "$FROM_ID" ] || fail "missing_from_segment"
[ -n "$TO_ID" ] || fail "missing_to_segment"

[ "$FROM_STATE" = "SEGMENT_SEALED" ] || fail "invalid_from_segment_state"
[ "$TO_STATE" = "BOOTSTRAP_READY" ] || fail "invalid_to_segment_state"
[ "$TO_NEXT_GATE" = "OPEN_NEXT_LEAF" ] || fail "invalid_next_gate"

printf '%s' "$FROM_ROOT" | grep -Eq '^0x[0-9a-fA-F]{64}$' || fail "invalid_global_root_format"
printf '%s' "$TO_PARENT_ROOT" | grep -Eq '^0x[0-9a-fA-F]{64}$' || fail "invalid_parent_global_root_format"

[ "$FROM_ROOT" = "$TO_PARENT_ROOT" ] || fail "root_mismatch"

echo "ALMS_ROLLOVER_VALID"
echo "from: $FROM_ID"
echo "to:   $TO_ID"
echo "root: $FROM_ROOT"
exit 0
