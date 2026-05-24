import { canonicalHash } from "./hash.js";
import { PolicyV1, RefusalCode, policyHash } from "./policy.js";
import { InterpreterResult } from "./interpreter.js";

export class ReceiptError extends Error {
  readonly code: ReceiptFailureCode;

  constructor(code: ReceiptFailureCode, message?: string) {
    super(message ?? code);
    this.name = "ReceiptError";
    this.code = code;
  }
}

export type ReceiptFailureCode =
  | "MISSING_BINDING"
  | "INVALID_RECEIPT_SCHEMA"
  | "VERDICT_BINDING_MISMATCH";

export interface ReceiptV1 {
  receipt_version: "receipt.v1";
  policy_hash: string;
  policy_version: "policy.v1";
  interpreter_hash: string;
  replay_engine_version: "replay.v1";
  action: string;
  input_hash: string;
  context_hash: string;
  result: "SUCCESS" | "REFUSAL";
  refusal_code: RefusalCode | null;
}

export interface EmitReceiptArgs {
  policy: PolicyV1;
  interpreter_hash: string;
  input: unknown;
  action: string;
  verdict: InterpreterResult;
  context?: unknown;
}

export const REPLAY_ENGINE_VERSION = "replay.v1" as const;
export const RECEIPT_VERSION = "receipt.v1" as const;

export function emitReceipt(args: EmitReceiptArgs): ReceiptV1 {
  return {
    receipt_version: RECEIPT_VERSION,
    policy_hash: policyHash(args.policy),
    policy_version: args.policy.version,
    interpreter_hash: args.interpreter_hash,
    replay_engine_version: REPLAY_ENGINE_VERSION,
    action: args.action,
    input_hash: canonicalHash(args.input),
    context_hash: canonicalHash(args.context ?? {}),
    result: args.verdict.result,
    refusal_code: args.verdict.refusal_code
  };
}

export function emitRefusal(args: Omit<EmitReceiptArgs, "verdict"> & { refusal_code: RefusalCode }): ReceiptV1 {
  return emitReceipt({
    ...args,
    verdict: {
      result: "REFUSAL",
      refusal_code: args.refusal_code
    }
  });
}

export function receiptHash(receipt: ReceiptV1): string {
  return canonicalHash(receipt);
}

function assertNonEmptyStringField(
  r: Record<string, unknown>,
  field: string
): string {
  const value = r[field];

  if (typeof value !== "string" || value.length === 0) {
    throw new ReceiptError("INVALID_RECEIPT_SCHEMA", field);
  }

  return value;
}

function assertRefusalCodeValue(value: unknown): RefusalCode | null {
  if (value === null) {
    return null;
  }

  if (typeof value !== "string" || value.length === 0) {
    throw new ReceiptError("VERDICT_BINDING_MISMATCH", "invalid refusal_code");
  }

  return value as RefusalCode;
}

export function validateReceiptEnvelope(receipt: unknown): ReceiptV1 {
  if (typeof receipt !== "object" || receipt === null || Array.isArray(receipt)) {
    throw new ReceiptError("INVALID_RECEIPT_SCHEMA", "receipt must be an object");
  }

  const r = receipt as Record<string, unknown>;

  const required = [
    "receipt_version",
    "policy_hash",
    "policy_version",
    "interpreter_hash",
    "replay_engine_version",
    "action",
    "input_hash",
    "context_hash",
    "result",
    "refusal_code"
  ];

  for (const field of required) {
    if (!(field in r)) {
      throw new ReceiptError("MISSING_BINDING", field);
    }
  }

  if (r.receipt_version !== RECEIPT_VERSION) {
    throw new ReceiptError("INVALID_RECEIPT_SCHEMA", "invalid receipt_version");
  }

  if (r.policy_version !== "policy.v1") {
    throw new ReceiptError("INVALID_RECEIPT_SCHEMA", "invalid policy_version");
  }

  if (r.replay_engine_version !== REPLAY_ENGINE_VERSION) {
    throw new ReceiptError("INVALID_RECEIPT_SCHEMA", "invalid replay_engine_version");
  }

  if (r.result !== "SUCCESS" && r.result !== "REFUSAL") {
    throw new ReceiptError("INVALID_RECEIPT_SCHEMA", "invalid result");
  }

  const result = r.result;
  const refusal_code = assertRefusalCodeValue(r.refusal_code);

  if (result === "SUCCESS" && refusal_code !== null) {
    throw new ReceiptError("VERDICT_BINDING_MISMATCH", "success receipt cannot carry refusal_code");
  }

  if (result === "REFUSAL" && refusal_code === null) {
    throw new ReceiptError("VERDICT_BINDING_MISMATCH", "refusal receipt requires refusal_code");
  }

  const policy_hash = assertNonEmptyStringField(r, "policy_hash");
  const interpreter_hash = assertNonEmptyStringField(r, "interpreter_hash");
  const input_hash = assertNonEmptyStringField(r, "input_hash");
  const context_hash = assertNonEmptyStringField(r, "context_hash");
  const action = assertNonEmptyStringField(r, "action");

  return {
    receipt_version: RECEIPT_VERSION,
    policy_hash,
    policy_version: "policy.v1",
    interpreter_hash,
    replay_engine_version: REPLAY_ENGINE_VERSION,
    action,
    input_hash,
    context_hash,
    result,
    refusal_code
  };
}
