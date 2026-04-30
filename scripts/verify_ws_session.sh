#!/usr/bin/env bash
# ALMS WebSocket Session Verifier v0.2
# Replays canonical JSON frame hash chains and validates integrity.

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: scripts/verify_ws_session.sh <path_to_session.json>" >&2
  exit 1
fi

FILE="$1"
if [[ ! -f "$FILE" ]]; then
  echo "Error: File not found" >&2
  exit 1
fi

schema="$(jq -r '.schema // empty' "$FILE")"
if [[ "$schema" != "alms.ws_session_receipt.v0.2" ]]; then
  printf '{"valid": false, "replay_match": false, "reason": "unsupported_schema", "schema": "%s"}\n' "$schema"
  exit 1
fi

COUNT="$(jq '.entries | length' "$FILE")"
prev_hash="0x0"
valid=true
reason=""

for ((i=0;i<COUNT;i++)); do
  canonical_frame="$(jq -r ".entries[$i].canonical_frame" "$FILE")"
  reported_entry_hash="$(jq -r ".entries[$i].entry_hash" "$FILE")"
  reported_prev_hash="$(jq -r ".entries[$i].prev_hash" "$FILE")"
  reported_canonical_frame_hash="$(jq -r ".entries[$i].canonical_frame_hash" "$FILE")"
  seq="$(jq -r ".entries[$i].seq" "$FILE")"

  expected_seq=$((i + 1))
  if [[ "$seq" != "$expected_seq" ]]; then
    valid=false; reason="bad_seq"; break
  fi

  recanonical_frame="$(printf '%s' "$canonical_frame" | jq -cS .)"
  calc_canonical_frame_hash="$(printf '%s' "$recanonical_frame" | sha256sum | awk '{print $1}')"
  calc_entry_hash="$(printf '%s' "${prev_hash}${recanonical_frame}" | sha256sum | awk '{print $1}')"

  if [[ "$canonical_frame" != "$recanonical_frame" ]]; then
    valid=false; reason="noncanonical_frame"; break
  fi
  if [[ "$reported_prev_hash" != "$prev_hash" ]]; then
    valid=false; reason="prev_hash_mismatch"; break
  fi
  if [[ "$reported_canonical_frame_hash" != "$calc_canonical_frame_hash" ]]; then
    valid=false; reason="canonical_frame_hash_mismatch"; break
  fi
  if [[ "$reported_entry_hash" != "$calc_entry_hash" ]]; then
    valid=false; reason="entry_hash_mismatch"; break
  fi

  prev_hash="$calc_entry_hash"
done

final_state_hash="$(jq -r '.final_state_hash' "$FILE")"
if [[ "$prev_hash" != "$final_state_hash" ]]; then
  valid=false
  reason="final_state_hash_mismatch"
fi

if [[ "$valid" == true ]]; then
  printf '{"valid": true, "replay_match": true, "deltas_processed": %s, "final_state_hash": "%s"}\n' "$COUNT" "$final_state_hash"
else
  printf '{"valid": false, "replay_match": false, "deltas_processed": %s, "reason": "%s"}\n' "$COUNT" "$reason"
  exit 1
fi
