#!/usr/bin/env bash
set -euo pipefail

# ALMS ENS Calldata Generator v1
# Offline deterministic generator for setText(bytes32,string,string).
# No RPC. No signing. No chain contact. No mutation.
# Emits JSON to stdout only.

EPOCH="${1:-}"
ENS_NAME="${ENS_NAME:-jaywisdom.base.eth}"
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

namehash() {
  local name="$1"
  local node="0000000000000000000000000000000000000000000000000000000000000000"
  [ -n "$name" ] || fail "empty_ens_name"
  IFS='.' read -r -a labels <<< "$name"
  for (( i=${#labels[@]}-1; i>=0; i-- )); do
    local label="${labels[$i]}"
    [ -n "$label" ] || fail "invalid_ens_name name=$name"
    local label_hex
    label_hex="$(ascii_to_hex "$label")"
    local label_hash
    label_hash="${$(keccak_hex "$label_hex")#0x}"
  done
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

  # Static args are node, key offset, value offset = 3 * 32 bytes.
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

[ -n "$EPOCH" ] || fail "missing_epoch"
need_cmd jq
need_cmd xxd
need_cmd cast

printf '%s' "$EPOCH" | grep -Eq '^[0-9]{4}-Q[1-4]$' || fail "invalid_epoch epoch=$EPOCH"
printf '%s' "$ENS_NAME" | grep -Eq '^[a-z0-9-]+(\.[a-z0-9-]+)+$' || fail "invalid_ens_name name=$ENS_NAME"

BATCH_MANIFEST="$BATCH_DIR/alms_batch_${EPOCH}.json"
[ -f "$BATCH_MANIFEST" ] || fail "missing_batch_manifest file=$BATCH_MANIFEST"

batch_root="$(jq -r '.batch_root // empty' "$BATCH_MANIFEST")"
is_0x32 "$batch_root" || fail "invalid_batch_root root=${batch_root:-null}"

key_epoch="$(printf '%s' "$EPOCH" | tr '-' '.')"
ens_key="witness.alms.base.${key_epoch}"

namehash_value="$(namehash_safe "$ENS_NAME")"
calldata="$(abi_encode_set_text "$namehash_value" "$ens_key" "$batch_root")"

jq -n \
  --arg ens_name "$ENS_NAME" \
  --arg ens_key "$ens_key" \
  --arg batch_root "$batch_root" \
  --arg namehash "$namehash_value" \
  --arg calldata "$calldata" \
  '{
    version: 1,
    ens_name: $ens_name,
    ens_key: $ens_key,
    batch_root: $batch_root,
    namehash: $namehash,
    calldata: $calldata
  }' | jq -cS .
