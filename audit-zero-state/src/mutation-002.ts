import { ZERO_STATE } from "./zero-state.ts";
import { canonicalize, utf8Bytes, bytesHex } from "./jcs.ts";
import { sha256Hex } from "./digest.ts";
import { runMutation001Audit } from "./mutation-001.ts";
import { exitRuntime } from "./runtime.ts";

const DETERMINISTIC_NONCE = "MUTATION_002_NONCE_0000000000000001" as const;

export async function runMutation002Audit() {
  const mutation001 = await runMutation001Audit();

  const payload = {
    schema: "SIGNED_PAYLOAD_STRUCTURE_V1",
    nonce: DETERMINISTIC_NONCE,
    previous_state_hash: mutation001.post_state_hash,
    claims: [
      "PAYLOAD_SOVEREIGNTY_ESTABLISHED",
      "RUNTIME_ROLE_EXECUTION_WITNESS_ONLY",
      "NO_AMBIENT_TIME",
      "NO_RANDOM_NONCE"
    ],
    signer: {
      scheme: "DETERMINISTIC_PLACEHOLDER_NO_PRIVATE_KEY",
      key_id: "KEY_DEFERRED_PRODUCTION_SIGNING"
    }
  };

  const payloadCanonical = canonicalize(payload);
  const payloadBytes = utf8Bytes(payloadCanonical);
  const payloadHash = await sha256Hex(payloadBytes);

  const operation = {
    type: "APPLY_SIGNED_PAYLOAD_STRUCTURE",
    nonce: DETERMINISTIC_NONCE,
    previous_state_hash: mutation001.post_state_hash,
    payload_hash: payloadHash
  };

  const opCanonical = canonicalize(operation);
  const opBytes = utf8Bytes(opCanonical);
  const opHash = await sha256Hex(opBytes);

  const postState = {
    ...ZERO_STATE,
    mutation_count: 2,
    last_mutation: {
      operation_hash: opHash,
      applied_at_state: mutation001.post_state_hash
    },
    signed_payload: {
      payload_hash: payloadHash,
      nonce: DETERMINISTIC_NONCE,
      signature_status: "STRUCTURE_ONLY_UNSIGNED"
    }
  };

  const postCanonical = canonicalize(postState);
  const postBytes = utf8Bytes(postCanonical);
  const postHash = await sha256Hex(postBytes);

  const auditRecord = {
    gate: "MUTATION_002_PARITY",
    previous_post_state_hash: mutation001.post_state_hash,
    nonce: DETERMINISTIC_NONCE,
    payload_hash: payloadHash,
    operation_hash: opHash,
    post_state_hash: postHash,
    payload_canonical_bytes_hex: bytesHex(payloadBytes),
    op_canonical_bytes_hex: bytesHex(opBytes),
    post_canonical_bytes_hex: bytesHex(postBytes),
    mutation_count_verified: postState.mutation_count === 2,
    ambient_time_used: false,
    random_nonce_used: false,
    signature_status: "STRUCTURE_ONLY_UNSIGNED"
  };

  if (!auditRecord.mutation_count_verified) {
    console.error("FAIL:MUTATION_002_COUNT");
    exitRuntime(1);
  }

  return auditRecord;
}
