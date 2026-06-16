#!/usr/bin/env bash
set -euo pipefail

# WRITE_RUN_0004.1 — Heterogeneous Diff Validation Runner
# Scope: manifest-pair only. No content fetch. No promotion.
# Usage:
#   scripts/run_diff_engine_tests.sh <manifest_A.json> <manifest_B.json>

A="${1:-}"
B="${2:-}"
ENGINE="scripts/diff_manifests_v1.sh"

if [ -z "$A" ] || [ -z "$B" ]; then
  echo "Usage: $0 <manifest_A.json> <manifest_B.json>"
  exit 1
fi

if [ ! -f "$A" ] || [ ! -f "$B" ]; then
  echo "MANIFEST_NOT_FOUND"
  exit 1
fi

if [ ! -x "$ENGINE" ]; then
  echo "ENGINE_NOT_EXECUTABLE: $ENGINE"
  exit 1
fi

OUT_ROOT="_truth/diff_engine/tests/$(date -u +%Y-%m-%dT%H-%M-%SZ)"
mkdir -p "$OUT_ROOT"

pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; exit 1; }

# 1) SAME vs SAME
echo "== CASE DIFF_001_SAME_MANIFEST =="
SAME_DIR="$OUT_ROOT/same"
mkdir -p "$SAME_DIR"
"$ENGINE" "$A" "$A" "$SAME_DIR" >/dev/null
jq -e '.added_count==0 and .removed_count==0 and .changed_count==0' "$SAME_DIR/diff_report.json" >/dev/null \
  && pass "DIFF_001_SAME_MANIFEST" \
  || fail "DIFF_001_SAME_MANIFEST"

# 2) HETEROGENEOUS A vs B
echo "== CASE DIFF_002_HETEROGENEOUS =="
HET_DIR="$OUT_ROOT/hetero"
mkdir -p "$HET_DIR"
"$ENGINE" "$A" "$B" "$HET_DIR" >/dev/null
jq -e '.changed_count==0' "$HET_DIR/diff_report.json" >/dev/null \
  && pass "DIFF_002_HETEROGENEOUS_NO_FALSE_CHANGED" \
  || fail "DIFF_002_HETEROGENEOUS_NO_FALSE_CHANGED"

# 3) CORRUPT JSON
echo "== CASE DIFF_003_CORRUPT_JSON =="
CORRUPT_DIR="$OUT_ROOT/corrupt"
mkdir -p "$CORRUPT_DIR"
cp "$A" "$CORRUPT_DIR/corrupt.json"
echo "{" >> "$CORRUPT_DIR/corrupt.json" # break JSON
set +e
"$ENGINE" "$CORRUPT_DIR/corrupt.json" "$A" "$CORRUPT_DIR" >/dev/null
RC=$?
set -e
[ "$RC" -ne 0 ] \
  && pass "DIFF_003_CORRUPT_JSON_FAIL_FAST" \
  || fail "DIFF_003_CORRUPT_JSON_FAIL_FAST"

# 4) TRUNCATED SHA (should not produce false 'changed' on hetero)
echo "== CASE DIFF_004_TRUNCATED_SHA =="
TRUNC_DIR="$OUT_ROOT/truncated"
mkdir -p "$TRUNC_DIR"
jq '.files[0].sha256 = (.files[0].sha256[0:16])' "$A" > "$TRUNC_DIR/trunc.json"
"$ENGINE" "$TRUNC_DIR/trunc.json" "$B" "$TRUNC_DIR" >/dev/null
jq -e '.changed_count==0' "$TRUNC_DIR/diff_report.json" >/dev/null \
  && pass "DIFF_004_TRUNCATED_SHA_NO_FALSE_CHANGED" \
  || fail "DIFF_004_TRUNCATED_SHA_NO_FALSE_CHANGED"

echo "ALL_TESTS_PASSED"
