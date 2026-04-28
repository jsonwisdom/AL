#!/usr/bin/env bash
set -euo pipefail

MONTH="${1:-$(date -u +%Y-%m)}"
LEDGER="_truth/ledger/$MONTH.jsonl"

test -f "$LEDGER"

prev_ts=""
count=0

while IFS= read -r line; do
  count=$((count + 1))

  printf '%s\n' "$line" | jq -e 'type == "object"' >/dev/null

  ts="$(printf '%s\n' "$line" | jq -r '.ts')"
  claim_id="$(printf '%s\n' "$line" | jq -r '.claim_id')"
  path="$(printf '%s\n' "$line" | jq -r '.path')"
  expected_sha="$(printf '%s\n' "$line" | jq -r '.sha256')"
  expected_bytes="$(printf '%s\n' "$line" | jq -r '.bytes')"

  test -f "$path"

  base="$(basename "$path" .json)"
  if [ "$claim_id" != "$base" ]; then
    echo "ALMS_LEDGER_VERIFY_FAIL claim_id_path_mismatch line=$count claim_id=$claim_id path=$path"
    exit 1
  fi

  actual_sha="$(sha256sum "$path" | awk '{print $1}')"
  actual_bytes="$(wc -c < "$path" | tr -d ' ')"

  if [ "$expected_sha" != "$actual_sha" ]; then
    echo "ALMS_LEDGER_VERIFY_FAIL receipt_hash_mismatch line=$count path=$path expected=$expected_sha actual=$actual_sha"
    exit 1
  fi

  if [ "$expected_bytes" != "$actual_bytes" ]; then
    echo "ALMS_LEDGER_VERIFY_FAIL receipt_bytes_mismatch line=$count path=$path expected=$expected_bytes actual=$actual_bytes"
    exit 1
  fi

  if [ -n "$prev_ts" ] && [[ "$ts" < "$prev_ts" ]]; then
    echo "ALMS_LEDGER_VERIFY_FAIL timestamp_order_violation line=$count prev_ts=$prev_ts ts=$ts"
    exit 1
  fi

  prev_ts="$ts"
done < "$LEDGER"

ledger_sha256="$(sha256sum "$LEDGER" | awk '{print $1}')"
echo "ALMS_LEDGER_VERIFY_OK month=$MONTH count=$count ledger=$LEDGER ledger_sha256=$ledger_sha256"
