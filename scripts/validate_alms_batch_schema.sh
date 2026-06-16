#!/usr/bin/env bash
set -euo pipefail

# ALMS Batch Schema Validator V1
# Enforces docs/spec/ALMS_BATCH_V1.md

MANIFEST="$1"

fail() {
  echo "FAIL $1" >&2
  exit 1
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "missing_command cmd=$1"
}

need_cmd jq
need_cmd grep

[ -f "$MANIFEST" ] || fail "missing_manifest"
jq -e . "$MANIFEST" >/dev/null || fail "invalid_json"

# Top-level keys exact match
jq -r 'keys_unsorted[]' "$MANIFEST" | LC_ALL=C sort > /tmp/keys.txt
printf "%s\n" batch_root batch_type boundaries epoch inputs merkle tx version | LC_ALL=C sort > /tmp/expected.txt
cmp -s /tmp/keys.txt /tmp/expected.txt || fail "invalid_top_level_keys"

# batch_type
[ "$(jq -r '.batch_type' "$MANIFEST")" = "ALMS_ATTESTATION_BATCH" ] || fail "invalid_batch_type"

# version
[ "$(jq -r '.version' "$MANIFEST")" = "1" ] || fail "invalid_version"

# boundaries exact match
jq -cS '.boundaries' "$MANIFEST" > /tmp/b1
printf '{"chain_contact":false,"execution_surface":"offline_terminal_math_only","financial_surface":false,"rpc":false,"signing":false}' > /tmp/b2
cmp -s /tmp/b1 /tmp/b2 || fail "invalid_boundaries"

# inputs fields
jq -e '.inputs.witness_files and .inputs.count and .inputs.hash_algorithm and .inputs.canonicalization and .inputs.ordering' "$MANIFEST" >/dev/null || fail "invalid_inputs_structure"

# no relative paths
jq -r '.inputs.witness_files[]' "$MANIFEST" | grep -E '\.|/' && fail "invalid_witness_path" || true

# merkle structure
jq -e '.merkle.leaf_hashes and .merkle.root and .merkle.construction' "$MANIFEST" >/dev/null || fail "invalid_merkle_structure"

# tx status
status="$(jq -r '.tx.status' "$MANIFEST")"
[ "$status" = "NOT_SUBMITTED" ] || [ "$status" = "SUBMITTED" ] || fail "invalid_tx_status"

echo "SCHEMA_OK"
