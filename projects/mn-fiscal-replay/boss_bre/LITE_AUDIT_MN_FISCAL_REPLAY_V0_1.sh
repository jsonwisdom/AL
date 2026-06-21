#!/bin/bash
# LITE_AUDIT_MN_FISCAL_REPLAY_V0_1.sh
# Minimal lane-scoped audit. No recursive scans. No heredoc firehose.
# Doctrine: NO_FAKE_GREEN / LANE_SCOPED / DISCOVERY_BEFORE_DELEGATION.

set -euo pipefail

ROOT="projects/mn-fiscal-replay"
INDEX="$ROOT/librarian/MN_FISCAL_REPLAY_LIBRARIAN_INDEX_V0_3.json"
OUT_DIR="$ROOT/boss_bre/audits"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
SAFE_TS=$(date -u +%Y-%m-%dT%H-%M-%SZ)
OUT_JSON="$OUT_DIR/LITE_AUDIT_MN_FISCAL_REPLAY_V0_1_${SAFE_TS}.json"

mkdir -p "$OUT_DIR"

PASS=0
FAIL=0

check_pass() { echo "[PASS] $1"; PASS=$((PASS+1)); }
check_fail() { echo "[FAIL] $1"; FAIL=$((FAIL+1)); }

if [ -f "$INDEX" ]; then
  check_pass "Librarian Index v0.3 exists"
else
  check_fail "Missing Librarian Index v0.3: $INDEX"
fi

for ID in MN_001 MN_002; do
  echo "--- $ID ---"

  if jq -e --arg id "$ID" '.manifest[] | select(.id==$id and .status=="MAINTENANCE_SAFE_BASELINE" and .public_content_claim=="BLOCKED" and .possible_content_delta==false)' "$INDEX" >/dev/null; then
    check_pass "$ID index entry is maintenance-safe and blocked"
  else
    check_fail "$ID index entry invalid or missing"
  fi

  FINAL="$ROOT/live_fetch/$ID/${ID}_FINAL_SAFE_STATUS_V0_1.json"
  if [ -f "$FINAL" ] && jq -e '.verdict=="PUBLIC_CONTENT_ANOMALY_UNPROVEN" and .public_content_claim=="BLOCKED" and .possible_content_delta==false' "$FINAL" >/dev/null; then
    check_pass "$ID final safe status valid"
  else
    check_fail "$ID final safe status missing or invalid"
  fi

  CHUNK="$ROOT/live_fetch/$ID/chunks/${ID}.chunked_verdict.json"
  if [ -f "$CHUNK" ] && jq -e '.public_content_claim=="BLOCKED"' "$CHUNK" >/dev/null; then
    check_pass "$ID chunk receipt exists and claim is blocked"
  else
    check_fail "$ID chunk receipt missing or invalid"
  fi

done

STATUS="CLEAN"
if [ "$FAIL" -gt 0 ]; then
  STATUS="REMEDIATION_REQUIRED"
fi

jq -n \
  --arg artifact "LITE_AUDIT_MN_FISCAL_REPLAY_V0_1" \
  --arg timestamp "$TS" \
  --arg status "$STATUS" \
  --arg index "$INDEX" \
  --argjson pass "$PASS" \
  --argjson fail "$FAIL" \
  '{artifact:$artifact,timestamp:$timestamp,status:$status,index:$index,pass_count:$pass,fail_count:$fail,public_content_claim:"BLOCKED",no_fake_green:true}' > "$OUT_JSON"

echo "=== LITE AUDIT COMPLETE ==="
echo "Status: $STATUS"
echo "Summary: $PASS PASS | 0 WARN | $FAIL FAIL"
echo "JSON: $OUT_JSON"
cat "$OUT_JSON" | jq .

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
