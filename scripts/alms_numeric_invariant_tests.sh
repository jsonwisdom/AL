#!/usr/bin/env bash
# =============================================================================
# ALMS Numeric Invariant Test Harness
# Maps current numeric meaning-lock behavior before refinement.
#
# Goal:
#   - prove true numeric drift fails
#   - identify formatting false positives
#   - document refine targets before source_presence or tolerance logic
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
EXTRACTOR="$PROJECT_ROOT/scripts/alms_extract_numbers.sh"
TMP_DIR="${TMPDIR:-/tmp}/alms_numeric_tests_$$"
mkdir -p "$TMP_DIR"
trap 'rm -rf "$TMP_DIR"' EXIT

if [ ! -x "$EXTRACTOR" ]; then
  chmod +x "$EXTRACTOR" 2>/dev/null || true
fi

run_pair() {
  local group="$1"
  local name="$2"
  local claim_a="$3"
  local claim_b="$4"
  local expected_now="$5"
  local expected_after_refine="$6"

  local a_json="$TMP_DIR/a.json"
  local b_json="$TMP_DIR/b.json"

  printf '%s' "$claim_a" | "$EXTRACTOR" > "$a_json"
  printf '%s' "$claim_b" | "$EXTRACTOR" > "$b_json"

  local hash_a hash_b actual
  hash_a=$(jq -r '.numbers_hash' "$a_json")
  hash_b=$(jq -r '.numbers_hash' "$b_json")

  if [ "$hash_a" = "$hash_b" ]; then
    actual="PASS"
  else
    actual="FAIL"
  fi

  local status="OK"
  if [ "$actual" != "$expected_now" ]; then
    status="UNEXPECTED"
  fi

  printf '| %s | %s | %s | %s | %s | %s | %s |\n' \
    "$group" "$name" "$expected_now" "$expected_after_refine" "$actual" "$status" "$hash_a / $hash_b"
}

printf '%s\n' '# ALMS Numeric Invariant Test Results'
printf '%s\n\n' 'PASS means the numeric extraction hashes match. FAIL means numeric drift or formatting drift was detected.'
printf '%s\n' '| Group | Case | Expected Now | Expected After Refine | Actual | Status | Hashes |'
printf '%s\n' '|---|---|---:|---:|---:|---:|---|'

# Case set A: formatting drift. These are expected to FAIL now, but should PASS after refine.
run_pair 'A formatting' '$3.7 billion vs $3.70 billion' \
  'The balance is $3.7 billion.' \
  'The balance is $3.70 billion.' \
  'FAIL' 'PASS'

run_pair 'A formatting' '$3,700,000,000 vs $3700000000' \
  'The balance is $3,700,000,000.' \
  'The balance is $3700000000.' \
  'FAIL' 'PASS'

run_pair 'A formatting' '3.7B vs 3.7bn' \
  'The balance is 3.7B.' \
  'The balance is 3.7bn.' \
  'FAIL' 'PASS'

# Case set B: true value drift. These must FAIL now and after refine.
run_pair 'B true drift' '3.7 billion vs 4.2 billion' \
  'The balance is 3.7 billion.' \
  'The balance is 4.2 billion.' \
  'FAIL' 'FAIL'

run_pair 'B true drift' '$3.7B vs $3.7M' \
  'The balance is $3.7B.' \
  'The balance is $3.7M.' \
  'FAIL' 'FAIL'

run_pair 'B true drift' '42% vs 43%' \
  'The increase was 42%.' \
  'The increase was 43%.' \
  'FAIL' 'FAIL'

# Case set C: multiple numbers. Current extractor is order-sensitive by design.
run_pair 'C multiple' 'same values swapped order' \
  'Revenue $3.7B, margin 42%.' \
  'Margin 42%, revenue $3.7B.' \
  'FAIL' 'DESIGN_DECISION'

run_pair 'C multiple' 'extra number added' \
  'Revenue $3.7B, margin 42%.' \
  'Revenue $3.7B, margin 42%, debt $1B.' \
  'FAIL' 'FAIL'

# Case set D: equivalent units. Current result documents the design gap.
run_pair 'D equivalent' '3.7B vs 3700M' \
  'The balance is 3.7B.' \
  'The balance is 3700M.' \
  'FAIL' 'DESIGN_DECISION'

printf '\n%s\n' 'Legend:'
printf '%s\n' '- Expected Now = behavior expected from the current strict extractor.'
printf '%s\n' '- Expected After Refine = target behavior for normalization/tolerance work.'
printf '%s\n' '- DESIGN_DECISION = do not change until claim model defines whether order or equivalent units should collapse.'
