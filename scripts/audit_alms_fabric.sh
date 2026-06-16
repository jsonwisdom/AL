#!/usr/bin/env bash
set -euo pipefail

# Hardened ALMS Fabric Adversarial Audit
# Deterministic, file-based, zero mutation of source

EPOCH="$1"
BASE="_truth/attest"
TMP="_audit_tmp_$EPOCH"

fail() { echo "AUDIT_FAIL $1"; }
pass() { echo "AUDIT_PASS $1"; }

rm -rf "$TMP"
mkdir -p "$TMP"

cp -r "$BASE" "$TMP/base"

BATCH_FILE="$TMP/base/batch/alms_batch_${EPOCH}.json"
[ -f "$BATCH_FILE" ] || { echo "AUDIT_FAIL missing_batch_file"; exit 1; }

# Test 1: Witness mutation
cp -r "$TMP/base" "$TMP/t1"
WFILE=$(ls "$TMP/t1/witness/"*.json | head -n1)
echo "corrupt" >> "$WFILE"
if scripts/verify_alms_batch.sh "$EPOCH" 2>/dev/null; then fail "witness_mutation"; else pass "witness_mutation"; fi

# Test 2: Extra witness
cp -r "$TMP/base" "$TMP/t2"
cp "$WFILE" "$TMP/t2/witness/extra.json"
if STRICT_MODE=1 scripts/verify_alms_batch.sh "$EPOCH" 2>/dev/null; then fail "extra_witness"; else pass "extra_witness"; fi

# Test 3: Manifest drift
cp -r "$TMP/base" "$TMP/t3"
jq '.extra="attack"' "$TMP/t3/batch/alms_batch_${EPOCH}.json" > "$TMP/t3/batch/tmp.json"
mv "$TMP/t3/batch/tmp.json" "$TMP/t3/batch/alms_batch_${EPOCH}.json"
if scripts/verify_alms_batch.sh "$EPOCH" 2>/dev/null; then fail "manifest_drift"; else pass "manifest_drift"; fi

# Test 4: Merkle tamper
cp -r "$TMP/base" "$TMP/t4"
jq '.merkle.root="0xdeadbeef"' "$TMP/t4/batch/alms_batch_${EPOCH}.json" > "$TMP/t4/batch/tmp.json"
mv "$TMP/t4/batch/tmp.json" "$TMP/t4/batch/alms_batch_${EPOCH}.json"
if scripts/verify_alms_batch.sh "$EPOCH" 2>/dev/null; then fail "merkle_tamper"; else pass "merkle_tamper"; fi

# Test 5: Calldata tamper (file-based)
OUT_FILE="$TMP/calldata.json"
scripts/generate_alms_ens_calldata.sh "$EPOCH" > "$OUT_FILE"
jq '.calldata="0xdeadbeef"' "$OUT_FILE" > "$TMP/bad.json"
if scripts/verify_alms_ens_calldata.sh "$TMP/bad.json" 2>/dev/null; then fail "calldata_tamper"; else pass "calldata_tamper"; fi

echo "AUDIT_COMPLETE"
