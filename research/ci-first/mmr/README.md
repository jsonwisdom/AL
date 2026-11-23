# COMPUTER WISDOM — CI-FIRST Merkle / MMR Gate

Scope: offline-only, synthetic data, no Cloudflare calls, no credentials, no production writes.

This experiment turns the previously reported eight-receipt Merkle and MMR values into an executable GitHub Actions check. Run:

    python3 research/ci-first/mmr/offline_gate.py

The gate deterministically generates eight synthetic canonical JSON receipt records and verifies 32 checks: ordered hash-chain links, Merkle roots for 4 and 8 receipts, MMR peak-height popcount invariants for sizes 1 through 8, two domain-separated MMR commitments, eight membership reconstructions, eight altered-receipt rejections, invalid-index rejection, full-suffix extension from 4 to 8, and modified-suffix rejection.

Fixed expected values match the archived local experiment, and failures cause a nonzero exit code.

Design caveats: The inclusion proof helper reconstructs siblings from the in-memory fixture and is not a production proof parser or standalone untrusted-witness verification API. The 4-to-8 extension uses the entire appended suffix; it is not a compact general-purpose MMR consistency proof. This GitHub CI smoke test does not independently validate the original operator's six checks or run Cloudflare Workers, D1 or R2.

Status: CI gate testable; production ledger HOLD.
AUTHORITY_CREATED=false
DEPLOYMENT=false
PRODUCTION_WRITE=false
EXTERNAL_ANCHOR=false
Do not merge until reviewed.
