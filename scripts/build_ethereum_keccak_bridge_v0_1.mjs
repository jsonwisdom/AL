#!/usr/bin/env node
// SPDX-License-Identifier: MIT
// Ethereum Keccak Bridge Builder v0.1
//
// Maps the ALMS replay lane into an EVM-verifiable keccak256 digest.
// This script does not replace the source SHA3-256 bridge hash and does not
// modify the ALMS replay result. It emits a separate bridge manifest.

import fs from "fs";
import { keccak256, toUtf8Bytes } from "ethers";

const OUTPUT = "vectors/ethereum_keccak_bridge_manifest_v0_1.json";
const DOMAIN_SEPARATOR = "ALMS_TO_EVM_BRIDGE_V0_1";

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

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

const source = {
  operator_root: "jaywisdom.eth",
  operator_alias: "jaywisdom.base.eth",
  project: "PRESS_YOUR_LUCK_WITH_JAY",
  source_verifier: "ALMS_CROSS_ROUND_REPLAY_VERIFIER_V0_1",
  source_result_commit_sha: "0a16480220fceb1b29a2e240ab569e15ebea5a39",
  source_result_file_sha256: "27b0c7d0a1e18c3012494c5e4c758d6fa1bea819729f55876905abfec51e59ca",
  source_attestation_uid: "0x499544987781f0797a6f3afa88108485e47fd3f3981ef52a71d5814514a07b4a",
  source_attestation_tx: "0x677f8d1593eb0035784f05c37176b495708b37d75c9c9e19fc58ee5e37e0cfaf",
  source_schema_uid: "0x42670c7e031397a449248671b47902c1fbd887b19e4f9db2587c5732b71be5e2",
  source_schema_id: 1574,
  source_result: "PASS",
  source_hash_domain: "SHA3_256_NOT_ETHEREUM_KECCAK256",
  source_sha256_replay_hash: "0xf72d4c0460572c8cc3ac3f9cc7ac9d674d635d1f06b085fc2e2c8a31accbefa7",
  source_sha3_256_bridge_hash: "0x980edb5f9e5a03d77c595cd1d8f5d31eaecf9918cd562c222377cbe8608c9260"
};

const preimageObject = {
  domain_separator: DOMAIN_SEPARATOR,
  manifest_name: "ETHEREUM_KECCAK_BRIDGE_MANIFEST_V0_1",
  manifest_version: "0.1",
  source_attestation_uid: source.source_attestation_uid,
  source_hash_domain: source.source_hash_domain,
  source_sha256_replay_hash: source.source_sha256_replay_hash,
  source_sha3_256_bridge_hash: source.source_sha3_256_bridge_hash,
  source_verifier: source.source_verifier,
  target_hash_domain: "ETHEREUM_KECCAK256"
};

const preimage = canonicalJson(preimageObject);
const ethereumKeccak256 = keccak256(toUtf8Bytes(preimage));

const manifest = {
  manifest_name: "ETHEREUM_KECCAK_BRIDGE_MANIFEST_V0_1",
  manifest_version: "0.1",
  operator_root: source.operator_root,
  operator_alias: source.operator_alias,
  project: source.project,
  source_verifier: source.source_verifier,
  source_result_commit_sha: source.source_result_commit_sha,
  source_result_file_sha256: source.source_result_file_sha256,
  source_attestation_uid: source.source_attestation_uid,
  source_attestation_tx: source.source_attestation_tx,
  source_schema_uid: source.source_schema_uid,
  source_schema_id: source.source_schema_id,
  source_result: source.source_result,
  source_hash_domain: source.source_hash_domain,
  source_sha256_replay_hash: source.source_sha256_replay_hash,
  source_sha3_256_bridge_hash: source.source_sha3_256_bridge_hash,
  target_hash_domain: "ETHEREUM_KECCAK256",
  bridge_input: {
    domain_separator: DOMAIN_SEPARATOR,
    encoding: "UTF8_CANONICAL_JSON",
    preimage
  },
  ethereum_keccak256: ethereumKeccak256,
  invariants: {
    non_equivalence_asserted: true,
    source_domain_preserved: true,
    evm_verifiable: true,
    doj_receipt_chain_separate_lane: true
  }
};

assert(manifest.source_hash_domain === "SHA3_256_NOT_ETHEREUM_KECCAK256", "source hash domain must remain SHA3_256_NOT_ETHEREUM_KECCAK256");
assert(manifest.target_hash_domain === "ETHEREUM_KECCAK256", "target hash domain must be ETHEREUM_KECCAK256");
assert(manifest.bridge_input.domain_separator === DOMAIN_SEPARATOR, "bridge domain separator mismatch");
assert(manifest.source_sha3_256_bridge_hash !== manifest.ethereum_keccak256, "source SHA3-256 bridge hash must not equal Ethereum keccak256");
assert(manifest.invariants.doj_receipt_chain_separate_lane === true, "DOJ receipt chain must remain a separate lane");

fs.writeFileSync(OUTPUT, JSON.stringify(manifest, null, 2) + "\n");
console.log(JSON.stringify(manifest, null, 2));
