#!/usr/bin/env node
'use strict';

const fs = require('fs');
const crypto = require('crypto');
const { validate, canonicalBytes } = require('./validate-receipt-taxonomy.cjs');

const MANIFEST_PATH = 'test/fixtures/receipt-taxonomy-golden-manifest.json';

function fail(message) {
  console.error(`FATAL: ${message}`);
  process.exit(1);
}

function readJson(path) {
  return JSON.parse(fs.readFileSync(path, 'utf8'));
}

function signatureDigest(receipt) {
  const clone = JSON.parse(JSON.stringify(receipt));
  delete clone.signature;
  return crypto.createHash('sha256').update(canonicalBytes(clone)).digest('hex');
}

const manifest = readJson(MANIFEST_PATH);
const librarian = manifest.golden_receipts.LIBRARIAN;
const gauntlet = manifest.golden_receipts.GAUNTLET;

const librarianReceipt = readJson(librarian.path);
const gauntletReceipt = readJson(gauntlet.path);

const librarianVerdict = validate(librarianReceipt);
const gauntletVerdict = validate(gauntletReceipt);

if (librarianVerdict !== 'LIBRARIAN_REPLAY_VALID') {
  fail(`Unexpected librarian validator result: ${librarianVerdict}`);
}
if (gauntletVerdict !== 'GAUNTLET_RUN_VALID') {
  fail(`Unexpected gauntlet validator result: ${gauntletVerdict}`);
}

if (signatureDigest(librarianReceipt) !== librarian.signature) {
  fail('Librarian golden signature mismatch');
}
if (signatureDigest(gauntletReceipt) !== gauntlet.signature) {
  fail('Gauntlet golden signature mismatch');
}

if (librarianReceipt.master_runtime?.status !== 'GREEN' || librarianReceipt.audit_summary?.settlement_guard !== 'PASS') {
  fail('Librarian golden receipt is not authorized operational green');
}
if (gauntletReceipt.verdict?.green_claim !== false || gauntletReceipt.verdict?.settlement_guard !== false) {
  fail('Gauntlet golden receipt attempted to claim operational green');
}
if (gauntletReceipt.verdict?.status !== 'RECORDED_NOT_YET_VERIFIED') {
  fail('Gauntlet golden receipt status drifted');
}

console.log('GOLDEN_RECEIPT_TAXONOMY_PASS');
console.log(`LIBRARIAN=${librarianVerdict}`);
console.log(`GAUNTLET=${gauntletVerdict}`);
