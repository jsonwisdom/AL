# Phase-1 Lineage Adversarial Vectors

These fixtures define graph attack classes for `AgentActionLinkV1` traversal.

Status: templates only until real Base Sepolia UIDs and observed walker JSON are filled in.

Rules:
- Do not treat expected output as observed output.
- Do not merge attack claims without raw walker JSON.
- Keep this layer JSON-in / JSON-out only.
- No UI, payments, observers, or schema changes in this phase.

Vector classes:
1. cycles
2. dangling
3. depth_bound
4. invalid_relation
5. partial_lineage
6. semantic_contradiction

Canonical identity rule:
- The child identity is the attestation UID itself.
- `parentUID` is the traversal pointer.
- Encoded `childUID` is advisory/sentinel metadata for the current schema.
