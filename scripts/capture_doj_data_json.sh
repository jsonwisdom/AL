#!/usr/bin/env bash
# Capture and hash verification for DOJ data.json
# Part of jsonwisdom/AL DOJ data_json lane

set -euo pipefail

TARGET_URL="https://www.justice.gov/data.json"
LANE_DIR="_truth/doj_data_json"
OUTPUT_DIR="$LANE_DIR/data"
MANIFEST_DIR="$LANE_DIR/manifests"
TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
SAFE_TIMESTAMP="$(date -u +"%Y%m%dT%H%M%SZ")"
INGEST_ID="doj_data_json_${SAFE_TIMESTAMP}"
RAW_FILE="$OUTPUT_DIR/raw_${SAFE_TIMESTAMP}.json"
SHA_FILE="$OUTPUT_DIR/receipt_${SAFE_TIMESTAMP}.sha256"
MANIFEST_FILE="$MANIFEST_DIR/manifest_${SAFE_TIMESTAMP}.json"

mkdir -p "$OUTPUT_DIR" "$MANIFEST_DIR"

echo "[INIT] Capturing DOJ data.json at $TIMESTAMP"
echo "[SOURCE] $TARGET_URL"

curl -L -sS -f \
  --user-agent "JSONWisdom-DOJ-Data-Audit/0.1" \
  "$TARGET_URL" \
  -o "$RAW_FILE"

jq empty "$RAW_FILE"

HASH_SHA256="$(sha256sum "$RAW_FILE" | awk '{print $1}')"
BYTE_COUNT="$(wc -c < "$RAW_FILE" | tr -d ' ')"
DATASET_COUNT="$(jq '.dataset | length' "$RAW_FILE")"

printf "%s  %s\n" "$HASH_SHA256" "$RAW_FILE" > "$SHA_FILE"

jq -n \
  --arg ingest_id "$INGEST_ID" \
  --arg timestamp "$TIMESTAMP" \
  --arg source "$TARGET_URL" \
  --arg raw_file "$RAW_FILE" \
  --arg sha_file "$SHA_FILE" \
  --arg hash_sha256 "$HASH_SHA256" \
  --argjson byte_count "$BYTE_COUNT" \
  --argjson dataset_count "$DATASET_COUNT" \
  '{
    ingest_id: $ingest_id,
    timestamp: $timestamp,
    source: $source,
    raw_file: $raw_file,
    sha_file: $sha_file,
    hash_sha256: $hash_sha256,
    byte_count: $byte_count,
    dataset_count: $dataset_count,
    authority: false,
    verification_state: "CAPTURED_NOT_INTERPRETED"
  }' > "$MANIFEST_FILE"

echo "[SUCCESS] DOJ data.json receipt generated"
echo "INGEST_ID=$INGEST_ID"
echo "RAW_FILE=$RAW_FILE"
echo "SHA_FILE=$SHA_FILE"
echo "MANIFEST_FILE=$MANIFEST_FILE"
echo "HASH_SHA256=$HASH_SHA256"
echo "BYTE_COUNT=$BYTE_COUNT"
echo "DATASET_COUNT=$DATASET_COUNT"
