#!/usr/bin/env bash
# =============================================================================
# ALMS V2 Mutation Demo
# Visual proof of tamper detection for Machine Speed ALMS V2.
#
# This script demonstrates:
#   clean receipt -> replay OK
#   one-character semantic mutation -> replay FAIL
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
RECEIPTS_DIR="$PROJECT_ROOT/_truth/receipts"
ORIGINAL="$RECEIPTS_DIR/demo_budget.json"
MUTATED="$RECEIPTS_DIR/demo_budget_mutated.json"
CLAIM='The project budget increased by 42% in Q1 2026.'

mkdir -p "$RECEIPTS_DIR"
chmod +x "$PROJECT_ROOT/scripts/alms_normalize.sh" "$PROJECT_ROOT/scripts/alms_verify.sh" 2>/dev/null || true

printf '%s\n' '=== ALMS V2 Mutation Demo ==='
printf 'Claim: %s\n\n' "$CLAIM"

printf '%s\n' '--- Step 1: Generate original receipt ---'
printf '%s' "$CLAIM" | "$PROJECT_ROOT/scripts/alms_verify.sh" > "$ORIGINAL"
printf 'ORIGINAL_RECEIPT=%s\n' "$ORIGINAL"
jq -r '"ORIGINAL_ID=\(.receipt_id)\nORIGINAL_VERDICT=\(.verdict)\nORIGINAL_HASH=\(.receipt_hash)"' "$ORIGINAL"

printf '\n%s\n' '--- Step 2: Replay original receipt; must pass ---'
if "$PROJECT_ROOT/scripts/alms_verify.sh" "$ORIGINAL" > /tmp/alms_demo_original_replay.json; then
  printf '%s\n' 'ORIGINAL_REPLAY=ALMS_VERIFY_OK'
else
  printf '%s\n' 'ORIGINAL_REPLAY=ALMS_VERIFY_FAIL'
  exit 1
fi

printf '\n%s\n' '--- Step 3: Mutate one semantic character: 42% -> 43% ---'
cp "$ORIGINAL" "$MUTATED"
sed -i.bak 's/42%/43%/' "$MUTATED"
rm -f "$MUTATED.bak"
printf 'MUTATED_RECEIPT=%s\n' "$MUTATED"
printf '%s\n' 'MUTATION=42%->43%'

printf '\n%s\n' '--- Step 4: Replay mutated receipt; must fail ---'
set +e
MUTATED_OUTPUT=$("$PROJECT_ROOT/scripts/alms_verify.sh" "$MUTATED" 2>&1 >/tmp/alms_demo_mutated_replay.json)
MUTATED_STATUS=$?
set -e

if [ "$MUTATED_STATUS" -eq 0 ]; then
  printf '%s\n' 'MUTATED_REPLAY=UNEXPECTED_PASS'
  printf '%s\n' 'ALMS_MUTATION_DEMO_FAIL mutation was accepted'
  exit 1
fi

printf '%s\n' 'MUTATED_REPLAY=ALMS_VERIFY_FAIL'
printf 'FAILURE_SIGNAL=%s\n' "$MUTATED_OUTPUT"

printf '\n%s\n' '--- Receipt Comparison ---'
printf '| Receipt | Claim | Receipt Hash | Replay |\n'
printf '|---|---|---|---|\n'
printf '| Original | %s | %s | OK |\n' \
  "$(jq -r '.original_claim' "$ORIGINAL")" \
  "$(jq -r '.receipt_hash' "$ORIGINAL")"
printf '| Mutated | %s | %s | FAIL |\n' \
  "$(jq -r '.original_claim' "$MUTATED")" \
  "$(jq -r '.receipt_hash' "$MUTATED")"

printf '\n%s\n' 'ALMS_MUTATION_DEMO_OK original_passed=true mutated_failed=true'
printf '%s\n' 'This proves the receipt is tamper-evident: one semantic edit breaks replay.'
