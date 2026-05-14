import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { createRequire } from "node:module";
import Ajv, { JSONSchemaType } from "ajv";
import addFormats from "ajv-formats";

const require = createRequire(import.meta.url);

const schemaPath = resolve(
  process.cwd(),
  "reports/baselines/schema/baseline_receipt_v1.json"
);
const schema = require(schemaPath);

export interface NetworkEvent {
  timestamp: number;
  method: string;
  resourceType: string;
  url: string;
  tier: number;
}

export interface BaselineMetrics {
  tier3PlusCount: number;
  eventCount: number;
}

export interface BaselineReceipt {
  schemaVersion: "baseline_receipt_v1";
  receiptType: "calibration" | "capture" | "curriculum";
  harnessVersion: string;
  commit: string;
  generatedAt: string;
  networkEvents: NetworkEvent[];
  metrics: BaselineMetrics;
  receiptHash: string;
}

const ajv = new Ajv({ allErrors: true, strict: true });
addFormats(ajv);

const validate = ajv.compile<BaselineReceipt>(
  schema as JSONSchemaType<BaselineReceipt>
);

export function loadBaseline(path: string): BaselineReceipt {
  const absolute = resolve(process.cwd(), path);

  let raw: string;
  try {
    raw = readFileSync(absolute, "utf8");
  } catch (err) {
    throw new Error(`Failed to read baseline at ${absolute}: ${err}`);
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch (err) {
    throw new Error(`Invalid JSON in baseline at ${absolute}: ${err}`);
  }

  const valid = validate(parsed);
  if (!valid) {
    const errors = ajv.errorsText(validate.errors, { separator: "\n" });
    throw new Error(
      `Baseline at ${absolute} does not match baseline_receipt_v1 schema:\n${errors}`
    );
  }

  return parsed;
}
