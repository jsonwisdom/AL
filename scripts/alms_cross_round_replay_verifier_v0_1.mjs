#!/usr/bin/env node
// SPDX-License-Identifier: MIT
// ALMS Cross-Round Replay Verifier v0.1

import fs from "fs";
import crypto from "crypto";

const INPUT = "vectors/cross_round_invariant_vectors_v0_1.json";
const OUTPUT = "vectors/cross_round_evaluation_result_v0_1.json";

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

function evaluateVector(vector) {
  let expectedViolation = "NONE";

  switch (vector.invariant) {
    case "C1": {
      const round = vector.rounds?.[0];
      const explained = round?.explanation_attestation?.submitted === true;
      const timely = round?.explanation_attestation?.submitted_within_7_days === true;
      if (round?.final_state === "UNCONSTITUTIONAL" && !(explained && timely)) {
        expectedViolation = "UNEXPLAINED_UNCONSTITUTIONAL";
      }
      break;
    }
    case "C2": {
      const unconstitutionalCount = (vector.rounds || []).filter(
        (round) => round.final_state === "UNCONSTITUTIONAL"
      ).length;
      if (unconstitutionalCount >= 2) {
        expectedViolation = "IDENTITY_FREEZE_ACTIVATED";
      }
      break;
    }
    case "C3": {
      const unconstitutionalCount = (vector.rounds || []).filter(
        (round) => round.final_state === "UNCONSTITUTIONAL"
      ).length;
      if (unconstitutionalCount >= 3) {
        expectedViolation = "SCHEMA_DEPRECATION";
      }
      break;
    }
    case "C4": {
      const driftDetected = (vector.rounds || []).some(
        (round) => round.drift_detected === true
      );
      if (driftDetected) {
        expectedViolation = "TAX_NOTICE_DRIFT";
      }
      break;
    }
    case "C5": {
      if (vector.attestation?.mismatch === true) {
        expectedViolation = "SCHEMA_UID_MISMATCH";
      }
      break;
    }
    default:
      expectedViolation = "UNKNOWN_INVARIANT";
  }

  const actualResult = expectedViolation === "NONE" ? "PASS" : "FAIL";

  const result = {
    vector_id: vector.vector_id,
    invariant: vector.invariant,
    expected_result: vector.expected_result,
    actual_result: actualResult,
    matched_expected: actualResult === vector.expected_result,
    violation: expectedViolation,
    strike_type: vector.strike_type ?? null
  };

  return {
    ...result,
    sha256_replay_hash: sha256Hex(result)
  };
}

function main() {
  const input = JSON.parse(fs.readFileSync(INPUT, "utf8"));
  const results = input.vectors.map(evaluateVector);
  const allMatched = results.every((result) => result.matched_expected);

  const output = {
    verifier: "ALMS_CROSS_ROUND_REPLAY_VERIFIER_V0_1",
    schema_uid: input.schema_uid,
    operator_root: input.operator_root,
    operator_alias: input.operator_alias,
    project: input.project,
    result: allMatched ? "PASS" : "FAIL",
    results,
    sha256_replay_hash: sha256Hex(results),
    eas_attestation_payload: {
      schema_uid: input.schema_uid,
      operator_root: input.operator_root,
      operator_alias: input.operator_alias,
      project: input.project,
      sha256_replay_hash: sha256Hex(results),
      verifier: "ALMS_CROSS_ROUND_REPLAY_VERIFIER_V0_1",
      result: allMatched ? "PASS" : "FAIL"
    }
  };

  fs.writeFileSync(OUTPUT, JSON.stringify(output, null, 2) + "\n");
  console.log(JSON.stringify(output, null, 2));

  if (!allMatched) {
    process.exit(1);
  }
}

main();
