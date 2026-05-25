export const POLICY_V0 = Object.freeze({
  policy_id: "ABI_POLICY_V0",
  neutrality_gate: {
    epsilon_static: "0.000001",
    epsilon_mode: "STATIC_ENFORCED_LOCAL_SHADOW",
    local_epsilon_active: false
  },
  temporal_gate: {
    sequence_rule: "STRICT_MONOTONIC",
    gap_policy: "REFUSE"
  },
  reconstruction: {
    raw_input_access_allowed: false,
    unresolved_policy: "RETURN_UNRESOLVED"
  },
  commitment: {
    state_hash_alg: "sha256-jcs-v0",
    future_commitment_mode: "MERKLE_DAG_READY_NOT_ACTIVE"
  }
} as const);
