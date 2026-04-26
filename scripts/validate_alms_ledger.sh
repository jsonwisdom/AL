#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LEDGER="$ROOT/_truth/ledger/alms_ledger.jsonl"

[[ -f "$LEDGER" ]] || { echo "MISSING_LEDGER"; exit 1; }

prev="GENESIS"
line_no=0

while IFS= read -r line; do
  [[ -z "$line" ]] && continue
  line_no=$((line_no + 1))

  got_prev="$(printf '%s\n' "$line" | jq -r '.previous_hash')"
  got_hash="$(printf '%s\n' "$line" | jq -r '.entry_hash')"

  [[ "$got_prev" == "$prev" ]] || {
    echo "CHAIN_BREAK line=$line_no expected_prev=$prev got=$got_prev"
    exit 1
  }

  recomputed="$(
    printf '%s\n' "$line" \
      | jq -c 'del(.entry_hash)' \
      | sha256sum \
      | awk '{print $1}'
  )"

  [[ "$recomputed" == "$got_hash" ]] || {
    echo "HASH_MISMATCH line=$line_no expected=$recomputed got=$got_hash"
    exit 1
  }

  prev="$got_hash"
done < "$LEDGER"

echo "ALMS_LEDGER_VALID lines=$line_no tip=$prev"
