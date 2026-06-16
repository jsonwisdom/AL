# Expand, Loop, Membrane, Return, Repeat v0.1

Status: Draft Runtime / Store Primitive  
Builder: Jason Wisdom / jaywisdom.eth / jaywisdom.base.eth  
Project: Jay's AL / Alabama Looking Glass / JSONWisdom Applied  
Scope: Machine-speed commerce, MCP agents, Base-compatible missions  
Authority: false

## Root Formula

```txt
Expand.
Loop.
Membrane.
Return.
Repeat.
```

This is the runtime rhythm for Jay's store.

A mission enters.  
The system expands context.  
The agent loops through bounded work.  
The membrane checks scope, payment, privacy, and receipts.  
The result returns with proof.  
The next mission repeats from a cleaner state.

## Six-Year-Old Version

```txt
Make the question bigger enough to understand.
Try the steps.
Check the rules.
Bring back the proof.
Try again better.
```

## Runtime Object

```json
{
  "runtime": "EXPAND_LOOP_MEMBRANE_RETURN_REPEAT",
  "expand": "gather_context_sources_scope_and_payment_requirements",
  "loop": "perform_bounded_steps_until_done_or_blocked",
  "membrane": "enforce_scope_privacy_payment_replay_and_receipt_rules",
  "return": "deliver_result_receipt_status_and_next_options",
  "repeat": "start_next_mission_from_receipted_state",
  "authority": false
}
```

## Store Translation

```json
{
  "store_loop": {
    "customer_input": "mission_or_document_or_question",
    "expand": "classify_need_and_required_proofs",
    "loop": "run_allowed_agent_steps",
    "membrane": "fail_closed_if_scope_payment_or_privacy_rules_break",
    "return": "summary_receipt_timeline_and_next_action",
    "repeat": "offer_next_paid_or_free_bounded_mission"
  }
}
```

## ABI Switch Translation

```json
{
  "abi_switches": {
    "EXPAND": "ON_when_input_and_scope_exist",
    "LOOP": "ON_when_steps_are_bounded",
    "MEMBRANE": "ALWAYS_ON",
    "RETURN": "ON_when_result_can_be_receipted",
    "REPEAT": "ON_when_next_mission_is_scoped"
  }
}
```

## MCP Agent Rule

MCP agents do not get open-ended authority.

They get mission loops.

```json
{
  "mcp_agent_mission_loop": {
    "agent_receives": [
      "mission_id",
      "scope_hash",
      "allowed_tools",
      "forbidden_tools",
      "payment_proof_status",
      "privacy_rules",
      "receipt_requirement"
    ],
    "agent_returns": [
      "result",
      "steps_taken",
      "tools_used",
      "receipt",
      "blocked_reasons",
      "next_options"
    ]
  }
}
```

## Membrane Checks

```json
{
  "membrane_checks": [
    "source_check",
    "scope_check",
    "privacy_check",
    "payment_proof_check",
    "tool_allowlist_check",
    "receipt_check",
    "replay_safety_check",
    "publish_safety_check"
  ]
}
```

## Fail-Closed Cases

```json
{
  "fail_closed": [
    "no_scope",
    "missing_required_payment_proof",
    "private_data_not_redacted",
    "tool_not_allowed",
    "live_api_call_attempted_during_replay",
    "result_cannot_be_receipted",
    "next_mission_not_scoped",
    "authority_claim_attempted"
  ]
}
```

## Profit Logic

```json
{
  "profit_logic": {
    "free": "teach_the_loop",
    "paid": "run_bounded_missions",
    "premium": "multi_step_loops_with_receipts_and_replay",
    "enterprise": "custom_membranes_and_verifier_contracts",
    "base_networks": "payment_proofs_public_witness_and_agent_commerce",
    "beyond": "chain_neutral_receipts_and_replay"
  }
}
```

## Public Store Line

```txt
Expand the mission. Loop the work. Membrane the risk. Return the receipt. Repeat safely.
```

## Final Line

```txt
Jay's store grows when every repeatable loop produces a safer receipt than the loop before it.
```

By Jason Wisdom  
jaywisdom.eth  
jaywisdom.base.eth