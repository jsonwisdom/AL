#!/usr/bin/env bash
set -euo pipefail

MONTH="${1:-$(date -u +%Y-%m)}"
ROOT_JSON="_truth/merkle/root.json"
PAYLOAD="_truth/eas/merkle_anchor_$MONTH.json"

test -f "$ROOT_JSON"
test -f "$PAYLOAD"

jq -e '.network == "base" and .root == "jaywisdom.eth" and .actor == "jaywisdom.base" and .status == "READY_FOR_EAS_UI_SIGNATURE"' "$PAYLOAD" >/dev/null

root_month="$(jq -r '.month' "$ROOT_JSON")"
payload_month="$(jq -r '.month' "$PAYLOAD")"

if [ "$root_month" != "$MONTH" ] || [ "$payload_month" != "$MONTH" ]; then
  echo "ALMS_EAS_PAYLOAD_VERIFY_FAIL month_mismatch expected=$MONTH root_month=$root_month payload_month=$payload_month"
  exit 1
fi

for field in merkle_root ledger_sha256 leaf_count algorithm; do
  expected="$(jq -r ".$field" "$ROOT_JSON")"
  actual="$(jq -r ".$field" "$PAYLOAD")"
  if [ "$expected" != "$actual" ]; then
    echo "ALMS_EAS_PAYLOAD_VERIFY_FAIL field_mismatch field=$field expected=$expected actual=$actual"
    exit 1
  fi
done

expected_payload_hash="sha256:$(jq -cS . "$ROOT_JSON" | sha256sum | awk '{print $1}')"
actual_payload_hash="$(jq -r '.payload_hash' "$PAYLOAD")"

if [ "$expected_payload_hash" != "$actual_payload_hash" ]; then
  echo "ALMS_EAS_PAYLOAD_VERIFY_FAIL payload_hash_mismatch expected=$expected_payload_hash actual=$actual_payload_hash"
  exit 1
fi

jq -e '.attestation_uid == "PENDING" and .tx_hash == "PENDING" and .attester == "PENDING"' "$PAYLOAD" >/dev/null

echo "ALMS_EAS_PAYLOAD_VERIFY_OK month=$MONTH payload=$PAYLOAD status=READY_FOR_EAS_UI_SIGNATURE"
