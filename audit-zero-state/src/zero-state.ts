export const ZERO_STATE = {
  constitutional_oracle_v1: {
    status: "SEALED",
    state: "BUILD_READY",
    axiom: "PROCEDURE_IS_AUTHORITY",
    receipt_rule: "NO_RECEIPT_NO_CANON",
    ambiguity_rule: "REFUSAL_OVER_AMBIGUITY"
  },
  zero_state_anchor: true,
  mutation_count: 0
} as const;
