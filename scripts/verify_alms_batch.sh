#!/usr/bin/env bash
set -euo pipefail

# ALMS Batch Verifier v1
# Offline deterministic verifier.
# No RPC. No signing. No chain contact. No financial surface.
# Reads manifest + witnesses. Mutates nothing.

EPOCH="${1:-}"
BATCH_DIR="${BATCH_DIR:-_truth/attest/batch}"
WITNESS_DIR="${WITNESS_DIR:-_truth/attest/witness}"
STRICT_MODE="${STRICT_MODE:-1}"

[ -n "$EPOCH" ] || { echo "FAIL missing_epoch" >&2; exit 1; }

MANIFEST="$BATCH_DIR/alms_batch_${EPOCH}.json"

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

need_cmd jq
need_cmd sha256sum
need_cmd xxd
need_cmd awk
need_cmd sort
need_cmd comm

[ -f "$MANIFEST" ] || fail "missing_manifest file=$MANIFEST"
jq -e . "$MANIFEST" >/dev/null || fail "invalid_manifest_json file=$MANIFEST"
[ -d "$WITNESS_DIR" ] || fail "missing_witness_dir dir=$WITNESS_DIR"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

batch_type="$(jq -r '.batch_type // empty' "$MANIFEST")"
[ "$batch_type" = "ALMS_ATTESTATION_BATCH" ] || fail "invalid_batch_type got=${batch_type:-null}"

manifest_epoch="$(jq -r '.epoch // empty' "$MANIFEST")"
[ "$manifest_epoch" = "$EPOCH" ] || fail "epoch_mismatch expected=$EPOCH got=${manifest_epoch:-null}"

version="$(jq -r '.version // empty' "$MANIFEST")"
[ "$version" = "1" ] || fail "invalid_version got=${version:-null}"

for field in '.inputs.witness_files' '.inputs.count' '.merkle.leaf_hashes' '.merkle.root' '.batch_root' '.tx.status'; do
  jq -e "$field" "$MANIFEST" >/dev/null || fail "missing_required_field field=$field"
done

jq -r '.inputs.witness_files[]' "$MANIFEST" > "$tmp/manifest_files.txt" || fail "invalid_witness_files"
LC_ALL=C sort "$tmp/manifest_files.txt" > "$tmp/manifest_files.sorted"

if [ "$(wc -l < "$tmp/manifest_files.txt" | tr -d ' ')" != "$(uniq "$tmp/manifest_files.sorted" | wc -l | tr -d ' ')" ]; then
  fail "duplicate_witness_files"
fi

if ! cmp -s "$tmp/manifest_files.txt" "$tmp/manifest_files.sorted"; then
  fail "witness_order_not_lexicographic"
fi

manifest_count="$(jq -r '.inputs.count' "$MANIFEST")"
actual_manifest_count="$(wc -l < "$tmp/manifest_files.txt" | tr -d ' ')"
[ "$manifest_count" = "$actual_manifest_count" ] || fail "count_mismatch expected=$manifest_count got=$actual_manifest_count"
[ "$actual_manifest_count" -gt 0 ] || fail "empty_witness_list"

jq -r '.merkle.leaf_hashes[]' "$MANIFEST" > "$tmp/manifest_leaves.txt" || fail "invalid_leaf_hashes"
leaf_count="$(wc -l < "$tmp/manifest_leaves.txt" | tr -d ' ')"
[ "$leaf_count" = "$actual_manifest_count" ] || fail "leaf_count_mismatch expected=$actual_manifest_count got=$leaf_count"

paste "$tmp/manifest_files.txt" "$tmp/manifest_leaves.txt" > "$tmp/manifest_pairs.tsv"

: > "$tmp/recomputed_pairs.tsv"
while IFS=$'\t' read -r file expected_leaf; do
  [ -f "$WITNESS_DIR/$file" ] || fail "missing_witness_file file=$file"
  is_0x32 "$expected_leaf" || fail "invalid_leaf_hash_format file=$file hash=$expected_leaf"
  jq -cS . "$WITNESS_DIR/$file" > "$tmp/canonical.json" || fail "invalid_witness_json file=$file"
  got="0x$(sha256sum "$tmp/canonical.json" | awk '{print $1}')"
  [ "$got" = "$expected_leaf" ] || fail "leaf_hash_mismatch file=$file expected=$expected_leaf got=$got"
  printf '%s\t%s\n' "$file" "$got" >> "$tmp/recomputed_pairs.tsv"
done < "$tmp/manifest_pairs.tsv"

if [ "$STRICT_MODE" = "1" ]; then
  find "$WITNESS_DIR" -maxdepth 1 -type f -name '*.json' -printf '%f\n' | LC_ALL=C sort > "$tmp/actual_files.sorted"
  if ! cmp -s "$tmp/manifest_files.sorted" "$tmp/actual_files.sorted"; then
    comm -23 "$tmp/actual_files.sorted" "$tmp/manifest_files.sorted" > "$tmp/unexpected.txt" || true
    extra="$(tr '\n' ',' < "$tmp/unexpected.txt" | sed 's/,$//')"
    fail "unexpected_witness_files_present files=${extra:-unknown}"
  fi
fi

awk -F '\t' '{print substr($2,3)}' "$tmp/recomputed_pairs.tsv" > "$tmp/level.hex"

while [ "$(wc -l < "$tmp/level.hex" | tr -d ' ')" -gt 1 ]; do
  : > "$tmp/next.hex"
  mapfile -t nodes < "$tmp/level.hex"
  n="${#nodes[@]}"
  i=0
  while [ "$i" -lt "$n" ]; do
    left="${nodes[$i]}"
    if [ $((i + 1)) -lt "$n" ]; then
      right="${nodes[$((i + 1))]}"
    else
      right="$left"
    fi
    printf '%s%s' "$left" "$right" | xxd -r -p | sha256sum | awk '{print $1}' >> "$tmp/next.hex"
    i=$((i + 2))
  done
  mv "$tmp/next.hex" "$tmp/level.hex"
done

computed_merkle="0x$(cat "$tmp/level.hex")"
manifest_merkle="$(jq -r '.merkle.root' "$MANIFEST")"
is_0x32 "$manifest_merkle" || fail "invalid_merkle_root_format root=$manifest_merkle"
[ "$computed_merkle" = "$manifest_merkle" ] || fail "merkle_root_mismatch expected=$manifest_merkle got=$computed_merkle"

computed_batch="0x$(printf '%s' "${computed_merkle#0x}" | xxd -r -p | sha256sum | awk '{print $1}')"
manifest_batch="$(jq -r '.batch_root' "$MANIFEST")"
is_0x32 "$manifest_batch" || fail "invalid_batch_root_format root=$manifest_batch"
[ "$computed_batch" = "$manifest_batch" ] || fail "batch_root_mismatch expected=$manifest_batch got=$computed_batch"

tx_status="$(jq -r '.tx.status' "$MANIFEST")"
case "$tx_status" in
  NOT_SUBMITTED|SUBMITTED) ;;
  *) fail "invalid_tx_status status=$tx_status" ;;
esac

tx_hash="$(jq -r '.tx.tx_hash // empty' "$MANIFEST")"
if [ -n "$tx_hash" ]; then
  printf '%s' "$tx_hash" | grep -Eq '^0x[0-9a-fA-F]{64}$' || fail "invalid_tx_hash tx_hash=$tx_hash"
fi

basescan_url="$(jq -r '.tx.basescan_url // empty' "$MANIFEST")"
if [ -n "$basescan_url" ]; then
  printf '%s' "$basescan_url" | grep -Eq '^https://(www\.)?basescan\.org/tx/0x[0-9a-fA-F]{64}$' || fail "invalid_basescan_url url=$basescan_url"
fi

if [ "$tx_status" = "NOT_SUBMITTED" ]; then
  [ -z "$tx_hash" ] || fail "tx_hash_present_when_not_submitted"
  [ -z "$basescan_url" ] || fail "basescan_url_present_when_not_submitted"
fi

jq -cS 'del(.tx)' "$MANIFEST" > "$tmp/manifest_no_tx.json"
no_tx_hash="0x$(sha256sum "$tmp/manifest_no_tx.json" | awk '{print $1}')"

# Zero mutation witness: recompute tx-free canonical object from verified parts.
jq -n \
  --arg epoch "$EPOCH" \
  --arg merkle_root "$computed_merkle" \
  --arg batch_root "$computed_batch" \
  --slurpfile rows <(awk -F '\t' '{print "{\"file\":\"" $1 "\",\"hash\":\"" $2 "\"}"}' "$tmp/recomputed_pairs.tsv" | jq -s '.') \
  '{
    batch_type: "ALMS_ATTESTATION_BATCH",
    epoch: $epoch,
    version: 1,
    boundaries: {
      rpc: false,
      signing: false,
      chain_contact: false,
      financial_surface: false,
      execution_surface: "offline_terminal_math_only"
    },
    inputs: {
      witness_files: ($rows[0] | map(.file)),
      count: ($rows[0] | length),
      hash_algorithm: "sha256",
      canonicalization: "jq -cS",
      ordering: "LC_ALL=C filename sort"
    },
    merkle: {
      construction: "binary_sha256_raw_32_byte_concat_duplicate_last_if_odd",
      leaf_hashes: ($rows[0] | map(.hash)),
      root: $merkle_root
    },
    batch_root: $batch_root
  }' | jq -cS . > "$tmp/recomputed_no_tx.json"

recomputed_no_tx_hash="0x$(sha256sum "$tmp/recomputed_no_tx.json" | awk '{print $1}')"
[ "$no_tx_hash" = "$recomputed_no_tx_hash" ] || fail "manifest_no_tx_mismatch expected=$no_tx_hash got=$recomputed_no_tx_hash"

echo "BATCH_OK epoch=$EPOCH count=$actual_manifest_count root=$computed_batch"
