# Lapis Auditor: GCS Trigger

## Purpose

This Cloud Function automates the Lapis Protocol Stewardship Invariant.

It monitors a GCS vault for `.sample.json` replay objects, invokes the replay verifier, and emits a `REPLAY_SUMMARY.json` artifact back into the vault.

No Base/EAS settlement should occur unless the replay summary verdict is `PASS`.

---

## Functionality

1. Receive `google.storage.object.v1.finalized` event.
2. Filter for replay sample objects.
3. Download replay sample into `/tmp`.
4. Execute `tools.verify_replay_demo.run_audit(...)`.
5. Emit `REPLAY_SUMMARY.json`.
6. Raise error if verdict != `PASS`.

---

## Doctrine Compliance

- **No Silent Overwrite**  
  Every mutation must produce a replay summary.

- **Double Anchor Phase 1**  
  L0 replay validation must pass before any L2 settlement.

- **Challengeable Replayability**  
  Failed replay objects remain inspectable through emitted summaries.

- **Recoverability over Invulnerability**  
  Failures are surfaced, recorded, and attributable.

---

## Deployment Notes

This function depends on:

- `tools/verify_replay_demo.py`
- `schemas/lapis/replayable_audit_demo.v0.1.schema.json`

Deployment packaging must include these paths or vendor them into the function source tree.

Recommended trigger:

- Event type: `google.storage.object.v1.finalized`
- Bucket: `wisdom-family-vault`

---

## Constitutional Build Order

1. Doctrine
2. Schema
3. Replay Artifact
4. Local Verifier
5. GCS Automation
6. Base/EAS Settlement

The chain receives only replay-validated lineage objects.
