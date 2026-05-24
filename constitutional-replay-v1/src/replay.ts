import { canonicalHash } from "./hash.js";
import { interpretPolicy, InterpreterResult } from "./interpreter.js";
import { loadPolicy, PolicyV1, policyHash } from "./policy.js";
import { ReceiptV1, validateReceiptEnvelope } from "./receipt.js";

export type ReplayStatus =
  | "VALID_REPLAY"
  | "REFUSAL_CONFIRMED"
  | "REPLAY_DIVERGENCE"
  | "RECEIPT_REJECTED";

export interface ReplayResult {
  replay_status: ReplayStatus;
  semantic_authority: "LOCAL_REPLAY";
  witness_status: "NOT_CHECKED";
  policy_hash_match: boolean;
  input_hash_match: boolean;
  interpreter_hash_match: boolean;
  replay_divergence: boolean;
  original_result: "SUCCESS" | "REFUSAL";
  replayed_result: "SUCCESS" | "REFUSAL" | null;
  original_refusal_code: string | null;
  replayed_refusal_code: string | null;
  failure_reason: string | null;
}

export interface ReplayReceiptArgs {
  receipt: unknown;
  policy: unknown;
  input: unknown;
  interpreter_hash: string;
}

function verdictMatches(receipt: ReceiptV1, replayed: InterpreterResult): boolean {
  return receipt.result === replayed.result && receipt.refusal_code === replayed.refusal_code;
}

function rejected(receipt: ReceiptV1 | null, failure: string): ReplayResult {
  return {
    replay_status: "RECEIPT_REJECTED",
    semantic_authority: "LOCAL_REPLAY",
    witness_status: "NOT_CHECKED",
    policy_hash_match: false,
    input_hash_match: false,
    interpreter_hash_match: false,
    replay_divergence: true,
    original_result: receipt?.result ?? "REFUSAL",
    replayed_result: null,
    original_refusal_code: receipt?.refusal_code ?? null,
    replayed_refusal_code: null,
    failure_reason: failure
  };
}

export function replayReceipt(args: ReplayReceiptArgs): ReplayResult {
  let receipt: ReceiptV1;

  try {
    receipt = validateReceiptEnvelope(args.receipt);
  } catch (error) {
    return rejected(null, error instanceof Error ? error.message : "INVALID_RECEIPT_SCHEMA");
  }

  let policy: PolicyV1;

  try {
    policy = loadPolicy(args.policy);
  } catch (error) {
    return rejected(receipt, error instanceof Error ? error.message : "POLICY_UNAVAILABLE");
  }

  const actualPolicyHash = policyHash(policy);
  const policy_hash_match = actualPolicyHash === receipt.policy_hash;
  const actualInputHash = canonicalHash(args.input);
  const input_hash_match = actualInputHash === receipt.input_hash;
  const interpreter_hash_match = args.interpreter_hash === receipt.interpreter_hash;

  if (!policy_hash_match) {
    return {
      ...rejected(receipt, "POLICY_HASH_MISMATCH"),
      policy_hash_match,
      input_hash_match,
      interpreter_hash_match
    };
  }

  if (!input_hash_match) {
    return {
      ...rejected(receipt, "INPUT_HASH_MISMATCH"),
      policy_hash_match,
      input_hash_match,
      interpreter_hash_match
    };
  }

  if (!interpreter_hash_match) {
    return {
      ...rejected(receipt, "INTERPRETER_HASH_MISMATCH"),
      policy_hash_match,
      input_hash_match,
      interpreter_hash_match
    };
  }

  const replayed = interpretPolicy(policy, args.input);
  const matches = verdictMatches(receipt, replayed);

  if (!matches) {
    return {
      replay_status: "REPLAY_DIVERGENCE",
      semantic_authority: "LOCAL_REPLAY",
      witness_status: "NOT_CHECKED",
      policy_hash_match,
      input_hash_match,
      interpreter_hash_match,
      replay_divergence: true,
      original_result: receipt.result,
      replayed_result: replayed.result,
      original_refusal_code: receipt.refusal_code,
      replayed_refusal_code: replayed.refusal_code,
      failure_reason: "VERDICT_MISMATCH"
    };
  }

  return {
    replay_status: receipt.result === "REFUSAL" ? "REFUSAL_CONFIRMED" : "VALID_REPLAY",
    semantic_authority: "LOCAL_REPLAY",
    witness_status: "NOT_CHECKED",
    policy_hash_match,
    input_hash_match,
    interpreter_hash_match,
    replay_divergence: false,
    original_result: receipt.result,
    replayed_result: replayed.result,
    original_refusal_code: receipt.refusal_code,
    replayed_refusal_code: replayed.refusal_code,
    failure_reason: null
  };
}
