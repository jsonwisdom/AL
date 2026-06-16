#!/usr/bin/env bash
# =============================================================================
# ALMS Source Match Test Harness
# Tests local source-excerpt numeric matching before integrating into verify.sh.
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MATCHER="$PROJECT_ROOT/scripts/alms_source_match.sh"
TMP_DIR="${TMPDIR:-/tmp}/alms_source_match_tests_$$"
mkdir -p "$TMP_DIR"
trap 'rm -rf "$TMP_DIR"' EXIT

if [ ! -x "$MATCHER" ]; then
  chmod +x "$MATCHER" 2>/dev/null || true
fi

run_case() {
  local name="$1"
  local claim="$2"
  local source="$3"
  local expected="$4"

  local claim_file="$TMP_DIR/claim.txt"
  local source_file="$TMP_DIR/source.txt"
  local output_file="$TMP_DIR/output.json"

  printf '%s' "$claim" > "$claim_file"
  printf '%s' "$source" > "$source_file"

  "$MATCHER" "$claim_file" "$source_file" > "$output_file"
  local passed actual status
  passed=$(jq -r '.passed' "$output_file")

  if [ "$passed" = "true" ]; then
    actual="PASS"
  else
    actual="FAIL"
  fi

  status="OK"
  if [ "$actual" != "$expected" ]; then
    status="UNEXPECTED"
  fi

  printf '| %s | %s | %s | %s |\n' "$name" "$expected" "$actual" "$status"
}

printf '%s\n' '# ALMS Source Match Test Results'
printf '%s\n\n' 'PASS means every claim number exists in the source excerpt as the same canonical tuple: unit + base_value + scale.'
printf '%s\n' '| Case | Expected | Actual | Status |'
printf '%s\n' '|---|---:|---:|---:|'

run_case 'single matching number' \
  'The projected balance is $3.7 billion [source:citation:mmb].' \
  'The projected balance is $3.7 billion for FY 2026-27.' \
  'PASS'

run_case 'single mismatched number' \
  'The projected balance is $4.2 billion [source:citation:mmb].' \
  'The projected balance is $3.7 billion for FY 2026-27.' \
  'FAIL'

run_case 'formatting equivalent: decimal padding' \
  'The projected balance is $3.70 billion [source:citation:mmb].' \
  'The projected balance is $3.7 billion for FY 2026-27.' \
  'PASS'

run_case 'formatting equivalent: commas' \
  'The projected balance is $3,700,000,000 [source:citation:mmb].' \
  'The projected balance is $3700000000 for FY 2026-27.' \
  'PASS'

run_case 'scale mismatch remains strict' \
  'The projected balance is $3.7 billion [source:citation:mmb].' \
  'The projected balance is $3700 million for FY 2026-27.' \
  'FAIL'

run_case 'multiple numbers all match' \
  'Revenue is $3.7 billion [source:citation:a] and margin is 42% [source:citation:b].' \
  'Revenue is $3.7 billion. Margin is 42%.' \
  'PASS'

run_case 'multiple numbers one mismatch' \
  'Revenue is $3.7 billion [source:citation:a] and margin is 43% [source:citation:b].' \
  'Revenue is $3.7 billion. Margin is 42%.' \
  'FAIL'

run_case 'extra source number allowed' \
  'Revenue is $3.7 billion [source:citation:a].' \
  'Revenue is $3.7 billion. Debt is $1 billion.' \
  'PASS'

printf '\n%s\n' 'Legend:'
printf '%s\n' '- Source may contain extra numbers; v1 only requires every claim number to be found in source.'
printf '%s\n' '- Scale remains strict: 3.7 billion and 3700 million do not match in v1.'
printf '%s\n' '- This is local excerpt matching only, not URL/PDF verification.'
