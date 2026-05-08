# State Jurisdiction Enum Constitutional Triple Receipt v1

## Status

```text
STATUS: SEALED
EPOCH: 02
DOMAIN: STATE_JURISDICTION
CLASS: CONSTITUTIONAL_TRIPLE
```

---

## 1. Bound Artifacts

| Surface | Path | Commit |
|---|---|---|
| Doctrine | `docs/state_workflows/STATE_JURISDICTION_ENUM_V1.md` | `ff0ff68aa077072aa2d64f96e738af049fed0a9c` |
| Schema | `schemas/state_jurisdiction_enum_v1.schema.json` | `f5fdeca542912b8247753deb9606f930bed37779` |
| Manifest | `schemas/membrane_surface_manifest_v1.json` | `8fe6ab10da3a5dc5095e4cf3ebe0adce305d22b4` |

### Binding Rule

All three artifacts must be present, byte-exact, and hash-matching for the triple to be valid.
Absence or mutation of any artifact invalidates the surface.

---

## 2. Constitutional Significance

This triple elevates state jurisdiction from descriptive governance prose to a closed, executable constitutional surface.

Effects:

- the enum becomes law, not metadata
- the schema becomes enforcement, not documentation
- the manifest becomes the binding surface, not a registry

After this triple, jurisdictional state is not interpreted. It is validated.

---

## 3. Locked Invariants

### 3.1 Closed Constitutional Surface

Only values enumerated in the doctrine and schema are representable.
No implicit, inferred, or undocumented states exist.

### 3.2 Refusal Invariant

Unknown or unscoped values must be rejected at validation across all surfaces.

```text
Fail closed, never open.
```

### 3.3 Tier-Scoped ACTIVE

`ACTIVE` is not a lifecycle flag.
`ACTIVE` is a tier-scoped constitutional condition.
`ACTIVE_SCAFFOLD_ONLY` does not authorize downstream claims.

### 3.4 Prohibited Ambiguity Set

The following values are constitutionally unrepresentable in any jurisdiction field:

```text
ACTIVE
OPERATIONAL
VERIFIED
COMPLETE
FULLY_VERIFIED
READY
GREEN
```

### 3.5 Six-Modality Enforcement

Doctrine, precedent, checklist, enum, schema, and type system must converge on the same surface.
Divergence is unconstitutional.

### 3.6 Self-Restraint by Construction

The surface is sealed, typed, validated, anchored, and refusal-enforced.
Geometry enforces doctrine; doctrine cannot override geometry.

---

## 4. Current Valid Enum Values

```text
NOT_ESTABLISHED
SUSPENDED
ACTIVE_SCAFFOLD_ONLY
ACTIVE_ECONOMIC_ONLY
ACTIVE_SPARSE_OVERLAY_ONLY
ACTIVE_FULL_STATE_WORKFLOW
```

No other jurisdiction values are permitted.

---

## 5. Current State Map

| State | Jurisdiction Enum | Basis |
|---|---|---|
| NY | `SUSPENDED` | NY-004 evidence incomplete; halt active |
| MN | `ACTIVE_SCAFFOLD_ONLY` | MN-001 scaffold CSV + manifest committed and hash-verified |

---

## 6. Constitutional Hash

```text
sha256:COMPUTED_BY_VERIFIER_AFTER_COMMIT
```

The constitutional hash is not embedded at authoring time.
It must be computed by a verifier using the canonical hashing procedure defined in Section 8, after this receipt and the bound artifacts are committed and stable.

---

## 7. Drift Rejection

This receipt rejects any attempt to:

- alter the enum without updating the doctrine, schema, and manifest in a coordinated, replay-verifiable change
- introduce new jurisdiction values without a corresponding constitutional update to this triple and its receipt

```text
ATTACHED_MARKDOWN != COMMITTED_REPO_STATE
```

The committed repository is the authority.

The following proposed values are rejected because they do not match the committed schema:

```text
ACTIVE_SPARSE_CLIMATE_ONLY
ACTIVE_FULL_COVERAGE
HALTED
OUTSIDE_JURISDICTION
DEPRECATED
```

They may not be used unless introduced by a future committed enum version.

---

## 8. Canonical Hashing Procedure

To compute the constitutional hash for this triple, a verifier MUST:

### 8.1 Resolve Artifacts

Load the following files from the repository at the same commit:

1. `docs/state_workflows/STATE_JURISDICTION_ENUM_V1.md`
2. `schemas/state_jurisdiction_enum_v1.schema.json`
3. `schemas/membrane_surface_manifest_v1.json`
4. `_truth/receipts/STATE_JURISDICTION_ENUM_TRIPLE_RECEIPT_V1.md`

### 8.2 Canonical Encoding

Each file MUST be read as raw bytes in repository order, with:

- no newline normalization
- no whitespace rewriting
- no JSON re-serialization
- no Markdown rewriting

The bytes used are exactly those stored in the repository.

### 8.3 Concatenation Order

Construct a single byte stream by concatenating the files in this exact order:

1. `docs/state_workflows/STATE_JURISDICTION_ENUM_V1.md`
2. `schemas/state_jurisdiction_enum_v1.schema.json`
3. `schemas/membrane_surface_manifest_v1.json`
4. `_truth/receipts/STATE_JURISDICTION_ENUM_TRIPLE_RECEIPT_V1.md`

### 8.4 Refusal Boundary

Before hashing, a verifier MUST assert that the committed schema enum contains exactly:

```text
NOT_ESTABLISHED
SUSPENDED
ACTIVE_SCAFFOLD_ONLY
ACTIVE_ECONOMIC_ONLY
ACTIVE_SPARSE_OVERLAY_ONLY
ACTIVE_FULL_STATE_WORKFLOW
```

A verifier MUST reject any machine-readable jurisdiction field using:

```text
ACTIVE
OPERATIONAL
VERIFIED
COMPLETE
FULLY_VERIFIED
READY
GREEN
ACTIVE_SPARSE_CLIMATE_ONLY
ACTIVE_FULL_COVERAGE
HALTED
OUTSIDE_JURISDICTION
DEPRECATED
```

If the refusal boundary fails, the constitutional hash MUST NOT be accepted.

### 8.5 Hash Function

Compute:

```text
sha256(concat_bytes)
```

### 8.6 Verification

A verifier MAY record the resulting hash as the concrete value replacing `COMPUTED_BY_VERIFIER_AFTER_COMMIT` in Section 6 in a future, separately sealed receipt version.

Any change to any of the four files changes the hash and invalidates any previously recorded constitutional hash.

This procedure is itself constitutional: any deviation from these steps produces a non-constitutional hash.

---

## 9. Constitutional Effect

This receipt seals the jurisdiction enum as a single, replay-verifiable constitutional artifact.

The triple is now a governed surface with:

- doctrine
- schema
- manifest
- receipt
- hash procedure
- refusal boundary

The law now travels with the type system, and the type system is now constitutional.

---

## Closure

```text
STATE_JURISDICTION_ENUM_TRIPLE: SEALED
UNKNOWN_VALUES: REJECTED
AMBIGUOUS_VALUES: REJECTED
ACTIVE: TIER_SCOPED_ONLY
```

Fail closed, never open.
