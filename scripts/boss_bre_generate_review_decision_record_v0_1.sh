#!/usr/bin/env bash
# Boss Bre review decision record generator v0.1
# Generates a draft human review record from tuning proposals.
# Does not authorize rule patches.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
STATE="$ROOT/projects/mn-fiscal-replay/boss_bre"
WITNESS_VERIFY="$STATE/witness_feed/witness_chain_verify_receipt.json"
TUNING_MANIFEST="$STATE/latest_rule_tuning_manifest.json"
PROPOSALS="$STATE/latest_rule_tuning_proposals.jsonl"
RULES="$ROOT/data/boss_bre_anomaly_rules.json"
OUT="$STATE/latest_review_decision_record.json"
UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
REVIEWER="${REVIEWER:-TODO_FILL_HUMAN_REVIEWER}"

mkdir -p "$STATE"

sha_file() {
  if [ -f "$1" ]; then sha256sum "$1" | awk '{print $1}'; else echo ""; fi
}

if [ ! -s "$PROPOSALS" ]; then
  jq -n \
    --arg utc "$UTC" \
    '{artifact:"boss_bre_review_decision_record",version:"0.1",status:"DECISION_RECORD_BLOCKED",generated_utc:$utc,blocked_reason:"RULE_TUNING_PROPOSALS_MISSING_OR_EMPTY",rules_patch_authorized:false,public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",human_review_required:true,no_fake_green:true}' \
    > "$OUT"
  echo "DECISION_RECORD_BLOCKED: RULE_TUNING_PROPOSALS_MISSING_OR_EMPTY"
  exit 0
fi

proposal_count="$(wc -l < "$PROPOSALS" | tr -d ' ')"
witness_sha="$(sha_file "$WITNESS_VERIFY")"
tuning_manifest_sha="$(sha_file "$TUNING_MANIFEST")"
proposals_sha="$(sha_file "$PROPOSALS")"
rules_sha="$(sha_file "$RULES")"

decisions_json="$(jq -sr '[.[] | {proposal_id:(.proposal_id // "sha256:UNKNOWN"), decision:"DEFER_MORE_EVIDENCE", reason:"TODO_HUMAN_REVIEW_REQUIRED", approved_rule_action:"NONE", jurisdiction:(.jurisdiction // "UNKNOWN"), rule_id:(.rule_id // "UNKNOWN_RULE"), current_severity:(.current_severity // .severity // "UNKNOWN"), proposal_class:(.proposal_class // "UNKNOWN"), source_pdf_sha256:(.source_pdf_sha256 // ""), source_text_sha256:(.source_text_sha256 // ""), evidence_excerpt_reviewed:(.evidence_excerpt // ""), human_review_required:true, public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW", no_fake_green:true}]' "$PROPOSALS")"

jq -n \
  --arg utc "$UTC" \
  --arg reviewer "$REVIEWER" \
  --arg witness_sha "sha256:$witness_sha" \
  --arg tuning_manifest_sha "sha256:$tuning_manifest_sha" \
  --arg proposals_sha "sha256:$proposals_sha" \
  --arg rules_sha "sha256:$rules_sha" \
  --argjson proposal_count "$proposal_count" \
  --argjson decisions "$decisions_json" \
  '{artifact:"boss_bre_review_decision_record",version:"0.1",status:"DRAFT_PENDING_HUMAN_REVIEW",review_scope:"RULE_TUNING_V0_1_TO_RULES_V0_2",generated_utc:$utc,reviewer:$reviewer,repo:"jsonwisdom/AL",workflow:"Boss Bre Public Audit",witness_chain_verify_receipt_sha256:$witness_sha,rule_tuning_manifest_sha256:$tuning_manifest_sha,rule_tuning_proposals_sha256:$proposals_sha,current_rules_sha256:$rules_sha,current_rules_version:"0.1",target_rules_version:"0.2",decision_mode:"HUMAN_REVIEW_REQUIRED",proposal_count:$proposal_count,allowed_decisions:["APPROVE_PROMOTE","APPROVE_SUPPRESS","APPROVE_REVIEW_REQUIRED","REJECT_NOISE","DEFER_MORE_EVIDENCE"],approval_requirements:{source_pdf_sha256_present:true,source_text_sha256_present:true,meaningful_evidence_excerpt_required:true,public_content_claim_must_remain_blocked_pending_review:true,no_fake_green_must_remain_true:true},decisions:$decisions,patch_authorization:{rules_patch_authorized:false,authorized_target:"data/boss_bre_anomaly_rules.json",must_increment_version:true,must_preserve_no_fake_green:true,must_preserve_no_fraud_verdict_without_source_and_human_review:true},claim_status:"REVIEW_DECISION_RECORD_ONLY",public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",human_review_required:true,no_fake_green:true}' \
  > "$OUT"

echo "REVIEW_DECISION_RECORD_DRAFTED"
echo "proposal_count=$proposal_count"
echo "rules_patch_authorized=false"
echo "output=$OUT"
echo "NO_FAKE_GREEN=ACTIVE"
