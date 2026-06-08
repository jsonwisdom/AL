# MISSING_CORPUS_RECEIPT

## Receipt

```json
{
  "receipt_type": "MISSING_CORPUS_RECEIPT",
  "version": "0.1",
  "status": "REPLAY_BLOCKED_BY_MISSING_CORPUS",
  "corpus": "witnessed/evidence",
  "authority": false,
  "semantic_inference": false,
  "subject": "MN_MMB_FEB_2026",
  "expected_receipt_count": 28,
  "observed_receipt_count": 0,
  "expected_root": "d8a6bbdb9add88c79da4a22201cd027d5a6f7b3682402f66ff8672ce10dbe23f",
  "observed_root": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "origin_pr": "jsonwisdom/AL#272",
  "origin_status": "BLOCKED_BY_MISSING_REAL_FIXTURES",
  "forensic_verdict": "REAL_28_FIXTURES_NEVER_COMMITTED",
  "placeholder_posture": "PLACEHOLDER_FAIL_CLOSED_INTENTIONAL",
  "rediscovered_by": "jsonwisdom/AL#310",
  "promotion_allowed": false,
  "replayable": false,
  "valid": false
}
```

## Summary

Ontology v2 did not fail. The missing corpus failed replay.

PR #310 repaired enough workflow and verifier tooling to expose the true replay state for `MN_MMB_FEB_2026`: the manifest and vector reference a 28-leaf corpus, but the repository contains zero committed JSON receipt bodies at the expected replay fixture path.

The verifier correctly computed the RFC6962 empty-tree root for zero inputs and refused to match the declared 28-leaf root.

## Origin Evidence

PR #272 introduced the MCP/Base witness scaffold and explicitly recorded that the replay surface was not complete.

The PR #272 comment trail states:

> PR #272 is NOT merge-ready yet.

> Blocking placeholders have been committed for:
> - `tests/fixtures/receipts/mn_mmb_feb2026/`
> - `tests/vectors/mn_mmb_feb2026_full.json`
> - `manifests/mn_mmb_feb2026_manifest.json`

> The replay workflow should fail until real 28-leaf fixtures and matching roots are committed.

## Forensic Conclusion

```text
REAL_28_FIXTURES_NEVER_COMMITTED
PLACEHOLDER_FAIL_CLOSED_INTENTIONAL
PR_310_REDISCOVERED_EXPECTED_FAILURE
REPLAY_BLOCKED_BY_MISSING_CORPUS
```

## Constitutional Boundary

This receipt does not restore receipts, re-root the manifest, alter Merkle logic, or promote any witnessed artifact.

Hard constraints preserved:

```text
witness_uid != eas_uid
observed != attested
witnessed/ != valid/
YELLOW != GREEN
authority = false
```

`FED-AI-2026-EAS-002` remains `WITNESSED / YELLOW / witnessed / authority:false`.

## Prohibited Repairs

The following actions remain prohibited:

- Do not fabricate 28 dummy receipts.
- Do not rebaseline the manifest or vector to the empty-tree root.
- Do not skip the replay gate.
- Do not mark this corpus `REPLAYABLE`.
- Do not claim `VALID` without committed receipt bodies and successful replay.

## Required Future Action

A future PR must do one of the following:

1. Recover and commit the original 28 canonical JSON receipt bodies, or
2. Declare `NEW_FIXTURE_CORPUS_REQUIRED`, generate a new corpus, compute a new root, and document that as a new evidence event.

Until then, the correct status is:

```text
REPLAY_BLOCKED_BY_MISSING_CORPUS
```
