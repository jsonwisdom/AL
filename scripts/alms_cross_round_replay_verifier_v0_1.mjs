#!/usr/bin/env node
// SPDX-License-Identifier: MIT
// ALMS Cross-Round Replay Verifier v0.1

import fs from "fs";
import crypto from "crypto";

const INPUT = "vectors/cross_round_invariant_vectors_v0_1.json";
const OUTPUT = "vectors/cross_round_evaluation_result_v0_1.json";
const ZERO_BYTES32 = "0x0000000000000000000000000000000000000000000000000000000000000000";

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

function bridgeHashHex(value) {
  // Node's built-in crypto does not universally expose Ethereum keccak256.
  // Until ethers/js-sha3 is added, emit an explicitly domain-labeled bridge hash
  // derived from SHA3-256 so it can never be confused with Solidity keccak256.
  return "0x" + crypto.createHash("sha3-256").update(canonicalJson(value)).digest("hex");
}

function isNonZeroBytes32(value) {
  return typeof value === "string" && value.startsWith("0x") && value.length > 2 && value !== ZERO_BYTES32;
}

function evaluateHistory(history) {
  if (!history || typeof history !== "object") {
    return "INVALID_HISTORY";
  }

  if (history.canonicalSchemaUID !== history.submittedSchemaUID) {
    return "C5_SCHEMA_UID_MISMATCH";
  }

  if (
    history.previousTaxNoticeStructureHash !== ZERO_BYTES32 &&
    history.currentTaxNoticeStructureHash !== ZERO_BYTES32 &&
    history.previousTaxNoticeStructureHash !== history.currentTaxNoticeStructureHash &&
    history.schemaVersionBumped === false
  ) {
    return "C4_TAX_NOTICE_DRIFT";
  }

  if (Number(history.unconstitutionalRounds24m || 0) >= 3) {
    return "C3_SCHEMA_ROTATION_REQUIRED";
  }

  if (Number(history.unconstitutionalRounds12m || 0) >= 2) {
    return "C2_IDENTITY_FREEZE_REQUIRED";
  }

  if (
    Number(history.unconstitutionalRounds12m || 0) >= 1 &&
    Number(history.lastUnconstitutionalTimestamp || 0) > 0 &&
    Number(history.explanationTimestamp || 0) === 0
  ) {
    return "C1_UNEXPLAINED_UNCONSTITUTIONAL";
  }

  return "NONE";
}

function evaluateVector(vector) {
  const violation = evaluateHistory(vector.history);
  const expectedViolation = vector.expected_violation ?? "NONE";

  const payload = {
    vector_id: vector.vector_id,
    history: vector.history,
    violation,
    expected_violation: expectedViolation
  };

  const sha256ReplayHash = sha256Hex(payload);
  const sha3BridgeHash = bridgeHashHex(payload);

  return {
    ...payload,
    passed: violation === expectedViolation,
    sha256_replay_hash: sha256ReplayHash,
    sha3_256_bridge_hash: sha3BridgeHash,
    bridge_hash_domain: "SHA3_256_NOT_ETHEREUM_KECCAK256"
  };
}

function main() {
  const input = JSON.parse(fs.readFileSync(INPUT, "utf8"));
  const results = input.vectors.map(evaluateVector);
  const allPassed = results.every((result) => result.passed);

  const replayPayload = {
    verifier: "ALMS_CROSS_ROUND_REPLAY_VERIFIER_V0_1",
    schema_name: input.schema_name,
    schema_version: input.schema_version,
    operator_root: input.operator_root,
    operator_alias: input.operator_alias,
    project: input.project,
    results
  };

  const sha256ReplayHash = sha256Hex(replayPayload);
  const sha3BridgeHash = bridgeHashHex(replayPayload);

  const output = {
    ...replayPayload,
    result: allPassed ? "PASS" : "FAIL",
    sha256_replay_hash: sha256ReplayHash,
    sha3_256_bridge_hash: sha3BridgeHash,
    bridge_hash_domain: "SHA3_256_NOT_ETHEREUM_KECCAK256",
    eas_attestation_payload: {
      schema_uid: input.schema_uid ?? "<REPLACE_AFTER_REGISTRATION>",
      operator_root: input.operator_root,
      operator_alias: input.operator_alias,
      project: input.project,
      sha256_replay_hash: sha256ReplayHash,
      sha3_256_bridge_hash: sha3BridgeHash,
      bridge_hash_domain: "SHA3_256_NOT_ETHEREUM_KECCAK256",
      verifier: "ALMS_CROSS_ROUND_REPLAY_VERIFIER_V0_1",
      result: allPassed ? "PASS" : "FAIL"
    }
  };

  fs.writeFileSync(OUTPUT, JSON.stringify(output, null, 2) + "\n");
  console.log(JSON.stringify(output, null, 2));

  if (!allPassed) {
    process.exit(1);
  }
}

main();
