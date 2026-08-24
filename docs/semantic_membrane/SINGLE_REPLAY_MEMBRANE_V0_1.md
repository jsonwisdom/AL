# Single Replay Membrane (SRM) V0.1

```text
STATUS                  = PROPOSED / PR-BOUND / NON-CANON
EVALUATION_MODE         = ACTIVE
CANON_STATUS            = UNCHANGED
AUTHORITY_CREATED       = FALSE
MERGE_AUTHORIZED        = FALSE
EXECUTION_AUTHORIZED    = FALSE
VERSION                 = 0.1
DATE                    = 2026-08-24
```

## Purpose

The Single Replay Membrane applies one evidence, burden, and state-derivation discipline across orthogonal domains without merging their operations.

SRM is a control profile. It does not bridge chains, combine tokenomics, bind identities, resolve customer-service claims, execute treasury actions, or inherit authority from any covered surface.

```text
SHARED_EVIDENCE_DISCIPLINE = TRUE
CROSS_DOMAIN_OPERATIONS    = FALSE
CROSS_DOMAIN_AUTHORITY     = FALSE
CROSS_DOMAIN_BURDEN_LOAN   = FORBIDDEN
```

## Relationship to the existing semantic membrane

SRM V0.1 is a draft profile layered beneath the existing frozen semantic-membrane specifications in this repository:

- `membrane_bootstrap_proof_v1.md`
- `trace_receipt_schema_v1.md`
- `receipt_verifier_test_vectors_v1.md`
- `verifier_convergence_report_v1.md`

SRM does not modify those specifications and does not claim continuity standing under them. In particular, this document is not a signed replay receipt, does not contain a completed artifact-set root, and does not satisfy the frozen signature gates.

```text
SRM_PROFILE_PASS != TRACE_RECEIPT_VALID
SRM_DRAFT         != SIGNED_CONTINUITY
SRM_PR            != BOOTSTRAP_PROOF
FROZEN_SPECS      = UNCHANGED
```

## Domains

| Domain ID | Operator-described surface | SRM interaction | Initial SRM state |
| --- | --- | --- | --- |
| `GPK_FACTORY` | GPK Factory / BoxDee / Larry #002 | Quarantine and preflight only | `HOLD` |
| `SOLANA_PUMP` | Generic pump.fun meme-coin surface | Read-only replay; no burden borrowing | `HOLD` |
| `BASE_CULTURE` | Base culture token `$BASED` | Read-only replay; no identity binding | `HOLD` |
| `COINBASE_LIVE` | Coinbase Live customer-service, futures, and treasury-preview surface | Coinbase-receipt-only evaluation | `PREVIEW_ONLY / HOLD` |

The labels above are operator-supplied scope declarations. They are not proof that a specific token, wallet, account, order, product, contract, or platform state exists.

## Source classes

Every admitted fact MUST carry one source class:

| Class | Meaning |
| --- | --- |
| `OBSERVED` | Directly read from the named surface at a frozen locator and time. |
| `RECEIPT` | Bound to exact bytes or a provider receipt whose digest is recorded. |
| `OPERATOR_REPORTED` | Supplied by the operator but not independently replayed in the current run. |
| `UNOBSERVED` | Required evidence was not read or was unavailable. |
| `CONTRADICTED` | Two or more admissible, bound records disagree. |

```text
OPERATOR_REPORTED != OBSERVED
OBSERVED          != RECEIPT
RECEIPT           != AUTHORITY
UNOBSERVED        != NONEXISTENT
SEARCH_MISS       != ABSENCE
```

## Minimum replay input

A domain replay is not burden-satisfied unless it freezes all applicable fields:

```json
{
  "srm_version": "0.1",
  "domain_id": "",
  "surface_id": "",
  "surface_locator": "",
  "network_or_provider": "",
  "exact_head_or_state_ref": "",
  "observed_at": "",
  "timezone": "",
  "requested_claim": "",
  "requested_action": "",
  "receipts": [
    {
      "receipt_type": "",
      "locator": "",
      "sha256": "",
      "source_class": "OBSERVED | RECEIPT | OPERATOR_REPORTED"
    }
  ],
  "open_surfaces": [],
  "authority_created": false
}
```

Missing inapplicable fields may be marked `NOT_APPLICABLE` with a reason. Missing applicable fields MUST remain missing and force `HOLD`; they may not be replaced by narrative.

## Shared invariants

### SRM-INV-001 — Replay before narrative

Interpretation begins only after the replay input is frozen.

```text
NARRATIVE_WITHOUT_REPLAY -> HOLD
```

### SRM-INV-002 — Burden is derived

`burden_satisfied` is verifier output, never caller input. It requires exact locators, applicable receipts, provenance, and reconciliation.

```text
CALLER_ASSERTED_BURDEN = INVALID
MISSING_APPLICABLE_EDGE -> HOLD
```

### SRM-INV-003 — Clarity control

The internal rule ID is `SRM_CLARITY_CONTROL_V0_1`. The operator phrase `CLARITY_ACT_COMPLIANCE` is retained only as an alias for this internal evidence rule.

It is not a claim of compliance with H.R. 3633, any enacted law, regulation, exchange rule, Coinbase policy, or other legal standard.

```text
NARRATIVE > RECEIPT                = FORBIDDEN
SRM_CLARITY_CONTROL                = INTERNAL_ONLY
CLARITY_ACT_COMPLIANCE_ALIAS       = NON_LEGAL
SRM_CLARITY_CONTROL != LEGAL_COMPLIANCE
```

### SRM-INV-004 — Customer-service orthogonality

Coinbase account, identity, eligibility, futures, treasury, support, or transaction claims may be evaluated only from applicable Coinbase-origin receipts plus any required human confirmation.

```text
PUMPFUN_RECEIPT   -> COINBASE_BURDEN = NO_EFFECT
BASE_TOKEN_STATE  -> COINBASE_BURDEN = NO_EFFECT
GPK_ASSET_RECEIPT -> COINBASE_BURDEN = NO_EFFECT
COINBASE_CLAIM    -> COINBASE_RECEIPTS_REQUIRED
```

### SRM-INV-005 — Treasury preview only

SRM may prepare a read-only preview. It may not sign, submit, route, place, allocate, transfer, mint, trade, or execute.

Execution requires a separate human approval and an exact receipt hash under the native domain's own controls.

```text
PREVIEW       != ORDER
ORDER_DRAFT   != SUBMISSION
HUMAN_REVIEW != EXECUTION
AUTO_EXECUTION = FALSE
```

### SRM-INV-006 — No fake green

No domain may claim `PASS`, `CANON`, `BOUND`, `RESOLVED`, or `EXECUTED` merely because a document, workflow, model response, UI display, or PR exists.

```text
CODE_EXISTS        != EXECUTION_RECEIPT
SCHEMA_VALID       != PASS
WORKFLOW_GREEN     != WORLD_TRUTH
UI_DISPLAY         != BACKEND_STATE
PR_OPEN            != CANON
PASS               != AUTHORITY
```

### SRM-INV-007 — Domain isolation

Evidence may be compared across domains, but a receipt from one domain cannot satisfy another domain's burden unless an explicit, receipt-bound edge is admitted and replayed.

```text
ADJACENCY != BINDING
REFERENCE != RECEIPT_EDGE
BRIDGE_CLAIM_WITHOUT_EDGE -> HOLD
```

## Deterministic state derivation

SRM uses the BoxDee result order already recorded in the account-wide query scope:

```text
FAIL > DELTA > HOLD > PASS
```

| State | Deterministic trigger |
| --- | --- |
| `FAIL` | Invariant violation or explicit contradiction between admissible bound receipts. |
| `DELTA` | Bound replay mismatch against the declared prior state. |
| `HOLD` | Missing edge, incomplete evidence, partial chain, partial replay, unresolved open surface, or missing required signature. |
| `PASS` | Every applicable gate is bound and reconciles for the exact requested claim. |

```text
INCOMPLETE != DELTA
MISSING_EDGE -> HOLD
BOUND_MISMATCH -> DELTA
CONTRADICTORY_ADMISSIBLE_RECEIPTS -> FAIL
```

An SRM result is claim-scoped. A `PASS` for one field, file, transaction, or support receipt does not create a repository-wide, account-wide, token-wide, or domain-wide pass.

## Replay procedure

1. Identify one domain and one exact claim.
2. Freeze the domain-native locator and observation time.
3. Freeze directory/file topology before semantic search when a repository is involved.
4. Read exact receipt bytes from the native surface.
5. Verify hashes and bindings.
6. Declare missing and open surfaces.
7. Derive `FAIL`, `DELTA`, `HOLD`, or `PASS` using the fixed precedence.
8. Emit a claim-scoped SRM result.
9. Require a separate human gate for any consequential next action.

## Result envelope

```json
{
  "schema_id": "SINGLE_REPLAY_MEMBRANE_RESULT_V0_1",
  "srm_version": "0.1",
  "domain_id": "",
  "surface_id": "",
  "claim_id": "",
  "input_digest": "",
  "receipt_digests": [],
  "result": "FAIL | DELTA | HOLD | PASS",
  "burden_satisfied": false,
  "missing_edges": [],
  "mismatches": [],
  "contradictions": [],
  "open_surfaces": [],
  "execution_authorized": false,
  "authority_created": false
}
```

This envelope is documentary in V0.1. No JSON Schema or executable verifier is introduced by this PR.

## Initial unified snapshot

The following state is derived from the operator command plus the absence of domain-native receipt bundles in this proposal:

```text
SRM_EVALUATION_MODE       = ACTIVE
SRM_CANON_STATUS          = PROPOSED / PR-BOUND
DOMAINS_DECLARED          = 4
DOMAIN_RECEIPT_BUNDLES    = 0
AUTHORITY_CREATED         = FALSE
CANON_MUTATION            = FALSE
NO_FAKE_GREEN             = TRUE
MEMBRANE                  = HOLD

GPK_BOXDEE_STATUS         = OPERATOR_REPORTED / HOLD
PUMP_SURFACE_STATUS       = HOLD
BASE_BASED_STATUS         = HOLD
COINBASE_LIVE_STATUS      = PREVIEW_ONLY / HOLD
```

`DRAFT_APPROVED`, `Larry #002`, `$BASED`, and `Coinbase Live` remain operator-described labels until exact native locators and receipts are admitted. This does not reject them; it preserves their burden state.

## OpenAI boundary

Models may classify, summarize, and propose SRM records. They may not derive authority, sign on the operator's behalf, create missing receipt facts, or promote a result.

```text
MODEL_OUTPUT       != VERIFICATION
TOOL_CALL          != DOMAIN_ACTION
AGENT_PERMISSION   != PROMOTION_AUTHORITY
OPENAI_API_KEY     = NOT_REQUIRED_FOR_THIS_DOCUMENT
API_KEY_CREATED    = FALSE
MODEL_EXECUTION    = NOT_A_REPLAY_RECEIPT
```

## Non-goals

SRM V0.1 does not:

- merge GPK, Solana, Base, and Coinbase operations;
- bridge chains or wallets;
- bind a token to a person or identity name;
- prove a mint, trade, balance, entitlement, listing, or custody state;
- resolve customer-service errors;
- provide legal, regulatory, financial, or platform-compliance certification;
- alter frozen semantic-membrane specifications;
- create a verifier, signature, attestation, transaction, or authority.

## Promotion gate

Merge, if separately approved by a human, would canonize only this documentation inside `jsonwisdom/AL`. It would not activate any domain operation or satisfy any domain burden.

Before an executable SRM version may claim conformance, a later PR must add:

1. a machine-readable input schema;
2. a deterministic result schema;
3. a verifier implementing the fixed precedence;
4. positive and negative test vectors for all four domains;
5. canonicalization and digest rules;
6. a replay receipt from an exact commit;
7. any signatures required by the frozen semantic-membrane contract.

```text
DOCUMENT_CREATED != SRM_EXECUTED
PR_CREATED       != SRM_CANON
MERGED_DOC       != DOMAIN_PASS
SRM_PASS         != AUTHORITY
AUTHORITY_CREATED = FALSE
```

## Source boundary

This proposal was reconciled against:

- the operator's SRM V0.1 command dated 2026-08-24;
- the read-only Drive document titled `BoxDee Account-Wide Query Scope V1 — 2026-08-24`;
- the four frozen files under `docs/semantic_membrane/` listed above;
- the exact `jsonwisdom/AL` base commit recorded in the pull request.

Drive bytes are not copied into this repository, and Drive search results are not treated as absence proof. Claims about pump.fun, `$BASED`, Coinbase, GPK bindings, or legislation require their own native receipts.

## Canon line

One membrane may govern the burden. No membrane may erase the boundary.
