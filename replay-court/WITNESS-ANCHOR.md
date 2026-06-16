# Replay Court Witness Anchor

Witness Anchor defines how Replay Court publishes third-party-verifiable roots for its protected constitutional memory.

Internal validation is not enough.
A replay-native system should make its memory externally witnessable.

## Purpose

```text
Make protected memory world-checkable.
Make tampering detectable.
Make stale mirrors visible.
Make constitutional history portable beyond repo trust.
```

## Scope

Witness roots cover the protected core and current constitutional telemetry heads.

Protected core:

```text
GAME_MECHANICS.md
AGENT_PLAYBOOK.md
replay-court/PROCESS.md
replay-court/SELF-AUDIT.md
replay-court/VALIDATOR.md
replay-court/REPAIR-LEDGER.md
replay-court/CONTRADICTION-STORE.md
replay-court/AUTHORITY-BOUNDS.md
replay-court/REPORT-TEMPLATE.md
replay-court/receipt-schema.json
```

Telemetry heads:

```text
artifacts/public/latest/level1-output.txt
artifacts/public/latest/verifier-current-tip.txt
artifacts/public/latest/oath.json
replay-court/example-report/README.md
```

## Anchor Cadence v0

```text
per protected-core merge
per completed repair
per public mirror refresh
manual anchor allowed for major milestones
```

Daily automation may be added later.

## Root Construction v0

For each anchored file:

```text
file_path
file_sha256
repo_commit
observed_at
```

Canonicalize the list by sorting `file_path` ascending.
Hash the canonical JSON list with SHA-256.

```text
witness_root = sha256(canonical_anchor_manifest)
```

## Anchor Manifest Fields

```text
anchor_id:
schema_version:
created_at:
repo:
repo_commit:
protected_core_files[]:
telemetry_heads[]:
witness_root:
previous_witness_root:
reason:
```

## Publication Targets v0

At least one public target:

```text
- GitHub issue comment
- GitHub release note
- committed manifest under anchors/
```

Future external targets:

```text
- OpenTimestamps
- EAS / Base attestation
- ENS text record pointer
- IPFS / content-addressed mirror
```

External anchoring must remain downstream of internal replay.

## Verification Procedure

A third party should be able to:

```text
1. fetch the anchor manifest
2. fetch each listed file at repo_commit
3. compute file_sha256 for each file
4. canonicalize the manifest file list
5. recompute witness_root
6. compare recomputed root to published witness_root
7. compare previous_witness_root chain if present
```

## Failure Conditions

```text
missing listed file
file hash mismatch
repo_commit mismatch
witness_root mismatch
previous_witness_root mismatch
protected core file omitted without authority-bound amendment
telemetry head stale after public mirror refresh
```

## Guardrails

```text
Witness roots do not create truth.
Witness roots do not authorize payment.
Witness roots do not erase contradiction.
Witness roots do not replace replay.
Witness roots make memory externally checkable.
```

## No Emergency Exception v0

Emergency bypass is not allowed in v0.

If the protected core changes, the witness root must reflect that change through the normal process.

## Invariant

```text
If constitutional memory cannot be externally witnessed, authority remains local and limited.
```
