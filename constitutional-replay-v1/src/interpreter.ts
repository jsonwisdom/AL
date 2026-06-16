import { PolicyV1, RefusalCode, assertRefusalCode } from "./policy.js";

export class InterpreterError extends Error {
  readonly code: InterpreterFailureCode;

  constructor(code: InterpreterFailureCode, message?: string) {
    super(message ?? code);
    this.name = "InterpreterError";
    this.code = code;
  }
}

export type InterpreterFailureCode =
  | "INPUT_SCHEMA_VIOLATION"
  | "AMOUNT_FORMAT_INVALID"
  | "UNHANDLED_REFUSAL"
  | "UNKNOWN_ACTION";

export type InterpreterResult =
  | {
      result: "SUCCESS";
      refusal_code: null;
    }
  | {
      result: "REFUSAL";
      refusal_code: RefusalCode;
    };

export interface PolicyInput {
  action: string;
  amount: string;
  recipient: string;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isDecimalString(value: string): boolean {
  return /^[0-9]+$/.test(value);
}

function amountGreaterThan(left: string, right: string): boolean {
  const normalizedLeft = left.replace(/^0+/, "") || "0";
  const normalizedRight = right.replace(/^0+/, "") || "0";

  if (normalizedLeft.length !== normalizedRight.length) {
    return normalizedLeft.length > normalizedRight.length;
  }

  return normalizedLeft > normalizedRight;
}

function refusal(policy: PolicyV1, code: RefusalCode): InterpreterResult {
  assertRefusalCode(policy, code);
  return {
    result: "REFUSAL",
    refusal_code: code
  };
}

function parseInput(raw: unknown): PolicyInput | null {
  if (!isRecord(raw)) {
    return null;
  }

  if (
    typeof raw.action !== "string" ||
    typeof raw.amount !== "string" ||
    typeof raw.recipient !== "string"
  ) {
    return null;
  }

  if (raw.action.length === 0 || raw.amount.length === 0 || raw.recipient.length === 0) {
    return null;
  }

  return {
    action: raw.action,
    amount: raw.amount,
    recipient: raw.recipient
  };
}

export function interpretPolicy(policy: PolicyV1, rawInput: unknown): InterpreterResult {
  const input = parseInput(rawInput);

  if (input === null) {
    return refusal(policy, "UNKNOWN_REFUSAL");
  }

  if (!isDecimalString(input.amount)) {
    return refusal(policy, "UNKNOWN_REFUSAL");
  }

  if (policy.blocked_actions.includes(input.action)) {
    return refusal(policy, "ACTION_NOT_ALLOWED");
  }

  if (!policy.allowed_actions.includes(input.action)) {
    return refusal(policy, "ACTION_NOT_ALLOWED");
  }

  if (
    input.action === "transfer_usdc" &&
    amountGreaterThan(input.amount, policy.limits.transfer_usdc_day)
  ) {
    return refusal(policy, "SPEND_LIMIT_EXCEEDED");
  }

  return {
    result: "SUCCESS",
    refusal_code: null
  };
}
