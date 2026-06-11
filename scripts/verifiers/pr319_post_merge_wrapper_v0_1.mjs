#!/usr/bin/env node
// SPDX-License-Identifier: MIT
// PR319 Post-Merge Cross-Round Verifier Wrapper v0.1

import fs from "fs";
import crypto from "crypto";

const INPUT = ".receipt/l3/post_merge_pr319_v0_1.json";
const OUTPUT = "logs/cross_round_verifier_pr319_v0_1.json";

const EXPECTED = {
  protocol: "L3_POST_MERGE_ANCHOR_RECEIPT_V0_1",
  operator: "jaywisdom.base.eth",
  repo: "jsonwisdom/AL",
  pr: "jsonwisdom/AL #319",
  merge_commit_sha: "95dafa1259828313c3a938f65d8a569943f51504",
  source_head_sha: "c2876f0be60a576e8c1cf51cfb6f3e25b2abbdc3",
  changed_files: 1,
  commits: 1,
  merge_timestamp: "2026-06-11T00:11:49Z",
  atomicity: true,
  topology: "clean",
  merkle_branch: "slim",
  inherited_forest: "none",
  replay_chain_continuity: true,
  membrane: "HOLDS",
  no_fake_green: true,
  authority: false,
  engine_status: "ALIGNED",
  next_gate: "CROSS_ROUND_VERIFIER_RUN",
  anchor_slot: ".receipt/l3/post_merge_pr319_v0_1.json"
};

function canonicalJson(value) {
  if (Array.isArray(value)) {
    return "[" + value.map(canonicalJson).join(",") + "]";
  }
  if (value && typeof value === "object") {
    return (
      "{" +
      Object.keys(value)
        .sort()
        .map((key) => JSON.stringify(key) + ":" + canonicalJson(value[key]))
        .join(",") +
      "}"
    );
  }
  return JSON.stringify(value);
}

function sha256Hex(value) {
  return "0x" + crypto.createHash("sha256").update(canonicalJson(value)).digest("hex");
}

function sha3BridgeHashHex(value) {
  return "0x" + crypto.createHash("sha3-256").update(canonicalJson(value)).digest("hex");
}

function checkEqual(anchor, key, expected) {
  const actual = anchor[key];
  return {
    field: key,
    expected,
    actual,
    passed: actual === expected
  };
}

function checkArray(anchor, key, expected) {
  const actual = anchor[key];
  const passed = Array.isArray(actual) &&
    actual.length === expected.length &&
    expected.every((value, index) => actual[index] === value);
  return {
    field: key,
    expected,
    actual,
    passed
  };
}

function checkLineage(anchor) {
  const expected = {
    pr_315: "oversized_surface",
    pr_318: "topology_lesson",
    pr_319: "merged_atomic_alignment_surface"
  };
  const actual = anchor.lineage;
  return {
    field: "lineage",
    expected,
    actual,
    passed: canonicalJson(actual) === canonicalJson(expected)
  };
}

function main() {
  const anchor = JSON.parse(fs.readFileSync(INPUT, "utf8"));

  const checks = [
    ...Object.entries(EXPECTED).map(([key, expected]) => checkEqual(anchor, key, expected)),
    checkLineage(anchor),
    checkArray(anchor, "compounding_basis", ["legibility", "replayability"])
  ];

  const allPassed = checks.every((check) => check.passed);

  const output = {
    verifier: "PR319_POST_MERGE_CROSS_ROUND_VERIFIER_WRAPPER_V0_1",
    input_anchor: INPUT,
    output_log: OUTPUT,
    result: allPassed ? "PASS" : "FAIL",
    checked_at: new Date().toISOString(),
    checks,
    replay_summary: {
      pr_315: anchor.lineage?.pr_315,
      pr_318: anchor.lineage?.pr_318,
      pr_319: anchor.lineage?.pr_319,
      atomicity: anchor.atomicity,
      topology: anchor.topology,
      merkle_branch: anchor.merkle_branch,
      inherited_forest: anchor.inherited_forest,
      membrane: anchor.membrane,
      no_fake_green: anchor.no_fake_green,
      authority: anchor.authority
    }
  };

  output.sha256_replay_hash = sha256Hex(output);
  output.sha3_256_bridge_hash = sha3BridgeHashHex(output);
  output.bridge_hash_domain = "SHA3_256_NOT_ETHEREUM_KECCAK256";

  fs.mkdirSync("logs", { recursive: true });
  fs.writeFileSync(OUTPUT, JSON.stringify(output, null, 2) + "\n");
  console.log(JSON.stringify(output, null, 2));

  if (!allPassed) {
    process.exit(1);
  }
}

main();
