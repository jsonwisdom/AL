#!/usr/bin/env bash
set -euo pipefail

# Poster 3 — Anchor001-Compatible Operator Script
# No private keys. No deploys. No custom Sepolia contract.
# This generates the exact hashes needed for the existing GitHub -> JCS -> SHA-256 -> Keccak -> EAS/Base path.

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1"; exit 1; }; }
need git
need python3

REPO="jsonwisdom/AL"
RECEIPT="receipts/poster3/canonical_settlement_poster3_testnet.final.json"
OUTDIR="receipts/poster3/anchor001"
mkdir -p "$OUTDIR"

COMMIT=$(git rev-parse HEAD)
BRANCH=$(git rev-parse --abbrev-ref HEAD)

python3 - <<'PY'
import json, hashlib, pathlib
receipt_path = pathlib.Path("receipts/poster3/canonical_settlement_poster3_testnet.final.json")
outdir = pathlib.Path("receipts/poster3/anchor001")
outdir.mkdir(parents=True, exist_ok=True)
obj = json.loads(receipt_path.read_text(encoding="utf-8"))
canonical = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
sha = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
(outdir / "poster3.canonical.json").write_text(canonical + "\n", encoding="utf-8")
(outdir / "poster3.sha256.txt").write_text("0x" + sha + "\n", encoding="utf-8")
print("POSTER3_SHA256=0x" + sha)
PY

POSTER3_SHA256=$(cat "$OUTDIR/poster3.sha256.txt" | tr -d '\n')

if command -v cast >/dev/null 2>&1; then
  POSTER3_KECCAK=$(cast keccak "$(cat "$OUTDIR/poster3.canonical.json")")
else
  python3 - <<'PY'
print("WARNING: cast not found; install Foundry or compute Keccak separately before EAS attestation.")
PY
  POSTER3_KECCAK="REQUIRES_CAST_KECCAK"
fi

cat > "$OUTDIR/eas_attestation_payload.json" <<EOF
{
  "schema_model": "ANCHOR_001_COMPATIBLE_POSTER3",
  "repo": "$REPO",
  "branch": "$BRANCH",
  "commit": "$COMMIT",
  "receipt_path": "$RECEIPT",
  "canonical_json_path": "$OUTDIR/poster3.canonical.json",
  "sha256": "$POSTER3_SHA256",
  "keccak256": "$POSTER3_KECCAK",
  "anchor_path": "GitHub commit -> JCS canonical bytes -> SHA-256 -> Keccak-256 -> EAS attestation on Base",
  "status": "READY_FOR_EAS_BASE_ATTESTATION",
  "operator_action": "Open EAS app on Base, connect wallet, attest this payload, copy attestation UID back."
}
EOF

cat <<EOF
=== POSTER 3 ANCHOR001 OPERATOR OUTPUT ===
repo: $REPO
branch: $BRANCH
commit: $COMMIT
receipt_path: $RECEIPT
canonical_json: $OUTDIR/poster3.canonical.json
sha256: $POSTER3_SHA256
keccak256: $POSTER3_KECCAK
payload: $OUTDIR/eas_attestation_payload.json

HUMAN NEXT STEP:
1. Open EAS app on Base.
2. Connect jaywisdom/base wallet.
3. Create an attestation using the payload file values.
4. Copy the EAS attestation UID back.

NO PRIVATE KEYS IN SHELL.
NO CUSTOM SEPOLIA CONTRACT.
NO DEPLOYMENT CEREMONY.
EOF
