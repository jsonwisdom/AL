#!/usr/bin/env bash
set -euo pipefail

MONTH="${1:-$(date -u +%Y-%m)}"
LEDGER="_truth/ledger/$MONTH.jsonl"
ROOT_JSON="_truth/merkle/root.json"

test -f "$LEDGER"
test -f "$ROOT_JSON"

EXPECTED_LEDGER_SHA="$(jq -r '.ledger_sha256' "$ROOT_JSON")"
ACTUAL_LEDGER_SHA="$(sha256sum "$LEDGER" | awk '{print $1}')"

if [ "$EXPECTED_LEDGER_SHA" != "$ACTUAL_LEDGER_SHA" ]; then
  echo "ALMS_MERKLE_VERIFY_FAIL ledger_sha256_mismatch expected=$EXPECTED_LEDGER_SHA actual=$ACTUAL_LEDGER_SHA"
  exit 1
fi

EXPECTED_COUNT="$(jq -r '.leaf_count' "$ROOT_JSON")"
ACTUAL_COUNT="$(wc -l < "$LEDGER" | tr -d ' ')"

if [ "$EXPECTED_COUNT" != "$ACTUAL_COUNT" ]; then
  echo "ALMS_MERKLE_VERIFY_FAIL leaf_count_mismatch expected=$EXPECTED_COUNT actual=$ACTUAL_COUNT"
  exit 1
fi

jq -e '.algorithm == "sha256_pairwise_sorted_v1" and .status == "READY_FOR_EAS_ANCHOR"' "$ROOT_JSON" >/dev/null

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

jq -r '.sha256' "$LEDGER" | LC_ALL=C sort > "$TMP/current.txt"

if [ "$ACTUAL_COUNT" = "0" ]; then
  echo "ALMS_MERKLE_VERIFY_FAIL empty_ledger ledger=$LEDGER"
  exit 1
fi

while [ "$(wc -l < "$TMP/current.txt" | tr -d ' ')" -gt 1 ]; do
  : > "$TMP/next.txt"
  mapfile -t nodes < "$TMP/current.txt"
  i=0
  while [ "$i" -lt "${#nodes[@]}" ]; do
    left="${nodes[$i]}"
    right="${nodes[$((i+1))]:-${nodes[$i]}}"
    printf '%s%s' "$left" "$right" | sha256sum | awk '{print $1}' >> "$TMP/next.txt"
    i=$((i+2))
  done
  LC_ALL=C sort "$TMP/next.txt" > "$TMP/current.txt"
done

ACTUAL_ROOT="$(cat "$TMP/current.txt")"
EXPECTED_ROOT="$(jq -r '.merkle_root' "$ROOT_JSON")"

if [ "$EXPECTED_ROOT" != "$ACTUAL_ROOT" ]; then
  echo "ALMS_MERKLE_VERIFY_FAIL root_mismatch expected=$EXPECTED_ROOT actual=$ACTUAL_ROOT"
  exit 1
fi

echo "ALMS_MERKLE_VERIFY_OK month=$MONTH leaf_count=$ACTUAL_COUNT merkle_root=$ACTUAL_ROOT"
