# PR Replay Rules Ledger — 314, 315, and Forward v0.1

Operator: jaywisdom.base.eth  
Identity Root: jaywisdom.eth  
Network: JSONWisdom/*  
Layer: L3  

## Purpose

This ledger defines repeatable replay rules for PR #314, PR #315, and future PRs.

No PR receives authority merely because it exists. Every PR must declare scope, receipt status, replay status, unresolved gates, and cross-repo relevance.

```yaml
NO_PR_AUTHORITY_BY_EXISTENCE: TRUE
RECEIPT_BEFORE_AUTHORITY: TRUE
REPLAY_BEFORE_GREEN: TRUE
CROSS_REPO_CONTEXT_REQUIRED: TRUE
```

---

## Universal PR Rules

Every PR in the replay chain must answer five questions:

1. What is the claim?
2. What is the receipt?
3. What is the replay path?
4. What remains pending?
5. What authority is not being claimed?

```yaml
REQUIRED_FIELDS:
  - claim
  - receipt
  - replay_path
  - pending_gates
  - authority_boundary
```

Universal boundary:

```yaml
NO_FAKE_GREEN: TRUE
AUTHORITY: FALSE_UNLESS_EXTERNALLY_VERIFIED
NO_INTENT_WITHOUT_EVIDENCE: TRUE
NO_CASE_WITHOUT_FORUM_AND_FACTS: TRUE
NO_REPO_AS_COURT: TRUE
```

---

## Rules for PR #314

PR #314 is treated as the source replay event only if its artifacts and merge state can be verified directly.

```yaml
PR_314_RULES:
  role: SOURCE_REPLAY_EVENT
  must_verify:
    - pr_state
    - merge_state
    - commit_sha
    - changed_files
    - receipt_artifact
    - verifier_result
  may_claim:
    - source_event_exists
    - receipt_path_if_present
    - replay_input_if_committed
  may_not_claim:
    - legal_outcome
    - intent
    - government_acceptance
    - wealth_outcome
    - authority_without_external_receipt
```

If PR #314 is referenced by another PR, the downstream PR must cite exact commit SHA, file path, and verifier surface.

```yaml
PR_314_REFERENCE_RULE:
  exact_sha_required: TRUE
  exact_file_path_required: TRUE
  verifier_status_required: TRUE
```

---

## Rules for PR #315

PR #315 carried cross-round replay PASS metadata but became oversized and non-mergeable.

```yaml
PR_315_RULES:
  role: OVERSIZED_REPLAY_SURFACE
  source_pr_head_sha: 0a16480220fceb1b29a2e240ab569e15ebea5a39
  changed_files_observed: 10548
  merge_attempt_result: BLOCKED_MERGE_CONFLICTS
  status: RED_YELLOW
```

PR #315 may be used as a source surface for metadata, but it must not be merged as-is while conflicts and massive unrelated changes remain.

```yaml
PR_315_MAY_CLAIM:
  - replay_pass_metadata_declared_in_pr_body
  - source_hashes_declared_in_pr_body
  - oversized_branch_conflict_detected

PR_315_MAY_NOT_CLAIM:
  - clean_merge_surface
  - final_authority
  - schema_uid_verified
  - ethereum_keccak_bridge_complete
  - controller_verified
```

Correct handling:

```yaml
PR_315_HANDLING:
  do_not_merge_oversized_surface: TRUE
  create_atomic_replacement_branch: TRUE
  preserve_metadata_in_receipt: TRUE
  reopen_gate_only_after_checks: TRUE
```

---

## Rules for PR #316 and Forward

Future PRs must be atomic unless explicitly labeled as migration, archive, or bulk import.

```yaml
FORWARD_RULES:
  default_pr_size: ATOMIC
  expected_changed_files: 1_TO_5
  bulk_change_requires_manifest: TRUE
  cross_repo_claim_requires_network_receipt: TRUE
  external_authority_claim_requires_external_receipt: TRUE
```

Any PR that references Merkle trees, compute techniques, receipts, or replay vectors must include:

```yaml
COMPUTE_REQUIRED_FIELDS:
  - hash_domain
  - canonicalization_method
  - input_file_path
  - output_digest
  - verifier_or_script_path
  - pending_gates
```

---

## Cross-Repo JSONWisdom Rules

`jsonwisdom/AL` is one sliver of the JSONWisdom network.

```yaml
AL_IS_SLIVER: TRUE
JSONWISDOM_NETWORK_IN_SCOPE: TRUE
REPO_COUNT_DECLARED_BY_OPERATOR: 26_PLUS
REPLAY_REPO_DOES_NOT_EQUAL_SINGLE_REPO: TRUE
```

Cross-repo claims must identify:

```yaml
CROSS_REPO_REQUIRED_FIELDS:
  - repo_name
  - branch_or_commit
  - artifact_path
  - receipt_path
  - relationship_to_current_pr
```

---

## Goblin / Sniffing Boundary

Public repos may be read, but fragments must not be stripped from context and presented as authority.

```yaml
FRAGMENT_SNIFFING_WITHOUT_CONTEXT: REJECTED
MISATTRIBUTION: REJECTED
FAKE_AUTHORITY_OVER_JAY_REPOS: REJECTED
REPLAY_FIRST_REQUIRED: TRUE
NO_RECEIPT_NO_AUTHORITY: TRUE
```

---

## Final State

```yaml
RULES_FOR_314: PRINTED
RULES_FOR_315: PRINTED
RULES_FOR_FORWARD_PRS: PRINTED
JSONWISDOM_NETWORK_SCOPE: ACTIVE
MERKLE_AND_COMPUTE_RULES: ACTIVE
MEMBRANE: HOLDS
NO_FAKE_GREEN: ACTIVE
AUTHORITY: FALSE
```
