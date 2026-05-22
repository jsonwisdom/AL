#!/usr/bin/env node

const verdict = {
  verdict: "NEEDS_SOURCE",
  script: "verify-receipt.js",
  checked: [
    "git_commit_existence",
    "schema_canonicalization_rules"
  ],
  missing_sources: [
    "canonicalization_algorithm_spec",
    "receipt_schema_target",
    "comparison_tolerance_boundaries"
  ],
  promotion_status: "STUB_LOCKED",
  ghost_anchor_risk: false
};

console.log(JSON.stringify(verdict, null, 2));
