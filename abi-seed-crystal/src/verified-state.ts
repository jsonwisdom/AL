import { sha256HexCanonical } from "./hash.js";
import { type P0NeutralityReceiptV0 } from "./p0-neutrality.js";
import {
  type P1TemporalReceiptV0,
  type TransitionClass
} from "./p1-temporal.js";

export type VerifiedStateV0 = Readonly<{
  type: "VERIFIED_STATE_V0";
  test_vector_id: string;
  state_hash_alg: "sha256-jcs-v0";
  previous_state_hash: string;
  current_state_hash: string;
  policy_hash: string;
  input_hash: string;
  p0_receipt_hash: string;
  p1_receipt_hash: string;
  sequence_number: number;
  previous_sequence_number: number;
  transition_class: TransitionClass;
  admissibility_status: "ADMISSIBLE";
  chain_status: "HASH_CONVERGENT";
  future_commitment_mode: "MERKLE_DAG_READY_NOT_ACTIVE";
}>;

export function emitVerifiedState(
  p0: P0NeutralityReceiptV0,
  p0Hash: string,
  p1: P1TemporalReceiptV0,
  p1Hash: string,
  previousStateHash: string
): VerifiedStateV0 {
  if (p0.verdict !== "ADMISSIBLE" || p1.verdict !== "ADMISSIBLE") {
    throw new Error("CANNOT_EMIT_NON_ADMISSIBLE_STATE");
  }

  if (p0.policy_hash !== p1.policy_hash) {
    throw new Error("POLICY_HASH_MISMATCH");
  }

  if (p0.input_hash !== p1.input_hash) {
    throw new Error("INPUT_HASH_MISMATCH");
  }

  if (p1.previous_state_hash !== previousStateHash) {
    throw new Error("PREVIOUS_STATE_HASH_MISMATCH");
  }

  const stateHashPayload = {
    state_hash_alg: "sha256-jcs-v0",
    previous_state_hash: previousStateHash,
    policy_hash: p1.policy_hash,
    input_hash: p1.input_hash,
    p0_receipt_hash: p0Hash,
    p1_receipt_hash: p1Hash,
    sequence_number: p1.sequence_number,
    previous_sequence_number: p1.previous_sequence_number,
    transition_class: p1.transition_class,
    future_commitment_mode: "MERKLE_DAG_READY_NOT_ACTIVE"
  } as const;

  return {
    type: "VERIFIED_STATE_V0",
    test_vector_id: p1.test_vector_id,
    state_hash_alg: "sha256-jcs-v0",
    previous_state_hash: previousStateHash,
    current_state_hash: sha256HexCanonical(stateHashPayload),
    policy_hash: p1.policy_hash,
    input_hash: p1.input_hash,
    p0_receipt_hash: p0Hash,
    p1_receipt_hash: p1Hash,
    sequence_number: p1.sequence_number,
    previous_sequence_number: p1.previous_sequence_number,
    transition_class: p1.transition_class,
    admissibility_status: "ADMISSIBLE",
    chain_status: "HASH_CONVERGENT",
    future_commitment_mode: "MERKLE_DAG_READY_NOT_ACTIVE"
  };
}
