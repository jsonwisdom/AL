#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

PREVIEW_FILE="${1:-}"
OUT_DIR="_truth/attest/witness"
OUT_FILE="${2:-$OUT_DIR/base_alms_root_2026_04_v2_witness.json}"

if [[ -z "$PREVIEW_FILE" ]]; then
  echo "FAIL no_preview_file_provided"
  echo "Usage: $0 _truth/attest/base_alms_attest_2026_04_v2_preview_*.txt [out.json]"
  exit 1
fi

if [[ ! -f "$PREVIEW_FILE" ]]; then
  echo "FAIL preview_file_not_found=$PREVIEW_FILE"
  exit 1
fi

require_line() {
  local key="$1"
  if ! grep -qE "^${key}(=|$)" "$PREVIEW_FILE"; then
    echo "FAIL missing_required_line=$key"
    exit 1
  fi
}

extract() {
  local key="$1"
  grep -E "^${key}=" "$PREVIEW_FILE" | head -n 1 | sed "s/^${key}=//"
}

require_line "schema_uid"
require_line "merkle_root"
require_line "func_sig"
require_line "request"
require_line "data"
require_line "NO_SIGNER_USED"
require_line "NO_TX_SENT"

SCHEMA_UID="$(extract schema_uid)"
MERKLE_ROOT="$(extract merkle_root)"
FUNC_SIG="$(extract func_sig)"
REQUEST="$(extract request)"
DATA="$(extract data)"

if [[ -z "$SCHEMA_UID" || -z "$MERKLE_ROOT" || -z "$FUNC_SIG" || -z "$REQUEST" || -z "$DATA" ]]; then
  echo "FAIL malformed_preview_empty_required_value"
  exit 1
fi

CAST_VERSION="$(cast --version 2>/dev/null | head -n 1 || echo unavailable)"
mkdir -p "$OUT_DIR"

jq -nS \
  --arg witness_type "ALMS_BASE_ATTEST_2026_04_V2" \
  --arg chain_id "8453" \
  --arg network "base" \
  --arg rpc_label "REDACTED_RPC" \
  --arg cast_version "$CAST_VERSION" \
  --arg script "scripts/attest_base_alms_root_2026_04_v2.sh" \
  --arg eas_contract "0xPLACEHOLDER_CONTRACT" \
  --arg schema_registry "0xPLACEHOLDER_SCHEMA_REGISTRY" \
  --arg schema_uid "$SCHEMA_UID" \
  --arg merkle_root "$MERKLE_ROOT" \
  --arg epoch "2026-04-v2" \
  --arg mode "GENESIS" \
  --arg func_sig "$FUNC_SIG" \
  --arg request "$REQUEST" \
  --arg data "$DATA" \
  --arg preview_file "$PREVIEW_FILE" \
  '{
    witness_type: $witness_type,
    version: 1,
    env: {
      chain_id: $chain_id,
      network: $network,
      rpc_label: $rpc_label,
      tooling: {
        cast_version: $cast_version,
        script: $script
      }
    },
    contracts: {
      eas_contract: $eas_contract,
      schema_registry: $schema_registry,
      schema_uid: $schema_uid
    },
    alms: {
      merkle_root: $merkle_root,
      epoch: $epoch,
      mode: $mode,
      witness_count: 1
    },
    attestation: {
      func_sig: $func_sig,
      request: $request,
      data: $data,
      recipient: "0x0000000000000000000000000000000000000000",
      expiration_time: "0",
      revocable: true,
      ref_uid: "0x0000000000000000000000000000000000000000000000000000000000000000",
      value: "0"
    },
    preview_source: {
      file: $preview_file,
      extraction_script: "SHELL:extract_preview_witness_v1",
      lines_required: [
        "schema_uid",
        "merkle_root",
        "func_sig",
        "request",
        "data",
        "NO_SIGNER_USED",
        "NO_TX_SENT"
      ]
    },
    tx: {
      status: "NOT_SUBMITTED",
      tx_hash: null,
      block_number: null,
      basescan_url: null
    }
  }' > "$OUT_FILE"

HASH="$(jq -cS . "$OUT_FILE" | sha256sum | awk '{print $1}')"
echo "WITNESS_OK file=$OUT_FILE hash=$HASH status=NOT_SUBMITTED"
