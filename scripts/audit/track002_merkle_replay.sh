#!/usr/bin/env bash
set -euo pipefail

EXPECTED_ROOT="dc4b992f9f6eb41139056a5f75af6d523ed6f55a9775da21401e8bc185e86f5c"
EXPECTED_ALGO="sha256_hex_concat_v1"
OUT="_truth/audit/track002_merkle_replay_report.json"

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
    PARENT=$(printf "%s%s" "$LEFT" "$RIGHT" | sha256sum | awk '{print $1}')
    NEXT+=("$PARENT")
  done

  CURRENT=("${NEXT[@]}")
done

REBUILT_ROOT="${CURRENT[0]}"
MATCH=false
[[ "$REBUILT_ROOT" == "$EXPECTED_ROOT" ]] && MATCH=true

{
  echo "{"
  echo "  \"track\": \"002_MERKLE_REPLAY\","
  echo "  \"parent_commit\": \"$(git rev-parse HEAD)\","
  echo "  \"algorithm\": \"$EXPECTED_ALGO\","
  echo "  \"leaf_count\": $N,"
  echo "  \"expected_root\": \"$EXPECTED_ROOT\","
  echo "  \"rebuilt_root\": \"$REBUILT_ROOT\","
  echo "  \"match\": $MATCH,"
  echo "  \"leaves\": ["
  for ((i=0;i<N;i++)); do
    echo "    {\"leaf_id\":\"${LEAF_IDS[$i]}\",\"canonical_sha256\":\"${LEVEL[$i]}\"}"
    [[ $i -lt $((N-1)) ]] && echo ","
  done
  echo "  ]"
  echo "}"
} > "$OUT"

if [[ "$MATCH" != true ]]; then
  echo "TRACK002_MERKLE_REPLAY_FAIL expected=$EXPECTED_ROOT got=$REBUILT_ROOT leaves=$N"
  cat "$OUT" | jq .
  exit 1
fi

echo "TRACK002_MERKLE_REPLAY_OK root=$REBUILT_ROOT leaves=$N algorithm=$EXPECTED_ALGO"
cat "$OUT" | jq .
