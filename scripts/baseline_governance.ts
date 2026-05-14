#!/usr/bin/env ts-node

import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { loadBaseline } from "../src/baselines/load_baseline.js";
import { writeDriftReceipt } from "../src/baselines/write_drift_receipt.js";
import { createHash } from "node:crypto";

function canonicalize(value: unknown): string {
  return JSON.stringify(sortCanonical(value));
}

function sortCanonical(value: unknown): unknown {
  if (Array.isArray(value)) {
    return value.map(sortCanonical);
  }
  if (value !== null && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([k, v]) => [k, sortCanonical(v)])
    );
  }
  return value;
}

function sha256(data: string): string {
  return createHash("sha256").update(data, "utf8").digest("hex");
}

interface ManifestEntry {
  runner: string;
  baselinePath: string;
  candidatePath: string;
  required: boolean;
}

interface BaselineManifest {
  schemaVersion: "baseline_manifest_v1";
  entries: ManifestEntry[];
}

function loadManifest(path: string): BaselineManifest {
  const absolute = resolve(process.cwd(), path);
  const raw = readFileSync(absolute, "utf8");
  const parsed = JSON.parse(raw);

  if (parsed.schemaVersion !== "baseline_manifest_v1") {
    throw new Error(
      `Invalid manifest schemaVersion: ${parsed.schemaVersion}`
    );
  }

  if (!Array.isArray(parsed.entries)) {
    throw new Error("Manifest missing entries[] array");
  }

  return parsed;
}

async function cmdStatus(manifestPath: string) {
  const manifest = loadManifest(manifestPath);

  console.log("Baseline Manifest Status");
  console.log("------------------------");

  for (const entry of manifest.entries) {
    const baselineAbs = resolve(process.cwd(), entry.baselinePath);
    const candidateAbs = resolve(process.cwd(), entry.candidatePath);

    const baselineExists = existsSync(baselineAbs);
    const candidateExists = existsSync(candidateAbs);

    console.log(`Runner: ${entry.runner}`);
    console.log(`  baseline:  ${baselineAbs}`);
    console.log(`  candidate: ${candidateAbs}`);
    console.log(`  required:  ${entry.required}`);
    console.log(`  baseline_exists:  ${baselineExists}`);
    console.log(`  candidate_exists: ${candidateExists}`);
    console.log("");
  }
}

async function cmdCheck(manifestPath: string) {
  const manifest = loadManifest(manifestPath);

  let driftDetected = false;

  for (const entry of manifest.entries) {
    const baselineAbs = resolve(process.cwd(), entry.baselinePath);
    const candidateAbs = resolve(process.cwd(), entry.candidatePath);

    try {
      const baseline = loadBaseline(baselineAbs);
      const candidate = loadBaseline(candidateAbs);

      const baselineCanon = canonicalize(baseline);
      const candidateCanon = canonicalize(candidate);

      const baselineHash = sha256(baselineCanon);
      const candidateHash = sha256(candidateCanon);

      if (baselineHash !== candidateHash) {
        console.error(`❌ Drift detected for runner: ${entry.runner}`);

        const receiptPath = writeDriftReceipt(
          baselineAbs,
          candidateAbs
        );

        console.error(`   Drift receipt: ${receiptPath}`);
        driftDetected = true;
      } else {
        console.log(`✓ Stable: ${entry.runner}`);
      }
    } catch (err) {
      console.error(`❌ Error checking runner ${entry.runner}:`);
      console.error(err);
      process.exit(2);
    }
  }

  if (driftDetected) {
    process.exit(1);
  }

  process.exit(0);
}

async function cmdApproveUpdate(args: string[]) {
  if (args.length < 6) {
    console.error(
      "Usage: approve-update <runner> <candidatePath> <baselinePath> --drift <receiptHash> --commit <commitHash> --reason \"text\" --reviewer \"name\""
    );
    process.exit(2);
  }

  const runner = args[0];
  const candidatePath = args[1];
  const baselinePath = args[2];

  const flags = {
    drift: "",
    commit: "",
    reason: "",
    reviewer: ""
  };

  for (let i = 3; i < args.length; i++) {
    if (args[i] === "--drift") flags.drift = args[++i];
    else if (args[i] === "--commit") flags.commit = args[++i];
    else if (args[i] === "--reason") flags.reason = args[++i];
    else if (args[i] === "--reviewer") flags.reviewer = args[++i];
  }

  if (!flags.drift || !flags.commit || !flags.reason || !flags.reviewer) {
    console.error("Missing required flags for approve-update");
    process.exit(2);
  }

  const evidence = {
    schemaVersion: "baseline_update_evidence_v1",
    runner,
    baselinePath,
    candidatePath,
    driftReceiptHash: flags.drift,
    commitHash: flags.commit,
    reasonForUpdate: flags.reason,
    reviewerSignoff: flags.reviewer,
    generatedAt: new Date().toISOString()
  };

  console.log(JSON.stringify(evidence, null, 2));
  process.exit(0);
}

async function main() {
  const [command, ...rest] = process.argv.slice(2);

  if (!command) {
    console.error("Commands: status | check | approve-update");
    process.exit(2);
  }

  if (command === "status") {
    if (rest.length !== 1) {
      console.error("Usage: status <manifestPath>");
      process.exit(2);
    }
    await cmdStatus(rest[0]);
    return;
  }

  if (command === "check") {
    if (rest.length !== 1) {
      console.error("Usage: check <manifestPath>");
      process.exit(2);
    }
    await cmdCheck(rest[0]);
    return;
  }

  if (command === "approve-update") {
    await cmdApproveUpdate(rest);
    return;
  }

  console.error(`Unknown command: ${command}`);
  process.exit(2);
}

main();
