#!/usr/bin/env bash
set -euo pipefail

# ALMS 2026-Q2 Portable Verification Entrypoint
# Read-only. Offline. No RPC. No signing. No mutation.

EPOCH="2026-Q2"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

fail() {
  echo "VERIFY_FAIL $1" >&2
  exit 1
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "missing_command cmd=$1"
}

need_file() {
  [ -f "$1" ] || fail "missing_file file=$1"
}

need_cmd jq
need_cmd sha256sum
need_cmd xxd
need_cmd cast

need_file "scripts/validate_alms_batch_schema.sh"
need_file "scripts/verify_alms_batch.sh"
need_file "scripts/generate_alms_ens_calldata.sh"
need_file "scripts/verify_alms_ens_calldata.sh"
need_file "scripts/audit_alms_fabric.sh"
need_file "_truth/attest/batch/alms_batch_${EPOCH}.json"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "ALMS_VERIFY_START epoch=$EPOCH"

# 1. Schema gate + batch verification.
STRICT_MODE=1 scripts/verify_alms_batch.sh "$EPOCH"

# 2. Deterministic calldata generation into temp file only.
scripts/generate_alms_ens_calldata.sh "$EPOCH" > "$TMP/ens_calldata_${EPOCH}.json"

# 3. Byte-exact calldata verification.
scripts/verify_alms_ens_calldata.sh "$TMP/ens_calldata_${EPOCH}.json"

# 4. Optional adversarial audit.
if [ "${RUN_AUDIT:-0}" = "1" ]; then
  scripts/audit_alms_fabric.sh "$EPOCH"
fi

root="$(jq -r '.batch_root' "_truth/attest/batch/alms_batch_${EPOCH}.json")"
echo "ALMS_VERIFY_OK epoch=$EPOCH root=$root"
