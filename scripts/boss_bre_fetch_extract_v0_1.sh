#!/usr/bin/env bash
# Boss Bre fetch/extract/rotate v0.1
# Purpose: ingest official public fiscal PDFs, hash them, extract text, rotate baseline/live state, and emit receipts.
# Doctrine: NO_FAKE_GREEN. This script never promotes PUBLIC_CONTENT_CLAIM.

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
JFILE="${JFILE:-$ROOT/data/mn_jurisdictions.json}"
TARGET_CODE="${JURISDICTION:-${1:-ALL}}"
UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

if [ ! -f "$JFILE" ]; then
  echo "BLOCKED_REASON: missing jurisdiction registry: $JFILE"
  exit 1
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "BLOCKED_REASON: jq is required"
  exit 1
fi
if ! command -v curl >/dev/null 2>&1; then
  echo "BLOCKED_REASON: curl is required"
  exit 1
fi

sha_file() {
  if [ -f "$1" ]; then sha256sum "$1" | awk '{print $1}'; else echo ""; fi
}

emit_receipt() {
  local outdir="$1" code="$2" name="$3" url="$4" status="$5" reason="$6" latest_hash="$7" previous_hash="$8" text_hash="$9" drift="${10}" receipt="$outdir/boss_bre_fetch_extract_receipt.json"
  jq -n \
    --arg utc "$UTC" \
    --arg code "$code" \
    --arg name "$name" \
    --arg url "$url" \
    --arg status "$status" \
    --arg reason "$reason" \
    --arg latest_hash "$latest_hash" \
    --arg previous_hash "$previous_hash" \
    --arg text_hash "$text_hash" \
    --arg drift "$drift" \
    '{artifact:"boss_bre_fetch_extract_receipt.json",version:"0.1",generated_utc:$utc,jurisdiction:$code,name:$name,source_url:$url,status:$status,blocked_reason:$reason,source_latest_sha256:$latest_hash,source_previous_sha256:$previous_hash,source_latest_text_sha256:$text_hash,drift_status:$drift,public_content_claim:"BLOCKED",human_review_required:true,no_fake_green:true,outputs:{source_latest_pdf:"source_latest.pdf",source_latest_text:"source_latest.txt",source_previous_pdf:"source_previous.pdf",source_previous_text:"source_previous.txt"}}' \
    > "$receipt"
}

process_lane() {
  local lane="$1" code name url outdir tmp_pdf tmp_headers latest_pdf previous_pdf latest_txt previous_txt latest_hash previous_hash text_hash status reason drift_status
  code="$(jq -r '.code' <<<"$lane")"
  name="$(jq -r '.name' <<<"$lane")"
  url="$(jq -r '.pdf_url // empty' <<<"$lane")"
  outdir="$ROOT/projects/mn-fiscal-replay/live_fetch/$code"
  mkdir -p "$outdir"

  tmp_pdf="$outdir/source_latest.pdf.tmp"
  tmp_headers="$outdir/source_latest.headers.tmp"
  latest_pdf="$outdir/source_latest.pdf"
  previous_pdf="$outdir/source_previous.pdf"
  latest_txt="$outdir/source_latest.txt"
  previous_txt="$outdir/source_previous.txt"
  status="FETCH_BLOCKED"
  reason=""
  drift_status="UNKNOWN"
  latest_hash=""
  previous_hash="$(sha_file "$latest_pdf")"
  text_hash=""

  echo "=== Boss Bre ingest: $code | $name ==="

  if [ -z "$url" ] || echo "$url" | grep -q '^TODO_'; then
    reason="SOURCE_URL_MISSING_OR_TODO"
    printf 'FETCH_BLOCKED: %s\n' "$reason" > "$outdir/fetch_status.txt"
    emit_receipt "$outdir" "$code" "$name" "$url" "$status" "$reason" "" "$previous_hash" "" "NO_SOURCE"
    return 0
  fi

  rm -f "$tmp_pdf" "$tmp_headers"
  if ! curl -L --fail --max-time 90 --connect-timeout 20 -D "$tmp_headers" -o "$tmp_pdf" "$url"; then
    reason="CURL_FETCH_FAILED"
    rm -f "$tmp_pdf"
    printf 'FETCH_BLOCKED: %s\nsource_url=%s\n' "$reason" "$url" > "$outdir/fetch_status.txt"
    emit_receipt "$outdir" "$code" "$name" "$url" "$status" "$reason" "" "$previous_hash" "" "FETCH_FAILED"
    return 0
  fi

  if [ ! -s "$tmp_pdf" ]; then
    reason="EMPTY_DOWNLOAD"
    rm -f "$tmp_pdf"
    printf 'FETCH_BLOCKED: %s\nsource_url=%s\n' "$reason" "$url" > "$outdir/fetch_status.txt"
    emit_receipt "$outdir" "$code" "$name" "$url" "$status" "$reason" "" "$previous_hash" "" "EMPTY_DOWNLOAD"
    return 0
  fi

  latest_hash="$(sha_file "$tmp_pdf")"

  if [ -f "$latest_pdf" ]; then
    current_hash="$(sha_file "$latest_pdf")"
    if [ "$latest_hash" = "$current_hash" ]; then
      drift_status="UNCHANGED_SOURCE_HASH"
    else
      cp "$latest_pdf" "$previous_pdf"
      [ -f "$latest_txt" ] && cp "$latest_txt" "$previous_txt" || true
      previous_hash="$current_hash"
      drift_status="SOURCE_HASH_CHANGED"
    fi
  else
    drift_status="BASELINE_ESTABLISHED"
  fi

  mv "$tmp_pdf" "$latest_pdf"

  if command -v pdftotext >/dev/null 2>&1; then
    if pdftotext -layout "$latest_pdf" "$latest_txt" 2>/dev/null; then
      text_hash="$(sha_file "$latest_txt")"
      status="FETCH_EXTRACT_COMPLETE"
      reason=""
    else
      status="FETCH_COMPLETE_EXTRACT_BLOCKED"
      reason="PDFTOTEXT_FAILED"
      : > "$latest_txt"
    fi
  else
    status="FETCH_COMPLETE_EXTRACT_BLOCKED"
    reason="PDFTOTEXT_MISSING"
    : > "$latest_txt"
  fi

  # If prior text exists, provide worker-compatible baseline/live hints.
  if [ -s "$previous_txt" ] && [ -s "$latest_txt" ]; then
    cp "$previous_txt" "$outdir/baseline_normalized.txt"
    cp "$latest_txt" "$outdir/live_normalized.txt"
  fi

  cat > "$outdir/fetch_status.txt" <<EOF
status=$status
source_url=$url
source_latest_sha256=$latest_hash
source_previous_sha256=$previous_hash
source_latest_text_sha256=$text_hash
drift_status=$drift_status
public_content_claim=BLOCKED
human_review_required=TRUE
no_fake_green=TRUE
EOF

  emit_receipt "$outdir" "$code" "$name" "$url" "$status" "$reason" "$latest_hash" "$previous_hash" "$text_hash" "$drift_status"
}

if [ "$TARGET_CODE" = "ALL" ]; then
  jq -c '.jurisdictions[]?' "$JFILE" | while IFS= read -r lane; do
    process_lane "$lane"
  done
else
  lane="$(jq -c --arg code "$TARGET_CODE" '.jurisdictions[]? | select(.code==$code)' "$JFILE" | head -n 1)"
  if [ -z "$lane" ]; then
    echo "BLOCKED_REASON: jurisdiction not found: $TARGET_CODE"
    exit 1
  fi
  process_lane "$lane"
fi

echo "=== Boss Bre fetch/extract complete ==="
echo "PUBLIC_CONTENT_CLAIM: BLOCKED"
echo "HUMAN_REVIEW_REQUIRED: TRUE"
echo "NO_FAKE_GREEN: ACTIVE"
