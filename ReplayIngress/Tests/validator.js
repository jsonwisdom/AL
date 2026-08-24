import fs from "node:fs";
import Ajv from "ajv";

const schema = JSON.parse(
  fs.readFileSync(new URL("../ReplayIngressSpec_V1.json", import.meta.url), "utf8")
);

const ajv = new Ajv({ allErrors: true, strict: false });

ajv.addFormat("date-time", {
  type: "string",
  validate(value) {
    return (
      /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/.test(value) &&
      !Number.isNaN(Date.parse(value))
    );
  }
});

export const validateReplayIngress = ajv.compile(schema);

export function basePacket(overrides = {}) {
  return {
    replay_result: "REPLAY_MATCH",
    receipt_id: "receipt-001",
    parent_receipt_ids: [],
    replay_hash: "sha256:example",
    procedure_id: "procedure-001",
    timestamp: "2026-08-24T13:14:00Z",
    authority_created: false,
    acceptance_created: false,
    correctness_proved: false,
    ...overrides
  };
}
