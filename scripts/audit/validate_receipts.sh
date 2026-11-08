#!/usr/bin/env bash
set -euo pipefail

# CI-FIRST: validate production receipts separately from preserved legacy claim-hash receipts.
# This validator never writes, upgrades, or re-labels evidence.
ROOT="${ALMS_RECEIPT_ROOT:-_truth/receipts}"
SCHEMA="$ROOT/schema.json"
test -f "$SCHEMA" || { echo "ALMS_RECEIPT_SCHEMA_FAIL missing_schema=$SCHEMA"; exit 1; }

production=0
legacy=0
found=0

while IFS= read -r -d '' f; do
  found=$((found + 1))
  base="${f##*/}"
  python3 -m json.tool "$f" >/dev/null || { echo "ALMS_RECEIPT_SCHEMA_FAIL invalid_json file=$f"; exit 1; }

  if [[ "$base" =~ ^CLAIM_[0-9]+\.receipt\.json$ ]]; then
    # These older source-hash records are not production verdicts or replay evidence.
    claim_id="${base%.receipt.json}"
    if ! jq -e --arg id "$claim_id" \
      'type == "object"
       and (.claim_id == $id)
       and (.claim_path == ("_truth/claims/" + $id + ".json"))
       and (.claim_hash | type == "string" and test("^[0-9a-fA-F]{64}$"))
       and (.version == 1)
       and (.status | type == "string" and length > 0)' "$f" >/dev/null; then
      echo "ALMS_RECEIPT_SCHEMA_FAIL malformed_legacy file=$f"
      exit 1
    fi
    legacy=$((legacy + 1))
    echo "ALMS_LEGACY_RECEIPT_INVENTORIED file=$f claim_id=$claim_id hash_format=VALID hash_content=UNKNOWN not_production=true"
    continue
  fi

  if [[ ! "$base" =~ ^CLAIM_[0-9]{8}_[0-9]{6}Z_[a-zA-Z0-9_-]+\.json$ ]]; then
    echo "ALMS_RECEIPT_SCHEMA_FAIL unclassified_claim_file=$f"
    exit 1
  fi

  claim_id="${base%.json}"
  if ! jq -e --arg id "$claim_id" \
    'type == "object"
     and (.claim_id == $id)
     and (.claim_id | type == "string" and test("^CLAIM_[0-9]{8}_[0-9]{6}Z_[a-zA-Z0-9_-]+$"))
     and (.timestamp_utc | type == "string" and test("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"))
     and (.actor | type == "string" and length > 0)
     and (.nonce | type == "string" and length >= 8)
     and (.inputs | type == "object")
     and (.outputs | type == "object")
     and (.verdict as $v | ["VERIFIED", "FALSE", "MISLEADING", "UNVERIFIED", "NEEDS_MORE_EVIDENCE", "VOID"] | index($v) != null)
     and (if .verdict == "VOID" then (.voids_claim_id | type == "string" and test("^CLAIM_[0-9]{8}_[0-9]{6}Z_[a-zA-Z0-9_-]+$")) else true end)
     and ((keys - ["claim_id", "timestamp_utc", "actor", "nonce", "inputs", "outputs", "verdict", "voids_claim_id"]) | length == 0)' "$f" >/dev/null; then
    echo "ALMS_RECEIPT_SCHEMA_FAIL invalid_production_record file=$f"
    exit 1
  fi

  production=$((production + 1))
  echo "ALMS_PRODUCTION_RECEIPT_SCHEMA_OK file=$f claim_id=$claim_id"
done < <(find "$ROOT" -maxdepth 1 -type f -name 'CLAIM_*.json' -print0 | LC_ALL=C sort -z)

if (( found == 0 || production == 0 )); then
  echo "ALMS_PRODUCTION_RECEIPTS_MISSING root=$ROOT production_count=$production legacy_count=$legacy"
  exit 1
fi

echo "ALMS_RECEIPT_SCHEMA_PASS production_count=$production legacy_count=$legacy"
echo "ALMS_RUNTIME_EXECUTION=UNKNOWN ALMS_LEGACY_HASH_CONTENT=UNKNOWN AUTHORITY_CREATED=false"
