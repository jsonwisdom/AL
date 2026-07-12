# Fixture 006 — Merkle Mutated Leaf

Attack vector: one approved fragment leaf is altered after the declared branch root was produced.

Expected behavior:

```text
RESULT = REJECT
PURE_ERROR = MERKLE_MISMATCH
CLI_EXIT_CODE = 8
ROOT_MATCH = FALSE
HISTORY_MUTATION = DETECTED
```

This fixture is scaffolding only. Concrete manifest, leaf, proof, and expected-output data are not yet present.
