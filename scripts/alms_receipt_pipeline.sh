#!/usr/bin/env bash
# ALMS Receipt Pipeline v0.1
# One-command wrapper for generate -> verify -> hash -> optional pin -> ledger candidate.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

usage() {
  cat <<'USAGE'
Usage:
  JSON stdin:
    printf '%s\n' '{"type":"x"}' | bash scripts/alms_receipt_pipeline.sh <receipt_name> --json --stdin

  JSON args:
    bash scripts/alms_receipt_pipeline.sh <receipt_name> --json '{"type":"x"}' '{"a":1}'

  Binary files:
    bash scripts/alms_receipt_pipeline.sh <receipt_name> --binary file1.bin [file2.bin]

Optional environment:
  PINATA_JWT=<jwt>   If set, pipeline attempts Pinata upload.

Rules:
  - No private keys.
  - No wallet dependency.
  - No EAS/ENS dependency.
  - No synthetic CID.
  - If IPFS backend is unavailable, receipt remains VALID and IPFS is PENDING.
USAGE
}

if [[ $# -lt 3 ]]; then usage >&2; exit 1; fi

RECEIPT_NAME="$1"
MODE="$2"
shift 2

if [[ ! "$RECEIPT_NAME" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo '{"valid":false,"reason":"bad_receipt_name"}'
  exit 1
fi

mkdir -p _truth/websocket_sessions _truth/ledger _truth/logs

RECEIPT_PATH="_truth/websocket_sessions/${RECEIPT_NAME}.json"
LEDGER_CANDIDATE="_truth/ledger/${RECEIPT_NAME}_candidate.json"
VERIFY_TMP="_truth/logs/${RECEIPT_NAME}.verify.json"
PIN_TMP="_truth/logs/${RECEIPT_NAME}.pinata.json"

# 1. Generate receipt
if [[ "$MODE" == "--json" ]]; then
  if [[ "${1:-}" == "--stdin" ]]; then
    bash scripts/ws_session_receipt.sh "$RECEIPT_NAME" --json --stdin
  else
    bash scripts/ws_session_receipt.sh "$RECEIPT_NAME" --json "$@"
  fi
elif [[ "$MODE" == "--binary" ]]; then
  bash scripts/ws_session_receipt.sh "$RECEIPT_NAME" --binary "$@"
else
  echo '{"valid":false,"reason":"bad_mode"}'
  exit 1
fi

# 2. Verify receipt
if ! bash scripts/verify_ws_session.sh "$RECEIPT_PATH" > "$VERIFY_TMP"; then
  cat "$VERIFY_TMP"
  exit 1
fi

VALID="$(jq -r '.valid' "$VERIFY_TMP")"
REPLAY_MATCH="$(jq -r '.replay_match' "$VERIFY_TMP")"
DELTAS_PROCESSED="$(jq -r '.deltas_processed' "$VERIFY_TMP")"

if [[ "$VALID" != "true" || "$REPLAY_MATCH" != "true" ]]; then
  cat "$VERIFY_TMP"
  exit 1
fi

# 3. Compute SHA-256
SHA256="$(sha256sum "$RECEIPT_PATH" | awk '{print $1}')"

# 4. Try IPFS pinning
IPFS_STATUS="PENDING"
IPFS_CID=""
IPFS_METHOD="none"
IPFS_ERROR=""

if command -v ipfs >/dev/null 2>&1; then
  if IPFS_OUT="$(ipfs add -Q "$RECEIPT_PATH" 2>&1)"; then
    IPFS_STATUS="PINNED"
    IPFS_CID="$IPFS_OUT"
    IPFS_METHOD="local_ipfs"
  else
    IPFS_STATUS="FAILED"
    IPFS_ERROR="$IPFS_OUT"
    IPFS_METHOD="local_ipfs"
  fi
elif [[ -n "${PINATA_JWT:-}" ]]; then
  if curl -sS -X POST "https://api.pinata.cloud/pinning/pinFileToIPFS" \
    -H "Authorization: Bearer ${PINATA_JWT}" \
    -F "file=@${RECEIPT_PATH}" > "$PIN_TMP"; then
    if IPFS_CID="$(jq -r '.IpfsHash // empty' "$PIN_TMP")" && [[ -n "$IPFS_CID" ]]; then
      IPFS_STATUS="PINNED"
      IPFS_METHOD="pinata"
    else
      IPFS_STATUS="FAILED"
      IPFS_METHOD="pinata"
      IPFS_ERROR="pinata_response_missing_IpfsHash"
    fi
  else
    IPFS_STATUS="FAILED"
    IPFS_METHOD="pinata"
    IPFS_ERROR="pinata_curl_failed"
  fi
fi

# 5. Write ledger candidate
jq -cn \
  --arg receipt_name "$RECEIPT_NAME" \
  --arg protocol "ALMS-WS" \
  --arg version "v0.3" \
  --arg receipt_path "$RECEIPT_PATH" \
  --arg sha256 "$SHA256" \
  --arg classification "VALID" \
  --arg verifier "scripts/verify_ws_session.sh" \
  --arg ipfs_status "$IPFS_STATUS" \
  --arg ipfs_cid "$IPFS_CID" \
  --arg ipfs_method "$IPFS_METHOD" \
  --arg ipfs_error "$IPFS_ERROR" \
  --argjson replay_match "$REPLAY_MATCH" \
  --argjson deltas_processed "$DELTAS_PROCESSED" \
  '{receipt_name:$receipt_name,protocol:$protocol,version:$version,receipt_path:$receipt_path,sha256:$sha256,classification:$classification,verification:{replay_match:$replay_match,deltas_processed:$deltas_processed,verifier:$verifier},ipfs:{status:$ipfs_status,cid:$ipfs_cid,method:$ipfs_method,error:$ipfs_error}}' \
  > "$LEDGER_CANDIDATE"

# 6. Print machine-readable summary
jq -cn \
  --arg receipt_name "$RECEIPT_NAME" \
  --arg receipt_path "$RECEIPT_PATH" \
  --arg sha256 "$SHA256" \
  --arg ledger_candidate "$LEDGER_CANDIDATE" \
  --arg ipfs_status "$IPFS_STATUS" \
  --arg ipfs_cid "$IPFS_CID" \
  --arg ipfs_method "$IPFS_METHOD" \
  --arg ipfs_error "$IPFS_ERROR" \
  --argjson valid "$VALID" \
  --argjson replay_match "$REPLAY_MATCH" \
  --argjson deltas_processed "$DELTAS_PROCESSED" \
  '{receipt_name:$receipt_name,receipt_path:$receipt_path,valid:$valid,replay_match:$replay_match,deltas_processed:$deltas_processed,sha256:$sha256,ipfs:{status:$ipfs_status,cid:$ipfs_cid,method:$ipfs_method,error:$ipfs_error},ledger_candidate:$ledger_candidate}'
