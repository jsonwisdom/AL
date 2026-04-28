#!/usr/bin/env bash
set -euo pipefail

ROOT="_truth/receipts"
SCHEMA="$ROOT/schema.json"

test -f "$SCHEMA"

mapfile -t RECEIPTS < <(find "$ROOT" -maxdepth 1 -type f -name 'CLAIM_*.json' | LC_ALL=C sort)

if [ "${#RECEIPTS[@]}" -eq 0 ]; then
  echo "ALMS_RECEIPTS_EMPTY root=$ROOT"
  exit 0
fi

for f in "${RECEIPTS[@]}"; do

  python3 -m json.tool "$f" >/dev/null
  jq -e 'type == "object"' "$f" >/dev/null

  claim_id="$(jq -r '.claim_id // empty' "$f")"
  timestamp_utc="$(jq -r '.timestamp_utc // empty' "$f")"
  actor="$(jq -r '.actor // empty' "$f")"
  nonce="$(jq -r '.nonce // empty' "$f")"
  verdict="$(jq -r '.verdict // empty' "$f")"
  base="$(basename "$f" .json)"

  if [ "$claim_id" != "$base" ]; then
    echo "ALMS_RECEIPT_SCHEMA_FAIL claim_id_filename_mismatch file=$f claim_id=$claim_id expected=$base"
    exit 1
  fi

  printf '%s\n' "$claim_id" | grep -Eq '^CLAIM_[0-9]{8}_[0-9]{6}Z_[a-zA-Z0-9_-]+$' || {
    echo "ALMS_RECEIPT_SCHEMA_FAIL invalid_claim_id file=$f claim_id=$claim_id"
    exit 1
  }

  printf '%s\n' "$timestamp_utc" | grep -Eq '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$' || {
    echo "ALMS_RECEIPT_SCHEMA_FAIL invalid_timestamp_utc file=$f timestamp_utc=$timestamp_utc"
    exit 1
  }

  test -n "$actor" || { echo "ALMS_RECEIPT_SCHEMA_FAIL missing_actor file=$f"; exit 1; }
  test "${#nonce}" -ge 8 || { echo "ALMS_RECEIPT_SCHEMA_FAIL nonce_too_short file=$f"; exit 1; }

  jq -e '.inputs | type == "object"' "$f" >/dev/null || {
    echo "ALMS_RECEIPT_SCHEMA_FAIL inputs_not_object file=$f"
    exit 1
  }

  jq -e '.outputs | type == "object"' "$f" >/dev/null || {
    echo "ALMS_RECEIPT_SCHEMA_FAIL outputs_not_object file=$f"
    exit 1
  }

  case "$verdict" in
    VERIFIED|FALSE|MISLEADING|UNVERIFIED|NEEDS_MORE_EVIDENCE|VOID) ;;
    *) echo "ALMS_RECEIPT_SCHEMA_FAIL invalid_verdict file=$f verdict=$verdict"; exit 1 ;;
  esac

  if [ "$verdict" = "VOID" ]; then
    jq -e '.voids_claim_id | test("^CLAIM_[0-9]{8}_[0-9]{6}Z_[a-zA-Z0-9_-]+$")' "$f" >/dev/null || {
      echo "ALMS_RECEIPT_SCHEMA_FAIL void_missing_target file=$f"
      exit 1
    }
  fi

  echo "ALMS_RECEIPT_OK file=$f claim_id=$claim_id verdict=$verdict"
done

echo "ALMS_RECEIPTS_VALIDATE_OK root=$ROOT count=${#RECEIPTS[@]}"
