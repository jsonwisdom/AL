#!/usr/bin/env bash
set -euo pipefail

INPUT="${1:-}"
OUT_DIR="arcade/zk/intents"
SCHEMA="arcade/zk/schemas/leaf_preimage_schema_v2.json"

mkdir -p "$OUT_DIR"

[[ -f "$INPUT" ]] || { echo "ERROR_HYDRATION_FAILURE: missing input"; exit 1; }

DATA_SHA="$(sha256sum "$INPUT" | awk '{print $1}')"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
OUT="$OUT_DIR/prover_output_intent_${TS}.json"

jq -e '
  type == "object" and
  has("player_id") and
  has("episode_id") and
  has("fragment_id") and
  has("replay_count") and
  has("egg_id")
' "$INPUT" >/dev/null || {
  echo "INPUT_REJECTED"
  exit 1
}

jq -nc \
  --arg ts "$TS" \
  --arg data_sha "$DATA_SHA" \
  '{
    intent_type:"PROVER_OUTPUT_INTENT",
    timestamp_utc:$ts,
    data_sha256:$data_sha,
    backend_state:"BLOCKED_BY_BACKEND",
    proof_state:"NOT_GENERATED",
    verifier_state:"NOT_EXECUTED",
    verdict:"SYSTEM_PENDING"
  }' > "$OUT"

echo "PROVER_OUTPUT_INTENT_EMITTED"
echo "$OUT"
