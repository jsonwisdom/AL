#!/usr/bin/env node
/*
Poster 3 Recursive Canonical JSON Replay Engine

Rules:
- Object keys sorted recursively at every depth
- Array order preserved
- JSON.stringify output with no whitespace
- UTF-8 bytes

This matches the current Poster 3 lane. Do not silently switch this receipt to another canonicalization rule.
*/

const fs = require('fs');
const crypto = require('crypto');

function canonicalize(value) {
  if (Array.isArray(value)) {
    return value.map(canonicalize);
  }
  if (value !== null && typeof value === 'object') {
    return Object.keys(value)
      .sort()
      .reduce((acc, key) => {
        acc[key] = canonicalize(value[key]);
        return acc;
      }, {});
  }
  return value;
}

function canonicalJSON(obj) {
  return JSON.stringify(canonicalize(obj));
}

function sha256Hex(s) {
  return '0x' + crypto.createHash('sha256').update(Buffer.from(s, 'utf8')).digest('hex');
}

function main() {
  const path = process.argv[2] || 'receipts/poster3/canonical_settlement_poster3_testnet.final.json';
  const expected = process.argv[3] || '0xcd45ea74afe9a545d971de87a1710ab3e3db0535d028dd09a9b55c23e4c28193';
  const obj = JSON.parse(fs.readFileSync(path, 'utf8'));
  const canonical = canonicalJSON(obj);
  const actual = sha256Hex(canonical);

  console.log(`path: ${path}`);
  console.log(`expected_sha256: ${expected}`);
  console.log(`actual_sha256:   ${actual}`);
  console.log(actual.toLowerCase() === expected.toLowerCase() ? 'RESULT: PASS' : 'RESULT: FAIL');
}

if (require.main === module) main();

module.exports = { canonicalize, canonicalJSON, sha256Hex };
