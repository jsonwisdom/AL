#!/usr/bin/env bash
# Boss Bre rule version compare v0.1
# Purpose: compare pre/post rule-tuning lead receipt outputs without mutating rules.
# Doctrine: NO_FAKE_GREEN. This script emits comparison receipts only.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
STATE="$ROOT/projects/mn-fiscal-replay/boss_bre"
BEFORE="${BEFORE:-$STATE/compare/before_latest_lead_receipts.jsonl}"
AFTER="${AFTER:-$STATE/latest_lead_receipts.jsonl}"
OUT_DIR="$STATE/compare"
OUT_JSON="$OUT_DIR/latest_rule_version_compare.json"
UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

mkdir -p "$OUT_DIR"

sha_file() {
  if [ -f "$1" ]; then sha256sum "$1" | awk '{print $1}'; else echo ""; fi
}

count_all() {
  if [ -s "$1" ]; then wc -l < "$1" | tr -d ' '; else echo 0; fi
}

count_sev() {
  local file="$1" sev="$2"
  if [ -s "$file" ]; then jq -sr --arg sev "$sev" '[.[] | select(.severity==$sev)] | length' "$file"; else echo 0; fi
}

count_class() {
  local file="$1" key="$2" val="$3"
  if [ -s "$file" ]; then jq -sr --arg key "$key" --arg val "$val" '[.[] | select(.[$key]==$val)] | length' "$file"; else echo 0; fi
}

if [ ! -s "$BEFORE" ]; then
  jq -n \
    --arg utc "$UTC" \
    --arg before "${BEFORE#$ROOT/}" \
    '{artifact:"latest_rule_version_compare.json",version:"0.1",generated_utc:$utc,status:"COMPARE_BLOCKED",blocked_reason:"BEFORE_LEADS_MISSING",before_path:$before,public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",claim_type:"RULE_VERSION_COMPARE_ONLY",human_review_required:true,no_fake_green:true}' \
    > "$OUT_JSON"
  echo "COMPARE_BLOCKED: BEFORE_LEADS_MISSING"
  exit 0
fi

if [ ! -s "$AFTER" ]; then
  jq -n \
    --arg utc "$UTC" \
    --arg after "${AFTER#$ROOT/}" \
    '{artifact:"latest_rule_version_compare.json",version:"0.1",generated_utc:$utc,status:"COMPARE_BLOCKED",blocked_reason:"AFTER_LEADS_MISSING",after_path:$after,public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",claim_type:"RULE_VERSION_COMPARE_ONLY",human_review_required:true,no_fake_green:true}' \
    > "$OUT_JSON"
  echo "COMPARE_BLOCKED: AFTER_LEADS_MISSING"
  exit 0
fi

before_total="$(count_all "$BEFORE")"
after_total="$(count_all "$AFTER")"
before_high="$(count_sev "$BEFORE" HIGH)"
after_high="$(count_sev "$AFTER" HIGH)"
before_medium="$(count_sev "$BEFORE" MEDIUM)"
after_medium="$(count_sev "$AFTER" MEDIUM)"
before_low="$(count_sev "$BEFORE" LOW)"
after_low="$(count_sev "$AFTER" LOW)"
before_blocked="$(count_class "$BEFORE" public_content_claim BLOCKED_PENDING_HUMAN_REVIEW)"
after_blocked="$(count_class "$AFTER" public_content_claim BLOCKED_PENDING_HUMAN_REVIEW)"

jq -n \
  --arg utc "$UTC" \
  --arg before_path "${BEFORE#$ROOT/}" \
  --arg after_path "${AFTER#$ROOT/}" \
  --arg before_sha "$(sha_file "$BEFORE")" \
  --arg after_sha "$(sha_file "$AFTER")" \
  --argjson before_total "$before_total" \
  --argjson after_total "$after_total" \
  --argjson before_high "$before_high" \
  --argjson after_high "$after_high" \
  --argjson before_medium "$before_medium" \
  --argjson after_medium "$after_medium" \
  --argjson before_low "$before_low" \
  --argjson after_low "$after_low" \
  --argjson before_blocked "$before_blocked" \
  --argjson after_blocked "$after_blocked" \
  '{artifact:"latest_rule_version_compare.json",version:"0.1",generated_utc:$utc,status:"RULE_VERSION_COMPARE_COMPLETE",before:{path:$before_path,sha256:$before_sha,total:$before_total,high:$before_high,medium:$before_medium,low:$before_low,blocked_pending:$before_blocked},after:{path:$after_path,sha256:$after_sha,total:$after_total,high:$after_high,medium:$after_medium,low:$after_low,blocked_pending:$after_blocked},delta:{total:($after_total-$before_total),high:($after_high-$before_high),medium:($after_medium-$before_medium),low:($after_low-$before_low),blocked_pending:($after_blocked-$before_blocked)},acceptance_gate:{public_claims_remain_blocked:($after_blocked==$after_total),human_review_required:true,no_fake_green:true},public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",claim_type:"RULE_VERSION_COMPARE_ONLY",human_review_required:true,no_fake_green:true}' \
  > "$OUT_JSON"

echo "RULE_VERSION_COMPARE_COMPLETE"
echo "before_total=$before_total after_total=$after_total"
echo "before_high=$before_high after_high=$after_high"
echo "output=$OUT_JSON"
echo "NO_FAKE_GREEN=ACTIVE"
