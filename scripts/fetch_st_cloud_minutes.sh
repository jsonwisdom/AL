#!/usr/bin/env bash
set -euo pipefail

# Fetch St. Cloud City Council minutes/proceedings from an explicit URL map.
#
# Authority: none.
# This script does not infer civic findings. It only acquires source files and
# records fetch status for replay.
#
# Usage:
#   bash scripts/fetch_st_cloud_minutes.sh data/saint_cloud/st_cloud_minutes_urls.tsv data/saint_cloud
#
# TSV columns:
#   meeting_date<TAB>source_id<TAB>url

URL_MAP="${1:-data/saint_cloud/st_cloud_minutes_urls.tsv}"
OUT_DIR="${2:-data/saint_cloud}"
MANIFEST_OUT="${OUT_DIR}/fetch_manifest.jsonl"

mkdir -p "${OUT_DIR}"
: > "${MANIFEST_OUT}"

if [[ ! -f "${URL_MAP}" ]]; then
  echo "URL map not found: ${URL_MAP}" >&2
  echo "Create a TSV with: meeting_date<TAB>source_id<TAB>url" >&2
  exit 2
fi

while IFS=$'\t' read -r meeting_date source_id url; do
  [[ -z "${meeting_date:-}" ]] && continue
  [[ "${meeting_date}" =~ ^# ]] && continue

  if [[ -z "${source_id:-}" || -z "${url:-}" ]]; then
    echo "Skipping malformed row for meeting_date=${meeting_date}" >&2
    continue
  fi

  pdf_path="${OUT_DIR}/${source_id}.pdf"
  txt_path="${OUT_DIR}/${source_id}.txt"
  status="FETCH_FAILED"
  http_code="000"

  http_code=$(curl -L --fail --silent --show-error --output "${pdf_path}" --write-out "%{http_code}" "${url}" || true)

  if [[ "${http_code}" == "200" && -s "${pdf_path}" ]]; then
    status="FETCHED"
    if command -v pdftotext >/dev/null 2>&1; then
      # -layout preserves rough page text; form-feed page separators are retained by poppler.
      pdftotext -layout "${pdf_path}" "${txt_path}" || status="FETCHED_TEXT_EXTRACTION_FAILED"
    else
      status="FETCHED_TEXT_EXTRACTION_SKIPPED"
    fi
  else
    rm -f "${pdf_path}" "${txt_path}"
  fi

  pdf_sha="null"
  txt_sha="null"
  if [[ -f "${pdf_path}" ]]; then
    pdf_sha="sha256:$(sha256sum "${pdf_path}" | awk '{print $1}')"
  fi
  if [[ -f "${txt_path}" ]]; then
    txt_sha="sha256:$(sha256sum "${txt_path}" | awk '{print $1}')"
  fi

  python3 - <<PY >> "${MANIFEST_OUT}"
import json
print(json.dumps({
  "meeting_date": ${meeting_date@Q},
  "source_id": ${source_id@Q},
  "source_url": ${url@Q},
  "status": ${status@Q},
  "http_code": ${http_code@Q},
  "pdf_path": ${pdf_path@Q},
  "txt_path": ${txt_path@Q},
  "pdf_sha256": ${pdf_sha@Q},
  "txt_sha256": ${txt_sha@Q},
}, sort_keys=True))
PY

done < "${URL_MAP}"

echo "Wrote fetch manifest: ${MANIFEST_OUT}"
