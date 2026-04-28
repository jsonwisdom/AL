#!/usr/bin/env bash
set -euo pipefail

SOURCE_URL="${1:?source url required}"
CLAIM_TEXT="${2:?claim text required}"
JURISDICTION="${3:-US-MN-HOUSE}"

mkdir -p _truth/audit/{sources,raw_text,normalized_text,receipts}

RUN_ID=$(printf "%s" "$SOURCE_URL" | sha256sum | cut -c1-12)
EXT="${SOURCE_URL##*.}"
EXT="${EXT%%\?*}"
SOURCE_FILE="_truth/audit/sources/${RUN_ID}.${EXT}"
RAW_FILE="_truth/audit/raw_text/${RUN_ID}_raw.txt"
NORM_FILE="_truth/audit/normalized_text/${RUN_ID}_norm.txt"
RECEIPT_FILE="_truth/audit/receipts/${RUN_ID}_receipt.json"

curl -LfsS "$SOURCE_URL" -o "$SOURCE_FILE"
SOURCE_SHA=$(sha256sum "$SOURCE_FILE" | awk '{print $1}')

echo "SOURCE_OK sha256=$SOURCE_SHA"

./scripts/canonicalize_source_v1.sh "$SOURCE_FILE" "$RAW_FILE"
RAW_SHA=$(sha256sum "$RAW_FILE" | awk '{print $1}')

echo "RAW_HASH_OK sha256=$RAW_SHA"

iconv -f UTF-8 -t UTF-8//IGNORE "$RAW_FILE" \
  | sed 's/[[:space:]]\+/ /g' \
  | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' \
  > "$NORM_FILE"

NORM_SHA=$(sha256sum "$NORM_FILE" | awk '{print $1}')

echo "NORMALIZED_HASH_OK sha256=$NORM_SHA"

if grep -Fqi -- "$CLAIM_TEXT" "$NORM_FILE"; then
  MATCH_STATUS="MATCH"
  echo "CLAIM_MATCH_OK"
else
  MATCH_STATUS="DRIFT"
  echo "CLAIM_MATCH_FAIL"
fi

cat <<EOF > "$RECEIPT_FILE"
{
  "schema": "portable_audit_receipt_v1",
  "engine": "zero_drift_v1.1.0",
  "meta": { "run_id": "$RUN_ID" },
  "jurisdiction": "$JURISDICTION",
  "source": { "url": "$SOURCE_URL", "sha256": "$SOURCE_SHA" },
  "evidence": {
    "raw_sha256": "$RAW_SHA",
    "norm_sha256": "$NORM_SHA",
    "claim": "$CLAIM_TEXT",
    "status": "$MATCH_STATUS"
  },
  "attestation": { "ens": "jaywisdom.base.eth", "status": "READY_TO_ANCHOR" }
}
EOF

echo "RECEIPT_READY file=$RECEIPT_FILE"
