#!/usr/bin/env bash
set -euo pipefail

RECEIPT="${1:-_truth/anchors/ALMS_EAS_FAST_ANCHOR_MANUAL.json}"
EXPECTED_CHAIN_ID="8453"
EXPECTED_SIGNER="0xa380552a27b0a5a2874ea7aa52cac09f542002e8"
EXPECTED_SCHEMA_UID="0xfa9437b2b101ca96baae516b089d58c2b781e832ffbafd28c4c6d4206ca87255"
EXPECTED_EAS="0x4200000000000000000000000000000000000021"
EXPECTED_MANUAL="docs/manuals/ALMS_EAS_FAST_ANCHOR_MANUAL.md"

need(){ command -v "$1" >/dev/null 2>&1 || { echo "MISSING_DEP:$1" >&2; exit 2; }; }
need jq
need curl
need sha256sum

hex32_re='^0x[0-9a-fA-F]{64}$'
addr_re='^0x[0-9a-fA-F]{40}$'
commit_re='^[0-9a-fA-F]{40}$'

fail(){ echo "ALMS_EAS_FAST_ANCHOR_VERIFY_FAIL:$1" >&2; exit 1; }
pass(){ echo "ALMS_EAS_FAST_ANCHOR_VERIFY_PASS"; }

[ -f "$RECEIPT" ] || fail "missing_receipt:$RECEIPT"

schema_uid=$(jq -r '.schema_uid // empty' "$RECEIPT")
attestation_uid=$(jq -r '.attestation_uid // empty' "$RECEIPT")
tx_hash=$(jq -r '.tx_hash // empty' "$RECEIPT")
signer=$(jq -r '.signer // empty' "$RECEIPT")
commit=$(jq -r '.commit // empty' "$RECEIPT")
content_hash=$(jq -r '.content_hash // empty' "$RECEIPT")
archive_sha=$(jq -r '.archiveSha256 // empty' "$RECEIPT")
byte_size=$(jq -r '.byte_size // empty' "$RECEIPT")
chain_id=$(jq -r '.chain_id // empty' "$RECEIPT")
status=$(jq -r '.status // empty' "$RECEIPT")
tx_receipt_status=$(jq -r '.tx_receipt_status // empty' "$RECEIPT")

[[ "$schema_uid" =~ $hex32_re ]] || fail "invalid_schema_uid"
[[ "$attestation_uid" =~ $hex32_re ]] || fail "invalid_attestation_uid"
[[ "$tx_hash" =~ $hex32_re ]] || fail "invalid_tx_hash"
[[ "$content_hash" =~ $hex32_re ]] || fail "invalid_content_hash"
[[ "$archive_sha" =~ $hex32_re ]] || fail "invalid_archiveSha256"
[[ "$signer" =~ $addr_re ]] || fail "invalid_signer"
[[ "$commit" =~ $commit_re ]] || fail "invalid_commit"
[[ "$chain_id" == "$EXPECTED_CHAIN_ID" ]] || fail "wrong_chain_id:$chain_id"
[[ "${signer,,}" == "$EXPECTED_SIGNER" ]] || fail "wrong_signer:$signer"
[[ "${schema_uid,,}" == "$EXPECTED_SCHEMA_UID" ]] || fail "wrong_schema_uid:$schema_uid"
[[ "$status" == "ATTESTED_CONFIRMED" ]] || fail "wrong_status:$status"
[[ "$tx_receipt_status" == "1" ]] || fail "wrong_tx_receipt_status:$tx_receipt_status"
[[ "$content_hash" == "$archive_sha" ]] || fail "content_hash_archive_mismatch"

raw_url="https://raw.githubusercontent.com/jsonwisdom/AL/${commit}/${EXPECTED_MANUAL}"
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT
curl -fsSL "$raw_url" -o "$tmp" || fail "fetch_manual_failed:$raw_url"

computed_size=$(wc -c < "$tmp" | tr -d ' ')
computed_hash="0x$(sha256sum "$tmp" | awk '{print $1}')"

[[ "$computed_size" == "$byte_size" ]] || fail "byte_size_mismatch:computed=$computed_size receipt=$byte_size"
[[ "${computed_hash,,}" == "${content_hash,,}" ]] || fail "sha256_mismatch:computed=$computed_hash receipt=$content_hash"

jq -n \
  --arg receipt "$RECEIPT" \
  --arg chain_id "$chain_id" \
  --arg signer "$signer" \
  --arg schema_uid "$schema_uid" \
  --arg attestation_uid "$attestation_uid" \
  --arg tx_hash "$tx_hash" \
  --arg commit "$commit" \
  --arg content_hash "$content_hash" \
  --arg byte_size "$byte_size" \
  --arg eas_contract "$EXPECTED_EAS" \
  '{status:"PASS", receipt:$receipt, chain_id:$chain_id, signer:$signer, schema_uid:$schema_uid, attestation_uid:$attestation_uid, tx_hash:$tx_hash, commit:$commit, content_hash:$content_hash, byte_size:($byte_size|tonumber), eas_contract:$eas_contract, no_ghost_anchor:true}'

pass
