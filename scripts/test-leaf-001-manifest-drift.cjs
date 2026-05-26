const fs = require("fs");
const crypto = require("crypto");

const path = "receipts/budget-forecast-001/receipt_manifest.json";
const EXPECTED = "a8b953ae26aa1bbf7d58538190224f751f9a08ea7da14491ebfd5f73b3197383";

const actual = crypto
  .createHash("sha256")
  .update(fs.readFileSync(path))
  .digest("hex");

if (actual !== EXPECTED) {
  console.error("CRITICAL: LEAF 001 MANIFEST DRIFT DETECTED");
  console.error({ expected: EXPECTED, actual });
  process.exit(1);
}

console.log("PASS: Leaf 001 manifest byte integrity verified");
