#!/usr/bin/env bash
set -euo pipefail

mkdir -p _truth/cw/tests

SOURCE="_truth/cw/tests/source.txt"
RECEIPT="_truth/cw/tests/receipt.json"
TAMPER="_truth/cw/tests/tamper.txt"

printf 'hello sovereign replay\n' > "$SOURCE"
printf 'tampered\n' > "$TAMPER"

URL='https://SOURCE.com/a/../report/?utm=123&utm_campaign=x#section'

GOLDEN="$(./scripts/canonicalize_uri.sh "$URL")"

if [ "$GOLDEN" != "https://source.com/report" ]; then
  echo "CW_KERNEL_TEST_FAIL reason=GOLDEN_URI_COLLAPSE expected=https://source.com/report got=$GOLDEN"
  exit 1
fi

./scripts/hash_receipt.sh "$URL" "$SOURCE" "$RECEIPT" >/tmp/cw_hash.out

PASS_OUT="$(./scripts/replay_receipt.sh "$RECEIPT" "$SOURCE")"
echo "$PASS_OUT" | grep -q 'CW_REPLAY_OK' || {
  echo "CW_KERNEL_TEST_FAIL reason=PASS_REPLAY_FAILED"
  echo "$PASS_OUT"
  exit 1
}

FAIL_OUT="$(./scripts/replay_receipt.sh "$RECEIPT" "$TAMPER" || true)"
echo "$FAIL_OUT" | grep -q 'reason=CONTENT_HASH_MISMATCH' || {
  echo "CW_KERNEL_TEST_FAIL reason=TAMPER_NOT_DETECTED"
  echo "$FAIL_OUT"
  exit 1
}

WAIT_OUT="$(./scripts/replay_receipt.sh "$RECEIPT" "_truth/cw/tests/missing.txt" || true)"
echo "$WAIT_OUT" | grep -q 'verdict=INDETERMINATE' || {
  echo "CW_KERNEL_TEST_FAIL reason=MISSING_SOURCE_NOT_INDETERMINATE"
  echo "$WAIT_OUT"
  exit 1
}

RH="$(jq -r '.receipt_hash' "$RECEIPT")"

echo "CW_KERNEL_TEST_OK golden_uri=$GOLDEN receipt_hash=$RH"
