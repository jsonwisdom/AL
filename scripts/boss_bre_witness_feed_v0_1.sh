#!/usr/bin/env bash
# Boss Bre witness feed shim v0.1
# Purpose: bind an anchored EAS receipt root to a replayable Witness event.
# Doctrine: NO_FAKE_GREEN. This script records witness metadata only; it never promotes public content claims.

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
STATE_DIR="$ROOT/projects/mn-fiscal-replay/boss_bre"
WITNESS_DIR="$STATE_DIR/witness_feed"
MANIFEST="$STATE_DIR/latest_lead_receipt_manifest.json"
LEADS_JSONL="$STATE_DIR/latest_lead_receipts.jsonl"
OUT="$WITNESS_DIR/latest_witness_event.json"
UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

EAS_UID="${EAS_UID:-}"
TX_HASH="${TX_HASH:-}"
WORKFLOW_RUN_ID="${WORKFLOW_RUN_ID:-}"
ANCHOR_CHAIN="${ANCHOR_CHAIN:-base}"
ANCHOR_SYSTEM="${ANCHOR_SYSTEM:-EAS}"
ANCHOR_STATUS="${ANCHOR_STATUS:-ANCHOR_PENDING}"

mkdir -p "$WITNESS_DIR"

sha_file() {
  if [ -f "$1" ]; then sha256sum "$1" | awk '{print $1}'; else echo ""; fi
}

repo_commit="$(git rev-parse HEAD)"
manifest_sha256="$(sha_file "$MANIFEST")"
lead_receipts_sha256="$(sha_file "$LEADS_JSONL")"
manifest_status="MISSING"
lead_receipts_status="MISSING"

[ -s "$MANIFEST" ] && manifest_status="PRESENT"
[ -s "$LEADS_JSONL" ] && lead_receipts_status="PRESENT"

if [ -z "$EAS_UID" ] || [ -z "$TX_HASH" ]; then
  ANCHOR_STATUS="ANCHOR_PENDING"
fi

jq -n \
  --arg artifact "latest_witness_event.json" \
  --arg version "0.1" \
  --arg utc "$UTC" \
  --arg system "BOSS_BRE" \
  --arg scope "MN" \
  --arg repo "jsonwisdom/AL" \
  --arg repo_commit "$repo_commit" \
  --arg workflow "Boss Bre Public Audit" \
  --arg workflow_run_id "$WORKFLOW_RUN_ID" \
  --arg anchor_system "$ANCHOR_SYSTEM" \
  --arg anchor_chain "$ANCHOR_CHAIN" \
  --arg anchor_status "$ANCHOR_STATUS" \
  --arg eas_uid "$EAS_UID" \
  --arg tx_hash "$TX_HASH" \
  --arg manifest_path "${MANIFEST#$ROOT/}" \
  --arg manifest_status "$manifest_status" \
  --arg manifest_sha256 "$manifest_sha256" \
  --arg lead_receipts_path "${LEADS_JSONL#$ROOT/}" \
  --arg lead_receipts_status "$lead_receipts_status" \
  --arg lead_receipts_sha256 "$lead_receipts_sha256" \
  '{artifact:$artifact,version:$version,generated_utc:$utc,system:$system,jurisdiction_scope:$scope,repo:$repo,repo_commit:$repo_commit,workflow:$workflow,workflow_run_id:$workflow_run_id,anchor:{system:$anchor_system,chain:$anchor_chain,status:$anchor_status,eas_uid:$eas_uid,tx_hash:$tx_hash},inputs:{lead_receipt_manifest:{path:$manifest_path,status:$manifest_status,sha256:$manifest_sha256},lead_receipts_jsonl:{path:$lead_receipts_path,status:$lead_receipts_status,sha256:$lead_receipts_sha256}},claim_status:"WITNESS_EVENT_ONLY",public_content_claim:"BLOCKED_PENDING_HUMAN_REVIEW",human_review_required:true,no_fake_green:true}' \
  > "$OUT"

echo "=== Boss Bre witness feed event complete ==="
echo "Witness event: $OUT"
echo "Anchor status: $ANCHOR_STATUS"
echo "Manifest sha256: $manifest_sha256"
echo "Lead receipts sha256: $lead_receipts_sha256"
echo "PUBLIC_CONTENT_CLAIM: BLOCKED_PENDING_HUMAN_REVIEW"
echo "NO_FAKE_GREEN: ACTIVE"
