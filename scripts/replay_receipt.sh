#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "usage: $0 <receipt_json> <source_file>" >&2
  exit 64
fi

RECEIPT="$1"
SOURCE_FILE="$2"

[ -f "$RECEIPT" ] || { echo "CW_REPLAY_WAIT verdict=INDETERMINATE reason=RECEIPT_UNAVAILABLE"; exit 3; }

RH="$(jq -r '.receipt_hash' "$RECEIPT")"

if [ ! -f "$SOURCE_FILE" ]; then
  echo "CW_REPLAY_WAIT verdict=INDETERMINATE reason=SOURCE_UNAVAILABLE receipt_hash=$RH"
  exit 3
fi

FETCH_URI="$(jq -r '.fetch_uri' "$RECEIPT")"
GOLDEN_STORED="$(jq -r '.golden_uri' "$RECEIPT")"
POLICY_STORED="$(jq -r '.policy_hash' "$RECEIPT")"
SOV_STORED="$(jq -r '.sovereign_hash' "$RECEIPT")"
URI_STORED="$(jq -r '.uri_hash' "$RECEIPT")"
CONTENT_STORED="$(jq -r '.content_hash' "$RECEIPT")"

sha_hex() { sha256sum | awk '{print $1}'; }

fail() {
  echo "CW_REPLAY_ERR root=jaywisdom.eth chain=base policy=golden-uri-v1 verdict=FAIL reason=$1 receipt_hash=$RH"
  exit 2
}

GOLDEN_NOW="$(./scripts/canonicalize_uri.sh "$FETCH_URI")"
[ "$GOLDEN_NOW" = "$GOLDEN_STORED" ] || fail "GOLDEN_URI_MISMATCH"

POLICY_JSON="$(jq -cS -n '{
  uri_policy:"golden-uri-v1",
  strip_params:["utm","utm_*","ref","fbclid","gclid","mc_cid","mc_eid"],
  preserve_params:["id","file","year","doc","page","version"]
}')"

SOVEREIGN_JSON="$(jq -cS '.sovereign' "$RECEIPT")"

POLICY_HASH="sha256:$(printf 'CW-POLICY-v1%s' "$POLICY_JSON" | sha_hex)"
SOVEREIGN_HASH="sha256:$(printf 'CW-SOVEREIGN-v1%s' "$SOVEREIGN_JSON" | sha_hex)"
URI_HASH="sha256:$(printf 'CW-URI-v1%s' "$GOLDEN_NOW" | sha_hex)"
CONTENT_HASH="sha256:$(cat "$SOURCE_FILE" | { printf 'CW-CONTENT-v1'; cat; } | sha_hex)"

[ "$POLICY_HASH" = "$POLICY_STORED" ] || fail "POLICY_HASH_MISMATCH"
[ "$SOVEREIGN_HASH" = "$SOV_STORED" ] || fail "SOVEREIGN_HASH_MISMATCH"
[ "$URI_HASH" = "$URI_STORED" ] || fail "URI_HASH_MISMATCH"
[ "$CONTENT_HASH" = "$CONTENT_STORED" ] || fail "CONTENT_HASH_MISMATCH"

RECEIPT_HASH="sha256:$(python3 - "$POLICY_HASH" "$SOVEREIGN_HASH" "$URI_HASH" "$CONTENT_HASH" <<'PY'
import sys, hashlib
parts = ["CW-RECEIPT-v1"] + sys.argv[1:]
b = b""
for p in parts:
    x = p.encode()
    b += len(x).to_bytes(8, "big") + x
print(hashlib.sha256(b).hexdigest())
PY
)"

[ "$RECEIPT_HASH" = "$RH" ] || fail "RECEIPT_HASH_MISMATCH"

echo "CW_REPLAY_OK root=jaywisdom.eth chain=base policy=golden-uri-v1 verdict=PASS receipt_hash=$RH"
