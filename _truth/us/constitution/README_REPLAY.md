# ALMS Public Replay — Article I

This repo contains a deterministic, replayable proof of the Article I aggregate root.

## Rule
ALMS_GLOBAL_MERKLE_RULE_V1
- section leaf = SHA256(section_id + ':' + section_root_sha256)
- parent = SHA256(left_raw_digest || right_raw_digest)
- odd leaf promoted unchanged

## Verify (local clone)

```bash
cd AL
python3 _truth/us/constitution/replay_article_i_root.py
```

Expected output:
- status: PASS
- computed_article_i_root_sha256 matches expected_article_i_root_sha256

## Verify (from GitHub without clone)

You can fetch the three section manifests and run the same computation in any environment.

Sources:
- _truth/us/constitution/a1_s8_merkle_manifest.json
- _truth/us/constitution/a1_s9_merkle_manifest.json
- _truth/us/constitution/a1_s10_merkle_manifest.json

## Guarantees
- Any byte change in any clause → section root changes → Article I root changes.
- Reproducible by any third party without trusting the author.

Proof > narrative.
