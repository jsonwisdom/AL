#!/usr/bin/env node
const fs = require('fs');
const crypto = require('crypto');

function loadJson(path) {
  return JSON.parse(fs.readFileSync(path, 'utf8'));
}

function canonicalJson(obj) {
  // Match Python json.dumps(obj, sort_keys=True, separators=(',', ':'))
  if (obj === null || typeof obj !== 'object') {
    return JSON.stringify(obj);
  }

  if (Array.isArray(obj)) {
    return '[' + obj.map(canonicalJson).join(',') + ']';
  }

  return '{' + Object.keys(obj)
    .sort()
    .map(key => JSON.stringify(key) + ':' + canonicalJson(obj[key]))
    .join(',') + '}';
}

function receiptSigningPayload(receipt) {
  const proof = receipt.proof || {};
  const proofWithoutSignature = {};

  for (const key of Object.keys(proof)) {
    if (key !== 'signature') {
      proofWithoutSignature[key] = proof[key];
    }
  }

  return {
    ...receipt,
    proof: proofWithoutSignature
  };
}

function verifySignature(receipt) {
  try {
    const proof = receipt.proof || {};
    const sigStr = proof.signature || '';
    if (!sigStr.startsWith('ed25519:')) return false;

    const sigHex = sigStr.slice(8);
    const signature = Buffer.from(sigHex, 'hex');

    const message = Buffer.from(canonicalJson(receiptSigningPayload(receipt)), 'utf8');

    const pubKeyHex = '37e9edc1ca6c423ec0955156b9bd318e7581ef4492b28a92235ee900d53174cc';
    const pubKeyBytes = Buffer.from(pubKeyHex, 'hex');

    // Ed25519 SPKI DER prefix for raw 32-byte public key
    const spkiHeader = Buffer.from('302a300506032b6570032100', 'hex');
    const derKey = Buffer.concat([spkiHeader, pubKeyBytes]);

    const publicKey = crypto.createPublicKey({
      key: derKey,
      format: 'der',
      type: 'spki'
    });

    return crypto.verify(null, message, publicKey, signature);
  } catch (e) {
    console.error('Signature verify error:', e.message);
    return false;
  }
}

function verify(receiptPath, bindingPath, policyPath) {
  try {
    const receipt = loadJson(receiptPath);
    const binding = loadJson(bindingPath);
    const policy = loadJson(policyPath);

    // === SCHEMA ENFORCEMENT ===
    if (receipt.receipt_type !== "AGENT_DELEGATION_RECEIPT_V0") {
      return "FAIL: schema invalid - wrong receipt_type";
    }
    if (receipt.receipt_version !== "0.0.1") {
      return "FAIL: schema invalid - wrong receipt_version";
    }

    const proof = receipt.proof || {};
    if (!proof.signature) {
      return "FAIL: schema invalid - missing signature in proof";
    }

    const requiredBinding = ["receipt_digest", "observed_files", "result_hash"];
    for (const field of requiredBinding) {
      if (!(field in binding)) {
        return `FAIL: schema invalid - missing ${field} in binding`;
      }
    }

    if (!Array.isArray(policy.allowed_paths)) {
      return "FAIL: schema invalid - allowed_paths must be array";
    }
    if (!Array.isArray(policy.forbidden_paths)) {
      return "FAIL: schema invalid - forbidden_paths must be array";
    }

    // === CRYPTO + REPLAY LOGIC ===
    if (!verifySignature(receipt)) {
      return "FAIL: signature mismatch";
    }

    // Binding digest match
    if (binding.receipt_digest !== receipt.proof.digest) {
      return "FAIL: receipt digest mismatch";
    }

    // Policy enforcement
    const observed = new Set(binding.observed_files || []);
    const allowed = new Set(policy.allowed_paths || []);
    const forbidden = new Set(policy.forbidden_paths || []);

    const forbiddenHit = [...observed].find(f => forbidden.has(f));
    if (forbiddenHit) {
      return `FAIL: forbidden file touched: ${forbiddenHit}`;
    }

    const unauthorized = [...observed].find(f => !allowed.has(f));
    if (unauthorized) {
      return "FAIL: scope violation - unauthorized file touched";
    }

    return "PASS";

  } catch (e) {
    return `FAIL: error - ${e.message}`;
  }
}

if (require.main === module) {
  if (process.argv.length !== 5) {
    console.error("Usage: node verify_fixture.js <receipt.json> <binding.json> <policy.json>");
    process.exit(1);
  }

  const result = verify(process.argv[2], process.argv[3], process.argv[4]);
  console.log(result);
}

module.exports = { verify, verifySignature, canonicalJson, receiptSigningPayload };
