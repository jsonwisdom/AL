#!/usr/bin/env bash
# Boss Bre PDF scanner: inventory every known PDF/source and persist sweep learning.
# Doctrine: NO_FAKE_GREEN. This script logs observations only; it never promotes a public claim.

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
JFILE="$ROOT/data/mn_jurisdictions.json"
STATE_DIR="$ROOT/projects/mn-fiscal-replay/boss_bre"
RUNS_DIR="$STATE_DIR/runs"
LEARN_FILE="$STATE_DIR/boss_bre_learning_state.json"
INVENTORY_FILE="$STATE_DIR/boss_bre_pdf_inventory.jsonl"
LATEST_SUMMARY="$STATE_DIR/latest_sweep_summary.json"
UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN_ID="${UTC//[:]/-}"
RUN_DIR="$RUNS_DIR/$RUN_ID"

mkdir -p "$RUN_DIR" "$STATE_DIR"

SCAN_JSONL="$RUN_DIR/pdf_scan.jsonl"
SCAN_MD="$RUN_DIR/pdf_scan.md"
: > "$SCAN_JSONL"

sha256_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  else
    shasum -a 256 "$1" | awk '{print $1}'
  fi
}

json_escape() {
  jq -Rs . <<<"$1"
}

record_json() {
  printf '%s\n' "$1" >> "$SCAN_JSONL"
  printf '%s\n' "$1" >> "$INVENTORY_FILE"
}

scan_repo_pdfs() {
  while IFS= read -r -d '' pdf; do
    rel="${pdf#$ROOT/}"
    size="$(wc -c < "$pdf" | tr -d ' ')"
    hash="$(sha256_file "$pdf")"
    text_status="NOT_ATTEMPTED"
    page_count="UNKNOWN"
    text_chars="0"

    if command -v pdfinfo >/dev/null 2>&1; then
      page_count="$(pdfinfo "$pdf" 2>/dev/null | awk -F: '/^Pages:/ {gsub(/^[ \t]+/, "", $2); print $2; exit}' || true)"
      [ -n "$page_count" ] || page_count="UNKNOWN"
    fi

    if command -v pdftotext >/dev/null 2>&1; then
      tmp="$RUN_DIR/$(basename "$pdf").txt"
      if pdftotext -layout "$pdf" "$tmp" 2>/dev/null; then
        text_status="EXTRACTED"
        text_chars="$(wc -c < "$tmp" | tr -d ' ')"
      else
        text_status="EXTRACT_BLOCKED"
      fi
    fi

    record_json "$(jq -nc \
      --arg utc "$UTC" \
      --arg kind "repo_pdf" \
      --arg path "$rel" \
      --arg sha256 "$hash" \
      --arg size_bytes "$size" \
      --arg page_count "$page_count" \
      --arg text_status "$text_status" \
      --arg text_chars "$text_chars" \
      '{utc:$utc,kind:$kind,path:$path,sha256:$sha256,size_bytes:($size_bytes|tonumber),page_count:$page_count,text_status:$text_status,text_chars:($text_chars|tonumber),public_content_claim:"BLOCKED",no_fake_green:true}')"
  done < <(find "$ROOT" -type f -iname '*.pdf' -print0 | sort -z)
}

scan_registry_urls() {
  [ -f "$JFILE" ] || return 0
  jq -c '.jurisdictions[]?' "$JFILE" | while IFS= read -r lane; do
    code="$(jq -r '.code' <<<"$lane")"
    name="$(jq -r '.name' <<<"$lane")"
    pdf_url="$(jq -r '.pdf_url // empty' <<<"$lane")"
    outdir="$ROOT/projects/mn-fiscal-replay/live_fetch/$code"
    mkdir -p "$outdir"

    status="SOURCE_URL_MISSING"
    http_status="NA"
    content_type="UNKNOWN"
    content_length="UNKNOWN"
    downloaded_sha256=""
    downloaded_path=""

    if [ -n "$pdf_url" ] && ! grep -q '^TODO_' <<<"$pdf_url"; then
      if command -v curl >/dev/null 2>&1; then
        header_file="$RUN_DIR/${code}_headers.txt"
        body_file="$outdir/source_latest.pdf"
        http_status="$(curl -L --fail --max-time 60 --connect-timeout 20 -w '%{http_code}' -D "$header_file" -o "$body_file.tmp" "$pdf_url" 2>/dev/null || true)"
        if [ -s "$body_file.tmp" ]; then
          mv "$body_file.tmp" "$body_file"
          downloaded_sha256="$(sha256_file "$body_file")"
          downloaded_path="${body_file#$ROOT/}"
          status="FETCHED"
          content_type="$(awk 'tolower($0) ~ /^content-type:/ {print substr($0, index($0,$2)); exit}' "$header_file" | tr -d '\r' || true)"
          content_length="$(wc -c < "$body_file" | tr -d ' ')"
        else
          rm -f "$body_file.tmp"
          status="FETCH_BLOCKED"
        fi
      else
        status="FETCH_BLOCKED_NO_CURL"
      fi
    fi

    printf '%s\n' "$status" > "$outdir/fetch_status.txt"
    [ -n "$downloaded_sha256" ] && printf 'source_latest_sha256=%s\n' "$downloaded_sha256" >> "$outdir/fetch_status.txt"
    [ -n "$downloaded_path" ] && printf 'source_latest_path=%s\n' "$downloaded_path" >> "$outdir/fetch_status.txt"

    record_json "$(jq -nc \
      --arg utc "$UTC" \
      --arg kind "registry_pdf_url" \
      --arg code "$code" \
      --arg name "$name" \
      --arg url "$pdf_url" \
      --arg status "$status" \
      --arg http_status "$http_status" \
      --arg content_type "$content_type" \
      --arg content_length "$content_length" \
      --arg downloaded_sha256 "$downloaded_sha256" \
      --arg downloaded_path "$downloaded_path" \
      '{utc:$utc,kind:$kind,code:$code,name:$name,url:$url,status:$status,http_status:$http_status,content_type:$content_type,content_length:$content_length,downloaded_sha256:$downloaded_sha256,downloaded_path:$downloaded_path,public_content_claim:"BLOCKED",no_fake_green:true}')"
  done
}

scan_repo_pdfs
scan_registry_urls

TOTAL_RECORDS="$(wc -l < "$SCAN_JSONL" | tr -d ' ')"
FETCHED="$(jq -sr '[.[] | select(.status=="FETCHED")] | length' "$SCAN_JSONL")"
REPO_PDFS="$(jq -sr '[.[] | select(.kind=="repo_pdf")] | length' "$SCAN_JSONL")"
BLOCKED="$(jq -sr '[.[] | select((.status // "") | test("BLOCKED|MISSING"))] | length' "$SCAN_JSONL")"
EXTRACTED="$(jq -sr '[.[] | select(.text_status=="EXTRACTED")] | length' "$SCAN_JSONL")"

cat > "$LATEST_SUMMARY" <<JSON
{
  "utc": "$UTC",
  "run_id": "$RUN_ID",
  "total_records": $TOTAL_RECORDS,
  "repo_pdfs": $REPO_PDFS,
  "fetched_registry_pdfs": $FETCHED,
  "blocked_or_missing_sources": $BLOCKED,
  "extracted_repo_pdfs": $EXTRACTED,
  "public_content_claim": "BLOCKED",
  "human_review_required": true,
  "no_fake_green": true,
  "scan_jsonl": "${SCAN_JSONL#$ROOT/}",
  "inventory_jsonl": "${INVENTORY_FILE#$ROOT/}"
}
JSON

# Learning state: carry compact observations into the next 15m run.
if [ -f "$LEARN_FILE" ]; then
  PRIOR_RUNS="$(jq -r '.runs_observed // 0' "$LEARN_FILE" 2>/dev/null || echo 0)"
else
  PRIOR_RUNS=0
fi
RUNS_OBSERVED=$((PRIOR_RUNS + 1))

jq -n \
  --arg utc "$UTC" \
  --argjson runs "$RUNS_OBSERVED" \
  --argjson total "$TOTAL_RECORDS" \
  --argjson repo_pdfs "$REPO_PDFS" \
  --argjson fetched "$FETCHED" \
  --argjson blocked "$BLOCKED" \
  --argjson extracted "$EXTRACTED" \
  '{
    updated_utc:$utc,
    runs_observed:$runs,
    last_total_records:$total,
    last_repo_pdfs:$repo_pdfs,
    last_fetched_registry_pdfs:$fetched,
    last_blocked_or_missing_sources:$blocked,
    last_extracted_repo_pdfs:$extracted,
    learned_rules:[
      "Never promote public content claims from scanner output",
      "Prefer registered source_latest.pdf when present",
      "Treat TODO or unreachable pdf_url as FETCH_BLOCKED",
      "Persist hashes so later sweeps can detect source churn",
      "Escalate lanes with changed PDF hashes to forensic worker"
    ],
    next_run_adjustments:{
      prioritize_changed_hashes:true,
      suppress_unchanged_hash_noise:true,
      keep_missing_payload_on_master_issue:true
    },
    public_content_claim:"BLOCKED",
    human_review_required:true,
    no_fake_green:true
  }' > "$LEARN_FILE"

{
  echo "# Boss Bre PDF Scan"
  echo
  echo "UTC: $UTC"
  echo
  echo "- Total records: $TOTAL_RECORDS"
  echo "- Repo PDFs: $REPO_PDFS"
  echo "- Registry PDFs fetched: $FETCHED"
  echo "- Blocked/missing sources: $BLOCKED"
  echo "- Repo PDFs text-extracted: $EXTRACTED"
  echo
  echo '```json'
  cat "$LATEST_SUMMARY"
  echo '```'
  echo
  echo "PUBLIC_CONTENT_CLAIM: BLOCKED"
  echo "HUMAN_REVIEW_REQUIRED: TRUE"
  echo "NO_FAKE_GREEN: ACTIVE"
} > "$SCAN_MD"

echo "=== Boss Bre PDF scanner complete ==="
echo "Summary: ${LATEST_SUMMARY#$ROOT/}"
echo "Learning: ${LEARN_FILE#$ROOT/}"
echo "Run log: ${SCAN_JSONL#$ROOT/}"
