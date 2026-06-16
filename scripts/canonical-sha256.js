#!/usr/bin/env node
const fs = require("fs");
const crypto = require("crypto");

function sortKeys(value) {
  if (Array.isArray(value)) return value.map(sortKeys);
  if (value && typeof value === "object" && value.constructor === Object) {
    return Object.keys(value).sort().reduce((out, key) => {
      out[key] = sortKeys(value[key]);
      return out;
    }, {});
  }
  return value;
}

function canonicalizeJsonFile(path) {
  const raw = fs.readFileSync(path, "utf8")
    .normalize("NFC")
    .replace(/\r\n/g, "\n")
    .replace(/\r/g, "\n")
    .trim();

  const parsed = JSON.parse(raw);
  return JSON.stringify(sortKeys(parsed)) + "\n";
}

const file = process.argv[2];
if (!file) {
  console.error("usage: node scripts/canonical-sha256.js <file.json>");
  process.exit(1);
}

const canonical = canonicalizeJsonFile(file);
const hash = crypto.createHash("sha256").update(canonical, "utf8").digest("hex");
console.log(hash);
