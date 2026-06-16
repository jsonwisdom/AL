#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
LEAF_DIR="$ROOT/_truth/anchors/leaf008"
PAYLOAD="$LEAF_DIR/PAYLOAD.txt"
ANCHORS="$LEAF_DIR/ANCHORS.json"
RECEIPT="$ROOT/_truth/receipts/leaf008_receipt.json"

cd "$ROOT"
mkdir -p "$LEAF_DIR" "$ROOT/_truth/receipts"

[ -f "$LEAF_DIR/PAYLOAD_REQUIRED.json" ] || { echo "FAIL missing PAYLOAD_REQUIRED.json"; exit 1; }
[ -s "$PAYLOAD" ] || { echo "FAIL missing payload bytes"; exit 1; }

payload_sha256="$(sha256sum "$PAYLOAD" | awk '{print $1}')"
payload_bytes="$(wc -c < "$PAYLOAD" | tr -d ' ')"
created_utc="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
baseline_commit="$(git rev-parse HEAD)"

jq -n \
  --arg leaf_id "008" \
  --arg designation "LEAF_008_MEME_COURT_OPENAI_V_MUSK" \
  --arg description "Public receipt for tracking Musk v. Altman with satire allowed and fake records forbidden." \
  --arg payload_type "raw_text" \
  --arg payload_path "_truth/anchors/leaf008/PAYLOAD.txt" \
  --arg payload_sha256 "$payload_sha256" \
  --argjson payload_bytes "$payload_bytes" \
  --arg baseline_commit "$baseline_commit" \
  --arg created_utc "$created_utc" \
  --arg anchor_identity "jaywisdom.eth" \
  '{
    leaf_id: $leaf_id,
    designation: $designation,
    description: $description,
    payload_type: $payload_type,
    payload_path: $payload_path,
    payload_sha256: $payload_sha256,
    payload_bytes: $payload_bytes,
    baseline_commit: $baseline_commit,
    created_utc: $created_utc,
    anchor_identity: $anchor_identity,
    court_case: {
      name: "Musk v. Altman",
      docket: "4:24-cv-04722",
      court: "U.S. District Court, Northern District of California",
      venue: "Oakland, California",
      judge: "Yvonne Gonzalez Rogers"
    },
    rules: [
      "Satire is allowed.",
      "Fake records are not.",
      "Receipts > vibes.",
      "Verification > narrative."
    ],
    anchor_allowed: false,
    status: "LOCAL_VERIFIED_PENDING_CI"
  }' > "$ANCHORS"

anchors_sha256="$(sha256sum "$ANCHORS" | awk '{print $1}')"

jq -n \
  --arg receipt "LEAF_008_MEME_COURT_RECEIPT" \
  --arg state "LOCAL_VERIFIED_PENDING_CI" \
  --arg payload_sha256 "$payload_sha256" \
  --arg anchors_sha256 "$anchors_sha256" \
  --arg anchors_path "_truth/anchors/leaf008/ANCHORS.json" \
  --arg created_utc "$created_utc" \
  '{
    receipt: $receipt,
    state: $state,
    payload_sha256: $payload_sha256,
    anchors_sha256: $anchors_sha256,
    anchors_path: $anchors_path,
    created_utc: $created_utc,
    next: "GitHub Actions green, then IPFS anchor."
  }' > "$RECEIPT"

echo "LEAF_008_LOCAL_VERIFIED"
echo "payload_sha256=$payload_sha256"
echo "anchors_sha256=$anchors_sha256"
echo "payload_bytes=$payload_bytes"
