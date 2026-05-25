import { sha256HexCanonical } from "./hash.js";

export type TransitionClass =
  | "REVERSIBLE"
  | "MONOTONIC"
  | "APPEND_ONLY"
  | "IRREVERSIBLE";

export type P1TemporalReceiptV0 = Readonly<{
  receipt_type: "P1_TEMPORAL_RECEIPT_V0";
  test_vector_id: string;
  policy_hash: string;
  previous_state_hash: string;
  p0_receipt_hash: string;
  input_hash: string;
  gate_id: "TEMPORAL_CONSISTENCY_GATE_V0";
  sequence_number: number;
  previous_sequence_number: number;
  sequence_delta: number;
  sequence_rule: "STRICT_MONOTONIC";
  ordering_status: "IN_ORDER" | "GAP_DETECTED" | "DUPLICATE_OR_REWIND";
  transition_class: TransitionClass;
  verdict: "ADMISSIBLE" | "REFUSE";
  reason: "WINDOW_CONVERGENT" | "GAP_DETECTED" | "DUPLICATE_OR_REWIND";
}>;

export function runP1TemporalGate(args: Readonly<{
  test_vector_id: string;
  policy_hash: string;
  previous_state_hash: string;
  p0_receipt_hash: string;
  input_hash: string;
  sequence_number: number;
  previous_sequence_number: number;
  transition_class: TransitionClass;
}>): P1TemporalReceiptV0 {
  const delta = args.sequence_number - args.previous_sequence_number;
  const admissible = delta === 1;

  return {
    receipt_type: "P1_TEMPORAL_RECEIPT_V0",
    test_vector_id: args.test_vector_id,
    policy_hash: args.policy_hash,
    previous_state_hash: args.previous_state_hash,
    p0_receipt_hash: args.p0_receipt_hash,
    input_hash: args.input_hash,
    gate_id: "TEMPORAL_CONSISTENCY_GATE_V0",
    sequence_number: args.sequence_number,
    previous_sequence_number: args.previous_sequence_number,
    sequence_delta: delta,
    sequence_rule: "STRICT_MONOTONIC",
    ordering_status:
      delta === 1
        ? "IN_ORDER"
        : delta > 1
          ? "GAP_DETECTED"
          : "DUPLICATE_OR_REWIND",
    transition_class: args.transition_class,
    verdict: admissible ? "ADMISSIBLE" : "REFUSE",
    reason:
      delta === 1
        ? "WINDOW_CONVERGENT"
        : delta > 1
          ? "GAP_DETECTED"
          : "DUPLICATE_OR_REWIND"
  };
}

export function hashP1TemporalReceipt(receipt: P1TemporalReceiptV0): string {
  return sha256HexCanonical(receipt);
}
