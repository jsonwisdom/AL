const fs = require("fs");
const crypto = require("crypto");

const canonicalPath = "data/budget-forecast-001/canonical.json";
const manifestPath = "receipts/budget-forecast-001/receipt_manifest.json";
const verifierPath = "scripts/verify-budget-forecast-001.cjs";

function readJson(path) {
  return JSON.parse(fs.readFileSync(path, "utf8"));
}

function sha256HexUtf8(s) {
  return crypto.createHash("sha256").update(Buffer.from(s, "utf8")).digest("hex");
}

const canonical = fs.readFileSync(canonicalPath, "utf8");
const manifest = readJson(manifestPath);
const verifier = fs.readFileSync(verifierPath, "utf8");

const canonicalHash = sha256HexUtf8(canonical);

const expectedMatch = verifier.match(/const EXPECTED_SHA256 = "([a-fA-F0-9]{64})"/);
if (!expectedMatch) {
  console.error("FAIL: EXPECTED_SHA256 not found in verifier");
  process.exit(1);
}

const expected = expectedMatch[1];

const required = [
  "audit_id",
  "network",
  "git_commit",
  "git_tag",
  "schema_uid",
  "schema_tx_hash",
  "attestation_uid",
  "attestation_tx_hash",
  "canonical_json_sha256",
  "witness_role",
  "replay_authority",
  "private_key_terminal"
];

for (const key of required) {
  if (!(key in manifest)) {
    console.error(`FAIL: missing manifest field ${key}`);
    process.exit(1);
  }
}

if (manifest.private_key_terminal !== false) {
  console.error("FAIL: private_key_terminal must be false");
  process.exit(1);
}

if (manifest.canonical_json_sha256 !== canonicalHash) {
  console.error("FAIL: manifest hash does not match canonical.json");
  console.error({ manifest: manifest.canonical_json_sha256, actual: canonicalHash });
  process.exit(1);
}

if (manifest.canonical_json_sha256 !== expected) {
  console.error("FAIL: manifest hash does not match verifier EXPECTED_SHA256");
  console.error({ manifest: manifest.canonical_json_sha256, expected });
  process.exit(1);
}

console.log("PASS: receipt manifest, canonical object, and verifier agree");
process.exit(0);
