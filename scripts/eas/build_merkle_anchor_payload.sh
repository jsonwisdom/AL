#!/usr/bin/env bash
set -euo pipefail

MONTH="${1:-$(date -u +%Y-%m)}"
ROOT_JSON="_truth/merkle/root.json"
OUT="_truth/eas/merkle_anchor_$MONTH.json"
mkdir -p _truth/eas

test -f "$ROOT_JSON"

root_month="$(jq -r '.month' "$ROOT_JSON")"
if [ "$root_month" != "$MONTH" ]; then
  echo "ALMS_EAS_PAYLOAD_BUILD_FAIL month_mismatch expected=$MONTH actual=$root_month"
  exit 1
fi

merkle_root="$(jq -r '.merkle_root' "$ROOT_JSON")"
ledger_sha256="$(jq -r '.ledger_sha256' "$ROOT_JSON")"
source_ledger="$(jq -r '.source_ledger' "$ROOT_JSON")"
leaf_count="$(jq -r '.leaf_count' "$ROOT_JSON")"
algorithm="$(jq -r '.algorithm' "$ROOT_JSON")"
root_status="$(jq -r '.status' "$ROOT_JSON")"

if [ "$root_status" != "READY_FOR_EAS_ANCHOR" ]; then
  echo "ALMS_EAS_PAYLOAD_BUILD_FAIL merkle_not_ready status=$root_status"
  exit 1
fi

printf '%s\n' "$merkle_root" | grep -Eq '^[a-f0-9]{64}$' || {
  echo "ALMS_EAS_PAYLOAD_BUILD_FAIL invalid_merkle_root root=$merkle_root"
  exit 1
}

payload_hash="$(jq -cS . "$ROOT_JSON" | sha256sum | awk '{print $1}')"
built_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

jq -cn \
  --arg payload_id "ALMS_EAS_MERKLE_ANCHOR_${MONTH//-/_}" \
  --arg network "base" \
  --arg root "jaywisdom.eth" \
  --arg actor "jaywisdom.base" \
  --arg month "$MONTH" \
  --arg source_merkle_root "$ROOT_JSON" \
  --arg source_ledger "$source_ledger" \
  --arg merkle_root "$merkle_root" \
  --arg ledger_sha256 "$ledger_sha256" \
  --arg algorithm "$algorithm" \
  --arg payload_hash "sha256:$payload_hash" \
  --arg status "READY_FOR_EAS_UI_SIGNATURE" \
  --arg built_at_utc "$built_at" \
  --argjson leaf_count "$leaf_count" \
  '{
    payload_id:$payload_id,
    network:$network,
    root:$root,
    actor:$actor,
    month:$month,
    source_merkle_root:$source_merkle_root,
    source_ledger:$source_ledger,
    merkle_root:$merkle_root,
    ledger_sha256:$ledger_sha256,
    leaf_count:$leaf_count,
    algorithm:$algorithm,
    payload_hash:$payload_hash,
    status:$status,
    attestation_uid:"PENDING",
    tx_hash:"PENDING",
    attester:"PENDING",
    built_at_utc:$built_at_utc
  }' > "$OUT"

echo "ALMS_EAS_PAYLOAD_BUILD_OK month=$MONTH merkle_root=$merkle_root payload=$OUT status=READY_FOR_EAS_UI_SIGNATURE"
