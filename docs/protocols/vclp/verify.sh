#!/usr/bin/env bash
set -euo pipefail

LEDGER="${1:-_truth/ledger.jsonl}"
PATTERNS="${2:-_truth/patterns.json}"

echo "=== VCLP Runtime Ledger Verification ==="

if [[ ! -f "$LEDGER" ]]; then
  echo "✗ ledger not found: $LEDGER"
  exit 1
fi

if [[ ! -f "$PATTERNS" ]]; then
  echo "✗ patterns not found: $PATTERNS"
  exit 1
fi

jq empty "$PATTERNS" >/dev/null
echo "✓ patterns.json valid"

line_no=0
prev_line_hash=""
failed=0

while IFS= read -r line; do
  line_no=$((line_no + 1))
  [[ -z "$line" ]] && continue

  if ! printf "%s" "$line" | jq empty >/dev/null 2>&1; then
    echo "✗ line $line_no invalid JSON"
    failed=1
    continue
  fi

  claim_id="$(printf "%s" "$line" | jq -r '.claim_id // empty')"
  claim_text="$(printf "%s" "$line" | jq -r '.claim_text // empty')"
  stored_text_hash="$(printf "%s" "$line" | jq -r '.artifacts.text_hash // empty' | sed 's/^sha256://')"
  prev_hash="$(printf "%s" "$line" | jq -r '.prev_hash // "null"')"

  if [[ -z "$claim_id" || -z "$claim_text" || -z "$stored_text_hash" ]]; then
    echo "✗ line $line_no missing required fields"
    failed=1
    continue
  fi

  computed_text_hash="$(printf "%s" "$claim_text" | sha256sum | awk '{print $1}')"

  if [[ "$computed_text_hash" != "$stored_text_hash" ]]; then
    echo "✗ $claim_id text_hash mismatch"
    echo "  stored:   sha256:$stored_text_hash"
    echo "  computed: sha256:$computed_text_hash"
    failed=1
  else
    echo "✓ $claim_id text_hash"
  fi

  if [[ "$line_no" -eq 1 ]]; then
    if [[ "$prev_hash" != "null" ]]; then
      echo "✗ $claim_id genesis prev_hash must be null"
      failed=1
    else
      echo "✓ $claim_id genesis"
    fi
  else
    expected_prev="sha256:$prev_line_hash"
    if [[ "$prev_hash" != "$expected_prev" ]]; then
      echo "✗ $claim_id prev_hash mismatch"
      echo "  expected: $expected_prev"
      echo "  got:      $prev_hash"
      failed=1
    else
      echo "✓ $claim_id prev_hash"
    fi
  fi

  prev_line_hash="$(printf "%s" "$line" | sha256sum | awk '{print $1}')"
done < "$LEDGER"

if [[ "$failed" -ne 0 ]]; then
  echo "❌ chain broken"
  exit 1
fi

echo "✅ chain valid — all checks passed"
