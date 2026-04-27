#!/usr/bin/env bash
set -euo pipefail

OUT="merkle_proofs.json"
TMP="$(mktemp)"

# Collect leaves (sorted, deterministic)
mapfile -t LEAVES < <(
  jq -r '.leaf_id + " " + .canonical_sha256' \
  _truth/receipts/*.receipt.json | LC_ALL=C sort
)

# Extract hashes only
HASHES=()
for L in "${LEAVES[@]}"; do
  HASHES+=("$(echo "$L" | awk '{print $2}')")
done

# Build tree layers
TREE=()
TREE+=("${HASHES[@]}")

LEVEL=("${HASHES[@]}")
PROOFS=()

while [ "${#LEVEL[@]}" -gt 1 ]; do
  NEXT=()
  for ((i=0; i<${#LEVEL[@]}; i+=2)); do
    LEFT="${LEVEL[i]}"
    if [ $((i+1)) -lt ${#LEVEL[@]} ]; then
      RIGHT="${LEVEL[i+1]}"
    else
      RIGHT="$LEFT"
    fi

    PARENT=$(printf "%s%s" "$LEFT" "$RIGHT" | sha256sum | awk '{print $1}')
    NEXT+=("$PARENT")
  done
  LEVEL=("${NEXT[@]}")
done

MERKLE_ROOT="${LEVEL[0]}"

# Build JSON output
{
  echo "{"
  echo "\"merkle_root\":\"$MERKLE_ROOT\","
  echo "\"leaf_count\":${#HASHES[@]},"
  echo "\"leaves\":["
  
  for i in "${!LEAVES[@]}"; do
    ID=$(echo "${LEAVES[$i]}" | awk '{print $1}')
    H=$(echo "${LEAVES[$i]}" | awk '{print $2}')
    
    echo "{"
    echo "\"leaf_id\":\"$ID\","
    echo "\"leaf_hash\":\"$H\","
    echo "\"proof\":[]"
    echo "}"
    
    if [ "$i" -lt $((${#LEAVES[@]}-1)) ]; then
      echo ","
    fi
  done

  echo "]"
  echo "}"
} > "$OUT"

echo "MERKLE_ROOT_BUILT $MERKLE_ROOT leaves=${#HASHES[@]}"
