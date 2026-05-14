#!/usr/bin/env node
import { readFileSync } from "node:fs";
import { validateReceipt } from "./validator.js";
import { validateReceiptSchema, validateLineageSchema } from "./validator.js";

const [, , receiptPath, lineagePath] = process.argv;
if (!receiptPath || !lineagePath) {
  console.error("Usage: replay <receipt.json> <lineage.json>");
  process.exit(1);
}

let receipt: unknown;
let lineage: unknown;

try {
  receipt = JSON.parse(readFileSync(receiptPath, "utf8"));
  lineage = JSON.parse(readFileSync(lineagePath, "utf8"));
} catch (e) {
  console.error("Parse failed:", (e as Error).message);
  process.exit(1);
}

const receiptSchemaResult = validateReceiptSchema(receipt);
if (!receiptSchemaResult.valid) {
  console.error("Schema validation failed for receipt:");
  console.error(JSON.stringify(receiptSchemaResult.errors, null, 2));
  process.exit(1);
}

const lineageSchemaResult = validateLineageSchema(lineage);
if (!lineageSchemaResult.valid) {
  console.error("Schema validation failed for lineage:");
  console.error(JSON.stringify(lineageSchemaResult.errors, null, 2));
  process.exit(1);
}

const result = validateReceipt(receipt as any, lineage as any);
console.log(JSON.stringify(result, null, 2));

if (result.verdict === "MATCH") process.exit(0);
if (result.verdict === "DIVERGENCE") process.exit(2);
process.exit(4);
