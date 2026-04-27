#!/usr/bin/env bash
set -euo pipefail

OUT="merkle_proofs.json"

# --- LOAD LEAVES (deterministic) ---
mapfile -t PAIRS < <(
  jq -r '.leaf_id + " " + .canonical_sha256' \
  _truth/receipts/*.receipt.json | LC_ALL=C sort
)

LEAF_IDS=()
LEVEL=()

for P in "${PAIRS[@]}"; do
  LEAF_IDS+=("$(echo "$P" | awk '{print $1}')")
  LEVEL+=("$(echo "$P" | awk '{print $2}')")
done

N=${#LEVEL[@]}

# --- INIT PROOF STORAGE ---
declare -A PROOFS

for ((i=0;i<N;i++)); do
  PROOFS[$i]=""
done

# --- BUILD TREE + PROOFS ---
CURRENT=("${LEVEL[@]}")

while [ "${#CURRENT[@]}" -gt 1 ]; do
  NEXT=()
  LEN=${#CURRENT[@]}

  for ((i=0;i<LEN;i+=2)); do
    LEFT="${CURRENT[i]}"
    
    if [ $((i+1)) -lt $LEN ]; then
      RIGHT="${CURRENT[i+1]}"
    else
      RIGHT="$LEFT"
    fi

    # record proof
    if [ $((i+1)) -lt $LEN ]; then
      PROOFS[$i]+=" {\"side\":\"right\",\"hash\":\"$RIGHT\"},"
      PROOFS[$((i+1))]+=" {\"side\":\"left\",\"hash\":\"$LEFT\"},"
    fi

    PARENT=$(printf "%s%s" "$LEFT" "$RIGHT" | sha256sum | awk '{print $1}')
    NEXT+=("$PARENT")
  done

  CURRENT=("${NEXT[@]}")
done

MERKLE_ROOT="${CURRENT[0]}"

# --- OUTPUT JSON ---
{
  echo "{"
  echo "\"algorithm\":\"sha256_hex_concat_v1\","
  echo "\"merkle_root\":\"$MERKLE_ROOT\","
  echo "\"leaf_count\":$N,"
  echo "\"leaves\":["

  for ((i=0;i<N;i++)); do
    ID="${LEAF_IDS[$i]}"
    H="${LEVEL[$i]}"
    P="${PROOFS[$i]}"

    # trim trailing comma
    P="${P%,}"

    echo "{"
    echo "\"leaf_id\":\"$ID\","
    echo "\"leaf_hash\":\"$H\","
    echo "\"proof\":[ $P ]"
    echo "}"

    if [ $i -lt $((N-1)) ]; then echo ","; fi
  done

  echo "]"
  echo "}"
} > "$OUT"

echo "MERKLE_PROOFS_OK root=$MERKLE_ROOT leaves=$N"
