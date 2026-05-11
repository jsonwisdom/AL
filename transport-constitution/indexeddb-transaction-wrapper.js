import {
  prepareReceiptForStorage,
  ZERO_HASH_FOR_EMPTY_DEGRADATION_LOG
} from './canonicalizeReceipt.js';

export { ZERO_HASH_FOR_EMPTY_DEGRADATION_LOG };

export const ConfidenceLevel = {
  ABSOLUTE: 0,
  CRYPTOGRAPHIC: 1,
  ECONOMIC: 2,
  SOCIAL: 3,
  HEURISTIC: 4,
  NONE: 5
};

export const RejectionCode = {
  NONE: 0,
  REJECT_INFLATED_CONFIDENCE: 1,
  REJECT_INVALID_SOURCE_HASH: 2,
  REJECT_INVALID_ATTESTER_PROOF: 3,
  REJECT_EXPIRED_TIMESTAMP: 4,
  REJECT_CONTEXT_MISMATCH: 5,
  REJECT_DEGRADATION_NOT_DECLARED: 6,
  REJECT_NON_CANONICAL_SERIALIZATION: 7,
  REJECT_LEDGER_HASH_MISMATCH: 8,
  REJECT_EMPTY_LEDGER_CLAIM: 9
};

const DB_CONFIG = {
  name: 'TransportConstitution',
  version: 2,
  storeName: 'receipts'
};

export function openDatabase() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_CONFIG.name, DB_CONFIG.version);

    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains(DB_CONFIG.storeName)) {
        const store = db.createObjectStore(DB_CONFIG.storeName, { keyPath: 'receiptHash' });
        store.createIndex('timestamp', 'timestamp', { unique: false });
        store.createIndex('attester', 'attester', { unique: false });
        store.createIndex('sourceContext', 'sourceContext', { unique: false });
        store.createIndex('targetContext', 'targetContext', { unique: false });
        store.createIndex('degradationLogHash', 'degradationLogHash', { unique: false });
        store.createIndex('isValid', 'isValid', { unique: false });
        store.createIndex('canonicalized', 'canonicalized', { unique: false });
      }
    };

    request.onsuccess = (event) => resolve(event.target.result);
    request.onerror = (event) => reject(event.target.error);
    request.onblocked = () => reject(new Error('database blocked — close other tabs'));
  });
}

export function constitutionalValidate(preparedReceipt, rawReceipt) {
  if (rawReceipt.targetConfidenceLevel < rawReceipt.sourceConfidenceLevel) {
    return { valid: false, rejectionCode: RejectionCode.REJECT_INFLATED_CONFIDENCE, reason: 'Confidence inflated' };
  }

  if (rawReceipt.sourceContext === rawReceipt.targetContext) {
    return { valid: false, rejectionCode: RejectionCode.REJECT_CONTEXT_MISMATCH, reason: 'Source and target contexts are identical' };
  }

  if (!Object.prototype.hasOwnProperty.call(rawReceipt, 'translation_loss')) {
    return { valid: false, rejectionCode: RejectionCode.REJECT_EMPTY_LEDGER_CLAIM, reason: 'translation_loss field is required' };
  }

  if (!preparedReceipt.canonicalized) {
    return { valid: false, rejectionCode: RejectionCode.REJECT_NON_CANONICAL_SERIALIZATION, reason: 'Receipt was not canonicalized' };
  }

  if (rawReceipt.translation_loss.length === 0 && preparedReceipt.degradationLogHash !== ZERO_HASH_FOR_EMPTY_DEGRADATION_LOG) {
    return { valid: false, rejectionCode: RejectionCode.REJECT_EMPTY_LEDGER_CLAIM, reason: 'Empty ledger must use zero sentinel' };
  }

  if (rawReceipt.translation_loss.length > 0 && preparedReceipt.degradationLogHash === ZERO_HASH_FOR_EMPTY_DEGRADATION_LOG) {
    return { valid: false, rejectionCode: RejectionCode.REJECT_DEGRADATION_NOT_DECLARED, reason: 'Non-empty ledger cannot use zero sentinel' };
  }

  if (!rawReceipt.sourceHash || rawReceipt.sourceHash === '0x' + '00'.repeat(32)) {
    return { valid: false, rejectionCode: RejectionCode.REJECT_INVALID_SOURCE_HASH, reason: 'Source hash is missing or zero' };
  }

  return { valid: true, rejectionCode: RejectionCode.NONE, reason: '' };
}

export async function writeReceipt(rawReceipt, options = { failClosed: true }) {
  let prepared;
  try {
    prepared = await prepareReceiptForStorage(rawReceipt);
  } catch (error) {
    return { success: false, receiptHash: null, rejectionCode: RejectionCode.REJECT_NON_CANONICAL_SERIALIZATION, error: error.message };
  }

  const validation = constitutionalValidate(prepared, rawReceipt);
  if (!validation.valid) {
    if (!options.failClosed) await storeRejectedReceipt(prepared, rawReceipt, validation);
    return { success: false, receiptHash: prepared.receiptHash, rejectionCode: validation.rejectionCode, reason: validation.reason };
  }

  await commitReceipt(prepared, rawReceipt);
  return { success: true, receiptHash: prepared.receiptHash, rejectionCode: RejectionCode.NONE, canonicalJSON: prepared.canonicalJSON };
}

async function commitReceipt(prepared, rawReceipt) {
  const db = await openDatabase();

  return new Promise((resolve, reject) => {
    const tx = db.transaction(DB_CONFIG.storeName, 'readwrite');
    const store = tx.objectStore(DB_CONFIG.storeName);

    const record = {
      receiptHash: prepared.receiptHash,
      canonicalJSON: prepared.canonicalJSON,
      degradationLogHash: prepared.degradationLogHash,
      timestamp: rawReceipt.timestamp || Date.now(),
      attester: rawReceipt.attester || '0x0',
      sourceContext: rawReceipt.sourceContext,
      targetContext: rawReceipt.targetContext,
      sourceConfidenceLevel: rawReceipt.sourceConfidenceLevel,
      targetConfidenceLevel: rawReceipt.targetConfidenceLevel,
      isValid: 1,
      canonicalized: true,
      version: '0.2.0',
      lossCount: rawReceipt.translation_loss.length,
      byteLength: prepared.fullByteLength,
      storedAt: Date.now()
    };

    const request = store.add(record);
    request.onsuccess = () => resolve(prepared.receiptHash);
    request.onerror = (event) => {
      if (event.target.error.name === 'ConstraintError') resolve(prepared.receiptHash);
      else reject(event.target.error);
    };
    tx.oncomplete = () => db.close();
    tx.onerror = (event) => { db.close(); reject(event.target.error); };
  });
}

async function storeRejectedReceipt(prepared, rawReceipt, validation) {
  const db = await openDatabase();

  return new Promise((resolve) => {
    const tx = db.transaction(DB_CONFIG.storeName, 'readwrite');
    const store = tx.objectStore(DB_CONFIG.storeName);

    const record = {
      receiptHash: prepared.receiptHash,
      canonicalJSON: prepared.canonicalJSON,
      degradationLogHash: prepared.degradationLogHash,
      timestamp: rawReceipt.timestamp || Date.now(),
      attester: rawReceipt.attester || '0x0',
      sourceContext: rawReceipt.sourceContext,
      targetContext: rawReceipt.targetContext,
      isValid: 0,
      canonicalized: true,
      rejectionCode: validation.rejectionCode,
      rejectionReason: validation.reason,
      storedAt: Date.now()
    };

    const request = store.add(record);
    request.onsuccess = () => resolve();
    request.onerror = () => resolve();
    tx.oncomplete = () => db.close();
  });
}

export async function getReceipt(receiptHash) {
  const db = await openDatabase();

  return new Promise((resolve, reject) => {
    const tx = db.transaction(DB_CONFIG.storeName, 'readonly');
    const request = tx.objectStore(DB_CONFIG.storeName).get(receiptHash);
    request.onsuccess = () => resolve(request.result || null);
    request.onerror = (event) => reject(event.target.error);
    tx.oncomplete = () => db.close();
  });
}

export async function getReceiptStats() {
  const db = await openDatabase();

  return new Promise((resolve, reject) => {
    const tx = db.transaction(DB_CONFIG.storeName, 'readonly');
    const store = tx.objectStore(DB_CONFIG.storeName);
    const validIndex = store.index('isValid');

    const totalReq = store.count();
    const validReq = validIndex.count(IDBKeyRange.only(1));
    const rejectedReq = validIndex.count(IDBKeyRange.only(0));

    tx.oncomplete = () => {
      db.close();
      resolve({ total: totalReq.result, valid: validReq.result, rejected: rejectedReq.result });
    };
    tx.onerror = (event) => { db.close(); reject(event.target.error); };
  });
}

export async function listValidReceipts(limit = 50) {
  const db = await openDatabase();

  return new Promise((resolve, reject) => {
    const tx = db.transaction(DB_CONFIG.storeName, 'readonly');
    const index = tx.objectStore(DB_CONFIG.storeName).index('isValid');
    const results = [];
    const request = index.openCursor(IDBKeyRange.only(1));

    request.onsuccess = (event) => {
      const cursor = event.target.result;
      if (cursor && results.length < limit) {
        results.push(cursor.value);
        cursor.continue();
      } else {
        resolve(results);
      }
    };
    request.onerror = (event) => reject(event.target.error);
    tx.oncomplete = () => db.close();
  });
}
