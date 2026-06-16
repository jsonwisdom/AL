#!/usr/bin/env bash
set -euo pipefail

: "${EAS_GRAPHQL_ENDPOINT:?Set EAS_GRAPHQL_ENDPOINT, e.g. https://your-service.onrender.com/graphql}"

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT_DIR="${OUT_DIR:-_truth/eas-indexer/live-probes/${STAMP}}"
mkdir -p "$OUT_DIR"

UID_ORIGINAL="0x4d6a7df50cba18e1086820732c158274b51adf9f17722c40d55fd3f73b5d6874"
UID_CORRECTION="0xcc3e5448328c3ca29282e05bacbc4dc96d4cd533f7144d0a437a6f39cceec1f1"

cat > "$OUT_DIR/query.graphql" <<'GRAPHQL'
query ALMSReplayOfficial($uids: [String!]) {
  attestations(
    where: { id: { in: $uids } }
    take: 10
  ) {
    id
    schemaId
    attester
    recipient
    time
    revocationTime
    revoked
    txid
    decodedDataJson
  }
}
GRAPHQL

cat > "$OUT_DIR/variables.json" <<JSON
{
  "uids": [
    "$UID_ORIGINAL",
    "$UID_CORRECTION"
  ]
}
JSON

AUTH_ARGS=()
if [[ -n "${EAS_GRAPHQL_TOKEN:-}" ]]; then
  AUTH_ARGS=(-H "Authorization: Bearer ${EAS_GRAPHQL_TOKEN}")
fi

python3 - <<'PY' "$OUT_DIR/query.graphql" "$OUT_DIR/variables.json" > "$OUT_DIR/payload.json"
import json, sys
query_path, vars_path = sys.argv[1:3]
with open(query_path, "r", encoding="utf-8") as f:
    query = f.read()
with open(vars_path, "r", encoding="utf-8") as f:
    variables = json.load(f)
print(json.dumps({"query": query, "variables": variables}, indent=2))
PY

HTTP_CODE=$(curl -sS -L \
  -X POST "$EAS_GRAPHQL_ENDPOINT" \
  -H "Content-Type: application/json" \
  "${AUTH_ARGS[@]}" \
  --data-binary "@$OUT_DIR/payload.json" \
  -o "$OUT_DIR/response.json" \
  -w "%{http_code}")

cat > "$OUT_DIR/receipt.json" <<JSON
{
  "receipt_type": "ISSUE_328_UID_REPLAY_PROBE",
  "generated_utc": "$STAMP",
  "repo": "jsonwisdom/AL",
  "issue": 328,
  "endpoint": "$EAS_GRAPHQL_ENDPOINT",
  "http_code": "$HTTP_CODE",
  "uids": [
    "$UID_ORIGINAL",
    "$UID_CORRECTION"
  ],
  "anchor_state": "YELLOW_READY",
  "no_fake_green": true,
  "green_gate_note": "Only promote after response.json contains expected UID records and resolver event status is separately recorded."
}
JSON

(
  cd "$OUT_DIR"
  sha256sum payload.json query.graphql variables.json response.json receipt.json > SHA256SUMS
)

printf '\n== ALMS UID REPLAY PROBE ==\n'
printf 'OUT_DIR=%s\n' "$OUT_DIR"
printf 'HTTP_CODE=%s\n' "$HTTP_CODE"
printf '\n== SHA256SUMS ==\n'
cat "$OUT_DIR/SHA256SUMS"
printf '\n== RESPONSE HEAD ==\n'
python3 -m json.tool "$OUT_DIR/response.json" | sed -n '1,80p' || sed -n '1,80p' "$OUT_DIR/response.json"
