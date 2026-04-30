#!/usr/bin/env bash
# ALMS WebSocket Session Receipt Captor v0.2
# Captures ordered JSON frames into a deterministic canonical SHA-256 hash chain.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SESSION_DIR="$ROOT_DIR/_truth/websocket_sessions"
mkdir -p "$SESSION_DIR"

usage() {
  cat <<'USAGE'
Usage:
  scripts/ws_session_receipt.sh <session_name> <json_frame1> [json_frame2 ...]
  printf '%s\n' '{"b":2,"a":1}' '{"type":"done"}' | scripts/ws_session_receipt.sh <session_name> --stdin

Output:
  Writes _truth/websocket_sessions/<session_name>.json and prints its path.

Rules:
  - No randomness.
  - No private keys.
  - No RPC.
  - Every payload must be valid JSON.
  - canonical_frame = jq -cS .
  - frame_hash = sha256(canonical_frame)
  - entry_hash = sha256(prev_hash + canonical_frame)
  - Hash chain starts from prev_hash = 0x0.
USAGE
}

sha256_text() {
  printf '%s' "$1" | sha256sum | awk '{print $1}'
}

canonicalize_frame() {
  printf '%s' "$1" | jq -cS .
}

if [[ $# -lt 2 ]]; then
  usage >&2
  exit 1
fi

SESSION_NAME="$1"
shift

if [[ ! "$SESSION_NAME" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "ALMS_WS_RECEIPT_INVALID reason=bad_session_name" >&2
  exit 1
fi

OUT_FILE="$SESSION_DIR/${SESSION_NAME}.json"
TMP_FILE="${OUT_FILE}.tmp"

frames=()
if [[ "${1:-}" == "--stdin" ]]; then
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    frames+=("$line")
  done
else
  frames=("$@")
fi

if [[ ${#frames[@]} -eq 0 ]]; then
  echo "ALMS_WS_RECEIPT_INVALID reason=no_frames" >&2
  exit 1
fi

prev_hash="0x0"
entries_json="[]"
seq_no=1

for raw_frame in "${frames[@]}"; do
  if ! canonical_frame="$(canonicalize_frame "$raw_frame")"; then
    echo "ALMS_WS_RECEIPT_INVALID reason=bad_json seq=$seq_no" >&2
    exit 1
  fi

  raw_frame_hash="$(sha256_text "$raw_frame")"
  canonical_frame_hash="$(sha256_text "$canonical_frame")"
  entry_hash="$(sha256_text "${prev_hash}${canonical_frame}")"

  entry="$(jq -cn \
    --argjson seq "$seq_no" \
    --arg type "canonical_json_frame" \
    --arg raw_frame_hash "$raw_frame_hash" \
    --arg canonical_frame "$canonical_frame" \
    --arg canonical_frame_hash "$canonical_frame_hash" \
    --arg prev_hash "$prev_hash" \
    --arg entry_hash "$entry_hash" \
    '{seq:$seq,type:$type,raw_frame_hash:$raw_frame_hash,canonical_frame:$canonical_frame,canonical_frame_hash:$canonical_frame_hash,prev_hash:$prev_hash,entry_hash:$entry_hash}')"

  entries_json="$(jq -cn --argjson entries "$entries_json" --argjson entry "$entry" '$entries + [$entry]')"
  prev_hash="$entry_hash"
  seq_no=$((seq_no + 1))
done

session_id="$(sha256_text "$SESSION_NAME")"
final_state_hash="$prev_hash"

jq -cn \
  --arg schema "alms.ws_session_receipt.v0.2" \
  --arg session_name "$SESSION_NAME" \
  --arg session_id "$session_id" \
  --arg initial_state_hash "0x0" \
  --arg canonicalization "jq -cS ." \
  --arg final_state_hash "$final_state_hash" \
  --argjson entries "$entries_json" \
  '{schema:$schema,session_name:$session_name,session_id:$session_id,initial_state_hash:$initial_state_hash,canonicalization:$canonicalization,entries:$entries,final_state_hash:$final_state_hash}' \
  > "$TMP_FILE"

mv "$TMP_FILE" "$OUT_FILE"
echo "$OUT_FILE"
