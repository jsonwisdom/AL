# subset_proof_v1 schema-mapping-v1

Status: DRAFT_PROJECTION_ONLY
Source law: `specs/subset_proof_v1/constraints-v1.md`
Ratified by: PR #181, merge `121fac730f2b7a0ca9312fbdbc6ad4389bd11c8d`

## Rule

```text
constraint_id → schema_path → schema_rule → fixture_ids → fixture_status
```

Every schema field MUST cite a constraint ID. If a field cannot cite a constraint, it MUST NOT enter the schema.

Fixtures listed here are declared by `constraints-v1.md` but are not implemented yet.

Current fixture status:

```text
DECLARED_NOT_IMPLEMENTED
```

This mapping is lawful derivation, not executable conformance.

---

## Core schema fields

| constraint_id | schema_path | schema_rule | fixture_ids | fixture_status |
| --- | --- | --- | --- | --- |
| HALT-001 | `$.proof_type` | `const: "HALT"` for halt proof branch | `halt_valid.json`, `halt_invalid_added_capability.json` | DECLARED_NOT_IMPLEMENTED |
| HALT-001 | `$.added_capabilities` | `const: []` when `proof_type == "HALT"` | `halt_valid.json`, `halt_invalid_added_capability.json` | DECLARED_NOT_IMPLEMENTED |
| HALT-002 | `$.pre_capabilities` | required array of capability strings | `halt_valid.json`, `halt_invalid_not_subset.json` | DECLARED_NOT_IMPLEMENTED |
| HALT-002 | `$.post_capabilities` | required array; verifier must check subset relation | `halt_valid.json`, `halt_invalid_not_subset.json` | DECLARED_NOT_IMPLEMENTED |
| HALT-002 | `$.subset_relation` | `const: "POST_SUBSET_OF_PRE"` for halt proof branch | `halt_valid.json`, `halt_invalid_not_subset.json` | DECLARED_NOT_IMPLEMENTED |
| HALT-003 | `$.strict_paths_expressible` | `const: false` when `proof_type == "HALT"` | `halt_invalid_strict_path_expressible.json` | DECLARED_NOT_IMPLEMENTED |
| HALT-004 | `$.halt_scope` | enum: `STRICT_ZONE_ALL`, `DOMAIN_SPLIT_RECEIPTED` | `halt_invalid_partial_without_domain_split_receipt.json`, `halt_valid_with_domain_split_receipt.json` | DECLARED_NOT_IMPLEMENTED |
| HALT-004 | `$.domain_split_receipt_hash` | required when `halt_scope == "DOMAIN_SPLIT_RECEIPTED"` | `halt_valid_with_domain_split_receipt.json` | DECLARED_NOT_IMPLEMENTED |
| HALT-005 | `$.active_classifier_receipt_hash` | required string | `halt_invalid_missing_active_classifier_receipt.json` | DECLARED_NOT_IMPLEMENTED |
| UNHALT-001 | `$.valid_receipt_hash` | required string when `proof_type == "UNHALT"` | `unhalt_valid.json`, `unhalt_invalid_missing_valid_receipt.json` | DECLARED_NOT_IMPLEMENTED |
| UNHALT-002 | `$.old_classifier_approval_hash` | required string when `proof_type == "UNHALT"` | `unhalt_invalid_missing_old_classifier_approval.json` | DECLARED_NOT_IMPLEMENTED |
| UNHALT-003 | `$.postmortem_receipt_hash` | required string when `proof_type == "UNHALT"` | `unhalt_invalid_missing_postmortem_receipt.json` | DECLARED_NOT_IMPLEMENTED |
| UNHALT-004 | `$.halted_capabilities` | required array for unhalt proof branch | `unhalt_valid.json`, `unhalt_invalid_new_capability.json` | DECLARED_NOT_IMPLEMENTED |
| UNHALT-004 | `$.post_capabilities` | required array; verifier must check restored set does not exceed pre-halt | `unhalt_valid.json`, `unhalt_invalid_new_capability.json` | DECLARED_NOT_IMPLEMENTED |
| UNHALT-005 | `$.pre_halt_capabilities` | required array for unhalt proof branch | `unhalt_invalid_new_capability.json` | DECLARED_NOT_IMPLEMENTED |
| UNHALT-005 | `$.no_new_capabilities_vs_pre_halt` | `const: true` when `proof_type == "UNHALT"` | `unhalt_invalid_new_capability.json` | DECLARED_NOT_IMPLEMENTED |
| UNHALT-006 | `$.delay_required` | boolean | `unhalt_invalid_delay_not_satisfied.json` | DECLARED_NOT_IMPLEMENTED |
| UNHALT-006 | `$.delay_satisfied` | if `delay_required == true`, must be `true` | `unhalt_invalid_delay_not_satisfied.json` | DECLARED_NOT_IMPLEMENTED |
| UPGRADE-001 | `$.old_law_receipt_hash` | required string when `proof_type == "UPGRADE_CLASSIFIER"` | `upgrade_classifier_pending_valid.json`, `upgrade_classifier_invalid_no_old_law_receipt.json` | DECLARED_NOT_IMPLEMENTED |
| UPGRADE-002 | `$.strict_to_optimistic_downgrade` | boolean | `upgrade_classifier_invalid_strict_downgrade_no_pending_window.json` | DECLARED_NOT_IMPLEMENTED |
| UPGRADE-002 | `$.pending_window_status` | if downgrade true, `const: "PENDING"` before activation | `upgrade_classifier_invalid_strict_downgrade_no_pending_window.json` | DECLARED_NOT_IMPLEMENTED |
| UPGRADE-003 | `$.policy_diff_hash` | required string when `proof_type == "UPGRADE_CLASSIFIER"` | `upgrade_classifier_invalid_missing_diff_hash.json` | DECLARED_NOT_IMPLEMENTED |
| UPGRADE-004 | `$.objection_status` | enum: `NONE`, `RESOLVED`; unresolved objections invalid | `upgrade_classifier_invalid_unresolved_objection.json` | DECLARED_NOT_IMPLEMENTED |
| UPGRADE-005 | `$.self_bootstrap_reduction` | `const: false` unless old law authorized reduction | `upgrade_classifier_invalid_self_bootstrap.json` | DECLARED_NOT_IMPLEMENTED |
| CONTAGION-001 | `$.touched_paths` | required array of path strings | `strict_contagion_valid.json`, `strict_contagion_invalid_optimistic_treasury_touch.json` | DECLARED_NOT_IMPLEMENTED |
| CONTAGION-001 | `$.derived_zone` | if touched strict paths exist, `const: "STRICT"` | `strict_contagion_valid.json`, `strict_contagion_invalid_optimistic_treasury_touch.json` | DECLARED_NOT_IMPLEMENTED |
| CONTAGION-002 | `$.call_graph` | array describing invoked actions | `strict_contagion_invalid_nontransitive_call.json` | DECLARED_NOT_IMPLEMENTED |
| CONTAGION-002 | `$.transitive_contagion_checked` | `const: true` for contagion proofs | `strict_contagion_invalid_nontransitive_call.json` | DECLARED_NOT_IMPLEMENTED |
| CONTAGION-003 | `$.contagion_derivation_receipt_hash` | required string | `strict_contagion_invalid_missing_derivation_receipt.json` | DECLARED_NOT_IMPLEMENTED |
| OPTIMISTIC-001 | `$.optimistic_window.wall_clock_ms` | required integer for optimistic proof branch | `optimistic_valid_within_window.json`, `optimistic_invalid_window_expired.json` | DECLARED_NOT_IMPLEMENTED |
| OPTIMISTIC-001 | `$.optimistic_window.sequence_delta` | required integer for optimistic proof branch | `optimistic_valid_within_window.json`, `optimistic_invalid_window_expired.json` | DECLARED_NOT_IMPLEMENTED |
| OPTIMISTIC-001 | `$.optimistic_window.receipt_depth` | required integer for optimistic proof branch | `optimistic_valid_within_window.json`, `optimistic_invalid_window_expired.json` | DECLARED_NOT_IMPLEMENTED |
| OPTIMISTIC-002 | `$.quarantine_status` | if verification fails or window expires, `const: "QUARANTINED"` | `optimistic_expired_quarantine_valid.json`, `optimistic_invalid_human_override_preserves_state.json` | DECLARED_NOT_IMPLEMENTED |
| OPTIMISTIC-003 | `$.replay_debt_charged_to_actor` | `const: true` when optimistic action fails | `optimistic_invalid_no_replay_debt_charge.json` | DECLARED_NOT_IMPLEMENTED |

---

## Explicitly rejected candidate fields

| field | blocker | reason |
| --- | --- | --- |
| `$.ui_hint` | SCHEMA_FIELD_WITHOUT_CONSTRAINT | Dashboard convenience is not law. |
| `$.display_color` | SCHEMA_FIELD_WITHOUT_CONSTRAINT | Renderer preference is not law. |
| `$.operator_note` | SCHEMA_FIELD_WITHOUT_CONSTRAINT | Narrative is not admissibility. |

---

## Status

```json
{
  "schema_may_be_drafted": true,
  "schema_may_claim_full_conformance": false,
  "reason": "fixtures are declared but not implemented"
}
```
