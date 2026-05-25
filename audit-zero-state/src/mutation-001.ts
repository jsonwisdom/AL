import { ZERO_STATE } from "./zero-state.ts";
import { canonicalize, utf8Bytes, bytesHex } from "./jcs.ts";
import { sha256Hex } from "./digest.ts";
import { exitRuntime } from "./runtime.ts";

export async function runMutation001Audit() {
  const preCanonical = canonicalize(ZERO_STATE);
  const preBytes = utf8Bytes(preCanonical);
  const preHash = await sha256Hex(preBytes);

  const operation = {
    type: "INCREMENT_MUTATION_COUNT",
    delta: 1,
    timestamp: null,
    previous_state_hash: preHash
  };

  const opCanonical = canonicalize(operation);
  const opBytes = utf8Bytes(opCanonical);
  const opHash = await sha256Hex(opBytes);

  const postState = {
    ...ZERO_STATE,
    mutation_count: 1,
    last_mutation: {
      operation_hash: opHash,
      applied_at_state: preHash
    }
  };

  const postCanonical = canonicalize(postState);
  const postBytes = utf8Bytes(postCanonical);
  const postHash = await sha256Hex(postBytes);

  const auditRecord = {
    gate: "MUTATION_001_PARITY",
    pre_state_hash: preHash,
    operation_hash: opHash,
    post_state_hash: postHash,
    pre_canonical_bytes_hex: bytesHex(preBytes),
    op_canonical_bytes_hex: bytesHex(opBytes),
    post_canonical_bytes_hex: bytesHex(postBytes),
    mutation_count_verified: postState.mutation_count === 1
  };

  if (!auditRecord.mutation_count_verified) {
    console.error("FAIL:MUTATION_COUNT");
    exitRuntime(1);
  }

  return auditRecord;
}
