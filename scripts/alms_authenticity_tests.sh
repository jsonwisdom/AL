#!/usr/bin/env bash
# =============================================================================
# ALMS Authenticity Test Harness
# Adversarial checks for scripts/alms_verify_anchor.sh.
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
EXTRACTOR="$PROJECT_ROOT/scripts/alms_extract_numbers.sh"
VERIFY_ANCHOR="$PROJECT_ROOT/scripts/alms_verify_anchor.sh"
TMP_DIR="${TMPDIR:-/tmp}/alms_authenticity_tests_$$"
mkdir -p "$TMP_DIR"
trap 'rm -rf "$TMP_DIR"' EXIT

URL="https://mn.gov/mmb-stat/000/az/forecast/2026/budget-and-economic-forecast/february.pdf"
GOOD_HASH="sha256:REPLACE_WITH_ACTUAL_HASH"
BAD_HASH="sha256:0000000000000000000000000000000000000000000000000000000000000000"
GOOD_ENS="alms.mn.mmb.feb2026.cid"
BAD_ENS="alms.bad.key"
GOOD_IPFS="bafyfixturegoodcid"
BAD_IPFS="bafyfixturebadcid"

REGISTRY="$PROJECT_ROOT/contracts/source_registry.v1.json"
REGISTRY_BAK="$TMP_DIR/source_registry.v1.json.bak"
cp "$REGISTRY" "$REGISTRY_BAK"
restore_registry() { cp "$REGISTRY_BAK" "$REGISTRY"; }
trap 'restore_registry; rm -rf "$TMP_DIR"' EXIT

set_registry() {
  local hash="$1" ipfs="$2" ens="$3"
  jq --arg url "$URL" --arg hash "$hash" --arg ipfs "$ipfs" --arg ens "$ens" \
    '.sources[0].url=$url | .sources[0].raw_hash=$hash | .sources[0].ipfs_cid=$ipfs | .sources[0].ens_key=$ens | .sources[0].status="ANCHORED"' \
    "$REGISTRY" > "$TMP_DIR/registry.new"
  cp "$TMP_DIR/registry.new" "$REGISTRY"
}

extract_numbers_array() {
  local claim="$1" out="$2"
  printf '%s' "$claim" | "$EXTRACTOR" | jq '.numbers' > "$out"
}

run_case() {
  local name="$1" claim="$2" expected="$3"
  local numbers="$TMP_DIR/numbers.json"
  extract_numbers_array "$claim" "$numbers"

  set +e
  output=$("$VERIFY_ANCHOR" "$numbers" 2>&1)
  code=$?
  set -e

  actual="PASS"
  if [ "$code" -ne 0 ]; then actual="FAIL"; fi
  if printf '%s' "$output" | grep -q 'ALMS_WARN source_authenticity_no_registry'; then actual="WARN"; fi

  status="OK"
  if [ "$actual" != "$expected" ]; then status="UNEXPECTED"; fi

  printf '| %s | %s | %s | %s | `%s` |\n' "$name" "$expected" "$actual" "$status" "$output"
}

printf '%s\n' '# ALMS Authenticity Test Results'
printf '%s\n' '| Case | Expected | Actual | Status | Signal |'
printf '%s\n' '|---|---:|---:|---:|---|'

set_registry "$GOOD_HASH" "$GOOD_IPFS" "$GOOD_ENS"
run_case 'correct hash + ipfs + ens' \
  "\$3.7B [source:url:$URL|$GOOD_HASH|ipfs:$GOOD_IPFS|ens:$GOOD_ENS]" \
  'PASS'

run_case 'wrong hash' \
  "\$3.7B [source:url:$URL|$BAD_HASH|ipfs:$GOOD_IPFS|ens:$GOOD_ENS]" \
  'FAIL'

run_case 'wrong ipfs' \
  "\$3.7B [source:url:$URL|$GOOD_HASH|ipfs:$BAD_IPFS|ens:$GOOD_ENS]" \
  'FAIL'

run_case 'wrong ens' \
  "\$3.7B [source:url:$URL|$GOOD_HASH|ipfs:$GOOD_IPFS|ens:$BAD_ENS]" \
  'FAIL'

run_case 'partial anchor only hash' \
  "\$3.7B [source:url:$URL|$GOOD_HASH]" \
  'PASS'

run_case 'no registry entry' \
  "\$3.7B [source:url:https://example.com/unregistered.pdf|$GOOD_HASH]" \
  'WARN'

printf '\n%s\n' 'Policy v1:'
printf '%s\n' '- Missing registry entry warns but does not hard-fail.'
printf '%s\n' '- Any declared hash/IPFS/ENS mismatch hard-fails.'
printf '%s\n' '- Registry is restored after tests.'
