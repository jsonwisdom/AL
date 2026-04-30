# ALMS Changelog

## v0.2.0 — Public Artifact-Surface Self-Verifying Checkpoint

### Summary

ALMS v0.2.0 establishes the first full public artifact-surface checkpoint. All public receipts, manifests, rollovers, and bootstrap artifacts are independently verifiable using the same scripts enforced by CI.

### Verification

- Receipt verification: PASS
- Segment manifest verification: PASS
- Rollover verification: PASS
- Bootstrap verification: PASS
- CI verifier suite: PASS

### Public Artifacts

- receipts/media_mesh_v1/global_root_receipt.final.json
- receipts/segment_002/leaf_001_receipt.final.json
- receipts/segments/segment_001_manifest.json
- receipts/segments/segment_002_manifest.json
- receipts/segments/segment_002_bootstrap.json
- receipts/segments/segment_003_bootstrap.json
- receipts/rollover/segment_001_to_002.json
- receipts/rollover/segment_002_to_003.json

### State Transition

```txt
ALMS_PUBLIC_FULL_ARTIFACT_SURFACE_SELF_VERIFYING
→ ALMS_V0_2_0_PUBLIC_ARTIFACT_SURFACE_CHECKPOINT
