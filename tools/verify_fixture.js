#!/usr/bin/env node
const fs = require('fs');
const crypto = require('crypto');

const V0_TEST_KEY_HEX = '37e9edc1ca6c423ec0955156b9bd318e7581ef4492b28a92235ee900d53174cc';

function loadJson(path) {
  return JSON.parse(fs.readFileSync(path, 'utf8'));
}

function canonicalJson(obj) {
  // Deterministic canonical JSON - recursive key sort, compact (matches Python)
  if (obj === null || typeof obj !== 'object') {
    return JSON.stringify(obj);
  }
  if (Array.isArray(obj)) {
    return '[' + obj.map(canonicalJson).join(',') + ']';
  }
  const sortedKeys = Object.keys(obj).sort();
  const pairs = sortedKeys.map(key => {
    return JSON.stringify(key) + ':' + canonicalJson(obj[key]);
  });
  return '{' + pairs.join(',') + '}';
}

function isHex32Bytes(value) {
  return typeof value === 'string' && /^[0-9a-fA-F]{64}$/.test(value);
}

function resolveDidKey(did) {
  // Minimal V1 DID resolver stub. Real did:key multicodec/multibase
  // decoding is intentionally deferred.
  if (typeof did !== 'string' || did.length === 0) {
    return { key: null, error: 'FAIL: did resolution failed' };
  }
  if (did.startsWith('did:key:')) {
    return { key: null, error: 'FAIL: did resolution unsupported' };
  }
  return { key: null, error: 'FAIL: did resolution unsupported' };
}

function resolvePublicKey(receipt) {
  const proof = receipt.proof || {};
  const receiptType = receipt.receipt_type;

  const publicKeyHex = proof.public_key;
  if (publicKeyHex) {
    if (publicKeyHex === 'V1_PUBLIC_KEY_HEX_PENDING') {
      return { key: null, error: 'FAIL: public key missing' };
    }
    if (!isHex32Bytes(publicKeyHex)) {
      return { key: null, error: 'FAIL: public key invalid' };
    }
    return { key: Buffer.from(publicKeyHex, 'hex'), error: null };
  }

  const did = proof.did;
  if (did) {
    if (did === 'did:key:V1_DID_KEY_PENDING') {
      return { key: null, error: 'FAIL: did resolution unsupported' };
    }
    return resolveDidKey(did);
  }

  if (receiptType === 'AGENT_DELEGATION_RECEIPT_V0') {
    return { key: Buffer.from(V0_TEST_KEY_HEX, 'hex'), error: null };
  }

  return { key: null, error: 'FAIL: public key missing' };
}

function makeEd25519PublicKey(rawPublicKeyBytes) {
  // Ed25519 SPKI DER prefix for raw 32-byte public key
  const spkiHeader = Buffer.from('302a300506032b6570032100', 'hex');
  const derKey = Buffer.concat([spkiHeader, rawPublicKeyBytes]);
  return crypto.createPublicKey({
    key: derKey,
    format: 'der',
    type: 'spki'
  });
}

function verifySignature(receipt) {
  try {
    const proof = receipt.proof || {};
    const sigStr = proof.signature || '';
    if (!sigStr.startsWith('ed25519:')) {
      return { ok: false, error: 'FAIL: signature mismatch' };
    }

    const sigHex = sigStr.slice(8);
    const signature = Buffer.from(sigHex, 'hex');

    const receiptForSigning = JSON.parse(JSON.stringify(receipt));
    receiptForSigning.proof = { ...proof };
    delete receiptForSigning.proof.signature;
    const message = Buffer.from(canonicalJson(receiptForSigning), 'utf8');

    const resolved = resolvePublicKey(receipt);
    if (resolved.error) {
      return { ok: false, error: resolved.error };
    }

    const publicKey = makeEd25519PublicKey(resolved.key);
    const valid = crypto.verify(null, message, publicKey, signature);
    if (!valid) {
      return { ok: false, error: 'FAIL: signature mismatch' };
    }
    return { ok: true, error: null };
  } catch (e) {
    if (e.message && e.message.includes('key')) {
      return { ok: false, error: 'FAIL: public key invalid' };
    }
    return { ok: false, error: 'FAIL: signature mismatch' };
  }
}

function verify(receiptPath, bindingPath, policyPath) {
  try {
    const receipt = loadJson(receiptPath);
    const binding = loadJson(bindingPath);
    const policy = loadJson(policyPath);

    const receiptType = receipt.receipt_type;
    const receiptVersion = receipt.receipt_version;

    if (!['AGENT_DELEGATION_RECEIPT_V0', 'AGENT_DELEGATION_RECEIPT_V1'].includes(receiptType)) {
      return 'FAIL: schema invalid - wrong receipt_type';
    }
    if (receiptType === 'AGENT_DELEGATION_RECEIPT_V0' && receiptVersion !== '0.0.1') {
      return 'FAIL: schema invalid - wrong receipt_version';
    }
    if (receiptType === 'AGENT_DELEGATION_RECEIPT_V1' && receiptVersion !== '1.0.0') {
      return 'FAIL: schema invalid - wrong receipt_version';
    }

    const proof = receipt.proof || {};
    if (!proof.signature) {
      return 'FAIL: schema invalid - missing signature in proof';
    }

    const requiredBinding = ['receipt_digest', 'observed_files', 'result_hash'];
    for (const field of requiredBinding) {
      if (!(field in binding)) {
        return `FAIL: schema invalid - missing ${field} in binding`;
      }
    }

    if (!Array.isArray(policy.allowed_paths)) {
      return 'FAIL: schema invalid - allowed_paths must be array';
    }
    if (!Array.isArray(policy.forbidden_paths)) {
      return 'FAIL: schema invalid - forbidden_paths must be array';
    }

    const sig = verifySignature(receipt);
    if (!sig.ok) {
      return sig.error;
    }

    if (binding.receipt_digest !== proof.digest) {
      return 'FAIL: receipt digest mismatch';
    }

    const observed = new Set(binding.observed_files || []);
    const allowed = new Set(policy.allowed_paths || []);
    const forbidden = new Set(policy.forbidden_paths || []);

    const forbiddenHit = [...observed].find(f => forbidden.has(f));
    if (forbiddenHit) {
      return `FAIL: forbidden file touched: ${forbiddenHit}`;
    }

    const unauthorized = [...observed].find(f => !allowed.has(f));
    if (unauthorized) {
      return 'FAIL: scope violation - unauthorized file touched';
    }

    return 'PASS';
  } catch (e) {
    return `FAIL: error - ${e.message}`;
  }
}

if (require.main === module) {
  if (process.argv.length !== 5) {
    console.error('Usage: node verify_fixture.js <receipt.json> <binding.json> <policy.json>');
    process.exit(1);
  }

  const result = verify(process.argv[2], process.argv[3], process.argv[4]);
  console.log(result);
}

module.exports = { verify, verifySignature, canonicalJson, resolvePublicKey, resolveDidKey };
