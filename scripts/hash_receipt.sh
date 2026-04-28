#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 3 ]; then
  echo "usage: $0 <fetch_uri> <source_file> <output_receipt_json>" >&2
  exit 64
fi

FETCH_URI="$1"
SOURCE_FILE="$2"
OUT="$3"

[ -f "$SOURCE_FILE" ] || { echo "CW_REPLAY_WAIT reason=SOURCE_UNAVAILABLE file=$SOURCE_FILE" >&2; exit 2; }

GOLDEN_URI="$(./scripts/canonicalize_uri.sh "$FETCH_URI")"

POLICY_JSON="$(jq -cS -n '{
  uri_policy:"golden-uri-v1",
  strip_params:["utm","utm_*","ref","fbclid","gclid","mc_cid","mc_eid"],
  preserve_params:["id","file","year","doc","page","version"]
}')"

SOVEREIGN_JSON="$(jq -cS -n '{
  ens_root:"jaywisdom.eth",
  ens_alias:"jaywisdom.base.eth",
  chain:"base",
  chain_id:8453,
  sovereign_epoch:"2026-Q2",
  authorized_signer:"0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8"
}')"

sha_hex() {
  sha256sum | awk '{print $1}'
}

POLICY_HASH="sha256:$(printf 'CW-POLICY-v1%s' "$POLICY_JSON" | sha_hex)"
SOVEREIGN_HASH="sha256:$(printf 'CW-SOVEREIGN-v1%s' "$SOVEREIGN_JSON" | sha_hex)"
URI_HASH="sha256:$(printf 'CW-URI-v1%s' "$GOLDEN_URI" | sha_hex)"
CONTENT_HASH="sha256:$(cat "$SOURCE_FILE" | { printf 'CW-CONTENT-v1'; cat; } | sha_hex)"

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

jq -cS -n \
  --arg kernel "cw-sovereign-replay-kernel-v1" \
  --arg fetch_uri "$FETCH_URI" \
  --arg golden_uri "$GOLDEN_URI" \
  --arg policy_hash "$POLICY_HASH" \
  --arg sovereign_hash "$SOVEREIGN_HASH" \
  --arg uri_hash "$URI_HASH" \
  --arg content_hash "$CONTENT_HASH" \
  --arg receipt_hash "$RECEIPT_HASH" \
  --argjson sovereign "$SOVEREIGN_JSON" \
  '{
    kernel:$kernel,
    fetch_uri:$fetch_uri,
    golden_uri:$golden_uri,
    policy_hash:$policy_hash,
    sovereign_hash:$sovereign_hash,
    uri_hash:$uri_hash,
    content_hash:$content_hash,
    receipt_hash:$receipt_hash,
    sovereign:$sovereign
  }' > "$OUT"

echo "CW_RECEIPT_HASHED receipt_hash=$RECEIPT_HASH out=$OUT"
