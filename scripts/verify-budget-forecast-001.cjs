const fs = require("fs");
const crypto = require("crypto");

const TARGET = "data/budget-forecast-001/canonical.json";
const EXPECTED_SHA256 = "ebd0028aa9878116bc6b6cdf49b645153582e13dfea95fc8d23ad90a8ef2dccb";

if (!fs.existsSync(TARGET)) {
  console.error("FAIL: missing target:", TARGET);
  process.exit(1);
}

const bytes = fs.readFileSync(TARGET);
const actual = crypto.createHash("sha256").update(bytes).digest("hex");

console.log("target:", TARGET);
console.log("sha256:", actual);

if (EXPECTED_SHA256 === "REPLACE_AFTER_FIRST_HASH") {
  console.log("BOOTSTRAP MODE: copy this sha256 into EXPECTED_SHA256");
  process.exit(0);
}

if (actual !== EXPECTED_SHA256) {
  console.error("FAIL: sha256 mismatch");
  process.exit(1);
}

console.log("PASS: budget forecast canonical hash verified");
process.exit(0);
