# PUBLIC_VERIFIER_V1

Status: FROZEN
Date: 2026-05-27
Scope: External verification surface for dual-witness replay membrane artifacts
Authority: NONE

## Purpose

Provide a minimal public verifier that checks replay evidence emitted by the membrane without re-running the membrane.

The membrane produces evidence.
The verifier checks evidence.

## Inputs

```json
{
  "verifier_id": "PUBLIC_VERIFIER_V1",
  "inputs": [
    "replay_manifest.json",
    "comparison_report.json",
    "determinism_audit_report.json",
    "INVARIANT_PROFILE_V1.json",
    "CANON_PROFILE_V1.json"
  ]
}
```

## Required Checks

```json
{
  "checks": [
    "profile_hashes_match_manifest",
    "profile_hashes_match_determinism_audit_report",
    "manifest_hash_1_equals_manifest_hash_2",
    "red_trace_hash_1_equals_red_trace_hash_2",
    "green_trace_hash_1_equals_green_trace_hash_2",
    "comparison_report_asserts_opposite_lawful_outcomes",
    "no_authority_claims_present"
  ]
}
```

## Output

```json
{
  "verifier_id": "PUBLIC_VERIFIER_V1",
  "verdict": "VALID",
  "reason": "all public verification checks passed",
  "authority": false
}
```

Invalid output must include a reason:

```json
{
  "verifier_id": "PUBLIC_VERIFIER_V1",
  "verdict": "INVALID",
  "reason": "profile hash mismatch",
  "authority": false
}
```

## Hash Rule

Profile hashes use the profile self-exclusion rule:

```text
sha256(canonical_json(profile with profile_hash = "sha256:SELF_EXCLUDED"))
```

Stable evidence hashes use:

```text
sha256(canonical_json(value))
```

Canonical JSON means sorted object keys, UTF-8, and no optional whitespace.

## Constitutional Boundary

The verifier must not:

- run the membrane
- re-evaluate invariants
- infer authority
- validate signer identity
- mutate artifacts

The verifier may only check evidence consistency.

## Constitutional Lock

```json
{
  "membrane_role": "produce_evidence",
  "verifier_role": "check_evidence",
  "execution_required": false,
  "authority": false,
  "interpretation": false
}
```
