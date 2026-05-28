# Open The Store: Machine-Speed Commerce v0.1

Status: Draft Store Blueprint  
Builder: Jason Wisdom / jaywisdom.eth / jaywisdom.base.eth  
Project: Jay's AL / Alabama Looking Glass / JSONWisdom Applied  
Scope: Productization, MCP agent integration, Base Networks and beyond  
Authority: false  
Legal advice: false  
Government authority claimed: false

## Root Claim

Open the store.

Jay's AL is sellable at machine speed because the framework already has product surfaces:

- receipts
- replay
- citizen letter review
- media flywheels
- governance flywheels
- school routes
- family learning
- Computer Wisdom bridge
- MCP agent missions
- Base-compatible payment proofs
- ABI-style on/off switches

## One-Line Store Positioning

```txt
JSONWisdom Applied sells machine-speed learning, verification, receipts, and replay as bounded missions.
```

## Six-Year-Old Version

```txt
Pick a mission.
Pay if it costs money.
The helper checks the rule.
You get a receipt.
```

## Storefront Categories

```json
{
  "storefront": {
    "learning_routes": "school_and_family_courses",
    "document_help": "plain_language_letter_review",
    "receipt_tools": "proof_cards_hashes_timelines",
    "replay_tools": "safe_review_without_live_mutation",
    "mcp_agents": "bounded_agent_missions",
    "base_networks": "payment_proofs_and_public_witness_paths",
    "developer_kits": "schemas_sdks_and_abi_switches",
    "enterprise_labs": "governance_media_and_compliance_learning_flywheels"
  }
}
```

## Sellable Products

### 1. Citizen Letter Review

```json
{
  "sku": "LETTER_REVIEW_V0_1",
  "customer": "citizen_or_family",
  "input": "photo_or_text_of_letter",
  "output": "plain_language_summary_deadlines_questions_receipt",
  "price_model": "per_review_or_subscription",
  "legal_advice": false
}
```

### 2. School Route Pack

```json
{
  "sku": "SCHOOL_ROUTE_PACK_V0_1",
  "customer": "teacher_parent_school_builder",
  "output": "lesson_routes_receipt_cards_privacy_games",
  "price_model": "classroom_license_or_family_pass",
  "student_private_data_collection": false
}
```

### 3. Receipt API

```json
{
  "sku": "RECEIPT_API_V0_1",
  "customer": "developers_agents_platforms",
  "output": "hash_receipt_timeline_and_signature_objects",
  "price_model": "usage_based",
  "machine_speed": true
}
```

### 4. Replay Lab

```json
{
  "sku": "REPLAY_LAB_V0_1",
  "customer": "builders_teams_auditors_students",
  "output": "safe_offline_replay_and_divergence_detection",
  "price_model": "seat_based_or_usage_based",
  "live_api_calls": false
}
```

### 5. MCP Agent Mission Pack

```json
{
  "sku": "MCP_AGENT_MISSION_PACK_V0_1",
  "customer": "agent_builders_and_operators",
  "output": "bounded_agent_missions_with_scope_payment_proof_and_receipts",
  "price_model": "per_mission_per_agent_or_subscription",
  "authority": false
}
```

### 6. Base Payment Proof Kit

```json
{
  "sku": "BASE_PAYMENT_PROOF_KIT_V0_1",
  "customer": "onchain_builders_agent_commerce_teams",
  "output": "payment_proof_gates_receipts_replay_paths_and_public_witness_templates",
  "price_model": "developer_license_or_usage",
  "chain": "Base_and_beyond"
}
```

## ABI On/Off Switches

ABI switches are mission gates.

They do not control people.
They control whether a bounded function is allowed to execute.

```json
{
  "abi_switches": {
    "ASK": "enabled_when_user_mission_exists",
    "CHECK": "enabled_when_source_or_document_exists",
    "BUILD": "enabled_when_scope_hash_exists",
    "REPLAY": "enabled_when_fixture_or_receipt_exists",
    "RECEIPT": "enabled_when_output_can_be_hashed",
    "PAY": "enabled_when_payment_proof_required",
    "PUBLISH": "enabled_when_private_data_removed"
  }
}
```

## Mission Gate Object

```json
{
  "mission_gate": {
    "mission_id": "string",
    "actor": "human_or_agent",
    "scope_hash": "sha256",
    "payment_proof_required": true,
    "payment_proof_present": false,
    "privacy_check_passed": false,
    "receipt_required": true,
    "execution_status": "OFF_UNTIL_PROVEN"
  }
}
```

## MCP Agent Integration

MCP agents should be allowed to act only through bounded missions.

```json
{
  "mcp_agent_rules": [
    "agent_must_declare_mission",
    "agent_must_receive_scope",
    "agent_must_not_collect_unneeded_private_data",
    "agent_must_create_receipt",
    "agent_must_refuse_live_replay_mutation",
    "agent_must_fail_closed_without_payment_proof_when_required"
  ]
}
```

## Base Networks And Beyond

Base is the first natural network because AL already has:

- jaywisdom.base.eth identity
- payment-proof framing
- receipt anchoring logic
- agent commerce compatibility
- public witness paths

Beyond Base, the store should remain chain-neutral:

```json
{
  "network_strategy": {
    "base": "first_public_witness_and_payment_proof_path",
    "beyond": "chain_neutral_receipts_and_replay",
    "truth_model": "receipts_not_chain_maximalism"
  }
}
```

## Profit Paths

```json
{
  "profit_paths": [
    "pay_per_document_review",
    "monthly_family_learning_pass",
    "teacher_classroom_license",
    "developer_receipt_api_usage",
    "replay_lab_subscriptions",
    "mcp_agent_mission_fees",
    "base_payment_proof_kits",
    "enterprise_governance_learning_labs",
    "custom_receipt_schema_design",
    "public_verifier_service_contracts"
  ]
}
```

## Store Safety Rules

```json
{
  "store_safety_rules": [
    "no_legal_advice_claims",
    "no_government_authority_claims",
    "no_private_child_data_collection",
    "no_live_api_calls_during_replay",
    "no_unverified_accusation_promotion",
    "no_harassment_or_targeting",
    "no_payment_claim_without_payment_proof",
    "no_execution_without_scope",
    "no_publish_without_private_data_removal"
  ]
}
```

## First Store Launch

Launch with three paid/free surfaces:

```json
{
  "phase_1": [
    {
      "name": "Free Demo: Zero to Receipt",
      "price": "free",
      "purpose": "teach the loop"
    },
    {
      "name": "Citizen Letter Review Receipt",
      "price": "paid_per_review",
      "purpose": "document understanding"
    },
    {
      "name": "MCP Agent Mission Receipt Kit",
      "price": "developer_license",
      "purpose": "agent commerce integration"
    }
  ]
}
```

## Public Store Line

```txt
Open the store: missions in, receipts out, replay ready, payment proof up front.
```

## Final Line

```txt
Jay's AL becomes profitable when every useful machine-speed action is sold as a bounded, receipted, replayable mission.
```

By Jason Wisdom  
jaywisdom.eth  
jaywisdom.base.eth