#!/usr/bin/env bash
# PR #260 Replay Verifier
# Authority: false | Merge permission: false
# Fetches Item/2145 from the authoritative St. Cloud source, runs ingestion,
# and compares output to the operator-reported claimed hash.
# Fails closed on any mismatch.

set -euo pipefail

COMMIT_HASH="${COMMIT_HASH:-67e9cb8eb48899e000be07cf08695a5ae830f457}"
SOURCE_ITEM="${SOURCE_ITEM:-2145}"
SOURCE_ID="${SOURCE_ID:-2025-03-10_minutes}"
MEETING_DATE="${MEETING_DATE:-2025-03-10}"
OFFICIAL_URL="${OFFICIAL_URL:-https://ci.stcloud.mn.us/ArchiveCenter/ViewFile/Item/${SOURCE_ITEM}}"
CLAIMED_CSV_SHA256="${CLAIMED_CSV_SHA256:-d2d412ee452aff49c0eb75adafaac4986b4eb23db3e672054f594877341e6fde}"

fail() {
  echo "ERROR: $*" >&2
  exit 2
}

[[ "${COMMIT_HASH}" =~ ^[0-9a-f]{40}$ ]] || fail "COMMIT_HASH must be a 40-character lowercase hex commit hash"
[[ "${MEETING_DATE}" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || fail "MEETING_DATE must be YYYY-MM-DD"
[[ "${CLAIMED_CSV_SHA256}" =~ ^[0-9a-f]{64}$ ]] || fail "CLAIMED_CSV_SHA256 must be 64 lowercase hex characters"
[[ "${OFFICIAL_URL}" =~ ^https://ci\.stcloud\.mn\.us/ArchiveCenter/ViewFile/Item/[0-9]+$ ]] || fail "OFFICIAL_URL must be canonical St. Cloud ArchiveCenter ViewFile URL"

EXPECTED_DISPLAY_DATE=$(python3 - <<PY
from datetime import datetime
print(datetime.strptime(${MEETING_DATE@Q}, "%Y-%m-%d").strftime("%B %-d, %Y"))
PY
)

WORK_DIR=$(mktemp -d)
trap 'rm -rf "${WORK_DIR}"' EXIT

PDF_PATH="${WORK_DIR}/${SOURCE_ID}.pdf"
TEXT_PATH="${WORK_DIR}/${SOURCE_ID}.txt"
INPUT_DIR="${WORK_DIR}/input"
OUTPUT_CSV="${WORK_DIR}/${SOURCE_ID}_contradiction_rows.csv"
MANIFEST="${WORK_DIR}/source_manifest.json"
CHAIN_CUSTODY="${WORK_DIR}/chain_of_custody.json"

mkdir -p "${INPUT_DIR}"

echo "PR #260 Replay Verifier"
echo "Source: ${OFFICIAL_URL}"
echo "Meeting date: ${MEETING_DATE} (${EXPECTED_DISPLAY_DATE})"
echo "Claimed CSV SHA256: ${CLAIMED_CSV_SHA256}"
echo "Authority: false"
echo "Merge permission: false"
echo

echo "Fetching source PDF..."
http_code=$(curl -L --fail --silent --show-error --output "${PDF_PATH}" --write-out "%{http_code}" "${OFFICIAL_URL}" || true)
[[ "${http_code}" == "200" ]] || fail "PDF fetch failed with HTTP status ${http_code}"
[[ -s "${PDF_PATH}" ]] || fail "PDF download failed or empty"

PDF_SHA256=$(sha256sum "${PDF_PATH}" | awk '{print $1}')
echo "PDF SHA256: ${PDF_SHA256}"

command -v pdftotext >/dev/null 2>&1 || fail "pdftotext is required"

FIRST_PAGE=$(pdftotext -f 1 -l 1 "${PDF_PATH}" -)
printf '%s' "${FIRST_PAGE}" | grep -qi "${EXPECTED_DISPLAY_DATE}" \
  || fail "identity gate failed: expected date '${EXPECTED_DISPLAY_DATE}' not found on first page"

printf '%s' "${FIRST_PAGE}" | grep -Eiq "St[.]?[[:space:]]*Cloud.*City[[:space:]]+Council|City[[:space:]]+Council.*St[.]?[[:space:]]*Cloud|CITY OF ST[.]?[[:space:]]*CLOUD PROCEEDINGS" \
  || fail "identity gate failed: St. Cloud City Council / Proceedings marker not found"

printf '%s' "${FIRST_PAGE}" | grep -Eiq "Minutes|Proceedings" \
  || fail "identity gate failed: Minutes/Proceedings marker not found"

if printf '%s' "${FIRST_PAGE}" | grep -Eiq "^[[:space:]]*Resolution[[:space:]]+No\."; then
  fail "identity gate failed: first page appears to be a resolution, not minutes/proceedings"
fi

echo "Identity gate passed."

pdftotext -layout "${PDF_PATH}" "${TEXT_PATH}"
[[ -s "${TEXT_PATH}" ]] || fail "text extraction produced empty output"
TEXT_SHA256=$(sha256sum "${TEXT_PATH}" | awk '{print $1}')
echo "Text SHA256: ${TEXT_SHA256}"

cp "${TEXT_PATH}" "${INPUT_DIR}/${SOURCE_ID}.txt"
cat > "${MANIFEST}" <<EOF
{
  "sources": [
    {
      "meeting_date": "${MEETING_DATE}",
      "source_id": "${SOURCE_ID}",
      "source_url": "${OFFICIAL_URL}",
      "local_path": "${INPUT_DIR}/${SOURCE_ID}.txt",
      "pdf_sha256": "sha256:${PDF_SHA256}",
      "txt_sha256": "sha256:${TEXT_SHA256}"
    }
  ]
}
EOF

echo "Running batch ingest..."
python3 scripts/saint_cloud_batch_ingest_v0_1.py \
  --input-dir "${INPUT_DIR}" \
  --manifest "${MANIFEST}" \
  --commit-hash "${COMMIT_HASH}" \
  --output "${OUTPUT_CSV}" > "${CHAIN_CUSTODY}"

[[ -s "${OUTPUT_CSV}" ]] || fail "output CSV was not produced"
OUTPUT_SHA256=$(sha256sum "${OUTPUT_CSV}" | awk '{print $1}')
ROW_COUNT=$(python3 - <<PY
import csv
with open(${OUTPUT_CSV@Q}, newline='', encoding='utf-8') as f:
    print(max(sum(1 for _ in csv.DictReader(f)), 0))
PY
)

echo "Rows emitted: ${ROW_COUNT}"
echo "Output CSV SHA256: ${OUTPUT_SHA256}"

if [[ "${OUTPUT_SHA256}" != "${CLAIMED_CSV_SHA256}" ]]; then
  echo
  echo "REPLAY FAILED: output hash mismatch" >&2
  echo "Expected: ${CLAIMED_CSV_SHA256}" >&2
  echo "Actual:   ${OUTPUT_SHA256}" >&2
  echo "This means the claimed ingest output is not reproducible from the authoritative source under this commit." >&2
  exit 1
fi

echo
cat <<EOF
{
  "replay_result": "MATCH",
  "authority": false,
  "merge_permission": false,
  "commit_hash": "${COMMIT_HASH}",
  "source_url": "${OFFICIAL_URL}",
  "meeting_date": "${MEETING_DATE}",
  "expected_display_date": "${EXPECTED_DISPLAY_DATE}",
  "pdf_sha256": "sha256:${PDF_SHA256}",
  "extracted_text_sha256": "sha256:${TEXT_SHA256}",
  "output_csv_sha256": "${OUTPUT_SHA256}",
  "claimed_csv_sha256": "${CLAIMED_CSV_SHA256}",
  "row_count": ${ROW_COUNT}
}
EOF

echo
echo "REPLAY VERIFICATION PASSED: output matches claimed hash."
