#!/usr/bin/env bash
# Normalize raw DOJ data.json into dataset-specific receipts
# Part of jsonwisdom/AL DOJ data_json lane

set -euo pipefail

RAW_DIR="_truth/doj_data_json/data"
OUTPUT_DIR="_truth/doj_data_json/datasets"
INDEX_DIR="_truth/doj_data_json/indexes"
EXTRACTED_AT="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
SAFE_TIMESTAMP="$(date -u +"%Y%m%dT%H%M%SZ")"

mkdir -p "$OUTPUT_DIR" "$INDEX_DIR"

LATEST_RAW="$(find "$RAW_DIR" -maxdepth 1 -type f -name 'raw_*.json' 2>/dev/null | sort | tail -n 1 || true)"

if [[ -z "$LATEST_RAW" ]]; then
  echo "[ERROR] No raw capture found in $RAW_DIR"
  echo "[HINT] Run scripts/capture_doj_data_json.sh first"
  exit 1
fi

jq empty "$LATEST_RAW"

echo "[PROCESS] Extracting DOJ datasets from: $LATEST_RAW"

DATASET_COUNT="$(jq '.dataset | length' "$LATEST_RAW")"
INDEX_FILE="$INDEX_DIR/dataset_index_${SAFE_TIMESTAMP}.jsonl"
: > "$INDEX_FILE"

jq -c '.dataset[]' "$LATEST_RAW" | while IFS= read -r dataset; do
  RAW_ID="$(printf '%s' "$dataset" | jq -r '.identifier // .title // "missing_identifier"')"
  SAFE_ID="$(printf '%s' "$RAW_ID" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/_/g; s/^_*//; s/_*$//; s/__*/_/g')"

  if [[ -z "$SAFE_ID" || "$SAFE_ID" == "null" ]]; then
    SAFE_ID="missing_identifier"
  fi

  DATASET_HASH="$(printf '%s' "$dataset" | sha256sum | awk '{print $1}')"
  SHORT_HASH="${DATASET_HASH:0:12}"
  RECEIPT_ID="${SAFE_ID}_${SHORT_HASH}"

  RECEIPT_FILE="$OUTPUT_DIR/receipt_${RECEIPT_ID}.json"
  MANIFEST_FILE="$OUTPUT_DIR/receipt_${RECEIPT_ID}.manifest.json"

  printf '%s\n' "$dataset" | jq . > "$RECEIPT_FILE"

  jq -n \
    --arg receipt_id "$RECEIPT_ID" \
    --arg source_file "$(basename "$LATEST_RAW")" \
    --arg extracted_at "$EXTRACTED_AT" \
    --arg hash_sha256 "$DATASET_HASH" \
    --arg raw_identifier "$RAW_ID" \
    --arg receipt_file "$RECEIPT_FILE" \
    --arg authority "false" \
    '{
      receipt_id: $receipt_id,
      source_file: $source_file,
      extracted_at: $extracted_at,
      hash_sha256: $hash_sha256,
      raw_identifier: $raw_identifier,
      receipt_file: $receipt_file,
      authority: false,
      verification_state: "NORMALIZED_NOT_INTERPRETED"
    }' > "$MANIFEST_FILE"

  jq -n \
    --arg receipt_id "$RECEIPT_ID" \
    --arg hash_sha256 "$DATASET_HASH" \
    --arg raw_identifier "$RAW_ID" \
    --arg receipt_file "$RECEIPT_FILE" \
    --arg manifest_file "$MANIFEST_FILE" \
    '{
      receipt_id: $receipt_id,
      hash_sha256: $hash_sha256,
      raw_identifier: $raw_identifier,
      receipt_file: $receipt_file,
      manifest_file: $manifest_file
    }' >> "$INDEX_FILE"
done

NORMALIZED_COUNT="$(wc -l < "$INDEX_FILE" | tr -d ' ')"

echo "[SUCCESS] Extraction complete"
echo "SOURCE=$LATEST_RAW"
echo "DATASET_COUNT=$DATASET_COUNT"
echo "NORMALIZED_COUNT=$NORMALIZED_COUNT"
echo "OUTPUT_DIR=$OUTPUT_DIR"
echo "INDEX_FILE=$INDEX_FILE"
