import { canonicalHash, assertCanonicalHash } from "./hash.js";

export class PolicyError extends Error {
  readonly code: PolicyFailureCode;

  constructor(code: PolicyFailureCode, message?: string) {
    super(message ?? code);
    this.name = "PolicyError";
    this.code = code;
  }
}

export const REFUSAL_CODES = [
  "SPEND_LIMIT_EXCEEDED",
  "ACTION_NOT_ALLOWED",
  "CONTRACT_NOT_ALLOWED",
  "DELEGATION_EXPIRED",
  "RATE_LIMIT_EXCEEDED",
  "SIGNATURE_INVALID",
  "POLICY_UNAVAILABLE",
  "ESCALATION_REQUIRED",
  "UNKNOWN_REFUSAL"
] as const;

export type RefusalCode = (typeof REFUSAL_CODES)[number];

export type PolicyFailureCode =
  | "POLICY_SCHEMA_VIOLATION"
  | "POLICY_VERSION_UNSUPPORTED"
  | "POLICY_HASH_MISMATCH"
  | "UNKNOWN_REFUSAL_CODE"
  | "CONFLICTING_ACTION_RULES"
  | "LIMIT_FORMAT_INVALID";

export interface PolicyV1 {
  version: "policy.v1";
  policy_id: string;
  required_inputs: string[];
  allowed_actions: string[];
  blocked_actions: string[];
  limits: {
    transfer_usdc_day: string;
  };
  refusal_codes: RefusalCode[];
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function assertString(value: unknown, code: PolicyFailureCode): string {
  if (typeof value !== "string" || value.length === 0) {
    throw new PolicyError(code);
  }
  return value;
}

function assertStringArray(value: unknown, code: PolicyFailureCode): string[] {
  if (!Array.isArray(value)) {
    throw new PolicyError(code);
  }

  const out = value.map((item) => assertString(item, code));
  const unique = new Set(out);

  if (unique.size !== out.length) {
    throw new PolicyError(code, `${code}: duplicate string array entry`);
  }

  return out;
}

function assertRefusalCodes(value: unknown): RefusalCode[] {
  const items = assertStringArray(value, "POLICY_SCHEMA_VIOLATION");
  const allowed = new Set<string>(REFUSAL_CODES);

  for (const item of items) {
    if (!allowed.has(item)) {
      throw new PolicyError("UNKNOWN_REFUSAL_CODE", item);
    }
  }

  if (items.length !== REFUSAL_CODES.length) {
    throw new PolicyError("UNKNOWN_REFUSAL_CODE", "refusal enum incomplete");
  }

  for (const code of REFUSAL_CODES) {
    if (!items.includes(code)) {
      throw new PolicyError("UNKNOWN_REFUSAL_CODE", `missing ${code}`);
    }
  }

  return items as RefusalCode[];
}

function assertDecimalString(value: unknown): string {
  const text = assertString(value, "LIMIT_FORMAT_INVALID");

  if (!/^[0-9]+$/.test(text)) {
    throw new PolicyError("LIMIT_FORMAT_INVALID", text);
  }

  return text;
}

function assertNoActionConflict(allowed: string[], blocked: string[]): void {
  const blockedSet = new Set(blocked);

  for (const action of allowed) {
    if (blockedSet.has(action)) {
      throw new PolicyError("CONFLICTING_ACTION_RULES", action);
    }
  }
}

export function validatePolicy(raw: unknown): PolicyV1 {
  if (!isRecord(raw)) {
    throw new PolicyError("POLICY_SCHEMA_VIOLATION", "policy must be an object");
  }

  if (raw.version !== "policy.v1") {
    throw new PolicyError("POLICY_VERSION_UNSUPPORTED");
  }

  const policy_id = assertString(raw.policy_id, "POLICY_SCHEMA_VIOLATION");
  const required_inputs = assertStringArray(raw.required_inputs, "POLICY_SCHEMA_VIOLATION");
  const allowed_actions = assertStringArray(raw.allowed_actions, "POLICY_SCHEMA_VIOLATION");
  const blocked_actions = assertStringArray(raw.blocked_actions, "POLICY_SCHEMA_VIOLATION");

  if (!isRecord(raw.limits)) {
    throw new PolicyError("POLICY_SCHEMA_VIOLATION", "limits must be an object");
  }

  const transfer_usdc_day = assertDecimalString(raw.limits.transfer_usdc_day);
  const refusal_codes = assertRefusalCodes(raw.refusal_codes);

  assertNoActionConflict(allowed_actions, blocked_actions);

  return {
    version: "policy.v1",
    policy_id,
    required_inputs,
    allowed_actions,
    blocked_actions,
    limits: {
      transfer_usdc_day
    },
    refusal_codes
  };
}

export function loadPolicy(raw: unknown): PolicyV1 {
  return validatePolicy(raw);
}

export function assertPolicyVersion(policy: PolicyV1, expected = "policy.v1"): void {
  if (policy.version !== expected) {
    throw new PolicyError("POLICY_VERSION_UNSUPPORTED", `expected=${expected} actual=${policy.version}`);
  }
}

export function assertRefusalCode(policy: PolicyV1, code: string): asserts code is RefusalCode {
  if (!policy.refusal_codes.includes(code as RefusalCode)) {
    throw new PolicyError("UNKNOWN_REFUSAL_CODE", code);
  }
}

export function policyHash(policy: PolicyV1): string {
  return canonicalHash(policy);
}

export function assertPolicyHash(raw: unknown, expectedHash: string): PolicyV1 {
  const policy = loadPolicy(raw);

  try {
    assertCanonicalHash(policy, expectedHash);
  } catch (error) {
    throw new PolicyError("POLICY_HASH_MISMATCH", error instanceof Error ? error.message : undefined);
  }

  return policy;
}
