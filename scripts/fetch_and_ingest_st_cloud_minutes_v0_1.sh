#!/usr/bin/env bash
# PR #260 | Saint Cloud lineage membrane v0.1
# Authority: false | Merge permission: false
# Empirical replay harness only. This script fetches operator-supplied public source bytes,
# records custody, and runs the infrastructure-only row emitter.

set -euo pipefail

COMMIT_HASH="${COMMIT_HASH:-aa0380b38a0c7777e5f0a80fb38cc4e86786c5cb}"
OFFICIAL_URL="${OFFICIAL_URL:-}"
SOURCE_ID="${SOURCE_ID:-2025-03-10_minutes}"
MEETING_DATE="${MEETING_DATE:-2025-03-10}"
PDF_DIR="${PDF_DIR:-data/saint_cloud}"
OUTPUT_DIR="${OUTPUT_DIR:-outputs/saint_cloud}"
MANIFEST="${PDF_DIR}/fetch_manifest.jsonl"
URL_MAP="${PDF_DIR}/st_cloud_minutes_urls.tsv"
OUTPUT_CSV="${OUTPUT_DIR}/${SOURCE_ID}_contradiction_rows.csv"

fail() {
  echo "ERROR: $*" >&2
  exit 2
}

case "${OFFICIAL_URL}" in
  ""|*REPLACE*|*example.com*|*Item/1234*)
    fail "OFFICIAL_URL must be set to the real St. Cloud ArchiveCenter/ViewFile URL. Refusing placeholder fetch."
    ;;
esac

[[ "${OFFICIAL_URL}" =~ ^https:// ]] || fail "OFFICIAL_URL must be https://"
[[ "${COMMIT_HASH}" =~ ^[0-9a-f]{40}$ ]] || fail "COMMIT_HASH must be a 40-character lowercase hex commit hash"

mkdir -p "${PDF_DIR}" "${OUTPUT_DIR}"

PDF_PATH="${PDF_DIR}/${SOURCE_ID}.pdf"
TEXT_PATH="${PDF_DIR}/${SOURCE_ID}.txt"

printf '%s\t%s\t%s\n' "${MEETING_DATE}" "${SOURCE_ID}" "${OFFICIAL_URL}" > "${URL_MAP}"

{
  printf '{"event":"fetch_start","meeting_date":"%s","source_id":"%s","source_url":"%s","timestamp":"%s","authority":false,"merge_permission":false}\n' \
    "${MEETING_DATE}" "${SOURCE_ID}" "${OFFICIAL_URL}" "$(date -Iseconds)"
} >> "${MANIFEST}"

http_code=$(curl -L --fail --silent --show-error --output "${PDF_PATH}" --write-out "%{http_code}" "${OFFICIAL_URL}" || true)
[[ "${http_code}" == "200" ]] || fail "fetch failed with HTTP status ${http_code}"
[[ -s "${PDF_PATH}" ]] || fail "downloaded PDF is empty: ${PDF_PATH}"

PDF_SHA256="sha256:$(sha256sum "${PDF_PATH}" | awk '{print $1}')"

command -v pdftotext >/dev/null 2>&1 || fail "pdftotext is required for replay text extraction"
pdftotext -layout "${PDF_PATH}" "${TEXT_PATH}"
[[ -s "${TEXT_PATH}" ]] || fail "text extraction produced empty file: ${TEXT_PATH}"
TEXT_SHA256="sha256:$(sha256sum "${TEXT_PATH}" | awk '{print $1}')"

{
  printf '{"event":"fetch_complete","meeting_date":"%s","source_id":"%s","source_url":"%s","http_code":"%s","pdf_path":"%s","txt_path":"%s","pdf_sha256":"%s","txt_sha256":"%s","timestamp":"%s","authority":false,"merge_permission":false}\n' \
    "${MEETING_DATE}" "${SOURCE_ID}" "${OFFICIAL_URL}" "${http_code}" "${PDF_PATH}" "${TEXT_PATH}" "${PDF_SHA256}" "${TEXT_SHA256}" "$(date -Iseconds)"
} >> "${MANIFEST}"

python3 scripts/saint_cloud_batch_ingest_v0_1.py \
  --input-dir "${PDF_DIR}" \
  --manifest data/saint_cloud/source_manifest.json \
  --commit-hash "${COMMIT_HASH}" \
  --output "${OUTPUT_CSV}"

CUSTODY_PATH="${OUTPUT_CSV%.csv}.chain_of_custody.json"
INGEST_RECEIPT="${OUTPUT_DIR}/${SOURCE_ID}_ingest_receipt.json"

cat > "${INGEST_RECEIPT}" <<EOF
{
  "authority": false,
  "merge_permission": false,
  "posture": "LINEAGE_MEMBRANE_EXTRACTION_SCAFFOLD",
  "meeting_date": "${MEETING_DATE}",
  "source_id": "${SOURCE_ID}",
  "source_url": "${OFFICIAL_URL}",
  "commit_hash": "${COMMIT_HASH}",
  "source_pdf": "${PDF_PATH}",
  "source_text": "${TEXT_PATH}",
  "pdf_sha256": "${PDF_SHA256}",
  "text_sha256": "${TEXT_SHA256}",
  "output_csv": "${OUTPUT_CSV}",
  "chain_of_custody": "${CUSTODY_PATH}",
  "timestamp": "$(date -Iseconds)"
}
EOF

echo "Ingestion complete."
echo "PDF: ${PDF_PATH} ${PDF_SHA256}"
echo "Text: ${TEXT_PATH} ${TEXT_SHA256}"
echo "Rows: ${OUTPUT_CSV}"
echo "Custody: ${CUSTODY_PATH}"
echo "Receipt: ${INGEST_RECEIPT}"
