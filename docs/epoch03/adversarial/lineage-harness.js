import { initEpoch03Engine } from "../engine.js";

const SURFACES = {
  doctrine: "../schema/epoch03.doctrine.json",
  fsm: "../schema/epoch03.fsm.json",
  receipt: "../schema/epoch03.receipt.json",
  taxonomy: "../constitutional-commons/adversarial.taxonomy.json"
};

async function loadJson(path) {
  const res = await fetch(path, { cache: "no-store" });
  if (!res.ok) throw new Error(`failed to load ${path}`);
  return res.json();
}

function tainted(code, message, extra = {}) {
  return { status: "TAINTED", code, message, ...extra };
}

function intact(extra = {}) {
  return { status: "INTACT", code: "OK", message: "Lineage surfaces recomputed and intact.", ...extra };
}

function requireRepoSurface(value, label) {
  if (!value || typeof value !== "object") {
    throw new Error(`${label} missing canonical repo surface`);
  }
}

export async function verifyEpoch03Lineage() {
  const engine = await initEpoch03Engine();
  const [doctrine, fsm, receipt, taxonomy] = await Promise.all([
    loadJson(SURFACES.doctrine),
    loadJson(SURFACES.fsm),
    loadJson(SURFACES.receipt),
    loadJson(SURFACES.taxonomy)
  ]);

  requireRepoSurface(doctrine, "doctrine");
  requireRepoSurface(fsm, "fsm");
  requireRepoSurface(receipt, "receipt");
  requireRepoSurface(taxonomy, "taxonomy");

  const doctrineHash = await engine.hashDoctrine(doctrine);
  const fsmHash = await engine.hashFsm(fsm);
  const receiptHash = await engine.sha256Hex(receipt);

  const declaredDoctrine = receipt.leaves && receipt.leaves.doctrine_hash;
  const declaredFsm = receipt.leaves && receipt.leaves.fsm_hash;

  if (declaredDoctrine && declaredDoctrine !== "TODO" && declaredDoctrine !== doctrineHash) {
    return tainted("TAINTED_LINEAGE_SURFACE_MISMATCH", "Doctrine hash does not match receipt lineage.", { doctrineHash, declaredDoctrine });
  }

  if (declaredFsm && declaredFsm !== "TODO" && declaredFsm !== fsmHash) {
    return tainted("TAINTED_LINEAGE_SURFACE_MISMATCH", "FSM hash does not match receipt lineage.", { fsmHash, declaredFsm });
  }

  if (receipt.validator_version && receipt.validator_version !== engine.validator_version) {
    return tainted("TAINTED_VALIDATOR_DRIFT", "Validator version does not match receipt lineage.", {
      expected: receipt.validator_version,
      actual: engine.validator_version
    });
  }

  const taxonomyClasses = Array.isArray(taxonomy.classes) ? taxonomy.classes : [];
  const classIds = new Set(taxonomyClasses.map((item) => item.id));

  return intact({
    engine_mode: engine.mode,
    validator_version: engine.validator_version,
    doctrine_hash: doctrineHash,
    fsm_hash: fsmHash,
    receipt_hash: receiptHash,
    taxonomy_classes: classIds.size,
    receipt_root: receipt.root || "TODO",
    lineage_id: receipt.receipt_id || "epoch03-render-receipt-v0.1.0"
  });
}

export async function computeLineageBadge() {
  try {
    const result = await verifyEpoch03Lineage();
    if (result.status !== "INTACT") return result;
    return {
      ...result,
      badge: `HOSTILE TO DRIFT — LINEAGE INTACT · ${result.taxonomy_classes}/10 classes registered · receipt_root=${result.receipt_root}`
    };
  } catch (error) {
    return tainted("LINEAGE_HARNESS_ERROR", error.message);
  }
}

window.epoch03LineageHarness = { verifyEpoch03Lineage, computeLineageBadge };
