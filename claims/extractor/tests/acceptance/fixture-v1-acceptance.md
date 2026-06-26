# Claim Extractor Membrane — Acceptance Tests v0.1

## Purpose

This file defines the constitutional acceptance behavior for `claims/extractor/fixture-v1.schema.json`.

No extractor implementation may be considered replay-admissible until it satisfies this membrane.

The extractor may identify explicit semantic commitments. It may not decide truth, summarize intent, infer vibes, or bundle multiple commitments into one fixture.

## Target Schema

```text
claims/extractor/fixture-v1.schema.json
```

## Verdict Codes

| Verdict | Meaning |
|---|---|
| `ACCEPT_FIXTURE` | Emit one schema-valid canonical fixture. |
| `ACCEPT_MULTIPLE_FIXTURES` | Emit exactly one fixture per atomic claim. |
| `REFUSE_CLARIFICATION` | Emit no accepted fixture; produce auditable clarification log. |
| `DROP_NO_FIXTURE` | Pure chatter or non-commitment; emit no fixture. |
| `HUMAN_REVIEW` | Contradiction or high-risk ambiguity requires review. |

## Reason Codes

| Reason Code | Meaning |
|---|---|
| `EXPLICIT_AGREEMENT` | Clear agreement language exists in raw text or bounded context. |
| `DEADLINE_ARTIFACT` | Deadline is tied to a specific artifact. |
| `REGIME_CHANGE` | Rule, regime, schema, or policy change is explicit. |
| `RESPONSIBILITY_ASSIGNMENT` | A named actor is assigned ownership or responsibility. |
| `NEGATIVE_COMMITMENT` | Explicit prohibition or immutability commitment. |
| `AMBIGUOUS_COMMITMENT` | Language is vague or non-binding. |
| `SOCIAL_CHATTER` | No replay-admissible commitment exists. |
| `MULTI_CLAIM_SPLIT` | Multiple atomic claims detected and split. |
| `CONTRADICTION_WINDOW` | Bounded context contains conflicting commitments. |
| `LOW_CONFIDENCE` | Confidence is below `0.95`. |
| `SCHEMA_INVALID` | Output does not validate against fixture schema. |
| `HASH_MISMATCH` | Raw or canonical hash does not recompute. |
| `NON_DETERMINISTIC_OUTPUT` | Same input does not replay to byte-identical output. |

## Acceptance Table

| ID | Input Snippet | Expected Output | Verdict | Reason |
|---|---|---|---|---|
| `CE_ACC_001` | `We agreed to freeze the canonicalization regime object before v1.` | One fixture with `extracted_claim` equal to the explicit sentence, `confidence >= 0.95`, `needs_clarification: false`. | `ACCEPT_FIXTURE` | `EXPLICIT_AGREEMENT`, `REGIME_CHANGE` |
| `CE_ACC_002` | `Ship the receipt format by Friday.` | One fixture preserving the deadline and artifact. | `ACCEPT_FIXTURE` | `DEADLINE_ARTIFACT` |
| `CE_ACC_003` | `Decision: freeze fixture-v1.schema.json before extractor code lands.` | One fixture preserving the decision and artifact. | `ACCEPT_FIXTURE` | `EXPLICIT_AGREEMENT`, `REGIME_CHANGE` |
| `CE_ACC_004` | `@jay owns the receipt format by Friday.` | One fixture preserving actor, artifact, and deadline. | `ACCEPT_FIXTURE` | `RESPONSIBILITY_ASSIGNMENT`, `DEADLINE_ARTIFACT` |
| `CE_ACC_005` | `Do not merge extractor code without schema validation.` | One fixture preserving the negative commitment. | `ACCEPT_FIXTURE` | `NEGATIVE_COMMITMENT` |
| `CE_REF_001` | `Let's maybe ship something soon.` | No accepted fixture; clarification log required. | `REFUSE_CLARIFICATION` | `AMBIGUOUS_COMMITMENT` |
| `CE_REF_002` | `Good work, this looks great.` | No fixture emitted. | `DROP_NO_FIXTURE` | `SOCIAL_CHATTER` |
| `CE_SPLIT_001` | `We agreed to freeze the canonicalization regime object before v1. Also ship the receipt format by Friday.` | Exactly two fixtures, one per atomic claim. | `ACCEPT_MULTIPLE_FIXTURES` | `MULTI_CLAIM_SPLIT` |
| `CE_REVIEW_001` | Current message: `Ship receipt format by Friday.` Prior bounded context: `Do not ship receipt format before schema review.` | No accepted fixture; human review log required. | `HUMAN_REVIEW` | `CONTRADICTION_WINDOW` |
| `CE_REF_003` | Any extracted candidate with `confidence: 0.94`. | `extracted_claim: null`, `needs_clarification: true`. | `REFUSE_CLARIFICATION` | `LOW_CONFIDENCE` |

## Canonicalization Invariants

Every emitted fixture must satisfy all of the following:

1. Validate against `claims/extractor/fixture-v1.schema.json`.
2. `raw_hash == sha256(raw_text_bytes)`.
3. `candidate_canonical_hash == sha256(JCS(NFC(fixture_without_candidate_canonical_hash)))` under the extractor canonicalization regime.
4. `normalization.unicode == "NFC"`.
5. `normalization.whitespace == "canonical"`.
6. `normalization.case == "preserve"`.
7. `normalization.json == "JCS"`.
8. `claim_id` matches `CHATFIXTURE_YYYYMMDD_HHMMSS_#####`.
9. `ingestion_id` matches `ING_YYYYMMDD_HHMMSS_#####`.
10. `regime.canonicalizer == "ALMS_EXTRACTOR_V1"`.

## Constitutional Invariants

1. No fixture may contain hallucinated or inferred meaning not present in `raw_text` plus bounded context.
2. One fixture may contain only one atomic claim.
3. Bundling is forbidden.
4. Lossy paraphrase is forbidden.
5. Tone interpretation is forbidden.
6. The extractor must be deterministic under fixed seed / temperature `0`.
7. Every refusal mode must produce an auditable log entry with reason code.
8. Ambiguous commitments must never be silently accepted.
9. Pure chatter may be silently dropped from fixture emission, but operational logs may still record the drop.
10. Clarification requests must generate lightweight trace receipts.

## Replay-Safety Tests

Any implementation must prove:

1. Same input produces byte-identical output fixture set.
2. Fixture self-validates locally before ALMS handoff.
3. Hashes recompute independently.
4. Context window remains bounded to at most 5 prior messages.
5. LLM-assisted extraction, if used, records input hash, prompt hash, model identifier, temperature, and output hash.
6. No network-dependent state may affect fixture output unless captured in the replay receipt.

## Golden Fixture Directory

Concrete examples should be committed under:

```text
claims/extractor/tests/fixtures/golden/
```

Minimum golden fixtures:

```text
positive_explicit_agreement.input.json
positive_explicit_agreement.expected.json
positive_deadline_artifact.input.json
positive_deadline_artifact.expected.json
refusal_ambiguous.input.json
refusal_ambiguous.expected.json
split_multi_claim.input.json
split_multi_claim.expected.json
review_contradiction.input.json
review_contradiction.expected.json
```

## Merge Gate

Extractor implementation is blocked until these acceptance behaviors exist as executable tests.

Schema without acceptance tests is advisory.

Acceptance tests make the membrane enforceable.
