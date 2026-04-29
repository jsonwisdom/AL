#!/usr/bin/env bash
set -euo pipefail

PASS=0
FAIL=0

echo "ADVERSARIAL_MATRIX_V2_ENFORCED"

make_tmp() {
  NAME="$1"
  DIR="/tmp/alms_${NAME}_$$"
  rm -rf "$DIR"
  mkdir -p "$DIR"
  cp -a _truth "$DIR/"
  cp -a scripts "$DIR/"
  cp -a site "$DIR/" 2>/dev/null || true
  cp -a _sources "$DIR/" 2>/dev/null || true
  echo "$DIR"
}

expect_fail() {
  NAME="$1"
  DIR="$2"

  echo
  echo "ATTACK: $NAME"

  set +e
  (cd "$DIR" && ./scripts/preflight_repo_audit.sh >/tmp/alms_preflight_$$ 2>&1)
  CODE=$?
  set -e

  if [ "$CODE" -ne 0 ]; then
    echo "PASS: $NAME blocked"
    PASS=$((PASS+1))
  else
    echo "FAIL: $NAME not blocked"
    cat /tmp/alms_preflight_$$
    FAIL=$((FAIL+1))
  fi

  rm -rf "$DIR"
}

TMP="$(make_tmp unknown_hash)"
sed -i 's/sha256:[a-f0-9]\{64\}/UNKNOWN_HASH/1' "$TMP/_truth/receipts/MN_001.json"
expect_fail "UNKNOWN_HASH injection" "$TMP"

TMP="$(make_tmp duplicate_hash)"
H="$(jq -r '.receipt_hash // .hash' "$TMP/_truth/receipts/MN_001.json")"
jq --arg h "$H" '.receipt_hash=$h' "$TMP/_truth/receipts/MN_002.json" > "$TMP/_truth/receipts/MN_002.tmp"
mv "$TMP/_truth/receipts/MN_002.tmp" "$TMP/_truth/receipts/MN_002.json"
expect_fail "duplicate receipt hash" "$TMP"

TMP="$(make_tmp delete_leaf)"
rm -f "$TMP/_truth/receipts/MN_001.json"
expect_fail "delete receipt leaf" "$TMP"

TMP="$(make_tmp tamper_root)"
echo "sha256:deadbeef" > "$TMP/_truth/merkle/root.txt"
expect_fail "tamper merkle root" "$TMP"

TMP="$(make_tmp reorder_manifest)"
jq '.leaves |= reverse' "$TMP/_truth/merkle/manifest.json" > "$TMP/_truth/merkle/manifest.tmp"
mv "$TMP/_truth/merkle/manifest.tmp" "$TMP/_truth/merkle/manifest.json"
expect_fail "reorder manifest leaves" "$TMP"

TMP="$(make_tmp missing_card_line)"
jq 'del(.extracted_line)' "$TMP/_truth/cards/MN_001.card.json" > "$TMP/_truth/cards/MN_001.tmp"
mv "$TMP/_truth/cards/MN_001.tmp" "$TMP/_truth/cards/MN_001.card.json"
expect_fail "missing card extracted_line" "$TMP"

echo
echo "RESULT pass=$PASS fail=$FAIL"

if [ "$FAIL" -gt 0 ]; then
  echo "ADVERSARIAL_MATRIX_FAIL"
  exit 1
fi

echo "ADVERSARIAL_MATRIX_OK"
