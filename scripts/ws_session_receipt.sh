#!/usr/bin/env bash
# ALMS WebSocket Session Receipt Captor v0.3
# Captures ordered JSON or binary frames into a deterministic SHA-256 hash chain.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SESSION_DIR="$ROOT_DIR/_truth/websocket_sessions"
mkdir -p "$SESSION_DIR"

usage() {
  cat <<'USAGE'
Usage:
  JSON mode:
    scripts/ws_session_receipt.sh <session_name> --json <json_frame1> [json_frame2 ...]
    printf '%s\n' '{"b":2,"a":1}' | scripts/ws_session_receipt.sh <session_name> --json --stdin

  Binary mode:
    scripts/ws_session_receipt.sh <session_name> --binary <file1> [file2 ...]

Rules:
  - No randomness.
  - No private keys.
  - No RPC.
  - JSON canonical form = jq -cS .
  - Binary canonical form = raw bytes.
  - Binary payload is stored as base64 for JSON ledger compatibility.
  - entry_hash = sha256(prev_hash + canonical_hash_material)
  - Hash chain starts from prev_hash = 0x0.
USAGE
}

sha256_text() { printf '%s' "$1" | sha256sum | awk '{print $1}'; }
sha256_file() { sha256sum "$1" | awk '{print $1}'; }
canonicalize_json() { printf '%s' "$1" | jq -cS .; }
base64_file() { base64 -w 0 "$1" 2>/dev/null || base64 "$1" | tr -d '\n'; }

if [[ $# -lt 3 ]]; then usage >&2; exit 1; fi

SESSION_NAME="$1"; shift
MODE="$1"; shift

if [[ ! "$SESSION_NAME" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "ALMS_WS_RECEIPT_INVALID reason=bad_session_name" >&2; exit 1
fi

if [[ "$MODE" != "--json" && "$MODE" != "--binary" ]]; then
  echo "ALMS_WS_RECEIPT_INVALID reason=bad_mode" >&2; usage >&2; exit 1
fi

OUT_FILE="$SESSION_DIR/${SESSION_NAME}.json"
TMP_FILE="${OUT_FILE}.tmp"
prev_hash="0x0"
entries_json="[]"
seq_no=1

append_entry() {
  local entry="$1"
  entries_json="$(jq -cn --argjson entries "$entries_json" --argjson entry "$entry" '$entries + [$entry]')"
  seq_no=$((seq_no + 1))
}

if [[ "$MODE" == "--json" ]]; then
  frames=()
  if [[ "${1:-}" == "--stdin" ]]; then
    while IFS= read -r line; do [[ -z "$line" ]] && continue; frames+=("$line"); done
  else
    frames=("$@")
  fi
  [[ ${#frames[@]} -eq 0 ]] && { echo "ALMS_WS_RECEIPT_INVALID reason=no_frames" >&2; exit 1; }

  for raw_frame in "${frames[@]}"; do
    if ! canonical_frame="$(canonicalize_json "$raw_frame")"; then
      echo "ALMS_WS_RECEIPT_INVALID reason=bad_json seq=$seq_no" >&2; exit 1
    fi
    raw_frame_hash="$(sha256_text "$raw_frame")"
    canonical_frame_hash="$(sha256_text "$canonical_frame")"
    entry_hash="$(sha256_text "${prev_hash}${canonical_frame_hash}")"
    entry="$(jq -cn --argjson seq "$seq_no" --arg type "canonical_json_frame" --arg raw_frame_hash "$raw_frame_hash" --arg canonical_frame "$canonical_frame" --arg canonical_frame_hash "$canonical_frame_hash" --arg prev_hash "$prev_hash" --arg entry_hash "$entry_hash" '{seq:$seq,type:$type,raw_frame_hash:$raw_frame_hash,canonical_frame:$canonical_frame,canonical_frame_hash:$canonical_frame_hash,prev_hash:$prev_hash,entry_hash:$entry_hash}')"
    append_entry "$entry"
    prev_hash="$entry_hash"
  done
else
  [[ $# -eq 0 ]] && { echo "ALMS_WS_RECEIPT_INVALID reason=no_binary_files" >&2; exit 1; }
  for frame_file in "$@"; do
    [[ ! -f "$frame_file" ]] && { echo "ALMS_WS_RECEIPT_INVALID reason=file_not_found file=$frame_file" >&2; exit 1; }
    binary_hash="$(sha256_file "$frame_file")"
    binary_b64="$(base64_file "$frame_file")"
    entry_hash="$(sha256_text "${prev_hash}${binary_hash}")"
    entry="$(jq -cn --argjson seq "$seq_no" --arg type "binary_frame" --arg binary_base64 "$binary_b64" --arg binary_hash "$binary_hash" --arg prev_hash "$prev_hash" --arg entry_hash "$entry_hash" '{seq:$seq,type:$type,binary_base64:$binary_base64,binary_hash:$binary_hash,prev_hash:$prev_hash,entry_hash:$entry_hash}')"
    append_entry "$entry"
    prev_hash="$entry_hash"
  done
fi

session_id="$(sha256_text "$SESSION_NAME")"
final_state_hash="$prev_hash"

jq -cn --arg schema "alms.ws_session_receipt.v0.3" --arg session_name "$SESSION_NAME" --arg session_id "$session_id" --arg initial_state_hash "0x0" --arg canonicalization "json: jq -cS .; binary: raw bytes" --arg final_state_hash "$final_state_hash" --argjson entries "$entries_json" '{schema:$schema,session_name:$session_name,session_id:$session_id,initial_state_hash:$initial_state_hash,canonicalization:$canonicalization,entries:$entries,final_state_hash:$final_state_hash}' > "$TMP_FILE"

mv "$TMP_FILE" "$OUT_FILE"
echo "$OUT_FILE"
