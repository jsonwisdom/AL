# Fixture 007 — Cross-Branch Proof Forgery

Attack vector: a structurally valid proof from one branch is presented under a different branch context.

Expected behavior:

```text
RESULT = REJECT
PURE_ERROR = MERKLE_MISMATCH
CLI_EXIT_CODE = 8
BRANCH_BINDING = INVALID
CROSS_BRANCH_PROOF_REUSE = REJECT
```

This fixture is scaffolding only. Concrete manifest, proof, sibling path, and expected-output data are not yet present.
