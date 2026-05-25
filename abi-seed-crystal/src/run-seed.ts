import { sha256HexCanonical } from "./hash.js";
import { POLICY_V0 } from "./policy.js";
import {
  runP0NeutralityGate,
  hashP0NeutralityReceipt
} from "./p0-neutrality.js";
import {
  runP1TemporalGate,
  hashP1TemporalReceipt,
  type TransitionClass
} from "./p1-temporal.js";
import { emitVerifiedState } from "./verified-state.js";
import { runA0Extraction } from "./a0-receipt-extraction.js";

const POLICY_HASH = sha256HexCanonical(POLICY_V0);

console.log("POLICY_V0_HASH:", POLICY_HASH);

const TEST_VECTORS: readonly {
  readonly test_vector_id: string;
  readonly previous_state_hash: string;
  readonly sequence_number: number;
  readonly previous_sequence_number: number;
  readonly transition_class: TransitionClass;
  readonly signal: {
    readonly values_log_space: readonly [string, string];
  };
}[] = [
  {
    test_vector_id: "PASS_BASIC_001",
    previous_state_hash: "GENESIS",
    sequence_number: 1,
    previous_sequence_number: 0,
    transition_class: "REVERSIBLE",
    signal: {
      values_log_space: ["0.100000", "-0.100000"]
    }
  },
  {
    test_vector_id: "FAIL_NEUTRALITY_001",
    previous_state_hash: "GENESIS",
    sequence_number: 1,
    previous_sequence_number: 0,
    transition_class: "REVERSIBLE",
    signal: {
      values_log_space: ["0.100000", "-0.090000"]
    }
  },
  {
    test_vector_id: "FAIL_TEMPORAL_GAP_001",
    previous_state_hash: "GENESIS",
    sequence_number: 3,
    previous_sequence_number: 0,
    transition_class: "REVERSIBLE",
    signal: {
      values_log_space: ["0.100000", "-0.100000"]
    }
  }
] as const;

for (const vector of TEST_VECTORS) {
  const inputHash = sha256HexCanonical(vector.signal);

  const p0 = runP0NeutralityGate({
    test_vector_id: vector.test_vector_id,
    policy_hash: POLICY_HASH,
    input_hash: inputHash,
    values_log_space: vector.signal.values_log_space,
    epsilon_static: POLICY_V0.neutrality_gate.epsilon_static
  });

  if (p0.verdict === "REFUSE") {
    console.log(`[${vector.test_vector_id}] P0 REFUSE. Halt.`);
    continue;
  }

  const p0Hash = hashP0NeutralityReceipt(p0);

  const p1 = runP1TemporalGate({
    test_vector_id: vector.test_vector_id,
    policy_hash: POLICY_HASH,
    previous_state_hash: vector.previous_state_hash,
    p0_receipt_hash: p0Hash,
    input_hash: inputHash,
    sequence_number: vector.sequence_number,
    previous_sequence_number: vector.previous_sequence_number,
    transition_class: vector.transition_class
  });

  if (p1.verdict === "REFUSE") {
    console.log(`[${vector.test_vector_id}] P1 REFUSE. Halt.`);
    continue;
  }

  const p1Hash = hashP1TemporalReceipt(p1);

  const verifiedState = emitVerifiedState(
    p0,
    p0Hash,
    p1,
    p1Hash,
    vector.previous_state_hash
  );

  const a0Receipt = runA0Extraction(verifiedState, {
    spec: "A0_PROJECTION_V0"
  });

  console.log(
    `[${vector.test_vector_id}] ADMISSIBLE. State Hash: ${verifiedState.current_state_hash}`
  );

  console.log(
    `[${vector.test_vector_id}] RECONSTRUCTION HASH: ${a0Receipt.reconstruction_hash}`
  );
}
