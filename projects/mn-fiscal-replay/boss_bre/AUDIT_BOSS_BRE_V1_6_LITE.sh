#!/bin/bash
# AUDIT_BOSS_BRE_V1_6_LITE.sh
# Lightweight audit that will not firehose Cloud Shell.
# Doctrine: NO_FAKE_GREEN / DISCOVERY_BEFORE_DELEGATION.

set -euo pipefail

ROOT="projects/mn-fiscal-replay"
INDEX="$ROOT/librarian/MN_FISCAL_REPLAY_LIBRARIAN_INDEX_V0_3.json"
OUT_DIR="$ROOT/boss_bre/audits"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
SAFE_TS=$(date -u +%Y-%m-%dT%H-%M-%SZ)
OUT_JSON="$OUT_DIR/BOSS_BRE_V1_6_LITE_AUDIT_${SAFE_TS}.json"
OUT_MD="$OUT_DIR/BOSS_BRE_V1_6_LITE_AUDIT_${SAFE_TS}.md"

mkdir -p "$OUT_DIR"

PASS=0
WARN=0
FAIL=0

echo "=== BOSS BRE V1.6 LITE AUDIT ==="
echo "Timestamp: $TS"

if [ ! -f "$INDEX" ]; then
  echo "[FAIL] Missing Librarian Index v0.3: $INDEX"
  FAIL=$((FAIL+1))
else
  echo "[PASS] Librarian Index v0.3 exists"
  PASS=$((PASS+1))
fi

if [ -f "$INDEX" ]; then
  echo ""
  echo "=== INDEX MANIFEST ==="
  jq -r '.manifest[] | "- " + .id + " | " + .status + " | claim=" + .public_content_claim + " | delta=" + (.possible_content_delta|tostring)' "$INDEX"

  for id in $(jq -r '.manifest[].id' "$INDEX"); do
    final=$(jq -r --arg id "$id" '.manifest[] | select(.id==$id) | .final_safe_status' "$INDEX")
    source_manifest=$(jq -r --arg id "$id" '.manifest[] | select(.id==$id) | .source_manifest' "$INDEX")
    source_url=$(jq -r --arg id "$id" '.manifest[] | select(.id==$id) | .source_url' "$INDEX")

    echo ""
    echo "=== CHECK $id ==="

    if [ -f "$final" ]; then
      verdict=$(jq -r '.verdict // empty' "$final")
      delta=$(jq -r '.possible_content_delta' "$final")
      claim=$(jq -r '.public_content_claim // empty' "$final")

      if [ "$verdict" = "PUBLIC_CONTENT_ANOMALY_UNPROVEN" ] && [ "$delta" = "false" ] && [ "$claim" = "BLOCKED" ]; then
        echo "[PASS] final safe status valid: $id"
        PASS=$((PASS+1))
      else
        echo "[FAIL] final safe status invalid: $id verdict=$verdict delta=$delta claim=$claim"
        FAIL=$((FAIL+1))
      fi
    else
      echo "[FAIL] final safe status missing: $id -> $final"
      FAIL=$((FAIL+1))
    fi

    if [ -f "$source_manifest" ]; then
      echo "[PASS] source manifest exists: $source_manifest"
      PASS=$((PASS+1))
    else
      echo "[FAIL] source manifest missing: $source_manifest"
      FAIL=$((FAIL+1))
    fi

    case "$source_url" in
      https://mn.gov/*|https://www.mn.gov/*)
        echo "[PASS] official mn.gov source URL: $source_url"
        PASS=$((PASS+1))
        ;;
      *)
        echo "[FAIL] non-official source URL: $source_url"
        FAIL=$((FAIL+1))
        ;;
    esac
  done
fi

echo ""
echo "=== UNINDEXED SOURCE MANIFEST CHECK ==="
UNINDEXED_COUNT=0
for manifest in _sources/MN_*/source_manifest.json; do
  [ -f "$manifest" ] || continue
  id=$(echo "$manifest" | cut -d/ -f2)

  if [ -f "$INDEX" ] && jq -e --arg id "$id" '.manifest[] | select(.id==$id)' "$INDEX" >/dev/null; then
    :
  else
    echo "[WARN] unindexed source manifest: $manifest"
    WARN=$((WARN+1))
    UNINDEXED_COUNT=$((UNINDEXED_COUNT+1))
  fi
done

if [ "$UNINDEXED_COUNT" -eq 0 ]; then
  echo "[PASS] no unindexed MN source manifests found"
  PASS=$((PASS+1))
fi

STATUS="CLEAN"
if [ "$FAIL" -gt 0 ]; then
  STATUS="REMEDIATION_REQUIRED"
elif [ "$WARN" -gt 0 ]; then
  STATUS="CLEAN_WITH_WARNINGS"
fi

jq -n \
  --arg artifact "BOSS_BRE_V1_6_LITE_AUDIT" \
  --arg timestamp "$TS" \
  --arg status "$STATUS" \
  --arg pass "$PASS" \
  --arg warn "$WARN" \
  --arg fail "$FAIL" \
  --arg index "$INDEX" \
  '{
    artifact: $artifact,
    timestamp: $timestamp,
    status: $status,
    pass_count: ($pass|tonumber),
    warn_count: ($warn|tonumber),
    fail_count: ($fail|tonumber),
    index: $index,
    public_content_claim: "BLOCKED",
    no_fake_green: true
  }' > "$OUT_JSON"

cat > "$OUT_MD" << EOF_MD
# Boss Bre v1.6 Lite Audit

- Timestamp: \`$TS\`
- Status: \`$STATUS\`
- Pass: \`$PASS\`
- Warn: \`$WARN\`
- Fail: \`$FAIL\`

\`NO_FAKE_GREEN\`

This lite audit checks only the sealed Librarian Index v0.3, final safe status receipts, official source manifests, and unindexed MN manifests. Deep recursive scan intentionally deferred to avoid Cloud Shell crash.

Receipt: \`$OUT_JSON\`
EOF_MD

echo ""
echo "=== AUDIT COMPLETE ==="
echo "Status: $STATUS"
echo "Summary: $PASS PASS | $WARN WARN | $FAIL FAIL"
echo "JSON: $OUT_JSON"
echo "MD: $OUT_MD"
