#!/usr/bin/env bash
set -euo pipefail

EXPECTED_COMMIT="13004719dd0c34f765ca95dfe8566b6feb2bf6cf"
EXPECTED_ROOT="ff55160908ff41d23f7af0df8873ef7a0dcf8163d1a308f58941e87b5a95bad9"
EXPECTED_KECCAK="0xb7e55f9e1f4f27cd96f38d74e6510e184a14772ef3f9f628d5acc68531dd185d"
EAS_SCHEMA_UID="0x3bab210b4da3faff084e146075caf9168efb5c9c87f18509bca2c07d7f2e49c"
EAS_UID="0x18b5b00c62c648df2ccf4a746645493fa2a0b0dcda6697052d8c3a3d1586c142"
CANONICAL_REPO="jsonwisdom/Welcome-to-JSONWISDOM"
CANONICAL_RECORD="examples/sample-record.json"

cat <<EOF
ANCHOR_001_CURRENT_REFERENCE
status=DOUBLE_ANCHORED_VERIFICATION_SURFACE_COMPLETE
canonical_repo=$CANONICAL_REPO
expected_commit=$EXPECTED_COMMIT
expected_merkle_root_sha256=$EXPECTED_ROOT
expected_leaf_keccak256=$EXPECTED_KECCAK
eas_schema_uid=$EAS_SCHEMA_UID
eas_attestation_uid=$EAS_UID
chain=Base
ens_status=DEFERRED
rule=NO_GHOST_ANCHOR

Manual verification path:
1. Clone $CANONICAL_REPO
2. Checkout $EXPECTED_COMMIT
3. Recompute JCS canonical bytes for $CANONICAL_RECORD
4. Run ./scripts/merkle-build.sh and confirm $EXPECTED_ROOT
5. Run ./scripts/keccak-leaf.sh $CANONICAL_RECORD and confirm $EXPECTED_KECCAK
6. Verify EAS UID on Base: $EAS_UID

This script is a reference gate, not a signer.
Signing power must remain outside the repo.
EOF
