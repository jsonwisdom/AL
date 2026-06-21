#!/usr/bin/env bash
# Boss Bre lead receipt builder v0.1
# Purpose: enrich anomaly leads with source PDF/text hashes and emit storefront-safe receipt objects.
# Doctrine: NO_FAKE_GREEN. Lead receipts are ANOMALY_LEAD_ONLY and BLOCKED_PENDING_HUMAN_REVIEW.

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
STATE_DIR="$ROOT/projects/mn-fiscal-replay/boss_bre"
LEADS_FILE="${LEADS_FILE:-$STATE_DIR/latest_anomaly_leads.jsonl}"
OUT_JSONL="$STATE_DIR/latest_lead_receipts.jsonl"
MANIFEST="$STATE_DIR/latest_lead_receipt_manifest.json"
JFILE="$ROOT/data/mn_jurisdictions.json"
UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

mkdir -p "$STATE_DIR"
: > "$OUT_JSONL"

sha_file() {
  if [ -f "$1" ]; then sha256sum "$1" | awk '{print $1}'; else echo ""; fi
}

json_get_or_empty() {
  jq -r "$1 // empty" 2>/dev/null || true
}

severity_rank() {
  case "$1" in
    HIGH) echo 3 ;;
    MEDIUM) echo 2 ;;
    LOW) echo 1 ;;
    *) echo 0 ;;
  esac
}

normalize_severity() {
  local severity="$1" label="$2" evidence="$3"
  case "$severity" in HIGH|MEDIUM|LOW) echo "$severity"; return 0 ;; esac
  if echo "$label $evidence" | grep -Eiq 'fraud|CMS|withhold|withheld|Medicaid|denied|disallowance|deficit|shortfall|variance'; then
    echo "HIGH"
  elif echo "$label $evidence" | grep -Eiq '\$[0-9,]+|billion|million|percent|reduction|decrease|increase|forecast'; then
    echo "MEDIUM"
  else
    echo "LOW"
  fi
}

write_empty_manifest() {
  local reason="$1"
  jq -n \
    --arg utc "$UTC" \
    --arg reason "$reason" \
    --arg output "${OUT_JSONL#$ROOT/}" \
    '{artifact:"latest_lead_receipt_manifest.json",version:"0.1",generated_utc:$utc,status:"NO_LEAD_RECEIPTS_EMITTED",blocked_reason:$reason,lead_receipt_count:0,high_count:0,medium_count:0,low_count:0,output_jsonl:$output,output_sha256:"",public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",claim_type:"ANOMALY_LEAD_ONLY",human_review_required:true,no_fake_green:true}' \
    > "$MANIFEST"
}

if [ ! -f "$LEADS_FILE" ]; then
  write_empty_manifest "ANOMALY_LEADS_FILE_MISSING"
  echo "LEAD_RECEIPTS_BLOCKED: ANOMALY_LEADS_FILE_MISSING"
  exit 0
fi

if [ ! -s "$LEADS_FILE" ]; then
  write_empty_manifest "ANOMALY_LEADS_EMPTY"
  echo "LEAD_RECEIPTS_EMPTY: no anomaly leads"
  exit 0
fi

index=0
while IFS= read -r lead; do
  [ -n "$lead" ] || continue
  if ! echo "$lead" | jq -e . >/dev/null 2>&1; then
    continue
  fi

  index=$((index + 1))
  lane="$(echo "$lead" | jq -r '.lane // "GLOBAL"')"
  rule_id="$(echo "$lead" | jq -r '.rule_id // "UNKNOWN_RULE"')"
  severity_raw="$(echo "$lead" | jq -r '.severity // "UNKNOWN"')"
  label="$(echo "$lead" | jq -r '.label // "UNKNOWN_LABEL"')"
  evidence="$(echo "$lead" | jq -r '.evidence_excerpt // ""')"
  source_path="$(echo "$lead" | jq -r '.source_path // ""')"
  severity="$(normalize_severity "$severity_raw" "$label" "$evidence")"

  lane_dir="$ROOT/projects/mn-fiscal-replay/live_fetch/$lane"
  fetch_receipt="$lane_dir/boss_bre_fetch_extract_receipt.json"
  source_pdf_url=""
  source_pdf_sha256=""
  source_text_sha256=""
  source_previous_sha256=""
  drift_status="UNKNOWN"

  if [ -f "$fetch_receipt" ]; then
    source_pdf_url="$(jq -r '.source_url // empty' "$fetch_receipt")"
    source_pdf_sha256="$(jq -r '.source_latest_sha256 // empty' "$fetch_receipt")"
    source_text_sha256="$(jq -r '.source_latest_text_sha256 // empty' "$fetch_receipt")"
    source_previous_sha256="$(jq -r '.source_previous_sha256 // empty' "$fetch_receipt")"
    drift_status="$(jq -r '.drift_status // "UNKNOWN"' "$fetch_receipt")"
  elif [ -f "$JFILE" ]; then
    source_pdf_url="$(jq -r --arg lane "$lane" '.jurisdictions[]? | select(.code==$lane) | .pdf_url // empty' "$JFILE" | head -n 1)"
  fi

  if [ -z "$source_pdf_sha256" ] && [ -f "$lane_dir/source_latest.pdf" ]; then
    source_pdf_sha256="$(sha_file "$lane_dir/source_latest.pdf")"
  fi
  if [ -z "$source_text_sha256" ] && [ -f "$lane_dir/source_latest.txt" ]; then
    source_text_sha256="$(sha_file "$lane_dir/source_latest.txt")"
  fi

  lead_id_material="$lane|$rule_id|$severity|$source_pdf_sha256|$source_text_sha256|$evidence"
  lead_id="$(printf '%s' "$lead_id_material" | sha256sum | awk '{print $1}')"

  jq -n \
    --arg utc "$UTC" \
    --arg lead_id "sha256:$lead_id" \
    --arg lane "$lane" \
    --arg source_path "$source_path" \
    --arg source_pdf_url "$source_pdf_url" \
    --arg source_pdf_sha256 "$source_pdf_sha256" \
    --arg source_text_sha256 "$source_text_sha256" \
    --arg source_previous_sha256 "$source_previous_sha256" \
    --arg drift_status "$drift_status" \
    --arg rule_id "$rule_id" \
    --arg severity "$severity" \
    --arg label "$label" \
    --arg evidence "$evidence" \
    '{artifact:"boss_bre_lead_receipt",version:"0.1",generated_utc:$utc,lead_id:$lead_id,jurisdiction:$lane,source_path:$source_path,source_pdf_url:$source_pdf_url,source_pdf_sha256:$source_pdf_sha256,source_text_sha256:$source_text_sha256,source_previous_sha256:$source_previous_sha256,drift_status:$drift_status,rule_id:$rule_id,severity:$severity,label:$label,evidence_excerpt:$evidence,claim_status:"ANOMALY_LEAD_ONLY",public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",human_review_required:true,no_fake_green:true}' \
    >> "$OUT_JSONL"
done < "$LEADS_FILE"

COUNT="$(wc -l < "$OUT_JSONL" | tr -d ' ')"
HIGH="$(jq -sr '[.[] | select(.severity=="HIGH")] | length' "$OUT_JSONL")"
MEDIUM="$(jq -sr '[.[] | select(.severity=="MEDIUM")] | length' "$OUT_JSONL")"
LOW="$(jq -sr '[.[] | select(.severity=="LOW")] | length' "$OUT_JSONL")"
UNIQUE_LANES="$(jq -sr '[.[].jurisdiction] | unique | length' "$OUT_JSONL")"
OUT_HASH="$(sha_file "$OUT_JSONL")"

jq -n \
  --arg utc "$UTC" \
  --arg output "${OUT_JSONL#$ROOT/}" \
  --arg output_sha256 "$OUT_HASH" \
  --argjson count "$COUNT" \
  --argjson high "$HIGH" \
  --argjson medium "$MEDIUM" \
  --argjson low "$LOW" \
  --argjson lanes "$UNIQUE_LANES" \
  '{artifact:"latest_lead_receipt_manifest.json",version:"0.1",generated_utc:$utc,status:"LEAD_RECEIPTS_EMITTED",lead_receipt_count:$count,high_count:$high,medium_count:$medium,low_count:$low,unique_lanes:$lanes,output_jsonl:$output,output_sha256:$output_sha256,public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",claim_type:"ANOMALY_LEAD_ONLY",human_review_required:true,no_fake_green:true}' \
  > "$MANIFEST"

echo "=== Boss Bre lead receipt builder complete ==="
echo "Lead receipts: $COUNT"
echo "High: $HIGH Medium: $MEDIUM Low: $LOW"
echo "Output: $OUT_JSONL"
echo "Manifest: $MANIFEST"
echo "PUBLIC_CONTENT_CLAIM: BLOCKED_PENDING_HUMAN_REVIEW"
echo "NO_FAKE_GREEN: ACTIVE"
