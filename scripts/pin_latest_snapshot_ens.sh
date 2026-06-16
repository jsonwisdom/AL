#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG="$ROOT/_truth/logs/ipfs_ens.log"
PIN_LEDGER="$ROOT/_truth/ledger/ipfs_pins.jsonl"

mkdir -p "$ROOT/_truth/logs" "$ROOT/_truth/ledger"

SNAPSHOT="$(ls -1t "$ROOT"/_truth/snapshots/alms_ledger_*.jsonl | head -n 1)"
SHA256="$(sha256sum "$SNAPSHOT" | awk '{print $1}')"
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

echo "PIN_START $TS $SNAPSHOT" >> "$LOG"

if [[ -z "${PINATA_JWT:-}" ]]; then
  echo "MISSING_PINATA_JWT" >&2
  echo "Set PINATA_JWT first."
  exit 1
fi

RESP="$(curl -sS -X POST "https://api.pinata.cloud/pinning/pinFileToIPFS" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -F "file=@${SNAPSHOT}")"

CID="$(printf '%s\n' "$RESP" | jq -r '.IpfsHash // empty')"

[[ -n "$CID" ]] || {
  echo "IPFS_PIN_FAILED $RESP" >&2
  exit 1
}

jq -cn \
  --arg ts "$TS" \
  --arg file "$(basename "$SNAPSHOT")" \
  --arg sha256 "$SHA256" \
  --arg cid "$CID" \
  '{type:"ALMS_IPFS_PIN",timestamp:$ts,file:$file,sha256:$sha256,cid:$cid}' >> "$PIN_LEDGER"

echo "PIN_OK cid=$CID sha256=$SHA256" >> "$LOG"

if [[ -n "${ENS_NAME:-}" && -n "${ENS_RESOLVER_ADDRESS:-}" && -n "${RPC_URL:-}" && -n "${PRIVATE_KEY:-}" ]]; then
  NODE="$(cast namehash "$ENS_NAME")"

  cast send "$ENS_RESOLVER_ADDRESS" \
    "setText(bytes32,string,string)" \
    "$NODE" \
    "alms.latest.cid" \
    "$CID" \
    --rpc-url "$RPC_URL" \
    --private-key "$PRIVATE_KEY" >> "$LOG" 2>&1

  cast send "$ENS_RESOLVER_ADDRESS" \
    "setText(bytes32,string,string)" \
    "$NODE" \
    "alms.latest.sha256" \
    "$SHA256" \
    --rpc-url "$RPC_URL" \
    --private-key "$PRIVATE_KEY" >> "$LOG" 2>&1

  echo "ENS_UPDATE_OK name=$ENS_NAME cid=$CID" >> "$LOG"
else
  echo "ENS_SKIPPED missing ENS_NAME/ENS_RESOLVER_ADDRESS/RPC_URL/PRIVATE_KEY" >> "$LOG"
fi

echo "$CID"
