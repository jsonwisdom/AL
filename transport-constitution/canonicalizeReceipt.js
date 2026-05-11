import { keccak_256 } from '../node_modules/@noble/hashes/esm/sha3.js';
import { utf8ToBytes, bytesToHex } from '../node_modules/@noble/hashes/esm/utils.js';

export const ZERO_HASH_FOR_EMPTY_DEGRADATION_LOG =
  '0xc218684497e411f185d34f0d618d35706509ec25c78a0871309f3e098867a78e';

function canonicalize(value) {
  if (value === null || typeof value !== 'object') return JSON.stringify(value);
  if (Array.isArray(value)) return '[' + value.map(canonicalize).join(',') + ']';

  return '{' + Object.keys(value).sort().map((key) => {
    return JSON.stringify(key) + ':' + canonicalize(value[key]);
  }).join(',') + '}';
}

function keccakHex(text) {
  return '0x' + bytesToHex(keccak_256(utf8ToBytes(text)));
}

export function verifyDegradationLogHash(translationLoss, expectedHash) {
  const ledger = Array.isArray(translationLoss) ? translationLoss : [];
  const canonicalLedger = canonicalize(ledger);
  const hash = keccakHex(canonicalLedger);
  return hash === expectedHash;
}

export async function prepareReceiptForStorage(rawReceipt) {
  if (!rawReceipt || typeof rawReceipt !== 'object') {
    throw new Error('rawReceipt must be an object');
  }

  if (!Object.prototype.hasOwnProperty.call(rawReceipt, 'translation_loss')) {
    throw new Error('translation_loss field is required');
  }

  if (!Array.isArray(rawReceipt.translation_loss)) {
    throw new Error('translation_loss must be an array');
  }

  const degradationLogHash =
    rawReceipt.translation_loss.length === 0
      ? ZERO_HASH_FOR_EMPTY_DEGRADATION_LOG
      : keccakHex(canonicalize(rawReceipt.translation_loss));

  const receiptForHash = {
    ...rawReceipt,
    degradationLogHash,
    canonicalized: true
  };

  const canonicalJSON = canonicalize(receiptForHash);
  const receiptHash = keccakHex(canonicalJSON);

  return {
    ...receiptForHash,
    receiptHash,
    canonicalJSON,
    degradationLogHash,
    canonicalized: true,
    fullByteLength: utf8ToBytes(canonicalJSON).length
  };
}
