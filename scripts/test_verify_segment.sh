#!/usr/bin/env bash
set -euo pipefail

GOOD="tests/fixtures/segment.good/segment_manifest.json"
BAD="tests/fixtures/segment.bad/segment_manifest.json"

fail() {
  echo "ALMS_SEGMENT_TESTS_FAIL"
  exit 1
}

if ./scripts/verify_segment.sh "$GOOD" >/dev/null; then
  echo "TEST_GOOD_SEGMENT"
else
  echo "TEST_GOOD_SEGMENT_FAILED"
  fail
fi

if ! ./scripts/verify_segment.sh "$BAD" >/dev/null; then
  echo "TEST_BAD_SEGMENT"
else
  echo "TEST_BAD_SEGMENT_FAILED"
  fail
fi

echo "ALMS_VERIFY_SEGMENT_TESTS_PASS"
exit 0
