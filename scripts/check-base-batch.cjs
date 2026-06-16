#!/usr/bin/env node

const fs = require("fs");

const required = [
  "batch_root",
  "artifact_manifest_uri",
  "artifact_count",
  "replay_state",
  "authority",
  "verified",
  "no_fake_green"
];

const file = process.argv[2];

if (!file) {
  console.error("usage: node scripts/check-base-batch.cjs <packet.json>");
  process.exit(1);
}

const packet = JSON.parse(fs.readFileSync(file, "utf8"));

for (const k of required) {
  if (!(k in packet)) {
    console.error(`BASE_BATCH_FAIL missing=${k}`);
    process.exit(1);
  }
}

if (
  packet.batch_root === "0x0000000000000000000000000000000000000000000000000000000000000000" ||
  packet.batch_root === "" ||
  packet.batch_root === null
) {
  console.error("BASE_BATCH_FAIL batch_root_zero_or_missing");
  process.exit(1);
}

if (!String(packet.artifact_manifest_uri).startsWith("ipfs://")) {
  console.error("BASE_BATCH_FAIL manifest_not_ipfs");
  process.exit(1);
}

if (Number(packet.artifact_count) <= 0) {
  console.error("BASE_BATCH_FAIL artifact_count_zero");
  process.exit(1);
}

if (packet.no_fake_green !== true) {
  console.error("BASE_BATCH_FAIL no_fake_green_not_true");
  process.exit(1);
}

if (packet.authority !== false) {
  console.error("BASE_BATCH_FAIL authority_overstated");
  process.exit(1);
}

if (packet.verified !== false) {
  console.error("BASE_BATCH_FAIL verified_overstated");
  process.exit(1);
}

console.log("BASE_BATCH_PASS boundary_fields_ok");
process.exit(0);
