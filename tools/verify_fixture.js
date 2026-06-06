#!/usr/bin/env node
// Minimal V0 replay verifier for AGENT_DELEGATION_RECEIPT_V0 fixtures.
// This V0 verifier intentionally uses MOCK proof values. It is a deterministic
// stranger-replay harness, not production cryptography.

const fs = require('fs');

const SKEW_SECONDS = 300;
const VALID_PROOF = 'mock-valid-signature';
const VALID_BINDING_PROOF = 'mock-valid-proof';

function fail(message) {
  console.log(`FAIL: ${message}`);
  process.exit(1);
}

function loadJson(path) {
  try {
    return JSON.parse(fs.readFileSync(path, 'utf8'));
  } catch (err) {
    fail(`invalid json: ${path}: ${err.message}`);
  }
}

function parseTime(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    fail('invalid expiration');
  }
  return date;
}

function requirePath(obj, path, label) {
  let cur = obj;
  for (const part of path) {
    if (!cur || !(part in cur)) {
      fail(`schema invalid - missing ${label}`);
    }
    cur = cur[part];
  }
  return cur;
}

function main() {
  const args = process.argv.slice(2);
  if (args.length !== 3) {
    console.log('usage: verify_fixture.js <receipt.json> <binding.json> <policy.json>');
    process.exit(2);
  }

  const receipt = loadJson(args[0]);
  const binding = loadJson(args[1]);
  const policy = loadJson(args[2]);

  if (receipt.receipt_type !== 'AGENT_DELEGATION_RECEIPT_V0') fail('invalid receipt type');
  if (binding.binding_type !== 'AGENT_RESULT_BINDING_V0') fail('invalid binding type');

  const expiresAtRaw = requirePath(receipt, ['scope', 'expires_at'], 'scope.expires_at');
  const signature = requirePath(receipt, ['proof', 'signature'], 'signature in receipt');
  const digest = requirePath(receipt, ['proof', 'digest'], 'digest in receipt');
  const bindingDigest = requirePath(binding, ['receipt_digest'], 'receipt digest in binding');
  const bindingProof = requirePath(binding, ['proof', 'value'], 'binding proof');

  const allowedPaths = policy.allowed_paths;
  const forbiddenPaths = policy.forbidden_paths;
  if (!Array.isArray(allowedPaths)) fail('schema invalid - policy allowed_paths must be array');
  if (!Array.isArray(forbiddenPaths)) fail('schema invalid - policy forbidden_paths must be array');

  const expiresAt = parseTime(expiresAtRaw);
  const now = new Date();
  if (now.getTime() > expiresAt.getTime() + SKEW_SECONDS * 1000) fail('receipt expired');

  if (signature !== VALID_PROOF) fail('signature mismatch');
  if (bindingDigest !== digest) fail('receipt digest mismatch');
  if (bindingProof !== VALID_BINDING_PROOF) fail('binding proof mismatch');

  const changedFiles = (binding.result && binding.result.changed_files) || [];
  for (const file of changedFiles) {
    if (forbiddenPaths.includes(file)) fail(`forbidden file touched: ${file}`);
    if (allowedPaths.length > 0 && !allowedPaths.includes(file)) fail(`file outside allowed paths: ${file}`);
  }

  console.log('PASS');
}

main();
