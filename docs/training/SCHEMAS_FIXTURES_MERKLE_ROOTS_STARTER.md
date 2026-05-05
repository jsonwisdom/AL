# Schemas, Fixtures, and Merkle Roots by Jay — Starter

Status: STARTER_INFRASTRUCTURE_ONLY

This starter pack separates three artifact classes:

1. schemas/ — validation contracts
2. _truth/write_runs/fixtures/ — non-custody test vectors
3. _truth/merkle/ — deterministic roots and manifests

## Rules

- Schemas define shape; they do not prove provenance.
- Fixtures test tools; they cannot open custody gates.
- Merkle roots summarize exact leaf bytes; they do not create new facts.
- Live packets must be emitted by the runner only.
- No synthetic data may enter the custody chain.

## Current WRITE_RUN_0002 boundary

- Live packet path: _truth/write_runs/WRITE_RUN_0002_packet.json
- Required state before runner output: ABSENT_BY_DESIGN
- Fixture path: _truth/write_runs/fixtures/WRITE_RUN_0002_packet.FIXTURE.json
- Validator: scripts/validate_write_run_0002.sh
- Acceptance frame: _truth/write_runs/WRITE_RUN_0002_ACCEPTANCE_FRAME_v1.1.json

## Starter Merkle rule

For a directory of JSON fixtures:

1. sort file paths lexicographically
2. hash each file with sha256 over raw bytes
3. write leaves as JSONL
4. if one leaf exists, root = leaf hash
5. if multiple leaves exist, hash adjacent pairs as raw concatenated hex strings encoded as text
6. carry odd leaf upward unchanged
7. write manifest JSON with root, count, rule_id, and leaves file

Rule ID: ALMS_STARTER_MERKLE_V1
