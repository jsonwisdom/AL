import { sha256HexCanonical } from "./hash.js";
import { type VerifiedStateV0 } from "./verified-state.js";

export type A0ExtractionReceiptV0 = Readonly<{
  layer: "A_RECONSTRUCTION_V0";
  verified_state_hash: string;
  state_hash: string;
  policy_hash: string;
  algorithm_hash: string;
  operation: "OPTIMIZE";
  input_authority: "VERIFIED_STATE_ONLY";
  raw_input_access: false;
  output_hash: string;
  reconstruction_hash: string;
  verdict: "COMPLETED" | "REFUSED";
  reason: "STATE_VERIFIED" | "INVALID_HANDSHAKE";
}>;

export function runA0Extraction(
  state: VerifiedStateV0,
  algorithmSpec: Record<string, unknown>
): A0ExtractionReceiptV0 {
  if (state.admissibility_status !== "ADMISSIBLE") {
    throw new Error("INVALID_HANDSHAKE");
  }

  const outputHash = sha256HexCanonical({
    claim: "OPERATIONAL",
    transition: state.transition_class
  });

  const algorithmHash = sha256HexCanonical(algorithmSpec);

  const reconstructionHash = sha256HexCanonical({
    verified_state_hash: state.current_state_hash,
    algorithm_hash: algorithmHash,
    output_hash: outputHash,
    policy_hash: state.policy_hash
  });

  return {
    layer: "A_RECONSTRUCTION_V0",
    verified_state_hash: state.current_state_hash,
    state_hash: state.current_state_hash,
    policy_hash: state.policy_hash,
    algorithm_hash: algorithmHash,
    operation: "OPTIMIZE",
    input_authority: "VERIFIED_STATE_ONLY",
    raw_input_access: false,
    output_hash: outputHash,
    reconstruction_hash: reconstructionHash,
    verdict: "COMPLETED",
    reason: "STATE_VERIFIED"
  };
}
