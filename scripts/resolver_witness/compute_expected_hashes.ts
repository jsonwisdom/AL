#!/usr/bin/env node
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const STATES_DIR = path.join(ROOT, 'tests', 'resolver_witness', 'fixtures', 'expected_graph_states');

const ORDERED_FILES = [
  'convergence_001.json',
  'convergence_002_hash_mismatch.json',
  'convergence_003_revocable_parent.json',
  'convergence_004_missing_attestation.json',
  'convergence_005_schema_violation.json',
];

function sortObject(value) {
  if (Array.isArray(value)) return value.map(sortObject);
  if (value !== null && typeof value === 'object') {
    return Object.keys(value).sort().reduce((acc, key) => {
      acc[key] = sortObject(value[key]);
      return acc;
    }, {});
  }
  return value;
}

function canonicalSerialize(obj) {
  return Buffer.from(JSON.stringify(sortObject(obj)), 'utf8');
}

const registry = {};
for (const filename of ORDERED_FILES) {
  const obj = JSON.parse(fs.readFileSync(path.join(STATES_DIR, filename), 'utf8'));
  registry[obj.test_id] = crypto.createHash('sha256').update(canonicalSerialize(obj)).digest('hex');
}

console.log(JSON.stringify(sortObject(registry), null, 2));
