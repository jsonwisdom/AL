#!/usr/bin/env bash
set -euo pipefail

GOOD="tests/fixtures/alms_receipt.good.json"
BAD="tests/fixtures/alms_receipt.bad.json"

echo "TEST_GOOD_RECEIPT"
./scripts/verify_receipt.sh "$GOOD" | grep -q "ALMS_RECEIPT_VALID"

echo "TEST_BAD_RECEIPT"
if ./scripts/verify_receipt.sh "$BAD" >/tmp/alms_bad_test.out 2>&1; then
  echo "BAD_RECEIPT_UNEXPECTEDLY_VALID"
  cat /tmp/alms_bad_test.out
  exit 1
fi

grep -q "ALMS_RECEIPT_INVALID" /tmp/alms_bad_test.out

echo "ALMS_VERIFY_RECEIPT_TESTS_PASS"
