# ALMS v0 Constitutional Constants

```yaml
# ALMS v0 Constitutional Constants
# SEALED at closure_commit: 045e90ee51feb76af0830554a30045fa43f58cd5
# This file contains no executable code, only frozen identity anchors.

ALMS_v0:
  STATUS: CONSTITUTIONAL_STACK_SEATED
  CLOSURE_COMMIT: 045e90ee51feb76af0830554a30045fa43f58cd5
  STACK_PRECLOSURE_BLOB_SHA: 1c16a77dde5d9beb0262d23d929f89a4be0397c9
  GLOBAL_STATE: NO_DRIFT

  COORDINATE_MODEL:
    commit_sha: "Repository state coordinate"
    git_blob_sha: "Git object identity verified via git hash-object"
    sha256: "External raw-byte attestation OPTIONAL_PENDING, not faked"

  COMPONENTS:
    - path: docs/ALMS-v0-PROVENANCE.md
      git_blob_sha: 0813c46b2e1917a78de8c301b7a957a7007b563a
    - path: docs/ALMS-v0-REGISTRY.md
      git_blob_sha: c97b3ad545c9ab1ff3259d4bf57ddc2b441f63ee
    - path: docs/ALMS-v0-EXECUTION.md
      git_blob_sha: 634b55178f7aafaf662586ace54f75ee55f9dfcb
    - path: docs/ALMS-v0-COURTROOM.md
      git_blob_sha: b508358dee86cad68bab2c8501044d6b6cf2126f
    - path: docs/ALMS-v0-STACK.md
      git_blob_sha: 1c16a77dde5d9beb0262d23d929f89a4be0397c9

EXTERNAL_ATTESTATIONS: OPTIONAL_PENDING

INVARIANTS:
  - NO_SELF_REFERENTIAL_PARADOX
  - NO_FAKE_SHA256_PLACEHOLDERS
  - GLOBAL_STATE_EQ_NO_DRIFT
```

## Status

These constants name the seated ALMS v0 constitutional closure without creating a self-referential hash loop.

`CLOSURE_COMMIT` identifies the commit that bound the v0 stack index to Git object identities.

`STACK_PRECLOSURE_BLOB_SHA` identifies the pre-closure stack file object that was bound by the closure commit.

External SHA-256 attestations remain optional and pending. They must be produced by trusted raw-byte execution and must not be inferred from connector content.
