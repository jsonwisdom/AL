#!/usr/bin/env node
'use strict';

const fs = require('fs');
const crypto = require('crypto');

function fail(message) {
  console.error(`FATAL: ${message}`);
  process.exit(1);
}

function readJson(path) {
  try {
    return JSON.parse(fs.readFileSync(path, 'utf8'));
  } catch (error) {
    fail(`Unable to read JSON receipt ${path}: ${error.message}`);
  }
}

function stableStringify(value) {
  if (value === null || typeof value !== 'object') return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(stableStringify).join(',')}]`;
  return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`).join(',')}}`;
}

function sha256(value) {
  return crypto.createHash('sha256').update(value).digest('hex');
}

function verifySignature(receipt) {
  if (!receipt.signature || typeof receipt.signature !== 'string') {
    fail('Missing signature field');
  }
  if (!receipt.signature.startsWith('SHA256:')) {
    fail(`Unsupported signature format: ${receipt.signature}`);
  }

  const clone = JSON.parse(JSON.stringify(receipt));
  const provided = clone.signature.slice('SHA256:'.length);
  delete clone.signature;
  const computed = sha256(stableStringify(clone));

  if (provided !== computed) {
    fail(`Signature mismatch: expected SHA256:${computed}, got SHA256:${provided}`);
  }
}

function validateLibrarian(receipt) {
  if (!receipt.receipt_id.startsWith('LIBRARIAN-REPLAY-')) {
    fail('Librarian receipt_id must start with LIBRARIAN-REPLAY-');
  }
  if (receipt.master_runtime?.status !== 'GREEN') {
    fail('Librarian receipt must assert master_runtime.status GREEN');
  }
  if (receipt.audit_summary?.settlement_guard !== 'PASS') {
    fail('Librarian receipt must have audit_summary.settlement_guard PASS');
  }
  if (receipt.audit_summary?.drift_detected !== false) {
    fail('Librarian receipt must have audit_summary.drift_detected false');
  }
  if (receipt.audit_summary?.node_count !== 5) {
    fail(`Librarian receipt must have node_count 5, got ${receipt.audit_summary?.node_count}`);
  }
  if (!Array.isArray(receipt.nodes) || receipt.nodes.length !== 5) {
    fail(`Librarian receipt must contain exactly 5 nodes, got ${Array.isArray(receipt.nodes) ? receipt.nodes.length : 'non-array'}`);
  }
  for (const node of receipt.nodes) {
    if (!node.evidence_card_sha256 || !String(node.evidence_card_sha256).startsWith('SHA256:')) {
      fail(`Node ${node.target_id || '<unknown>'} missing evidence_card_sha256`);
    }
  }
}

function validateGauntlet(receipt) {
  if (!receipt.receipt_id.startsWith('GAUNTLET-RUN-')) {
    fail('Gauntlet receipt_id must start with GAUNTLET-RUN-');
  }
  if (receipt.workflow !== 'constitutional-gauntlet') {
    fail('Gauntlet receipt workflow must be constitutional-gauntlet');
  }
  if (receipt.verdict?.settlement_guard !== false) {
    fail('Gauntlet receipt must have verdict.settlement_guard false');
  }
  if (receipt.verdict?.green_claim !== false) {
    fail('Gauntlet receipt must have verdict.green_claim false');
  }
  if (receipt.verdict?.status !== 'RECORDED_NOT_YET_VERIFIED') {
    fail(`Gauntlet receipt must be RECORDED_NOT_YET_VERIFIED, got ${receipt.verdict?.status}`);
  }
  if (typeof receipt.verdict?.pytest_returncode !== 'number') {
    fail('Gauntlet receipt must preserve numeric verdict.pytest_returncode');
  }
  if (receipt.audit_summary?.settlement_guard === 'PASS' || receipt.master_runtime?.status === 'GREEN') {
    fail('Gauntlet receipt must not masquerade as settlement/runtime green');
  }
}

function validate(receipt) {
  if (!receipt.receipt_id || typeof receipt.receipt_id !== 'string') {
    fail('Missing receipt_id');
  }

  verifySignature(receipt);

  if (receipt.receipt_id.startsWith('LIBRARIAN-REPLAY-')) {
    validateLibrarian(receipt);
    return 'LIBRARIAN_REPLAY_VALID';
  }

  if (receipt.receipt_id.startsWith('GAUNTLET-RUN-')) {
    validateGauntlet(receipt);
    return 'GAUNTLET_RUN_VALID';
  }

  fail(`Unknown receipt taxonomy for ${receipt.receipt_id}`);
}

if (require.main === module) {
  const paths = process.argv.slice(2);
  if (paths.length === 0) {
    fail('Usage: node scripts/validate-receipt-taxonomy.cjs RECEIPT_JSON [RECEIPT_JSON...]');
  }

  for (const path of paths) {
    const receipt = readJson(path);
    const verdict = validate(receipt);
    console.log(`${path}: ${verdict}`);
  }
}

module.exports = { validate, stableStringify };
