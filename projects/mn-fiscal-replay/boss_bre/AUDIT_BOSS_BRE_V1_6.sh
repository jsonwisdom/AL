#!/bin/bash
# AUDIT_BOSS_BRE_V1_6.sh
# Boss Bre v1.6 Repository Integrity Audit
# Doctrine: NO_FAKE_GREEN / DISCOVERY_BEFORE_DELEGATION / no raw dump without index.

set -euo pipefail

ROOT="projects/mn-fiscal-replay"
INDEX="$ROOT/librarian/MN_FISCAL_REPLAY_LIBRARIAN_INDEX_V0_3.json"
OUT_DIR="$ROOT/boss_bre/audits"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
SAFE_TS=$(date -u +%Y-%m-%dT%H-%M-%SZ)
OUT_JSON="$OUT_DIR/BOSS_BRE_V1_6_AUDIT_${SAFE_TS}.json"
OUT_MD="$OUT_DIR/BOSS_BRE_V1_6_AUDIT_${SAFE_TS}.md"

mkdir -p "$OUT_DIR"

PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

PASS_ITEMS=()
FAIL_ITEMS=()
WARN_ITEMS=()

pass() {
  echo "[PASS] $1"
  PASS_ITEMS+=("$1")
  PASS_COUNT=$((PASS_COUNT+1))
}

fail() {
  echo "[FAIL] $1"
  FAIL_ITEMS+=("$1")
  FAIL_COUNT=$((FAIL_COUNT+1))
}

warn() {
  echo "[WARN] $1"
  WARN_ITEMS+=("$1")
  WARN_COUNT=$((WARN_COUNT+1))
}

echo "=== BOSS BRE V1.6 REPOSITORY AUDIT ==="
echo "Timestamp: $TS"
echo "Root: $ROOT"

if [ ! -d "$ROOT" ]; then
  echo "BLOCKED_REASON: Missing root directory: $ROOT"
  exit 1
fi

echo ""
echo "[0] Checking Librarian Index v0.3..."
if [ -f "$INDEX" ]; then
  pass "Librarian Index v0.3 exists"
else
  fail "Missing Librarian Index v0.3: $INDEX"
fi

echo ""
echo "[1] Checking maintenance baselines listed in Librarian Index..."
if [ -f "$INDEX" ]; then
  mapfile -t INDEX_IDS < <(jq -r '.manifest[].id' "$INDEX" 2>/dev/null || true)

  if [ "${#INDEX_IDS[@]}" -eq 0 ]; then
    fail "Librarian Index contains no manifest entries"
  fi

  for id in "${INDEX_IDS[@]}"; do
    status=$(jq -r --arg id "$id" '.manifest[] | select(.id==$id) | .status // empty' "$INDEX")
    claim=$(jq -r --arg id "$id" '.manifest[] | select(.id==$id) | .public_content_claim // empty' "$INDEX")
    final=$(jq -r --arg id "$id" '.manifest[] | select(.id==$id) | .final_safe_status // empty' "$INDEX")
    source_manifest=$(jq -r --arg id "$id" '.manifest[] | select(.id==$id) | .source_manifest // empty' "$INDEX")
    source_url=$(jq -r --arg id "$id" '.manifest[] | select(.id==$id) | .source_url // empty' "$INDEX")

    if [ "$status" = "MAINTENANCE_SAFE_BASELINE" ]; then
      pass "$id status is MAINTENANCE_SAFE_BASELINE"
    else
      fail "$id status is not MAINTENANCE_SAFE_BASELINE: $status"
    fi

    if [ "$claim" = "BLOCKED" ]; then
      pass "$id public_content_claim is BLOCKED"
    else
      fail "$id public_content_claim is not BLOCKED: $claim"
    fi

    if [ -n "$final" ] && [ -f "$final" ]; then
      verdict=$(jq -r '.verdict // empty' "$final")
      delta=$(jq -r '.possible_content_delta' "$final")
      if [ "$verdict" = "PUBLIC_CONTENT_ANOMALY_UNPROVEN" ] && [ "$delta" = "false" ]; then
        pass "$id final safe status is valid"
      else
        fail "$id final safe status invalid: verdict=$verdict possible_content_delta=$delta"
      fi
    else
      fail "$id final safe status missing: $final"
    fi

    if [ -n "$source_manifest" ] && [ -f "$source_manifest" ]; then
      pass "$id source manifest exists"
    else
      fail "$id source manifest missing: $source_manifest"
    fi

    case "$source_url" in
      https://mn.gov/*|https://www.mn.gov/*)
        pass "$id source URL is official mn.gov"
        ;;
      *)
        fail "$id source URL is not official mn.gov: $source_url"
        ;;
    esac
  done
fi

echo ""
echo "[2] Checking live_fetch lanes for final status receipts..."
shopt -s nullglob
LIVE_DIRS=("$ROOT"/live_fetch/*/)
shopt -u nullglob

if [ "${#LIVE_DIRS[@]}" -eq 0 ]; then
  warn "No live_fetch directories found"
else
  for dir in "${LIVE_DIRS[@]}"; do
    jurisdiction=$(basename "$dir")
    status_file="${dir}${jurisdiction}_FINAL_SAFE_STATUS_V0_1.json"
    verdict_file="${dir}chunks/${jurisdiction}.chunked_verdict.json"

    if [ -f "$status_file" ]; then
      pass "Final safe status sealed: $jurisdiction"
    else
      warn "Missing final safe status: $jurisdiction"
    fi

    if [ -f "$verdict_file" ]; then
      pass "Chunk verdict receipt exists: $jurisdiction"
    else
      warn "Missing chunk verdict receipt: $jurisdiction"
    fi
  done
fi

echo ""
echo "[3] Checking raw PDFs against Librarian Index..."
shopt -s nullglob
PDFS=("$ROOT"/live_fetch/*/*.pdf)
shopt -u nullglob

if [ -f "$INDEX" ]; then
  if [ "${#PDFS[@]}" -eq 0 ]; then
    warn "No live_fetch PDFs found"
  else
    for file in "${PDFS[@]}"; do
      filename=$(basename "$file")
      jurisdiction="${filename%_live.pdf}"

      if jq -e --arg id "$jurisdiction" '.manifest[] | select(.id==$id)' "$INDEX" >/dev/null 2>&1; then
        pass "Raw PDF indexed by Librarian: $jurisdiction"
      else
        warn "Raw PDF without Librarian maintenance index entry: $jurisdiction"
      fi
    done
  fi
fi

echo ""
echo "[4] Checking for placeholder / suspicious URLs..."
PLACEHOLDER_HITS=$(grep -RInE 'placeholder|REAL/OFFICIAL|march-update\.pdf|example\.com|TODO.*URL|insert.*URL' "$ROOT" 2>/dev/null || true)

if [ -z "$PLACEHOLDER_HITS" ]; then
  pass "No placeholder/suspicious URL strings found under $ROOT"
else
  warn "Placeholder/suspicious URL strings found"
fi

echo ""
echo "[5] Checking for possible next manifests..."
shopt -s nullglob
SOURCE_MANIFESTS=(_sources/MN_*/source_manifest.json)
shopt -u nullglob

NEXT_MANIFESTS=()
for manifest in "${SOURCE_MANIFESTS[@]}"; do
  id=$(echo "$manifest" | cut -d/ -f2)
  if [ -f "$INDEX" ] && jq -e --arg id "$id" '.manifest[] | select(.id==$id)' "$INDEX" >/dev/null 2>&1; then
    :
  else
    NEXT_MANIFESTS+=("$manifest")
  fi
done

if [ "${#NEXT_MANIFESTS[@]}" -eq 0 ]; then
  pass "No unindexed MN source manifests found"
else
  warn "Unindexed MN source manifests found: ${NEXT_MANIFESTS[*]}"
fi

STATUS="CLEAN_WITH_WARNINGS"
if [ "$FAIL_COUNT" -gt 0 ]; then
  STATUS="REMEDIATION_REQUIRED"
elif [ "$WARN_COUNT" -eq 0 ]; then
  STATUS="CLEAN"
fi

python3 - "$OUT_JSON" "$TS" "$STATUS" "$PASS_COUNT" "$WARN_COUNT" "$FAIL_COUNT" \
  "$(printf '%s\n' "${PASS_ITEMS[@]}" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().splitlines()))')" \
  "$(printf '%s\n' "${WARN_ITEMS[@]}" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().splitlines()))')" \
  "$(printf '%s\n' "${FAIL_ITEMS[@]}" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().splitlines()))')" \
  "$PLACEHOLDER_HITS" \
  "$(printf '%s\n' "${NEXT_MANIFESTS[@]}" | python3 -c 'import json,sys; print(json.dumps([x for x in sys.stdin.read().splitlines() if x]))')" << 'PY'
import json, sys
from pathlib import Path

out = Path(sys.argv[1])
receipt = {
  "artifact": "BOSS_BRE_V1_6_AUDIT",
  "timestamp": sys.argv[2],
  "status": sys.argv[3],
  "pass_count": int(sys.argv[4]),
  "warn_count": int(sys.argv[5]),
  "fail_count": int(sys.argv[6]),
  "passes": json.loads(sys.argv[7]),
  "warnings": json.loads(sys.argv[8]),
  "failures": json.loads(sys.argv[9]),
  "placeholder_hits": sys.argv[10].splitlines() if sys.argv[10] else [],
  "unindexed_source_manifests": json.loads(sys.argv[11]),
  "public_content_claim": "BLOCKED",
  "no_fake_green": True
}
out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
PY

cat > "$OUT_MD" << EOF_MD
# Boss Bre v1.6 Audit

- Timestamp: \`$TS\`
- Status: \`$STATUS\`
- Pass: \`$PASS_COUNT\`
- Warn: \`$WARN_COUNT\`
- Fail: \`$FAIL_COUNT\`

## Doctrine

\`NO_FAKE_GREEN\`

Public content claims remain blocked unless final receipts prove claimability.

## Receipt

\`$OUT_JSON\`
EOF_MD

echo ""
echo "=== AUDIT COMPLETE ==="
echo "Status: $STATUS"
echo "Summary: $PASS_COUNT PASS | $WARN_COUNT WARN | $FAIL_COUNT FAIL"
echo "JSON: $OUT_JSON"
echo "MD: $OUT_MD"

if [ "$FAIL_COUNT" -gt 0 ]; then
  echo "REMEDIATION REQUIRED before new discovery."
else
  echo "NO BLOCKING FAILURES. Review warnings before new discovery."
fi
