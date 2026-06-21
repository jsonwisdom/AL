#!/usr/bin/env bash
# Boss Bre rule tuning report v0.1
# Proposal-only: reads lead receipts and proposes tuning actions. Does not mutate live rules.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
STATE="$ROOT/projects/mn-fiscal-replay/boss_bre"
CONFIG="$ROOT/data/boss_bre_rule_tuning_v0_1.json"
RULES="$ROOT/data/boss_bre_anomaly_rules.json"
LEADS="${LEADS:-$STATE/latest_lead_receipts.jsonl}"
OUT_JSONL="$STATE/latest_rule_tuning_proposals.jsonl"
OUT_MANIFEST="$STATE/latest_rule_tuning_manifest.json"
UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

mkdir -p "$STATE"
: > "$OUT_JSONL"

sha_file() {
  if [ -f "$1" ]; then sha256sum "$1" | awk '{print $1}'; else echo ""; fi
}

write_blocked() {
  local reason="$1"
  jq -n \
    --arg utc "$UTC" \
    --arg reason "$reason" \
    '{artifact:"latest_rule_tuning_manifest.json",version:"0.1",generated_utc:$utc,status:"RULE_TUNING_BLOCKED",blocked_reason:$reason,proposal_count:0,public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",claim_type:"RULE_TUNING_PROPOSAL_ONLY",human_review_required:true,no_fake_green:true}' \
    > "$OUT_MANIFEST"
  echo "RULE_TUNING_BLOCKED: $reason"
}

if [ ! -f "$CONFIG" ]; then
  write_blocked "TUNING_CONFIG_MISSING"
  exit 0
fi
if [ ! -f "$RULES" ]; then
  write_blocked "ANOMALY_RULES_MISSING"
  exit 0
fi
if [ ! -s "$LEADS" ]; then
  write_blocked "LEAD_RECEIPTS_MISSING_OR_EMPTY"
  exit 0
fi

classify_proposal() {
  local severity="$1" label="$2" evidence="$3"
  local text="$label $evidence"
  if echo "$text" | grep -Eiq 'page header|table of contents|contents|appendix|source:|accessed|OCR|layout'; then
    echo "SUPPRESS_NOISE"
  elif echo "$text" | grep -Eiq 'fraud|CMS|Medicaid|withhold|withheld|denied|disallowance|deficit|shortfall|variance'; then
    [ "$severity" = "HIGH" ] && echo "REQUIRE_HUMAN_REVIEW" || echo "PROMOTE_TO_HIGH"
  elif echo "$text" | grep -Eiq 'million|billion|forecast|reduction|decrease|increase|reserve|debt service'; then
    [ "$severity" = "LOW" ] && echo "DEMOTE_TO_LOW" || echo "DEMOTE_TO_MEDIUM"
  else
    echo "REQUIRE_HUMAN_REVIEW"
  fi
}

while IFS= read -r lead; do
  [ -n "$lead" ] || continue
  if ! echo "$lead" | jq -e . >/dev/null 2>&1; then
    continue
  fi
  jurisdiction="$(echo "$lead" | jq -r '.jurisdiction // "UNKNOWN"')"
  rule_id="$(echo "$lead" | jq -r '.rule_id // "UNKNOWN_RULE"')"
  severity="$(echo "$lead" | jq -r '.severity // "UNKNOWN"')"
  label="$(echo "$lead" | jq -r '.label // "UNKNOWN_LABEL"')"
  evidence="$(echo "$lead" | jq -r '.evidence_excerpt // ""')"
  source_pdf_sha="$(echo "$lead" | jq -r '.source_pdf_sha256 // ""')"
  source_text_sha="$(echo "$lead" | jq -r '.source_text_sha256 // ""')"
  proposal_class="$(classify_proposal "$severity" "$label" "$evidence")"
  proposal_id="sha256:$(printf '%s|%s|%s|%s|%s' "$jurisdiction" "$rule_id" "$severity" "$proposal_class" "$evidence" | sha256sum | awk '{print $1}')"

  jq -n \
    --arg utc "$UTC" \
    --arg proposal_id "$proposal_id" \
    --arg jurisdiction "$jurisdiction" \
    --arg rule_id "$rule_id" \
    --arg severity "$severity" \
    --arg proposal_class "$proposal_class" \
    --arg label "$label" \
    --arg evidence "$evidence" \
    --arg source_pdf_sha "$source_pdf_sha" \
    --arg source_text_sha "$source_text_sha" \
    '{artifact:"boss_bre_rule_tuning_proposal",version:"0.1",generated_utc:$utc,proposal_id:$proposal_id,jurisdiction:$jurisdiction,rule_id:$rule_id,current_severity:$severity,proposal_class:$proposal_class,label:$label,evidence_excerpt:$evidence,source_pdf_sha256:$source_pdf_sha,source_text_sha256:$source_text_sha,mutates_live_rules:false,requires_human_review_before_patch:true,public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",claim_type:"RULE_TUNING_PROPOSAL_ONLY",human_review_required:true,no_fake_green:true}' \
    >> "$OUT_JSONL"
done < "$LEADS"

COUNT="$(wc -l < "$OUT_JSONL" | tr -d ' ')"
PROMOTE="$(jq -sr '[.[] | select(.proposal_class=="PROMOTE_TO_HIGH")] | length' "$OUT_JSONL")"
SUPPRESS="$(jq -sr '[.[] | select(.proposal_class=="SUPPRESS_NOISE")] | length' "$OUT_JSONL")"
REVIEW="$(jq -sr '[.[] | select(.proposal_class=="REQUIRE_HUMAN_REVIEW")] | length' "$OUT_JSONL")"
OUT_SHA="$(sha_file "$OUT_JSONL")"
LEADS_SHA="$(sha_file "$LEADS")"
RULES_SHA="$(sha_file "$RULES")"
CONFIG_SHA="$(sha_file "$CONFIG")"

jq -n \
  --arg utc "$UTC" \
  --arg output "${OUT_JSONL#$ROOT/}" \
  --arg output_sha "$OUT_SHA" \
  --arg leads "${LEADS#$ROOT/}" \
  --arg leads_sha "$LEADS_SHA" \
  --arg rules_sha "$RULES_SHA" \
  --arg config_sha "$CONFIG_SHA" \
  --argjson count "$COUNT" \
  --argjson promote "$PROMOTE" \
  --argjson suppress "$SUPPRESS" \
  --argjson review "$REVIEW" \
  '{artifact:"latest_rule_tuning_manifest.json",version:"0.1",generated_utc:$utc,status:"RULE_TUNING_PROPOSALS_EMITTED",proposal_count:$count,promote_to_high_count:$promote,suppress_noise_count:$suppress,require_human_review_count:$review,output_jsonl:$output,output_sha256:$output_sha,input_leads_jsonl:$leads,input_leads_sha256:$leads_sha,rules_sha256:$rules_sha,tuning_config_sha256:$config_sha,mutates_live_rules:false,requires_human_review_before_patch:true,public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",claim_type:"RULE_TUNING_PROPOSAL_ONLY",human_review_required:true,no_fake_green:true}' \
  > "$OUT_MANIFEST"

echo "RULE_TUNING_PROPOSALS=$COUNT"
echo "PROMOTE_TO_HIGH=$PROMOTE"
echo "SUPPRESS_NOISE=$SUPPRESS"
echo "REQUIRE_HUMAN_REVIEW=$REVIEW"
echo "manifest=$OUT_MANIFEST"
echo "NO_FAKE_GREEN=ACTIVE"
