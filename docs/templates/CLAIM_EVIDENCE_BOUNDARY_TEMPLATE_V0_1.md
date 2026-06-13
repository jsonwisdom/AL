# CLAIM_EVIDENCE_BOUNDARY_TEMPLATE_V0_1

## STATUS: REUSABLE_FIXTURE_TEMPLATE
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

This template defines the standard structure for documenting claims in the repo without turning reported information into verified fact.

Use this for Zora, Base, token, revenue, artifact, profile, API, validator, fixture, and replay claims.

## Template

```markdown
# <CLAIM_NAME>_V0_1

## STATUS: <DRAFT | REPORTED | READ_ONLY_PLAN | VERIFIED_BY_OUTPUT | BLOCKED>
## AUTHORITY: FALSE
## NO_FAKE_GREEN: TRUE

One plain-English sentence describing what this file is and what it is not.

## 1. Reported Claim / Claimed Mechanics

The following is reported, claimed, observed in a screenshot, or proposed. It is not verified unless the evidence section says so.

```text
claim_subject=<thing being claimed>
claim_source=<self_report | screenshot | csv_export | rpc_output | api_response | repo_file | manual_entry>
claim_status=<reported | observed | unverified | verified_by_output>
assistant_independent_verification=false
```

## 2. Evidence That Would Verify It

```text
required_evidence_1=<specific command, file, screenshot, API output, explorer readback, or hash>
required_evidence_2=<optional additional evidence>
required_evidence_3=<optional additional evidence>
```

Acceptable evidence examples:

```text
local_command_stdout
committed_json_receipt
csv_export
rpc_call_output
verified_contract_abi
screenshot_with_visible_field
explorer_readback
api_response_json
sha256_hash
commit_sha
```

## 3. Current Evidence Status

```text
evidence_present=false
raw_output_committed=false
validator_output_committed=false
screenshot_observed=false
api_or_rpc_readback_observed=false
claim_verified=false
```

## 4. Hard Boundary

```text
reported_claim != verified_fact
screenshot != full_export
transaction_hash != contract_verification
transfer_history != revenue
claimable != claimed
view_call != transaction
profile_surface != full_catalog
operator_report != independent_verification
```

## 5. Allowed Next Action

```text
next_action=<one concrete action>
allowed_mode=read_only
wallet_control=false
signing=false
broadcast=false
```

## 6. Forbidden Upgrade

```text
reported_to_verified_without_evidence=false
screenshot_to_revenue=false
profile_to_full_catalog=false
transaction_to_contract_verification=false
operator_report_to_independent_verification=false
```

## Ruling

```text
CLAIM_STATUS = <REPORTED | OBSERVED | VERIFIED_BY_OUTPUT | BLOCKED>
VERIFIED_FEED_REQUIRED = TRUE
REVENUE = NOT_CONFIRMED
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
```

## Usage Notes

Use this template when cleaning older files that sound stronger than their evidence supports.

Recommended replacements:

```text
"locked" -> "recorded" unless a real command output or commit readback exists
"validated" -> "validated by <specific output>" or "pending validation"
"classifier" -> "script" or "manual review" unless a real classifier exists
"node query" -> "RPC command" only when an actual RPC command/output exists
"anchor" -> "candidate anchor" unless source bytes and verification output exist
"operator-reported" -> "self-reported" when the same person supplied the claim
```

## Ruling

```text
TEMPLATE_READY = TRUE
RETROACTIVE_REPO_CLEANUP_STANDARD = TRUE
AUTHORITY = FALSE
NO_FAKE_GREEN = TRUE
```
