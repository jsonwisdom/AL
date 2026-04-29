#!/usr/bin/env bash
set -euo pipefail

# ALMS Aggregation Layer v1
# Offline deterministic Merkle batch builder.
# No RPC. No signing. No chain contact. No financial surface.

EPOCH="${1:-2026-Q2}"
WITNESS_DIR="${WITNESS_DIR:-_truth/attest/witness}"
OUT_DIR="${OUT_DIR:-_truth/attest/batch}"
OUT_FILE="$OUT_DIR/alms_batch_${EPOCH}.json"

fail() {
  echo "FAIL batch_build_failed reason=$1" >&2
  exit 1
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "missing_command_$1"
}

need_cmd jq
need_cmd sha256sum
need_cmd xxd

[ -d "$WITNESS_DIR" ] || fail "missing_witness_dir"
mkdir -p "$OUT_DIR"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

find "$WITNESS_DIR" -maxdepth 1 -type f -name '*.json' -printf '%f\n' | LC_ALL=C sort > "$tmp/files.txt"
count="$(wc -l < "$tmp/files.txt" | tr -d ' ')"
[ "$count" -gt 0 ] || fail "no_witness_files"

: > "$tmp/leaves.tsv"
while IFS= read -r file; do
  src="$WITNESS_DIR/$file"
  jq -cS . "$src" > "$tmp/canonical.json" || fail "invalid_json_$file"
  leaf="$(sha256sum "$tmp/canonical.json" | awk '{print $1}')"
  printf '%s\t0x%s\n' "$file" "$leaf" >> "$tmp/leaves.tsv"
done < "$tmp/files.txt"

awk -F '\t' '{print substr($2,3)}' "$tmp/leaves.tsv" > "$tmp/level.hex"

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

merkle_root="0x$(cat "$tmp/level.hex")"
batch_root="0x$(printf '%s' "${merkle_root#0x}" | xxd -r -p | sha256sum | awk '{print $1}')"

jq -n \
  --arg epoch "$EPOCH" \
  --arg merkle_root "$merkle_root" \
  --arg batch_root "$batch_root" \
  --slurpfile leaf_rows <(awk -F '\t' '{print "{\"file\":\"" $1 "\",\"hash\":\"" $2 "\"}"}' "$tmp/leaves.tsv" | jq -s '.') \
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
      witness_files: ($leaf_rows[0] | map(.file)),
      count: ($leaf_rows[0] | length),
      hash_algorithm: "sha256",
      canonicalization: "jq -cS",
      ordering: "LC_ALL=C filename sort"
    },
    merkle: {
      construction: "binary_sha256_raw_32_byte_concat_duplicate_last_if_odd",
      leaf_hashes: ($leaf_rows[0] | map(.hash)),
      root: $merkle_root
    },
    batch_root: $batch_root,
    tx: {
      status: "NOT_SUBMITTED",
      tx_hash: null,
      basescan_url: null
    }
  }' > "$OUT_FILE.tmp"

jq -cS . "$OUT_FILE.tmp" > "$OUT_FILE"
rm -f "$OUT_FILE.tmp"

echo "BATCH_BUILT epoch=$EPOCH count=$count root=$batch_root file=$OUT_FILE"
