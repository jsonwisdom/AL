#!/usr/bin/env bash
set -euo pipefail

# ALMS ENS Calldata Verifier v1
# Offline deterministic verifier for generated calldata envelope files.
# No RPC. No signing. No chain contact. No mutation.

ENVELOPE="${1:-}"
BATCH_DIR="${BATCH_DIR:-_truth/attest/batch}"

fail() {
  echo "FAIL $1" >&2
  exit 1
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "missing_command cmd=$1"
}

is_0x32() {
  printf '%s' "$1" | grep -Eq '^0x[0-9a-f]{64}$'
}

hex_len_bytes() {
  local hex="$1"
  hex="${hex#0x}"
  echo $(( ${#hex} / 2 ))
}

pad_right_32() {
  local hex="$1"
  local rem=$(( ${#hex} % 64 ))
  if [ "$rem" -eq 0 ]; then
    printf '%s' "$hex"
  else
    printf '%s' "$hex"
    printf '%0.s0' $(seq 1 $((64 - rem)))
  fi
}

uint256_hex() {
  printf '%064x' "$1"
}

ascii_to_hex() {
  printf '%s' "$1" | xxd -p -c 256
}

keccak_hex() {
  local input_hex="$1"
  input_hex="${input_hex#0x}"
  cast keccak "0x${input_hex}" | tr 'A-F' 'a-f'
}

namehash_safe() {
  local name="$1"
  local node="0000000000000000000000000000000000000000000000000000000000000000"
  [ -n "$name" ] || fail "empty_ens_name"
  IFS='.' read -r -a labels <<< "$name"
  for (( i=${#labels[@]}-1; i>=0; i-- )); do
    local label="${labels[$i]}"
    [ -n "$label" ] || fail "invalid_ens_name name=$name"
    local label_hex label_hash combined
    label_hex="$(ascii_to_hex "$label")"
    label_hash="$(keccak_hex "$label_hex")"
    label_hash="${label_hash#0x}"
    combined="${node}${label_hash}"
    node="$(keccak_hex "$combined")"
    node="${node#0x}"
  done
  printf '0x%s' "$node"
}

abi_encode_set_text() {
  local node="$1"
  local key="$2"
  local value="$3"

  local selector="59d1d43c"
  local node_hex="${node#0x}"
  local key_hex value_hex key_len value_len key_blob value_blob key_offset value_offset

  key_hex="$(ascii_to_hex "$key")"
  value_hex="$(ascii_to_hex "$value")"
  key_len="$(hex_len_bytes "$key_hex")"
  value_len="$(hex_len_bytes "$value_hex")"

  key_blob="$(uint256_hex "$key_len")$(pad_right_32 "$key_hex")"
  value_blob="$(uint256_hex "$value_len")$(pad_right_32 "$value_hex")"

  key_offset=96
  value_offset=$((96 + ${#key_blob} / 2))

  printf '0x%s%s%s%s%s%s' \
    "$selector" \
    "$node_hex" \
    "$(uint256_hex "$key_offset")" \
    "$(uint256_hex "$value_offset")" \
    "$key_blob" \
    "$value_blob"
}

[ -n "$ENVELOPE" ] || fail "missing_envelope_file"
[ -f "$ENVELOPE" ] || fail "missing_envelope_file file=$ENVELOPE"

need_cmd jq
need_cmd xxd
need_cmd cast

jq -e . "$ENVELOPE" >/dev/null || fail "invalid_calldata_json"

jq -r 'keys_unsorted[]' "$ENVELOPE" | LC_ALL=C sort > /tmp/alms_calldata_keys.$$ 
printf "%s\n" batch_root calldata ens_key ens_name namehash version | LC_ALL=C sort > /tmp/alms_calldata_expected.$$ 
cmp -s /tmp/alms_calldata_keys.$$ /tmp/alms_calldata_expected.$$ || fail "invalid_calldata_keys"
rm -f /tmp/alms_calldata_keys.$$ /tmp/alms_calldata_expected.$$

version="$(jq -r '.version' "$ENVELOPE")"
[ "$version" = "1" ] || fail "invalid_version version=$version"

ens_name="$(jq -r '.ens_name' "$ENVELOPE")"
ens_key="$(jq -r '.ens_key' "$ENVELOPE")"
batch_root="$(jq -r '.batch_root' "$ENVELOPE")"
namehash_manifest="$(jq -r '.namehash' "$ENVELOPE")"
calldata_manifest="$(jq -r '.calldata' "$ENVELOPE")"

printf '%s' "$ens_name" | grep -Eq '^[a-z0-9-]+(\.[a-z0-9-]+)+$' || fail "invalid_ens_name name=$ens_name"
printf '%s' "$ens_key" | grep -Eq '^witness\.alms\.base\.[0-9]{4}\.Q[1-4]$' || fail "invalid_ens_key key=$ens_key"
is_0x32 "$batch_root" || fail "invalid_batch_root root=$batch_root"
is_0x32 "$namehash_manifest" || fail "invalid_namehash namehash=$namehash_manifest"
printf '%s' "$calldata_manifest" | grep -Eq '^0x[0-9a-f]+$' || fail "invalid_calldata_format"

key_epoch="$(printf '%s' "$ens_key" | sed -E 's/^witness\.alms\.base\.([0-9]{4})\.Q([1-4])$/\1-Q\2/')"
BATCH_MANIFEST="$BATCH_DIR/alms_batch_${key_epoch}.json"
[ -f "$BATCH_MANIFEST" ] || fail "missing_batch_manifest file=$BATCH_MANIFEST"

batch_manifest_root="$(jq -r '.batch_root // empty' "$BATCH_MANIFEST")"
[ "$batch_manifest_root" = "$batch_root" ] || fail "batch_root_mismatch expected=$batch_manifest_root got=$batch_root"

namehash_got="$(namehash_safe "$ens_name")"
[ "$namehash_got" = "$namehash_manifest" ] || fail "namehash_mismatch expected=$namehash_manifest got=$namehash_got"

calldata_got="$(abi_encode_set_text "$namehash_got" "$ens_key" "$batch_root")"
[ "$calldata_got" = "$calldata_manifest" ] || fail "calldata_mismatch expected=$calldata_manifest got=$calldata_got"

echo "ENS_CALLDATA_OK key=$ens_key root=$batch_root"
