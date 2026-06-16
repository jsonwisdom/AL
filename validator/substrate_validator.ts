// validator/substrate_validator.ts
// SUBSTRATE_VALIDATOR_V0_1
// MODE: CANON (no lax mode, no discretionary override)

import { createHash } from "crypto";

type InvariantConfig = {
  description: string;
  required: boolean;
  value: boolean | null;
  reject_if_false: boolean;
};

type PropertiesConfig = Record<string, { type: string; description: string }>;

type WarningRule = {
  condition: string;
  level: "warn";
  message: string;
};

type ValidatorSchema = {
  $schema: string;
  principles: {
    id: string;
    principle: string;
    meaning: string;
    severity: "fatal" | "warning";
  }[];
  sovereign_root: string;
  operational_membrane: string;
  required_invariants: Record<string, InvariantConfig>;
  properties: PropertiesConfig;
  warnings: Record<string, WarningRule>;
  fatal_conditions: string[];
  verdicts: {
    ADMISSIBLE: { description: string };
    ADMISSIBLE_WITH_WARNINGS: { description: string };
    REJECTED_PLATFORM_CAPTURE_RISK: { description: string };
  };
  evaluation_logic: {
    steps: string[];
  };
  doctrine: {
    hard_gate: string;
    anti_capture: string;
  };
};

type SubstrateDocument = {
  $schema: string;
  substrate: string;
  version: string;
  properties: Record<string, boolean>;
  required_invariants: Record<string, InvariantConfig>;
  evaluation?: {
    warnings_triggered: string[];
    fatal_conditions_triggered: string[];
    verdict: string;
  };
  doctrine?: {
    anti_capture: string;
  };
};

type InvariantTraceEntry = {
  name: string;
  required: boolean;
  value: boolean | null;
  reject_if_false: boolean;
  failed: boolean;
};

type RefusalWitness = {
  reason: string;
  fatal_conditions_triggered: string[];
  invariants_failed: string[];
};

type SubstrateValidationReceipt = {
  substrate: string;
  version: string;
  timestamp: string;
  input_hash: string;
  fatal_conditions_triggered: string[];
  warnings_triggered: string[];
  invariant_trace: InvariantTraceEntry[];
  verdict: "ADMISSIBLE" | "ADMISSIBLE_WITH_WARNINGS" | "REJECTED_PLATFORM_CAPTURE_RISK";
  refusal_witness: RefusalWitness | null;
  doctrine_applied: {
    hard_gate: string;
    anti_capture: string;
  };
};

// Cryptographic hash for receipt binding
function sha256(input: string): string {
  return createHash("sha256").update(input, "utf8").digest("hex");
}

// Evaluate conditions like:
// "properties.MIGRATABLE == false"
// "required_invariants.receipts_portable.value == false"
function evaluateCondition(condition: string, ctx: any): boolean {
  const parts = condition.split("==").map((p) => p.trim());
  if (parts.length !== 2) return false;

  const left = parts[0];
  const rightRaw = parts[1];

  const path = left.split(".");
  let current: any = ctx;
  for (const segment of path) {
    if (segment in current) {
      current = current[segment];
    } else {
      return false;
    }
  }

  let right: any;
  if (rightRaw === "true") right = true;
  else if (rightRaw === "false") right = false;
  else right = rightRaw;

  return current === right;
}

// CANON MODE validator: no lax path, no discretionary override
export function validateSubstrateCanon(
  schema: ValidatorSchema,
  substrateDoc: SubstrateDocument
): SubstrateValidationReceipt {
  const ctx = {
    properties: substrateDoc.properties,
    required_invariants: substrateDoc.required_invariants
  };

  const invariant_trace: InvariantTraceEntry[] = [];
  const invariants_failed: string[] = [];
  const fatal_conditions_triggered: string[] = [];
  const warnings_triggered: string[] = [];

  // 1. Evaluate required invariants (hard gate)
  for (const [name, inv] of Object.entries(substrateDoc.required_invariants)) {
    const failed = inv.reject_if_false && inv.value === false;
    invariant_trace.push({
      name,
      required: inv.required,
      value: inv.value,
      reject_if_false: inv.reject_if_false,
      failed
    });
    if (failed) {
      invariants_failed.push(name);
      fatal_conditions_triggered.push(`required_invariants.${name}.value == false`);
    }
  }

  // 2. Evaluate fatal conditions from schema
  for (const cond of schema.fatal_conditions) {
    if (evaluateCondition(cond, ctx)) {
      fatal_conditions_triggered.push(cond);
    }
  }

  // 3. Evaluate warnings
  for (const [warnName, warnRule] of Object.entries(schema.warnings)) {
    if (evaluateCondition(warnRule.condition, ctx)) {
      warnings_triggered.push(warnName);
    }
  }

  // 4. Verdict logic (CANON MODE)
  let verdict: SubstrateValidationReceipt["verdict"];
  let refusal_witness: RefusalWitness | null = null;

  if (fatal_conditions_triggered.length > 0 || invariants_failed.length > 0) {
    verdict = "REJECTED_PLATFORM_CAPTURE_RISK";
    refusal_witness = {
      reason:
        "One or more fatal conditions or required invariants failed. Substrate represents platform capture risk.",
      fatal_conditions_triggered,
      invariants_failed
    };
  } else if (warnings_triggered.length > 0) {
    verdict = "ADMISSIBLE_WITH_WARNINGS";
  } else {
    verdict = "ADMISSIBLE";
  }

  const timestamp = new Date().toISOString();
  const input_hash = sha256(JSON.stringify(substrateDoc));

  const receipt: SubstrateValidationReceipt = {
    substrate: substrateDoc.substrate,
    version: substrateDoc.version,
    timestamp,
    input_hash,
    fatal_conditions_triggered,
    warnings_triggered,
    invariant_trace,
    verdict,
    refusal_witness,
    doctrine_applied: {
      hard_gate: schema.doctrine.hard_gate,
      anti_capture: schema.doctrine.anti_capture
    }
  };

  return receipt;
}
