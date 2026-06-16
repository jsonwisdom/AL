# ALMS Audit Instructions

Inspect:
- README.md
- AGENTS.md
- docs/ALMS_OPERATOR_GUIDE.md
- scripts/build_merkle_root.sh
- scripts/preflight_repo_audit.sh
- status.json
- _truth/status/last_run.json
- _truth/merkle/manifest.json
- _truth/merkle/root.txt

Rules:
- Do not edit receipts.
- Do not manually edit Merkle outputs.
- Do not advance lifecycle state from pending logs.
- Do not call a root valid unless it can be recomputed.

Finding labels:
VALID
PARTIAL_VALID
ROOT_SURFACE_DRIFT
MISSING_ATTESTATION
UNKNOWN_HASH_PRESENT
ALMS_REVIEW_REQUIRED
