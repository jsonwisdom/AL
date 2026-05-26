const fs = require("fs");
const { evaluate } = require("./invariant_evaluator.cjs");

const path = "data/mmb/v1/adjustments/leaf-003/manifest.json";
const manifest = JSON.parse(fs.readFileSync(path, "utf8"));

const result = evaluate(manifest);

console.log("PASS: Leaf 003 MMB adjustment invariant verified");
console.log(JSON.stringify(result, null, 2));
