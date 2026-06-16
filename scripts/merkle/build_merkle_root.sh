#!/usr/bin/env bash
set -euo pipefail

MONTH="${1:-$(date -u +%Y-%m)}"
LEDGER="_truth/ledger/$MONTH.jsonl"
OUT="_truth/merkle/root.json"
mkdir -p _truth/merkle

test -f "$LEDGER"

LEDGER_SHA256="$(sha256sum "$LEDGER" | awk '{print $1}')"
LEAF_COUNT="$(wc -l < "$LEDGER" | tr -d ' ')"

if [ "$LEAF_COUNT" = "0" ]; then
  echo "ALMS_MERKLE_BUILD_FAIL empty_ledger ledger=$LEDGER"
  exit 1
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

jq -r '.sha256' "$LEDGER" | LC_ALL=C sort > "$TMP/level_0.txt"
cp "$TMP/level_0.txt" "$TMP/current.txt"
level=0

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
  level=$((level+1))
  LC_ALL=C sort "$TMP/next.txt" > "$TMP/level_$level.txt"
  cp "$TMP/level_$level.txt" "$TMP/current.txt"
done

MERKLE_ROOT="$(cat "$TMP/current.txt")"
BUILT_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

jq -cn \
  --arg root_id "ALMS_MERKLE_ROOT_${MONTH//-/_}" \
  --arg month "$MONTH" \
  --arg source_ledger "$LEDGER" \
  --arg ledger_sha256 "$LEDGER_SHA256" \
  --arg merkle_root "$MERKLE_ROOT" \
  --arg algorithm "sha256_pairwise_sorted_v1" \
  --arg status "READY_FOR_EAS_ANCHOR" \
  --arg built_at_utc "$BUILT_AT" \
  --argjson leaf_count "$LEAF_COUNT" \
  '{root_id:$root_id, month:$month, source_ledger:$source_ledger, ledger_sha256:$ledger_sha256, merkle_root:$merkle_root, leaf_count:$leaf_count, algorithm:$algorithm, status:$status, built_at_utc:$built_at_utc}' \
  > "$OUT"

echo "ALMS_MERKLE_BUILD_OK month=$MONTH leaf_count=$LEAF_COUNT merkle_root=$MERKLE_ROOT root=$OUT"
