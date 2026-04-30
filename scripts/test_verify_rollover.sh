#!/usr/bin/env bash
set -euo pipefail

GOOD="tests/fixtures/rollover.good/rollover.json"
BAD="tests/fixtures/rollover.bad/rollover.json"

fail() {
  echo "ALMS_ROLLOVER_TESTS_FAIL"
  exit 1
}

if ./scripts/verify_rollover.sh "$GOOD" >/dev/null; then
  echo "TEST_GOOD_ROLLOVER"
else
  echo "TEST_GOOD_ROLLOVER_FAILED"
  fail
fi

if ! ./scripts/verify_rollover.sh "$BAD" >/dev/null; then
  echo "TEST_BAD_ROLLOVER"
else
  echo "TEST_BAD_ROLLOVER_FAILED"
  fail
fi

echo "ALMS_VERIFY_ROLLOVER_TESTS_PASS"
exit 0
